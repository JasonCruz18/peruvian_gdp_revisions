# CITATION.cff Update Template

**Purpose:** Template for updating CITATION.cff after obtaining ORCID and DOIs

**When to use:** After you have:
1. ✅ Your ORCID (from ORCID_SETUP_GUIDE.md)
2. ✅ Data DOI (from Zenodo data upload)
3. ✅ Code DOI (from GitHub release)

---

## Current CITATION.cff Issues to Fix

### Issue 1: ORCID Placeholder (Line 12)
**Current:**
```yaml
orcid: "https://orcid.org/0000-0000-0000-0000"  # TODO: Add your ORCID
```

**Replace with:**
```yaml
orcid: "https://orcid.org/0000-0002-XXXX-XXXX"  # Your real ORCID
```

### Issue 2: Missing Data DOI Reference
**Current:** No reference to the Zenodo data deposit

**Add this section after line 28 (before `preferred-citation`):**
```yaml
references:
  - type: dataset
    title: "Peru GDP Real-Time Dataset (1994-present)"
    authors:
      - family-names: "Cruz"
        given-names: "Jason"
        orcid: "https://orcid.org/0000-0002-XXXX-XXXX"
    year: 2024
    publisher: "Zenodo"
    doi: "10.5281/zenodo.XXXXXXX"  # Data DOI from Zenodo
    url: "https://doi.org/10.5281/zenodo.XXXXXXX"
    license: "CC-BY-4.0"
```

### Issue 3: Release Date (Line 6)
**Current:**
```yaml
date-released: "2025-12-15"
```

**Update to actual release date:**
```yaml
date-released: "2024-12-28"  # or your actual release date
```

---

## Complete Updated CITATION.cff

Here's the full file with all updates:

```yaml
cff-version: 1.2.0
message: "If you use this software or dataset, please cite it as below."
type: software
title: "Peru GDP Real-Time Dataset Construction Pipeline"
version: "1.0.0"
date-released: "2024-12-28"  # UPDATED: Actual release date
authors:
  - family-names: "Cruz"
    given-names: "Jason"
    email: "jj.cruza@up.edu.pe"
    affiliation: "Universidad del Pacífico - CIUP"
    orcid: "https://orcid.org/0000-0002-XXXX-XXXX"  # UPDATED: Your real ORCID
repository-code: "https://github.com/JasonCruz18/peru_gdp_revisions"
url: "https://github.com/JasonCruz18/peru_gdp_revisions"
abstract: >-
  Production-ready pipeline for constructing real-time datasets (RTD) of
  Peruvian GDP revisions from BCRP Weekly Reports. Features automated web
  scraping, PDF processing, comprehensive data cleaning (70+ functions),
  and transformation to multiple dataset formats. Includes interactive
  dashboard for visualization and exploration.
keywords:
  - GDP revisions
  - Real-time data
  - Peru
  - Economic statistics
  - Data pipeline
  - Nowcasting
license: MIT

# NEW SECTION: Reference to the data deposit
references:
  - type: dataset
    title: "Peru GDP Real-Time Dataset (1994-present)"
    authors:
      - family-names: "Cruz"
        given-names: "Jason"
        orcid: "https://orcid.org/0000-0002-XXXX-XXXX"  # UPDATED: Your ORCID
    year: 2024
    publisher: "Zenodo"
    doi: "10.5281/zenodo.XXXXXXX"  # UPDATED: Data DOI from Zenodo
    url: "https://doi.org/10.5281/zenodo.XXXXXXX"
    license: "CC-BY-4.0"

preferred-citation:
  type: article
  title: "Rationality and Nowcasting on Peruvian GDP Revisions"
  authors:
    - family-names: "Cruz"
      given-names: "Jason"
      orcid: "https://orcid.org/0000-0002-XXXX-XXXX"  # UPDATED: Your ORCID
  year: 2025
  journal: "TBD"  # TODO: Update when paper is accepted
  institution: "Universidad del Pacífico - CIUP"
```

---

## How to Update CITATION.cff

### Option 1: Manual Edit (Recommended)

1. **Open CITATION.cff in your text editor**
2. **Find and replace:**
   - Line 6: Update date to `2024-12-28` (or actual date)
   - Line 12: Replace `0000-0000-0000-0000` with your ORCID
   - After line 28: Add the `references:` section (copy from template above)
   - In references section: Add your ORCID again
   - In references section: Add Data DOI from Zenodo
   - In preferred-citation: Add your ORCID
3. **Save the file**
4. **Test validity:** Go to https://citation-file-format.github.io/cff-initializer-javascript/
   - Paste your updated CITATION.cff
   - Check for errors
5. **Commit changes:**
   ```bash
   git add CITATION.cff
   git commit -m "docs: update CITATION.cff with ORCID and data DOI"
   git push
   ```

### Option 2: Use Edit Tool (I can help)

Let me know when you have:
- ✅ Your ORCID
- ✅ Data DOI from Zenodo

And I'll update the file for you!

---

## Validation Checklist

Before committing, verify:

- [ ] **ORCID format correct:** Starts with `0000-`, has 4 groups of 4 digits
- [ ] **Data DOI format correct:** Starts with `10.5281/zenodo.`
- [ ] **Date format correct:** `YYYY-MM-DD`
- [ ] **All ORCIDs match:** Same ORCID in all 3 places
- [ ] **URLs correct:** DOI URLs resolve (test after Zenodo publish)
- [ ] **No syntax errors:** Test at https://citation-file-format.github.io/cff-initializer-javascript/

---

## When to Update CITATION.cff

### Update Timeline:

1. **Now (or soon):**
   - [x] Date released → `2024-12-28`
   - [ ] ORCID → Get from https://orcid.org/register
   - Commit: "docs: update release date and ORCID"

2. **After Zenodo upload:**
   - [ ] Add `references:` section with data DOI
   - [ ] Commit: "docs: add data DOI to CITATION.cff"

3. **After GitHub release:**
   - Already automatic! GitHub uses CITATION.cff for releases
   - Code DOI will reference this file

4. **After paper acceptance:**
   - [ ] Update `journal: "TBD"` with actual journal name
   - [ ] Commit: "docs: update journal name in CITATION.cff"

---

## Additional Files to Update (After Getting Info)

Once you have ORCID and DOIs, also update:

### 1. README.md
- Add DOI badges at top
- Update citation section

### 2. DIB_MANUSCRIPT_DRAFT.md
- Search for `[YOUR_ORCID_ID]` → Replace with ORCID
- Search for `[DATA_DOI]` → Replace with data DOI
- Search for `[CODE_DOI]` → Replace with code DOI

### 3. docs/DATA_AVAILABILITY.md
- Replace "To be assigned" with actual DOIs

### 4. ZENODO_README.md
- Search for `[Your ORCID ID]` → Replace
- DOI already has placeholder, will be filled by Zenodo

---

## Example with Real Values

**If your ORCID is:** `0000-0002-1825-0097`
**If your data DOI is:** `10.5281/zenodo.7654321`

**Then CITATION.cff line 12 becomes:**
```yaml
orcid: "https://orcid.org/0000-0002-1825-0097"
```

**And the references section becomes:**
```yaml
references:
  - type: dataset
    title: "Peru GDP Real-Time Dataset (1994-present)"
    authors:
      - family-names: "Cruz"
        given-names: "Jason"
        orcid: "https://orcid.org/0000-0002-1825-0097"
    year: 2024
    publisher: "Zenodo"
    doi: "10.5281/zenodo.7654321"
    url: "https://doi.org/10.5281/zenodo.7654321"
    license: "CC-BY-4.0"
```

---

## Testing Your Updated CITATION.cff

### Validator Tool:
https://citation-file-format.github.io/cff-initializer-javascript/

1. Copy your entire CITATION.cff content
2. Paste into the validator
3. Look for errors (red highlights)
4. Fix any issues
5. When green checkmark appears ✅ → You're good!

### GitHub's CFF Reader:
After committing, GitHub automatically:
- Reads CITATION.cff
- Shows "Cite this repository" button
- Generates citation in multiple formats

---

## Quick Command Reference

```bash
# After getting ORCID
git add CITATION.cff
git commit -m "docs: add ORCID to CITATION.cff"
git push

# After getting data DOI
git add CITATION.cff
git commit -m "docs: add data DOI reference to CITATION.cff"
git push

# Update multiple files at once
git add CITATION.cff README.md docs/DATA_AVAILABILITY.md
git commit -m "docs: update all files with ORCID and DOIs"
git push
```

---

**Status:** Template ready to use
**Next Actions:**
1. Get ORCID (5-10 min) → Use ORCID_SETUP_GUIDE.md
2. Upload to Zenodo (2 hours) → Use ZENODO_UPLOAD_GUIDE.md
3. Update this file with real values
4. Commit and push

---

**Last Updated:** December 28, 2024
**Version:** 1.0
