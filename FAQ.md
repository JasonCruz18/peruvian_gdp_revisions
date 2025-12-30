# Frequently Asked Questions (FAQ)

Common questions and answers about the Peru GDP Real-Time Dataset project.

---

## Table of Contents

1. [General Questions](#general-questions)
2. [Installation](#installation)
3. [Usage](#usage)
4. [Dashboard](#dashboard)
5. [Data Quality](#data-quality)
6. [Troubleshooting](#troubleshooting)
7. [Contributing](#contributing)

---

## General Questions

### What is this project?

The Peru GDP Real-Time Dataset (RTD) is a production-ready pipeline that automatically constructs real-time datasets of Peruvian GDP revisions from the Central Reserve Bank of Peru (BCRP) Weekly Reports.

### Who should use this project?

- **Researchers** studying GDP revisions, nowcasting, or real-time macroeconomic data
- **Economists** analyzing Peruvian economic statistics
- **Policy makers** needing historical GDP data with revision tracking
- **Students** learning about data pipeline construction and economic statistics

### Is this an official BCRP project?

No. This is an independent academic research project that uses publicly available data from the BCRP.

### Can I use this for my research?

Yes! The project is licensed under MIT License, which allows free use with attribution. Please cite using the information in [CITATION.cff](CITATION.cff).

### What data does this project generate?

- Monthly GDP growth rates (Real-Time Dataset format)
- Quarterly/Annual GDP growth rates
- Releases format datasets (1st, 2nd, 3rd releases)
- Benchmark datasets (pre base-year changes)
- Base-year adjusted datasets

---

## Installation

### What are the system requirements?

- **Python**: 3.10 or higher
- **Java**: JRE (for PDF processing with tabula-py)
- **Browser**: Chrome, Firefox, or Edge (for web scraping)
- **Storage**: ~2 GB for data and dependencies
- **RAM**: Minimum 4 GB (8 GB recommended)

### How long does installation take?

- First-time installation: 5-10 minutes
- Dependency installation: 2-3 minutes
- Configuration: < 1 minute

### Do I need to install Java?

Yes. The pipeline uses `tabula-py` for PDF table extraction, which requires Java Runtime Environment (JRE).

### Can I run this without downloading PDFs?

Yes! Use `--skip-download` flag:
```bash
python scripts/update_rtd.py --skip-download
```

This is useful if you already have the PDFs or want to test the cleaning/transformation steps.

### Does this work on Windows/Mac/Linux?

Yes! The pipeline is cross-platform and tested on:
- Ubuntu 18.04+
- Windows 10+
- macOS 10.14+

---

## Usage

### How do I run the complete pipeline?

```bash
python scripts/update_rtd.py
```

This runs all 6 steps and generates the complete RTD.

### How long does the pipeline take?

- **Complete pipeline** (first run): 30-45 minutes
- **Download only** (Step 1): 15-30 minutes
- **Processing** (Steps 2-6): 10-15 minutes
- **Updates** (incremental): 5-10 minutes

### Can I run specific steps only?

Yes:
```bash
# Run steps 3-6 only
python scripts/update_rtd.py --steps 3,4,5,6

# Run step 3 only
python scripts/update_rtd.py --steps 3
```

### How do I update the dataset with new data?

Just run the pipeline again:
```bash
python scripts/update_rtd.py
```

The pipeline is idempotent - it will:
- Download only new PDFs
- Skip already processed files
- Update existing datasets

### Where are the output files?

All datasets are saved in `data/output/`:
```
data/output/
├── monthly_gdp_vintages.csv
├── quarterly_gdp_vintages.csv
├── monthly_gdp_releases.csv
├── quarterly_gdp_releases.csv
└── [8+ more dataset variants]
```

### Can I use the code as a Python package?

Yes! Install in development mode:
```bash
pip install -e .
```

Then import:
```python
from peru_gdp_rtd.config import get_settings
from peru_gdp_rtd.scrapers import pdf_downloader
# ... etc
```

---

## Dashboard

### How do I run the dashboard?

```bash
# Install dashboard dependencies
pip install -r dashboard/requirements.txt

# Run dashboard
streamlit run dashboard/app.py
```

The dashboard will open in your browser at `http://localhost:8501`.

### Can I customize the dashboard colors?

Yes! Edit `dashboard/config.py` and change the `THEME_PRESET`:
```python
THEME_PRESET = "academic"  # or "ocean", "forest", "sunset", "custom"
```

Or define custom colors in the `"custom"` theme section.

### How do I add my project logo?

1. Save your logo as PNG: `dashboard/assets/logo.png`
2. Set in `dashboard/config.py`:
```python
USE_LOGO = True
LOGO_WIDTH = 200  # Adjust width as needed
```

### Can I deploy the dashboard online?

Yes! Options:
1. **Streamlit Cloud** (easiest, free)
2. **Heroku**
3. **AWS/GCP/Azure**
4. **Your own server**

See `dashboard/README.md` for deployment guides.

### The dashboard shows "No datasets found"

Run the pipeline first to generate datasets:
```bash
python scripts/update_rtd.py
```

---

## Data Quality

### How accurate is the data?

The data comes directly from BCRP official publications. The pipeline applies:
- 70+ cleaning functions
- Automated validation checks
- Manual quality review

Accuracy depends on:
1. BCRP data quality (source)
2. PDF extraction accuracy (tabula-py)
3. Cleaning logic (extensively tested)

### How do I validate the data quality?

Run the validation script:
```bash
python scripts/validate_rtd.py --verbose
```

This checks for:
- Missing values
- Value ranges
- Duplicates
- Continuity
- Format issues

### What if I find errors in the data?

1. Check if it's a source error (BCRP PDF)
2. Check if it's a processing error (cleaning logic)
3. Open an issue on GitHub with details
4. Submit a pull request with fixes

### How often is the data updated?

The BCRP publishes Weekly Reports every week. To get the latest data:
```bash
python scripts/update_rtd.py
```

We recommend updating monthly or quarterly depending on your needs.

---

## Troubleshooting

### "FileNotFoundError: config/config.yaml not found"

**Solution**:
```bash
cp config/config.example.yaml config/config.yaml
```

### "tabula.errors.JavaNotFoundError"

**Solution**: Install Java Runtime Environment (JRE).

- **Windows**: Download from [java.com](https://www.java.com)
- **macOS**: `brew install openjdk`
- **Linux**: `sudo apt install default-jre`

### "Selenium WebDriverException"

**Solution**:
```bash
pip install --upgrade webdriver-manager
```

Or try a different browser in `config/config.yaml`:
```yaml
scraper:
  browser: "firefox"  # instead of "chrome"
```

### "ModuleNotFoundError: No module named 'peru_gdp_rtd'"

**Solution**:
```bash
# Activate virtual environment
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows

# Install package
pip install -e .
```

### The pipeline is very slow

**Possible causes**:
1. **Slow internet**: PDF downloads take time
2. **Many PDFs**: First run processes ~60 files
3. **Limited RAM**: Close other applications

**Solutions**:
- Use `--skip-download` to skip PDF download
- Process fewer files: adjust `max_downloads` in config
- Run overnight for first-time setup

### Tests are failing

**Solution**:
```bash
# Check Python version
python --version  # Should be 3.10+

# Reinstall dependencies
pip install -r requirements.txt

# Run tests
python tests/test_smoke.py
```

### The dashboard won't start

**Solution**:
```bash
# Install dashboard dependencies
pip install streamlit plotly pandas

# Or
pip install -r dashboard/requirements.txt

# Run dashboard
streamlit run dashboard/app.py
```

---

## Contributing

### How can I contribute?

1. **Report bugs**: Open GitHub issues
2. **Suggest features**: Open feature request issues
3. **Improve documentation**: Submit PRs for typos/clarifications
4. **Add features**: Fork, develop, and submit PRs
5. **Share feedback**: Email or GitHub discussions

See [CONTRIBUTING.md](docs/CONTRIBUTING.md) for detailed guidelines.

### What should I know before contributing?

- **Python 3.10+**
- **Code formatting**: Black (line length 100)
- **Type hints**: Required for all functions
- **Documentation**: Google-style docstrings
- **Testing**: Add tests for new features

### How do I set up a development environment?

```bash
# Clone repository
git clone https://github.com/JasonCruz18/peru_gdp_revisions.git
cd peru_gdp_revisions

# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Install in editable mode
pip install -e .

# Run tests
python tests/test_smoke.py
```

### Can I add new cleaning functions?

Yes! Add them to appropriate cleaner module:
```python
# peru_gdp_rtd/cleaners/custom_cleaners.py
def my_cleaning_function(df):
    """Your cleaning logic."""
    return df
```

Then import in `__init__.py` and use in cleaner classes.

### How do I report a bug?

1. Check if it's already reported in [GitHub Issues](https://github.com/JasonCruz18/peru_gdp_revisions/issues)
2. If not, open a new issue with:
   - Clear title
   - Steps to reproduce
   - Expected vs actual behavior
   - Environment details (OS, Python version, etc.)
   - Error messages and stack traces

---

## Additional Resources

- **Main README**: [README.md](README.md)
- **Installation Guide**: [docs/INSTALLATION.md](docs/INSTALLATION.md)
- **Usage Guide**: [docs/USAGE.md](docs/USAGE.md)
- **Architecture**: [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)
- **Contributing**: [docs/CONTRIBUTING.md](docs/CONTRIBUTING.md)
- **GitHub**: https://github.com/JasonCruz18/peru_gdp_revisions

---

## Contact

**Questions not answered here?**

- **Email**: jj.cruza@up.edu.pe
- **GitHub Issues**: https://github.com/JasonCruz18/peru_gdp_revisions/issues
- **GitHub Discussions**: https://github.com/JasonCruz18/peru_gdp_revisions/discussions

---

*Last updated: December 15, 2025*
