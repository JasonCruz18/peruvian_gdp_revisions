# Usage Guide

Comprehensive guide for using the Peru GDP Real-Time Dataset construction pipeline.

## Table of Contents

1. [Quick Start](#quick-start)
2. [Command-Line Interface](#command-line-interface)
3. [Python API](#python-api)
4. [Common Workflows](#common-workflows)
5. [Output Datasets](#output-datasets)
6. [Configuration Options](#configuration-options)
7. [Advanced Usage](#advanced-usage)

---

## Quick Start

### Run Complete Pipeline

The simplest way to build the GDP Real-Time Dataset:

```bash
# Navigate to project directory
cd peru_gdp_revisions

# Run complete pipeline (all 6 steps)
python scripts/update_rtd.py
```

This will:
1. Download PDFs from BCRP (15-30 minutes)
2. Extract relevant pages
3. Clean and standardize tables
4. Concatenate data across years
5. Apply metadata and track base-year changes
6. Convert to releases format

**Output**: All datasets in `data/output/` directory.

---

## Command-Line Interface

### Basic Commands

```bash
# Run all steps
python scripts/update_rtd.py

# Verbose output for debugging
python scripts/update_rtd.py --verbose

# Dry run (see what would happen without executing)
python scripts/update_rtd.py --dry-run
```

### Selective Step Execution

Run specific pipeline steps:

```bash
# Run only steps 3-6 (skip download and input generation)
python scripts/update_rtd.py --steps 3,4,5,6

# Skip PDF download (useful for testing)
python scripts/update_rtd.py --skip-download

# Run only data cleaning step
python scripts/update_rtd.py --steps 3
```

**Pipeline Steps:**
- **Step 1**: Download PDFs from BCRP
- **Step 2**: Shorten PDFs (extract key tables)
- **Step 3**: Clean tables and build RTD
- **Step 4**: Concatenate RTD across years
- **Step 5**: Apply metadata and benchmarks
- **Step 6**: Convert to releases format

### Custom Configuration

```bash
# Use custom configuration file
python scripts/update_rtd.py --config path/to/custom_config.yaml

# Example with all options
python scripts/update_rtd.py \
  --config config/config.yaml \
  --steps 1,2,3,4,5,6 \
  --verbose
```

### Help and Documentation

```bash
# Show help message
python scripts/update_rtd.py --help
```

---

## Python API

### Basic Usage

```python
from peru_gdp_rtd.config import get_settings
```bash
# Download only
python scripts/update_rtd.py --steps 1

# Shorten PDFs only
python scripts/update_rtd.py --steps 2

# Clean/build vintages only
python scripts/update_rtd.py --steps 3

# Concatenate + metadata + releases
python scripts/update_rtd.py --steps 4,5,6
```

### Web Scraping

```python
from peru_gdp_rtd.scrapers import pdf_downloader
from peru_gdp_rtd.config import get_settings

settings = get_settings('config/config.yaml')

# Download PDFs from BCRP
pdf_downloader(
    browser=settings.scraper.browser,
    headless=settings.scraper.headless,
    max_downloads=settings.scraper.max_downloads,
)
```

### PDF Processing

```python
from peru_gdp_rtd.processors import extract_table, organize_files_by_year
from peru_gdp_rtd.config import get_settings

settings = get_settings('config/config.yaml')

# Organize downloaded files by year
organize_files_by_year(
    new_wr_folder=settings.paths.new_wr,
    old_wr_folder=settings.paths.old_wr,
)

# Extract tables from a PDF
tables = extract_table(
    pdf_path='new_weekly_reports/2020/NS_01_enero_2020.pdf',
    pages=[3, 4],
    area=[[100, 50, 500, 750]],
)
```

### Data Cleaning

```python
from peru_gdp_rtd.cleaners import NewTableCleaner, clean_columns_values
from peru_gdp_rtd.config import get_settings
import pandas as pd

settings = get_settings('config/config.yaml')

# Initialize cleaner
cleaner = NewTableCleaner(
    df=raw_dataframe,
    wr_number=1234,
    table_num=1,
    config=settings,
)

# Apply cleaning pipeline
cleaned_df = cleaner.clean()

# Use specific cleaning functions
df_clean = clean_columns_values(
    df=raw_dataframe,
    decimal_places=1,
)
```

### RTD Construction

```python
from peru_gdp_rtd.transformers import VintagesPreparator, apply_base_year_sentinel
from peru_gdp_rtd.config import get_settings

settings = get_settings('config/config.yaml')

# Prepare vintage datasets
preparator = VintagesPreparator(
    df=cleaned_dataframe,
    base_year=2007,
    vintage_name='2020_01',
    config=settings,
)
monthly_vintage, quarterly_vintage = preparator.prepare_vintages()

# Apply base-year sentinels
df_with_sentinel = apply_base_year_sentinel(
    df=monthly_vintage,
    base_year=2007,
)
```

### Metadata Management

```python
from peru_gdp_rtd.transformers import MetadataHandler
from peru_gdp_rtd.config import get_settings

settings = get_settings('config/config.yaml')

# Initialize metadata handler
handler = MetadataHandler(config=settings)

# Process metadata and create benchmarks
monthly_rtd, quarterly_rtd = handler.load_rtd_datasets()
benchmark_monthly, benchmark_quarterly = handler.create_benchmark_datasets()
```

---

## Common Workflows

### Workflow 1: Initial Setup and Full Run

First-time users starting from scratch:

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Configure the pipeline
cp config/config.example.yaml config/config.yaml

# 3. Verify installation
python tests/test_smoke.py

# 4. Run complete pipeline
python scripts/update_rtd.py --verbose
```

### Workflow 2: Update Existing Dataset

Update RTD with new weekly reports:

```bash
# Download only new PDFs and process them
python scripts/update_rtd.py

# The pipeline is idempotent - it will:
# - Skip already processed files
# - Download only new PDFs
# - Update existing datasets
```

### Workflow 3: Testing and Development

Test changes without downloading PDFs:

```bash
# 1. Skip download step
python scripts/update_rtd.py --skip-download --verbose

# 2. Or run only specific steps
python scripts/update_rtd.py --steps 3,4,5,6 --verbose

# 3. Use dry-run mode
python scripts/update_rtd.py --dry-run
```

### Workflow 4: Custom Analysis

Use the pipeline for custom data extraction:

```python
from peru_gdp_rtd.config import get_settings
from peru_gdp_rtd.processors import extract_table
from peru_gdp_rtd.cleaners import NewTableCleaner
import pandas as pd

settings = get_settings('config/config.yaml')

# Extract and clean specific PDF
tables = extract_table(
    pdf_path='new_weekly_reports/2020/NS_01_enero_2020.pdf',
    pages=[3],
    area=[[100, 50, 500, 750]],
)

# Clean table
cleaner = NewTableCleaner(
    df=tables[0],
    wr_number=1234,
    table_num=1,
    config=settings,
)
clean_df = cleaner.clean()

# Analyze
print(clean_df.describe())
```

### Workflow 5: Batch Processing Multiple Years

Process specific year ranges:

```python
from peru_gdp_rtd.config import get_settings
```

---

## Output Datasets

All datasets are saved in `data/output/` directory.

### Real-Time Datasets (RTD)

**Format**: Each row is a vintage, each column is a target period.

```
data/output/
├── monthly_gdp_rtd.csv                      # Monthly GDP growth rates
└── quarterly_annual_gdp_rtd.csv             # Quarterly/annual GDP growth
```

**Structure Example**:
```
vintage_id | 2020_01 | 2020_02 | 2020_03 | ...
-----------|---------|---------|---------|-----
2020_02    |   3.5   |   2.1   |   NaN   | ...
2020_03    |   3.3   |   2.0   |   1.8   | ...
```

### Base-Year Adjusted Datasets

Remove revisions caused by base-year changes:

```
data/output/
├── by_adjusted_monthly_gdp_rtd.csv
└── by_adjusted_quarterly_annual_gdp_rtd.csv
```

### Benchmark Datasets

Only vintages immediately before base-year changes:

```
data/output/
├── monthly_gdp_benchmark.csv
├── quarterly_annual_gdp_benchmark.csv
├── by_adjusted_monthly_gdp_benchmark.csv
└── by_adjusted_quarterly_annual_gdp_benchmark.csv
```

### Releases Datasets

**Format**: Each row is a target period, columns are release numbers.

```
data/output/
├── monthly_gdp_releases.csv                 # Monthly GDP by release
├── quarterly_annual_gdp_releases.csv        # Quarterly GDP by release
└── [benchmark and adjusted versions]
```

**Structure Example**:
```
target_period | first_release | second_release | third_release | ...
--------------|---------------|----------------|---------------|-----
2020_01       |     3.5       |      3.3       |      3.4      | ...
2020_02       |     2.1       |      2.0       |      1.9      | ...
```

### Vintage-Format Intermediate Files

Stored in `data/input/`:

```
data/input/
├── monthly/
│   ├── 2020_01.csv
│   ├── 2020_02.csv
│   └── ...
└── quarterly/
    ├── 2020_01.csv
    └── ...
```

### Using Output Datasets

```python
import pandas as pd

# Load RTD
monthly_rtd = pd.read_csv('data/output/monthly_gdp_rtd.csv', index_col=0)
quarterly_rtd = pd.read_csv('data/output/quarterly_annual_gdp_rtd.csv', index_col=0)

# Load releases format
monthly_releases = pd.read_csv('data/output/monthly_gdp_releases.csv', index_col=0)

# Example: Calculate mean revision
revisions = monthly_releases['second_release'] - monthly_releases['first_release']
print(f"Mean revision: {revisions.mean():.2f}")

# Example: Plot revision patterns
import matplotlib.pyplot as plt
revisions.plot(kind='hist', bins=30)
plt.xlabel('Revision (percentage points)')
plt.title('Distribution of GDP Revisions')
plt.show()
```

---

## Configuration Options

### Key Configuration Sections

#### Project Settings
```yaml
project:
  name: "Peru GDP RTD"
  version: "1.0.0"
  author: "Jason Cruz"
```

#### Scraper Settings
```yaml
scraper:
  browser: "chrome"              # Browser: chrome, firefox, edge
  headless: false                # Run in background
  download_timeout: 30           # Timeout per PDF (seconds)
  max_downloads: 60              # Maximum PDFs to download
  rate_limit_min: 1.0            # Min delay between requests (seconds)
  rate_limit_max: 3.0            # Max delay between requests (seconds)
```

#### Cleaning Settings
```yaml
cleaning:
  decimal_places: 1              # Precision for growth rates
  pipeline_version: "s3.0.0"     # Version identifier
```

#### Feature Flags
```yaml
features:
  enable_alerts: true            # Play audio alerts
  persist_format: "csv"          # Output format: csv or parquet
```

### Modifying Configuration

```bash
# Edit configuration
nano config/config.yaml

# Or copy and customize
cp config/config.yaml config/custom.yaml
# Edit custom.yaml
python scripts/update_rtd.py --config config/custom.yaml
```

---

## Advanced Usage

### Custom Sector Mappings

Add or modify sector mappings in `config/config.yaml`:

```yaml
cleaning:
  sector_mappings_english:
    agropecuario: "agriculture"
    pesca: "fishing"
    minería e hidrocarburos: "mining"
    # Add custom mappings
    your_sector: "custom_name"
```

### Custom Processing Logic

Extend the pipeline with custom functions:

```python
from peru_gdp_rtd.cleaners import NewTableCleaner
from peru_gdp_rtd.config import get_settings

class CustomTableCleaner(NewTableCleaner):
    """Custom cleaner with additional logic."""

    def clean(self):
        """Override clean method."""
        df = super().clean()

        # Add custom processing
        df = self.custom_transformation(df)

        return df

    def custom_transformation(self, df):
        """Your custom transformation logic."""
        # Example: Apply custom filter
        df = df[df['sector'] != 'excluded_sector']
        return df

# Use custom cleaner
settings = get_settings('config/config.yaml')
cleaner = CustomTableCleaner(df=data, wr_number=1234, table_num=1, config=settings)
result = cleaner.clean()
```

### Parallel Processing

Process multiple years in parallel:

```python
from concurrent.futures import ProcessPoolExecutor
from peru_gdp_rtd.config import get_settings
```

### Export to Different Formats

```python
import pandas as pd

# Load RTD
rtd = pd.read_csv('data/output/monthly_gdp_rtd.csv', index_col=0)

# Export to Excel
rtd.to_excel('data/output/monthly_gdp_rtd.xlsx')

# Export to Parquet (more efficient for large datasets)
rtd.to_parquet('data/output/monthly_gdp_rtd.parquet')

# Export to Stata
rtd.to_stata('data/output/monthly_gdp_rtd.dta')

# Export to JSON
rtd.to_json('data/output/monthly_gdp_rtd.json', orient='index')
```

### Integration with Statistical Software

#### R Integration

```r
# Load RTD in R
library(readr)
monthly_rtd <- read_csv("data/output/monthly_gdp_rtd.csv")

# Analyze revisions
library(dplyr)
revisions <- monthly_rtd %>%
  mutate(across(everything(), ~. - lag(.)))

# Plot
library(ggplot2)
ggplot(revisions, aes(x=vintage_id, y=`2020_01`)) +
  geom_line() +
  theme_minimal()
```

#### Stata Integration

```stata
* Load RTD in Stata
import delimited "data/output/monthly_gdp_rtd.csv", clear

* Analyze revisions
gen revision = second_release - first_release
summarize revision

* Test for rationality
reg revision first_release
```

---

## Best Practices

1. **Always use version control**: Commit configuration changes
2. **Backup data regularly**: Before running updates
3. **Use verbose mode for debugging**: `--verbose` flag
4. **Test with dry-run first**: `--dry-run` flag
5. **Monitor memory usage**: Large datasets can consume significant RAM
6. **Document custom modifications**: Comment your code changes
7. **Keep dependencies updated**: `pip install --upgrade -r requirements.txt`

---

## Next Steps

- **Explore notebooks**: Interactive tutorials in `notebooks/`
- **Review architecture**: [docs/ARCHITECTURE.md](ARCHITECTURE.md)
- **Contribute**: [docs/CONTRIBUTING.md](CONTRIBUTING.md)
- **Run dashboard**: `streamlit run dashboard/app.py` (if available)

---

## Additional Resources

- **Main README**: [README.md](../README.md)
- **Installation Guide**: [docs/INSTALLATION.md](INSTALLATION.md)
- **API Reference**: Source code documentation
- **GitHub Issues**: https://github.com/JasonCruz18/peru_gdp_revisions/issues
