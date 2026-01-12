"""
Concatenation utilities for merging vintage datasets into unified RTD.

This module provides functions to concatenate vintage-format GDP tables across
years and sources (OLD + NEW) into a unified Real-Time Dataset. Handles column
alignment, chronological ordering, and type enforcement.
"""

import os
import re
import time
from typing import List, Optional

import pandas as pd


def target_period_monthly_sort_key(tp: str) -> tuple:
    """
    Convert monthly target period to (year, month) tuple for sorting.

    Args:
        tp: Target period in format 'tp_YYYYmM' or 'YYYYmM'.

    Returns:
        Tuple of (year, month) for sorting, or (9999, 0) for unmatched patterns.

    Example:
        >>> target_period_monthly_sort_key("tp_2017m7")
        (2017, 7)
        >>> target_period_monthly_sort_key("2017m12")
        (2017, 12)
    """
    if tp.startswith("tp_"):
        tp = tp[3:]
    m = re.match(r"(\d{4})m(\d+)", tp)
    if m:
        return (int(m.group(1)), int(m.group(2)))
    return (9999, 0)


def target_period_quarterly_sort_key(col: str) -> tuple:
    """
    Convert quarterly/annual target period to (year, type, quarter) for sorting.

    Quarterly periods are sorted before annual periods within each year.

    Args:
        col: Target period in format 'tp_YYYYqN' or 'tp_YYYY'.

    Returns:
        Tuple of (year, type_flag, quarter) for sorting.
        - type_flag: 0 for quarters, 1 for annual
        - Returns (9999, 9, col) for unmatched patterns

    Example:
        >>> target_period_quarterly_sort_key("tp_2017q1")
        (2017, 0, 1)
        >>> target_period_quarterly_sort_key("tp_2017")
        (2017, 1, 0)
    """
    if not col.startswith("tp_"):
        return (9999, 9, col)

    body = col[3:]  # Remove 'tp_' prefix

    # Match quarterly pattern: '2017q1'
    m = re.match(r"^(\d{4})q(\d)$", body)
    if m:
        year = int(m.group(1))
        q = int(m.group(2))
        return (year, 0, q)  # Quarters first (type_flag=0)

    # Match annual pattern: '2017'
    m2 = re.match(r"^(\d{4})$", body)
    if m2:
        year = int(m2.group(1))
        return (year, 1, 0)  # Annual after quarters (type_flag=1)

    return (9999, 9, col)


def concatenate_table_1(
    input_data_subfolder: str,
    persist: bool = False,
    persist_folder: Optional[str] = None,
    csv_file_label: Optional[str] = None,
    persist_format: str = "csv",
    force: bool = False,
) -> pd.DataFrame:
    """
    Concatenate all Table 1 (monthly GDP) vintage files into unified RTD.

    Performs row-based concatenation of monthly GDP vintages:
    1. Loads all CSV/Parquet files from year subfolders under table_1/
    2. Builds union of all tp_* columns across files
    3. Sorts tp_* columns chronologically
    4. Reindexes all DataFrames to match full column schema
    5. Vertically concatenates all data
    6. Enforces consistent dtypes
    7. Optionally persists unified RTD to disk

    Args:
        input_data_subfolder: Root folder containing table_1/ subfolder with year folders.
        persist: If True, save unified RTD to disk.
        persist_folder: Folder for saving output (default: same as input_data_subfolder).
        csv_file_label: Custom filename for output (default: 'monthly_gdp_vintages.csv').
        force: If True, reprocess all files regardless of timestamps.

    Returns:
        Unified RTD DataFrame with columns: industry, vintage, tp_YYYYmM...

    Example:
        >>> unified = concatenate_table_1(
        ...     "./data/input",
        ...     "./record",
        ...     "concat_table_1.txt",
        ...     persist=True
        ... )
        >>> print(f"Unified RTD shape: {unified.shape}")
    """
    from pathlib import Path

    start_time = time.time()
    print("\n>> Starting Table 1 concatenation (monthly GDP)...")

    # Determine output path
    output_folder = persist_folder or input_data_subfolder
    output_filename = csv_file_label or "monthly_gdp_vintages.csv"
    output_path = Path(output_folder) / output_filename
    if output_path.suffix:
        output_path = output_path.with_suffix(f".{persist_format}")
    else:
        output_path = output_path.with_name(f"{output_path.name}.{persist_format}")

    # Look for table_1 data in new unified structure
    table_1_folder = os.path.join(input_data_subfolder, "table_1")

    if not os.path.exists(table_1_folder):
        elapsed_time = round(time.time() - start_time)
        print(f"WARNING: Table 1 folder not found: {table_1_folder}")
        print("\n>> Summary (Concatenate Table 1):")
        print(">> Status: skipped (input folder missing)")
        print(f">> Input folder: {table_1_folder}")
        print(f">> Output file: {output_path}")
        print(">> Year folders found: 0")
        print(">> Input files available: 0")
        print(">> Files processed: 0")
        print(">> Final shape: (0, 0)")
        print(f">> Time elapsed: {elapsed_time} seconds")
        return pd.DataFrame()

    print(f">> Input folder: {table_1_folder}")

    # Collect all year folders and input files
    year_folders = sorted(
        [
            f
            for f in os.listdir(table_1_folder)
            if f.isdigit() and os.path.isdir(os.path.join(table_1_folder, f))
        ],
        key=int,
    )

    all_input_files = []
    for year in year_folders:
        year_folder = os.path.join(table_1_folder, year)
        files = sorted([f for f in os.listdir(year_folder) if f.endswith((".csv", ".parquet"))])
        all_input_files.extend([Path(year_folder) / f for f in files])

    if not all_input_files:
        elapsed_time = round(time.time() - start_time)
        print("WARNING: No input files found to concatenate.")
        print("\n>> Summary (Concatenate Table 1):")
        print(">> Status: skipped (no input files)")
        print(f">> Input folder: {table_1_folder}")
        print(f">> Output file: {output_path}")
        print(f">> Year folders found: {len(year_folders)}")
        print(">> Input files available: 0")
        print(">> Files processed: 0")
        print(">> Final shape: (0, 0)")
        print(f">> Time elapsed: {elapsed_time} seconds")
        return pd.DataFrame()

    # Check if concatenation needed (timestamp-based)
    if not force and output_path.exists():
        output_mtime = output_path.stat().st_mtime
        needs_update = any(f.stat().st_mtime > output_mtime for f in all_input_files if f.exists())

        if not needs_update:
            print(f">> Output up-to-date: {output_path}")
            print(">> Skipping concatenation (use force=True to reprocess)")
            unified_df = (
                pd.read_parquet(output_path)
                if output_path.suffix == ".parquet"
                else pd.read_csv(output_path)
            )
            elapsed_time = round(time.time() - start_time)
            print("\n>> Summary (Concatenate Table 1):")
            print(">> Status: skipped (output up-to-date)")
            print(f">> Input folder: {table_1_folder}")
            print(f">> Output file: {output_path}")
            print(f">> Year folders found: {len(year_folders)}")
            print(f">> Input files available: {len(all_input_files)}")
            print(">> Files processed: 0")
            print(f">> Final shape: {unified_df.shape}")
            print(f">> Time elapsed: {elapsed_time} seconds")
            return unified_df

    loaded_dfs: List[pd.DataFrame] = []
    file_counter = 0

    for full_path in all_input_files:
        file = full_path.name
        try:
            if file.endswith(".parquet"):
                df = pd.read_parquet(full_path)
            else:
                df = pd.read_csv(full_path)

            loaded_dfs.append(df)
            file_counter += 1
        except Exception as e:
            print(f"WARNING: Error loading {file}: {e}")
            continue

    if not loaded_dfs:
        elapsed_time = round(time.time() - start_time)
        print("WARNING: No readable input files found to concatenate.")
        print("\n>> Summary (Concatenate Table 1):")
        print(">> Status: skipped (no readable inputs)")
        print(f">> Input folder: {table_1_folder}")
        print(f">> Output file: {output_path}")
        print(f">> Year folders found: {len(year_folders)}")
        print(f">> Input files available: {len(all_input_files)}")
        print(">> Files processed: 0")
        print(">> Final shape: (0, 0)")
        print(f">> Time elapsed: {elapsed_time} seconds")
        return pd.DataFrame()

    # Build union of all tp_* columns
    base_cols = ["industry", "vintage"]
    all_tp_cols = set()

    for df in loaded_dfs:
        for col in df.columns:
            if col.startswith("tp_"):
                all_tp_cols.add(col)

    # Sort tp_* columns chronologically
    tp_cols_sorted = sorted(list(all_tp_cols), key=target_period_monthly_sort_key)

    # Final column schema
    final_cols = base_cols + tp_cols_sorted

    # Reindex each DataFrame to match full schema
    aligned_dfs = []
    for df in loaded_dfs:
        if "industry" not in df.columns or "vintage" not in df.columns:
            print("WARNING: Skipping DataFrame missing 'industry' or 'vintage' column")
            continue

        df = df.reindex(columns=final_cols)
        aligned_dfs.append(df)

    if not aligned_dfs:
        elapsed_time = round(time.time() - start_time)
        print("WARNING: No valid DataFrames to concatenate.")
        print("\n>> Summary (Concatenate Table 1):")
        print(">> Status: skipped (no valid inputs)")
        print(f">> Input folder: {table_1_folder}")
        print(f">> Output file: {output_path}")
        print(f">> Year folders found: {len(year_folders)}")
        print(f">> Input files available: {len(all_input_files)}")
        print(f">> Files processed: {file_counter}")
        print(">> Final shape: (0, 0)")
        print(f">> Time elapsed: {elapsed_time} seconds")
        return pd.DataFrame()

    # Vertical concatenation
    unified_df = pd.concat(aligned_dfs, axis=0, ignore_index=True)

    # Enforce consistent dtypes
    unified_df["industry"] = unified_df["industry"].astype(str)
    unified_df["vintage"] = unified_df["vintage"].astype(str)

    for col in tp_cols_sorted:
        unified_df[col] = pd.to_numeric(unified_df[col], errors="coerce").astype(float)

    # Persist if requested
    if persist:
        persist_folder = persist_folder or input_data_subfolder
        os.makedirs(persist_folder, exist_ok=True)
        fname = csv_file_label or "gdp_rtd_table_1_unified.csv"
        out_path = Path(persist_folder) / fname
        if out_path.suffix:
            out_path = out_path.with_suffix(f".{persist_format}")
        else:
            out_path = out_path.with_name(f"{out_path.name}.{persist_format}")
        if out_path.suffix == ".parquet":
            unified_df.to_parquet(out_path, index=False)
        else:
            unified_df.to_csv(out_path, index=False)
        print(f">> Unified RTD (Table 1) saved to {out_path}")

    # Summary
    elapsed_time = round(time.time() - start_time)
    output_final = out_path if persist else output_path
    print("\n>> Summary (Concatenate Table 1):")
    print(">> Status: completed")
    print(f">> Input folder: {table_1_folder}")
    print(f">> Output file: {output_final}")
    print(f">> Year folders found: {len(year_folders)}")
    print(f">> Input files available: {len(all_input_files)}")
    print(f">> Files processed: {file_counter}")
    print(f">> Final shape: {unified_df.shape}")
    print(f">> Time elapsed: {elapsed_time} seconds")

    return unified_df


def concatenate_table_2(
    input_data_subfolder: str,
    persist: bool = False,
    persist_folder: Optional[str] = None,
    csv_file_label: Optional[str] = None,
    persist_format: str = "csv",
    force: bool = False,
) -> pd.DataFrame:
    """
    Concatenate all Table 2 (quarterly/annual GDP) vintage files into unified RTD.

    Similar to concatenate_table_1 but handles quarterly and annual target periods.
    Sorts tp_* columns with quarters before annuals within each year.

    Args:
        input_data_subfolder: Root folder containing table_2/ subfolder with year folders.
        persist: If True, save unified RTD to disk.
        persist_folder: Folder for saving output.
        csv_file_label: Custom filename for output (default: 'quarterly_gdp_vintages.csv').
        force: If True, reprocess all files regardless of timestamps.

    Returns:
        Unified RTD DataFrame with columns: industry, vintage, tp_YYYYqN, tp_YYYY...

    Example:
        >>> unified = concatenate_table_2(
        ...     "./data/input",
        ...     "./record",
        ...     "concat_table_2.txt",
        ...     persist=True
        ... )
    """
    from pathlib import Path

    start_time = time.time()
    print("\n>> Starting Table 2 concatenation (quarterly/annual GDP)...")

    # Determine output path
    output_folder = persist_folder or input_data_subfolder
    output_filename = csv_file_label or "quarterly_gdp_vintages.csv"
    output_path = Path(output_folder) / output_filename
    if output_path.suffix:
        output_path = output_path.with_suffix(f".{persist_format}")
    else:
        output_path = output_path.with_name(f"{output_path.name}.{persist_format}")

    # Look for table_2 data in new unified structure
    table_2_folder = os.path.join(input_data_subfolder, "table_2")

    if not os.path.exists(table_2_folder):
        elapsed_time = round(time.time() - start_time)
        print(f"WARNING: Table 2 folder not found: {table_2_folder}")
        print("\n>> Summary (Concatenate Table 2):")
        print(">> Status: skipped (input folder missing)")
        print(f">> Input folder: {table_2_folder}")
        print(f">> Output file: {output_path}")
        print(">> Year folders found: 0")
        print(">> Input files available: 0")
        print(">> Files processed: 0")
        print(">> Final shape: (0, 0)")
        print(f">> Time elapsed: {elapsed_time} seconds")
        return pd.DataFrame()

    print(f">> Input folder: {table_2_folder}")

    # Collect all year folders and input files
    year_folders = sorted(
        [
            f
            for f in os.listdir(table_2_folder)
            if f.isdigit() and os.path.isdir(os.path.join(table_2_folder, f))
        ],
        key=int,
    )

    all_input_files = []
    for year in year_folders:
        year_folder = os.path.join(table_2_folder, year)
        files = sorted([f for f in os.listdir(year_folder) if f.endswith((".csv", ".parquet"))])
        all_input_files.extend([Path(year_folder) / f for f in files])

    if not all_input_files:
        elapsed_time = round(time.time() - start_time)
        print("WARNING: No input files found to concatenate.")
        print("\n>> Summary (Concatenate Table 2):")
        print(">> Status: skipped (no input files)")
        print(f">> Input folder: {table_2_folder}")
        print(f">> Output file: {output_path}")
        print(f">> Year folders found: {len(year_folders)}")
        print(">> Input files available: 0")
        print(">> Files processed: 0")
        print(">> Final shape: (0, 0)")
        print(f">> Time elapsed: {elapsed_time} seconds")
        return pd.DataFrame()

    # Check if concatenation needed (timestamp-based)
    if not force and output_path.exists():
        output_mtime = output_path.stat().st_mtime
        needs_update = any(f.stat().st_mtime > output_mtime for f in all_input_files if f.exists())

        if not needs_update:
            print(f">> Output up-to-date: {output_path}")
            print(">> Skipping concatenation (use force=True to reprocess)")
            unified_df = (
                pd.read_parquet(output_path)
                if output_path.suffix == ".parquet"
                else pd.read_csv(output_path)
            )
            elapsed_time = round(time.time() - start_time)
            print("\n>> Summary (Concatenate Table 2):")
            print(">> Status: skipped (output up-to-date)")
            print(f">> Input folder: {table_2_folder}")
            print(f">> Output file: {output_path}")
            print(f">> Year folders found: {len(year_folders)}")
            print(f">> Input files available: {len(all_input_files)}")
            print(">> Files processed: 0")
            print(f">> Final shape: {unified_df.shape}")
            print(f">> Time elapsed: {elapsed_time} seconds")
            return unified_df

    loaded_dfs: List[pd.DataFrame] = []
    file_counter = 0

    for full_path in all_input_files:
        file = full_path.name
        try:
            if file.endswith(".parquet"):
                df = pd.read_parquet(full_path)
            else:
                df = pd.read_csv(full_path)

            loaded_dfs.append(df)
            file_counter += 1
        except Exception as e:
            print(f"WARNING: Error loading {file}: {e}")
            continue

    if not loaded_dfs:
        elapsed_time = round(time.time() - start_time)
        print("WARNING: No readable input files found to concatenate.")
        print("\n>> Summary (Concatenate Table 2):")
        print(">> Status: skipped (no readable inputs)")
        print(f">> Input folder: {table_2_folder}")
        print(f">> Output file: {output_path}")
        print(f">> Year folders found: {len(year_folders)}")
        print(f">> Input files available: {len(all_input_files)}")
        print(">> Files processed: 0")
        print(">> Final shape: (0, 0)")
        print(f">> Time elapsed: {elapsed_time} seconds")
        return pd.DataFrame()

    # Build union of all tp_* columns
    base_cols = ["industry", "vintage"]
    all_tp_cols = set()

    for df in loaded_dfs:
        for col in df.columns:
            if col.startswith("tp_"):
                all_tp_cols.add(col)

    # Sort tp_* columns: quarters first, then annual for each year
    tp_cols_sorted = sorted(list(all_tp_cols), key=target_period_quarterly_sort_key)

    # Final column schema
    final_cols = base_cols + tp_cols_sorted

    # Reindex each DataFrame to match full schema
    aligned_dfs = []
    for df in loaded_dfs:
        if "industry" not in df.columns or "vintage" not in df.columns:
            print("WARNING: Skipping DataFrame missing 'industry' or 'vintage' column")
            continue

        df = df.reindex(columns=final_cols)
        aligned_dfs.append(df)

    if not aligned_dfs:
        elapsed_time = round(time.time() - start_time)
        print("WARNING: No valid DataFrames to concatenate.")
        print("\n>> Summary (Concatenate Table 2):")
        print(">> Status: skipped (no valid inputs)")
        print(f">> Input folder: {table_2_folder}")
        print(f">> Output file: {output_path}")
        print(f">> Year folders found: {len(year_folders)}")
        print(f">> Input files available: {len(all_input_files)}")
        print(f">> Files processed: {file_counter}")
        print(">> Final shape: (0, 0)")
        print(f">> Time elapsed: {elapsed_time} seconds")
        return pd.DataFrame()

    # Vertical concatenation
    unified_df = pd.concat(aligned_dfs, axis=0, ignore_index=True)

    # Enforce consistent dtypes
    unified_df["industry"] = unified_df["industry"].astype(str)
    unified_df["vintage"] = unified_df["vintage"].astype(str)

    for col in tp_cols_sorted:
        unified_df[col] = pd.to_numeric(unified_df[col], errors="coerce").astype(float)

    # Persist if requested
    if persist:
        persist_folder = persist_folder or input_data_subfolder
        os.makedirs(persist_folder, exist_ok=True)
        fname = csv_file_label or "gdp_rtd_table_2_unified.csv"
        out_path = Path(persist_folder) / fname
        if out_path.suffix:
            out_path = out_path.with_suffix(f".{persist_format}")
        else:
            out_path = out_path.with_name(f"{out_path.name}.{persist_format}")
        if out_path.suffix == ".parquet":
            unified_df.to_parquet(out_path, index=False)
        else:
            unified_df.to_csv(out_path, index=False)
        print(f">> Unified RTD (Table 2) saved to {out_path}")

    # Summary
    elapsed_time = round(time.time() - start_time)
    output_final = out_path if persist else output_path
    print("\n>> Summary (Concatenate Table 2):")
    print(">> Status: completed")
    print(f">> Input folder: {table_2_folder}")
    print(f">> Output file: {output_final}")
    print(f">> Year folders found: {len(year_folders)}")
    print(f">> Input files available: {len(all_input_files)}")
    print(f">> Files processed: {file_counter}")
    print(f">> Final shape: {unified_df.shape}")
    print(f">> Time elapsed: {elapsed_time} seconds")

    return unified_df
