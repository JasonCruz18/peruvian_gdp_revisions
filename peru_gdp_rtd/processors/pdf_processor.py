"""
PDF shortening for BCRP Weekly Reports.

This module provides functionality to generate shortened PDFs from raw WR PDFs
by extracting only pages containing relevant keywords (e.g., GDP tables). For 4-page
outputs, it retains only pages 1 and 3 where key tables typically appear.
"""

import os
import re
import time
from typing import List, Optional, Set

import fitz  # PyMuPDF

try:
    from pypdf import PdfReader, PdfWriter
except ImportError:  # Defer hard failure to runtime with clearer message
    PdfReader = None
    PdfWriter = None
from tqdm import tqdm

from peru_gdp_rtd.config.settings import Settings
from peru_gdp_rtd.processors.metadata import ns_sort_key


def search_keywords(pdf_file: str, keywords: List[str]) -> List[int]:
    """
    Find 0-indexed page numbers containing any of the given keywords.

    Args:
        pdf_file: Path to the PDF file to search.
        keywords: List of keywords to search for (case-sensitive).

    Returns:
        List of page indices (0-indexed) where any keyword appears.

    Example:
        >>> pages = search_keywords("report.pdf", ["GDP", "economy"])
        >>> print(f"Keywords found on pages: {pages}")
    """
    pages_with_keywords = []
    with fitz.open(pdf_file) as doc:
        for page_num in range(doc.page_count):
            page_text = doc.load_page(page_num).get_text()
            if any(keyword in page_text for keyword in keywords):
                pages_with_keywords.append(page_num)
    return pages_with_keywords


def shortened_pdf(pdf_file: str, pages: List[int], output_folder: str) -> int:
    """
    Create a PDF containing only selected pages from source PDF.

    Args:
        pdf_file: Path to the source PDF file.
        pages: List of 0-indexed page numbers to retain.
        output_folder: Destination folder for the shortened PDF.

    Returns:
        Number of pages in the shortened PDF (0 if no pages were selected).

    Note:
        Output filename mirrors the source filename.
    """
    if PdfReader is None or PdfWriter is None:
        raise ImportError(
            "pypdf is required for PDF shortening. Install with `pip install pypdf`."
        )
    if not pages:
        return 0

    os.makedirs(output_folder, exist_ok=True)
    new_pdf_file = os.path.join(output_folder, os.path.basename(pdf_file))

    with fitz.open(pdf_file) as doc:
        new_doc = fitz.open()
        for page_idx in pages:
            new_doc.insert_pdf(doc, from_page=page_idx, to_page=page_idx)
        new_doc.save(new_pdf_file)
        count = new_doc.page_count
        new_doc.close()

    return count


def read_input_pdf_files(input_pdf_record_folder: str, input_pdf_record_txt: str) -> Set[str]:
    """
    Read filenames of previously processed PDFs from record file.

    Args:
        input_pdf_record_folder: Folder containing the record file.
        input_pdf_record_txt: Name of the record file.

    Returns:
        Set of filenames that have already been processed.
    """
    record_path = os.path.join(input_pdf_record_folder, input_pdf_record_txt)
    if not os.path.exists(record_path):
        return set()

    with open(record_path, "r", encoding="utf-8") as f:
        return set(line.strip() for line in f if line.strip())


def write_input_pdf_files(
    input_pdf_files: Set[str], input_pdf_record_folder: str, input_pdf_record_txt: str
) -> None:
    """
    Write processed PDF filenames to record file.

    Args:
        input_pdf_files: Set of filenames to write.
        input_pdf_record_folder: Folder for the record file.
        input_pdf_record_txt: Name of the record file.

    Note:
        Filenames are written in sorted order for deterministic output.
    """
    record_path = os.path.join(input_pdf_record_folder, input_pdf_record_txt)
    os.makedirs(input_pdf_record_folder, exist_ok=True)

    with open(record_path, "w", encoding="utf-8") as f:
        for filename in sorted(input_pdf_files, key=ns_sort_key):
            f.write(filename + "\n")


def ask_continue_input(message: str) -> bool:
    """
    Prompt user for yes/no decision.

    Args:
        message: Prompt message to display.

    Returns:
        True if user answers 'y', False if 'n'.
    """
    while True:
        answer = input(f"{message} (y = yes / n = no): ").strip().lower()
        if answer in ("y", "n"):
            return answer == "y"


def pdf_input_generator(
    settings: Settings,
    keywords: Optional[List[str]] = None,
    interactive: bool = True,
    verbose: bool = True,
    force: bool = False,
) -> None:
    """
    Generate shortened PDFs from raw WR PDFs by extracting pages matching keywords.

    Processes raw PDFs organized in yearly subfolders, extracting only pages that
    contain specified keywords. For 4-page outputs (typical when searching for
    "economic sectors"), retains only pages 1 and 3 which contain GDP percentage
    variation tables.

    Args:
        settings: Configuration settings object.
        keywords: Keywords to search for. If None, uses default GDP table keywords.
        interactive: If True, prompts user between folders. If False, processes all.
        verbose: If True, prints detailed progress information.
        force: If True, reprocess all files regardless of timestamps.

    Note:
        Uses timestamp-based processing - only regenerates if source is newer than output.
    """
    from pathlib import Path

    start_time = time.time()

    # Use default keywords if none provided
    if keywords is None:
        keywords = ["sectores económicos", "economic sectors"]

    # Get paths from configuration
    raw_pdf_folder = Path(settings.paths.pdf_raw)
    input_pdf_folder = Path(settings.paths.pdf_input)

    # Ensure output folder exists
    input_pdf_folder.mkdir(parents=True, exist_ok=True)

    record_folder = Path(settings.paths.record)
    record_txt = settings.record_files.get("shortened_pdfs", "2_shortened_pdfs.txt")
    processed_shortened = read_input_pdf_files(str(record_folder), record_txt)

    years_found = []
    total_files = 0
    new_counter = 0
    skipped_counter = 0

    print("\n>> Starting PDF shortening...")
    print(f">> Raw PDF folder: {raw_pdf_folder}")
    print(f">> Shortened PDF folder: {input_pdf_folder}")
    print(f">> Record file: {record_folder / record_txt}")

    # Process each year folder
    for folder in sorted(os.listdir(raw_pdf_folder)):
        if folder in {"_quarantine", "shortened_pdfs"}:
            continue

        folder_path = raw_pdf_folder / folder
        if not folder_path.is_dir():
            continue

        years_found.append(folder)
        pdf_files = sorted([f for f in os.listdir(folder_path) if f.endswith(".pdf")])
        if not pdf_files:
            continue
        total_files += len(pdf_files)

        if verbose:
            print(f"\n>> Processing year folder: {folder}")

        folder_new_count = 0
        folder_skipped_count = 0

        # Process PDFs in this year with progress bar
        pbar = tqdm(
            pdf_files,
            desc=f"Shortening PDFs in {folder}",
            unit="PDF",
            disable=not verbose,
        )

        for filename in pbar:
            pdf_file = folder_path / filename
            output_folder_year = input_pdf_folder / folder
            output_folder_year.mkdir(parents=True, exist_ok=True)
            output_file = output_folder_year / filename

            # Record-based skip (with optional force override)
            if not force and filename in processed_shortened:
                folder_skipped_count += 1
                continue

            # Timestamp-based skip for safety when record is incomplete
            if not force and output_file.exists():
                if pdf_file.stat().st_mtime <= output_file.stat().st_mtime:
                    folder_skipped_count += 1
                    processed_shortened.add(filename)
                    continue

            # Extract pages with keywords
            pages_with_keywords = search_keywords(str(pdf_file), keywords)
            num_pages = shortened_pdf(
                str(pdf_file), pages_with_keywords, output_folder=str(output_folder_year)
            )

            if num_pages == 0:
                continue

            # Special handling for 4-page outputs
            # (contains both levels and percentage variations tables)
            short_pdf_file = output_folder_year / filename
            reader = PdfReader(str(short_pdf_file))

            if len(reader.pages) == 4:
                # Keep only pages 1 and 3 (percentage variation tables)
                writer = PdfWriter()
                writer.add_page(reader.pages[0])  # Monthly GDP % variations
                writer.add_page(reader.pages[2])  # Quarterly/annual GDP % variations
                with open(short_pdf_file, "wb") as f_out:
                    writer.write(f_out)

            folder_new_count += 1
            processed_shortened.add(filename)

        pbar.close()

        if verbose:
            print(
                f">> Shortened PDFs saved in '{output_folder_year}' "
                f"({folder_new_count} new, {folder_skipped_count} skipped)"
            )

        new_counter += folder_new_count
        skipped_counter += folder_skipped_count

        # Ask to continue to next folder
        if interactive and not ask_continue_input(
            f"Do you want to continue to the next folder after '{folder}'?"
        ):
            if verbose:
                print(">> Process stopped by user.")
            break

    # Print summary
    elapsed_time = round(time.time() - start_time)
    print("\n>> Summary (Shorten PDFs):")
    print(f">> Raw PDF folder: {raw_pdf_folder}")
    print(f">> Shortened PDF folder: {input_pdf_folder}")
    print(f">> Record file: {record_folder / record_txt}")
    print(f">> Year folders processed: {len(years_found)}")
    print(f">> PDFs scanned: {total_files}")
    print(f">> PDFs skipped (already shortened): {skipped_counter}")
    print(f">> PDFs generated: {new_counter}")
    print(f">> Time elapsed: {elapsed_time} seconds")

    # Persist updated record
    write_input_pdf_files(processed_shortened, str(record_folder), record_txt)
