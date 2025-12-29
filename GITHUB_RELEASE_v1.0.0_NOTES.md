# GitHub Release v1.0.0 - Release Notes

**Title:** Peru GDP Real-Time Dataset v1.0.0

**Tag:** v1.0.0

**Release Date:** December 28, 2024

---

## Release Notes

This is the first stable release of the Peru GDP Real-Time Dataset construction pipeline, accompanying the Data in Brief submission.

### Features

**Complete Data Pipeline:**
- Automated web scraping of BCRP Weekly Reports (1994-present)
- PDF processing and text extraction
- Comprehensive data cleaning (70+ functions)
- Real-time dataset construction in two formats (vintages and releases)
- Interactive dashboard for data exploration

**Dataset Coverage:**
- **Time span:** 1994-present (30+ years)
- **Vintages tracked:** 1,000+ publication dates
- **Economic sectors:** 8 ISIC sectors + GDP aggregate
- **Frequencies:** Monthly, quarterly, annual
- **Base-year adjustments:** Automated handling of 1990, 1994, 2007 bases

**Output Formats:**
- 16 CSV files (vintages + releases formats)
- Parquet files for efficient processing
- Comprehensive metadata and documentation

### Data Availability

**Data Repository:** Zenodo
**Data DOI:** [TO BE ADDED AFTER ZENODO UPLOAD]
**Code DOI:** Will be automatically assigned via Zenodo-GitHub integration

All datasets are licensed under CC-BY-4.0 and freely available for research and analysis.

### Documentation

**Comprehensive Documentation Suite (120+ pages):**
- Complete data dictionary (43 pages)
- Zenodo upload guide (15 pages)
- GitHub release guide (14 pages)
- DIB submission checklist (18 pages)
- Data availability statement
- CHANGELOG with full development history

**Code Quality:**
- Full type annotations
- Comprehensive docstrings
- Modular architecture (6-stage pipeline)
- Extensive logging and error handling
- Production-ready code

### Reproducibility

This release provides **full reproducibility:**

1. **Clone repository:**
   ```bash
   git clone https://github.com/JasonCruz18/peru_gdp_revisions.git
   cd peru_gdp_revisions
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run complete pipeline:**
   ```bash
   python scripts/run_full_pipeline.py
   ```

**Note:** The pipeline downloads 1,000+ PDFs and processes them automatically. Full execution takes approximately 2-3 hours depending on internet connection.

### Citation

If you use this code or dataset, please cite:

```bibtex
@software{cruz2024peru_gdp_pipeline,
  author = {Cruz, Jason},
  title = {Peru GDP Real-Time Dataset Construction Pipeline},
  year = {2024},
  version = {1.0.0},
  publisher = {GitHub},
  url = {https://github.com/JasonCruz18/peru_gdp_revisions},
  doi = {[CODE_DOI]}
}

@dataset{cruz2024peru_gdp_data,
  author = {Cruz, Jason},
  title = {Peru GDP Real-Time Dataset (1994-present)},
  year = {2024},
  publisher = {Zenodo},
  doi = {[DATA_DOI]}
}
```

**Data Article (In Review):**
Cruz, J. (2025). Peru GDP Real-Time Dataset (1994-present). *Data in Brief*.

### System Requirements

- Python 3.9+
- 2GB RAM minimum
- 500MB disk space for code
- 2GB disk space for downloaded PDFs and processed data
- Internet connection for PDF downloads

### Dependencies

Key packages:
- pandas >= 2.0.0
- selenium >= 4.0.0
- PyMuPDF >= 1.23.0
- beautifulsoup4 >= 4.12.0
- streamlit >= 1.28.0 (for dashboard)

See `requirements.txt` for complete list.

### Project Structure

```
peru_gdp_revisions/
├── peru_gdp_rtd/           # Main package (30 modules)
│   ├── stage_1/            # PDF download
│   ├── stage_2/            # PDF shortening
│   ├── stage_3/            # Vintage construction
│   ├── stage_4/            # RTD concatenation
│   ├── stage_5/            # Metadata & base-year adjustment
│   └── stage_6/            # Releases format conversion
├── data/
│   ├── input/              # Downloaded PDFs
│   └── output/             # Processed datasets
│       ├── vintages/       # 8 CSV + 8 Parquet files
│       └── releases/       # 8 CSV + 8 Parquet files
├── scripts/                # Pipeline execution scripts
├── dashboard/              # Interactive Streamlit dashboard
├── tests/                  # Unit tests
└── docs/                   # Documentation

Total: 30 Python modules, 120+ pages documentation
```

### Known Issues

None. This is a stable release ready for production use.

### Future Development

Planned features for v2.0.0:
- Automated monthly updates
- Additional economic indicators
- Regional GDP disaggregation
- API for data access

### Support

For questions, issues, or contributions:
- **Issues:** https://github.com/JasonCruz18/peru_gdp_revisions/issues
- **Email:** jj.cruza@up.edu.pe
- **Institution:** Universidad del Pacífico - CIUP

### License

**Code:** MIT License
**Data:** CC-BY-4.0

### Acknowledgments

Data source: Banco Central de Reserva del Perú (BCRP)
Institution: Universidad del Pacífico - Centro de Investigación (CIUP)

---

## Files Included in This Release

All source code files are included automatically via GitHub release.

**Additional documentation files:**
- README.md
- CHANGELOG.md
- CITATION.cff
- LICENSE
- docs/DATA_DICTIONARY.md
- docs/DATA_AVAILABILITY.md
- ZENODO_UPLOAD_GUIDE.md
- GITHUB_RELEASE_GUIDE.md
- DIB_SUBMISSION_CHECKLIST.md

**NOT included in release (separate Zenodo deposit):**
- 16 CSV data files (17 MB total)
- Processed Parquet files
- Downloaded PDF files

These are available separately via Zenodo data repository (see Data DOI above).

---

## Changelog Summary

See CHANGELOG.md for complete development history.

**Major Milestones:**
- Dec 23, 2024: Timestamp-based incremental processing implemented
- Dec 22, 2024: Base-year adjustment system completed
- Dec 20, 2024: Releases format conversion added
- Nov 2024: Interactive dashboard implemented
- Oct 2024: Six-stage pipeline architecture finalized
- Earlier: Initial development and testing

**Total commits:** 50+
**Development period:** 3+ months
**Lines of code:** 5,000+

---

## Verification

To verify this release:

1. **Check code DOI:** [CODE_DOI] (assigned by Zenodo)
2. **Check data DOI:** [DATA_DOI] (from Zenodo deposit)
3. **Verify checksums:** See `checksums.txt` (if included)
4. **Run tests:** `pytest tests/` (if test suite available)

---

**Release Type:** Stable
**Status:** Production-ready
**Zenodo Integration:** Enabled
**DOI Assignment:** Automatic

---

## Instructions for Release Creation

**When creating this release on GitHub:**

1. Go to: https://github.com/JasonCruz18/peru_gdp_revisions/releases/new

2. Fill in:
   - **Tag:** v1.0.0
   - **Title:** Peru GDP Real-Time Dataset v1.0.0
   - **Description:** Copy the "Release Notes" section above

3. **Before publishing:**
   - Ensure Zenodo-GitHub integration is enabled
   - Verify all documentation files are in the repository
   - Check that CITATION.cff is up to date

4. **After publishing:**
   - Wait 10-30 minutes for Zenodo to assign Code DOI
   - Update this file with the assigned Code DOI
   - Update CITATION.cff with Code DOI
   - Update README.md with DOI badges
   - Update DIB_MANUSCRIPT_DRAFT.md with Code DOI

---

**Created:** December 28, 2024
**Purpose:** Prepared release notes for Data in Brief submission
**Next Step:** Follow GITHUB_RELEASE_GUIDE.md to create release
