"""
Validator Module

Quality checks and manual review flagging for OCR outputs.
Validates CSV structure, content, and confidence scores.

Author: Jason Cruz
Institution: Universidad del Pacífico - CIUP
Date: January 2026
"""

import pandas as pd
import shutil
from pathlib import Path
from typing import List, Dict, Tuple
import logging

logger = logging.getLogger(__name__)


def validate_csv_structure(
    df: pd.DataFrame,
    table_type: str = "table_1"
) -> List[str]:
    """
    Validate CSV structure against expected format.

    Args:
        df: DataFrame to validate
        table_type: "table_1" (monthly) or "table_2" (quarterly)

    Returns:
        List of validation errors (empty if valid)
    """
    errors = []

    # Check 1: Must have at least 3 columns (Spanish sectors, English sectors, + data)
    if len(df.columns) < 3:
        errors.append(f"Too few columns: {len(df.columns)} < 3")
        return errors  # Critical error, stop validation

    # Check 2: First two columns must be sector names
    if df.columns[0] != 'sectores_economicos':
        errors.append(f"First column should be 'sectores_economicos', got '{df.columns[0]}'")

    if df.columns[1] != 'economic_sectors':
        errors.append(f"Second column should be 'economic_sectors', got '{df.columns[1]}'")

    # Check 3: Minimum number of rows (sectors)
    if len(df) < 8:
        errors.append(f"Too few sectors: {len(df)} < 8")

    # Check 4: Expected sectors present
    required_sectors_es = ['agropecuario', 'pesca', 'manufactura', 'construccion', 'pbi']
    required_sectors_en = ['agriculture', 'fishing', 'manufacturing', 'construction', 'gdp']

    if 'sectores_economicos' in df.columns:
        sectors_es = df['sectores_economicos'].str.lower().tolist()
        for sector in required_sectors_es:
            if not any(sector in s for s in sectors_es):
                errors.append(f"Missing Spanish sector: {sector}")

    if 'economic_sectors' in df.columns:
        sectors_en = df['economic_sectors'].str.lower().tolist()
        for sector in required_sectors_en:
            if not any(sector in s for s in sectors_en):
                errors.append(f"Missing English sector: {sector}")

    # Check 5: Numeric columns parse correctly
    numeric_cols = df.columns[2:]
    for col in numeric_cols:
        if not pd.api.types.is_numeric_dtype(df[col]):
            errors.append(f"Column '{col}' is not numeric")

    # Check 6: Reasonable value ranges (-100% to +500%)
    numeric_data = df.iloc[:, 2:].select_dtypes(include='number')
    if (numeric_data > 500).any().any():
        errors.append("Unrealistic values > 500% detected")

    if (numeric_data < -100).any().any():
        errors.append("Unrealistic values < -100% detected")

    # Check 7: Column count appropriate for table type
    if table_type == "table_1":
        # Monthly: expect 15-30 columns (2 sector cols + 12-24 months + mean)
        if not (15 <= len(df.columns) <= 35):
            errors.append(
                f"Unexpected column count for monthly table: {len(df.columns)} "
                f"(expected 15-35)"
            )

    elif table_type == "table_2":
        # Quarterly: expect 8-20 columns (2 sector cols + 4-16 quarters + year)
        if not (8 <= len(df.columns) <= 25):
            errors.append(
                f"Unexpected column count for quarterly table: {len(df.columns)} "
                f"(expected 8-25)"
            )

    # Check 8: No completely empty rows
    if df.isnull().all(axis=1).any():
        empty_rows = df.isnull().all(axis=1).sum()
        errors.append(f"{empty_rows} completely empty row(s) found")

    if errors:
        logger.warning(f"Validation failed: {len(errors)} error(s)")
    else:
        logger.info("Validation passed")

    return errors


def calculate_confidence_score(
    df: pd.DataFrame,
    ocr_confidence: float,
    validation_errors: List[str]
) -> float:
    """
    Calculate combined confidence score.

    Combines OCR confidence with validation results.

    Args:
        df: Converted DataFrame
        ocr_confidence: OCR confidence score (0-1)
        validation_errors: List of validation errors

    Returns:
        Combined confidence score (0-1)
    """
    # Start with OCR confidence
    confidence = ocr_confidence

    # Penalize for validation errors
    error_penalty = min(0.05 * len(validation_errors), 0.3)  # Max 30% penalty
    confidence -= error_penalty

    # Penalize for missing values
    missing_ratio = df.isnull().sum().sum() / df.size
    if missing_ratio > 0.1:  # More than 10% missing
        confidence -= 0.1

    # Bonus for having all expected sectors
    expected_sectors = ['agropecuario', 'pesca', 'mineria', 'manufactura',
                       'construccion', 'comercio', 'pbi']
    if 'sectores_economicos' in df.columns:
        sectors = df['sectores_economicos'].str.lower().tolist()
        found_sectors = sum(1 for exp in expected_sectors if any(exp in s for s in sectors))
        sector_completeness = found_sectors / len(expected_sectors)
        if sector_completeness >= 0.9:
            confidence += 0.05  # 5% bonus for completeness

    # Clamp to [0, 1]
    confidence = max(0.0, min(1.0, confidence))

    logger.debug(f"Confidence score: {confidence:.2%} (OCR: {ocr_confidence:.2%}, "
                f"errors: {len(validation_errors)}, missing: {missing_ratio:.1%})")

    return confidence


def flag_for_manual_review(
    pdf_path: str,
    csv_path: str,
    preprocessed_image_path: str,
    confidence: float,
    issues: List[str],
    review_dir: str = "OCR/review"
) -> None:
    """
    Create review package for low-confidence output.

    Args:
        pdf_path: Original PDF file
        csv_path: OCR-generated CSV file
        preprocessed_image_path: Preprocessed image
        confidence: Confidence score
        issues: List of detected issues
        review_dir: Base directory for review packages
    """
    pdf_file = Path(pdf_path)
    csv_file = Path(csv_path)
    image_file = Path(preprocessed_image_path)

    # Create review subdirectory
    # Structure: review_dir/YYYY/ns-XX-YYYY/
    year = pdf_file.stem.split('_')[-1]  # Extract year from filename
    review_subdir = Path(review_dir) / year / pdf_file.stem
    review_subdir.mkdir(parents=True, exist_ok=True)

    # Copy original PDF
    if pdf_file.exists():
        shutil.copy(pdf_file, review_subdir / "original.pdf")

    # Copy preprocessed image
    if image_file.exists():
        shutil.copy(image_file, review_subdir / "preprocessed.png")

    # Copy OCR output CSV
    if csv_file.exists():
        shutil.copy(csv_file, review_subdir / "ocr_output.csv")

    # Generate issues report
    issues_file = review_subdir / "issues.txt"
    with open(issues_file, 'w', encoding='utf-8') as f:
        f.write(f"OCR Review Required\n")
        f.write(f"=" * 60 + "\n\n")
        f.write(f"PDF: {pdf_file.name}\n")
        f.write(f"Confidence: {confidence:.1%}\n")
        f.write(f"Status: NEEDS MANUAL VERIFICATION\n\n")

        f.write(f"Issues Detected ({len(issues)}):\n")
        f.write("-" * 60 + "\n")
        for i, issue in enumerate(issues, 1):
            f.write(f"{i}. {issue}\n")

        f.write("\n" + "=" * 60 + "\n")
        f.write("Manual Correction Instructions:\n")
        f.write("=" * 60 + "\n")
        f.write("1. Open 'original.pdf' to view the source document\n")
        f.write("2. Compare with 'ocr_output.csv' to identify errors\n")
        f.write("3. Correct errors in 'ocr_output.csv'\n")
        f.write("4. Save corrected version to:\n")
        f.write(f"   {csv_file.relative_to(Path.cwd())}\n")
        f.write("5. Delete this review folder when done\n\n")

        f.write("Common OCR Errors:\n")
        f.write("  - O (letter) → 0 (zero)\n")
        f.write("  - l (lowercase L) → 1 (one)\n")
        f.write("  - S (letter) → 5 (five)\n")
        f.write("  - Missing decimal points\n")
        f.write("  - Transposed digits\n")
        f.write("  - Missing or incorrect sector names\n")

    logger.warning(f"Flagged for manual review: {pdf_file.name} ({confidence:.1%} confidence)")
    logger.info(f"Review package created: {review_subdir}")


def should_flag_for_review(
    confidence: float,
    validation_errors: List[str],
    threshold: float = 0.85
) -> bool:
    """
    Determine if output should be flagged for manual review.

    Args:
        confidence: Combined confidence score
        validation_errors: List of validation errors
        threshold: Confidence threshold

    Returns:
        True if should flag, False otherwise
    """
    # Flag if confidence below threshold
    if confidence < threshold:
        return True

    # Flag if critical validation errors present
    critical_keywords = ['too few', 'missing', 'not numeric', 'unrealistic']
    critical_errors = [
        err for err in validation_errors
        if any(keyword in err.lower() for keyword in critical_keywords)
    ]

    if len(critical_errors) >= 2:  # Multiple critical errors
        return True

    return False


def generate_validation_report(results: Dict[str, any]) -> str:
    """
    Generate human-readable validation report.

    Args:
        results: Dictionary with validation results

    Returns:
        Formatted report string
    """
    report = []
    report.append("OCR Validation Report")
    report.append("=" * 60)

    report.append(f"File: {results.get('filename', 'N/A')}")
    report.append(f"Table Type: {results.get('table_type', 'N/A')}")
    report.append(f"")

    report.append(f"Confidence Scores:")
    report.append(f"  OCR Confidence: {results.get('ocr_confidence', 0):.1%}")
    report.append(f"  Combined Score: {results.get('combined_confidence', 0):.1%}")
    report.append(f"  Status: {'PASS' if results.get('combined_confidence', 0) >= 0.85 else 'NEEDS REVIEW'}")
    report.append(f"")

    report.append(f"DataFrame Shape: {results.get('shape', 'N/A')}")
    report.append(f"Missing Values: {results.get('missing_count', 0)}")
    report.append(f"")

    errors = results.get('validation_errors', [])
    if errors:
        report.append(f"Validation Errors ({len(errors)}):")
        for i, error in enumerate(errors, 1):
            report.append(f"  {i}. {error}")
    else:
        report.append("Validation: ✓ All checks passed")

    report.append("=" * 60)

    return "\n".join(report)


if __name__ == "__main__":
    # Test validator
    import sys

    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    if len(sys.argv) < 2:
        print("Usage: python validator.py <csv_file>")
        print("  csv_file: CSV file to validate")
        sys.exit(1)

    csv_file = sys.argv[1]

    # Load CSV
    try:
        df = pd.read_csv(csv_file, sep=';', encoding='utf-8-sig')
        print(f"Loaded CSV: {csv_file}")
        print(f"Shape: {df.shape}\n")
    except Exception as e:
        print(f"✗ Failed to load CSV: {e}")
        sys.exit(1)

    # Determine table type
    table_type = "table_2" if "table_2" in csv_file or "quarterly" in csv_file else "table_1"

    # Validate
    errors = validate_csv_structure(df, table_type)

    if errors:
        print(f"✗ Validation failed: {len(errors)} error(s)\n")
        for i, error in enumerate(errors, 1):
            print(f"  {i}. {error}")
    else:
        print(f"✓ Validation passed\n")

    # Calculate confidence (simulated OCR confidence)
    ocr_conf = 0.88
    combined_conf = calculate_confidence_score(df, ocr_conf, errors)

    print(f"Confidence Scores:")
    print(f"  OCR: {ocr_conf:.1%}")
    print(f"  Combined: {combined_conf:.1%}")

    # Check if should flag
    should_flag = should_flag_for_review(combined_conf, errors)
    print(f"  Status: {'NEEDS REVIEW' if should_flag else 'PASS'}")

    # Generate report
    results = {
        'filename': Path(csv_file).name,
        'table_type': table_type,
        'ocr_confidence': ocr_conf,
        'combined_confidence': combined_conf,
        'shape': df.shape,
        'missing_count': df.isnull().sum().sum(),
        'validation_errors': errors
    }

    print(f"\n" + generate_validation_report(results))
