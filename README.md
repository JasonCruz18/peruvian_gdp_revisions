# Peru GDP Real-Time Dataset

> Automated pipeline for building Peruvian GDP real-time datasets from BCRP Weekly Reports

[![Python](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.18099975.svg)](https://doi.org/10.5281/zenodo.18099975)

> **Published Dataset:** The complete Peru GDP Real-Time Dataset is openly available on Zenodo.
> This repository contains the **code pipeline** that builds and updates the dataset.
> To access the **ready-to-use data** (raw sources, intermediate tables, and final outputs), visit:
>
> **[Peru GDP Real-Time Dataset on Zenodo](https://doi.org/10.5281/zenodo.18099975)**

## Overview

This project builds Real-Time Datasets (RTD) of Peruvian GDP revisions from the Central Reserve Bank of Peru (BCRP) Weekly Reports. The pipeline downloads PDFs, shortens them to key tables, cleans and structures the data, and produces vintage and release datasets for analysis.

This repository is focused on dataset construction and reproducibility. It does not include a user dashboard.

Key features:
- Automated BCRP PDF download with record-based idempotency
- Shortened PDFs with key GDP tables only
- Table extraction and cleaning for old (CSV) and new (PDF) sources
- **OCR pipeline for pre-2013 scanned documents** (demonstrated on year 2001, see `OCR/README.md`)
- Vintage dataset construction and concatenation
- Base-year and benchmark revision handling
- Configuration-driven execution with a one-button CLI

---

## Quick Start

### Installation

Choose your preferred method (both are one-line simple):

#### Option A: Conda (Recommended - Includes Java)

```bash
# Clone the repository
git clone https://github.com/JasonCruz18/peru_gdp_revisions.git
cd peru_gdp_revisions

# Create environment with all dependencies
conda env create -f environment.yml

# Activate environment
conda activate peru_gdp_rtd
```

#### Option B: Pip + Virtual Environment

```bash
# Clone the repository
git clone https://github.com/JasonCruz18/peru_gdp_revisions.git
cd peru_gdp_revisions

# Create and activate virtual environment
python -m venv peru_gdp_rtd
source peru_gdp_rtd/bin/activate  # On Windows: peru_gdp_rtd\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

Note: Java (JRE) must be installed separately for PDF processing.

### Configuration

```bash
# Copy example configuration
cp config/config.example.yaml config/config.yaml
```

### Run Pipeline

```bash
# One-button update - runs complete pipeline
python scripts/update_rtd.py

# Run specific steps only
python scripts/update_rtd.py --steps 3,4,5,6

# Skip PDF download (useful for testing)
python scripts/update_rtd.py --skip-download

# Verbose output for debugging
python scripts/update_rtd.py --verbose
```

Outputs are written to `data/output/vintages/` and `data/output/releases/`. File extensions follow `features.persist_format` (csv or parquet).

---

## Project Structure

```
peru_gdp_revisions/
|-- peru_gdp_rtd/
|   |-- config/
|   |   |-- settings.py
|   |   `-- __init__.py
|   |-- scrapers/
|   |   `-- bcrp_scraper.py
|   |-- processors/
|   |   |-- pdf_processor.py
|   |   |-- file_organizer.py
|   |   `-- metadata.py
|   |-- cleaners/
|   |   `-- ...
|   |-- transformers/
|   |   |-- vintage_preparator.py
|   |   |-- concatenator.py
|   |   |-- metadata_handler.py
|   |   `-- releases_converter.py
|   |-- orchestration/
|   |   |-- runners.py
|   |   `-- validation.py
|   `-- utils/
|       |-- data_manager.py
|       `-- progress.py
|-- OCR/                       # Standalone OCR pipeline (year 2001 demonstration)
|   |-- ocr_config/
|   |   |-- config.yaml
|   |   `-- settings.py
|   |-- ocr_processors/
|   |   |-- image_preprocessor.py
|   |   |-- table_extractor.py
|   |   |-- ocr_engine.py
|   |   |-- csv_converter.py
|   |   `-- validator.py
|   |-- ocr_utils/
|   |   |-- logger.py
|   |   |-- progress_tracker.py
|   |   `-- file_manager.py
|   |-- output/                # OCR results for year 2001
|   |   `-- table_1/2001/
|   |-- raw/                   # gitignored; scanned PDFs
|   |   `-- 2001/
|   |-- README.md
|   |-- MANUAL_REVIEW_GUIDE.md
|   `-- requirements.txt
|-- config/
|   |-- config.yaml
|   `-- config.example.yaml
|-- scripts/
|   |-- update_rtd.py
|   |-- validate_rtd.py
|   `-- run_ocr_pipeline.py   # OCR pipeline runner
|-- data/                      # gitignored; shown for reference
|   |-- raw/
|   |   |-- new_weekly_reports/
|   |   |   |-- 2013/
|   |   |   |-- ...
|   |   |   |-- shortened_pdfs/
|   |   |   `-- _quarantine/
|   |   `-- old_weekly_reports/  # Manually-curated pre-2013 data
|   |       |-- table_1/
|   |       `-- table_2/
|   |-- input/
|   |   |-- table_1/
|   |   `-- table_2/
|   `-- output/
|       |-- vintages/
|       `-- releases/
|-- metadata/
|   `-- wr_metadata.csv
|-- record/                    # gitignored
|   |-- 1_downloaded_pdfs.txt
|   `-- 2_shortened_pdfs.txt
|-- docs/
|-- notebooks/
|-- tests/
|-- requirements.txt
|-- requirements-dev.txt
`-- README.md
```

---

## Pipeline Steps

The pipeline consists of 6 sequential steps:

### Step 1: Download PDFs
- Scrapes the BCRP Weekly Reports page
- Downloads new PDFs to `data/raw/new_weekly_reports/`
- Tracks downloads in `record/1_downloaded_pdfs.txt`
- Organizes PDFs into year folders

### Step 2: Shorten PDFs
- Extracts key pages with GDP tables
- Writes shortened PDFs to `data/raw/new_weekly_reports/shortened_pdfs/<year>/`
- Tracks processed files in `record/2_shortened_pdfs.txt`

### Step 3: Clean Tables and Build Vintages
- Extracts and cleans tables from old CSVs and shortened PDFs
- Creates vintage-format files in `data/input/table_1/` and `data/input/table_2/`

### Step 4: Concatenate RTDs
- Merges vintages across years
- Outputs RTDs to `data/output/vintages/`

### Step 5: Metadata and Benchmarks
- Updates `metadata/wr_metadata.csv`
- Applies base-year sentinel adjustments
- Generates benchmark datasets in `data/output/vintages/`

### Step 6: Convert to Releases
- Converts vintages to release-format datasets
- Outputs to `data/output/releases/`

---

## Output Datasets

All outputs are written to `data/output/` with extension based on `features.persist_format`.

### Vintage datasets (`data/output/vintages/`)
- `monthly_gdp_vintages.<ext>`
- `quarterly_gdp_vintages.<ext>`
- `monthly_gdp_vintages_adjusted.<ext>`
- `quarterly_gdp_vintages_adjusted.<ext>`
- `monthly_gdp_vintages_benchmark.<ext>`
- `quarterly_gdp_vintages_benchmark.<ext>`
- `monthly_gdp_vintages_adjusted_benchmark.<ext>`
- `quarterly_gdp_vintages_adjusted_benchmark.<ext>`

### Releases datasets (`data/output/releases/`)
- `monthly_gdp_releases.<ext>`
- `quarterly_gdp_releases.<ext>`
- `monthly_gdp_releases_adjusted.<ext>`
- `quarterly_gdp_releases_adjusted.<ext>`
- `monthly_gdp_releases_benchmark.<ext>`
- `quarterly_gdp_releases_benchmark.<ext>`
- `monthly_gdp_releases_adjusted_benchmark.<ext>`
- `quarterly_gdp_releases_adjusted_benchmark.<ext>`

---

## Usage Examples

### Command-Line Interface

```bash
# Run complete pipeline
python scripts/update_rtd.py

# Run steps 3-6 only
python scripts/update_rtd.py --steps 3,4,5,6

# Use custom configuration
python scripts/update_rtd.py --config path/to/custom_config.yaml

# Dry run (see what would be executed)
python scripts/update_rtd.py --dry-run
```

### Validate Outputs

```bash
python scripts/validate_rtd.py
```

### Jupyter Notebooks

Open `notebooks/new_gdp_rtd.ipynb` for a full walkthrough with explanations and examples.

---

## Configuration

Key settings in `config/config.yaml`:

```yaml
scraper:
  browser: "chrome"     # chrome, firefox, edge
  headless: false
  max_downloads: 60

features:
  persist_format: "parquet"   # csv or parquet
  validate_data: true

record_files:
  downloaded_pdfs: "1_downloaded_pdfs.txt"
  shortened_pdfs: "2_shortened_pdfs.txt"
```

See `config/config.example.yaml` for all options.

---

## Requirements

- Python 3.10 or higher
- Java Runtime Environment (JRE) for tabula-py
- Chrome, Firefox, or Edge for Selenium web scraping

---

## Data Sources

Main source: [BCRP Weekly Reports](https://www.bcrp.gob.pe/publicaciones/nota-semanal.html)

The pipeline processes two types of data:
- **NEW data** (2013+): Digital PDFs with editable tables — downloaded automatically by the pipeline.
- **OLD data** (pre-2013): Scanned PDFs converted to CSV and OCR-assisted processing. These raw historical inputs are not generated by the pipeline and must be obtained separately.

> **Important:** To run the full pipeline from scratch (including pre-2013 data), you need the raw CSV files for old weekly reports. These are available in the [Zenodo data repository](https://doi.org/10.5281/zenodo.18099975) under the `raw/` and `input/` directories. Download them and place them in the corresponding `data/raw/old_weekly_reports/` and `data/input/` folders before running the pipeline.

---

## Development

### Install Development Dependencies

```bash
pip install -r requirements-dev.txt
```

### Code Formatting

```bash
black peru_gdp_rtd/
isort peru_gdp_rtd/
flake8 peru_gdp_rtd/
```

### Running Tests

```bash
pytest tests/
```

---

## Documentation

- Installation Guide: [docs/INSTALLATION.md](docs/INSTALLATION.md)
- Usage Guide: [docs/USAGE.md](docs/USAGE.md)
- Architecture: [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)
- Data Availability: [docs/DATA_AVAILABILITY.md](docs/DATA_AVAILABILITY.md)
- FAQ: [FAQ.md](FAQ.md)

---

## Research Context

This project supports the data article:

**"Peru GDP Real-Time Dataset (1994-2025): Tracking Three Decades of Revisions"**
by Jason Cruz, Diego Winkelried, and Javier Torres — *Data in Brief* (submitted)

The datasets generated by this pipeline enable analysis of:
- GDP revision patterns in emerging markets
- Nowcasting accuracy using real-time data
- Information content of preliminary releases

---

## Contributing

Contributions are welcome. Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Format code with Black (`black .`)
4. Run tests (`pytest`)
5. Commit changes (`git commit -m 'Add amazing feature'`)
6. Push to branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

---

## Citation

### For the Research Paper & Dataset

If you use this dataset or research in your work, please cite:

```bibtex
@article{cruz2025gdp,
  title={Peru GDP Real-Time Dataset (1994-2025): Tracking Three Decades of Revisions},
  author={Cruz, Jason and Winkelried, Diego and Torres, Javier},
  journal={Data in Brief},
  year={2025},
  institution={Universidad del Pac\'ifico - CIUP}
}
```

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Acknowledgments

Data sourced from the Banco Central de Reserva del Perú (BCRP). We thank the BCRP for maintaining the Weekly Reports archive and making economic data publicly accessible.

This project was developed at Universidad del Pacífico - Centro de Investigación (CIUP), Lima, Peru.

**Funding:** This work was funded by the National Council for Science, Technology, and Technological Innovation (CONCYTEC) and the National Program for Scientific Research and Advanced Studies (PROCIENCIA) under the framework of the competition "E041-2025-04 Research Projects in Social Sciences," according to contract PE501096145-2025.

---

## Contact

Jason Cruz
Email: jj.cruza@up.edu.pe
GitHub: [@JasonCruz18](https://github.com/JasonCruz18)

---

## Support

For issues, questions, or contributions:
- GitHub Issues: https://github.com/JasonCruz18/peru_gdp_revisions/issues
- Email: jj.cruza@up.edu.pe
- Documentation: [FAQ.md](FAQ.md) and [docs/](docs/)
