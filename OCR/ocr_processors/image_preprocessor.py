"""
Image Preprocessing Module

Implements complete 11-step image preprocessing pipeline for OCR quality enhancement.
Based on the OCR preprocessing workflow used in this project.

Steps:
1. PDF to PNG conversion (300 DPI)
2. Grayscale conversion
3. Adaptive binarization (Otsu's method)
4. Noise removal (median filtering)
5. Skew correction (deskewing)
6. DPI scaling (ensure ≥300 DPI)
7. Contrast enhancement (CLAHE)
8. Morphological thinning (optional)
9. Border removal

Author: Jason Cruz
Institution: Universidad del Pacífico - CIUP
Date: January 2026
"""

import cv2
import numpy as np
from pathlib import Path
from typing import List, Tuple, Optional
from pdf2image import convert_from_path
from skimage.morphology import thin
import logging

logger = logging.getLogger(__name__)


class ImagePreprocessor:
    """
    Complete image preprocessing pipeline for OCR enhancement.

    Handles all preprocessing steps from PDF conversion through final
    image optimization for Tesseract OCR.
    """

    def __init__(
        self,
        target_dpi: int = 300,
        apply_clahe: bool = True,
        clahe_clip_limit: float = 2.0,
        clahe_tile_grid_size: Tuple[int, int] = (8, 8),
        noise_removal_method: str = "median",
        median_kernel_size: int = 3,
        skew_angle_threshold: float = 0.5,
        thinning: bool = False,
        border_size: int = 10,
    ):
        """
        Initialize image preprocessor with configuration.

        Args:
            target_dpi: Minimum DPI for OCR (default: 300)
            apply_clahe: Enable CLAHE contrast enhancement
            clahe_clip_limit: CLAHE clipping limit
            clahe_tile_grid_size: CLAHE tile grid size
            noise_removal_method: "median", "gaussian", or "bilateral"
            median_kernel_size: Kernel size for median filtering
            skew_angle_threshold: Only correct skew if angle > this
            thinning: Apply morphological thinning (can hurt accuracy)
            border_size: Pixels to remove from each edge
        """
        self.target_dpi = target_dpi
        self.apply_clahe = apply_clahe
        self.clahe_clip_limit = clahe_clip_limit
        self.clahe_tile_grid_size = clahe_tile_grid_size
        self.noise_removal_method = noise_removal_method
        self.median_kernel_size = median_kernel_size
        self.skew_angle_threshold = skew_angle_threshold
        self.thinning = thinning
        self.border_size = border_size

        logger.info(f"ImagePreprocessor initialized: DPI={target_dpi}, CLAHE={apply_clahe}")

    def pdf_to_png(self, pdf_path: str, dpi: int = 300) -> List[np.ndarray]:
        """
        Step 1: Convert PDF pages to PNG images at specified DPI.

        Args:
            pdf_path: Path to PDF file
            dpi: Resolution in dots per inch

        Returns:
            List of numpy arrays (images), one per page

        Raises:
            FileNotFoundError: If PDF doesn't exist
            Exception: If PDF conversion fails
        """
        pdf_file = Path(pdf_path)

        if not pdf_file.exists():
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")

        try:
            logger.debug(f"Converting PDF to PNG: {pdf_file.name} at {dpi} DPI")

            # Convert all pages
            pil_images = convert_from_path(str(pdf_file), dpi=dpi, fmt="png")

            # Convert PIL images to numpy arrays
            images = [np.array(img) for img in pil_images]

            logger.info(f"Converted {len(images)} page(s) from {pdf_file.name}")
            return images

        except Exception as e:
            logger.error(f"PDF conversion failed for {pdf_file.name}: {e}")
            raise

    def convert_to_grayscale(self, image: np.ndarray) -> np.ndarray:
        """
        Step 2: Convert color image to grayscale.

        Args:
            image: Input image (color or grayscale)

        Returns:
            Grayscale image
        """
        if len(image.shape) == 3:
            # Color image - convert to grayscale
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            logger.debug("Converted to grayscale")
            return gray
        else:
            # Already grayscale
            logger.debug("Image already grayscale")
            return image

    def apply_adaptive_binarization(self, image: np.ndarray) -> np.ndarray:
        """
        Step 3: Apply adaptive binarization to separate text from background.

        Uses Otsu's method for automatic threshold determination.

        Args:
            image: Grayscale image

        Returns:
            Binary image (0 or 255)
        """
        # Otsu's binarization
        _, binary = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        logger.debug("Applied adaptive binarization (Otsu)")
        return binary

    def remove_noise(self, image: np.ndarray, method: Optional[str] = None) -> np.ndarray:
        """
        Step 4: Remove noise using specified filtering method.

        Args:
            image: Input image
            method: "median", "gaussian", or "bilateral" (None = use instance default)

        Returns:
            Denoised image
        """
        if method is None:
            method = self.noise_removal_method

        if method == "median":
            denoised = cv2.medianBlur(image, self.median_kernel_size)
        elif method == "gaussian":
            denoised = cv2.GaussianBlur(image, (3, 3), 0)
        elif method == "bilateral":
            denoised = cv2.bilateralFilter(image, 9, 75, 75)
        else:
            # Fallback: non-local means denoising
            denoised = cv2.fastNlMeansDenoising(image, None, 10, 7, 21)

        logger.debug(f"Applied {method} noise removal")
        return denoised

    def correct_skew(self, image: np.ndarray) -> np.ndarray:
        """
        Step 5: Detect and correct skew angle (deskewing).

        Uses minimum area rectangle detection to find text orientation.
        Only corrects if skew angle exceeds threshold.

        Args:
            image: Binary image

        Returns:
            Deskewed image
        """
        # Find all non-zero pixels
        coords = np.column_stack(np.where(image > 0))

        if len(coords) == 0:
            logger.warning("No text detected for skew correction")
            return image

        # Get minimum area rectangle
        angle = cv2.minAreaRect(coords)[-1]

        # Normalize angle
        if angle < -45:
            angle = -(90 + angle)
        else:
            angle = -angle

        # Reject angles near ±90° (these are orientation issues, not skew)
        if abs(abs(angle) - 90) < 5:
            logger.debug(f"Skew angle {angle:.2f}° near ±90°, likely orientation issue - skipping")
            return image

        # Only correct if skew is significant
        if abs(angle) < self.skew_angle_threshold:
            logger.debug(f"Skew angle {angle:.2f}° below threshold, skipping correction")
            return image

        # Rotate to correct skew
        h, w = image.shape[:2]
        center = (w // 2, h // 2)
        M = cv2.getRotationMatrix2D(center, angle, 1.0)
        rotated = cv2.warpAffine(
            image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE
        )

        logger.debug(f"Corrected skew: {angle:.2f}°")
        return rotated

    def scale_to_dpi(self, image: np.ndarray, target_dpi: Optional[int] = None) -> np.ndarray:
        """
        Step 6: Ensure image meets minimum DPI requirement.

        Upscales if necessary using bicubic interpolation.

        Args:
            image: Input image
            target_dpi: Target DPI (None = use instance default)

        Returns:
            Scaled image
        """
        if target_dpi is None:
            target_dpi = self.target_dpi

        current_height = image.shape[0]

        # Assuming standard letter page height (11 inches)
        min_height = int(11 * target_dpi)

        if current_height >= min_height:
            logger.debug(f"Image DPI sufficient ({current_height} >= {min_height})")
            return image

        # Calculate scale factor
        scale_factor = min_height / current_height
        new_width = int(image.shape[1] * scale_factor)

        # Upscale using bicubic interpolation
        scaled = cv2.resize(image, (new_width, min_height), interpolation=cv2.INTER_CUBIC)

        logger.debug(
            f"Scaled image: {current_height}px → {min_height}px (factor: {scale_factor:.2f})"
        )
        return scaled

    def enhance_contrast(self, image: np.ndarray) -> np.ndarray:
        """
        Step 7: Apply CLAHE (Contrast Limited Adaptive Histogram Equalization).

        Essential for scans with shadows, fading, or uneven lighting.

        Args:
            image: Grayscale image

        Returns:
            Contrast-enhanced image
        """
        if not self.apply_clahe:
            logger.debug("CLAHE disabled, skipping")
            return image

        clahe = cv2.createCLAHE(
            clipLimit=self.clahe_clip_limit, tileGridSize=self.clahe_tile_grid_size
        )
        enhanced = clahe.apply(image)

        logger.debug(
            f"Applied CLAHE (clip={self.clahe_clip_limit}, grid={self.clahe_tile_grid_size})"
        )
        return enhanced

    def apply_thinning(self, image: np.ndarray) -> np.ndarray:
        """
        Step 8: Apply morphological thinning to separate touching characters.

        WARNING: Can reduce accuracy in some cases. Use with caution.

        Args:
            image: Binary image

        Returns:
            Thinned image
        """
        if not self.thinning:
            logger.debug("Thinning disabled, skipping")
            return image

        # Convert to binary (0 or 1)
        binary = (image > 127).astype(np.uint8)

        # Apply thinning
        thinned = thin(binary)

        # Convert back to 0-255 range
        result = (thinned * 255).astype(np.uint8)

        logger.debug("Applied morphological thinning")
        return result

    def remove_borders(self, image: np.ndarray, border_size: Optional[int] = None) -> np.ndarray:
        """
        Step 9: Remove borders to avoid edge artifacts.

        Args:
            image: Input image
            border_size: Pixels to remove from each edge (None = use instance default)

        Returns:
            Cropped image
        """
        if border_size is None:
            border_size = self.border_size

        h, w = image.shape[:2]

        # Check if image is large enough
        if h <= 2 * border_size or w <= 2 * border_size:
            logger.warning(f"Image too small for border removal ({h}x{w}), skipping")
            return image

        # Crop borders
        cropped = image[border_size : h - border_size, border_size : w - border_size]

        logger.debug(f"Removed {border_size}px borders")
        return cropped

    def preprocess_for_ocr(
        self,
        pdf_path: str,
        page_num: int = 0,
        save_intermediate: bool = False,
        output_dir: Optional[str] = None,
    ) -> np.ndarray:
        """
        Complete preprocessing pipeline: Execute all steps in sequence.

        Args:
            pdf_path: Path to PDF file
            page_num: Page number to process (0-indexed)
            save_intermediate: Save intermediate images for debugging
            output_dir: Directory to save intermediate images (if enabled)

        Returns:
            Preprocessed image ready for OCR

        Raises:
            ValueError: If page_num exceeds number of pages
            FileNotFoundError: If PDF doesn't exist
        """
        pdf_file = Path(pdf_path)
        logger.info(f"Starting preprocessing: {pdf_file.name}, page {page_num}")

        # Step 1: PDF → PNG
        images = self.pdf_to_png(pdf_path, dpi=self.target_dpi)

        if page_num >= len(images):
            raise ValueError(f"Page {page_num} exceeds PDF pages ({len(images)})")

        image = images[page_num]

        if save_intermediate and output_dir:
            self._save_intermediate(image, output_dir, pdf_file.stem, "01_original")

        # Step 2: Grayscale
        gray = self.convert_to_grayscale(image)
        if save_intermediate and output_dir:
            self._save_intermediate(gray, output_dir, pdf_file.stem, "02_grayscale")

        # Step 3: Adaptive binarization
        binary = self.apply_adaptive_binarization(gray)
        if save_intermediate and output_dir:
            self._save_intermediate(binary, output_dir, pdf_file.stem, "03_binary")

        # Step 4: Noise removal
        denoised = self.remove_noise(binary)
        if save_intermediate and output_dir:
            self._save_intermediate(denoised, output_dir, pdf_file.stem, "04_denoised")

        # Step 5: Skew correction
        deskewed = self.correct_skew(denoised)
        if save_intermediate and output_dir:
            self._save_intermediate(deskewed, output_dir, pdf_file.stem, "05_deskewed")

        # Step 6: Scale to target DPI
        scaled = self.scale_to_dpi(deskewed)
        if save_intermediate and output_dir:
            self._save_intermediate(scaled, output_dir, pdf_file.stem, "06_scaled")

        # Step 7: Contrast enhancement (CLAHE)
        enhanced = self.enhance_contrast(scaled)
        if save_intermediate and output_dir:
            self._save_intermediate(enhanced, output_dir, pdf_file.stem, "07_enhanced")

        # Step 8: Thinning (optional)
        thinned = self.apply_thinning(enhanced)
        if save_intermediate and output_dir:
            self._save_intermediate(thinned, output_dir, pdf_file.stem, "08_thinned")

        # Step 9: Border removal
        clean = self.remove_borders(thinned)
        if save_intermediate and output_dir:
            self._save_intermediate(clean, output_dir, pdf_file.stem, "09_final")

        logger.info(f"Preprocessing complete: {pdf_file.name}")
        return clean

    def _save_intermediate(
        self, image: np.ndarray, output_dir: str, pdf_stem: str, step_name: str
    ) -> None:
        """
        Save intermediate preprocessing image for debugging.

        Args:
            image: Image to save
            output_dir: Output directory
            pdf_stem: PDF filename stem
            step_name: Preprocessing step name
        """
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        filename = f"{pdf_stem}_{step_name}.png"
        filepath = output_path / filename

        cv2.imwrite(str(filepath), image)
        logger.debug(f"Saved intermediate: {filename}")


if __name__ == "__main__":
    # Test image preprocessor
    import sys

    logging.basicConfig(
        level=logging.DEBUG, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    if len(sys.argv) < 2:
        print("Usage: python image_preprocessor.py <pdf_path>")
        sys.exit(1)

    pdf_path = sys.argv[1]

    preprocessor = ImagePreprocessor(target_dpi=300, apply_clahe=True)

    try:
        processed_image = preprocessor.preprocess_for_ocr(
            pdf_path, page_num=0, save_intermediate=True, output_dir="OCR/temp_images/test"
        )

        print(f"✓ Preprocessing successful")
        print(f"  Output shape: {processed_image.shape}")
        print(f"  Intermediate images saved to: OCR/temp_images/test/")

    except Exception as e:
        print(f"✗ Preprocessing failed: {e}")
        sys.exit(1)
