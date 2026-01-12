# OCR Pipeline for Peru GDP Real-Time Dataset

**Standalone OCR pipeline for extracting GDP growth rate tables from scanned Weekly Report PDFs. Demonstrated on year 2001 (12 PDFs) as methodological example.**

## Overview

This OCR (Optical Character Recognition) pipeline extracts GDP growth rate tables from scanned PDF documents and converts them to structured CSV files. It implements a complete 11-step image preprocessing workflow based on the methodology described in the project's technical supplement (_Supplement.tex).

**Important Note:** This pipeline was developed and tested on **year 2001 (12 PDFs)** as a methodological demonstration for the Data in Brief manuscript. It shows the transparent process used for initial data extraction from scanned documents, followed by manual human curation. The final curated CSVs in `data/raw/old_weekly_reports/` represent the official raw data.

### Key Features

- **Complete Preprocessing Pipeline:** 11-step image enhancement (grayscale, binarization, denoising, deskewing, CLAHE contrast enhancement, border removal)
- **Dual Table Handling:** Automatically extracts upper table (growth rates) while ignoring lower table (levels)
- **Bilingual Support:** Recognizes both Spanish and English sector names (post-2000 PDFs)
- **Fuzzy Matching:** Tolerates OCR errors in sector name recognition
- **Quality Assurance:** Confidence scoring and automatic flagging of low-quality outputs for manual review
- **Resume Support:** Checkpoint-based progress tracking enables resuming after interruptions
- **Comprehensive Validation:** Automated checks for CSV structure, sector names, and numeric values

### Demonstrated Results (Year 2001)

- **Input:** 12 scanned PDF files from year 2001
- **Output:** 12 CSV files in `OCR/output/table_1/2001/`
- **Processing Time:** ~3 minutes (15 seconds per PDF)
- **Data Completeness:** 70.5% (755 missing values out of 2,561 cells)
- **Sectors Extracted:** 114 sector-month observations
- **OCR Errors:** Demonstrates need for manual review (e.g., "agropacuaro"→"agropecuario", "posci"→"pesca")

---

## Installation

### 1. System Requirements

**Windows:**
```bash
# Install Tesseract OCR 5.x
# Download from: https://github.com/UB-Mannheim/tesseract/wiki
# Install to: C:\Program Files\Tesseract-OCR
# IMPORTANT: Include Spanish (spa) and English (eng) language packs during installation
# Add to PATH

# Install Poppler (for pdf2image)
# Download from: https://github.com/oschwartz10612/poppler-windows/releases
# Extract and add bin/ directory to PATH
```

**Verify Installation:**
```bash
# Check Tesseract
tesseract --version
# Should show: tesseract 5.x.x

# Check languages
tesseract --list-langs
# Should include: eng, spa

# Check Poppler
pdftoppm -v
```

### 2. Python Dependencies

```bash
# From the project root directory:
cd OCR
pip install -r requirements.txt
```

**Dependencies Installed:**
- `Pillow` - Image manipulation
- `opencv-python` - Image preprocessing
- `scikit-image` - Advanced image processing
- `pdf2image` - PDF to PNG conversion
- `pytesseract` - Tesseract Python wrapper
- `pandas`, `numpy` - Data processing
- `tqdm` - Progress bars
- `pyyaml` - Configuration management

---

## Quick Start

### Process All PDFs (1994-2012)

```bash
# From project root:
python scripts/run_ocr_pipeline.py
```

This will:
1. Process all 228 PDFs in `OCR/raw/`
2. Generate CSVs in `OCR/output/table_1/` and `OCR/output/table_2/`
3. Flag low-confidence outputs in `OCR/review/` for manual verification
4. Save progress to `OCR/checkpoints/ocr_progress.json`
5. Generate summary report in `OCR/logs/`

### Process Specific Years

```bash
# Single year
python scripts/run_ocr_pipeline.py --year 2000

# Year range
python scripts/run_ocr_pipeline.py --years 1994-2000

# Resume from checkpoint
python scripts/run_ocr_pipeline.py --resume

# Verbose output (for debugging)
python scripts/run_ocr_pipeline.py -v --save-images
```

---

## Pipeline Architecture

### Folder Structure

```
OCR/
├── ocr_processors/          # Core processing modules
│   ├── image_preprocessor.py    # 11-step preprocessing pipeline
│   ├── ocr_engine.py             # Tesseract execution
│   ├── table_extractor.py        # Table region extraction
│   ├── csv_converter.py          # OCR → CSV conversion
│   └── validator.py              # Quality checks
│
├── ocr_config/              # Configuration
│   ├── config.yaml              # Main settings file
│   └── settings.py              # Settings loader
│
├── ocr_utils/               # Utilities
│   ├── progress_tracker.py      # Checkpoint management
│   ├── logger.py                # Logging setup
│   └── file_manager.py          # File operations
│
├── raw/                     # INPUT: Scanned PDFs
│   ├── 1994/ (12 PDFs)
│   ├── 1995/ (12 PDFs)
│   └── ... (through 2012)
│
├── output/                  # OUTPUT: Generated CSVs
│   ├── table_1/ (monthly data)
│   └── table_2/ (quarterly/annual data)
│
├── review/                  # Low-confidence outputs for manual correction
├── temp_images/             # Intermediate preprocessed images
├── logs/                    # Processing logs
└── checkpoints/             # Progress tracking
```

### Processing Workflow

```
PDF → PNG Conversion → Image Preprocessing (11 steps) →
Table Extraction → OCR Execution → Post-Processing →
CSV Conversion → Validation → Output/Review
```

**11-Step Image Preprocessing:**
1. PDF to PNG (300 DPI)
2. Grayscale conversion
3. Adaptive binarization (Otsu's method)
4. Noise removal (median filtering)
5. Skew correction (deskewing)
6. DPI scaling (ensure ≥300 DPI)
7. Contrast enhancement (CLAHE)
8. Morphological thinning (optional)
9. Border removal

---

## Configuration

Edit `OCR/ocr_config/config.yaml` to customize pipeline behavior:

### Key Settings

**Image Preprocessing:**
```yaml
preprocessing:
  target_dpi: 300                    # Minimum DPI for OCR
  noise_removal_method: "median"     # median, gaussian, bilateral
  contrast_enhancement: true         # Apply CLAHE
  clahe_clip_limit: 2.0
  skew_angle_threshold: 0.5          # Only correct if skew > 0.5°
```

**Tesseract OCR:**
```yaml
tesseract:
  language: "spa+eng"                # Spanish + English
  psm: 6                             # Page segmentation mode
  oem: 3                             # OCR Engine Mode (LSTM + Legacy)
```

**Validation:**
```yaml
validation:
  confidence_threshold: 0.85         # Flag if confidence < 85%
  expected_min_sectors: 8            # Minimum sector rows
```

**Table Extraction:**
```yaml
table_extraction:
  extract_upper_table_only: true     # Ignore lower table (levels)
  upper_table_region_ratio: [0.0, 0.5]  # Crop to top 50%
```

---

## Output Format

### CSV Structure (Compatible with peru_gdp_rtd)

**Monthly Table (table_1):**
```csv
sectores_economicos;economic_sectors;1992_ene;1992_feb;...;1993_nov;1993_mean
agropecuario;agriculture and livestock;3.7;3.6;...;9.6;5.3
pesca;fishing;-29.8;-26.4;...;12.3;43.6
mineria e hidrocarburos;mining and fuel;-1.4;-5.5;...;1.4;8.1
manufactura;manufacturing;-3.5;-2.3;...;8.8;9.2
construccion;construction;27.7;12.8;...;28.8;12.8
comercio;commerce;4.2;11.2;...;8.0;4.0
otros servicios;other services;3.1;4.9;...;6.5;5.0
pbi;gdp;1.3;1.8;...;7.5;6.7
```

**Quarterly Table (table_2):**
```csv
sectores_económicos;economic_sectors;1997_1;1997_2;1997_3;1997_4;1997_year;...
agropecuario;agriculture and livestock;17.0;4.3;-4.8;6.4;4.9;...
pesca;fishing;-11.7;25.0;7.8;-55.9;-12.1;...
...
```

### File Naming Convention

- **Input:** `OCR/raw/YYYY/ns_XX_YYYY.pdf` (underscore)
- **Output:** `OCR/output/table_1/YYYY/ns-XX-YYYY.csv` (hyphen)

---

## Manual Review Workflow

### When is Manual Review Needed?

OCR automatically flags outputs for manual review when:
- OCR confidence score < 85%
- Validation errors detected (missing columns, invalid sectors, etc.)
- Extreme values detected (>500% or <-100%)

### Review Process

1. **Check the flagged files list:**
   ```bash
   cat OCR/needs_review.txt
   ```

2. **For each flagged file, review package in `OCR/review/YYYY/ns-XX-YYYY/`:**
   - `original.pdf` - Scanned source document
   - `preprocessed.png` - After image preprocessing
   - `ocr_output.csv` - OCR result needing correction
   - `issues.txt` - List of detected problems

3. **Manually correct the CSV:**
   - Compare `ocr_output.csv` with `original.pdf`
   - Fix errors (digit misrecognition, missing values, incorrect sectors)
   - Common OCR errors: O→0, l→1, S→5, missing decimal points

4. **Move corrected CSV to output:**
   ```bash
   cp OCR/review/1994/ns-03-1994/ocr_output.csv OCR/output/table_1/1994/ns-03-1994.csv
   ```

5. **Delete review folder:**
   ```bash
   rm -rf OCR/review/1994/ns-03-1994/
   ```

6. **Verify all corrections:**
   ```bash
   python scripts/run_ocr_pipeline.py --verify
   ```

---

## Integration with Main Pipeline

### Option A: Copy Outputs to Existing Location (Recommended)

```bash
# After OCR completes and manual review is done:
cp -r OCR/output/table_1/* data/raw/old_weekly_reports/table_1/
cp -r OCR/output/table_2/* data/raw/old_weekly_reports/table_2/

# Run existing pipeline:
python scripts/update_rtd.py
```

### Option B: Update Configuration

Modify `config/config.yaml` to include OCR outputs:
```yaml
paths:
  old_weekly_reports:
    - "data/raw/old_weekly_reports"
    - "OCR/output"  # Add this line
```

---

## Troubleshooting

### "Tesseract not found" Error

**Problem:** `pytesseract.TesseractNotFoundError`

**Solution:**
1. Verify Tesseract is installed: `tesseract --version`
2. Add to PATH if needed (Windows): `C:\Program Files\Tesseract-OCR`
3. Or set path explicitly in code:
   ```python
   import pytesseract
   pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
   ```

### "Poppler not found" Error

**Problem:** `pdf2image.exceptions.PDFInfoNotInstalledError`

**Solution:**
1. Download Poppler for Windows: https://github.com/oschwartz10612/poppler-windows/releases
2. Extract and add `poppler-xx.xx.x/Library/bin/` to PATH
3. Restart terminal/IDE

### Low OCR Accuracy

**Problem:** Many files flagged for manual review (>20%)

**Possible Causes:**
1. **Poor scan quality** - Check original PDFs
2. **Wrong language pack** - Verify Spanish+English installed: `tesseract --list-langs`
3. **Preprocessing too aggressive** - Try reducing `clahe_clip_limit` or disabling `thinning`
4. **Wrong PSM mode** - Experiment with different values (3, 4, 6, 11)

**Solution:**
1. Test on a single PDF with debugging:
   ```bash
   python scripts/run_ocr_pipeline.py --year 2000 --save-images -v
   ```
2. Inspect preprocessed images in `OCR/temp_images/`
3. Adjust preprocessing parameters in `config.yaml`

### Memory Issues

**Problem:** Out of memory errors during processing

**Solution:**
1. Process in smaller batches:
   ```bash
   python scripts/run_ocr_pipeline.py --years 1994-1998
   python scripts/run_ocr_pipeline.py --years 1999-2004
   python scripts/run_ocr_pipeline.py --years 2005-2012
   ```
2. Enable auto-cleanup:
   ```yaml
   progress:
     auto_cleanup_temp: true
   ```
3. Disable intermediate image saving:
   ```yaml
   progress:
     save_intermediate_images: false
   ```

---

## Performance Optimization

### Speed

- **Parallel Processing:** Currently sequential. Future enhancement: process multiple PDFs in parallel
- **DPI Settings:** Lower DPI = faster but less accurate (300 recommended minimum)
- **Preprocessing Steps:** Disable optional steps (thinning) if not needed

### Accuracy

- **Higher DPI:** Increase to 400-600 for poor quality scans (slower)
- **CLAHE Enhancement:** Essential for shadowed/faded scans
- **Skew Correction:** Critical for tilted pages
- **Manual Verification:** Budget ~5-10% of outputs for human review

---

## Expected Results

### Success Metrics

Based on the challenges described in _Supplement.tex (warped text, shadows, blur, highlighted entries):

| Metric | Target | Notes |
|--------|--------|-------|
| High Confidence (>90%) | 85-90% | Good scan quality, clear tables |
| Medium Confidence (85-90%) | 5-10% | Minor issues, automated processing acceptable |
| Low Confidence (<85%) | 5% | Needs manual review |
| Complete Failure | <1% | Extremely poor scans, manual transcription |

### Total Processing Time

- **Setup:** 10-15 minutes (install dependencies, verify Tesseract)
- **Full Pipeline:** 2-3 hours (228 PDFs)
- **Manual Review:** 1-2 hours (10-20 flagged files)
- **Total:** ~4-5 hours from start to finish

---

## Advanced Usage

### Custom Configuration File

```bash
python scripts/run_ocr_pipeline.py --config path/to/custom_config.yaml
```

### Debugging Mode

```bash
# Save all intermediate images and verbose logging
python scripts/run_ocr_pipeline.py --save-images -v --year 2000
```

### Force Reprocessing

```bash
# Ignore existing outputs and reprocess everything
python scripts/run_ocr_pipeline.py --force
```

### Verification Only

```bash
# Validate existing outputs without reprocessing
python scripts/run_ocr_pipeline.py --verify
```

---

## Contributing

### Extending the Pipeline

**Adding New Preprocessing Steps:**
1. Add method to `ocr_processors/image_preprocessor.py`
2. Update `preprocess_for_ocr()` to include new step
3. Add configuration options to `config.yaml`

**Improving OCR Accuracy:**
1. Experiment with Tesseract PSM modes (1-13)
2. Try different binarization methods
3. Adjust CLAHE parameters for specific scan characteristics

**Supporting Other Countries:**
1. Update language packs in `tesseract.language`
2. Modify sector name mappings in `csv_converter.py`
3. Adjust table structure detection if layout differs

---

## Citation

If you use this OCR pipeline in your research, please cite:

```bibtex
@software{cruz2026ocr,
  author = {Cruz, Jason},
  title = {OCR Pipeline for Peru GDP Real-Time Dataset},
  year = {2026},
  publisher = {GitHub},
  url = {https://github.com/JasonCruz18/peru_gdp_revisions}
}
```

---

## Support

For issues, questions, or contributions:
- **GitHub Issues:** https://github.com/JasonCruz18/peru_gdp_revisions/issues
- **Email:** jj.cruza@up.edu.pe
- **Documentation:** See `MANUAL_REVIEW_GUIDE.md` for detailed review instructions

---

## License

MIT License - See project LICENSE file for details.

---

## Acknowledgments

- **Tesseract OCR:** Google's open-source OCR engine
- **BCRP Renzo Rossini Library:** For access to historical Weekly Report volumes
- **CONCYTEC-PROCIENCIA:** Funding support (Grant E041-2025-04)
