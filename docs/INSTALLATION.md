# Installation Guide

Complete installation guide for the Peru GDP Real-Time Dataset construction pipeline.

## Table of Contents

1. [System Requirements](#system-requirements)
2. [Prerequisites](#prerequisites)
3. [Installation Methods](#installation-methods)
4. [Configuration](#configuration)
5. [Verification](#verification)
6. [Troubleshooting](#troubleshooting)

---

## System Requirements

### Operating Systems
- **Windows**: Windows 10 or later
- **macOS**: macOS 10.14 (Mojave) or later
- **Linux**: Ubuntu 18.04+, Debian 10+, or equivalent

### Hardware Requirements
- **RAM**: Minimum 4 GB (8 GB recommended)
- **Storage**: 2 GB free space for data and dependencies
- **Internet**: Required for downloading PDFs from BCRP

---

## Prerequisites

### 1. Python

**Version Required**: Python 3.10 or higher

#### Check Python Version
```bash
python --version
# or
python3 --version
```

#### Install Python

**Windows:**
- Download from [python.org](https://www.python.org/downloads/)
- During installation, check "Add Python to PATH"

**macOS:**
```bash
# Using Homebrew
brew install python@3.10
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install python3.10 python3.10-venv python3-pip
```

### 2. Java Runtime Environment (JRE)

Required for `tabula-py` PDF processing.

#### Check Java Installation
```bash
java -version
```

#### Install Java

**Windows:**
- Download from [java.com](https://www.java.com/download/)
- Or use [OpenJDK](https://adoptium.net/)

**macOS:**
```bash
brew install openjdk@11
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install default-jre
```

### 3. Web Browser

Required for Selenium web scraping.

**Supported browsers:**
- Google Chrome (recommended)
- Mozilla Firefox
- Microsoft Edge

The pipeline automatically manages browser drivers via `webdriver-manager`.

### 4. Git (Optional but Recommended)

For version control and cloning the repository.

**Check Git installation:**
```bash
git --version
```

**Install Git:**
- Windows: [git-scm.com](https://git-scm.com/download/win)
- macOS: `brew install git`
- Linux: `sudo apt install git`

---

## Installation Methods

### 🚀 Quick Install (One Command)

**The simplest way to get started:**

#### Option A: Conda (Recommended)

```bash
# Clone repository
git clone https://github.com/JasonCruz18/peru_gdp_revisions.git
cd peru_gdp_revisions

# Create environment with ALL dependencies
conda env create -f environment.yml

# Activate environment
conda activate peru_gdp_rtd

# You're ready! Skip to Configuration section below.
```

**✅ Advantages:**
- One command installs everything
- Includes Java (OpenJDK 11) - no separate installation needed
- Exact environment name: `peru_gdp_rtd`
- Tested on Windows, macOS, Linux

#### Option B: Pip + Virtual Environment

```bash
# Clone repository
git clone https://github.com/JasonCruz18/peru_gdp_revisions.git
cd peru_gdp_revisions

# Create virtual environment
python -m venv peru_gdp_rtd
source peru_gdp_rtd/bin/activate  # Windows: peru_gdp_rtd\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

**⚠️ Note:** Java (JRE) must be installed separately (see Prerequisites above).

---

### Method 1: Standard Installation (Detailed)

#### Step 1: Clone the Repository

```bash
git clone https://github.com/JasonCruz18/peru_gdp_revisions.git
cd peru_gdp_revisions
```

Or download as ZIP and extract.

#### Step 2: Create Virtual Environment (Recommended)

**Using venv:**
```bash
# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (macOS/Linux)
source venv/bin/activate
```

**Using conda:**
```bash
# Create conda environment
conda create -n gdp_revisions python=3.10

# Activate
conda activate gdp_revisions
```

#### Step 3: Install Dependencies

```bash
# Install required packages
pip install -r requirements.txt

# Optional: Install development dependencies
pip install -r requirements-dev.txt
```

#### Step 4: Configure the Pipeline

```bash
# Copy example configuration
cp config/config.example.yaml config/config.yaml

# Edit if needed (optional - defaults work out of the box)
nano config/config.yaml  # or use any text editor
```

### Method 2: Conda Installation (Alternative Details)

**(See Quick Install above for the simplest approach)**

For users who want more control over the conda environment:

#### Manual Conda Environment Creation

```bash
# Clone repository
git clone https://github.com/JasonCruz18/peru_gdp_revisions.git
cd peru_gdp_revisions

# Create environment with Python 3.10
conda create -n peru_gdp_rtd python=3.10

# Activate environment
conda activate peru_gdp_rtd

# Install dependencies via conda and pip
conda install -c conda-forge pandas numpy pyyaml requests selenium openjdk pymupdf
pip install -r requirements.txt
```

#### Verify Conda Installation

```bash
# Activate environment
conda activate peru_gdp_rtd

# Test the installation
pytest tests/test_smoke.py -v

# Check pipeline help
python scripts/update_rtd.py --help
```

**💡 Tip:** The `environment.yml` file includes Java (OpenJDK 11) automatically, so you don't need to install it separately when using `conda env create -f environment.yml`.

### Method 3: Exact Version Reproducibility

For exact reproducibility with pinned versions:

```bash
# Clone repository
git clone https://github.com/JasonCruz18/peru_gdp_revisions.git
cd peru_gdp_revisions

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install with exact pinned versions
pip install -r requirements-frozen.txt

# Configure
cp config/config.example.yaml config/config.yaml
```

This ensures the exact same package versions used during development.

### Method 4: Development Installation

For contributors who want to modify the code:

```bash
# Clone repository
git clone https://github.com/JasonCruz18/peru_gdp_revisions.git
cd peru_gdp_revisions

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in editable mode with dev dependencies
pip install -e .
pip install -r requirements-dev.txt

# Set up configuration
cp config/config.example.yaml config/config.yaml
```

### Method 3: Docker Installation (Future)

*Coming soon - containerized deployment*

---

## Configuration

### Configuration File

The main configuration is in `config/config.yaml`. Key settings:

```yaml
# Project metadata
project:
  name: "Peru GDP RTD"
  version: "1.0.0"

# Web scraping settings
scraper:
  browser: "chrome"           # Options: chrome, firefox, edge
  headless: false             # Run browser in background
  download_timeout: 30        # Timeout per PDF download (seconds)
  max_downloads: 60           # Maximum PDFs to download
  rate_limit_min: 1.0         # Minimum delay between requests (seconds)
  rate_limit_max: 3.0         # Maximum delay between requests (seconds)

# Data cleaning settings
cleaning:
  decimal_places: 1           # Decimal precision for growth rates
  pipeline_version: "s3.0.0"  # Pipeline version identifier

# Feature flags
features:
  enable_alerts: true         # Play audio alerts
  persist_format: "csv"       # Output format: csv or parquet
```

### Directory Structure

The pipeline will create these directories automatically:

```
peru_gdp_revisions/
├── data/                   # Generated datasets (gitignored)
│   ├── input/              # Intermediate processing data
│   ├── output/             # Final RTD datasets
│   └── records/            # Processing records
├── new_weekly_reports/     # Downloaded PDF files (gitignored)
├── old_weekly_reports/     # Historical CSV files (gitignored)
└── record/                 # Legacy progress tracking (gitignored)
```

### Environment Variables (Optional)

Set these if you need custom paths:

```bash
# Linux/macOS
export PERU_GDP_CONFIG="/path/to/custom/config.yaml"
export PERU_GDP_DATA="/path/to/data/directory"

# Windows
set PERU_GDP_CONFIG=C:\path\to\custom\config.yaml
set PERU_GDP_DATA=C:\path\to\data\directory
```

---

## Verification

### Step 1: Verify Installation

```bash
# Check package version
python -c "import peru_gdp_rtd; print(peru_gdp_rtd.__version__)"
# Expected output: 1.0.0

# Check all modules load correctly
python -c "from peru_gdp_rtd.config import get_settings; print('OK')"
```

### Step 2: Run Smoke Tests

```bash
# Run test suite
python tests/test_smoke.py

# Expected output:
# [PASS] Package import
# [PASS] Config loading
# [PASS] Config paths
# [PASS] Sector mappings
# [PASS] Month mappings
# [PASS] Base years
# [PASS] All modules importable
#
# Results: 7 passed, 0 failed
# [OK] All smoke tests passed!
```

### Step 3: Test Pipeline (Dry Run)

```bash
# Test pipeline without making changes
python scripts/update_rtd.py --dry-run

# Expected output:
# Loading configuration from: config/config.yaml
# Project: Peru GDP RTD v1.0.0
# Running all pipeline steps (1-6)
# DRY RUN MODE - No changes will be made
# Would run steps: [1, 2, 3, 4, 5, 6]
```

### Step 4: Run Complete Pipeline (Optional)

**Warning**: This will download ~60 PDF files from BCRP (may take 15-30 minutes).

```bash
# Run complete pipeline
python scripts/update_rtd.py --verbose

# Or skip download for faster testing
python scripts/update_rtd.py --skip-download --verbose
```

---

## Troubleshooting

### Common Issues

#### Issue 1: `FileNotFoundError: config/config.yaml not found`

**Solution:**
```bash
cp config/config.example.yaml config/config.yaml
```

#### Issue 2: `ModuleNotFoundError: No module named 'peru_gdp_rtd'`

**Cause**: Package not installed or virtual environment not activated.

**Solution:**
```bash
# Activate virtual environment
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows

# Reinstall package
pip install -e .
```

#### Issue 3: `tabula.errors.JavaNotFoundError`

**Cause**: Java Runtime Environment not installed.

**Solution:**
```bash
# Check Java installation
java -version

# If not installed, install JRE (see Prerequisites section)
```

#### Issue 4: Selenium WebDriver Errors

**Example**: `selenium.common.exceptions.WebDriverException`

**Solution:**
```bash
# Update webdriver-manager
pip install --upgrade webdriver-manager

# Or specify a different browser in config.yaml
scraper:
  browser: "firefox"  # Try firefox instead of chrome
```

#### Issue 5: Permission Errors on Windows

**Example**: `PermissionError: [WinError 5] Access is denied`

**Solution:**
- Run terminal as Administrator
- Or install to a directory where you have write permissions

#### Issue 6: SSL Certificate Errors

**Example**: `ssl.SSLError` or `CERTIFICATE_VERIFY_FAILED`

**Solution:**
```bash
# Update certifi package
pip install --upgrade certifi

# Or temporarily disable SSL verification (not recommended)
# Set environment variable:
# export SSL_CERT_FILE=/path/to/cert.pem  # Linux/macOS
# set SSL_CERT_FILE=C:\path\to\cert.pem   # Windows
```

#### Issue 7: Out of Memory Errors

**Cause**: Processing large PDF files with limited RAM.

**Solution:**
- Close other applications
- Process fewer files at once by adjusting `max_downloads` in config.yaml
- Increase system RAM if possible

### Getting Help

If you encounter issues not listed here:

1. **Check the logs**: Run with `--verbose` flag for detailed output
2. **Search existing issues**: [GitHub Issues](https://github.com/JasonCruz18/peru_gdp_revisions/issues)
3. **Open a new issue**: Include:
   - Operating system and version
   - Python version (`python --version`)
   - Java version (`java -version`)
   - Full error message and stack trace
   - Steps to reproduce

---

## Next Steps

After successful installation:

1. **Explore the notebooks**: `notebooks/new_gdp_rtd.ipynb` for interactive walkthrough
2. **Read the usage guide**: [docs/USAGE.md](USAGE.md)
3. **Review the architecture**: [docs/ARCHITECTURE.md](ARCHITECTURE.md)
4. **Run the pipeline**: `python scripts/update_rtd.py`

---

## Uninstallation

To remove the package and clean up:

```bash
# Deactivate virtual environment
deactivate

# Remove virtual environment directory
rm -rf venv  # Linux/macOS
rmdir /s venv  # Windows

# Remove generated data (optional)
rm -rf data/ new_weekly_reports/ old_weekly_reports/ record/

# Remove the repository
cd ..
rm -rf peru_gdp_revisions
```

---

## Additional Resources

- **Main README**: [README.md](../README.md)
- **Usage Guide**: [docs/USAGE.md](USAGE.md)
- **Architecture**: [docs/ARCHITECTURE.md](ARCHITECTURE.md)
- **Contributing**: [docs/CONTRIBUTING.md](CONTRIBUTING.md)
- **GitHub Repository**: https://github.com/JasonCruz18/peru_gdp_revisions
- **BCRP Weekly Reports**: https://www.bcrp.gob.pe/publicaciones/nota-semanal.html
