# DOI Update Checklist

**Purpose:** Track and execute all file updates after obtaining Data DOI and Code DOI

**When to use:** After completing Zenodo upload AND GitHub release

---

## Step 1: Collect Your DOIs

**IMPORTANT:** Fill these in before proceeding!

```
DATA DOI (from Zenodo data upload):
10.5281/zenodo._____________

CODE DOI (from GitHub release + Zenodo):
10.5281/zenodo._____________

ORCID (if obtained):
0000-0002-____-____
```

---

## Step 2: Update CITATION.cff

**File:** `CITATION.cff`

### Update 1: Add ORCID (if obtained)

**Find (line 12):**
```yaml
    orcid: "https://orcid.org/0000-0000-0000-0000"  # TODO: Add your ORCID
```

**Replace with:**
```yaml
    orcid: "https://orcid.org/0000-0002-____-____"  # Your real ORCID
```

### Update 2: Add Data DOI Reference

**Insert after line 28 (after `license: MIT`):**

```yaml
references:
  - type: dataset
    title: "Peru GDP Real-Time Dataset (1994-present)"
    authors:
      - family-names: "Cruz"
        given-names: "Jason"
        orcid: "https://orcid.org/0000-0002-____-____"  # Your ORCID
    year: 2024
    publisher: "Zenodo"
    doi: "10.5281/zenodo._____________"  # Your DATA DOI
    url: "https://doi.org/10.5281/zenodo._____________"
    license: "CC-BY-4.0"
```

### Update 3: Add ORCID to preferred-citation

**Find (line 33-35):**
```yaml
  authors:
    - family-names: "Cruz"
      given-names: "Jason"
```

**Replace with:**
```yaml
  authors:
    - family-names: "Cruz"
      given-names: "Jason"
      orcid: "https://orcid.org/0000-0002-____-____"  # Your ORCID
```

**Status:** [ ] CITATION.cff updated

---

## Step 3: Update README.md

**File:** `README.md`

### Add DOI Badges at Top

**Insert at line 1 (very top of file):**

```markdown
[![Data DOI](https://zenodo.org/badge/DOI/10.5281/zenodo._____________.svg)](https://doi.org/10.5281/zenodo._____________)
[![Code DOI](https://zenodo.org/badge/DOI/10.5281/zenodo._____________.svg)](https://doi.org/10.5281/zenodo._____________)

```

**Note:** Leave blank line after badges!

### Update Citation Section

**Find the "Citation" or "How to Cite" section and update BibTeX entries:**

```bibtex
@dataset{cruz2024peru_gdp_data,
  author = {Cruz, Jason},
  title = {Peru GDP Real-Time Dataset (1994-present)},
  year = {2024},
  publisher = {Zenodo},
  doi = {10.5281/zenodo._____________},  # DATA DOI
  url = {https://doi.org/10.5281/zenodo._____________}
}

@software{cruz2024peru_gdp_pipeline,
  author = {Cruz, Jason},
  title = {Peru GDP Real-Time Dataset Construction Pipeline},
  year = {2024},
  version = {1.0.0},
  publisher = {Zenodo},
  doi = {10.5281/zenodo._____________},  # CODE DOI
  url = {https://doi.org/10.5281/zenodo._____________}
}
```

**Status:** [ ] README.md updated

---

## Step 4: Update docs/DATA_AVAILABILITY.md

**File:** `docs/DATA_AVAILABILITY.md`

**Find:** Lines with "To be assigned upon publication"

**Replace with:**

```markdown
## Data Repository

All datasets are publicly available on Zenodo:

**Data DOI:** https://doi.org/10.5281/zenodo._____________

**Repository:** https://zenodo.org/record/_____________

## Code Repository

Complete source code is available on GitHub and archived on Zenodo:

**Code DOI:** https://doi.org/10.5281/zenodo._____________

**GitHub:** https://github.com/JasonCruz18/peru_gdp_revisions

**Zenodo Archive:** https://zenodo.org/record/_____________
```

**Status:** [ ] DATA_AVAILABILITY.md updated

---

## Step 5: Update DIB_MANUSCRIPT_DRAFT.md

**File:** `DIB_MANUSCRIPT_DRAFT.md`

### Multiple Search-and-Replace Operations:

**Operation 1: Replace [DATA_DOI]**
```
Find: [DATA_DOI]
Replace with: 10.5281/zenodo._____________
```
**Locations:** Lines ~42, ~60, ~250+

**Operation 2: Replace [CODE_DOI]**
```
Find: [CODE_DOI]
Replace with: 10.5281/zenodo._____________
```
**Locations:** Lines ~42, ~60, ~250+

**Operation 3: Replace [YOUR_ORCID_ID]**
```
Find: [YOUR_ORCID_ID]
Replace with: 0000-0002-____-____
```
**Locations:** Lines ~41, ~45

**Operation 4: Replace [YOUR_FULL_NAME]**
```
Find: [YOUR_FULL_NAME]
Replace with: Jason Cruz
```
**Locations:** Title page, line ~28

**Operation 5: Replace [YOUR_EMAIL]**
```
Find: [YOUR_EMAIL]
Replace with: jj.cruza@up.edu.pe
```
**Locations:** Line ~32

**Operation 6: Replace [YOUR_INSTITUTION]**
```
Find: [YOUR_INSTITUTION]
Replace with: Universidad del Pacífico
```
**Locations:** Line ~33

**Operation 7: Replace [YOUR_GITHUB_USERNAME]**
```
Find: [YOUR_GITHUB_USERNAME]
Replace with: JasonCruz18
```
**Locations:** Lines ~60, ~250+

**Status:** [ ] DIB_MANUSCRIPT_DRAFT.md updated

---

## Step 6: Update ZENODO_README.md

**File:** `ZENODO_README.md`

**Find (line ~236):**
```markdown
**Author ORCID:** [Your ORCID ID]
```

**Replace with:**
```markdown
**Author ORCID:** https://orcid.org/0000-0002-____-____
```

**Find citation section and update DOIs:**
```bibtex
doi = {10.5281/zenodo._____________},  # DATA DOI
```

**Status:** [ ] ZENODO_README.md updated

---

## Step 7: Update GITHUB_RELEASE_v1.0.0_NOTES.md

**File:** `GITHUB_RELEASE_v1.0.0_NOTES.md`

**Find:**
```markdown
**Data DOI:** [TO BE ADDED AFTER ZENODO UPLOAD]
**Code DOI:** Will be automatically assigned via Zenodo-GitHub integration
```

**Replace with:**
```markdown
**Data DOI:** https://doi.org/10.5281/zenodo._____________
**Code DOI:** https://doi.org/10.5281/zenodo._____________
```

**Find citation section and update:**
```bibtex
doi = {10.5281/zenodo._____________},  # DATA DOI
doi = {10.5281/zenodo._____________},  # CODE DOI
```

**Status:** [ ] GITHUB_RELEASE_v1.0.0_NOTES.md updated

---

## Step 8: Verify All URLs Work

**Test each DOI URL in browser:**

- [ ] https://doi.org/10.5281/zenodo._____________ (DATA) → loads Zenodo page
- [ ] https://doi.org/10.5281/zenodo._____________ (CODE) → loads Zenodo page
- [ ] https://zenodo.org/record/_____________ (DATA) → loads Zenodo page
- [ ] https://zenodo.org/record/_____________ (CODE) → loads Zenodo page
- [ ] https://orcid.org/0000-0002-____-____ → loads your ORCID profile

**All links working?** [ ] Yes / [ ] No

---

## Step 9: Commit All Changes

**After updating all files above:**

```bash
# Add all updated files
git add CITATION.cff README.md docs/DATA_AVAILABILITY.md
git add DIB_MANUSCRIPT_DRAFT.md ZENODO_README.md
git add GITHUB_RELEASE_v1.0.0_NOTES.md

# Commit with descriptive message
git commit -m "docs: update all files with Zenodo DOIs and ORCID

Added permanent identifiers to all documentation:
- Data DOI: 10.5281/zenodo._____________
- Code DOI: 10.5281/zenodo._____________
- ORCID: 0000-0002-____-____

Updated files:
- CITATION.cff (added data DOI reference + ORCID)
- README.md (added DOI badges)
- docs/DATA_AVAILABILITY.md
- DIB_MANUSCRIPT_DRAFT.md
- ZENODO_README.md
- GITHUB_RELEASE_v1.0.0_NOTES.md

All DOI links verified and working."

# Push to GitHub
git push origin main
```

**Status:** [ ] Changes committed and pushed

---

## Step 10: Final Verification Checklist

Before proceeding to manuscript finalization:

### File Updates Complete:
- [ ] CITATION.cff has data DOI reference
- [ ] CITATION.cff has ORCID (3 locations)
- [ ] README.md has DOI badges at top
- [ ] README.md has updated citations
- [ ] DATA_AVAILABILITY.md has both DOIs
- [ ] DIB_MANUSCRIPT_DRAFT.md has no [PLACEHOLDER] values
- [ ] ZENODO_README.md has ORCID
- [ ] GITHUB_RELEASE_v1.0.0_NOTES.md has both DOIs

### DOI Verification:
- [ ] Data DOI resolves correctly
- [ ] Code DOI resolves correctly
- [ ] Zenodo data page shows correct title
- [ ] Zenodo code page shows correct title
- [ ] ORCID profile is public and complete

### GitHub Status:
- [ ] All changes committed
- [ ] All changes pushed to origin/main
- [ ] GitHub shows updated files
- [ ] "Cite this repository" button works (from CITATION.cff)

### Ready for Next Step:
- [ ] All placeholders replaced
- [ ] All DOIs verified
- [ ] All files committed
- [ ] Ready to finalize manuscript in Word

---

## Quick Reference: Your Information

Fill this in once and use for all replacements:

```
Full Name:        Jason Cruz
Email:            jj.cruza@up.edu.pe
Institution:      Universidad del Pacífico
Department:       CIUP (Centro de Investigación)
GitHub Username:  JasonCruz18
GitHub Repo:      peru_gdp_revisions

ORCID:           0000-0002-____-____
Data DOI:        10.5281/zenodo._____________
Code DOI:        10.5281/zenodo._____________

Data URL:        https://doi.org/10.5281/zenodo._____________
Code URL:        https://doi.org/10.5281/zenodo._____________
ORCID URL:       https://orcid.org/0000-0002-____-____
```

---

## Automation Option

If you prefer, you can use find-and-replace in your editor:

**VS Code / Most Editors:**
1. Open "Find and Replace" (Ctrl+H or Cmd+H)
2. Enable "Replace in Files" mode
3. Use the search-replace pairs from this document
4. Preview changes before applying
5. Apply all replacements

**Command Line (Linux/Mac):**
```bash
# Replace DATA_DOI in all markdown files
sed -i 's/\[DATA_DOI\]/10.5281\/zenodo._____________/g' *.md docs/*.md

# Replace CODE_DOI in all markdown files
sed -i 's/\[CODE_DOI\]/10.5281\/zenodo._____________/g' *.md docs/*.md

# Replace ORCID
sed -i 's/\[YOUR_ORCID_ID\]/0000-0002-____-____/g' *.md docs/*.md
```

**Note:** Test on a single file first!

---

## Time Estimate

**Total time for all updates:** ~30 minutes

- Step 1 (Collect DOIs): 2 min
- Step 2 (CITATION.cff): 5 min
- Step 3 (README.md): 5 min
- Step 4 (DATA_AVAILABILITY.md): 3 min
- Step 5 (DIB_MANUSCRIPT_DRAFT.md): 8 min
- Step 6 (ZENODO_README.md): 2 min
- Step 7 (GITHUB_RELEASE notes): 2 min
- Step 8 (Verify URLs): 2 min
- Step 9 (Commit): 1 min
- Step 10 (Final check): 5 min

---

## What's Next?

After completing all updates in this checklist:

**Next Document:** DIB_MANUSCRIPT_DRAFT.md → Copy into Word template

**Next Action:** Finalize manuscript (see DIB_SUBMISSION_CHECKLIST.md, Step 7)

**Timeline:** Ready to submit within 1 hour after DOIs obtained!

---

**Created:** December 28, 2024
**Purpose:** Systematic DOI and ORCID update tracking
**Status:** Ready to use after Zenodo upload and GitHub release
