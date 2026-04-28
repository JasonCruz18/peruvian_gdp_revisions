"""
OCR Engine Module

Tesseract OCR execution with confidence scoring and post-processing.
Handles common OCR errors and extracts tabular text.

Author: Jason Cruz
Institution: Universidad del Pacífico - CIUP
Date: January 2026
"""

import re
import numpy as np
import pytesseract
from typing import Tuple, Dict, Optional
import logging

logger = logging.getLogger(__name__)


class TesseractNotConfiguredError(Exception):
    """Raised when Tesseract is not properly installed or configured."""

    pass


def check_tesseract_installation() -> None:
    """
    Verify Tesseract OCR is installed and accessible.

    Raises:
        TesseractNotConfiguredError: If Tesseract is not found
    """
    try:
        version = pytesseract.get_tesseract_version()
        logger.info(f"Tesseract version: {version}")
    except pytesseract.TesseractNotFoundError:
        raise TesseractNotConfiguredError(
            "Tesseract OCR not found. Please install Tesseract and add to PATH.\n"
            "Download from: https://github.com/UB-Mannheim/tesseract/wiki"
        )


def check_tesseract_languages(required_langs: list = ["spa", "eng"]) -> None:
    """
    Verify required language packs are installed.

    Args:
        required_langs: List of required language codes

    Raises:
        TesseractNotConfiguredError: If required languages are missing
    """
    try:
        available_langs = pytesseract.get_languages()
        missing_langs = [lang for lang in required_langs if lang not in available_langs]

        if missing_langs:
            raise TesseractNotConfiguredError(
                f"Missing Tesseract language packs: {missing_langs}\n"
                f"Available: {available_langs}\n"
                f"Install Spanish and English language data."
            )

        logger.info(f"Tesseract languages available: {', '.join(required_langs)}")

    except Exception as e:
        logger.error(f"Language check failed: {e}")
        raise


def run_tesseract_ocr(
    image: np.ndarray,
    language: str = "spa+eng",
    psm: int = 6,
    oem: int = 3,
    config: Optional[str] = None,
) -> Tuple[str, float]:
    """
    Execute Tesseract OCR on preprocessed image.

    Args:
        image: Preprocessed binary image
        language: Language(s) for OCR (e.g., "spa+eng")
        psm: Page segmentation mode (6 = uniform block of text)
        oem: OCR Engine Mode (3 = Default/LSTM + Legacy)
        config: Additional Tesseract config string

    Returns:
        Tuple of (ocr_text, confidence_score)

    Raises:
        TesseractNotConfiguredError: If Tesseract fails
    """
    if config is None:
        config = f"--psm {psm} --oem {oem}"

    try:
        # Run OCR
        logger.debug(f"Running Tesseract: lang={language}, psm={psm}, oem={oem}")

        ocr_text = pytesseract.image_to_string(image, lang=language, config=config)

        # Get detailed data with confidence scores
        ocr_data = pytesseract.image_to_data(
            image, lang=language, config=config, output_type=pytesseract.Output.DICT
        )

        # Calculate average confidence
        confidences = [
            float(conf)
            for conf in ocr_data["conf"]
            if conf != "-1"  # -1 indicates no confidence (empty block)
        ]

        if confidences:
            avg_confidence = sum(confidences) / len(confidences) / 100.0  # Normalize to 0-1
        else:
            avg_confidence = 0.0
            logger.warning("No confidence scores available")

        logger.info(f"OCR complete: {len(ocr_text)} chars, {avg_confidence:.1%} confidence")

        return ocr_text, avg_confidence

    except pytesseract.TesseractError as e:
        logger.error(f"Tesseract OCR failed: {e}")
        raise TesseractNotConfiguredError(f"Tesseract execution failed: {e}")


def post_process_ocr_text(raw_text: str) -> str:
    """
    Post-process OCR output to fix common recognition errors.

    Common errors in numeric tables:
    - O (letter) → 0 (zero)
    - l (lowercase L) → 1 (one)
    - S (letter) → 5 (five) in numeric context
    - B (letter) → 8 (eight) in numeric context
    - Remove stray characters: |, }, {, etc.

    Args:
        raw_text: Raw OCR output

    Returns:
        Cleaned OCR text
    """
    text = raw_text

    # Fix common digit misrecognitions in numeric contexts
    # Pattern: digit-O-digit → digit-0-digit
    text = re.sub(r"(\d)O(\d)", r"\g<1>0\g<2>", text)
    text = re.sub(r"(\d)O(\s)", r"\g<1>0\g<2>", text)
    text = re.sub(r"(\s)O(\d)", r"\g<1>0\g<2>", text)

    # Pattern: digit-l-digit → digit-1-digit
    text = re.sub(r"(\d)l(\d)", r"\g<1>1\g<2>", text)
    text = re.sub(r"(\d)l(\s)", r"\g<1>1\g<2>", text)

    # Pattern: digit-S → digit-5 (less confident, only at end)
    text = re.sub(r"(\d)S(\s)", r"\g<1>5\g<2>", text)

    # Remove common stray characters from table borders
    stray_chars = ["|", "}", "{", "~", "`", "^"]
    for char in stray_chars:
        text = text.replace(char, "")

    # Fix decimal separators (comma → period in Spanish numeric context)
    # Pattern: digit,digit → digit.digit
    text = re.sub(r"(\d),(\d)", r"\g<1>.\g<2>", text)

    # Normalize whitespace
    text = re.sub(r"[ \t]+", " ", text)  # Multiple spaces → single space
    text = re.sub(r"\n\s+\n", "\n\n", text)  # Multiple blank lines → double newline

    # Remove leading/trailing whitespace from lines
    lines = [line.strip() for line in text.split("\n")]
    text = "\n".join(lines)

    logger.debug("Applied post-processing corrections")
    return text


def extract_confidence_scores(ocr_data: Dict) -> Dict[str, float]:
    """
    Extract word-level confidence scores from Tesseract output.

    Useful for identifying problematic regions.

    Args:
        ocr_data: Tesseract output dictionary (from image_to_data)

    Returns:
        Dictionary mapping words to confidence scores
    """
    word_confidences = {}

    for i, word in enumerate(ocr_data["text"]):
        if word.strip():  # Non-empty word
            conf = ocr_data["conf"][i]
            if conf != "-1":
                word_confidences[word] = float(conf) / 100.0

    return word_confidences


def identify_low_confidence_words(ocr_data: Dict, threshold: float = 0.70) -> list:
    """
    Identify words with confidence below threshold.

    Args:
        ocr_data: Tesseract output dictionary
        threshold: Confidence threshold (0-1)

    Returns:
        List of (word, confidence) tuples for low-confidence words
    """
    low_confidence = []

    for i, word in enumerate(ocr_data["text"]):
        if word.strip():
            conf = ocr_data["conf"][i]
            if conf != "-1":
                confidence = float(conf) / 100.0
                if confidence < threshold:
                    low_confidence.append((word, confidence))

    if low_confidence:
        logger.warning(f"Found {len(low_confidence)} low-confidence words")

    return low_confidence


def run_ocr_with_validation(
    image: np.ndarray, language: str = "spa+eng", psm: int = 6, oem: int = 3
) -> Dict[str, any]:
    """
    Run OCR with comprehensive validation and metadata extraction.

    Args:
        image: Preprocessed image
        language: Language(s) for OCR
        psm: Page segmentation mode
        oem: OCR Engine Mode

    Returns:
        Dictionary containing:
            - text: OCR output text
            - text_cleaned: Post-processed text
            - confidence: Average confidence score
            - word_count: Number of words recognized
            - low_confidence_words: List of problematic words
            - metadata: Additional OCR metadata
    """
    # Run OCR
    raw_text, confidence = run_tesseract_ocr(image, language, psm, oem)

    # Post-process
    cleaned_text = post_process_ocr_text(raw_text)

    # Get detailed data
    config = f"--psm {psm} --oem {oem}"
    ocr_data = pytesseract.image_to_data(
        image, lang=language, config=config, output_type=pytesseract.Output.DICT
    )

    # Extract metadata
    word_confidences = extract_confidence_scores(ocr_data)
    low_conf_words = identify_low_confidence_words(ocr_data, threshold=0.70)

    result = {
        "text": raw_text,
        "text_cleaned": cleaned_text,
        "confidence": confidence,
        "word_count": len([w for w in ocr_data["text"] if w.strip()]),
        "low_confidence_words": low_conf_words,
        "metadata": {
            "language": language,
            "psm": psm,
            "oem": oem,
            "word_confidences": word_confidences,
        },
    }

    logger.info(
        f"OCR validation complete: {result['word_count']} words, "
        f"{len(low_conf_words)} low-confidence"
    )

    return result


if __name__ == "__main__":
    # Test OCR engine
    import sys
    import cv2
    from pathlib import Path

    logging.basicConfig(
        level=logging.DEBUG, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    # Check Tesseract installation
    try:
        check_tesseract_installation()
        check_tesseract_languages(["spa", "eng"])
        print("✓ Tesseract is properly configured\n")
    except TesseractNotConfiguredError as e:
        print(f"✗ Tesseract configuration error:\n{e}")
        sys.exit(1)

    if len(sys.argv) < 2:
        print("Usage: python ocr_engine.py <image_path>")
        print("  image_path: Preprocessed binary image of table")
        sys.exit(1)

    image_path = sys.argv[1]

    # Load image
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    if image is None:
        print(f"✗ Failed to load image: {image_path}")
        sys.exit(1)

    print(f"Loaded image: {image.shape}\n")

    # Run OCR with validation
    result = run_ocr_with_validation(image, language="spa+eng", psm=6, oem=3)

    print(f"OCR Results:")
    print(f"  Confidence: {result['confidence']:.1%}")
    print(f"  Word count: {result['word_count']}")
    print(f"  Low-confidence words: {len(result['low_confidence_words'])}")

    if result["low_confidence_words"]:
        print(f"\n  Problematic words:")
        for word, conf in result["low_confidence_words"][:10]:  # Show first 10
            print(f"    '{word}': {conf:.1%}")

    print(f"\nOCR Text (first 500 chars):")
    print("-" * 60)
    print(result["text_cleaned"][:500])
    print("-" * 60)

    # Save result
    output_dir = Path("OCR/temp_images/test")
    output_dir.mkdir(parents=True, exist_ok=True)

    with open(output_dir / "ocr_output.txt", "w", encoding="utf-8") as f:
        f.write(result["text_cleaned"])

    print(f"\n✓ Full OCR output saved to: {output_dir}/ocr_output.txt")
