"""Validation utilities for Peru GDP RTD pipeline.

This module provides validation functions for data quality checks
and incremental processing decisions.
"""

import os
from pathlib import Path
from typing import List, Optional
import pandas as pd
import logging

logger = logging.getLogger(__name__)


def validate_rtd_dataframe(
    df: pd.DataFrame,
    stage_name: str,
    required_columns: Optional[List[str]] = None,
    min_rows: int = 1,
) -> None:
    """Validate RTD DataFrame meets quality requirements.

    Args:
        df: DataFrame to validate
        stage_name: Name of processing stage (for error messages)
        required_columns: List of columns that must be present
        min_rows: Minimum number of rows required

    Raises:
        ValueError: If validation fails
    """
    if required_columns is None:
        required_columns = ["industry", "vintage"]

    # Check not empty
    if len(df) < min_rows:
        raise ValueError(
            f"{stage_name}: DataFrame has {len(df)} rows, expected at least {min_rows}"
        )

    # Check required columns
    missing = set(required_columns) - set(df.columns)
    if missing:
        raise ValueError(f"{stage_name}: Missing required columns: {missing}")

    # Check for null values in key columns
    for col in required_columns:
        null_count = df[col].isna().sum()
        if null_count > 0:
            raise ValueError(
                f"{stage_name}: Column '{col}' has {null_count} null values"
            )

    # Check for target period columns (tp_*)
    tp_cols = [c for c in df.columns if c.startswith("tp_")]
    if not tp_cols:
        raise ValueError(f"{stage_name}: No target period columns (tp_*) found")

    logger.debug(
        f"{stage_name} validation passed: {df.shape[0]} rows, "
        f"{len(tp_cols)} target periods"
    )


def needs_processing(
    source_file: Path,
    output_file: Path,
    force: bool = False,
) -> bool:
    """Determine if source file needs (re)processing.

    Uses timestamp-based comparison: process if output doesn't exist
    or is older than source.

    Args:
        source_file: Input file path
        output_file: Output file path
        force: If True, always return True (force reprocessing)

    Returns:
        True if processing is needed, False otherwise
    """
    if force:
        logger.debug(f"Force reprocessing: {source_file.name}")
        return True

    if not output_file.exists():
        logger.debug(f"Output missing, need to process: {source_file.name}")
        return True

    source_mtime = source_file.stat().st_mtime
    output_mtime = output_file.stat().st_mtime

    if source_mtime > output_mtime:
        logger.debug(f"Source newer than output: {source_file.name}")
        return True

    logger.debug(f"Output up-to-date: {source_file.name}")
    return False


def validate_input_exists(
    input_path: Path,
    stage_name: str,
) -> None:
    """Validate that input path exists.

    Args:
        input_path: Path to validate
        stage_name: Name of processing stage (for error messages)

    Raises:
        FileNotFoundError: If input path doesn't exist
    """
    if not input_path.exists():
        raise FileNotFoundError(
            f"{stage_name}: Input path not found: {input_path}"
        )

    logger.debug(f"{stage_name}: Input validated: {input_path}")


def validate_output_created(
    output_path: Path,
    stage_name: str,
) -> None:
    """Validate that output was created successfully.

    Args:
        output_path: Expected output path
        stage_name: Name of processing stage (for error messages)

    Raises:
        FileNotFoundError: If output was not created
    """
    if not output_path.exists():
        raise FileNotFoundError(
            f"{stage_name}: Output file was not created: {output_path}"
        )

    # Check file is not empty
    if output_path.stat().st_size == 0:
        raise ValueError(
            f"{stage_name}: Output file is empty: {output_path}"
        )

    logger.debug(
        f"{stage_name}: Output validated: {output_path} "
        f"({output_path.stat().st_size:,} bytes)"
    )
