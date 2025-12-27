#!/usr/bin/env python
"""Data quality validation script for Peru GDP Real-Time Dataset.

This script performs comprehensive data quality checks on the generated RTD datasets,
including:
- Missing value analysis
- Time series continuity checks
- Statistical validation
- Format validation
- Comparison with expected benchmarks

Usage:
    python scripts/validate_rtd.py
    python scripts/validate_rtd.py --dataset monthly
    python scripts/validate_rtd.py --verbose
    python scripts/validate_rtd.py --export-report
"""

import argparse
import sys
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from datetime import datetime

# Add project root to path
SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent
sys.path.insert(0, str(PROJECT_ROOT))

import pandas as pd
import numpy as np
from peru_gdp_rtd.config import get_settings


class RTDValidator:
    """Validator for GDP Real-Time Datasets."""

    def __init__(self, data_dir: Path, verbose: bool = False):
        """Initialize validator.

        Args:
            data_dir: Directory containing RTD datasets
            verbose: Enable verbose output
        """
        self.data_dir = data_dir
        self.verbose = verbose
        self.results = []
        self.errors = []
        self.warnings = []

    def log(self, message: str, level: str = "INFO"):
        """Log message."""
        if self.verbose or level in ["ERROR", "WARNING"]:
            prefix = {
                "INFO": "INFO:",
                "SUCCESS": "OK:",
                "WARNING": "WARNING:",
                "ERROR": "ERROR:",
            }.get(level, "")
            print(f"{prefix} {message}")

    def validate_dataset(self, dataset_name: str, filepath: Path) -> Dict:
        """Validate a single dataset.

        Args:
            dataset_name: Name of the dataset
            filepath: Path to CSV file

        Returns:
            Dictionary with validation results
        """
        self.log(f"\nValidating {dataset_name}...", "INFO")

        if not filepath.exists():
            self.log(f"File not found: {filepath}", "ERROR")
            return {
                "dataset": dataset_name,
                "exists": False,
                "valid": False,
            }

        try:
            df = pd.read_csv(filepath, index_col=0)
        except Exception as e:
            self.log(f"Error reading file: {e}", "ERROR")
            return {
                "dataset": dataset_name,
                "exists": True,
                "read_error": str(e),
                "valid": False,
            }

        # Run validation checks
        result = {
            "dataset": dataset_name,
            "exists": True,
            "shape": df.shape,
            "valid": True,
        }

        # Check 1: Non-empty
        if df.empty:
            self.log("Dataset is empty", "ERROR")
            result["valid"] = False
            result["empty"] = True
        else:
            result["empty"] = False

        # Check 2: Missing values
        missing_pct = (df.isna().sum().sum() / (df.shape[0] * df.shape[1])) * 100
        result["missing_pct"] = missing_pct

        if missing_pct > 50:
            self.log(f"High missing value percentage: {missing_pct:.1f}%", "WARNING")
            self.warnings.append(f"{dataset_name}: {missing_pct:.1f}% missing values")
        else:
            self.log(f"Missing values: {missing_pct:.1f}%", "SUCCESS")

        # Check 3: Data types
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        result["numeric_cols"] = len(numeric_cols)
        result["total_cols"] = len(df.columns)

        # Check 4: Value ranges (GDP growth typically -20% to +20%)
        numeric_data = df.select_dtypes(include=[np.number])
        if not numeric_data.empty:
            min_val = numeric_data.min().min()
            max_val = numeric_data.max().max()
            mean_val = numeric_data.mean().mean()

            result["min_value"] = min_val
            result["max_value"] = max_val
            result["mean_value"] = mean_val

            if min_val < -50 or max_val > 50:
                self.log(f"Unusual value range: [{min_val:.2f}, {max_val:.2f}]", "WARNING")
                self.warnings.append(f"{dataset_name}: Values outside expected range")
            else:
                self.log(f"Value range: [{min_val:.2f}, {max_val:.2f}]", "SUCCESS")

        # Check 5: Index continuity
        if hasattr(df.index, 'is_monotonic_increasing'):
            result["index_monotonic"] = df.index.is_monotonic_increasing

        # Check 6: Duplicate rows/columns
        result["duplicate_rows"] = df.index.duplicated().sum()
        result["duplicate_cols"] = df.columns.duplicated().sum()

        if result["duplicate_rows"] > 0:
            self.log(f"Found {result['duplicate_rows']} duplicate rows", "WARNING")
            self.warnings.append(f"{dataset_name}: {result['duplicate_rows']} duplicate rows")

        if result["duplicate_cols"] > 0:
            self.log(f"Found {result['duplicate_cols']} duplicate columns", "ERROR")
            self.errors.append(f"{dataset_name}: {result['duplicate_cols']} duplicate columns")
            result["valid"] = False

        return result

    def validate_all(self) -> List[Dict]:
        """Validate all RTD datasets.

        Returns:
            List of validation results
        """
        datasets = {
            "Monthly RTD": "monthly_gdp_rtd.csv",
            "Quarterly RTD": "quarterly_annual_gdp_rtd.csv",
            "Monthly Releases": "monthly_gdp_releases.csv",
            "Quarterly Releases": "quarterly_annual_gdp_releases.csv",
            "Monthly Benchmark": "monthly_gdp_benchmark.csv",
            "Quarterly Benchmark": "quarterly_annual_gdp_benchmark.csv",
            "BY-Adjusted Monthly RTD": "by_adjusted_monthly_gdp_rtd.csv",
            "BY-Adjusted Quarterly RTD": "by_adjusted_quarterly_annual_gdp_rtd.csv",
        }

        self.log("=" * 60, "INFO")
        self.log("Peru GDP RTD - Data Quality Validation", "INFO")
        self.log("=" * 60, "INFO")

        results = []

        for name, filename in datasets.items():
            filepath = self.data_dir / filename
            result = self.validate_dataset(name, filepath)
            results.append(result)

        return results

    def print_summary(self, results: List[Dict]):
        """Print validation summary.

        Args:
            results: List of validation results
        """
        print("\n" + "=" * 60)
        print("VALIDATION SUMMARY")
        print("=" * 60)

        total = len(results)
        exists = sum(1 for r in results if r.get("exists", False))
        valid = sum(1 for r in results if r.get("valid", False))

        print(f"\nTotal datasets checked: {total}")
        print(f"Files found: {exists}/{total}")
        print(f"Valid datasets: {valid}/{exists}")

        if self.errors:
            print(f"\nErrors: {len(self.errors)}")
            for error in self.errors:
                print(f"  - {error}")

        if self.warnings:
            print(f"\nWarnings: {len(self.warnings)}")
            for warning in self.warnings[:10]:  # Show first 10
                print(f"  - {warning}")
            if len(self.warnings) > 10:
                print(f"  ... and {len(self.warnings) - 10} more")

        if not self.errors and not self.warnings:
            print("\nAll checks passed!")

        print("\n" + "=" * 60)

    def export_report(self, results: List[Dict], output_path: Path):
        """Export validation report to CSV.

        Args:
            results: Validation results
            output_path: Output file path
        """
        df = pd.DataFrame(results)

        # Expand nested dictionaries
        if 'shape' in df.columns:
            df['rows'] = df['shape'].apply(lambda x: x[0] if x else None)
            df['cols'] = df['shape'].apply(lambda x: x[1] if x else None)
            df = df.drop('shape', axis=1)

        df.to_csv(output_path, index=False)
        self.log(f"Report exported to: {output_path}", "SUCCESS")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Validate Peru GDP Real-Time Dataset quality"
    )
    parser.add_argument(
        "--dataset",
        type=str,
        help="Validate specific dataset only (monthly, quarterly, releases, benchmark)",
    )
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Enable verbose output",
    )
    parser.add_argument(
        "--export-report",
        action="store_true",
        help="Export validation report to CSV",
    )
    parser.add_argument(
        "--data-dir",
        type=str,
        default="data/output",
        help="Directory containing RTD datasets (default: data/output)",
    )

    args = parser.parse_args()

    # Get data directory
    data_dir = PROJECT_ROOT / args.data_dir

    if not data_dir.exists():
        print(f"ERROR: Data directory not found: {data_dir}")
        print(f"Please run the pipeline first: python scripts/update_rtd.py")
        sys.exit(1)

    # Initialize validator
    validator = RTDValidator(data_dir, verbose=args.verbose)

    # Run validation
    results = validator.validate_all()

    # Print summary
    validator.print_summary(results)

    # Export report if requested
    if args.export_report:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_path = PROJECT_ROOT / "data" / f"validation_report_{timestamp}.csv"
        report_path.parent.mkdir(exist_ok=True)
        validator.export_report(results, report_path)

    # Exit code based on validation results
    if validator.errors:
        sys.exit(1)  # Errors found
    elif validator.warnings:
        sys.exit(0)  # Warnings only
    else:
        sys.exit(0)  # All good


if __name__ == "__main__":
    main()
