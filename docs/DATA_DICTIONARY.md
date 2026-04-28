# Peru GDP RTD - Data Dictionary

**Version:** 1.0.0
**Last Updated:** December 28, 2024
**Dataset:** Peru GDP Real-Time Dataset (1994-present)

---

## Table of Contents

1. [Overview](#overview)
2. [File Organization](#file-organization)
3. [Data Format Types](#data-format-types)
4. [Variable Definitions](#variable-definitions)
5. [Industry Classifications](#industry-classifications)
6. [Special Values](#special-values)
7. [Time Period Notation](#time-period-notation)
8. [Base-Year Changes](#base-year-changes)
9. [File Naming Conventions](#file-naming-conventions)
10. [Usage Examples](#usage-examples)

---

## Overview

This data dictionary describes the structure, variables, and coding conventions used in the Peru GDP Real-Time Dataset. The dataset is available in two complementary formats:

- **Vintage Format:** Tracks what data were available at each release date (columns = release dates)
- **Releases Format:** Tracks how individual observations were revised over time (columns = revision sequences)

Both formats contain the same underlying information but organized differently to facilitate different types of analysis.

---

## File Organization

### Directory Structure

```
data/output/
├── vintages/           # Vintage format datasets (8 files)
│   ├── monthly_gdp_vintages.csv
│   ├── quarterly_gdp_vintages.csv
│   ├── monthly_gdp_vintages_adjusted.csv
│   ├── quarterly_gdp_vintages_adjusted.csv
│   ├── monthly_gdp_vintages_benchmark.csv
│   ├── quarterly_gdp_vintages_benchmark.csv
│   ├── monthly_gdp_vintages_adjusted_benchmark.csv
│   └── quarterly_gdp_vintages_adjusted_benchmark.csv
│
└── releases/           # Releases format datasets (8 files)
    ├── monthly_gdp_releases.csv
    ├── quarterly_gdp_releases.csv
    ├── monthly_gdp_releases_adjusted.csv
    ├── quarterly_gdp_releases_adjusted.csv
    ├── monthly_gdp_releases_benchmark.csv
    ├── quarterly_gdp_releases_benchmark.csv
    ├── monthly_gdp_releases_adjusted_benchmark.csv
    └── quarterly_gdp_releases_adjusted_benchmark.csv
```

### File Count
- **Total:** 16 CSV files
- **Vintages:** 8 files
- **Releases:** 8 files

---

## Data Format Types

### Format 1: Vintage Format (8 files in `vintages/`)

**Structure:** Long-format panel data where each row represents an observation in a specific vintage.

**Index Columns:**
- **Row number** (unnamed column 0): Sequential row identifier
- **`industry`** (string): Economic sector code
- **`vintage`** (string): Publication date in `YYYYmM` format

**Data Columns:**
- **`tp_YYYYmM`** (float): Target period columns, where:
  - `tp` = "target period" prefix
  - `YYYYmM` = year and month of the reference period
  - Example: `tp_2020m1` = January 2020
  - Values: GDP growth rates (year-over-year percentage change)

**Example:**
```
| (index) | industry | vintage | tp_2019m1 | tp_2019m2 | tp_2019m3 | ...
|---------|----------|---------|-----------|-----------|-----------|
| 0       | gdp      | 2019m2  | 2.3       | NaN       | NaN       | ...
| 1       | gdp      | 2019m3  | 2.3       | 2.5       | NaN       | ...
| 2       | gdp      | 2019m4  | 2.3       | 2.4       | 2.6       | ...
```

**Interpretation:**
- Each row represents what data were available at a specific vintage (publication date)
- Columns represent reference periods (when the economic activity occurred)
- `NaN` values indicate data not yet published at that vintage
- This format answers: "What did we know about Q1 2019 as of April 2019?"

---

### Format 2: Releases Format (8 files in `releases/`)

**Structure:** Wide-format panel data where each row represents a target period.

**Index Column:**
- **`target_period`** (string): Reference period in `YYYYmM`, `YYYYqQ`, or `YYYY` format

**Data Columns:**
- **`industry_N`** (float): Revision sequence columns, where:
  - `industry` = sector code (e.g., `gdp`, `agriculture`, `manufacturing`)
  - `N` = revision number (1, 2, 3, ...)
  - Example: `gdp_1` = First release (flash estimate) for total GDP
  - Example: `gdp_2` = Second release (first revision) for total GDP
  - Example: `gdp_3` = Third release (second revision) for total GDP
  - Values: GDP growth rates (year-over-year percentage change)

**Revision Sequence:**
- **`_1`**: First release (flash estimate, typically 2-4 weeks after period end)
- **`_2`**: Second release (first revision, typically 1 month after first release)
- **`_3`**: Third release (second revision)
- **`_4`, `_5`, ..., `_N`**: Subsequent revisions (can go up to 19+ revisions for some periods)

**Example:**
```
| target_period | gdp_1 | gdp_2 | gdp_3 | agriculture_1 | agriculture_2 | ...
|---------------|-------|-------|-------|---------------|---------------|
| 2019m1        | 2.3   | 2.3   | 2.4   | 3.5           | 3.5           | ...
| 2019m2        | 2.5   | 2.4   | 2.4   | 3.6           | 3.7           | ...
| 2019m3        | 2.6   | 2.5   | 2.6   | -2.4          | -2.3          | ...
```

**Interpretation:**
- Each row represents a specific reference period
- Columns show the sequence of published values for that period
- `NaN` values indicate revisions not yet occurred
- This format answers: "How was January 2019 GDP initially reported and how was it revised?"

---

## Variable Definitions

### Vintage Format Variables

| Variable | Type | Description | Example Values |
|----------|------|-------------|----------------|
| `(index)` | int | Sequential row number | 0, 1, 2, ... |
| `industry` | string | Economic sector code | "gdp", "agriculture", "manufacturing" |
| `vintage` | string | Publication date (YYYYmM format) | "2020m1", "2020m2", "2020m3" |
| `tp_YYYYmM` | float | GDP growth rate for target period YYYY month M | -15.3, 0.0, 3.5, 12.7 |
| `tp_YYYYqQ` | float | GDP growth rate for target period YYYY quarter Q | 2.3, 4.5 |
| `tp_YYYY` | float | GDP growth rate for target year YYYY | 2.4, 3.1 |

### Releases Format Variables

| Variable | Type | Description | Example Values |
|----------|------|-------------|----------------|
| `target_period` | string | Reference period (YYYYmM, YYYYqQ, or YYYY) | "2020m1", "2020q1", "2020" |
| `industry_N` | float | GDP growth rate for industry at revision N | -15.3, 0.0, 3.5, 12.7 |

**Notes:**
- GDP growth rates are **year-over-year percentage changes**
- Precision: 1 decimal place (e.g., 2.3%, not 2.28%)
- Missing values coded as `NaN` (not 0, which would indicate zero growth)
- Negative values indicate contraction

---

## Industry Classifications

### Sector Codes

The dataset includes **8 economic sectors**:

| Code (English) | Code (Spanish) | Description | ISIC Classification |
|----------------|----------------|-------------|---------------------|
| `agriculture` | `agropecuario` | Agriculture and Livestock | ISIC Section A |
| `fishing` | `pesca` | Fishing | ISIC Section B (part) |
| `mining` | `minería e hidrocarburos` | Mining and Hydrocarbons | ISIC Section B (part), C |
| `manufacturing` | `manufactura` | Manufacturing | ISIC Section D |
| `electricity` | `electricidad y agua` | Electricity and Water | ISIC Section E |
| `construction` | `construcción` | Construction | ISIC Section F |
| `commerce` | `comercio` | Commerce | ISIC Section G |
| `services` | `otros servicios` | Other Services | ISIC Sections H-P |
| `gdp` | `pbi` | Total GDP | All sections |

**Additional Aggregates (in some files):**
- **`primary_sector`**: Agriculture + Fishing + Mining
- **`non_primary`**: All sectors except primary (GDP - primary_sector)

### Sector Hierarchy

```
GDP (Total)
├── Primary Sector
│   ├── Agriculture and Livestock
│   ├── Fishing
│   └── Mining and Hydrocarbons
│
└── Non-Primary Sector
    ├── Manufacturing
    ├── Electricity and Water
    ├── Construction
    ├── Commerce
    └── Other Services
```

### Industry Code Mapping

The dataset uses standardized English names. Original Spanish names from BCRP are mapped as follows:

| Spanish (BCRP Source) | English (Dataset) |
|----------------------|-------------------|
| Agropecuario | agriculture |
| Pesca | fishing |
| Minería e Hidrocarburos | mining |
| Manufactura | manufacturing |
| Electricidad y Agua | electricity |
| Construcción | construction |
| Comercio | commerce |
| Otros Servicios | services |
| PBI | gdp |

**Note:** The mapping handles variations and typos (e.g., "construccion" → "construcción" → "construction")

---

## Special Values

### Sentinel Value: `-999999.0`

**Meaning:** Observation affected by base-year methodology change

**When it appears:**
- Present **only** in files with prefix `by_adjusted_` (base-year adjusted)
- Marks observations during periods when BCRP changed the GDP calculation base year
- Indicates data are not comparable to other periods without adjustment

**Affected Vintages:**

| Base Year Change | First Affected Vintage | Reason |
|-----------------|----------------------|---------|
| 1990 → 1994 | 1994m1 (January 1994) | Introduction of 1994 base year |
| 1994 → 2007 | 2000m7 (WR 28, 2000) | Introduction of 2007 base year |
| 2007 → 2019 | 2014m3 (WR 11, 2014) | Introduction of 2019 base year* |

*Note: The 2019 base year change is not currently in effect (removed from config as of Dec 2024).

**Example:**
```
| target_period | gdp_1    | gdp_2    | gdp_3    |
|---------------|----------|----------|----------|
| 1999m12       | 0.9      | 1.0      | 1.0      |  ← Base 1994
| 2000m1        | -999999.0| -999999.0| -999999.0|  ← Base year change
| 2000m2        | 3.2      | 3.1      | 3.2      |  ← Base 2007
```

**Interpretation:**
- Values before change: Calculated using 1994 base year
- Values after change: Calculated using 2007 base year
- Sentinel values mark the transition period
- Not directly comparable without rebasing

**Files with Sentinel Values:**
- `monthly_gdp_vintages_adjusted.csv`
- `quarterly_gdp_vintages_adjusted.csv`
- `monthly_gdp_vintages_adjusted_benchmark.csv`
- `quarterly_gdp_vintages_adjusted_benchmark.csv`
- All 4 corresponding releases format files

**Files WITHOUT Sentinel Values (clean data):**
- `monthly_gdp_vintages.csv`
- `quarterly_gdp_vintages.csv`
- `monthly_gdp_vintages_benchmark.csv`
- `quarterly_gdp_vintages_benchmark.csv`
- All 4 corresponding releases format files

---

### Missing Values: `NaN`

**Meaning:** Data not available / not yet published

**When it appears:**

1. **Real-time data constraint** (vintage format):
   - Future periods unknown at past vintages
   - Example: In vintage 2020m1, data for 2020m2 (February 2020) is `NaN` because it hasn't occurred yet

2. **Publication lags**:
   - Recent periods may not yet be published
   - BCRP publishes with ~2-4 week lag

3. **No further revisions** (releases format):
   - If a period has only 3 revisions, columns `_4`, `_5`, ... will be `NaN`

4. **Historical gaps**:
   - Some early periods (1992-1993) have incomplete coverage due to limited archive availability

**Interpretation:**
- `NaN` ≠ Zero growth (zero growth is coded as `0.0`)
- `NaN` = Data point does not exist or is not yet available
- Normal and expected in real-time datasets

---

In wide-format vintages and releases datasets, missingness can be high even when the data product is behaving correctly. This is a structural feature of real-time panels:

- In vintages files, each row is one publication snapshot, so many future `tp_*` columns are naturally unavailable at that vintage.
- In releases files, later revision columns remain `NaN` until those revisions actually occur.
- Missingness should therefore be interpreted relative to publication timing, not as evidence of a pipeline failure by itself.

---

### Large-Magnitude Values

Some observations may fall outside a simple screening range such as `[-50, 50]`. These values should be interpreted carefully, but they are not automatically coding errors.

Potential sources include:

- genuine extreme short-run movements in specific sectors or unusual reporting periods
- benchmark revisions and methodological changes
- base-year transitions
- source-table peculiarities inherited from the published Weekly Reports

Examples flagged during validation include values such as `990.00`, `232.50`, and `-90.40`. These should be reviewed substantively when used in analysis, especially if they appear in a small number of target periods or sectors.

The sentinel value `-999999.0` is different from those cases: it is an intentional marker for base-year-affected observations in adjusted datasets and should not be treated as an economic growth rate.

---

## Time Period Notation

### Monthly Periods

**Format:** `YYYYmM`

- **YYYY:** 4-digit year
- **m:** Literal character "m" (for "month")
- **M:** 1- or 2-digit month (1-12)

**Examples:**
- `2020m1` = January 2020
- `2020m12` = December 2020
- `2019m3` = March 2019

**Range in Dataset:** `1992m1` to `2024m12` (and beyond)

---

### Quarterly Periods

**Format:** `YYYYqQ`

- **YYYY:** 4-digit year
- **q:** Literal character "q" (for "quarter")
- **Q:** 1-digit quarter (1-4)

**Examples:**
- `2020q1` = Q1 2020 (January-March)
- `2020q2` = Q2 2020 (April-June)
- `2020q3` = Q3 2020 (July-September)
- `2020q4` = Q4 2020 (October-December)

**Range in Dataset:** `1992q1` to `2024q4` (and beyond)

---

### Annual Periods

**Format:** `YYYY`

- **YYYY:** 4-digit year

**Examples:**
- `2020` = Calendar year 2020
- `2019` = Calendar year 2019

**Range in Dataset:** `1992` to `2024` (and beyond)

---

### Vintage Dates

**Format:** `YYYYmM` (same as monthly periods)

**Meaning:** Publication date of the BCRP Weekly Report

**Examples:**
- `2020m1` = Published in January 2020
- `2020m2` = Published in February 2020

**Notes:**
- Vintages are at monthly frequency (one publication per month)
- Actual publication is weekly, but data aggregated to monthly vintages
- Multiple weekly reports in a month → Last report of month used as "vintage"

---

## Base-Year Changes

### What is a Base Year?

The **base year** is the reference year for calculating GDP in constant prices. When BCRP changes the base year, they update:
- Sector weights (relative importance of industries)
- Data sources
- Calculation methodology
- Historical data (rebased to new year)

**Result:** Structural break in time series

---

### Historical Base Year Changes in Peru

| Period | Base Year | Effective From | Notes |
|--------|-----------|----------------|-------|
| 1992-1993 | 1990 | 1992m1 | Initial base year in dataset |
| 1994-1999 | 1994 | 1994m1 (WR 1, 1994) | First change in dataset |
| 2000-2013 | 2007 | 2000m7 (WR 28, 2000) | Second change in dataset |
| 2014-present | 2007 | 2014m3 (WR 11, 2014) | Most recent change |

**Note:** The 2019 base year was announced but not yet implemented in the dataset as of December 2024.

---

### Impact on Data

**Example: 2000m7 Base Year Change (1994 → 2007)**

Before change (1994 base):
```
1999m12: GDP = 0.9% growth
2000m1:  GDP = 3.0% growth
2000m2:  GDP = 3.2% growth
```

After change (2007 base):
```
1999m12: GDP = 1.0% growth   ← Rebased to 2007
2000m1:  GDP = 3.1% growth   ← New methodology
2000m2:  GDP = 3.2% growth   ← New methodology
```

**Result:** All historical values potentially revised

---

### Dataset Handling of Base Year Changes

#### **Option 1: Regular Files (no prefix)**

Files: `monthly_gdp_vintages.csv`, `quarterly_gdp_vintages.csv`, etc.

**Handling:** Clean data with all base year changes incorporated
- Historical values rebased to current base year
- No structural breaks
- Directly comparable across all periods
- **Use these for:** Most analyses, forecasting, general research

#### **Option 2: Base-Year Adjusted Files (`by_adjusted_` prefix)**

Files: `monthly_gdp_vintages_adjusted.csv`, etc.

**Handling:** Original data preserved with sentinel values marking changes
- Sentinel value `-999999.0` flags affected observations
- Shows raw revision pattern including base year effects
- Historical values NOT rebased
- **Use these for:** Studying revision behavior, understanding base year impacts

#### **Option 3: Benchmark Files (`_benchmark` suffix)**

Files: `monthly_gdp_vintages_benchmark.csv`, etc.

**Handling:** Only observations from stable base year periods
- Excludes observations around base year change points
- Pre-2000 data (1994 base) isolated from post-2000 data (2007 base)
- **Use these for:** Econometric models requiring consistent methodology

---

### Identifying Base Year Changes

**Method 1: Check metadata**
```bash
# Read metadata/wr_metadata.csv
# Look for rows where benchmark_revision == True
```

**Method 2: Look for sentinel values**
```python
# In by_adjusted_* files
import pandas as pd
df = pd.read_csv('monthly_gdp_vintages_adjusted.csv')
base_year_changes = df[df == -999999.0].dropna(how='all')
```

**Method 3: Check configuration**
```yaml
# In config/config.yaml
metadata:
  base_years:
    - year: 1994, wr: 1, base_year: 1990
    - year: 2000, wr: 28, base_year: 1994
    - year: 2014, wr: 11, base_year: 2007
```

---

## File Naming Conventions

### Prefix: `by_adjusted_`

**Meaning:** Base-year adjusted dataset

**Indicates:**
- Contains sentinel values (`-999999.0`) marking base year changes
- Preserves original revision patterns including methodological changes
- NOT directly comparable across base year boundaries without adjustment

**Files:**
- `monthly_gdp_vintages_adjusted.csv`
- `quarterly_gdp_vintages_adjusted.csv`
- `monthly_gdp_vintages_adjusted_benchmark.csv`
- `quarterly_gdp_vintages_adjusted_benchmark.csv`
- `monthly_gdp_releases_adjusted.csv`
- `quarterly_gdp_releases_adjusted.csv`
- `monthly_gdp_releases_adjusted_benchmark.csv`
- `quarterly_gdp_releases_adjusted_benchmark.csv`

---

### Suffix: `_benchmark`

**Meaning:** Benchmark dataset (stable methodology periods only)

**Indicates:**
- Excludes observations affected by base year changes
- Contains only data from periods with consistent methodology
- Suitable for econometric estimation without structural breaks

**Files:**
- `monthly_gdp_vintages_benchmark.csv`
- `quarterly_gdp_vintages_benchmark.csv`
- `monthly_gdp_vintages_adjusted_benchmark.csv`
- `quarterly_gdp_vintages_adjusted_benchmark.csv`
- `monthly_gdp_releases_benchmark.csv`
- `quarterly_gdp_releases_benchmark.csv`
- `monthly_gdp_releases_adjusted_benchmark.csv`
- `quarterly_gdp_releases_adjusted_benchmark.csv`

---

### Suffix: `_releases`

**Meaning:** Releases format (revision sequences)

**Indicates:**
- Data organized by target period (rows) and revision sequence (columns)
- Columns: `industry_1`, `industry_2`, `industry_3`, etc.
- Facilitates revision analysis

**Files:** All 8 files in `data/output/releases/` directory

---

### Frequency Indicators

**`monthly_`**: Monthly frequency data
- Target periods: `YYYYmM` (e.g., `2020m1`)
- 12 observations per year

**`quarterly_annual_`**: Quarterly and annual frequency combined
- Target periods: `YYYYqQ` (e.g., `2020q1`) and `YYYY` (e.g., `2020`)
- 4 quarterly + 1 annual = 5 observations per year

---

### Full Naming Pattern

**Pattern:** `[prefix]_[frequency]_gdp_[variant][_format].[ext]`

**Components:**
- `[prefix]`: `by_adjusted` (optional)
- `[frequency]`: `monthly` or `quarterly_annual`
- `[variant]`: `rtd` or `benchmark`
- `[_format]`: `_releases` (optional, indicates releases format)
- `[ext]`: `csv` or `parquet`

**Examples:**
- `monthly_gdp_vintages.csv` → Monthly RTD, vintage format, all data
- `monthly_gdp_releases_adjusted_benchmark.csv` → Monthly benchmark, releases format, with base-year sentinels
- `quarterly_gdp_vintages.parquet` → Quarterly/annual RTD, vintage format, Parquet file

---

## Usage Examples

### Example 1: Loading Vintage Format Data

```python
import pandas as pd

# Load monthly RTD (vintage format)
df_vintage = pd.read_csv('data/output/vintages/monthly_gdp_vintages.csv', index_col=0)

# Filter to specific industry
gdp_data = df_vintage[df_vintage['industry'] == 'gdp']

# Get all vintages for a specific target period (January 2020)
jan_2020 = gdp_data['tp_2020m1']

# Result: Time series showing how Jan 2020 GDP was reported across all vintages
print(jan_2020.head())
```

**Output:**
```
vintage
2020m2    -15.3
2020m3    -15.5
2020m4    -15.7
...
```

---

### Example 2: Loading Releases Format Data

```python
import pandas as pd

# Load monthly releases (releases format)
df_releases = pd.read_csv('data/output/releases/monthly_gdp_releases.csv', index_col=0)

# Get revision sequence for January 2020 GDP
jan_2020_revisions = df_releases.loc['2020m1', ['gdp_1', 'gdp_2', 'gdp_3']]

# Result: Shows 1st, 2nd, 3rd releases for Jan 2020
print(jan_2020_revisions)
```

**Output:**
```
gdp_1   -15.3  (1st release, flash estimate)
gdp_2   -15.5  (2nd release, 1st revision)
gdp_3   -15.7  (3rd release, 2nd revision)
```

---

### Example 3: Handling Missing Values

```python
import pandas as pd

df = pd.read_csv('data/output/vintages/monthly_gdp_vintages.csv', index_col=0)

# Count missing values by vintage
missing_by_vintage = df.groupby('vintage').apply(lambda x: x.isnull().sum().sum())

# Fill missing with forward fill (carry last known value forward)
df_filled = df.fillna(method='ffill')

# Or drop rows with any missing values
df_complete = df.dropna()
```

---

### Example 4: Identifying Base Year Changes

```python
import pandas as pd

# Load base-year adjusted file
df_adj = pd.read_csv('data/output/vintages/monthly_gdp_vintages_adjusted.csv', index_col=0)

# Find sentinel values
sentinel = -999999.0
base_year_affected = df_adj == sentinel

# Get target periods affected
affected_periods = base_year_affected.any(axis=0)
affected_cols = affected_periods[affected_periods].index.tolist()

print(f"Periods with base year changes: {affected_cols}")
```

**Output:**
```
Periods with base year changes: ['tp_1994m1', 'tp_2000m7', 'tp_2014m3']
```

---

### Example 5: Calculating Revision Statistics

```python
import pandas as pd
import numpy as np

# Load releases format
df = pd.read_csv('data/output/releases/monthly_gdp_releases.csv', index_col=0)

# Calculate revision (2nd release - 1st release)
df['revision_1to2'] = df['gdp_2'] - df['gdp_1']

# Mean absolute revision
mean_abs_revision = df['revision_1to2'].abs().mean()

# Revision distribution
print(df['revision_1to2'].describe())
```

---

### Example 6: Comparing Frequencies

```python
import pandas as pd

# Load monthly data
df_monthly = pd.read_csv('data/output/vintages/monthly_gdp_vintages.csv', index_col=0)

# Load quarterly data
df_quarterly = pd.read_csv('data/output/vintages/quarterly_gdp_vintages.csv', index_col=0)

# Monthly columns: tp_2020m1, tp_2020m2, ...
# Quarterly columns: tp_2020q1, tp_2020q2, ...

# Note: Quarterly values are NOT simple averages of monthly values
# They are independently published by BCRP
```

---

## Data Quality Notes

### Completeness

- **1992-1993:** Partial coverage due to limited digital archive
- **1994-2001:** Good coverage, some gaps
- **2002-present:** Complete coverage

### Accuracy

- **Source:** Official BCRP publications (authoritative)
- **Extraction:** Automated pipeline with 70+ cleaning functions
- **Validation:** Monotonicity checks, continuity validation, format standardization

### Known Limitations

1. **Pre-2002 Gaps:** Some vintages missing due to unavailable source PDFs
2. **Base-Year Discontinuities:** Structural breaks at 1994, 2000, 2014
3. **Revision Depth:** Number of revisions varies (some periods have 19+, others only 1-2)
4. **Publication Frequency:** Weekly reports aggregated to monthly vintages (may lose intra-month variation)

### Quality Assurance

- Timestamp-based incremental processing (prevents duplicates)
- Automated monotonicity checks (vintage dates must be sequential)
- Continuity validation (no unexpected gaps in time series)
- Format standardization (consistent sector names, date formats)
- Base-year change tracking (metadata-driven flagging)

---

## Version History

### Version 1.0.0 (December 2024)
- Initial public release
- Coverage: 1992-2024
- 16 dataset files (8 vintage + 8 releases formats)
- 1000+ vintages tracked
- Complete documentation

---

## Support and Contact

For questions about data definitions or usage:

- **GitHub Issues:** https://github.com/[username]/peru_gdp_revisions/issues
- **Email:** [your.email@institution.edu]
- **Documentation:** See project README and guides in `docs/`

For questions about source data or BCRP methodology:

- **BCRP Website:** https://www.bcrp.gob.pe
- **Weekly Reports:** https://www.bcrp.gob.pe/publicaciones/nota-semanal.html

---

**Document Version:** 1.0
**Last Updated:** December 28, 2024
**Maintainer:** Peru GDP RTD Project Team
