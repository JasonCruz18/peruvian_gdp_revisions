"""
CSV Converter Module

Converts OCR text output to structured CSV format matching existing data.
Handles sector name standardization and proper CSV formatting.

Output Format:
sectores_economicos;economic_sectors;1992_ene;1992_feb;...
agropecuario;agriculture and livestock;3.7;3.6;...
pesca;fishing;-29.8;-26.4;...

Author: Jason Cruz
Institution: Universidad del Pacífico - CIUP
Date: January 2026
"""

import re
import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional
from pathlib import Path
import logging

logger = logging.getLogger(__name__)


# Sector name mappings (Spanish → standardized Spanish)
SECTOR_MAPPINGS_ES = {
    'agropecuario': 'agropecuario',
    'agro pecuario': 'agropecuario',
    'agricultura': 'agropecuario',
    'agriculture': 'agropecuario',

    'pesca': 'pesca',
    'fishing': 'pesca',

    'mineria': 'mineria e hidrocarburos',
    'minería': 'mineria e hidrocarburos',
    'mineria e hidrocarburos': 'mineria e hidrocarburos',
    'minería e hidrocarburos': 'mineria e hidrocarburos',
    'mineria y hidrocarburos': 'mineria e hidrocarburos',
    'mining': 'mineria e hidrocarburos',
    'mining and fuel': 'mineria e hidrocarburos',

    'manufactura': 'manufactura',
    'manufacturing': 'manufactura',

    'electricidad': 'electricidad y agua',
    'electricidad y agua': 'electricidad y agua',
    'electricity': 'electricidad y agua',
    'electricity and water': 'electricidad y agua',

    'construccion': 'construccion',
    'construcción': 'construccion',
    'construction': 'construccion',

    'comercio': 'comercio',
    'commerce': 'comercio',

    'otros servicios': 'otros servicios',
    'other services': 'otros servicios',
    'servicios': 'otros servicios',
    'services': 'otros servicios',

    'pbi': 'pbi',
    'gdp': 'pbi',
    'total': 'pbi',
}

# English equivalents
SECTOR_MAPPINGS_EN = {
    'agropecuario': 'agriculture and livestock',
    'pesca': 'fishing',
    'mineria e hidrocarburos': 'mining and fuel',
    'manufactura': 'manufacturing',
    'electricidad y agua': 'electricity and water',
    'construccion': 'construction',
    'comercio': 'commerce',
    'otros servicios': 'other services',
    'pbi': 'gdp',
}


def parse_table_structure(ocr_text: str, table_type: str = "table_1") -> pd.DataFrame:
    """
    Parse OCR text into tabular structure.

    Uses robust parsing that identifies sector rows by matching known sector names,
    then extracts all numeric values from each row.

    Args:
        ocr_text: Cleaned OCR output text
        table_type: "table_1" (monthly) or "table_2" (quarterly)

    Returns:
        DataFrame with parsed table data

    Raises:
        ValueError: If parsing fails
    """
    # Known sector keywords for identification (Spanish and English)
    KNOWN_SECTORS = [
        # Spanish
        'agropecuario', 'agricola', 'agrícola', 'pecuario',
        'pesca', 'mineria', 'minería', 'mineria metalica', 'minería metálica',
        'petroleo', 'petróleo', 'manufactura', 'procesadores', 'resto industria',
        'construccion', 'construcción', 'gobierno', 'otros', 'comercio', 'resto',
        'pbi', 'electricidad', 'servicios',
        # English (for bilingual PDFs 2000+)
        'agriculture', 'farming', 'livestock',
        'fishing',
        'mining', 'mining and fuel', 'metallic mining',
        'petroleum', 'crude oil',
        'manufacturing',
        'construction',
        'government',
        'commerce', 'trade',
        'services', 'other services',
        'gdp', 'electricity'
    ]

    lines = [line.strip() for line in ocr_text.split('\n') if line.strip()]

    if not lines:
        raise ValueError("Empty OCR text")

    # Extract data rows by identifying sector names
    rows = []
    for line in lines:
        # Skip header/title lines (Spanish and English)
        line_upper = line.upper()
        if any(keyword in line_upper for keyword in ['CUADRO', 'PRODUCTO', 'BRUTO', 'INTERNO', 'VARIACION',
                                                       'GROSS', 'DOMESTIC', 'PRODUCT', 'TABLE', 'GROWTH']):
            continue
        if line.startswith('Ene.') or line.startswith('PO ') or line.startswith('1/') or line.startswith('Jan.'):
            continue

        # Check if line starts with a known sector (fuzzy matching for OCR errors)
        line_lower = line.lower()
        is_sector_row = False
        for known_sector in KNOWN_SECTORS:
            # Exact or starts-with match
            if line_lower.startswith(known_sector):
                is_sector_row = True
                break
            # Fuzzy match for OCR errors (allow 1-2 character differences in first 6 chars)
            if len(known_sector) >= 4 and len(line_lower) >= 4:
                # Check if first few characters are similar (handles "agropeciano"→"agropecuario", "menera"→"mineria")
                line_prefix = line_lower[:min(6, len(known_sector))]
                sector_prefix = known_sector[:min(6, len(known_sector))]
                # Count matching characters in prefix
                matches = sum(c1 == c2 for c1, c2 in zip(line_prefix, sector_prefix))
                if matches >= len(sector_prefix) - 2:  # Allow 2 mismatches
                    is_sector_row = True
                    break

        if is_sector_row:
            # Extract all tokens from the line
            tokens = line.split()

            # Separate sector name from numeric values
            # Find where the sector name ends (first numeric value)
            sector_tokens = []
            value_tokens = []
            found_first_number = False

            for token in tokens:
                # Check if token looks numeric (digits, negative signs, decimals)
                if re.search(r'[-−=~]?\d', token):
                    found_first_number = True
                    value_tokens.append(token)
                elif found_first_number:
                    value_tokens.append(token)
                else:
                    sector_tokens.append(token)

            if sector_tokens and value_tokens:
                sector_name = ' '.join(sector_tokens)
                rows.append([sector_name] + value_tokens)

    if not rows:
        raise ValueError("No sector rows found in OCR text")

    # Create DataFrame
    df = pd.DataFrame(rows)

    logger.info(f"Parsed table: {len(df)} rows x {len(df.columns)} columns")
    return df


def standardize_sector_names(df: pd.DataFrame) -> pd.DataFrame:
    """
    Standardize sector names using mapping dictionaries.

    Adds both Spanish and English sector columns.

    Args:
        df: DataFrame with sector names in first column

    Returns:
        DataFrame with standardized sector columns
    """
    if df.empty or len(df.columns) < 1:
        raise ValueError("DataFrame must have at least one column")

    # Extract sector names (first column)
    raw_sectors = df.iloc[:, 0].astype(str).str.lower().str.strip()

    # Map to standardized Spanish names
    sectors_es = []
    sectors_en = []

    for raw_sector in raw_sectors:
        # Try exact match first
        sector_es = SECTOR_MAPPINGS_ES.get(raw_sector)

        if sector_es is None:
            # Try fuzzy match (partial string match)
            for key, value in SECTOR_MAPPINGS_ES.items():
                if key in raw_sector or raw_sector in key:
                    sector_es = value
                    break

        if sector_es is None:
            logger.warning(f"Unknown sector: '{raw_sector}', keeping as-is")
            sector_es = raw_sector

        # Get English equivalent
        sector_en = SECTOR_MAPPINGS_EN.get(sector_es, sector_es)

        sectors_es.append(sector_es)
        sectors_en.append(sector_en)

    # Create new DataFrame with standardized sectors
    result = pd.DataFrame({
        'sectores_economicos': sectors_es,
        'economic_sectors': sectors_en
    })

    # Append numeric columns (skip first column which was sectors)
    numeric_cols = df.iloc[:, 1:].copy()
    result = pd.concat([result, numeric_cols], axis=1)

    logger.info(f"Standardized {len(sectors_es)} sector names")
    return result


def clean_numeric_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean and validate numeric columns.

    Args:
        df: DataFrame with sector columns + numeric data

    Returns:
        DataFrame with cleaned numeric columns
    """
    # Start from column 2 (after Spanish and English sector names)
    numeric_cols = df.columns[2:]

    for col in numeric_cols:
        # Convert to numeric, coercing errors
        df[col] = pd.to_numeric(df[col], errors='coerce')

    logger.debug(f"Cleaned {len(numeric_cols)} numeric columns")
    return df


def format_column_names(df: pd.DataFrame, table_type: str = "table_1") -> pd.DataFrame:
    """
    Format column names to match existing CSV structure.

    Args:
        df: DataFrame with parsed data
        table_type: "table_1" (monthly) or "table_2" (quarterly)

    Returns:
        DataFrame with properly formatted column names
    """
    # First two columns are always the same
    new_columns = ['sectores_economicos', 'economic_sectors']

    # Format remaining columns based on table type
    for col in df.columns[2:]:
        col_str = str(col)

        if table_type == "table_1":
            # Monthly format: YYYY_mmm (e.g., 2000_ene, 2000_feb)
            # Try to extract year and month
            match = re.search(r'(\d{4})', col_str)
            if match:
                year = match.group(1)
                # Month abbreviation (ene, feb, mar, etc.)
                month_match = re.search(r'(ene|feb|mar|abr|may|jun|jul|ago|sep|oct|nov|dic)', col_str, re.I)
                if month_match:
                    month = month_match.group(1).lower()
                    new_columns.append(f"{year}_{month}")
                else:
                    # Fallback: keep original
                    new_columns.append(col_str)
            else:
                new_columns.append(col_str)

        elif table_type == "table_2":
            # Quarterly format: YYYY_Q (e.g., 2000_1, 2000_2, 2000_3, 2000_4)
            # or annual: YYYY_year (e.g., 2000_year)
            match = re.search(r'(\d{4})', col_str)
            if match:
                year = match.group(1)
                # Quarter (I, II, III, IV or 1, 2, 3, 4)
                quarter_match = re.search(r'(IV|III|II|I|[1-4])', col_str)
                if quarter_match:
                    quarter = quarter_match.group(1)
                    # Convert roman to number
                    if quarter == 'I':
                        quarter = '1'
                    elif quarter == 'II':
                        quarter = '2'
                    elif quarter == 'III':
                        quarter = '3'
                    elif quarter == 'IV':
                        quarter = '4'
                    new_columns.append(f"{year}_{quarter}")
                elif 'year' in col_str.lower() or 'año' in col_str.lower():
                    new_columns.append(f"{year}_year")
                else:
                    new_columns.append(col_str)
            else:
                new_columns.append(col_str)
        else:
            new_columns.append(col_str)

    # Apply new column names
    if len(new_columns) == len(df.columns):
        df.columns = new_columns
        logger.info(f"Formatted column names for {table_type}")
    else:
        logger.warning(f"Column count mismatch: {len(new_columns)} != {len(df.columns)}")

    return df


def format_as_semicolon_csv(
    df: pd.DataFrame,
    output_path: str,
    separator: str = ";",
    encoding: str = "utf-8-sig"
) -> None:
    """
    Save DataFrame as semicolon-separated CSV with UTF-8 BOM.

    Matches existing CSV format used in peru_gdp_rtd pipeline.

    Args:
        df: DataFrame to save
        output_path: Output file path
        separator: Column separator (default: semicolon)
        encoding: File encoding (default: UTF-8 with BOM for Excel)
    """
    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)

    df.to_csv(
        output_file,
        sep=separator,
        encoding=encoding,
        index=False,
        na_rep=""
    )

    logger.info(f"Saved CSV: {output_file.name} ({len(df)} rows x {len(df.columns)} cols)")


def convert_ocr_to_csv(
    ocr_text: str,
    output_path: str,
    table_type: str = "table_1"
) -> pd.DataFrame:
    """
    Complete OCR→CSV conversion pipeline.

    Args:
        ocr_text: Cleaned OCR output
        output_path: Output CSV file path
        table_type: "table_1" (monthly) or "table_2" (quarterly)

    Returns:
        Converted DataFrame

    Raises:
        ValueError: If conversion fails
    """
    logger.info(f"Converting OCR to CSV: {table_type}")

    # Step 1: Parse table structure
    df = parse_table_structure(ocr_text, table_type)

    # Step 2: Standardize sector names
    df = standardize_sector_names(df)

    # Step 3: Clean numeric columns
    df = clean_numeric_columns(df)

    # Step 4: Format column names
    df = format_column_names(df, table_type)

    # Step 5: Save as CSV
    format_as_semicolon_csv(df, output_path)

    logger.info(f"CSV conversion complete: {output_path}")
    return df


if __name__ == "__main__":
    # Test CSV converter
    import sys

    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    if len(sys.argv) < 3:
        print("Usage: python csv_converter.py <ocr_text_file> <output_csv>")
        print("  ocr_text_file: OCR output text file")
        print("  output_csv: Output CSV file path")
        sys.exit(1)

    ocr_text_file = sys.argv[1]
    output_csv = sys.argv[2]

    # Determine table type from filename
    table_type = "table_2" if "table_2" in output_csv or "quarterly" in output_csv else "table_1"

    # Load OCR text
    with open(ocr_text_file, 'r', encoding='utf-8') as f:
        ocr_text = f.read()

    print(f"Loaded OCR text: {len(ocr_text)} characters")
    print(f"Table type: {table_type}\n")

    try:
        # Convert to CSV
        df = convert_ocr_to_csv(ocr_text, output_csv, table_type)

        print(f"✓ Conversion successful")
        print(f"  Output: {output_csv}")
        print(f"  Shape: {df.shape}")
        print(f"\nFirst few rows:")
        print(df.head().to_string())

    except Exception as e:
        print(f"✗ Conversion failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
