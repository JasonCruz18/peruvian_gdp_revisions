# Zenodo Upload Recommendation for Peru GDP RTD

**Date:** January 12, 2026
**For:** Data in Brief Manuscript Submission
**DOI:** 10.5281/zenodo.18099975

---

## Executive Summary

**RECOMMENDATION: Upload ONLY the final output datasets (16 CSV files) to Zenodo.**
**Do NOT upload raw/input data or scanned PDFs.**

### Rationale:
1. **DIB Best Practice**: Share final analysis-ready datasets, not intermediate processing files
2. **Data Completeness**: Final outputs are the authoritative, quality-assured data product
3. **Transparency**: Code repository provides full reproducibility (raw→output transformation)
4. **File Size**: Keep Zenodo deposit manageable (~20-25 MB vs. 5+ GB with all data)
5. **User Experience**: Researchers want clean, ready-to-use datasets

---

## What to Upload to Zenodo

### ✅ INCLUDE: Final Output Datasets (16 CSV files)

**Directory:** `data/output/vintages/` and `data/output/releases/`

**Files to upload:**

#### Vintage Format (8 files):
```
vintages/monthly_gdp_vintages.csv                          (~2.9 MB)
vintages/monthly_gdp_vintages_adjusted.csv                  (~2.9 MB)
vintages/monthly_gdp_vintages_benchmark.csv                 (~2.9 MB)
vintages/monthly_gdp_vintages_adjusted_benchmark.csv        (~2.9 MB)
vintages/quarterly_gdp_vintages.csv                         (~1.3 MB)
vintages/quarterly_gdp_vintages_adjusted.csv                (~1.3 MB)
vintages/quarterly_gdp_vintages_benchmark.csv               (~1.3 MB)
vintages/quarterly_gdp_vintages_adjusted_benchmark.csv      (~1.3 MB)
```

#### Releases Format (8 files):
```
releases/monthly_gdp_releases.csv                           (~212 KB)
releases/monthly_gdp_releases_adjusted.csv                  (~219 KB)
releases/monthly_gdp_releases_benchmark.csv                 (~192 KB)
releases/monthly_gdp_releases_adjusted_benchmark.csv        (~192 KB)
releases/quarterly_gdp_releases.csv                         (~186 KB)
releases/quarterly_gdp_releases_adjusted.csv                (~205 KB)
releases/quarterly_gdp_releases_benchmark.csv               (~171 KB)
releases/quarterly_gdp_releases_adjusted_benchmark.csv      (~171 KB)
```

**Total Size:** ~20-25 MB

**File Organization in Zenodo:**
```
peru_gdp_rtd_v1.0/
├── vintages/
│   ├── monthly_gdp_vintages.csv
│   ├── monthly_gdp_vintages_adjusted.csv
│   ├── monthly_gdp_vintages_benchmark.csv
│   ├── monthly_gdp_vintages_adjusted_benchmark.csv
│   ├── quarterly_gdp_vintages.csv
│   ├── quarterly_gdp_vintages_adjusted.csv
│   ├── quarterly_gdp_vintages_benchmark.csv
│   └── quarterly_gdp_vintages_adjusted_benchmark.csv
├── releases/
│   ├── monthly_gdp_releases.csv
│   ├── monthly_gdp_releases_adjusted.csv
│   ├── monthly_gdp_releases_benchmark.csv
│   ├── monthly_gdp_releases_adjusted_benchmark.csv
│   ├── quarterly_gdp_releases.csv
│   ├── quarterly_gdp_releases_adjusted.csv
│   ├── quarterly_gdp_releases_benchmark.csv
│   └── quarterly_gdp_releases_adjusted_benchmark.csv
├── README.md                    (ZENODO_README.md from repository)
└── LICENSE.txt                  (CC-BY-4.0 license text)
```

---

## ❌ EXCLUDE: Do NOT Upload These

### 1. Raw Scanned PDFs (228 files, ~500 MB)
- **Location:** `OCR/raw/1994/` through `OCR/raw/2012/`
- **Why exclude:**
  - Not necessary - final curated CSVs are the authoritative data
  - Large file size burden
  - Users cannot process scanned images themselves
  - Would require Zenodo "Restricted Access" (>50MB per file)
- **Transparency maintained via:**
  - Complete OCR code in GitHub repository
  - Year 2001 demonstration outputs (12 CSVs) in `OCR/output/table_1/2001/`
  - Detailed methodology in ZENODO_README and _Supplement.tex

### 2. Downloaded Post-2013 PDFs (~4 GB)
- **Location:** `data/raw/new_weekly_reports/2013/` through `data/raw/new_weekly_reports/2025/`
- **Why exclude:**
  - Available online: https://www.bcrp.gob.pe/publicaciones/nota-semanal.html
  - Users can re-download using code repository
  - Extremely large file size
  - BCRP is authoritative source
- **Transparency maintained via:**
  - Web scraping code in `peru_gdp_rtd/scrapers/bcrp_scraper.py`
  - Complete pipeline documentation

### 3. Raw Input CSVs - Pre-2013 (~5-10 MB)
- **Location:** `data/raw/old_weekly_reports/table_1/` and `table_2/`
- **Why exclude:**
  - Intermediate processing files
  - NOT analysis-ready (require cleaning)
  - Already processed into final outputs
  - Users won't know how to use these correctly
- **Alternative consideration:** COULD include if reviewers request, but NOT recommended
- **Transparency maintained via:**
  - OCR pipeline code (`OCR/` directory)
  - Year 2001 demonstration showing raw OCR → curated CSV process
  - Cleaning pipeline code (`peru_gdp_rtd/cleaners/`)

### 4. Input Vintages (~15 MB)
- **Location:** `data/input/table_1/` and `table_2/` (annual vintage files)
- **Why exclude:**
  - Intermediate processing stage
  - Final concatenated output supersedes these
  - Users want complete dataset, not year-by-year fragments
- **Transparency maintained via:**
  - Vintage preparation code
  - Concatenation module documentation

---

## ✅ INCLUDE: Documentation Files

### 1. README.md (REQUIRED)
- **Source:** `ZENODO_README.md` from repository
- **Content:** Complete dataset documentation with:
  - File structure and naming conventions
  - Data dictionary (column descriptions)
  - Coverage information
  - Data collection methodology (including OCR details)
  - Citation information
  - Usage examples
  - Contact information

### 2. LICENSE.txt (REQUIRED)
- **License:** Creative Commons Attribution 4.0 International (CC-BY-4.0)
- **Content:** Full license text from https://creativecommons.org/licenses/by/4.0/legalcode.txt
- **Why CC-BY-4.0:**
  - Standard for open data
  - Permits commercial and academic reuse
  - Requires attribution only
  - Aligned with DIB journal policy

### 3. CITATION.cff (OPTIONAL but RECOMMENDED)
- **Format:** Citation File Format (machine-readable)
- **Content:**
```yaml
cff-version: 1.2.0
title: "Peru GDP Real-Time Dataset (1994-2025)"
message: "If you use this dataset, please cite it as below."
type: dataset
authors:
  - family-names: Cruz
    given-names: Jason
    orcid: "https://orcid.org/0009-0001-4640-5500"
  - family-names: Winkelried
    given-names: Diego
    orcid: "https://orcid.org/0000-0002-9388-2617"
  - family-names: Torres
    given-names: Javier
    orcid: "https://orcid.org/0000-0001-6850-1395"
version: "1.0.0"
date-released: "2025-01-26"
doi: "10.5281/zenodo.18099975"
url: "https://github.com/JasonCruz18/peru_gdp_revisions"
keywords:
  - real-time data
  - GDP revisions
  - Peru
  - emerging markets
  - nowcasting
license: CC-BY-4.0
```

---

## Zenodo Metadata Configuration

When uploading to Zenodo, configure metadata as follows:

### Basic Information:
- **Upload type:** Dataset
- **Publication date:** 2025-01-26 (or actual submission date)
- **Title:** Peru GDP Real-Time Dataset (1994-2025)
- **Authors:**
  - Jason Cruz (ORCID: 0009-0001-4640-5500) [Corresponding]
  - Diego Winkelried (ORCID: 0000-0002-9388-2617)
  - Javier Torres (ORCID: 0000-0001-6850-1395)

### Description (Abstract):
```
This dataset provides a comprehensive real-time database of Peru's GDP growth
rates spanning 1994-2025, comprising over 1000 data releases across 30+ years.
The dataset includes monthly, quarterly, and annual GDP growth rates for
aggregate GDP and 8 economic sectors, organized in vintage format (columns =
release dates) and releases format (columns = revision sequences). Data were
systematically collected from the Central Reserve Bank of Peru (BCRP) Weekly
Reports using Optical Character Recognition for pre-2013 scanned documents and
automated web scraping for 2013-2025 digital publications. The dataset enables
research on GDP revision patterns, real-time forecasting, nowcasting, and
statistical quality assessment in emerging economies.
```

### Keywords (comma-separated):
```
real-time macroeconomic data, GDP revisions, emerging markets, Peru,
nowcasting, vintage data, data curation, BCRP, economic indicators,
revision analysis
```

### Additional Information:
- **Version:** 1.0.0
- **Language:** English
- **License:** Creative Commons Attribution 4.0 International (CC-BY-4.0)
- **Access right:** Open Access
- **Related identifiers:**
  - **Is supplement to:** (GitHub repository) https://github.com/JasonCruz18/peru_gdp_revisions (isSupplementTo, URL)
  - **Cites:** (If you have a related paper DOI, add here)

### Communities:
- Search and add: "Economic Data", "Open Science", if available

### Funding:
- **Grant Title:** Proyectos de Investigación en Ciencias Sociales
- **Funder:** CONCYTEC / PROCIENCIA
- **Grant Number:** E041-2025-04

---

## How the DIB Paper Should Reference Data

### In Specifications Table:
```
Data accessibility:
Repository name: Zenodo
Data identification number: 10.5281/zenodo.18099975
Direct URL to data: https://doi.org/10.5281/zenodo.18099975
Related code repository: https://github.com/JasonCruz18/peru_gdp_revisions
Instructions: Dataset freely accessible via DOI. 16 CSV files organized in
vintages/ and releases/ directories. Complete documentation in README.md.
Full reproducibility via code repository.
```

### In Methods Section - Data Lineage:
```
The final dataset on Zenodo represents the authoritative, quality-assured
data product after complete processing. Pre-2013 data in the repository were
initially extracted using OCR (demonstrated on year 2001, achieving 70.5%
automated completeness) and then underwent extensive manual verification.
Post-2013 data were collected via automated web scraping. All data were
processed through a 70+ function cleaning pipeline. The complete processing
code is publicly available in the GitHub repository, enabling full
reproducibility from source PDFs to final datasets.
```

### In Limitations Section:
```
The Zenodo deposit contains only the final processed datasets (16 CSV files).
Raw source materials (scanned PDFs for 1994-2012, downloaded PDFs for 2013-2025)
are not included due to file size constraints and because: (1) post-2013 PDFs
remain freely available from BCRP, and (2) pre-2013 data required extensive
manual curation after OCR, making the curated CSVs the authoritative source.
Complete processing code and year 2001 OCR demonstration outputs are available
in the GitHub repository to ensure full transparency and reproducibility.
```

---

## Transparency Strategy

### What Users Get:
1. **Zenodo (10.5281/zenodo.18099975):**
   - Final analysis-ready datasets (16 CSV files)
   - Complete documentation (README)
   - License information

2. **GitHub (peru_gdp_revisions):**
   - Complete source code (all processing steps)
   - OCR pipeline with year 2001 demonstration
   - Technical supplement documentation
   - Tutorial notebooks
   - Configuration files
   - Test suite

### Reproducibility Flow:
```
Source PDFs (BCRP website or library scans)
    ↓
GitHub Code Repository
    ↓  (OCR for pre-2013)
    ↓  (Web scraping for 2013+)
    ↓  (70+ cleaning functions)
    ↓  (Vintage construction)
    ↓  (Metadata handling)
    ↓  (Format conversion)
    ↓
Zenodo Final Datasets (16 CSV files)
```

### User Benefits:
- **Researchers:** Get clean, ready-to-use data immediately from Zenodo
- **Replicators:** Can reproduce entire pipeline using GitHub code
- **Methodologists:** Can inspect OCR demonstration (year 2001) and understand data quality
- **Extenders:** Can update dataset with new releases using provided code

---

## File Size Comparison

| Option | Files | Total Size | Zenodo OK? | Recommended? |
|--------|-------|------------|------------|--------------|
| **Final outputs only** | 16 CSVs | ~20-25 MB | ✅ Yes | ✅ **YES** |
| + Raw pre-2013 CSVs | +180 files | ~35 MB | ✅ Yes | ⚠️ Maybe if requested |
| + Downloaded PDFs | +500 files | ~4 GB | ⚠️ Large | ❌ NO |
| + Scanned PDFs | +228 files | ~500 MB | ⚠️ Large | ❌ NO |
| Everything | 900+ files | ~5 GB | ❌ Too large | ❌ **NO** |

**Zenodo limits:** 50 GB per dataset (but discouraged for large files)

---

## Pre-Publication Checklist

Before publishing on Zenodo:

- [ ] Ensure all 16 CSV files are final versions (from latest pipeline run)
- [ ] Create vintages/ and releases/ subdirectories
- [ ] Copy ZENODO_README.md to README.md
- [ ] Create LICENSE.txt with CC-BY-4.0 full text
- [ ] Create CITATION.cff file (optional but recommended)
- [ ] Verify all file names match documentation
- [ ] Test: Download and open one file from each variant to confirm format
- [ ] Complete Zenodo metadata form (all fields)
- [ ] Double-check DOI reserved: 10.5281/zenodo.18099975
- [ ] Add funding information (CONCYTEC grant)
- [ ] Link to GitHub repository in "Related identifiers"
- [ ] **DO NOT PUBLISH** until DIB manuscript is accepted (keep as draft)
- [ ] After DIB acceptance: Publish Zenodo dataset
- [ ] Copy final DOI into DIB manuscript before final submission

---

## Recommended Zenodo Upload Workflow

### Step 1: Prepare Files Locally
```bash
# Create Zenodo upload directory
mkdir zenodo_upload
cd zenodo_upload

# Create subdirectories
mkdir vintages releases

# Copy vintage files
cp ../data/output/vintages/monthly_gdp_*.csv vintages/
cp ../data/output/vintages/quarterly_gdp_*.csv vintages/

# Copy releases files
cp ../data/output/releases/monthly_gdp_*.csv releases/
cp ../data/output/releases/quarterly_gdp_*.csv releases/

# Copy documentation
cp ../ZENODO_README.md README.md

# Create LICENSE.txt
# (Download CC-BY-4.0 text from https://creativecommons.org/licenses/by/4.0/legalcode.txt)

# Create CITATION.cff
# (Use template above)

# Verify structure
ls -R
```

### Step 2: Create ZIP Archive (Optional but Recommended)
```bash
zip -r peru_gdp_rtd_v1.0.zip vintages/ releases/ README.md LICENSE.txt CITATION.cff
```

### Step 3: Upload to Zenodo
1. Go to https://zenodo.org/deposit/18099975 (your reserved DOI)
2. Upload either:
   - Individual files + directories, OR
   - Single ZIP file
3. Fill metadata form (use template above)
4. Click "Save" (NOT "Publish" yet)
5. **Keep as DRAFT** until DIB acceptance

### Step 4: After DIB Acceptance
1. Review uploaded files one final time
2. Update "Related identifiers" if paper DOI is available
3. Click "Publish"
4. Copy final Zenodo DOI badge into DIB manuscript
5. Update GitHub README with Zenodo badge

---

## Summary

**UPLOAD TO ZENODO:** Final 16 CSV files + README + LICENSE
**TOTAL SIZE:** ~20-25 MB (well within limits)
**TRANSPARENCY:** Complete via GitHub code repository + OCR demonstration
**USER EXPERIENCE:** Clean, analysis-ready data immediately available
**REPRODUCIBILITY:** Full pipeline code enables replication and updates

This approach follows DIB best practices, keeps Zenodo deposit manageable, and provides complete transparency through the combination of final datasets (Zenodo) + complete methodology (GitHub + DIB paper).

---

**Created:** January 12, 2026
**For Review By:** Jason Cruz, Diego Winkelried, Javier Torres
**Action Required:** Confirm approach before Zenodo publication
