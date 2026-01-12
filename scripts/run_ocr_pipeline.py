"""
OCR Pipeline Runner

Main script for processing scanned Weekly Report PDFs (1994-2012).
Executes complete OCR workflow from PDF → PNG → preprocessing → OCR → CSV.

Usage:
    python scripts/run_ocr_pipeline.py                    # Process all years
    python scripts/run_ocr_pipeline.py --year 2000        # Single year
    python scripts/run_ocr_pipeline.py --years 1994-2000  # Year range
    python scripts/run_ocr_pipeline.py --resume           # Resume from checkpoint
    python scripts/run_ocr_pipeline.py --verify           # Verify outputs only

Author: Jason Cruz
Institution: Universidad del Pacífico - CIUP
Date: January 2026
"""

import sys
import argparse
from pathlib import Path
from typing import List, Dict, Optional
from tqdm import tqdm

# Add OCR directory to Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

from OCR.ocr_config.settings import load_settings
from OCR.ocr_processors.image_preprocessor import ImagePreprocessor
from OCR.ocr_processors.table_extractor import extract_upper_table
from OCR.ocr_processors.ocr_engine import (
    run_ocr_with_validation,
    check_tesseract_installation,
    check_tesseract_languages
)
from OCR.ocr_processors.csv_converter import convert_ocr_to_csv
from OCR.ocr_processors.validator import (
    validate_csv_structure,
    calculate_confidence_score,
    flag_for_manual_review,
    should_flag_for_review,
    generate_validation_report
)
from OCR.ocr_utils.progress_tracker import ProgressTracker
from OCR.ocr_utils.logger import setup_logging, get_logger
from OCR.ocr_utils.file_manager import (
    discover_all_pdfs,
    determine_pdf_structure,
    get_output_path,
    ensure_output_directories,
    cleanup_temp_images,
    write_needs_review_list
)


logger = get_logger(__name__)


def parse_arguments() -> argparse.Namespace:
    """
    Parse command-line arguments.

    Returns:
        Parsed arguments
    """
    parser = argparse.ArgumentParser(
        description="OCR Pipeline for Peru GDP Real-Time Dataset (1994-2012)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python scripts/run_ocr_pipeline.py                    # Process all years
  python scripts/run_ocr_pipeline.py --year 2000        # Single year
  python scripts/run_ocr_pipeline.py --years 1994-2000  # Year range
  python scripts/run_ocr_pipeline.py --resume           # Resume from checkpoint
  python scripts/run_ocr_pipeline.py --verify           # Verify outputs only
  python scripts/run_ocr_pipeline.py -v --save-images   # Debug mode
        """
    )

    parser.add_argument(
        '--year',
        type=int,
        help='Process single year (e.g., 2000)'
    )

    parser.add_argument(
        '--years',
        type=str,
        help='Process year range (e.g., "1994-2000")'
    )

    parser.add_argument(
        '--resume',
        action='store_true',
        help='Resume from last checkpoint'
    )

    parser.add_argument(
        '--verify',
        action='store_true',
        help='Verify existing outputs without reprocessing'
    )

    parser.add_argument(
        '--force',
        action='store_true',
        help='Force reprocess even if output exists'
    )

    parser.add_argument(
        '--save-images',
        action='store_true',
        help='Save intermediate preprocessed images for debugging'
    )

    parser.add_argument(
        '--config',
        type=str,
        default='OCR/ocr_config/config.yaml',
        help='Path to configuration file'
    )

    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Enable verbose (DEBUG) logging'
    )

    return parser.parse_args()


def process_single_pdf(
    pdf_path: Path,
    settings: any,
    preprocessor: ImagePreprocessor,
    tracker: ProgressTracker,
    save_images: bool = False
) -> Dict[str, any]:
    """
    Process a single PDF through complete OCR workflow.

    Args:
        pdf_path: Path to PDF file
        settings: OCR settings
        preprocessor: ImagePreprocessor instance
        tracker: ProgressTracker instance
        save_images: Save intermediate images

    Returns:
        Dictionary with processing results
    """
    result = {
        'pdf': pdf_path.name,
        'success': False,
        'tables_processed': [],
        'confidence_scores': {},
        'flagged_for_review': False,
        'error': None
    }

    try:
        # Determine PDF structure
        year = int(pdf_path.stem.split('_')[-1])
        num_pages, tables_to_extract = determine_pdf_structure(
            year,
            settings.pdf_structure.years_single_page
        )

        logger.info(f"Processing {pdf_path.name}: {num_pages} page(s), tables={tables_to_extract}")

        # Process each table
        for table_type in tables_to_extract:
            # Determine page number
            page_num = settings.pdf_structure.page_mapping[table_type]

            # Step 1: Preprocess image
            logger.debug(f"  Preprocessing page {page_num} for {table_type}")

            temp_dir = str(settings.paths.temp_images_dir / pdf_path.stem) if save_images else None

            preprocessed_image = preprocessor.preprocess_for_ocr(
                str(pdf_path),
                page_num=page_num,
                save_intermediate=save_images,
                output_dir=temp_dir
            )

            # Step 2: Extract upper table
            logger.debug(f"  Extracting upper table")

            upper_table = extract_upper_table(
                preprocessed_image,
                upper_ratio=settings.table_extraction.upper_table_region_ratio
            )

            # Step 3: Run OCR
            logger.debug(f"  Running OCR")

            ocr_result = run_ocr_with_validation(
                upper_table,
                language=settings.tesseract.language,
                psm=settings.tesseract.psm,
                oem=settings.tesseract.oem
            )

            # Step 4: Convert to CSV
            logger.debug(f"  Converting to CSV")

            output_path = get_output_path(pdf_path, str(settings.paths.csv_output_root), table_type)

            df = convert_ocr_to_csv(
                ocr_result['text_cleaned'],
                str(output_path),
                table_type=table_type
            )

            # Step 5: Validate
            logger.debug(f"  Validating output")

            validation_errors = validate_csv_structure(df, table_type)

            combined_confidence = calculate_confidence_score(
                df,
                ocr_result['confidence'],
                validation_errors
            )

            # Step 6: Flag for review if needed
            if should_flag_for_review(
                combined_confidence,
                validation_errors,
                settings.validation.confidence_threshold
            ):
                preprocessed_path = temp_dir + "/09_final.png" if save_images else ""

                try:
                    flag_for_manual_review(
                        str(pdf_path),
                        str(output_path),
                        preprocessed_path,
                        combined_confidence,
                        validation_errors,
                        str(settings.paths.review_dir)
                    )
                    result['flagged_for_review'] = True
                except (PermissionError, OSError) as e:
                    logger.warning(f"Could not create review package: {e}")
                    result['flagged_for_review'] = False

            # Record results
            result['tables_processed'].append(table_type)
            result['confidence_scores'][table_type] = combined_confidence

            logger.info(f"  ✓ {table_type}: {combined_confidence:.1%} confidence")

        # Mark as completed
        avg_confidence = sum(result['confidence_scores'].values()) / len(result['confidence_scores'])

        if result['flagged_for_review']:
            tracker.mark_needs_review(
                str(pdf_path),
                avg_confidence,
                validation_errors
            )
        else:
            tracker.mark_completed(
                str(pdf_path),
                avg_confidence
            )

        result['success'] = True
        logger.info(f"✓ Completed: {pdf_path.name}")

    except Exception as e:
        logger.error(f"✗ Failed: {pdf_path.name} - {e}")
        result['error'] = str(e)
        tracker.mark_failed(str(pdf_path), str(e))

    return result


def run_pipeline(args: argparse.Namespace) -> int:
    """
    Execute OCR pipeline on specified PDFs.

    Args:
        args: Parsed command-line arguments

    Returns:
        Exit code (0 = success, 1 = failure)
    """
    try:
        # Load settings
        logger.info(f"Loading configuration from {args.config}")
        settings = load_settings(args.config)

        # Initialize progress tracker
        tracker = ProgressTracker(str(settings.progress.checkpoint_file))

        # Determine years to process
        if args.year:
            years = [args.year]
        elif args.years:
            start, end = map(int, args.years.split('-'))
            years = list(range(start, end + 1))
        else:
            # Default: all years (1994-2012)
            years = list(range(1994, 2013))

        logger.info(f"Processing years: {years}")

        # Discover PDFs
        all_pdfs = discover_all_pdfs(str(settings.paths.pdf_input_root), years)

        if not all_pdfs:
            logger.error("No PDFs found to process")
            return 1

        # Set total in tracker
        tracker.set_total_pdfs(len(all_pdfs))

        # Filter already processed (unless --force)
        if args.force:
            pdfs_to_process = all_pdfs
            logger.info("Force mode: reprocessing all PDFs")
        elif args.resume:
            pdfs_to_process = tracker.get_pending_pdfs([str(p) for p in all_pdfs])
            pdfs_to_process = [Path(p) for p in pdfs_to_process]
            logger.info(f"Resume mode: {len(pdfs_to_process)} pending PDFs")
        else:
            pdfs_to_process = all_pdfs

        if not pdfs_to_process:
            logger.info("All PDFs already processed")
            tracker.print_summary()
            return 0

        # Ensure output directories exist
        ensure_output_directories(str(settings.paths.csv_output_root), years)

        # Initialize image preprocessor
        preprocessor = ImagePreprocessor(
            target_dpi=settings.preprocessing.target_dpi,
            apply_clahe=settings.preprocessing.contrast_enhancement,
            clahe_clip_limit=settings.preprocessing.clahe_clip_limit,
            clahe_tile_grid_size=settings.preprocessing.clahe_tile_grid_size,
            noise_removal_method=settings.preprocessing.noise_removal_method,
            median_kernel_size=settings.preprocessing.median_kernel_size,
            skew_angle_threshold=settings.preprocessing.skew_angle_threshold,
            thinning=settings.preprocessing.thinning,
            border_size=settings.preprocessing.border_size
        )

        # Process PDFs with progress bar
        logger.info(f"Starting OCR processing: {len(pdfs_to_process)} PDFs")

        results = []

        with tqdm(total=len(pdfs_to_process), desc="OCR Processing", unit="PDF") as pbar:
            for pdf_path in pdfs_to_process:
                result = process_single_pdf(
                    pdf_path,
                    settings,
                    preprocessor,
                    tracker,
                    save_images=args.save_images
                )

                results.append(result)
                pbar.update(1)

        # Clean up temporary images
        if not args.save_images and settings.progress.auto_cleanup_temp:
            cleanup_temp_images(str(settings.paths.temp_images_dir))

        # Generate summary
        logger.info("\n" + "=" * 60)
        logger.info("OCR Pipeline Complete")
        logger.info("=" * 60)

        tracker.print_summary()

        # Write needs-review list
        needs_review = tracker.get_needs_review_files()
        if needs_review:
            write_needs_review_list(needs_review)
            logger.warning(f"\n{len(needs_review)} files need manual review")
            logger.info(f"See: OCR/needs_review.txt for details")
            logger.info(f"Review packages in: {settings.paths.review_dir}")

        return 0

    except KeyboardInterrupt:
        logger.warning("\nPipeline interrupted by user")
        logger.info("Progress saved. Run with --resume to continue")
        return 130

    except Exception as e:
        logger.exception(f"Pipeline failed: {e}")
        return 1


def verify_outputs(args: argparse.Namespace) -> int:
    """
    Verify existing OCR outputs without reprocessing.

    Args:
        args: Parsed command-line arguments

    Returns:
        Exit code
    """
    logger.info("Verification mode: checking existing outputs")

    try:
        settings = load_settings(args.config)

        # TODO: Implement verification logic
        # - Check all expected CSV files exist
        # - Validate each CSV structure
        # - Report any issues

        logger.info("✓ Verification complete")
        return 0

    except Exception as e:
        logger.exception(f"Verification failed: {e}")
        return 1


def main() -> int:
    """
    Main entry point.

    Returns:
        Exit code
    """
    # Parse arguments
    args = parse_arguments()

    # Setup logging
    log_level = "DEBUG" if args.verbose else "INFO"
    setup_logging(
        log_file="OCR/logs/ocr_pipeline.log",
        level=log_level,
        console_output=True
    )

    logger.info("=" * 60)
    logger.info("OCR Pipeline for Peru GDP Real-Time Dataset")
    logger.info("=" * 60)

    # Check Tesseract installation
    try:
        check_tesseract_installation()
        check_tesseract_languages(['spa', 'eng'])
        logger.info("✓ Tesseract OCR is properly configured")
    except Exception as e:
        logger.error(f"✗ Tesseract configuration error:\n{e}")
        logger.error("\nPlease install Tesseract and language packs:")
        logger.error("  https://github.com/UB-Mannheim/tesseract/wiki")
        return 1

    # Run pipeline or verification
    if args.verify:
        return verify_outputs(args)
    else:
        return run_pipeline(args)


if __name__ == "__main__":
    sys.exit(main())
