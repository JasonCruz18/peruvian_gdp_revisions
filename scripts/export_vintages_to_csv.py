"""
Export vintage Parquet files to CSV format for Zenodo upload.

This script converts all vintage .parquet files to .csv format
for Data in Brief submission, which requires open data formats.
"""

import pandas as pd
from pathlib import Path


def export_vintages_to_csv():
    """Export all vintage parquet files to CSV format."""
    vintages_dir = Path("data/output/vintages")

    if not vintages_dir.exists():
        print(f"Error: {vintages_dir} does not exist")
        return

    # Find all parquet files
    parquet_files = list(vintages_dir.glob("*.parquet"))

    if not parquet_files:
        print(f"No parquet files found in {vintages_dir}")
        return

    print(f"Found {len(parquet_files)} parquet files to convert")
    print("-" * 60)

    for parquet_file in sorted(parquet_files):
        csv_file = parquet_file.with_suffix('.csv')

        print(f"Converting: {parquet_file.name}")

        # Read parquet and write to CSV
        df = pd.read_parquet(parquet_file)
        df.to_csv(csv_file, index=True)

        # Show file sizes
        parquet_size = parquet_file.stat().st_size / 1024  # KB
        csv_size = csv_file.stat().st_size / 1024  # KB

        print(f"  -> {csv_file.name}")
        print(f"  Parquet: {parquet_size:.1f} KB | CSV: {csv_size:.1f} KB")
        print()

    print("-" * 60)
    print(f"Successfully converted {len(parquet_files)} files to CSV")
    print(f"CSV files saved in: {vintages_dir}")


if __name__ == "__main__":
    export_vintages_to_csv()
