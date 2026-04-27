# Changelog

All notable changes to the Peru GDP Real-Time Dataset Construction Pipeline will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-12-17

### 🎉 Initial Release

First stable release of the Peru GDP Real-Time Dataset Construction Pipeline. This release includes a complete, production-ready pipeline for constructing real-time datasets of Peruvian GDP revisions from BCRP Weekly Reports.

### Added

#### Core Pipeline Features
- **Automated Web Scraping**: Selenium-based scraper for BCRP Weekly Reports (1992-present)
- **PDF Processing**: Keyword-based extraction with support for both scanned (pre-2013) and digital PDFs
- **Comprehensive Data Cleaning**: 70+ specialized transformation functions organized in 7 modules
- **Real-Time Dataset Construction**: Vintage tracking with multiple output formats
- **Metadata Management**: Automatic extraction of base-year changes and revision metadata
- **One-Button Update Script**: `scripts/update_rtd.py` for effortless dataset updates

#### Data Outputs
- **Vintage Format**: Monthly, quarterly, and annual GDP growth rates
- **Releases Format**: 1st, 2nd, 3rd release tracking for revision analysis
- **Benchmark Datasets**: Base-year consistent datasets with sentinel values
- **Base-Year Adjusted**: Datasets adjusted for structural breaks (1990, 1994, 2007, 2019)

#### Documentation
- **Comprehensive Guides**: Installation, usage, architecture, and contributing docs
- **Tutorial Notebooks**: 6 step-by-step Jupyter notebooks covering all pipeline stages
- **Data Availability Statement**: Journal-ready AEA-compliant statement
- **FAQ**: Common questions and troubleshooting

#### Development Infrastructure
- **Configuration Management**: Type-safe YAML-based configuration with 231-line config file
- **Testing**: Comprehensive test suite with CI/CD via GitHub Actions
- **Cross-Platform Support**: Tested on Ubuntu, Windows, macOS
- **Python Support**: Compatible with Python 3.10, 3.11, 3.12

#### Interactive Features
- **Progress Tracking**: tqdm-based progress bars for all processing steps

### Security

#### Fixed Vulnerabilities (2025-12-17)
- **urllib3**: Upgraded 2.5.0 → 2.6.2 (High severity - Cookie injection)
- **notebook**: Upgraded 7.0.6 → 7.5.1 (High severity - XSS vulnerability)
- **requests**: Upgraded 2.31.0 → 2.32.5 (Moderate severity)
- **selenium**: Upgraded 4.35.0 → 4.39.0 (Moderate severity)
- **PyMuPDF**: Upgraded 1.23.26 → 1.26.7 (Moderate severity)
- **ipywidgets**: Upgraded 8.1.3 → 8.1.8 (Moderate severity)
- **PyPDF2 → pypdf**: Migrated 3.0.1 → 6.4.2 (Fixed infinite loop vulnerability)

### Repository Structure

#### Reorganization (2025-12-17)
- **Consolidated Raw Data**: Created `data/raw/` for all raw data files
  - `new_weekly_reports/` → `data/raw/new_weekly_reports/`
  - `old_weekly_reports/` → `data/raw/old_weekly_reports/`
- **Clearer Naming**: Renamed `input/` → `shortened_pdfs/` for trimmed PDFs
- **OCR Support**: Added `OCR/` folder for scanned PDF proof-of-concept
- **Improved Organization**: Professional structure suitable for journal submission

#### File Structure
```
peru_gdp_revisions/
├── peru_gdp_rtd/          # Main Python package (7 modules, 2,435 lines)
├── scripts/               # Execution scripts
├── notebooks/             # 8 tutorial notebooks
├── docs/                  # Comprehensive documentation
├── data/
│   ├── input/            # Intermediate processing data
│   ├── output/           # Final RTD datasets (16 CSV files)
│   └── raw/              # Raw data files
│       ├── new_weekly_reports/  # BCRP PDFs (2013-present)
│       └── old_weekly_reports/  # Pre-2013 scanned data
├── metadata/             # Revision metadata (wr_metadata.csv)
├── OCR/                  # OCR proof-of-concept
├── tests/                # Test suite
└── .github/workflows/    # CI/CD pipelines
```

### Dependencies

#### Core Dependencies
- **Data Processing**: pandas 2.1.4, numpy 1.26.3
- **Configuration**: pyyaml 6.0.3
- **Web Scraping**: selenium 4.39.0, webdriver-manager 4.0.2, requests 2.32.5, urllib3 2.6.2
- **PDF Processing**: PyMuPDF 1.26.7, pypdf 6.4.2, tabula-py 2.9.0
- **Utilities**: roman 4.1, tqdm 4.66.5, colorama 0.4.6

#### Development Dependencies
- **Notebooks**: jupyter 1.0.0, notebook 7.5.1, ipywidgets 8.1.8
- **Code Quality**: black 23.0.0, flake8 6.0.0, isort 5.12.0
- **Testing**: pytest 7.4.0, pytest-cov 4.1.0

#### System Requirements
- **Python**: 3.10, 3.11, or 3.12
- **Java**: JRE (for tabula-py PDF processing)
- **Browser**: Chrome, Firefox, or Edge (for Selenium)

### Performance

- **Processing Speed**: ~30-45 minutes for complete pipeline (first run)
- **Incremental Updates**: <5 minutes for weekly updates
- **Memory Usage**: ~500 MB peak during RTD concatenation
- **Storage**: ~2 GB including dependencies

### Known Limitations

1. **Historical Data (pre-2013)**: Scanned PDFs may have OCR errors requiring manual verification
2. **Base-Year Changes**: Peru changed base years multiple times (1990, 1994, 2007, 2019), causing structural breaks
3. **Missing Observations**: Some periods may be missing if not published in Weekly Reports
4. **Revision Timing**: Exact timing of some revisions may be approximate
5. **BCRP Website Changes**: Scraper may require updates if BCRP restructures their website

### License

- **Code**: MIT License
- **Data**: Derived from publicly available BCRP publications

### Citation

```bibtex
@software{cruz2025gdp_pipeline,
  author = {Cruz, Jason},
  title = {Peru GDP Real-Time Dataset Construction Pipeline},
  year = {2025},
  version = {1.0.0},
  url = {https://github.com/JasonCruz18/peru_gdp_revisions}
}
```

### Acknowledgments

- **BCRP** for publishing Weekly Reports with GDP statistics
- **Universidad del Pacífico - CIUP** for research support
- **Open source community** for tools and libraries

---

## [Unreleased]

### Changed
- Repository cleanup to keep the public codebase focused on reproducible dataset construction
- Removed bundled dashboard code and internal publication/support artifacts from the main repository
- Removed the unused audio-alert feature and its `pygame` dependency

### Planned Features
- Docker containerization for simplified deployment
- PostgreSQL database backend option
- Automated data quality reporting
- Extended coverage to other Latin American countries
- API endpoint for programmatic data access
- OCR pipeline for complete pre-2013 data processing

---

**Contributors**: Jason Cruz (Universidad del Pacífico - CIUP)

**Repository**: https://github.com/JasonCruz18/peru_gdp_revisions

**Last Updated**: December 17, 2025
