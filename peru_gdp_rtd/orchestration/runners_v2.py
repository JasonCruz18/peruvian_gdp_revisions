"""
Refactored workflow orchestration runners (v1.0.0).

This module provides consolidated, validated runners that:
1. Process both OLD and NEW data sources in one function
2. Use the new unified output structure (vintages/table_1/YYYY/)
3. Add comprehensive validation
4. Support incremental processing with `force` flag
5. Are truly independent with clear input/output contracts
"""

from collections import defaultdict
import logging
import time
from pathlib import Path
from typing import Dict

import pandas as pd

from peru_gdp_rtd.cleaners import NewTableCleaner, OldTableCleaner
from peru_gdp_rtd.processors.metadata import (
    extract_table,
    parse_ns_meta,
)
from peru_gdp_rtd.transformers import VintagesPreparator
from peru_gdp_rtd.orchestration.validation import (
    validate_input_exists,
    validate_rtd_dataframe,
    validate_output_created,
)

logger = logging.getLogger(__name__)


def _build_month_order_map_from_files(files):
    """Build month order map per year from a flat list of WR files."""
    grouped = defaultdict(list)
    for f in files:
        issue, year = parse_ns_meta(f.name)
        if issue and year:
            try:
                grouped[year].append((f.name, int(issue)))
            except ValueError:
                continue

    month_map: Dict[str, int] = {}
    for _year, items in grouped.items():
        for idx, (fname, _issue) in enumerate(sorted(items, key=lambda x: x[1])):
            month_map[fname] = idx + 1
    return month_map


def build_table_1_vintages(
    old_csv_folder: str,
    new_pdf_folder: str,
    output_folder: str,
    pipeline_version: str = "v1.0.0",
    persist_format: str = "parquet",
    force: bool = False,
) -> Dict[str, int]:
    """Build Table 1 (monthly GDP) vintages from both OLD and NEW sources.

    This consolidated runner processes both:
    - OLD CSV files (pre-2013 data) from old_weekly_reports/
    - NEW PDF files (2013+ data) from shortened_pdfs/

    Output structure: vintages/table_1/YYYY/ns-XX-YYYY.parquet

    Args:
        old_csv_folder: Path to OLD CSV files (by year)
        new_pdf_folder: Path to NEW (shortened) PDF files
        output_folder: Output root (e.g., data/output/vintages/table_1)
        pipeline_version: Pipeline version string for metadata
        force: If True, reprocess all files regardless of timestamps

    Returns:
        Dictionary with processing statistics: {
            'old_processed': int,
            'new_processed': int,
            'old_skipped': int,
            'new_skipped': int,
            'total_processed': int,
        }

    Raises:
        FileNotFoundError: If input folders don't exist
        ValueError: If validation fails
    """
    start_time = time.time()
    stats = {
        'old_processed': 0,
        'new_processed': 0,
        'old_skipped': 0,
        'new_skipped': 0,
    }

    logger.info("=" * 70)
    logger.info("Building Table 1 vintages (monthly GDP)")
    logger.info("=" * 70)

    # Validate inputs
    old_csv_path = Path(old_csv_folder)
    if (old_csv_path / "table_1").exists():
        old_csv_path = old_csv_path / "table_1"
    new_pdf_path = Path(new_pdf_folder)
    output_path = Path(output_folder)

    if old_csv_path.exists():
        validate_input_exists(old_csv_path, "Table 1 OLD CSV")
    else:
        logger.warning(f"OLD CSV folder not found: {old_csv_path} - skipping OLD data")

    if new_pdf_path.exists():
        validate_input_exists(new_pdf_path, "Table 1 NEW PDF")
    else:
        logger.warning(f"NEW PDF folder not found: {new_pdf_path} - skipping NEW data")

    # Create output directory
    output_path.mkdir(parents=True, exist_ok=True)

    # Process OLD CSV files (timestamp-based, no record files needed)
    if old_csv_path.exists():
        logger.info("Processing OLD CSV files (pre-2013)...")
        old_stats = _process_old_csv_table_1(
            str(old_csv_path),
            output_folder,
            pipeline_version,
            persist_format,
            force,
        )
        stats['old_processed'] = old_stats['processed']
        stats['old_skipped'] = old_stats['skipped']

    # Process NEW PDF files (timestamp-based, no record files needed)
    if new_pdf_path.exists():
        logger.info("Processing NEW PDF files (2013+)...")
        new_stats = _process_new_pdf_table_1(
            new_pdf_folder,
            output_folder,
            pipeline_version,
            persist_format,
            force,
        )
        stats['new_processed'] = new_stats['processed']
        stats['new_skipped'] = new_stats['skipped']

    # Summary
    stats['total_processed'] = stats['old_processed'] + stats['new_processed']
    elapsed = round(time.time() - start_time)

    logger.info("=" * 70)
    logger.info("Table 1 Processing Summary:")
    logger.info(f"  OLD CSV: {stats['old_processed']} processed, {stats['old_skipped']} skipped")
    logger.info(f"  NEW PDF: {stats['new_processed']} processed, {stats['new_skipped']} skipped")
    logger.info(f"  TOTAL: {stats['total_processed']} vintages created")
    logger.info(f"  Time: {elapsed} seconds")
    logger.info("=" * 70)

    return stats


def build_table_2_vintages(
    old_csv_folder: str,
    new_pdf_folder: str,
    output_folder: str,
    pipeline_version: str = "v1.0.0",
    persist_format: str = "parquet",
    force: bool = False,
) -> Dict[str, int]:
    """Build Table 2 (quarterly/annual GDP) vintages from both OLD and NEW sources.

    This consolidated runner processes both:
    - OLD CSV files (pre-2013 data) from old_weekly_reports/
    - NEW PDF files (2013+ data) from shortened_pdfs/

    Output structure: vintages/table_2/YYYY/ns-XX-YYYY.parquet

    Args:
        old_csv_folder: Path to OLD CSV files (by year)
        new_pdf_folder: Path to NEW (shortened) PDF files
        output_folder: Output root (e.g., data/output/vintages/table_2)
        pipeline_version: Pipeline version string for metadata
        force: If True, reprocess all files regardless of timestamps

    Returns:
        Dictionary with processing statistics

    Raises:
        FileNotFoundError: If input folders don't exist
        ValueError: If validation fails
    """
    start_time = time.time()
    stats = {
        'old_processed': 0,
        'new_processed': 0,
        'old_skipped': 0,
        'new_skipped': 0,
    }

    logger.info("=" * 70)
    logger.info("Building Table 2 vintages (quarterly/annual GDP)")
    logger.info("=" * 70)

    # Validate inputs
    old_csv_path = Path(old_csv_folder)
    if (old_csv_path / "table_2").exists():
        old_csv_path = old_csv_path / "table_2"
    new_pdf_path = Path(new_pdf_folder)
    output_path = Path(output_folder)

    if old_csv_path.exists():
        validate_input_exists(old_csv_path, "Table 2 OLD CSV")
    else:
        logger.warning(f"OLD CSV folder not found: {old_csv_path} - skipping OLD data")

    if new_pdf_path.exists():
        validate_input_exists(new_pdf_path, "Table 2 NEW PDF")
    else:
        logger.warning(f"NEW PDF folder not found: {new_pdf_path} - skipping NEW data")

    # Create output directory
    output_path.mkdir(parents=True, exist_ok=True)

    # Process OLD CSV files (timestamp-based, no record files needed)
    if old_csv_path.exists():
        logger.info("Processing OLD CSV files (pre-2013)...")
        old_stats = _process_old_csv_table_2(
            str(old_csv_path),
            output_folder,
            pipeline_version,
            persist_format,
            force,
        )
        stats['old_processed'] = old_stats['processed']
        stats['old_skipped'] = old_stats['skipped']

    # Process NEW PDF files (timestamp-based, no record files needed)
    if new_pdf_path.exists():
        logger.info("Processing NEW PDF files (2013+)...")
        new_stats = _process_new_pdf_table_2(
            new_pdf_folder,
            output_folder,
            pipeline_version,
            persist_format,
            force,
        )
        stats['new_processed'] = new_stats['processed']
        stats['new_skipped'] = new_stats['skipped']

    # Summary
    stats['total_processed'] = stats['old_processed'] + stats['new_processed']
    elapsed = round(time.time() - start_time)

    logger.info("=" * 70)
    logger.info("Table 2 Processing Summary:")
    logger.info(f"  OLD CSV: {stats['old_processed']} processed, {stats['old_skipped']} skipped")
    logger.info(f"  NEW PDF: {stats['new_processed']} processed, {stats['new_skipped']} skipped")
    logger.info(f"  TOTAL: {stats['total_processed']} vintages created")
    logger.info(f"  Time: {elapsed} seconds")
    logger.info("=" * 70)

    return stats


def _process_old_csv_table_1(
    old_csv_folder: str,
    output_folder: str,
    pipeline_version: str,
    persist_format: str,
    force: bool,
) -> Dict[str, int]:
    """Process OLD CSV files for Table 1 using timestamp-based incremental processing."""
    from peru_gdp_rtd.orchestration.validation import needs_processing

    stats = {'processed': 0, 'skipped': 0}
    old_csv_path = Path(old_csv_folder)
    prep = VintagesPreparator()
    cleaner = OldTableCleaner()

    # Find all year folders
    year_folders = sorted([
        f for f in old_csv_path.iterdir()
        if f.is_dir() and f.name.isdigit()
    ])

    for year_folder in year_folders:
        year = year_folder.name
        output_year_folder = Path(output_folder) / year
        output_year_folder.mkdir(parents=True, exist_ok=True)
        month_order_map = prep.build_month_order_map(str(year_folder), extensions=(".csv",))

        # Find all CSV files in this year
        csv_files = sorted(year_folder.glob("*.csv"))

        for csv_file in csv_files:
            ext = "parquet" if persist_format.lower() == "parquet" else "csv"
            output_file = output_year_folder / f"{csv_file.stem}.{ext}"

            # Check if processing needed (timestamp-based)
            if not needs_processing(csv_file, output_file, force):
                stats['skipped'] += 1
                continue

            try:
                # Extract table
                raw_table = pd.read_csv(csv_file, sep=";", encoding="utf-8")

                # Clean table
                clean_table = cleaner.clean_table_1(raw_table)
                issue, yr = parse_ns_meta(csv_file.name)
                if not issue or not yr:
                    logger.error(f"Failed to parse WR metadata from {csv_file.name}")
                    stats['skipped'] += 1
                    continue
                if month_order_map.get(csv_file.name) is None:
                    logger.error(f"Missing month order mapping for {csv_file.name}")
                    stats['skipped'] += 1
                    continue
                clean_table.insert(0, "year", int(yr))
                clean_table.insert(1, "wr", int(issue))

                # Convert to vintage format
                vintage = prep.prepare_table_1(clean_table, csv_file.name, month_order_map)
                vintage.attrs["pipeline_version"] = pipeline_version

                # Validate
                validate_rtd_dataframe(vintage, f"Table 1 OLD {csv_file.name}")

                # Save
                if persist_format.lower() == "csv":
                    vintage.to_csv(output_file, index=False)
                else:
                    vintage.to_parquet(output_file, index=False)
                validate_output_created(output_file, f"Table 1 OLD {csv_file.name}")

                stats['processed'] += 1
                logger.debug(f"Processed: {csv_file.name}")

            except Exception as e:
                logger.error(f"Failed to process {csv_file.name}: {e}")
                continue

    return stats


def _process_new_pdf_table_1(
    new_pdf_folder: str,
    output_folder: str,
    pipeline_version: str,
    persist_format: str,
    force: bool,
) -> Dict[str, int]:
    """Process NEW PDF files for Table 1 using timestamp-based incremental processing."""
    from peru_gdp_rtd.orchestration.validation import needs_processing

    stats = {'processed': 0, 'skipped': 0}
    new_pdf_path = Path(new_pdf_folder)
    prep = VintagesPreparator()
    cleaner = NewTableCleaner()

    # Find all PDF files
    pdf_files = sorted(new_pdf_path.rglob("*.pdf"))
    month_order_map = _build_month_order_map_from_files(pdf_files)

    for pdf_file in pdf_files:
        # Determine year from filename
        issue, yr = parse_ns_meta(pdf_file.name)
        if not issue or not yr:
            logger.error(f"Failed to parse WR metadata from {pdf_file.name}")
            stats['skipped'] += 1
            continue
        year = str(yr)
        if month_order_map.get(pdf_file.name) is None:
            logger.error(f"Missing month order mapping for {pdf_file.name}")
            stats['skipped'] += 1
            continue

        output_year_folder = Path(output_folder) / year
        output_year_folder.mkdir(parents=True, exist_ok=True)
        ext = "parquet" if persist_format.lower() == "parquet" else "csv"
        output_file = output_year_folder / f"{pdf_file.stem}.{ext}"

        # Check if processing needed (timestamp-based)
        if not needs_processing(pdf_file, output_file, force):
            stats['skipped'] += 1
            continue

        try:
            # Extract table
            raw_table = extract_table(str(pdf_file), page=1)
            if raw_table is None:
                logger.error(f"No table extracted from {pdf_file.name} page 1")
                stats['skipped'] += 1
                continue

            # Clean table
            clean_table = cleaner.clean_table_1(raw_table)
            clean_table.insert(0, "year", int(yr))
            clean_table.insert(1, "wr", int(issue))

            # Convert to vintage format
            vintage = prep.prepare_table_1(clean_table, pdf_file.name, month_order_map)
            vintage.attrs["pipeline_version"] = pipeline_version

            # Validate
            validate_rtd_dataframe(vintage, f"Table 1 NEW {pdf_file.name}")

            # Save
            if persist_format.lower() == "csv":
                vintage.to_csv(output_file, index=False)
            else:
                vintage.to_parquet(output_file, index=False)
            validate_output_created(output_file, f"Table 1 NEW {pdf_file.name}")

            stats['processed'] += 1
            logger.debug(f"Processed: {pdf_file.name}")

        except Exception as e:
            logger.error(f"Failed to process {pdf_file.name}: {e}")
            continue

    return stats


def _process_old_csv_table_2(
    old_csv_folder: str,
    output_folder: str,
    pipeline_version: str,
    persist_format: str,
    force: bool,
) -> Dict[str, int]:
    """Process OLD CSV files for Table 2 using timestamp-based incremental processing."""
    from peru_gdp_rtd.orchestration.validation import needs_processing

    stats = {'processed': 0, 'skipped': 0}
    old_csv_path = Path(old_csv_folder)
    prep = VintagesPreparator()
    cleaner = OldTableCleaner()

    # Find all year folders
    year_folders = sorted([
        f for f in old_csv_path.iterdir()
        if f.is_dir() and f.name.isdigit()
    ])

    for year_folder in year_folders:
        year = year_folder.name
        output_year_folder = Path(output_folder) / year
        output_year_folder.mkdir(parents=True, exist_ok=True)
        month_order_map = prep.build_month_order_map(str(year_folder), extensions=(".csv",))

        # Find all CSV files in this year
        csv_files = sorted(year_folder.glob("*.csv"))

        for csv_file in csv_files:
            ext = "parquet" if persist_format.lower() == "parquet" else "csv"
            output_file = output_year_folder / f"{csv_file.stem}.{ext}"

            # Check if processing needed (timestamp-based)
            if not needs_processing(csv_file, output_file, force):
                stats['skipped'] += 1
                continue

            try:
                # Extract table
                raw_table = pd.read_csv(csv_file, sep=";", encoding="utf-8")

                # Clean table
                clean_table = cleaner.clean_table_2(raw_table)
                issue, yr = parse_ns_meta(csv_file.name)
                if not issue or not yr:
                    logger.error(f"Failed to parse WR metadata from {csv_file.name}")
                    stats['skipped'] += 1
                    continue
                if month_order_map.get(csv_file.name) is None:
                    logger.error(f"Missing month order mapping for {csv_file.name}")
                    stats['skipped'] += 1
                    continue
                clean_table.insert(0, "year", int(yr))
                clean_table.insert(1, "wr", int(issue))

                # Convert to vintage format
                vintage = prep.prepare_table_2(clean_table, csv_file.name, month_order_map)
                vintage.attrs["pipeline_version"] = pipeline_version

                # Validate
                validate_rtd_dataframe(vintage, f"Table 2 OLD {csv_file.name}")

                # Save
                if persist_format.lower() == "csv":
                    vintage.to_csv(output_file, index=False)
                else:
                    vintage.to_parquet(output_file, index=False)
                validate_output_created(output_file, f"Table 2 OLD {csv_file.name}")

                stats['processed'] += 1
                logger.debug(f"Processed: {csv_file.name}")

            except Exception as e:
                logger.error(f"Failed to process {csv_file.name}: {e}")
                continue

    return stats


def _process_new_pdf_table_2(
    new_pdf_folder: str,
    output_folder: str,
    pipeline_version: str,
    persist_format: str,
    force: bool,
) -> Dict[str, int]:
    """Process NEW PDF files for Table 2 using timestamp-based incremental processing."""
    from peru_gdp_rtd.orchestration.validation import needs_processing

    stats = {'processed': 0, 'skipped': 0}
    new_pdf_path = Path(new_pdf_folder)
    prep = VintagesPreparator()
    cleaner = NewTableCleaner()

    # Find all PDF files
    pdf_files = sorted(new_pdf_path.rglob("*.pdf"))
    month_order_map = _build_month_order_map_from_files(pdf_files)

    for pdf_file in pdf_files:
        # Determine year from filename
        issue, yr = parse_ns_meta(pdf_file.name)
        if not issue or not yr:
            logger.error(f"Failed to parse WR metadata from {pdf_file.name}")
            stats['skipped'] += 1
            continue
        year = str(yr)
        if month_order_map.get(pdf_file.name) is None:
            logger.error(f"Missing month order mapping for {pdf_file.name}")
            stats['skipped'] += 1
            continue

        output_year_folder = Path(output_folder) / year
        output_year_folder.mkdir(parents=True, exist_ok=True)
        ext = "parquet" if persist_format.lower() == "parquet" else "csv"
        output_file = output_year_folder / f"{pdf_file.stem}.{ext}"

        # Check if processing needed (timestamp-based)
        if not needs_processing(pdf_file, output_file, force):
            stats['skipped'] += 1
            continue

        try:
            # Extract table
            raw_table = extract_table(str(pdf_file), page=2)
            if raw_table is None:
                logger.error(f"No table extracted from {pdf_file.name} page 2")
                stats['skipped'] += 1
                continue

            # Clean table
            clean_table = cleaner.clean_table_2(raw_table)
            clean_table.insert(0, "year", int(yr))
            clean_table.insert(1, "wr", int(issue))

            # Convert to vintage format
            vintage = prep.prepare_table_2(clean_table, pdf_file.name, month_order_map)
            vintage.attrs["pipeline_version"] = pipeline_version

            # Validate
            validate_rtd_dataframe(vintage, f"Table 2 NEW {pdf_file.name}")

            # Save
            if persist_format.lower() == "csv":
                vintage.to_csv(output_file, index=False)
            else:
                vintage.to_parquet(output_file, index=False)
            validate_output_created(output_file, f"Table 2 NEW {pdf_file.name}")

            stats['processed'] += 1
            logger.debug(f"Processed: {pdf_file.name}")

        except Exception as e:
            logger.error(f"Failed to process {pdf_file.name}: {e}")
            continue

    return stats
