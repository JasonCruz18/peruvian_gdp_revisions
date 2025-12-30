# Peru GDP Real-Time Dataset

> Automated pipeline for building Peruvian GDP real-time datasets from BCRP Weekly Reports

[![Python](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Overview

This project builds Real-Time Datasets (RTD) of Peruvian GDP revisions from the Central Reserve Bank of Peru (BCRP) Weekly Reports. The pipeline downloads PDFs, shortens them to key tables, cleans and structures the data, and produces vintage and release datasets for analysis.

Key features:
- Automated BCRP PDF download with record-based idempotency
- Shortened PDFs with key GDP tables only
- Table extraction and cleaning for old (CSV) and new (PDF) sources
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
|       |-- alerts.py
|       `-- progress.py
|-- config/
|   |-- config.yaml
|   `-- config.example.yaml
|-- scripts/
|   |-- update_rtd.py
|   `-- validate_rtd.py
|-- data/                      # gitignored; shown for reference
|   |-- raw/
|   |   |-- new_weekly_reports/
|   |   |   |-- 2013/
|   |   |   |-- ...
|   |   |   |-- shortened_pdfs/
|   |   |   `-- _quarantine/
|   |   `-- old_weekly_reports/
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
- `monthly_gdp_rtd.<ext>`
- `quarterly_annual_gdp_rtd.<ext>`
- `by_adjusted_monthly_gdp_rtd.<ext>`
- `by_adjusted_quarterly_annual_gdp_rtd.<ext>`
- `monthly_gdp_benchmark.<ext>`
- `quarterly_annual_gdp_benchmark.<ext>`
- `by_adjusted_monthly_gdp_benchmark.<ext>`
- `by_adjusted_quarterly_annual_gdp_benchmark.<ext>`

### Releases datasets (`data/output/releases/`)
- `monthly_gdp_releases.<ext>`
- `quarterly_annual_gdp_releases.<ext>`
- `by_adjusted_monthly_gdp_releases.<ext>`
- `by_adjusted_quarterly_annual_gdp_releases.<ext>`
- `monthly_gdp_benchmark_releases.<ext>`
- `quarterly_annual_gdp_benchmark_releases.<ext>`
- `by_adjusted_monthly_gdp_benchmark_releases.<ext>`
- `by_adjusted_quarterly_annual_gdp_benchmark_releases.<ext>`

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
  enable_alerts: false
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
- New data (2013+): digital PDFs with editable tables
- Old data (pre-2013): scanned PDFs converted to CSV

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

This project supports the research paper:

"Rationality and Nowcasting on Peruvian GDP Revisions"
by Jason Cruz, Diego Winkelried, and Javier Torres (Universidad del Pacifico - CIUP)

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
@article{cruz_etal_2025,
  title={Rationality and Nowcasting on Peruvian GDP Revisions},
  author={Cruz, Jason and Winkelried, Diego and Torres, Javier},
  year={2025},
  journal={Data in Brief},
  institution={Universidad del Pacifico - CIUP}
}
```

### For the Code/Software

If you use this code repository or pipeline, please cite:

```bibtex
@software{cruz2024pipeline,
  title={Peru GDP Real-Time Dataset Construction Pipeline},
  author={Cruz, Jason},
  year={2024},
  url={https://github.com/JasonCruz18/peru_gdp_revisions},
  institution={Universidad del Pacifico - CIUP}
}
```

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Acknowledgments

- Central Reserve Bank of Peru (BCRP) for public access to Weekly Reports
- Universidad del Pacifico - CIUP for research support

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
