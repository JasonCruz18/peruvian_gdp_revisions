# Data in Brief Submission Checklist

**Project:** Peru GDP Real-Time Dataset
**Target Journal:** Data in Brief (Elsevier)
**Submission Goal:** January 26, 2025
**Current Status:** In Progress

---

## Overall Progress: 30% Complete

- [x] Project exploration and assessment
- [x] DIB journal fit assessment (Result: **EXCELLENT FIT - 9.5/10**)
- [x] Dataset CSV files generated (16 files)
- [x] Zenodo upload guide created
- [x] GitHub release guide created
- [x] Zenodo README created
- [ ] Zenodo data upload completed
- [ ] GitHub release created
- [ ] DIB template completed
- [ ] ORCID registered/verified
- [ ] Data dictionary created
- [ ] Documentation updated with DOIs
- [ ] Manuscript submitted

---

## CRITICAL TASKS (Must Complete)

### 🔴 Task 1: Upload Datasets to Zenodo [IN PROGRESS - 80% DONE]

**Status:** Preparation complete, upload pending
**Estimated Time Remaining:** 2 hours
**Priority:** CRITICAL

#### Completed:
- [x] Generate CSV versions of vintage files (8 files)
- [x] Verify all 16 CSV files exist
- [x] Create ZENODO_README.md
- [x] Create ZENODO_UPLOAD_GUIDE.md

#### Remaining Steps:
- [ ] **Create Zenodo account** (if needed) - 5 min
- [ ] **Start new upload** - 2 min
- [ ] **Upload 16 CSV files + README** - 15 min
  - [ ] 8 vintage files (2.9 MB × 4 + 1.3 MB × 4)
  - [ ] 8 releases files (192-219 KB each)
  - [ ] ZENODO_README.md
- [ ] **Fill basic information** - 30 min
  - [ ] Title: "Peru GDP Real-Time Dataset (1994-present)"
  - [ ] Authors with ORCID
  - [ ] Description (250+ words)
  - [ ] Keywords (7 keywords)
  - [ ] Version: 1.0.0
- [ ] **Select license:** CC-BY-4.0 - 2 min
- [ ] **Add subjects:** Economics > Macroeconomics - 5 min
- [ ] **Add GitHub link** as "is compiled/created by" - 10 min
- [ ] **Final review** - 10 min
- [ ] **Publish and obtain DOI** - 5 min
- [ ] **Copy DOI and save:** `10.5281/zenodo.XXXXXXX`

**Guide:** See [ZENODO_UPLOAD_GUIDE.md](ZENODO_UPLOAD_GUIDE.md)

**Output:** Data DOI (10.5281/zenodo.XXXXXXX)

---

### 🔴 Task 2: Create GitHub Release v1.0.0 [NOT STARTED]

**Status:** Ready to start (guides created)
**Estimated Time:** 1-2 hours
**Priority:** CRITICAL
**Dependencies:** None (can start now)

#### Steps:
- [ ] **Enable Zenodo-GitHub integration** - 10 min
  - Log in to Zenodo
  - Link GitHub account
  - Toggle on peru_gdp_revisions repository
- [ ] **Review RELEASE_NOTES_v1.0.0.md** - 10 min
- [ ] **Create git tag:** `v1.0.0` - 5 min
  ```bash
  git tag -a v1.0.0 -m "Release v1.0.0 - Initial Public Release"
  git push origin v1.0.0
  ```
- [ ] **Create GitHub release** - 20 min
  - Go to Releases → Draft new release
  - Tag: v1.0.0
  - Title: "Peru GDP RTD v1.0.0 - Initial Public Release"
  - Description: Use RELEASE_NOTES_v1.0.0.md content
  - Publish release
- [ ] **Wait for Zenodo DOI** - 10-15 min
- [ ] **Retrieve code DOI from Zenodo** - 5 min
- [ ] **Copy DOI:** `10.5281/zenodo.YYYYYYY`

**Guide:** See [GITHUB_RELEASE_GUIDE.md](GITHUB_RELEASE_GUIDE.md)

**Output:** Code DOI (10.5281/zenodo.YYYYYYY)

---

### 🔴 Task 3: Complete DIB Article Template [NOT STARTED]

**Status:** Awaiting DOIs from Tasks 1-2
**Estimated Time:** 6-8 hours
**Priority:** CRITICAL
**Dependencies:** Tasks 1-2 (need both DOIs)

#### Sections to Complete:

##### **Specifications Table** - 30 min
- [ ] Subject area: Economics / Macroeconomics
- [ ] Specific subject area: Real-Time Macroeconomic Data, GDP Revisions
- [ ] Type of data: Tables (CSV)
- [ ] Data collection method: Web scraping, PDF extraction, systematic cleaning
- [ ] Data format: Raw and processed
- [ ] Data source location: Peru (BCRP)
- [ ] Data accessibility:
  - Repository: Zenodo
  - Data DOI: [INSERT from Task 1]
  - Code DOI: [INSERT from Task 2]
- [ ] Related research article: [Optional - your forthcoming paper]

##### **Value of the Data** - 1-2 hours
- [ ] Why data are valuable (5 bullet points)
- [ ] Who can benefit (researchers, policymakers, students)
- [ ] How data can be used (revision analysis, nowcasting, etc.)
- [ ] What makes it unique

##### **Data Description** - 2-3 hours
- [ ] Overview of dataset structure
- [ ] Description of 16 CSV files
- [ ] Vintage format vs Releases format explanation
- [ ] Coverage details (time, sectors, frequency)
- [ ] Sample data snippets or tables
- [ ] Reference to figures (if creating any)

##### **Experimental Design, Materials, and Methods** - 2-3 hours
- [ ] Describe 6-stage pipeline
- [ ] Data sources (BCRP Weekly Reports)
- [ ] PDF processing methodology
- [ ] Cleaning procedures (reference 70+ functions)
- [ ] Vintage construction process
- [ ] Base-year adjustment methodology
- [ ] Quality validation procedures
- [ ] Software and tools used
- [ ] Reference _Supplement.tex for technical details

##### **Ethics Statement** - 5 min
- [ ] "This research uses publicly available data from Banco Central de Reserva del Perú. No ethical approval was required."

##### **CRediT Author Statement** - 10 min
- [ ] Conceptualization: [Your Name]
- [ ] Data curation: [Your Name]
- [ ] Formal analysis: [Your Name]
- [ ] Methodology: [Your Name]
- [ ] Software: [Your Name]
- [ ] Writing - original draft: [Your Name]

##### **Declaration of Competing Interest** - 5 min
- [ ] "The authors declare that they have no known competing financial interests or personal relationships that could have appeared to influence the work reported in this paper."

##### **Acknowledgments** - 10 min
- [ ] Acknowledge BCRP for data
- [ ] Acknowledge institution
- [ ] Optional: Funding acknowledgments

##### **References** - 30 min
- [ ] BCRP Weekly Reports URL
- [ ] Data repository (Zenodo)
- [ ] Code repository (GitHub)
- [ ] Related software/methods papers (if applicable)

**Template:** See [DIB/data-in-brief-article-template.docx](DIB/data-in-brief-article-template.docx)

**Output:** Completed DIB manuscript (.docx)

---

## HIGH PRIORITY TASKS

### 🟡 Task 4: Register ORCID and Update CITATION.cff [NOT STARTED]

**Status:** Quick task
**Estimated Time:** 10-15 minutes
**Priority:** HIGH

#### Steps:
- [ ] **Check if you have ORCID already** - 1 min
  - Go to https://orcid.org
  - Try to sign in
- [ ] **If no ORCID, register** - 5 min
  - Sign up at https://orcid.org/register
  - Free account
  - Use institutional email
- [ ] **Copy your ORCID:** `0000-0002-XXXX-XXXX` format
- [ ] **Update CITATION.cff** - 5 min
  - Replace placeholder: `0000-0000-0000-0000`
  - Add your actual ORCID
  - Add data DOI (from Task 1)
- [ ] **Commit changes:**
  ```bash
  git add CITATION.cff
  git commit -m "docs: update ORCID and data DOI"
  git push
  ```

**Output:** Valid CITATION.cff with real ORCID

---

### 🟡 Task 5: Create Data Dictionary [NOT STARTED]

**Status:** Ready to start
**Estimated Time:** 2-3 hours
**Priority:** HIGH

#### Content to Document:

##### **Column Definitions**
- [ ] Vintage format index: `period` (format examples)
- [ ] Vintage format columns: Release dates (format: YYYY-MM-DD)
- [ ] Releases format index: `target_period`
- [ ] Releases format columns: `_1`, `_2`, `_3` (revision sequences)

##### **Industry Code Mappings**
- [ ] All 8 sectors (English ↔ Spanish)
- [ ] Code names used in datasets
- [ ] Sector aggregations

##### **Special Values**
- [ ] Sentinel value: `-999999.0`
  - When it appears
  - What it means
  - Which files contain it
- [ ] Missing values: `NaN`
  - Why they occur
  - Normal in real-time data

##### **Period Notation**
- [ ] Monthly: `2020m1` = January 2020
- [ ] Quarterly: `2020q1` = Q1 2020
- [ ] Annual: `2020` = Year 2020

##### **File Naming Conventions**
- [ ] `by_adjusted_` prefix meaning
- [ ] `_benchmark` suffix meaning
- [ ] `_releases` suffix meaning
- [ ] Vintage vs Releases format distinction

##### **Base-Year Changes**
- [ ] 1990 base year: until 1999
- [ ] 1994 base year: 2000-2013
- [ ] 2007 base year: 2014-present
- [ ] Affected vintages and how they're flagged

**File:** Create `docs/DATA_DICTIONARY.md`

**Output:** Comprehensive data dictionary

---

## MEDIUM PRIORITY TASKS

### 🟢 Task 6: Prepare Graphical Abstract [OPTIONAL]

**Status:** Not started (optional but recommended)
**Estimated Time:** 2-4 hours
**Priority:** MEDIUM

#### Requirements (from DIB guide):
- [ ] Minimum 531 x 1328 pixels (h × w)
- [ ] File type: TIFF, EPS, PDF, or MS Office
- [ ] Concise, pictorial, professional
- [ ] Summarizes data article visually

#### Suggested Content:
- [ ] Flow diagram showing pipeline stages:
  ```
  BCRP PDFs → Scraping → Cleaning → Vintages → RTD (Vintage Format)
                                             ↓
                                      RTD (Releases Format)
  ```
- [ ] Include: Data coverage stats, file counts, key features

#### Tools:
- **Option A:** Python (matplotlib/seaborn) - programmatic
- **Option B:** PowerPoint/Keynote - manual but flexible
- **Option C:** draw.io / Lucidchart - professional diagrams

**Output:** Graphical abstract image file

---

### 🟢 Task 7: Update Documentation with DOIs [BLOCKED]

**Status:** Waiting for DOIs from Tasks 1-2
**Estimated Time:** 30 minutes
**Priority:** MEDIUM
**Dependencies:** Tasks 1-2 completed

#### Files to Update:

##### **README.md**
- [ ] Add DOI badges at top:
  ```markdown
  [![Data DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.XXXXXXX.svg)](https://doi.org/10.5281/zenodo.XXXXXXX)
  [![Code DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.YYYYYYY.svg)](https://doi.org/10.5281/zenodo.YYYYYYY)
  ```
- [ ] Update citation section with real DOIs

##### **docs/DATA_AVAILABILITY.md**
- [ ] Replace "To be assigned" with actual DOIs
- [ ] Update data repository URL
- [ ] Update code repository DOI

##### **CITATION.cff** (if not done in Task 4)
- [ ] Add data DOI to references section
- [ ] Verify all metadata correct

##### **_Supplement.tex**
- [ ] Add DOIs in references/bibliography
- [ ] Update data availability statement

##### **ZENODO_README.md** (for data upload)
- [ ] Add final data DOI
- [ ] Add code repository DOI

**Commit:**
```bash
git add README.md docs/DATA_AVAILABILITY.md CITATION.cff _Supplement.tex
git commit -m "docs: add Zenodo DOIs throughout documentation"
git push
```

**Output:** All documentation updated with persistent identifiers

---

## SUBMISSION TASKS

### 📤 Task 8: Submit to Data in Brief [BLOCKED]

**Status:** Waiting for all critical tasks
**Estimated Time:** 1 hour
**Priority:** FINAL STEP
**Dependencies:** Tasks 1-5 completed

#### Pre-Submission Checklist:

##### **Manuscript Ready:**
- [ ] DIB template fully completed
- [ ] All sections filled (no TBD or placeholders)
- [ ] Both DOIs included (data + code)
- [ ] References formatted correctly
- [ ] Word count appropriate
- [ ] Spell-checked and proofread

##### **Data Ready:**
- [ ] Data on Zenodo with DOI
- [ ] Data DOI resolves correctly
- [ ] README comprehensive
- [ ] License appropriate (CC-BY-4.0)

##### **Code Ready:**
- [ ] Code on GitHub
- [ ] GitHub release created (v1.0.0)
- [ ] Code DOI assigned
- [ ] Documentation complete

##### **Supporting Materials:**
- [ ] Cover letter drafted (optional)
- [ ] Highlights prepared (3-5 bullet points)
- [ ] Graphical abstract (if created)
- [ ] All author information confirmed
- [ ] Corresponding author email valid

#### Submission Process:

1. [ ] Go to Data in Brief submission system
   - URL: https://www.editorialmanager.com/dib/default.aspx
2. [ ] Create account or log in
3. [ ] Click "Submit New Manuscript"
4. [ ] Select article type: **"Data Article"**
5. [ ] Upload manuscript (.docx)
6. [ ] Upload graphical abstract (if created)
7. [ ] Fill submission form:
   - [ ] Title
   - [ ] Abstract
   - [ ] Keywords
   - [ ] Authors with ORCIDs
   - [ ] Data repository link (Zenodo)
   - [ ] Code repository link (GitHub)
8. [ ] Upload cover letter (optional)
9. [ ] Suggest reviewers (optional, usually helpful)
10. [ ] Review and submit

**Output:** Manuscript submitted, tracking number received

---

## TIMELINE SUMMARY

### Week 1: Data & Code DOIs (Dec 29 - Jan 5)
- **Days 1-2:** Upload to Zenodo → Data DOI ✅
- **Day 3:** Create GitHub Release → Code DOI ✅
- **Day 4-5:** ORCID + CITATION.cff ✅
- **Day 6-7:** Start data dictionary ✅

### Week 2-3: Manuscript (Jan 6 - Jan 19)
- **Days 1-2:** Complete data dictionary
- **Days 3-5:** DIB template - Specs, Value, Data Description
- **Days 6-8:** DIB template - Methods, Ethics, References
- **Days 9-10:** Internal review and revisions
- **Day 11:** (Optional) Graphical abstract

### Week 4: Submission (Jan 20 - Jan 26)
- **Day 1:** Update all docs with DOIs
- **Day 2:** Prepare cover letter
- **Day 3:** Final proofreading
- **Day 4:** Test all links and DOIs
- **Day 5:** Buffer day (catch-up)
- **Day 6:** **SUBMIT** ✅

**Target Submission Date:** January 26, 2025

---

## FILES CREATED TODAY

Ready to use:

1. ✅ **ZENODO_README.md** - Comprehensive README for data deposit
2. ✅ **ZENODO_UPLOAD_GUIDE.md** - Step-by-step Zenodo instructions
3. ✅ **GITHUB_RELEASE_GUIDE.md** - GitHub release and DOI guide
4. ✅ **scripts/export_vintages_to_csv.py** - CSV conversion script
5. ✅ **16 CSV files** in data/output/ (vintages + releases)
6. ✅ **DIB_SUBMISSION_CHECKLIST.md** (this file)

---

## IMMEDIATE NEXT STEPS

**Today (December 28):**
1. 🔴 **Upload to Zenodo** → Follow ZENODO_UPLOAD_GUIDE.md
2. 🔴 **Create GitHub Release** → Follow GITHUB_RELEASE_GUIDE.md

**Tomorrow (December 29):**
3. 🟡 **Register/verify ORCID** → Update CITATION.cff
4. 🟡 **Start data dictionary** → Create docs/DATA_DICTIONARY.md

**This Week:**
5. 🔴 **Begin DIB template** → Focus on Specifications Table and Value sections

---

## QUESTIONS & ANSWERS

**Q: Can I start Task 3 (DIB template) before Tasks 1-2?**
A: Yes, partially! You can draft most sections, but will need DOIs for:
- Specifications Table (Data Accessibility section)
- References section
- Final submission

**Q: Do I need ORCID before Zenodo upload?**
A: No, but it's helpful. Zenodo can link ORCID during upload if you sign in with ORCID.

**Q: How long after GitHub release until Zenodo DOI?**
A: Typically 10-15 minutes, can be up to 30 minutes during high traffic.

**Q: Can I update files after publishing on Zenodo?**
A: Yes, by creating a "New version". Original version remains accessible.

**Q: What if I find an error after DIB submission?**
A: Can upload corrected version to Zenodo (new version), update manuscript during revisions.

---

## RESOURCES

### Guides Created:
- [ZENODO_UPLOAD_GUIDE.md](ZENODO_UPLOAD_GUIDE.md) - Zenodo step-by-step
- [GITHUB_RELEASE_GUIDE.md](GITHUB_RELEASE_GUIDE.md) - GitHub release instructions
- [ZENODO_README.md](ZENODO_README.md) - Data deposit README

### DIB Documentation:
- [DIB/guide_for_authors.pdf](DIB/guide_for_authors.pdf) - Complete submission guide
- [DIB/FAQ.txt](DIB/FAQ.txt) - Journal FAQ
- [DIB/Policies and Guidelines.txt](DIB/Policies and Guidelines.txt) - Scope and requirements
- [DIB/data-in-brief-article-template.docx](DIB/data-in-brief-article-template.docx) - Template

### External Resources:
- **Zenodo:** https://zenodo.org
- **ORCID:** https://orcid.org
- **GitHub Docs:** https://docs.github.com/en/repositories/releasing-projects-on-github
- **DIB Journal:** https://www.journals.elsevier.com/data-in-brief

---

**Checklist Version:** 1.0
**Last Updated:** December 28, 2024
**Next Review:** After Tasks 1-2 completed
