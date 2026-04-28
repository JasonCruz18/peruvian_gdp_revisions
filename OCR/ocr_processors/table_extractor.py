"""
Table Extraction Module

Extracts upper table (growth rates) while ignoring lower table (levels).
Each page contains two tables - we only want the top one.

Author: Jason Cruz
Institution: Universidad del Pacífico - CIUP
Date: January 2026
"""

import cv2
import numpy as np
from typing import List, Tuple, Optional
import logging

logger = logging.getLogger(__name__)


def detect_horizontal_lines(image: np.ndarray, min_line_length: int = 40) -> List[int]:
    """
    Detect horizontal lines in image (table borders).

    Args:
        image: Binary image
        min_line_length: Minimum length to consider a line

    Returns:
        List of y-coordinates where horizontal lines are detected
    """
    # Create horizontal kernel
    horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (min_line_length, 1))

    # Detect horizontal lines
    detect_horizontal = cv2.morphologyEx(image, cv2.MORPH_OPEN, horizontal_kernel, iterations=2)

    # Find row positions with lines
    # Sum across width - high values indicate horizontal lines
    row_sums = detect_horizontal.sum(axis=1)
    threshold = image.shape[1] * 0.5  # Line must span at least 50% of width

    line_positions = np.where(row_sums > threshold)[0].tolist()

    logger.debug(f"Detected {len(line_positions)} horizontal line segments")
    return line_positions


def find_table_separator(image: np.ndarray, horizontal_lines: List[int]) -> Optional[int]:
    """
    Find the separator between upper and lower tables.

    Strategy: Look for a significant gap or thick line in the middle region.

    Args:
        image: Binary image
        horizontal_lines: List of y-coordinates with detected lines

    Returns:
        Y-coordinate of separator (None if not found)
    """
    height = image.shape[0]

    # Focus on middle region (40-60% of page)
    mid_start = int(height * 0.4)
    mid_end = int(height * 0.6)

    # Find lines in middle region
    mid_lines = [y for y in horizontal_lines if mid_start <= y <= mid_end]

    if not mid_lines:
        logger.warning("No separator line found in middle region")
        return None

    # Use the first significant line in middle region
    separator = mid_lines[0]

    logger.debug(f"Table separator detected at y={separator} ({separator/height:.1%} of height)")
    return separator


def extract_upper_table(
    image: np.ndarray, upper_ratio: Tuple[float, float] = (0.0, 0.5)
) -> np.ndarray:
    """
    Extract upper table region (growth rates) from page.

    Uses simple strategy: crop to top portion of page (default: top 50%).
    This works because tables are consistently positioned.

    Args:
        image: Preprocessed binary image
        upper_ratio: Tuple of (start_ratio, end_ratio) for vertical crop

    Returns:
        Cropped image containing only upper table

    Raises:
        ValueError: If ratio is invalid
    """
    if not (0 <= upper_ratio[0] < upper_ratio[1] <= 1.0):
        raise ValueError(f"Invalid upper_ratio: {upper_ratio}")

    height = image.shape[0]

    # Calculate crop boundaries
    start_y = int(height * upper_ratio[0])
    end_y = int(height * upper_ratio[1])

    # Crop to upper portion
    upper_table = image[start_y:end_y, :]

    logger.info(
        f"Extracted upper table: {upper_table.shape[0]}x{upper_table.shape[1]} "
        f"({upper_ratio[0]:.0%}-{upper_ratio[1]:.0%} of page)"
    )

    return upper_table


def extract_upper_table_auto(image: np.ndarray) -> np.ndarray:
    """
    Automatically detect and extract upper table using line detection.

    Fallback: If detection fails, crop to top 50%.

    Args:
        image: Preprocessed binary image

    Returns:
        Cropped image containing upper table
    """
    # Try automatic detection
    try:
        horizontal_lines = detect_horizontal_lines(image)

        if not horizontal_lines:
            logger.warning("No horizontal lines detected, using default crop")
            return extract_upper_table(image)

        separator = find_table_separator(image, horizontal_lines)

        if separator is None:
            logger.warning("Table separator not found, using default crop")
            return extract_upper_table(image)

        # Crop from top to separator
        upper_table = image[:separator, :]

        logger.info(f"Auto-extracted upper table: {upper_table.shape[0]}x{upper_table.shape[1]}")
        return upper_table

    except Exception as e:
        logger.error(f"Auto extraction failed: {e}, using default crop")
        return extract_upper_table(image)


def validate_table_region(image: np.ndarray, min_text_density: float = 0.05) -> bool:
    """
    Validate that extracted region contains table content.

    Args:
        image: Extracted table region
        min_text_density: Minimum ratio of black pixels

    Returns:
        True if region appears to contain table, False otherwise
    """
    # Calculate text density (ratio of black pixels in binary image)
    total_pixels = image.size
    text_pixels = np.sum(image > 0)  # White pixels in binary image
    text_density = text_pixels / total_pixels

    is_valid = text_density >= min_text_density

    if not is_valid:
        logger.warning(f"Low text density: {text_density:.1%} < {min_text_density:.1%}")
    else:
        logger.debug(f"Text density: {text_density:.1%}")

    return is_valid


def detect_table_boundaries(image: np.ndarray) -> Optional[Tuple[int, int, int, int]]:
    """
    Detect table boundaries (x_min, y_min, x_max, y_max).

    Useful for precise cropping to remove page margins.

    Args:
        image: Binary image

    Returns:
        Tuple of (x_min, y_min, x_max, y_max) or None if detection fails
    """
    # Find all non-zero (text) pixels
    coords = np.column_stack(np.where(image > 0))

    if len(coords) == 0:
        logger.warning("No text pixels found for boundary detection")
        return None

    # Get bounding box
    y_min, x_min = coords.min(axis=0)
    y_max, x_max = coords.max(axis=0)

    # Add small margin
    margin = 10
    height, width = image.shape
    x_min = max(0, x_min - margin)
    y_min = max(0, y_min - margin)
    x_max = min(width, x_max + margin)
    y_max = min(height, y_max + margin)

    logger.debug(f"Table boundaries: x={x_min}-{x_max}, y={y_min}-{y_max}")
    return (x_min, y_min, x_max, y_max)


def crop_to_table(image: np.ndarray) -> np.ndarray:
    """
    Crop image to tight bounds around table content.

    Removes excess margins while preserving table data.

    Args:
        image: Binary image with table

    Returns:
        Cropped image
    """
    boundaries = detect_table_boundaries(image)

    if boundaries is None:
        logger.warning("Boundary detection failed, returning original image")
        return image

    x_min, y_min, x_max, y_max = boundaries

    # Crop to boundaries
    cropped = image[y_min:y_max, x_min:x_max]

    logger.info(f"Cropped to table: {image.shape} → {cropped.shape}")
    return cropped


if __name__ == "__main__":
    # Test table extractor
    import sys
    from pathlib import Path

    logging.basicConfig(
        level=logging.DEBUG, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    if len(sys.argv) < 2:
        print("Usage: python table_extractor.py <image_path>")
        print("  image_path: Preprocessed binary image")
        sys.exit(1)

    image_path = sys.argv[1]

    # Load image
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    if image is None:
        print(f"✗ Failed to load image: {image_path}")
        sys.exit(1)

    print(f"Loaded image: {image.shape}")

    # Extract upper table (method 1: simple crop)
    upper_simple = extract_upper_table(image, upper_ratio=(0.0, 0.5))
    print(f"\n✓ Simple extraction: {upper_simple.shape}")

    # Extract upper table (method 2: automatic detection)
    upper_auto = extract_upper_table_auto(image)
    print(f"✓ Auto extraction: {upper_auto.shape}")

    # Validate
    is_valid = validate_table_region(upper_auto)
    print(f"✓ Validation: {'PASS' if is_valid else 'FAIL'}")

    # Save results
    output_dir = Path("OCR/temp_images/test")
    output_dir.mkdir(parents=True, exist_ok=True)

    cv2.imwrite(str(output_dir / "upper_simple.png"), upper_simple)
    cv2.imwrite(str(output_dir / "upper_auto.png"), upper_auto)

    print(f"\n✓ Results saved to: {output_dir}/")
