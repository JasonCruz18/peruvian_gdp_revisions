# Peru GDP Real-Time Dataset (1994-2025)

**Version:** 1.0.0
**Last Updated:** January 2025
**DOI:** [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.18099975.svg)](https://doi.org/10.5281/zenodo.18099975)
**License:** CC-BY-4.0
**Related Code Repository:** https://github.com/JasonCruz18/peru_gdp_revisions

---

## Overview

This dataset provides a comprehensive real-time database (RTD) of Peru's Gross Domestic Product (GDP) growth rates, tracking revisions from 1994 to 2025. The accompanying code pipeline allows for updates to extend coverage to the present and beyond. The data are sourced from the Central Reserve Bank of Peru (BCRP) Weekly Reports and systematically transformed into structured formats suitable for revision analysis, nowcasting, and forecasting research.

**Key Features:**
- **Coverage:** Monthly, quarterly, and annual GDP growth rates (1994–2025)
- **Vintages Tracked:** 1000+ data releases across 30+ years
- **Sectors:** 8 economic sectors (Primary, Manufacturing, Construction, Commerce, etc.)
- **Base-Year Adjustments:** Accounts for methodological changes (1990, 1994, 2007 base years)
- **Dual Formats:** Vintage format (columns = release dates) and Releases format (columns = revision sequences)

---

## Dataset Structure

This deposit contains **16 CSV files** organized into two categories:

### 1. Vintage Format Datasets (8 files)

Files in **`vintages/`** directory use the **vintage format** where:
- **Rows** = Reference periods (e.g., 2020m1 = January 2020)
- **Columns** = Release dates (e.g., 2020-01-17 = data published on January 17, 2020)
- **Values** = GDP growth rates as published on that release date

**Files:**
1. `monthly_gdp_vintages.csv` (2.9 MB) – Monthly GDP growth rates, all vintages
2. `quarterly_gdp_vintages.csv` (1.3 MB) – Quarterly and annual GDP, all vintages
3. `monthly_gdp_vintages_adjusted.csv` (2.9 MB) – Monthly GDP with base-year sentinel values
4. `quarterly_gdp_vintages_adjusted.csv` (1.3 MB) – Quarterly/annual with base-year adjustments
5. `monthly_gdp_vintages_benchmark.csv` (2.9 MB) – Monthly GDP benchmark (pre base-year changes only)
6. `quarterly_gdp_vintages_benchmark.csv` (1.3 MB) – Quarterly/annual benchmark
7. `monthly_gdp_vintages_adjusted_benchmark.csv` (2.9 MB) – Benchmark with base-year sentinel values
8. `quarterly_gdp_vintages_adjusted_benchmark.csv` (1.3 MB) – Benchmark quarterly/annual adjusted

### 2. Releases Format Datasets (8 files)

Files in **`releases/`** directory use the **releases format** where:
- **Rows** = Target periods (e.g., 2020m1 = January 2020)
- **Columns** = Revision sequences (e.g., `_1` = 1st release, `_2` = 2nd release, `_3` = 3rd+ release)
- **Values** = GDP growth rates for each revision

**Files:**
1. `monthly_gdp_releases.csv` (212 KB) – Monthly GDP by revision sequence
2. `quarterly_gdp_releases.csv` (186 KB) – Quarterly/annual by revision sequence
3. `monthly_gdp_releases_adjusted.csv` (219 KB) – Monthly with base-year adjustments
4. `quarterly_gdp_releases_adjusted.csv` (205 KB) – Quarterly/annual adjusted
5. `monthly_gdp_releases_benchmark.csv` (192 KB) – Benchmark monthly releases
6. `quarterly_gdp_releases_benchmark.csv` (171 KB) – Benchmark quarterly/annual
7. `monthly_gdp_releases_adjusted_benchmark.csv` (192 KB) – Benchmark monthly adjusted
8. `quarterly_gdp_releases_adjusted_benchmark.csv` (171 KB) – Benchmark quarterly/annual adjusted

---

## Data Dictionary

### Column Naming Conventions

#### Vintage Format:
- **Index:** `period` (e.g., `2020m1`, `2020q1`, `2020`)
- **Columns:** Release dates in `YYYY-MM-DD` format (e.g., `2020-01-17`)

#### Releases Format:
- **Index:** `target_period` (e.g., `2020m1`)
- **Columns:** Revision indicators:
  - `_1`: First release (flash estimate)
  - `_2`: Second release (first revision)
  - `_3`: Third or later release (subsequent revisions)

### Industry Codes

All datasets include 8 economic sectors:

| Code | English Name | Spanish Name |
|------|-------------|--------------|
| `primary_sector` | Primary Sector | Sector Primario |
| `manufacturing` | Manufacturing | Manufactura |
| `construction` | Construction | Construcción |
| `commerce` | Commerce | Comercio |
| `other_services` | Other Services | Otros Servicios |
| `gdp` | Total GDP | PBI Total |
| `non_primary` | Non-Primary Sector | Sector No Primario |
| `electricity_water` | Electricity & Water | Electricidad y Agua |

### Special Values

- **Base-Year Sentinel:** `-999999.0`
  - Indicates observations affected by base-year methodology changes
  - Present in `by_adjusted_*` files only
  - Periods: 1994m1 (base 1990→1994), 2000m7 (base 1994→2007), 2014m3 (base 2007→2019)

- **Missing Values:** `NaN` or empty cells
  - Data not yet published for that vintage
  - Normal in real-time datasets (future values unknown at past release dates)

---

## Data Sources

### Primary Source
**Banco Central de Reserva del Perú (BCRP) - Weekly Reports (Nota Semanal)**
- URL: https://www.bcrp.gob.pe/publicaciones/nota-semanal.html
- Historical Archive: https://www.bcrp.gob.pe/publicaciones/nota-semanal/nota-semanal-archivo.html
- Update Frequency: Weekly (every Friday)
- Coverage: 1994–2025

### Data Collection Method
Data were collected using an automated pipeline:
1. **Web Scraping:** Selenium-based scraper downloads PDF reports
2. **PDF Extraction:** Tabula-py extracts GDP tables from PDFs
3. **Data Cleaning:** 70+ cleaning functions standardize formats
4. **Vintage Construction:** Systematic aggregation by release date
5. **Quality Validation:** Automated checks for continuity and monotonicity

Full methodology documented in the accompanying research code repository.

---

## Use Cases

This dataset enables:

1. **Revision Analysis:** Study patterns in GDP revisions (noise vs news, bias, efficiency)
2. **Nowcasting:** Real-time forecasting using current vintage data
3. **Forecast Evaluation:** Assess forecast accuracy using historical vintages
4. **Policy Analysis:** Understand information available to policymakers at decision time
5. **Cross-Country Comparisons:** Compare Peru's revision patterns with other emerging economies
6. **Methodological Research:** Test real-time data methods in emerging market context

---

## Citation

If you use this dataset in your research, please cite:

### Data Citation (BibTeX)
```bibtex
@dataset{peru_gdp_rtd_2024,
  author       = {Cruz, Jason and Winkelried, Diego and Torres, Javier},
  title        = {Peru GDP Real-Time Dataset (1994-present)},
  year         = {2024},
  publisher    = {Zenodo},
  version      = {1.0.0},
  doi          = {10.5281/zenodo.18099975},
  url          = {https://doi.org/10.5281/zenodo.18099975}
}
```

### Author ORCIDs
- Jason Cruz: https://orcid.org/0009-0001-4640-5500
- Diego Winkelried: https://orcid.org/0000-0002-9388-2617
- Javier Torres: https://orcid.org/0000-0001-6850-1395

### Related Research Article
[Optional: Add reference to your forthcoming research paper]

---

## Reproducibility

This dataset is fully reproducible using the open-source code repository:
- **Repository:** https://github.com/JasonCruz18/peru_gdp_revisions
- **Code DOI:** [To be assigned via GitHub-Zenodo integration]
- **Requirements:** Python 3.9+, 2GB disk space
- **Installation:** `pip install -e .`
- **Execution:** `python scripts/run_full_pipeline.py`

**System Requirements:**
- Operating System: Windows, macOS, or Linux
- Python 3.9 or higher
- Java 8+ (for Tabula-py PDF extraction)
- Internet connection (for downloading source PDFs)

**Processing Time:** ~15 minutes for full pipeline (on standard laptop)

---

## Data Quality & Validation

**Quality Assurance Measures:**
- Timestamp-based incremental processing (prevents duplicates)
- Automated monotonicity checks (release dates sequential)
- Continuity validation (no gaps in time series)
- Format standardization (consistent sector names, date formats)
- Base-year change tracking (metadata-driven)

**Known Limitations:**
- Pre-2002 data may have gaps due to limited digital archive availability
- Some Weekly Reports missing from BCRP archive (minimal impact)
- Base-year changes create structural breaks (flagged with sentinel values)

---

## License

**Data License:** Creative Commons Attribution 4.0 International (CC-BY-4.0)

You are free to:
- **Share:** Copy and redistribute in any medium or format
- **Adapt:** Remix, transform, and build upon the material

Under the following terms:
- **Attribution:** You must give appropriate credit, provide a link to the license, and indicate if changes were made

**Code License:** MIT License (see code repository)

---

## Contact

For questions, issues, or collaboration inquiries:

**Corresponding Author:** Jason Cruz
- **Email:** jj.cruza@up.edu.pe
- **Institution:** Universidad del Pacífico - Centro de Investigación (CIUP)
- **ORCID:** https://orcid.org/0009-0001-4640-5500

**Co-Authors:**
- Diego Winkelried (ORCID: https://orcid.org/0000-0002-9388-2617)
- Javier Torres (ORCID: https://orcid.org/0000-0001-6850-1395)

**Issue Tracking:** https://github.com/JasonCruz18/peru_gdp_revisions/issues

---

## Version History

### Version 1.0.0 (January 2025)
- Initial public release
- Coverage: 1994–2025
- 16 datasets (8 vintage format + 8 releases format)
- 1000+ vintages tracked
- Comprehensive documentation
- Fully reproducible pipeline
- Published on Zenodo with DOI: 10.5281/zenodo.18099975

---

## Acknowledgments

Data sourced from the Banco Central de Reserva del Perú (BCRP). We thank the BCRP for maintaining the Weekly Reports archive and making economic data publicly accessible.

This project was developed at Universidad del Pacífico - Centro de Investigación (CIUP), Lima, Peru.

**Funding:** This work was funded by the Consejo Nacional de Ciencia, Tecnología e Innovación Tecnológica (CONCYTEC) and the Programa Nacional de Investigación Científica y Estudios Avanzados (PROCIENCIA) under the call "E041-2025-04 Proyectos de Investigación en Ciencias Sociales".

---

**Last Updated:** January 3, 2025
**Dataset Version:** 1.0.0
**README Version:** 1.0
