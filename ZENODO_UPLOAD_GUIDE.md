# Zenodo Upload Guide - Peru GDP RTD

**Purpose:** Step-by-step instructions for uploading the Peru GDP Real-Time Dataset to Zenodo and obtaining a DOI.

**Estimated Time:** 2-3 hours (first time), 1 hour (if familiar with Zenodo)

---

## Prerequisites

- [ ] Zenodo account (create at https://zenodo.org if needed)
- [ ] ORCID iD (register at https://orcid.org if needed)
- [ ] All CSV files generated (16 files total)
- [ ] ZENODO_README.md completed

---

## Step 1: Create Zenodo Account (if needed)

1. Go to https://zenodo.org
2. Click "Sign up" (top right)
3. Choose one of:
   - **Sign in with ORCID** (recommended - links your ORCID automatically)
   - Sign in with GitHub
   - Create with email

**Time:** 5 minutes

---

## Step 2: Start New Upload

1. Log in to Zenodo
2. Click **"Upload"** → **"New upload"** (top right, green button)
3. You'll see the upload form with sections:
   - Files
   - Basic information
   - License
   - Funding (optional)

**Note:** Don't click "Publish" until everything is complete!

---

## Step 3: Upload Dataset Files

### Files to Upload (16 CSV files)

**From `data/output/vintages/`** (8 files):
- [ ] `monthly_gdp_vintages.csv` (2.9 MB)
- [ ] `quarterly_gdp_vintages.csv` (1.3 MB)
- [ ] `monthly_gdp_vintages_adjusted.csv` (2.9 MB)
- [ ] `quarterly_gdp_vintages_adjusted.csv` (1.3 MB)
- [ ] `monthly_gdp_vintages_benchmark.csv` (2.9 MB)
- [ ] `quarterly_gdp_vintages_benchmark.csv` (1.3 MB)
- [ ] `monthly_gdp_vintages_adjusted_benchmark.csv` (2.9 MB)
- [ ] `quarterly_gdp_vintages_adjusted_benchmark.csv` (1.3 MB)

**From `data/output/releases/`** (8 files):
- [ ] `monthly_gdp_releases.csv` (212 KB)
- [ ] `quarterly_gdp_releases.csv` (186 KB)
- [ ] `monthly_gdp_releases_adjusted.csv` (219 KB)
- [ ] `quarterly_gdp_releases_adjusted.csv` (205 KB)
- [ ] `monthly_gdp_releases_benchmark.csv` (192 KB)
- [ ] `quarterly_gdp_releases_benchmark.csv` (171 KB)
- [ ] `monthly_gdp_releases_adjusted_benchmark.csv` (192 KB)
- [ ] `quarterly_gdp_releases_adjusted_benchmark.csv` (171 KB)

**Additional File:**
- [ ] `ZENODO_README.md` (renamed to `README.md` when uploading)

### Upload Process:

1. Click **"Choose files"** or drag-and-drop
2. Select all 16 CSV files + README
3. Wait for upload to complete (green checkmarks)
4. **Total size:** ~17 MB (well under Zenodo's 50 GB limit per file)

**Time:** 10-15 minutes (depending on internet speed)

---

## Step 4: Fill Basic Information

### Digital Object Identifier (DOI)
- [ ] **Leave default:** "No" (Zenodo will auto-generate)
- Alternative: Reserve DOI first if you need it for the manuscript

### Publication Type
- [ ] Select: **"Dataset"**

### Publication Date
- [ ] Enter: **December 28, 2024** (or current date)

### Title
```
Peru GDP Real-Time Dataset (1994-present)
```

### Authors
- [ ] Click **"Add creator"**
- [ ] Enter your name: `[Family name], [Given names]`
- [ ] Add **ORCID iD** (click "Lookup" if logged in with ORCID)
- [ ] Add **Affiliation:** Your institution (e.g., "Universidad del Pacífico" or "CIUP")

**For multiple authors:** Click "Add creator" again

### Description (Abstract)

```
This dataset provides a comprehensive real-time database (RTD) of Peru's Gross Domestic Product (GDP) growth rates from 1994 to the present. Data are sourced from the Central Reserve Bank of Peru (Banco Central de Reserva del Perú, BCRP) Weekly Reports and systematically transformed into structured formats suitable for revision analysis, nowcasting, and forecasting research.

The dataset includes 16 CSV files organized in two formats:
(1) Vintage format: columns represent release dates, enabling analysis of information available at specific points in time
(2) Releases format: columns represent revision sequences (1st, 2nd, 3rd+ releases), facilitating revision pattern analysis

Key features:
- Coverage: Monthly, quarterly, and annual GDP growth rates (1994–2024)
- Vintages tracked: 1000+ data releases across 30+ years
- Sectors: 8 economic sectors (Primary, Manufacturing, Construction, Commerce, etc.)
- Base-year adjustments: Accounts for methodological changes (1990, 1994, 2007 base years)
- Fully reproducible: Complete Python pipeline available at GitHub

The data enable research on GDP revision patterns, real-time forecasting, nowcasting, forecast evaluation, and cross-country comparisons of statistical practices in emerging economies.
```

### Version
- [ ] Enter: **1.0.0**

### Language
- [ ] Select: **English**

### Keywords (7 keywords, one per line)
```
GDP
Real-time data
Peru
Economic revisions
Nowcasting
Macroeconomic data
Time series
```

### Additional Notes (optional)
```
This dataset is accompanied by open-source code for full reproducibility.
Code repository: https://github.com/[yourusername]/peru_gdp_revisions

For detailed methodology, see the repository documentation.

Related research article (in preparation): "Rationality and Nowcasting on Peruvian GDP Revisions"
```

**Time:** 20-30 minutes

---

## Step 5: Select License

### Recommended License for Data: CC-BY-4.0

- [ ] Select: **"Creative Commons Attribution 4.0 International"** (CC-BY-4.0)

**Why CC-BY-4.0?**
- Most permissive while requiring attribution
- Widely accepted in academia
- Compatible with Data in Brief requirements
- Allows commercial use, derivative works

**Alternative:** CC0 (public domain) if you want to waive all rights

**Time:** 2 minutes

---

## Step 6: Add Communities (Optional but Recommended)

Communities help discoverability. Search and add:

- [ ] **"Economics"** (if available)
- [ ] **"Latin America"** (if available)
- [ ] **"Open Data"** (if available)

**Note:** Community managers must approve inclusion, but deposit is published immediately regardless.

**Time:** 5 minutes

---

## Step 7: Subjects/Disciplines

- [ ] Select: **"Economics and Business"** → **"Macroeconomics"**
- [ ] Add: **"Economics and Business"** → **"Econometrics"** (if applicable)

**Time:** 2 minutes

---

## Step 8: Funding (Optional)

If your research was funded:

- [ ] Click **"Add grant"**
- [ ] Enter funder name and grant number
- [ ] Example: "Universidad del Pacífico Internal Research Grant #12345"

**Time:** 5 minutes (if applicable)

---

## Step 9: Related/Alternate Identifiers

Add links to related resources:

### Is compiled/created by (Code Repository)
- [ ] Identifier: `https://github.com/[yourusername]/peru_gdp_revisions`
- [ ] Relation: **"is compiled/created by"**
- [ ] Resource type: **"Software"**

### Is supplemented by (Documentation)
- [ ] Identifier: `https://github.com/[yourusername]/peru_gdp_revisions/blob/main/README.md`
- [ ] Relation: **"is supplemented by"**
- [ ] Resource type: **"Publication / Technical note"**

**Time:** 10 minutes

---

## Step 10: Contributors (Optional)

If others contributed but are not authors:

- [ ] Click **"Add contributor"**
- [ ] Enter name and role (e.g., "Data Curator", "Project Manager")

**Time:** 5 minutes (if applicable)

---

## Step 11: References (Optional)

Add key references:

```
Banco Central de Reserva del Perú (BCRP). Weekly Reports (Nota Semanal). Available at: https://www.bcrp.gob.pe/publicaciones/nota-semanal.html
```

**Time:** 5 minutes

---

## Step 12: Final Review

### Pre-Publication Checklist

- [ ] All 17 files uploaded (16 CSVs + 1 README)
- [ ] Title correct and descriptive
- [ ] All authors listed with ORCID iDs
- [ ] Description is comprehensive (250+ words)
- [ ] Keywords added (7 keywords)
- [ ] License selected (CC-BY-4.0)
- [ ] Publication type = "Dataset"
- [ ] Version = 1.0.0
- [ ] Publication date set
- [ ] GitHub repository linked
- [ ] Description mentions Data in Brief compatibility
- [ ] No typos or errors

**Time:** 10 minutes

---

## Step 13: Publish!

### Before Clicking Publish:

⚠️ **IMPORTANT:** Once published, you **cannot delete** the record. You can only:
- Upload new versions (recommended for updates)
- Add metadata corrections

### Publish Process:

1. [ ] Scroll to bottom of form
2. [ ] Review the **"Preview"** section (shows how it will look)
3. [ ] Click green **"Publish"** button
4. [ ] Confirm publication in popup

### After Publishing:

1. **DOI is immediately assigned** (appears at top of page)
   - Format: `10.5281/zenodo.XXXXXXX`
   - Full URL: `https://doi.org/10.5281/zenodo.XXXXXXX`

2. **Copy your DOI** and save it securely

3. Download the **citation files** (BibTeX, JSON, etc.)

**Time:** 5 minutes

---

## Step 14: Post-Publication Actions

### Immediate Tasks:

1. [ ] **Copy DOI URL** → Save to text file
2. [ ] **Test DOI link** → Verify it resolves correctly
3. [ ] **Download citation** → Save BibTeX for reference
4. [ ] **Share the link** → Email to collaborators (if applicable)

### Update Project Files:

1. [ ] Update `CITATION.cff` with Zenodo DOI
2. [ ] Update `docs/DATA_AVAILABILITY.md` with Zenodo DOI
3. [ ] Update `README.md` with DOI badge
4. [ ] Update DIB template with Zenodo DOI
5. [ ] Commit changes to GitHub

**Time:** 15 minutes

---

## Troubleshooting

### Common Issues:

**"Upload failed"**
- Check file size (max 50 GB per file)
- Check internet connection
- Try uploading files in batches

**"ORCID not linking"**
- Manually enter ORCID in "Name identifier" field
- Format: `0000-0002-1234-5678` (find at https://orcid.org)

**"Can't find the right community"**
- Skip this step; not required for publication
- You can request community inclusion post-publication

**"Need to make changes after publishing"**
- Click "New version" to upload corrected version
- Original version remains accessible
- DOI updates to concept DOI (version-independent)

---

## After Obtaining DOI

### Next Steps:

1. ✅ **Task 2 Complete:** Upload datasets to Zenodo ✓
2. **Proceed to Task 3:** Create GitHub Release v1.0.0 with code DOI
3. **Then Task 4:** Complete DIB Article Template (using Zenodo DOI)

---

## Quick Reference: What You'll Need

### Information to Have Ready:

- Full name and affiliation
- ORCID iD
- GitHub repository URL
- Funding information (if applicable)
- Current date
- Brief description of dataset (250+ words)

### Files to Upload:

- 16 CSV files (~17 MB total)
- 1 README file (ZENODO_README.md)

### Estimated Total Time:

- **First-time users:** 2-3 hours
- **Experienced users:** 1 hour
- **File upload time:** 10-15 minutes (most of the time)

---

## Resources

- **Zenodo Help:** https://help.zenodo.org
- **Zenodo FAQs:** https://help.zenodo.org/faq/
- **Zenodo Support:** info@zenodo.org
- **License Chooser:** https://creativecommons.org/choose/

---

**Document Version:** 1.0
**Last Updated:** December 28, 2024
**Author:** Peru GDP RTD Project Team
