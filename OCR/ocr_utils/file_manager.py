"""
File Manager Utility

File discovery, organization, and management for OCR pipeline.

Author: Jason Cruz
Institution: Universidad del Pacífico - CIUP
Date: January 2026
"""

import re
from pathlib import Path
from typing import List, Dict, Tuple
import logging

logger = logging.getLogger(__name__)


class PDFFileInfo:
    """Container for PDF file metadata."""

    def __init__(self, path: Path, year: int, issue: int, num_pages: int):
        self.path = path
        self.year = year
        self.issue = issue
        self.num_pages = num_pages
        self.filename = path.name

    def __repr__(self):
        return f"PDFFileInfo({self.filename}, year={self.year}, issue={self.issue}, pages={self.num_pages})"


def discover_pdfs(pdf_dir: str, year: int) -> List[Path]:
    """
    Discover all PDF files for a specific year.

    Args:
        pdf_dir: Base directory (e.g., "OCR/raw")
        year: Year to search (e.g., 1994)

    Returns:
        List of PDF file paths, sorted by issue number
    """
    year_dir = Path(pdf_dir) / str(year)

    if not year_dir.exists():
        logger.warning(f"Year directory not found: {year_dir}")
        return []

    # Find all PDF files
    pdf_files = list(year_dir.glob("ns_*_*.pdf"))

    # Sort by issue number
    def extract_issue(path: Path) -> int:
        # Extract issue number from filename: ns_XX_YYYY.pdf
        match = re.search(r"ns_(\d+)_\d{4}\.pdf", path.name)
        if match:
            return int(match.group(1))
        return 0

    pdf_files.sort(key=extract_issue)

    logger.info(f"Found {len(pdf_files)} PDFs for year {year}")
    return pdf_files


def discover_all_pdfs(pdf_dir: str, years: range) -> List[Path]:
    """
    Discover all PDFs across multiple years.

    Args:
        pdf_dir: Base directory (e.g., "OCR/raw")
        years: Range of years (e.g., range(1994, 2013))

    Returns:
        List of all PDF file paths
    """
    all_pdfs = []

    for year in years:
        year_pdfs = discover_pdfs(pdf_dir, year)
        all_pdfs.extend(year_pdfs)

    logger.info(f"Total PDFs discovered: {len(all_pdfs)} across {len(years)} years")
    return all_pdfs


def determine_pdf_structure(year: int, years_single_page: List[int]) -> Tuple[int, List[str]]:
    """
    Determine PDF structure based on year.

    Args:
        year: PDF year
        years_single_page: List of years with 1-page PDFs

    Returns:
        Tuple of (num_pages, tables_to_extract)
            - num_pages: 1 or 2
            - tables_to_extract: ["table_1"] or ["table_1", "table_2"]
    """
    if year in years_single_page:
        # 1-page PDFs: Only Table 1 (monthly data)
        return (1, ["table_1"])
    else:
        # 2-page PDFs: Table 1 + Table 2
        return (2, ["table_1", "table_2"])


def get_output_path(pdf_path: Path, output_dir: str, table_type: str) -> Path:
    """
    Get output CSV path for a PDF.

    Args:
        pdf_path: Input PDF path (e.g., OCR/raw/1994/ns_03_1994.pdf)
        output_dir: Output base directory (e.g., "OCR/output")
        table_type: "table_1" or "table_2"

    Returns:
        Output CSV path (e.g., OCR/output/table_1/1994/ns-03-1994.csv)
    """
    # Extract year from filename
    match = re.search(r"_(\d{4})\.pdf$", pdf_path.name)
    if not match:
        raise ValueError(f"Cannot extract year from filename: {pdf_path.name}")

    year = match.group(1)

    # Convert filename: ns_XX_YYYY.pdf → ns-XX-YYYY.csv
    csv_filename = pdf_path.stem.replace("_", "-") + ".csv"

    # Build output path
    output_path = Path(output_dir) / table_type / year / csv_filename

    return output_path


def ensure_output_directories(output_dir: str, years: range) -> None:
    """
    Create output directory structure.

    Args:
        output_dir: Base output directory (e.g., "OCR/output")
        years: Range of years to create directories for
    """
    for table_type in ["table_1", "table_2"]:
        for year in years:
            year_dir = Path(output_dir) / table_type / str(year)
            year_dir.mkdir(parents=True, exist_ok=True)

    logger.info(f"Created output directories: {output_dir}")


def cleanup_temp_images(temp_dir: str) -> None:
    """
    Delete temporary preprocessed images.

    Args:
        temp_dir: Temporary images directory
    """
    temp_path = Path(temp_dir)

    if not temp_path.exists():
        return

    # Count files before deletion
    files = list(temp_path.rglob("*.png"))
    count = len(files)

    # Delete all PNG files
    for file in files:
        file.unlink()

    # Remove empty directories
    for dir_path in sorted(temp_path.rglob("*"), reverse=True):
        if dir_path.is_dir() and not any(dir_path.iterdir()):
            dir_path.rmdir()

    logger.info(f"Cleaned up {count} temporary images from {temp_dir}")


def write_needs_review_list(
    needs_review: List[Dict], output_file: str = "OCR/needs_review.txt"
) -> None:
    """
    Write list of files needing manual review.

    Args:
        needs_review: List of file info dictionaries
        output_file: Output file path
    """
    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("Files Needing Manual Review\n")
        f.write("=" * 80 + "\n\n")

        if not needs_review:
            f.write("No files need review. All outputs passed validation.\n")
        else:
            f.write(f"Total files: {len(needs_review)}\n\n")

            for file_info in needs_review:
                filename = file_info.get("filename", "N/A")
                confidence = file_info.get("confidence", 0.0)
                issues = file_info.get("issues", [])

                f.write(f"{filename}\n")
                f.write(f"  Confidence: {confidence:.1%}\n")
                f.write(f"  Issues:\n")
                for issue in issues:
                    f.write(f"    - {issue}\n")
                f.write("\n")

        f.write("=" * 80 + "\n")
        f.write("See OCR/review/ directory for detailed review packages.\n")

    logger.info(f"Wrote needs-review list: {output_file} ({len(needs_review)} files)")


if __name__ == "__main__":
    # Test file manager
    import sys

    logging.basicConfig(
        level=logging.DEBUG, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    # Test PDF discovery
    print("Testing PDF discovery...")
    pdfs_1994 = discover_pdfs("OCR/raw", 1994)
    print(f"  Found {len(pdfs_1994)} PDFs for 1994")

    if pdfs_1994:
        print(f"  First: {pdfs_1994[0].name}")
        print(f"  Last: {pdfs_1994[-1].name}")

    # Test PDF structure determination
    print("\nTesting PDF structure determination...")
    years_single = [1994, 1995, 1996]

    for year in [1994, 1997, 2000]:
        num_pages, tables = determine_pdf_structure(year, years_single)
        print(f"  {year}: {num_pages} page(s), tables={tables}")

    # Test output path generation
    print("\nTesting output path generation...")
    if pdfs_1994:
        test_pdf = pdfs_1994[0]
        output_path = get_output_path(test_pdf, "OCR/output", "table_1")
        print(f"  Input:  {test_pdf}")
        print(f"  Output: {output_path}")

    # Test directory creation
    print("\nTesting directory creation...")
    ensure_output_directories("OCR/output", range(1994, 2013))
    print("  ✓ Output directories created")

    print("\n✓ File manager tests complete")
