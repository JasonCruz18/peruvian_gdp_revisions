"""
DataFrame cleaning utilities for GDP RTD construction.

This module provides common cleaning functions for both Table 1 and Table 2 extracted
from BCRP Weekly Reports. Includes operations for handling NaNs, row/column manipulation,
text normalization, and sector label standardization.
"""

import re
import unicodedata
from typing import List

import numpy as np
import pandas as pd

from peru_gdp_rtd.cleaners.text_cleaners import remove_rare_characters, remove_tildes


def drop_nan_rows(df: pd.DataFrame) -> pd.DataFrame:
    """
    Drop rows where all values are NaN.

    Args:
        df: DataFrame to clean.

    Returns:
        DataFrame with all-NaN rows removed.
    """
    return df.dropna(how="all")


def drop_nan_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Drop columns where all values are NaN.

    Args:
        df: DataFrame to clean.

    Returns:
        DataFrame with all-NaN columns removed.
    """
    return df.dropna(axis=1, how="all")


def swap_first_second_row(df: pd.DataFrame) -> pd.DataFrame:
    """
    Swap first and second rows in the first and last columns.

    Fixes misplaced headers in certain WR tables.

    Args:
        df: DataFrame to modify.

    Returns:
        DataFrame with swapped rows.
    """
    # Swap first column
    temp = df.iloc[0, 0]
    df.iloc[0, 0] = df.iloc[1, 0]
    df.iloc[1, 0] = temp

    # Swap last column
    temp = df.iloc[0, -1]
    df.iloc[0, -1] = df.iloc[1, -1]
    df.iloc[1, -1] = temp

    return df


def reset_index(df: pd.DataFrame) -> pd.DataFrame:
    """
    Reset DataFrame index after row drops/reorders.

    Args:
        df: DataFrame to reset.

    Returns:
        DataFrame with reset RangeIndex.
    """
    df.reset_index(drop=True, inplace=True)
    return df


def remove_digit_slash(df: pd.DataFrame) -> pd.DataFrame:
    """
    Strip patterns like '12/' at the start of values in first, penultimate, and last columns.

    Args:
        df: DataFrame to clean.

    Returns:
        DataFrame with digit-slash patterns removed.
    """
    df.iloc[:, [0, -2, -1]] = df.iloc[:, [0, -2, -1]].apply(
        lambda x: x.str.replace(r"\d+/", "", regex=True)
    )
    return df


def separate_text_digits(df: pd.DataFrame) -> pd.DataFrame:
    """
    Split alphanumeric tokens in penultimate column into text and numeric parts.

    If the penultimate column mixes letters and digits:
    - Text-only part moves to last column (when it's NaN)
    - Numeric part stays in penultimate column with harmonized decimal separator

    Args:
        df: DataFrame to process.

    Returns:
        DataFrame with separated text and digits.
    """
    for index, row in df.iterrows():
        token = str(row.iloc[-2])
        if any(char.isdigit() for char in token) and any(char.isalpha() for char in token):
            if pd.isnull(row.iloc[-1]):
                # Move letters to last column
                df.loc[index, df.columns[-1]] = "".join(
                    filter(lambda x: x.isalpha() or x == " ", token)
                )
                # Keep digits in penultimate column
                df.loc[index, df.columns[-2]] = "".join(
                    filter(lambda x: not (x.isalpha() or x == " "), token)
                )

            # Detect and harmonize decimal separator
            if "," in token:
                parts = token.split(",")
            elif "." in token:
                parts = token.split(".")
            else:
                parts = [token, ""]

            cleaned_integer = "".join(filter(lambda x: x.isdigit() or x == "-", parts[0]))
            cleaned_decimal = "".join(filter(lambda x: x.isdigit(), parts[1]))
            cleaned_numeric = (
                f"{cleaned_integer},{cleaned_decimal}" if cleaned_decimal else cleaned_integer
            )
            df.loc[index, df.columns[-2]] = cleaned_numeric

    return df


def extract_years(df: pd.DataFrame) -> List[str]:
    """
    Return list of column names that are 4-digit years.

    Args:
        df: DataFrame to analyze.

    Returns:
        List of column names matching 4-digit year pattern.

    Example:
        >>> extract_years(df)
        ['2020', '2021', '2022']
    """
    year_columns = [col for col in df.columns if re.match(r"\b\d{4}\b", str(col))]
    return year_columns


def first_row_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Set first row as column headers and drop it from data area.

    Args:
        df: DataFrame to modify.

    Returns:
        DataFrame with first row promoted to header.
    """
    df.columns = df.iloc[0]
    df = df.drop(df.index[0])
    return df


def clean_columns_values(df: pd.DataFrame) -> pd.DataFrame:
    """
    Normalize headers and values across the DataFrame.

    - Headers: lowercase ASCII with underscores, 'ano' -> 'year'
    - Values: remove tildes, replace commas with dots for numeric conversion
    - Sector labels: lowercase and sanitized

    Args:
        df: DataFrame to clean.

    Returns:
        DataFrame with normalized columns and values.
    """
    # Normalize column headers
    normalized_columns = pd.Index(df.columns).str.lower()
    normalized_columns = [
        (
            unicodedata.normalize("NFKD", col).encode("ASCII", "ignore").decode("utf-8")
            if isinstance(col, str)
            else col
        )
        for col in normalized_columns
    ]
    normalized_columns = pd.Index(normalized_columns)
    normalized_columns = (
        normalized_columns.str.replace(" ", "_").str.replace("ano", "year").str.replace("-", "_")
    )

    # Clean values column-by-column and rebuild the dataframe so duplicate names and dtype
    # transitions do not trigger pandas assignment errors.
    cleaned_columns = []
    for idx in range(len(df.columns)):
        series = df.iloc[:, idx].astype("object").copy()
        series = series.apply(lambda x: remove_tildes(x) if isinstance(x, str) else x)
        series = series.apply(
            lambda x: str(x).replace(",", ".") if isinstance(x, (int, float, str)) else x
        )
        cleaned_columns.append(series)

    cleaned_df = pd.concat(cleaned_columns, axis=1)
    cleaned_df.columns = normalized_columns
    cleaned_df.index = df.index

    # Lowercase and clean the first occurrence of the sector label columns.
    for sector_col in ["sectores_economicos", "economic_sectors"]:
        match_positions = np.flatnonzero(cleaned_df.columns == sector_col)
        if len(match_positions) == 0:
            continue
        idx = int(match_positions[0])
        cleaned_df.iloc[:, idx] = (
            cleaned_df.iloc[:, idx].astype(str).str.lower().apply(remove_rare_characters)
        )

    return cleaned_df


def convert_float(df: pd.DataFrame) -> pd.DataFrame:
    """
    Convert all columns except sector labels to numeric.

    Args:
        df: DataFrame to convert.

    Returns:
        DataFrame with numeric columns converted (errors coerced to NaN).
    """
    excluded_columns = {"sectores_economicos", "economic_sectors"}
    converted_columns = []

    for idx, col in enumerate(df.columns):
        series = df.iloc[:, idx].copy()
        if col not in excluded_columns:
            series = pd.to_numeric(series, errors="coerce")
        converted_columns.append(series)

    converted_df = pd.concat(converted_columns, axis=1)
    converted_df.columns = df.columns
    converted_df.index = df.index
    return converted_df


def relocate_last_column(df: pd.DataFrame) -> pd.DataFrame:
    """
    Move last column to second position.

    Args:
        df: DataFrame to modify.

    Returns:
        DataFrame with last column relocated to index 1.
    """
    last_column = df.pop(df.columns[-1])
    df.insert(1, last_column.name, last_column)
    return df


def clean_first_row(df: pd.DataFrame) -> pd.DataFrame:
    """
    Normalize the first row: lowercase, remove tildes and rare characters, 'ano' -> 'year'.

    Args:
        df: DataFrame to modify.

    Returns:
        DataFrame with cleaned first row.
    """
    from peru_gdp_rtd.cleaners.text_cleaners import remove_rare_characters_first_row

    for idx in range(len(df.columns)):
        value = df.iat[0, idx]
        if isinstance(value, str):
            value = value.lower()
            value = remove_tildes(value)
            value = remove_rare_characters_first_row(value)
            value = value.replace("ano", "year")
            df.iat[0, idx] = value
    return df


def replace_set_sep(df: pd.DataFrame) -> pd.DataFrame:
    """
    Rename columns containing 'set' to use 'sep' instead.

    Portuguese 'setembro' is abbreviated as 'set', but we use 'sep' for consistency.

    Args:
        df: DataFrame to modify.

    Returns:
        DataFrame with 'set' replaced by 'sep' in column names.
    """
    columns = df.columns
    for column in columns:
        if "set" in str(column):
            new_column = str(column).replace("set", "sep")
            df.rename(columns={column: new_column}, inplace=True)
    return df


def spaces_se_es(df: pd.DataFrame) -> pd.DataFrame:
    """
    Remove surrounding spaces from sector label columns.

    Args:
        df: DataFrame to clean.

    Returns:
        DataFrame with trimmed sector labels.
    """
    for sector_col in ["sectores_economicos", "economic_sectors"]:
        match_positions = np.flatnonzero(df.columns == sector_col)
        if len(match_positions) == 0:
            continue
        idx = int(match_positions[0])
        df.iloc[:, idx] = df.iloc[:, idx].astype(str).str.strip()
    return df


def replace_services(df: pd.DataFrame) -> pd.DataFrame:
    """
    Unify 'services' naming in sector labels.

    Replaces 'servicios' -> 'otros servicios' and 'services' -> 'other services'
    when both columns contain those tokens.

    Args:
        df: DataFrame to modify.

    Returns:
        DataFrame with unified service sector names.
    """
    se_positions = np.flatnonzero(df.columns == "sectores_economicos")
    es_positions = np.flatnonzero(df.columns == "economic_sectors")
    if len(se_positions) == 0 or len(es_positions) == 0:
        return df

    se_idx = int(se_positions[0])
    es_idx = int(es_positions[0])
    se_series = df.iloc[:, se_idx].copy()
    es_series = df.iloc[:, es_idx].copy()

    if ("servicios" in se_series.values) and ("services" in es_series.values):
        df.iloc[:, se_idx] = se_series.replace({"servicios": "otros servicios"})
        df.iloc[:, es_idx] = es_series.replace({"services": "other services"})
    return df


def replace_mineria(df: pd.DataFrame) -> pd.DataFrame:
    """
    Unify 'mineria' naming in Spanish sector labels.

    Replaces 'mineria' -> 'mineria e hidrocarburos' when the latter is absent.

    Args:
        df: DataFrame to modify.

    Returns:
        DataFrame with standardized mining sector name.
    """
    match_positions = np.flatnonzero(df.columns == "sectores_economicos")
    if len(match_positions) == 0:
        return df

    idx = int(match_positions[0])
    series = df.iloc[:, idx].copy()
    if ("mineria" in series.values) and ("mineria e hidrocarburos" not in series.values):
        df.iloc[:, idx] = series.replace({"mineria": "mineria e hidrocarburos"})
    return df


def replace_mining(df: pd.DataFrame) -> pd.DataFrame:
    """
    Unify 'mining' naming in English sector labels.

    Replaces 'mining and fuels' -> 'mining and fuel' for consistency.

    Args:
        df: DataFrame to modify.

    Returns:
        DataFrame with standardized mining sector name.
    """
    match_positions = np.flatnonzero(df.columns == "economic_sectors")
    if len(match_positions) == 0:
        return df

    idx = int(match_positions[0])
    series = df.iloc[:, idx].copy()
    if "mining and fuels" in series.values:
        df.iloc[:, idx] = series.replace({"mining and fuels": "mining and fuel"})
    return df


def rounding_values(df: pd.DataFrame, decimals: int = 1) -> pd.DataFrame:
    """
    Round all float64 columns to specified decimal places.

    Args:
        df: DataFrame to round.
        decimals: Number of decimal places (default: 1).

    Returns:
        DataFrame with rounded values.
    """
    rounded_columns = []
    for idx in range(len(df.columns)):
        series = df.iloc[:, idx].copy()
        if pd.api.types.is_float_dtype(series):
            series = series.round(decimals)
        rounded_columns.append(series)

    rounded_df = pd.concat(rounded_columns, axis=1)
    rounded_df.columns = df.columns
    rounded_df.index = df.index
    return rounded_df


def drop_rare_caracter_row(df: pd.DataFrame) -> pd.DataFrame:
    """
    Remove rows containing the '}' character anywhere.

    Args:
        df: DataFrame to clean.

    Returns:
        DataFrame with rare character rows removed.
    """
    rare_caracter_row = df.apply(lambda row: "}" in row.values, axis=1)
    df = df[~rare_caracter_row]
    return df
