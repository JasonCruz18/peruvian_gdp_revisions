# Peru GDP Real-Time Dataset (1994-present)
## Data in Brief - Manuscript Draft

**Status:** DRAFT - Awaiting DOIs
**Date:** December 28, 2024
**Version:** 0.9 (Pre-submission)

---

## INSTRUCTIONS FOR COMPLETION

This draft contains all DIB manuscript sections. Complete the following before submission:

### Required Actions:
1. **[TODO]** Add Data DOI (from Zenodo upload) → See `[DATA_DOI]` placeholders
2. **[TODO]** Add Code DOI (from GitHub release) → See `[CODE_DOI]` placeholders
3. **[TODO]** Add your name, affiliation, ORCID → See `[YOUR_*]` placeholders
4. **[TODO]** Add email address → See `[YOUR_EMAIL]` placeholder
5. **[TODO]** Review and customize "Value of the Data" section
6. **[TODO]** Add any figures or tables (optional but recommended)
7. **[TODO]** Final proofreading

### How to Use:
1. Copy sections into DIB template Word document (`DIB/data-in-brief-article-template.docx`)
2. Replace all `[PLACEHOLDER]` values with actual information
3. Format according to template style
4. Submit via Editorial Manager

---

## TITLE PAGE

### Article Title
**Peru GDP Real-Time Dataset (1994-present)**

### Author Information
**Jason Cruz¹,***
**[ORCID]:** https://orcid.org/[JASON_ORCID]

**Diego Winkelried¹**
**[ORCID]:** https://orcid.org/[DIEGO_ORCID]

**Javier Torres¹**
**[ORCID]:** https://orcid.org/[JAVIER_ORCID]

**Affiliations:**
¹ Centro de Investigación (CIUP), Universidad del Pacífico, Lima, Peru

**Corresponding Author:**
* Jason Cruz
Email: jj.cruza@up.edu.pe
Address: Universidad del Pacífico, Av. Salaverry 2020, Jesús María, Lima, Peru

---

## SPECIFICATIONS TABLE

| Subject | Economics, Econometrics, Macroeconomics |
|---------|----------------------------------------|
| Specific subject area | Real-Time Macroeconomic Data, GDP Revisions, Nowcasting |
| Type of data | Tables (CSV format) |
| How data were acquired | Web scraping (Selenium), PDF extraction (Tabula-py), systematic data cleaning pipeline |
| Data format | Raw and processed |
| Parameters for data collection | GDP growth rates from BCRP Weekly Reports (Nota Semanal), 1994-present |
| Description of data collection | Automated 6-stage pipeline: (1) PDF download via web scraping, (2) Table extraction from PDFs, (3) Data cleaning (70+ functions), (4) Vintage construction, (5) Metadata handling and base-year adjustments, (6) Releases format conversion |
| Data source location | **Institution:** Banco Central de Reserva del Perú (BCRP)<br>**City/Country:** Lima, Peru<br>**URLs:**<br>• Current reports: https://www.bcrp.gob.pe/publicaciones/nota-semanal.html<br>• Historical archive: https://www.bcrp.gob.pe/publicaciones/nota-semanal/nota-semanal-archivo.html |
| Data accessibility | **Repository:** Zenodo<br>**Data DOI:** [DATA_DOI]<br>**Data URL:** https://doi.org/[DATA_DOI]<br>**Code Repository:** GitHub<br>**Code DOI:** [CODE_DOI]<br>**Code URL:** https://github.com/JasonCruz18/peru_gdp_revisions<br>**License:** Data: CC-BY-4.0, Code: MIT<br>**Files:** 16 CSV files (~17 MB total) |
| Related research article | [OPTIONAL: Add reference to your forthcoming research paper]<br>Example: Author(s), "Rationality and Nowcasting on Peruvian GDP Revisions," Journal Name (in preparation) |

---

## ABSTRACT

This data article describes a comprehensive real-time database (RTD) of Peru's Gross Domestic Product (GDP) growth rates spanning from 1994 to the present. The dataset tracks over 1,000 vintages of GDP data sourced from the Central Reserve Bank of Peru (Banco Central de Reserva del Perú, BCRP) Weekly Reports. The data are systematically transformed into two complementary formats: (1) vintage format, where columns represent release dates enabling analysis of information available at specific points in time, and (2) releases format, where columns represent revision sequences facilitating the study of how initial estimates are revised over time. The dataset includes monthly, quarterly, and annual GDP growth rates for 8 economic sectors (agriculture, fishing, mining, manufacturing, electricity and water, construction, commerce, and other services), along with total GDP. Special attention is given to methodological changes in base-year calculations (1990, 1994, 2007), with alternative versions of the dataset that either incorporate these changes seamlessly or flag affected observations with sentinel values. The data are provided in CSV format (16 files, 17 MB total) and are fully reproducible using the accompanying open-source Python pipeline. This dataset enables research on GDP revision patterns, real-time forecasting, nowcasting, forecast evaluation, cross-country comparisons of statistical practices, and policy analysis in emerging market contexts.

**Keywords:** GDP; Real-time data; Peru; Economic revisions; Nowcasting; Macroeconomic data; Time series

---

## VALUE OF THE DATA

### Why are these data valuable?

• **Enables revision analysis:** The dataset provides a complete revision history of Peru's GDP, allowing researchers to study patterns in how initial estimates are revised over time. This is crucial for understanding the quality of real-time economic information in emerging markets.

• **Supports nowcasting and real-time forecasting:** By preserving what data were available at each point in time (vintage format), the dataset enables realistic out-of-sample forecasting exercises that respect the information constraints faced by forecasters and policymakers.

• **Facilitates forecast evaluation:** Researchers can assess the accuracy of forecasts using the data that were actually available when forecasts were made, rather than final revised data. This provides more realistic evaluation of forecasting methods.

• **Enables policy analysis:** The dataset allows researchers to understand what information was available to policymakers at decision points, enabling better evaluation of policy decisions and recommendations for improving real-time data quality.

• **Supports cross-country research:** As one of few publicly available real-time GDP datasets for an emerging South American economy, it enables comparative studies of revision patterns, statistical practices, and data quality across developed and developing economies.

• **Provides methodological transparency:** The fully documented and reproducible data construction process serves as a template for creating real-time datasets for other countries or economic variables, promoting open science in macroeconomic research.

### Who can benefit from these data?

• **Academic researchers** studying business cycles, forecasting, monetary policy, fiscal policy, or statistical agency practices in emerging markets

• **Central bank economists** conducting nowcasting, forecasting, or policy analysis for Peru or similar economies

• **International organizations** (IMF, World Bank, IDB) analyzing economic conditions in Peru or conducting cross-country studies of data quality

• **Graduate students** learning about real-time data analysis, forecasting methods, or emerging market macroeconomics

• **Policy analysts** evaluating the quality of economic statistics and recommending improvements to statistical agencies

• **Data scientists** interested in time series analysis, revision modeling, or applied econometrics in emerging markets

### How can these data be used?

• **Revision analysis:** Study systematic patterns in GDP revisions (bias, efficiency, predictability) to assess the quality of preliminary estimates

• **Nowcasting:** Develop models to predict current-quarter GDP using mixed-frequency data and incomplete information

• **Forecast evaluation:** Test forecasting models using real-time data to obtain unbiased performance metrics

• **Real-time vs. final data comparisons:** Quantify how conclusions change when using preliminary vs. revised data

• **Base-year methodology analysis:** Study the impact of base-year changes on GDP measurement and revision patterns

• **Cross-country comparisons:** Compare Peru's revision patterns with other countries (using datasets like ALFRED for the U.S., Euro Area RTD, or UK real-time databases)

• **Methodological research:** Test and develop new methods for handling real-time data, revisions, and mixed-frequency models

### What is unique about these data?

• **First comprehensive real-time GDP dataset for Peru:** No other publicly available dataset provides this level of vintage tracking for Peru

• **Dual format design:** Both vintage format (columns = release dates) and releases format (columns = revision sequences) in a single dataset, optimized for different research questions

• **Base-year change tracking:** Systematic documentation and handling of methodological changes, with alternative dataset versions for different research needs

• **Full reproducibility:** Complete open-source pipeline with 70+ cleaning functions, enabling users to update the dataset, customize processing, or apply methods to other countries

• **Long time span:** 30+ years of data (1994-present) covering multiple business cycles and structural changes in Peru's economy

• **High-frequency coverage:** Monthly, quarterly, and annual data for all major economic sectors, not just aggregate GDP

• **Professional quality:** Automated validation checks, comprehensive documentation, cross-platform compatibility, and production-ready code

---

## DATA DESCRIPTION

### Overview

The Peru GDP Real-Time Dataset consists of 16 CSV files totaling approximately 17 MB, organized into two main formats and four data variants. All files contain year-over-year GDP growth rates (percentage changes) for Peru's economy and its sectors, tracked across multiple releases from 1994 to the present.

### File Organization

The dataset is organized into two directories:

**1. Vintage Format** (`vintages/` directory, 8 files):
- Data organized with release dates as columns and reference periods as rows
- Answers: "What did we know about period X as of date Y?"
- Facilitates real-time forecasting and nowcasting exercises

**2. Releases Format** (`releases/` directory, 8 files):
- Data organized with revision sequences as columns and reference periods as rows
- Answers: "How was period X initially reported and how was it subsequently revised?"
- Facilitates revision analysis and forecast evaluation

### Data Variants

Each format contains four variants (2 formats × 4 variants = 8 files per directory):

**A. Monthly RTD** (e.g., `monthly_gdp_vintages.csv`):
- Monthly GDP growth rates
- Complete revision history
- All base-year changes incorporated seamlessly

**B. Quarterly/Annual RTD** (e.g., `quarterly_gdp_vintages.csv`):
- Quarterly and annual GDP growth rates
- Lower frequency, longer historical coverage

**C. Base-Year Adjusted RTD** (e.g., `monthly_gdp_vintages_adjusted.csv`):
- Same as (A) but with sentinel values (`-999999.0`) marking base-year affected observations
- Preserves original revision patterns including methodological changes

**D. Benchmark RTD** (e.g., `monthly_gdp_vintages_benchmark.csv`):
- Excludes observations around base-year change points
- Suitable for econometric models requiring consistent methodology

Each variant exists in both vintage and releases formats, yielding 16 total files.

### File Specifications

| File Name Pattern | Format | Frequency | Size Range | Rows | Columns |
|-------------------|--------|-----------|------------|------|---------|
| `monthly_gdp_*.csv` | Vintage | Monthly | 2.9-3.0 MB | ~5,000 | ~400 |
| `quarterly_annual_gdp_*.csv` | Vintage | Quarterly/Annual | 1.3-1.4 MB | ~2,000 | ~170 |
| `monthly_gdp_*_releases.csv` | Releases | Monthly | 192-219 KB | ~380 | ~150 |
| `quarterly_annual_gdp_*_releases.csv` | Releases | Quarterly/Annual | 171-205 KB | ~130 | ~75 |

### Economic Sectors Covered

The dataset includes 8 economic sectors:

1. **Agriculture** (`agriculture`): Agriculture and livestock
2. **Fishing** (`fishing`): Fishing and aquaculture
3. **Mining** (`mining`): Mining and hydrocarbons
4. **Manufacturing** (`manufacturing`): Manufacturing industries
5. **Electricity** (`electricity`): Electricity and water supply
6. **Construction** (`construction`): Construction
7. **Commerce** (`commerce`): Wholesale and retail trade
8. **Services** (`services`): Other services (transportation, finance, government, etc.)
9. **GDP** (`gdp`): Total GDP (all sectors)

### Time Coverage

- **Start:** January 1992 (`1992m1`) for most sectors
- **End:** Present (dataset updated as new BCRP reports published)
- **Vintages tracked:** 1,000+ release dates (monthly frequency)
- **Observations:** ~5,000 monthly observations, ~2,000 quarterly/annual observations

### Data Format Details

#### Vintage Format Structure

```
| (index) | industry | vintage | tp_2019m1 | tp_2019m2 | tp_2019m3 | ...
|---------|----------|---------|-----------|-----------|-----------|
| 0       | gdp      | 2019m2  | 2.3       | NaN       | NaN       |
| 1       | gdp      | 2019m3  | 2.3       | 2.5       | NaN       |
| 2       | gdp      | 2019m4  | 2.3       | 2.4       | 2.6       |
```

- **Index columns:** Row number, `industry` (sector code), `vintage` (publication date)
- **Data columns:** `tp_YYYYmM` (target period), values = GDP growth rates
- **Missing values:** `NaN` (data not yet published at that vintage)

#### Releases Format Structure

```
| target_period | gdp_1 | gdp_2 | gdp_3 | agriculture_1 | agriculture_2 | ...
|---------------|-------|-------|-------|---------------|---------------|
| 2019m1        | 2.3   | 2.3   | 2.4   | 3.5           | 3.5           |
| 2019m2        | 2.5   | 2.4   | 2.4   | 3.6           | 3.7           |
| 2019m3        | 2.6   | 2.5   | 2.6   | -2.4          | -2.3          |
```

- **Index column:** `target_period` (reference period)
- **Data columns:** `industry_N` where N = revision number (1, 2, 3, ...)
- **Values:** GDP growth rates (year-over-year percentage change)
- **Missing values:** `NaN` (revision not yet occurred)

### Special Values and Coding

**Missing Values (NaN):**
- Indicate data not yet available or not published
- Normal in real-time datasets (future periods unknown at past vintages)
- Do NOT represent zero growth (coded as `0.0`)

**Sentinel Values (-999999.0):**
- Present ONLY in `by_adjusted_*` files
- Mark observations affected by base-year methodology changes
- Three main change points:
  - 1994m1: Introduction of 1994 base year
  - 2000m7: Introduction of 2007 base year (Weekly Report 28, 2000)
  - 2014m3: Continuation of 2007 base year (Weekly Report 11, 2014)

### Data Quality

**Completeness:**
- 1992-1993: Partial coverage (~40% of vintages)
- 1994-2001: Good coverage (~80% of vintages)
- 2002-present: Complete coverage (~95-100% of vintages)

**Accuracy:**
- Source: Official BCRP publications (primary authority for Peru GDP)
- Extraction: Automated pipeline with validation checks
- Precision: 1 decimal place (e.g., 2.3%, not 2.28%)

**Validation:**
- Monotonicity checks (vintage dates sequential)
- Continuity validation (no unexpected gaps)
- Format standardization (consistent sector names, date formats)
- Base-year change tracking (metadata-driven flagging)

### Accompanying Documentation

In addition to the 16 data files, the repository includes:

- **README.md:** Quick start guide and project overview
- **DATA_DICTIONARY.md:** Comprehensive variable definitions (43 pages)
- **CITATION.cff:** Citation metadata
- **LICENSE:** MIT license for code, CC-BY-4.0 for data
- **metadata/wr_metadata.csv:** Revision calendar and base-year tracking
- **docs/:** 6 detailed documentation files (installation, usage, architecture, etc.)
- **notebooks/:** 7 tutorial Jupyter notebooks
- **_Supplement.tex:** 35-page technical documentation

---

## EXPERIMENTAL DESIGN, MATERIALS, AND METHODS

### Data Sources

#### Primary Source: BCRP Weekly Reports (Nota Semanal)

The data are sourced from the **Banco Central de Reserva del Perú (BCRP)** Weekly Reports (*Nota Semanal*), published every Friday since 1992.

**URLs:**
- Current reports: https://www.bcrp.gob.pe/publicaciones/nota-semanal.html
- Historical archive: https://www.bcrp.gob.pe/publicaciones/nota-semanal/nota-semanal-archivo.html

**Content:**
Each 4-page PDF report contains:
- Page 1: Cover page with report metadata
- Page 2: Monetary policy indicators
- Page 3: GDP growth rates by sector (Table 1)
- Page 4: Additional macroeconomic indicators

**Publication Frequency:** Weekly (typically Fridays)

**Historical Coverage:** 1992-present (30+ years, 1,500+ reports)

#### Data Collection Method

Data collection is fully automated using a 6-stage Python pipeline:

### Stage 1: PDF Download (Web Scraping)

**Tool:** Selenium WebDriver 4.0+

**Process:**
1. Navigate to BCRP Weekly Reports archive page
2. Extract list of available PDF URLs by year
3. Download PDFs with rate limiting (5-10 seconds between requests)
4. Organize by year: `data/raw/new_weekly_reports/YYYY/`
5. Validate downloads (file size, PDF format)

**Code:** `peru_gdp_rtd/scrapers/bcrp_scraper.py` (248 lines)

**Output:** ~1,500 PDF files, organized by year (1992-present)

### Stage 2: PDF Shortening

**Tools:** PyMuPDF 1.23+, pypdf 4.0+

**Purpose:** Extract only GDP-relevant pages to reduce processing time

**Process:**
1. Read 4-page PDF
2. Search for keywords: "ECONOMIC SECTORS" or "SECTORES ECONÓMICOS"
3. Extract pages 1 and 3 (cover + GDP table)
4. Save shortened PDF: `data/raw/new_weekly_reports/shortened_pdfs/YYYY/`

**Code:** `peru_gdp_rtd/processors/pdf_processor.py` (152 lines)

**Output:** Shortened PDFs (~50% size reduction)

### Stage 3: Vintage Construction

**Tools:** Tabula-py 2.8+, pandas 2.0+

**Sub-stages:**

#### 3a. Old Data Processing (1992-2012 CSV files)

- Source: Pre-digitized CSV files from early BCRP reports
- Location: `data/raw/old_weekly_reports/`
- Processing: Clean column names, standardize formats, parse dates
- Code: `peru_gdp_rtd/cleaners/old_table_cleaner.py` (247 lines)

#### 3b. New Data Processing (2013-present PDFs)

- Source: PDF tables extracted via Tabula
- Extraction: `tabula.read_pdf()` with custom area parameters
- Processing: 70+ cleaning functions across 7 modules
- Code: `peru_gdp_rtd/cleaners/new_table_cleaner.py` (312 lines)

#### 3c. Data Cleaning Functions (70+ functions)

**Text Cleaning** (`text_cleaners.py`, 4 functions):
- Remove special characters, normalize whitespace
- Handle Spanish accents and encoding issues
- Standardize date formats

**Table Cleaning** (`table_cleaners.py`, 22 functions):
- Remove header rows, merge split cells
- Handle multi-line sector names
- Extract numeric values from text

**Column Handling** (`column_handlers.py`, 14 functions):
- Rename columns consistently
- Map Spanish sector names to English codes
- Parse period labels (monthly, quarterly, annual)

**Sector-Specific Cleaning**:
- `table1_cleaners.py` (13 functions): Monthly GDP tables
- `table2_cleaners.py` (13 functions): Quarterly/annual tables

**Vintage Preparation** (`vintage_preparator.py`, 8 functions):
- Reshape data to vintage format
- Align sector codes across vintages
- Validate data consistency

**Code Organization:**
```
peru_gdp_rtd/cleaners/
├── text_cleaners.py       (4 functions)
├── table_cleaners.py      (22 functions)
├── column_handlers.py     (14 functions)
├── table1_cleaners.py     (13 functions)
├── table2_cleaners.py     (13 functions)
├── old_table_cleaner.py   (OldTableCleaner class)
├── new_table_cleaner.py   (NewTableCleaner class)
└── vintage_preparator.py  (8 functions)
```

**Output:** Individual vintage files, one per year
- Location: `data/input/table_1/YYYY/` (monthly)
- Location: `data/input/table_2/YYYY/` (quarterly/annual)
- Format: Parquet or CSV

### Stage 4: RTD Concatenation

**Purpose:** Merge individual vintages into unified real-time dataset

**Process:**
1. List all vintage files across years
2. Read and stack vertically (append rows)
3. Sort by vintage date and target period
4. Validate continuity (no gaps in time series)
5. Save concatenated RTD

**Code:** `peru_gdp_rtd/transformers/concatenator.py` (368 lines)

**Output:**
- `data/output/vintages/monthly_gdp_rtd.parquet` (331 KB)
- `data/output/vintages/quarterly_annual_gdp_rtd.parquet` (143 KB)

### Stage 5: Metadata Handling and Base-Year Adjustments

**Sub-stages:**

#### 5a. Metadata Extraction

**Purpose:** Track publication dates and base-year changes

**Source:** PDF metadata, filename patterns, BCRP announcements

**Process:**
1. Extract publication date from PDF or filename
2. Identify base-year change vintages from configuration
3. Create revision calendar: `metadata/wr_metadata.csv`

**Metadata Columns:**
- `year`, `wr` (week number), `month`: Publication identifiers
- `revision_calendar_tab_1`: Monthly data revision schedule
- `revision_calendar_tab_2`: Quarterly/annual data revision schedule
- `benchmark_revision`: Boolean flag for base-year changes
- `base_year`: Active base year (1990, 1994, or 2007)
- `base_year_affected`: Boolean flag for affected observations

**Code:** `peru_gdp_rtd/transformers/metadata_handler.py` (415 lines)

#### 5b. Base-Year Sentinel Application

**Purpose:** Flag observations affected by methodology changes

**Process:**
1. Read metadata to identify affected vintages
2. Replace values with sentinel `-999999.0` at change points
3. Save as `by_adjusted_*` variants

**Affected Vintages:**
- 1994m1: 1990 → 1994 base year transition
- 2000m7 (WR 28): 1994 → 2007 base year transition
- 2014m3 (WR 11): Reaffirmation of 2007 base year

**Output:**
- `by_adjusted_monthly_gdp_rtd.parquet` (328 KB)
- `by_adjusted_quarterly_annual_gdp_rtd.parquet` (139 KB)

#### 5c. Benchmark Dataset Generation

**Purpose:** Create datasets excluding base-year change periods

**Process:**
1. Filter out vintages flagged with `benchmark_revision == True`
2. Remove observations within ±6 months of change point
3. Save as `*_benchmark` variants

**Output:**
- `monthly_gdp_benchmark.parquet` (246 KB)
- `quarterly_annual_gdp_benchmark.parquet` (100 KB)

### Stage 6: Releases Format Conversion

**Purpose:** Transform vintage format to releases format

**Algorithm:**
1. For each target period (reference period):
   - Extract all vintages containing that period
   - Sort by publication date
   - Assign revision numbers (1, 2, 3, ...)
   - Reshape: columns = revisions, rows = target periods

2. Handle multiple releases per month:
   - Keep last release of each month as representative vintage
   - Earlier releases within same month considered duplicates

**Code:** `peru_gdp_rtd/transformers/releases_converter.py` (122 lines)

**Output:** 8 releases format files in `data/output/releases/`

### Incremental Processing (Timestamp-Based)

**Purpose:** Efficient pipeline re-runs (only process changed data)

**Method:**
- Compare file modification timestamps (source vs. output)
- Skip processing if output newer than source
- Similar to Make/CMake/Ninja build systems

**Implementation:**
- `peru_gdp_rtd/orchestration/validation.py` (151 lines)
- `needs_processing(source, output, force)` function
- Checks: output exists? output older than source?

**Benefits:**
- ~90% time reduction for incremental updates
- Self-healing (auto-rebuilds deleted outputs)
- No manual record file management

### Pipeline Orchestration

**Main Script:** `scripts/update_rtd.py` (448 lines)

**Execution:**
```bash
python scripts/update_rtd.py [--force] [--verbose]
```

**Flags:**
- `--force`: Reprocess all files (ignore timestamps)
- `--verbose`: Detailed logging

**Typical Runtime:**
- Full pipeline (cold start): ~15 minutes
- Incremental update: ~2 minutes

### Software and Dependencies

**Core Dependencies:**
- Python 3.10+
- pandas 2.0+ (data manipulation)
- numpy 1.24+ (numerical computing)
- pyyaml 6.0+ (configuration)
- selenium 4.0+ (web scraping)
- tabula-py 2.8+ (PDF extraction, requires Java 8+)
- PyMuPDF 1.23+ (PDF processing)

**Development Dependencies:**
- pytest 7.4+ (testing)
- black 23.0+ (code formatting)
- isort 5.12+ (import sorting)

**System Requirements:**
- Operating System: Windows, macOS, or Linux
- RAM: 4 GB minimum
- Disk Space: 2 GB (includes source PDFs)
- Java: Version 8+ (for Tabula-py)

**Installation:**
```bash
# Clone repository
git clone https://github.com/JasonCruz18/peru_gdp_revisions.git
cd peru_gdp_revisions

# Install dependencies
pip install -e .

# Or use conda
conda env create -f environment.yml
conda activate gdp_revisions
```

### Data Validation

**Quality Checks Implemented:**

1. **Timestamp Validation:** Ensure vintage dates are monotonic
2. **Continuity Checks:** No unexpected gaps in time series
3. **Range Validation:** GDP growth rates within plausible bounds (-50% to +50%)
4. **Sector Consistency:** All vintages contain same sectors
5. **Format Standardization:** Consistent column names, date formats

**Code:** `peru_gdp_rtd/orchestration/validation.py`

### Reproducibility

**Full reproducibility ensured by:**

1. **Version Control:** All code on GitHub with release tags
2. **Dependency Management:** Pinned versions in `requirements.txt`
3. **Configuration Files:** All parameters in `config/config.yaml`
4. **Automated Pipeline:** One-command execution (`python scripts/update_rtd.py`)
5. **Comprehensive Documentation:** 6 markdown guides + API documentation
6. **Test Suite:** 7 smoke tests covering critical path

**To Reproduce:**
```bash
# 1. Clone repository and install
git clone https://github.com/JasonCruz18/peru_gdp_revisions.git
cd peru_gdp_revisions
pip install -e .

# 2. Run pipeline
python scripts/update_rtd.py

# 3. Verify outputs
pytest tests/
```

**Expected Processing Time:** ~15-20 minutes (first run)

---

## ETHICS STATEMENT

This research uses publicly available data from the Banco Central de Reserva del Perú (BCRP). All source data are official government publications available without restrictions on the BCRP website. No human subjects were involved in this research. No ethical approval was required.

---

## DECLARATION OF COMPETING INTEREST

The authors declare that they have no known competing financial interests or personal relationships that could have appeared to influence the work reported in this paper.

---

## CREDIT AUTHOR STATEMENT

**Jason Cruz:** Conceptualization, Data curation, Formal analysis, Investigation, Methodology, Software, Validation, Visualization, Writing - original draft, Writing - review & editing.

**Diego Winkelried:** Conceptualization, Formal analysis, Methodology, Supervision, Writing - review & editing.

**Javier Torres:** Conceptualization, Formal analysis, Methodology, Supervision, Writing - review & editing.

---

## ACKNOWLEDGMENTS

The authors thank the Banco Central de Reserva del Perú (BCRP) for maintaining the Weekly Reports archive and making economic data publicly accessible.

[OPTIONAL: Add institutional acknowledgments]
[OPTIONAL: Add funding acknowledgments - see Funding section]

---

## FUNDING

[OPTION 1: If funded]
This work was supported by [Funding Organization] under Grant [Number]. The funding source had no involvement in study design, data collection, analysis, interpretation, writing, or the decision to submit for publication.

[OPTION 2: If not funded]
This research did not receive any specific grant from funding agencies in the public, commercial, or not-for-profit sectors.

---

## REFERENCES

[1] Banco Central de Reserva del Perú (BCRP). Weekly Reports (Nota Semanal). Available at: https://www.bcrp.gob.pe/publicaciones/nota-semanal.html (accessed December 28, 2024).

[2] Banco Central de Reserva del Perú (BCRP). Weekly Reports Archive (Nota Semanal - Archivo). Available at: https://www.bcrp.gob.pe/publicaciones/nota-semanal/nota-semanal-archivo.html (accessed December 28, 2024).

[3] Cruz, J., Winkelried, D., & Torres, J. (2024). Peru GDP Real-Time Dataset (1994-present) [Data set]. Zenodo. https://doi.org/[DATA_DOI]

[4] Cruz, J., Winkelried, D., & Torres, J. (2024). Peru GDP RTD: Code Repository (v1.0.0) [Software]. Zenodo. https://doi.org/[CODE_DOI]

[OPTIONAL: Add references to related research papers, methodological papers, or similar RTD papers]

**Examples of Related RTD Literature (add if relevant):**

[5] Croushore, D., Stark, T. (2001). A real-time data set for macroeconomists. Journal of Econometrics, 105(1), 111-130.

[6] Castle, J.L., Hendry, D.F., Kitov, O.I. (2013). Forecasting and nowcasting macroeconomic variables: A methodological overview. Office for National Statistics UK, Dataset.

[7] Giannone, D., Henry, J., Lalik, M., Modugno, M. (2012). An area-wide real-time database for the euro area. Review of Economics and Statistics, 94(4), 1000-1013.

---

## APPENDIX (Optional)

### Appendix A: File Descriptions Summary

[TABLE: 16 files with descriptions, sizes, and purposes - copy from Data Description section if helpful]

### Appendix B: Sample Data Snippets

[OPTIONAL: Include 2-3 small tables showing actual data examples]

### Appendix C: Pipeline Flowchart

[OPTIONAL: Include a visual diagram of the 6-stage pipeline]

---

## END OF MANUSCRIPT

**Word Count:** ~5,000 words (estimated)

**Submission Checklist:**
- [ ] All placeholders replaced with actual values
- [ ] DOIs added (data + code)
- [ ] Author information complete with ORCID
- [ ] References formatted correctly
- [ ] Spell-checked and proofread
- [ ] Copied into Word template
- [ ] Graphical abstract prepared (optional)
- [ ] Supplementary files uploaded (if any)

---

**Document Version:** 0.9 (Pre-submission Draft)
**Last Updated:** December 28, 2024
**Next Step:** Add DOIs after Zenodo upload and GitHub release
