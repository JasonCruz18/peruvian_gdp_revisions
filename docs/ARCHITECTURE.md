# Architecture Documentation

Comprehensive guide to the Peru GDP RTD pipeline architecture, design decisions, and implementation details.

## Table of Contents

1. [Overview](#overview)
2. [Design Principles](#design-principles)
3. [System Architecture](#system-architecture)
4. [Module Structure](#module-structure)
5. [Data Flow](#data-flow)
6. [Key Design Decisions](#key-design-decisions)
7. [Extension Points](#extension-points)

---

## Overview

### Project Transformation

The Peru GDP RTD pipeline was transformed from a monolithic 4,393-line script into a modular, production-ready system:

**Before (Monolithic)**:
- 1 file: 4,393 lines of code
- Hardcoded values throughout
- Difficult to test and maintain
- No separation of concerns

**After (Modular)**:
- 14+ focused modules
- 28 Python files (~4,000+ lines)
- 100+ specialized functions
- Zero hardcoding (YAML-driven)
- Clear separation of concerns
- Type-safe with complete type hints
- Black-formatted for consistency

### Core Components

The pipeline consists of 6 major layers:

1. **Configuration Layer** - Type-safe settings management
2. **Scraping Layer** - Web scraping and PDF downloading
3. **Processing Layer** - PDF parsing and file organization
4. **Cleaning Layer** - Data standardization (70+ functions)
5. **Transformation Layer** - RTD construction and format conversion
6. **Orchestration Layer** - High-level workflow coordination

---

## Design Principles

### 1. Modularity

**Principle**: Each module has a single, well-defined responsibility.

**Benefits**:
- Easy to understand and maintain
- Simple to test individual components
- Facilitates code reuse
- Enables parallel development

**Example**:
```python
# Each module focuses on one task
from peru_gdp_rtd.scrapers import pdf_downloader      # Web scraping only
from peru_gdp_rtd.processors import extract_table     # PDF processing only
from peru_gdp_rtd.cleaners import NewTableCleaner     # Data cleaning only
from peru_gdp_rtd.transformers import VintagesPreparator  # RTD construction only
```

### 2. Configuration-Driven

**Principle**: Zero hardcoded values - all settings in YAML configuration.

**Benefits**:
- Easy to customize without code changes
- Single source of truth for settings
- Environment-specific configurations
- Version-controlled settings

**Implementation**:
```yaml
# config/config.yaml
scraper:
  browser: "chrome"
  max_downloads: 60

cleaning:
  decimal_places: 1
  sector_mappings_english:
    agropecuario: "agriculture"
```

```python
# Type-safe access
settings = get_settings('config/config.yaml')
browser = settings.scraper.browser  # Type: str
max_downloads = settings.scraper.max_downloads  # Type: int
```

### 3. Type Safety

**Principle**: Complete type hints throughout the codebase.

**Benefits**:
- Catch errors at development time
- Better IDE support (autocomplete, refactoring)
- Self-documenting code
- Improved maintainability

**Example**:
```python
from typing import List, Tuple, Optional
import pandas as pd
from pathlib import Path

def extract_table(
    pdf_path: Path,
    pages: List[int],
    area: Optional[List[List[float]]] = None,
) -> List[pd.DataFrame]:
    """Extract tables from PDF.

    Args:
        pdf_path: Path to PDF file
        pages: List of page numbers to extract
        area: Optional extraction area coordinates

    Returns:
        List of extracted DataFrames
    """
    ...
```

### 4. Idempotency

**Principle**: Pipeline can be run multiple times safely without duplicating work.

**Benefits**:
- Safe re-execution after failures
- Incremental updates
- Efficient use of computational resources
- Predictable behavior

**Implementation**:
```python
class RecordManager:
    """Tracks processed files to avoid reprocessing."""

    def is_processed(self, file_id: str) -> bool:
        """Check if file was already processed."""
        return file_id in self.records

    def mark_processed(self, file_id: str) -> None:
        """Mark file as processed."""
        self.records.add(file_id)
        self.save()
```

### 5. Separation of Concerns

**Principle**: Clear boundaries between different responsibilities.

**Layers**:
- **Scraping**: Only handles web interaction and downloads
- **Processing**: Only handles file manipulation and parsing
- **Cleaning**: Only handles data standardization
- **Transformation**: Only handles format conversions
- **Orchestration**: Only coordinates workflow

### 6. Error Resilience

**Principle**: Graceful handling of errors with detailed reporting.

**Features**:
- Try-except blocks with specific error handling
- Detailed error messages and stack traces
- Summary reports after completion
- Partial failure tolerance

---

## System Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     User Interface                          │
│  (CLI: scripts/update_rtd.py, Notebooks, Dashboard)         │
└────────────────────────┬────────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────────┐
│                  Orchestration Layer                        │
│     (peru_gdp_rtd.orchestration.runners)                    │
│  ┌─────────┬─────────┬─────────┬─────────┬─────────┐       │
│  │ Step 1  │ Step 2  │ Step 3  │ Step 4  │ Step 5  │       │
│  │ Step 6  │         │         │         │         │       │
│  └─────────┴─────────┴─────────┴─────────┴─────────┘       │
└──────┬────────┬────────┬────────┬────────┬─────────────────┘
       │        │        │        │        │
┌──────▼───┐ ┌─▼──────┐ ┌▼──────┐ ┌▼─────┐ ┌▼────────────┐
│ Scraping │ │ Process│ │ Clean │ │ Trans│ │   Utils     │
│  Layer   │ │  Layer │ │ Layer │ │ Layer│ │   Layer     │
│          │ │        │ │       │ │      │ │             │
│ - BCRP   │ │ - PDF  │ │ - 70+ │ │ - RTD│ │ - Alerts    │
│   Scraper│ │   Proc │ │   Func│ │   Concat │ - Records   │
│ - Driver │ │ - File │ │ - Old │ │ - Meta│ │ - Progress  │
│   Mgmt   │ │   Org  │ │   Clean│ │ - Release│ │ Tracking│
└──────────┘ └────────┘ └───────┘ └──────┘ └─────────────┘
       │          │          │         │           │
       └──────────┴──────────┴─────────┴───────────┘
                         │
                ┌────────▼────────┐
                │ Configuration   │
                │     Layer       │
                │  (YAML-driven)  │
                └─────────────────┘
```

### Data Flow

```
BCRP Website
    │
    ▼
[1. Web Scraping] → PDFs downloaded to new_weekly_reports/
    │
    ▼
[2. PDF Processing] → Extract relevant pages → data/input/
    │
    ▼
[3. Data Cleaning] → Standardize tables → data/input/
    │
    ▼
[4. Concatenation] → Merge vintages → monthly_gdp_rtd.csv
    │                                   quarterly_annual_gdp_rtd.csv
    ▼
[5. Metadata] → Apply base-year info → by_adjusted_*.csv
    │                                   benchmark_*.csv
    ▼
[6. Releases] → Convert format → *_releases.csv
    │
    ▼
Final Datasets in data/output/
```

---

## Module Structure

### 1. Configuration Module (`peru_gdp_rtd.config`)

**Purpose**: Type-safe configuration management.

**Files**:
- `settings.py` - Pydantic models for type-safe settings
- `__init__.py` - Exports `get_settings()` function

**Key Classes**:
```python
class ProjectSettings(BaseModel):
    """Project metadata."""
    name: str
    version: str
    author: str

class ScraperSettings(BaseModel):
    """Web scraping configuration."""
    browser: str
    headless: bool
    max_downloads: int
    download_timeout: int
    rate_limit_min: float
    rate_limit_max: float

class Settings(BaseModel):
    """Main settings container."""
    project: ProjectSettings
    scraper: ScraperSettings
    paths: PathSettings
    cleaning: CleaningSettings
    metadata: MetadataSettings
    features: FeaturesSettings
```

**Usage**:
```python
from peru_gdp_rtd.config import get_settings

settings = get_settings('config/config.yaml')
print(settings.project.name)  # "Peru GDP RTD"
```

### 2. Scraping Module (`peru_gdp_rtd.scrapers`)

**Purpose**: Download PDFs from BCRP website.

**Files**:
- `bcrp_scraper.py` - Main scraping logic with Selenium
- `utils.py` - Helper functions for web interaction

**Key Functions**:
```python
def pdf_downloader(
    browser: str = "chrome",
    headless: bool = False,
    max_downloads: int = 60,
    rate_limit: Tuple[float, float] = (1.0, 3.0),
) -> None:
    """Download PDFs from BCRP Weekly Reports."""
```

**Features**:
- Selenium-based browser automation
- Rate limiting to mimic human behavior
- Retry logic with exponential backoff
- Progress tracking with tqdm
- Automatic driver management (webdriver-manager)

### 3. Processing Module (`peru_gdp_rtd.processors`)

**Purpose**: File organization and PDF parsing.

**Files**:
- `pdf_processor.py` - PDF table extraction with Tabula
- `file_organizer.py` - Year-based file organization
- `metadata.py` - Metadata parsing utilities

**Key Functions**:
```python
def extract_table(
    pdf_path: Path,
    pages: List[int],
    area: Optional[List[List[float]]] = None,
) -> List[pd.DataFrame]:
    """Extract tables from PDF using Tabula."""

def organize_files_by_year(
    new_wr_folder: Path,
    old_wr_folder: Path,
) -> Dict[int, List[Path]]:
    """Organize files into year-based subdirectories."""
```

### 4. Cleaning Module (`peru_gdp_rtd.cleaners`)

**Purpose**: Data standardization and normalization.

**70+ cleaning functions across 7 modules**:

#### 4.1 `text_cleaners.py` (4 functions)
```python
def normalize_text(text: str) -> str
def remove_accents(text: str) -> str
def clean_whitespace(text: str) -> str
def standardize_sector_name(text: str, mapping: Dict) -> str
```

#### 4.2 `table_cleaners.py` (22 functions)
```python
def remove_empty_rows(df: pd.DataFrame) -> pd.DataFrame
def remove_empty_columns(df: pd.DataFrame) -> pd.DataFrame
def clean_columns_values(df: pd.DataFrame, decimal_places: int) -> pd.DataFrame
def convert_to_numeric(df: pd.DataFrame) -> pd.DataFrame
# ... 18 more functions
```

#### 4.3 `column_handlers.py` (14 functions)
```python
def rename_columns(df: pd.DataFrame, mapping: Dict) -> pd.DataFrame
def reorder_columns(df: pd.DataFrame, order: List[str]) -> pd.DataFrame
def drop_columns(df: pd.DataFrame, columns: List[str]) -> pd.DataFrame
# ... 11 more functions
```

#### 4.4 `table1_cleaners.py` (13 functions)
Table 1-specific cleaning logic (monthly GDP data)

#### 4.5 `table2_cleaners.py` (13 functions)
Table 2-specific cleaning logic (quarterly/annual GDP data)

#### 4.6 `old_table_cleaner.py` (1 class)
```python
class OldTableCleaner:
    """Cleaner for OLD CSV files (pre-2013)."""

    def clean(self) -> pd.DataFrame:
        """Apply complete cleaning pipeline."""
```

#### 4.7 `new_table_cleaner.py` (1 class)
```python
class NewTableCleaner:
    """Cleaner for NEW PDF files (2013+)."""

    def clean(self) -> pd.DataFrame:
        """Apply complete cleaning pipeline."""
```

**Design Pattern**: Strategy pattern with composable functions.

### 5. Transformation Module (`peru_gdp_rtd.transformers`)

**Purpose**: RTD construction and format conversion.

**Files**:
- `vintage_preparator.py` - Prepare vintage datasets
- `concatenator.py` - Merge vintages into RTD (372 lines)
- `metadata_handler.py` - Base-year tracking (655 lines)
- `releases_converter.py` - Convert to releases format (241 lines)

**Key Classes**:
```python
class VintagesPreparator:
    """Prepare vintage-format datasets."""

    def prepare_vintages(self) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """Return monthly and quarterly vintages."""

class MetadataHandler:
    """Handle base-year changes and benchmarks."""

    def create_benchmark_datasets(self) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """Create benchmark RTD datasets."""

class ReleasesConverter:
    """Convert RTD to releases format."""

    def convert(self, rtd: pd.DataFrame) -> pd.DataFrame:
        """Convert vintage format to releases format."""
```

### 6. Orchestration Module (`peru_gdp_rtd.orchestration`)

**Purpose**: High-level workflow coordination.

**Files**:
- `runners.py` - 6 step runner functions

**Key Functions**:
```python
def run_step1_download(settings: Settings) -> None:
    """Step 1: Download PDFs from BCRP."""

def run_step2_generate_inputs(settings: Settings) -> None:
    """Step 2: Shorten PDFs (extract key tables)."""

def run_step3_clean_and_build(settings: Settings) -> None:
    """Step 3: Clean tables and build RTD."""

def run_step4_concatenate(settings: Settings) -> None:
    """Step 4: Concatenate RTD across years."""

def run_step5_metadata(settings: Settings) -> None:
    """Step 5: Apply metadata and benchmarks."""

def run_step6_releases(settings: Settings) -> None:
    """Step 6: Convert to releases format."""
```

### 7. Utils Module (`peru_gdp_rtd.utils`)

**Purpose**: Shared utilities and helpers.

**Files**:
- `data_manager.py` - RecordManager for idempotency
- `alerts.py` - Audio alert utilities

**Key Classes**:
```python
class RecordManager:
    """Track processed files for idempotency."""

    def is_processed(self, file_id: str) -> bool
    def mark_processed(self, file_id: str) -> None
    def get_all_processed(self) -> Set[str]
    def save(self) -> None
    def load(self) -> None

def play_alert_track(audio_file: Path) -> None:
    """Play audio alert using pygame."""
```

---

## Data Flow

### Step-by-Step Data Transformation

#### Input: BCRP Weekly Reports (PDFs)
```
Raw PDF from BCRP website
│
├─ Table 1: Monthly GDP by sector
│  - Scanned images (pre-2013)
│  - Digital tables (2013+)
│
└─ Table 2: Quarterly/Annual GDP by sector
   - Similar structure to Table 1
```

#### Step 1: Web Scraping
```python
# Input: BCRP website
# Output: PDFs in new_weekly_reports/

new_weekly_reports/
├── NS_01_enero_2020.pdf
├── NS_02_enero_2020.pdf
└── ...
```

#### Step 2: PDF Shortening
```python
# Input: Downloaded PDFs
# Output: Extracted tables in data/input/

extract_table(pdf_path, pages=[3, 4])
# Returns: [DataFrame(table1), DataFrame(table2)]
```

#### Step 3: Data Cleaning
```python
# Input: Raw extracted tables
# Output: Cleaned tables

cleaner = NewTableCleaner(df, wr_number=1234, table_num=1, config=settings)
clean_df = cleaner.clean()

# Transformations applied:
# 1. Remove empty rows/columns
# 2. Standardize sector names
# 3. Convert to numeric
# 4. Normalize text
# 5. Round to decimal places
# ... 65 more transformations
```

#### Step 4: Vintage Preparation
```python
# Input: Cleaned tables
# Output: Vintage-format datasets

preparator = VintagesPreparator(df, base_year=2007, vintage_name='2020_01')
monthly_vintage, quarterly_vintage = preparator.prepare_vintages()

# Format:
# vintage_id | sector | 2020_01 | 2020_02 | ...
```

#### Step 5: RTD Concatenation
```python
# Input: Individual vintages
# Output: Complete RTD

concatenator = RTDConcatenator(vintage_files)
rtd = concatenator.concatenate()

# Format:
# vintage_id | 2020_01 | 2020_02 | 2020_03 | ...
# 2020_02    |   3.5   |   2.1   |   NaN   | ...
# 2020_03    |   3.3   |   2.0   |   1.8   | ...
```

#### Step 6: Metadata Application
```python
# Input: RTD
# Output: Metadata-enhanced RTD

handler = MetadataHandler(config=settings)
by_adjusted_rtd = handler.apply_base_year_adjustments(rtd)
benchmark_rtd = handler.create_benchmark_datasets()
```

#### Step 7: Releases Conversion
```python
# Input: RTD
# Output: Releases-format dataset

converter = ReleasesConverter()
releases = converter.convert(rtd)

# Format:
# target_period | first_release | second_release | third_release | ...
# 2020_01       |     3.5       |      3.3       |      3.4      | ...
```

---

## Key Design Decisions

### 1. Why Pydantic for Configuration?

**Decision**: Use Pydantic models instead of plain dictionaries.

**Rationale**:
- Type safety at runtime
- Automatic validation
- Clear error messages
- IDE autocomplete support
- Self-documenting schemas

**Alternative Considered**: dataclasses
**Why Pydantic Won**: Built-in validation and YAML integration

### 2. Why Class-Based Cleaners?

**Decision**: Use `OldTableCleaner` and `NewTableCleaner` classes.

**Rationale**:
- Encapsulate state (df, wr_number, table_num, config)
- Reusable across multiple files
- Extensible via inheritance
- Clear interface (`clean()` method)

**Alternative Considered**: Pure functional approach
**Why Classes Won**: State management and extensibility

### 3. Why Separate OLD and NEW Cleaners?

**Decision**: Two separate cleaner classes instead of one with conditionals.

**Rationale**:
- Different data formats (scanned vs digital)
- Different cleaning requirements
- Avoid complex conditional logic
- Easier to maintain and test

### 4. Why RecordManager for Idempotency?

**Decision**: Track processed files in JSON records.

**Rationale**:
- Avoid reprocessing on reruns
- Resume after failures
- Efficient incremental updates
- Simple file-based persistence

**Alternative Considered**: Database (SQLite)
**Why JSON Won**: Simplicity and no external dependencies

### 5. Why 6 Separate Steps?

**Decision**: Break pipeline into 6 sequential steps.

**Rationale**:
- Modular execution (run specific steps)
- Clear checkpoints for debugging
- Easy to parallelize in future
- Matches conceptual workflow

**Alternative Considered**: Monolithic pipeline
**Why 6 Steps Won**: Flexibility and maintainability

### 6. Why Configuration-Driven?

**Decision**: Move all settings to YAML configuration.

**Rationale**:
- No code changes for customization
- Environment-specific configs
- Version-controlled settings
- Easy to share and replicate

**Alternative Considered**: Environment variables
**Why YAML Won**: Better structure and organization

---

## Extension Points

### Adding New Cleaning Functions

```python
# In cleaners/custom_cleaners.py
def my_custom_cleaning_function(df: pd.DataFrame) -> pd.DataFrame:
    """Custom cleaning logic."""
    # Your logic here
    return df

# Use in NewTableCleaner
class CustomTableCleaner(NewTableCleaner):
    def clean(self):
        df = super().clean()
        df = my_custom_cleaning_function(df)
        return df
```

### Adding New Data Sources

```python
# In scrapers/new_source_scraper.py
def scrape_new_source(url: str, settings: Settings) -> None:
    """Scrape from alternative data source."""
    # Your scraping logic
    pass

# Register in orchestration
def run_step1_download(settings: Settings) -> None:
    pdf_downloader(...)  # Existing BCRP scraper
    scrape_new_source(...)  # New source
```

### Adding New Output Formats

```python
# In transformers/custom_converter.py
class CustomFormatConverter:
    """Convert RTD to custom format."""

    def convert(self, rtd: pd.DataFrame) -> pd.DataFrame:
        """Your conversion logic."""
        pass

# Use in Step 6
converter = CustomFormatConverter()
custom_format = converter.convert(rtd)
custom_format.to_csv('data/output/custom_format.csv')
```

### Adding New Pipeline Steps

```python
# In orchestration/runners.py
def run_step7_custom(settings: Settings) -> None:
    """Step 7: Your custom processing."""
    # Your logic here
    pass

# Call from update_rtd.py
if 7 in steps_to_run:
    run_step7_custom(settings)
```

---

## Performance Considerations

### Memory Usage

**Large DataFrames**: RTD datasets can grow large over time.

**Optimization Strategies**:
1. Use `dtype` specifications when reading CSVs
2. Consider Parquet format for large datasets
3. Process data in chunks if needed
4. Use generators for iteration

```python
# Memory-efficient CSV reading
rtd = pd.read_csv(
    'data/output/monthly_gdp_rtd.csv',
    dtype={'vintage_id': 'str'},
    index_col=0,
)

# Or use Parquet
rtd.to_parquet('data/output/monthly_gdp_rtd.parquet')
rtd = pd.read_parquet('data/output/monthly_gdp_rtd.parquet')
```

### Execution Time

**Bottlenecks**:
1. PDF download (15-30 minutes)
2. PDF parsing with Tabula (5-10 minutes)
3. Data cleaning (2-5 minutes)

**Optimization Strategies**:
1. Skip download with `--skip-download`
2. Process specific years only
3. Parallel processing (future enhancement)
4. Cache intermediate results

---

## Testing Strategy

### Test Levels

1. **Unit Tests**: Individual functions
2. **Integration Tests**: Module interactions
3. **Smoke Tests**: End-to-end basic functionality
4. **System Tests**: Complete pipeline execution

### Current Test Coverage

```
tests/
├── test_smoke.py          # Basic smoke tests (7 tests)
└── [Future tests]
```

**Smoke Tests**:
- Package import
- Config loading
- Config paths
- Sector mappings
- Month mappings
- Base years
- All modules importable

---

## Future Enhancements

1. **Parallel Processing**: Process multiple years concurrently
2. **Database Backend**: SQLite for metadata and records
3. **API Server**: FastAPI for programmatic access
4. **Monitoring**: Prometheus metrics and Grafana dashboards
5. **CI/CD**: Automated testing and deployment
6. **Docker**: Containerized deployment
7. **Logging**: Structured logging with correlation IDs

---

## Additional Resources

- **Main README**: [README.md](../README.md)
- **Installation**: [docs/INSTALLATION.md](INSTALLATION.md)
- **Usage Guide**: [docs/USAGE.md](USAGE.md)
- **Contributing**: [docs/CONTRIBUTING.md](CONTRIBUTING.md)
