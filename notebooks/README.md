# Notebooks - Educational Materials

This folder contains Jupyter notebooks that provide user-friendly guides and tutorials for the Peru GDP Real-Time Dataset construction pipeline.

## Available Notebooks

### `new_gdp_rtd.ipynb`
**Main User Guide - Complete Pipeline Walkthrough** ⭐ **UPDATED TO MODULAR STRUCTURE**

This is the primary educational notebook for users who want to understand and run the GDP Real-Time Dataset construction pipeline interactively.

**Recent Update (December 2024):**
- **Refactored to use modular imports** from `peru_gdp_rtd` package
- Now demonstrates the professional modular architecture with organized imports
- All functions imported from specialized modules (scrapers, processors, cleaners, transformers, utils)
- Cleaner, more maintainable code structure

**Features:**
- Step-by-step execution of the complete pipeline
- Detailed explanations of each processing stage
- Visual progress indicators and optional audio alerts
- Interactive cells for exploring intermediate results
- Comprehensive documentation of data transformations
- **Uses production-quality modular code** (same as `scripts/update_rtd.py`)

**Module Organization:**
```python
peru_gdp_rtd.config         # Configuration management
peru_gdp_rtd.scrapers       # Web scraping and PDF downloading
peru_gdp_rtd.processors     # PDF processing and table extraction
peru_gdp_rtd.cleaners       # Data cleaning and normalization
peru_gdp_rtd.transformers   # RTD construction and transformations
peru_gdp_rtd.utils          # Utilities (alerts, data management)
```

**Recommended for:**
- First-time users learning the pipeline
- Researchers who want to understand the methodology
- Users who prefer interactive exploration over script execution
- Educational purposes and demonstrations
- Learning the modular architecture of the codebase

**Usage:**
```bash
# From repository root
jupyter notebook notebooks/new_gdp_rtd.ipynb

# Or open directly from Jupyter Lab
cd notebooks && jupyter lab
```

### `old_gdp_rtd.ipynb`
**Legacy Notebook - Old GDP Data Processing**

Historical notebook focused on processing the older vintage of GDP data (pre-2007 base year changes).

**Purpose:**
- Documents the processing approach for historical GDP tables
- Useful for understanding data structure evolution
- Reference for handling legacy data formats

**Recommended for:**
- Understanding historical data processing decisions
- Reference when working with old vintage data
- Comparative analysis of old vs. new data structures

## Relationship to Production Scripts

These notebooks complement the production pipeline (`scripts/update_rtd.py`):

| Feature | Notebooks | Production Scripts |
|---------|-----------|-------------------|
| **Purpose** | Interactive learning & exploration | Automated execution |
| **Code Base** | **Same modular peru_gdp_rtd package** | Same modular peru_gdp_rtd package |
| **Execution** | Cell-by-cell, user-controlled | One-command, fully automated |
| **Output** | Visible intermediate results | Final datasets only |
| **Best For** | Learning, debugging, customization | Regular updates, production use |

**When to use notebooks:**
- Learning how the pipeline works
- Debugging specific pipeline stages
- Exploring intermediate data outputs
- Customizing the pipeline for research needs
- Understanding the modular architecture

**When to use scripts:**
- Regular dataset updates
- Automated/scheduled executions
- Production deployments
- CI/CD integration
- When you need the complete pipeline without interaction

## Modular Architecture Benefits

Both notebooks and scripts now use the same refactored modular architecture:

✅ **Organized imports** - Functions grouped by purpose (scraping, cleaning, transforming)
✅ **Maintainability** - Each module has a single, clear responsibility
✅ **Reusability** - Import only what you need
✅ **Type safety** - Complete type hints throughout
✅ **Professional quality** - Production-ready code in educational context

## Future Notebook Development

Planned step-by-step tutorial notebooks to cover specific topics:

1. **01_web_scraping.ipynb** - Web scraping from BCRP website using Selenium
2. **02_pdf_processing.ipynb** - Extracting and processing tables from PDFs
3. **03_data_cleaning.ipynb** - Cleaning and standardizing economic data
4. **04_rtd_construction.ipynb** - Building vintage and real-time datasets
5. **05_metadata_management.ipynb** - Handling base-year changes and benchmark revisions
6. **06_releases_datasets.ipynb** - Converting vintages to releases format

These tutorials will demonstrate specific aspects of the modular architecture in focused, digestible notebooks.

## Optional Audio Alerts

The notebooks can use audio alerts to notify users when long-running operations complete. This is optional convenience functionality for interactive sessions.

**Audio alert functions** (from `peru_gdp_rtd.utils`):
```python
init_audio()              # Initialize pygame mixer
load_alert_track()        # Load an alert sound from alert_track/
play_alert_track()        # Play the alert
stop_alert_track()        # Stop playback
```

## Contributing

If you create additional educational notebooks, please:
- Use the modular `peru_gdp_rtd` imports (see `new_gdp_rtd.ipynb` for template)
- Follow the naming convention: `descriptive_name.ipynb`
- Include comprehensive markdown cells explaining each step
- Add the notebook description to this README
- Ensure notebooks are self-contained and reproducible
- Group imports by module for clarity
