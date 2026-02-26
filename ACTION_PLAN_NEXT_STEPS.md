# Action Plan - Your Next Steps

**Created:** December 28, 2024
**Status:** Ready to Execute
**Total Time Needed:** ~5 hours over next 4 weeks

---

## 🎯 IMMEDIATE ACTIONS (You Can Do These NOW)

### ✅ Action 1: Get Your ORCID (10 minutes)

**Why:** Required for all submissions, used in Zenodo and DIB

**Steps:**
1. Open: `ORCID_SETUP_GUIDE.md`
2. Go to: https://orcid.org/register
3. Fill in:
   - Name: Jason Cruz
   - Email: jj.cruza@up.edu.pe
   - Password: *(create one)*
4. Verify email
5. **Copy your ORCID:** `0000-0002-XXXX-XXXX`
6. Save it somewhere safe!

**Output:** Your permanent ORCID ID

**Time:** 10 minutes

**Next:** Update CITATION.cff (Action 2)

---

### ✅ Action 2: Update CITATION.cff with ORCID (5 minutes)

**Why:** Makes your code properly citable

**Steps:**
1. Open: `CITATION_CFF_TEMPLATE.md` (for reference)
2. Edit: `CITATION.cff` in your project
3. Find line 12:
   ```yaml
   orcid: "https://orcid.org/0000-0000-0000-0000"  # TODO
   ```
4. Replace with your real ORCID:
   ```yaml
   orcid: "https://orcid.org/0000-0002-XXXX-XXXX"
   ```
5. Also update line 6 (date):
   ```yaml
   date-released: "2024-12-28"
   ```
6. Save file
7. Commit:
   ```bash
   git add CITATION.cff
   git commit -m "docs: add ORCID and update release date"
   git push
   ```

**Output:** Updated CITATION.cff

**Time:** 5 minutes

**Next:** Commit the new guides (Action 3)

---

### ✅ Action 3: Commit All Documentation (2 minutes)

**Why:** Save all the guides we created today

**Command:**
```bash
git add ORCID_SETUP_GUIDE.md CITATION_CFF_TEMPLATE.md ACTION_PLAN_NEXT_STEPS.md

git commit -m "docs: add ORCID setup guide and action plan"

git push origin main
```

**Output:** All guides saved to GitHub

**Time:** 2 minutes

**Next:** Zenodo upload (when ready)

---

## 📋 ACTIONS REQUIRING EXTERNAL WEBSITES (Do When Ready)

### 🌐 Action 4: Upload to Zenodo (2-3 hours)

**When:** When you have 2-3 uninterrupted hours

**Prerequisites:**
- ✅ ORCID obtained (from Action 1)
- ✅ Stable internet connection
- ✅ 2-3 hours available

**Steps:**
1. **Open:** `ZENODO_UPLOAD_GUIDE.md`
2. **Follow steps 1-14** carefully
3. **Upload:** 16 CSV files + ZENODO_README.md
4. **Fill metadata:** Use info from the guide
5. **Publish**
6. **CRITICAL:** Copy Data DOI immediately!
   - Format: `10.5281/zenodo.XXXXXXX`
   - Save in a text file!

**Output:**
- Data published on Zenodo
- Data DOI: `10.5281/zenodo.XXXXXXX`

**Time:** 2-3 hours (first time)

**Files to upload:**
```
From data/output/vintages/:
1. monthly_gdp_vintages.csv
2. quarterly_gdp_vintages.csv
3. monthly_gdp_vintages_adjusted.csv
4. quarterly_gdp_vintages_adjusted.csv
5. monthly_gdp_vintages_benchmark.csv
6. quarterly_gdp_vintages_benchmark.csv
7. monthly_gdp_vintages_adjusted_benchmark.csv
8. quarterly_gdp_vintages_adjusted_benchmark.csv

From data/output/releases/:
9. monthly_gdp_releases.csv
10. quarterly_gdp_releases.csv
11. monthly_gdp_releases_adjusted.csv
12. quarterly_gdp_releases_adjusted.csv
13. monthly_gdp_releases_benchmark.csv
14. quarterly_gdp_releases_benchmark.csv
15. monthly_gdp_releases_adjusted_benchmark.csv
16. quarterly_gdp_releases_adjusted_benchmark.csv

Plus:
17. ZENODO_README.md (rename to README.md)
```

**Next:** GitHub release (Action 5)

---

### 🌐 Action 5: Create GitHub Release (1 hour)

**When:** Right after Zenodo upload (same day if possible)

**Prerequisites:**
- ✅ Zenodo account created (from Action 4)
- ✅ All code committed and pushed

**Steps:**
1. **Open:** `GITHUB_RELEASE_GUIDE.md`
2. **Follow steps 1-8** carefully
3. **Enable Zenodo-GitHub integration**
4. **Create release:** Tag v1.0.0
5. **Wait:** 10-30 minutes for Zenodo DOI
6. **CRITICAL:** Copy Code DOI immediately!
   - Format: `10.5281/zenodo.YYYYYYY`
   - Save in a text file!

**Output:**
- GitHub release v1.0.0 created
- Code DOI: `10.5281/zenodo.YYYYYYY`

**Time:** 1 hour

**Next:** Update all docs with DOIs (Action 6)

---

### 📝 Action 6: Update Files with DOIs (30 minutes)

**When:** Immediately after Actions 4 & 5

**Prerequisites:**
- ✅ Data DOI from Zenodo
- ✅ Code DOI from GitHub release
- ✅ ORCID from Action 1

**Files to Update:**

#### 1. CITATION.cff (add data DOI reference)
Open `CITATION_CFF_TEMPLATE.md` for the exact code to add.

Add after line 28:
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
    doi: "10.5281/zenodo.XXXXXXX"  # Your data DOI
    url: "https://doi.org/10.5281/zenodo.XXXXXXX"
    license: "CC-BY-4.0"
```

#### 2. README.md (add DOI badges)
Add at top of README:
```markdown
[![Data DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.XXXXXXX.svg)](https://doi.org/10.5281/zenodo.XXXXXXX)
[![Code DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.YYYYYYY.svg)](https://doi.org/10.5281/zenodo.YYYYYYY)
```

#### 3. docs/DATA_AVAILABILITY.md
Replace "To be assigned" with:
```markdown
**Data DOI:** https://doi.org/10.5281/zenodo.XXXXXXX
**Code DOI:** https://doi.org/10.5281/zenodo.YYYYYYY
```

#### 4. DIB_MANUSCRIPT_DRAFT.md
Search and replace:
- `[DATA_DOI]` → `10.5281/zenodo.XXXXXXX`
- `[CODE_DOI]` → `10.5281/zenodo.YYYYYYY`
- `[YOUR_ORCID_ID]` → `0000-0002-XXXX-XXXX`
- `[YOUR_FULL_NAME]` → `Jason Cruz`
- `[YOUR_EMAIL]` → `jj.cruza@up.edu.pe`
- `[YOUR_INSTITUTION]` → `Universidad del Pacífico`
- `[YOUR_GITHUB_USERNAME]` → `JasonCruz18`

**Commit:**
```bash
git add CITATION.cff README.md docs/DATA_AVAILABILITY.md DIB_MANUSCRIPT_DRAFT.md
git commit -m "docs: add DOIs and complete author information"
git push
```

**Output:** All documentation updated with permanent identifiers

**Time:** 30 minutes

**Next:** Finalize manuscript (Action 7)

---

### 📄 Action 7: Finalize DIB Manuscript (1 hour)

**When:** After all DOIs obtained (Actions 4-6 complete)

**Steps:**

1. **Open:** `DIB_MANUSCRIPT_DRAFT.md`
2. **Verify:** All `[PLACEHOLDER]` values replaced
3. **Copy content** into Word template:
   - Open: `DIB/data-in-brief-article-template.docx`
   - Paste sections from draft
   - Format according to template styles
4. **Add title page:**
   - Title: "Peru GDP Real-Time Dataset (1994-present)"
   - Author: Jason Cruz
   - Affiliation: Universidad del Pacífico - CIUP
   - Email: jj.cruza@up.edu.pe
   - ORCID: Your ORCID
5. **Check Specifications Table:**
   - Data DOI correct?
   - Code DOI correct?
   - All URLs work?
6. **Spell-check** and proofread
7. **Save:** `Peru_GDP_RTD_DIB_Manuscript.docx`

**Output:** Completed DIB manuscript in Word format

**Time:** 1 hour

**Next:** Submit (Action 8)

---

### 🚀 Action 8: Submit to Data in Brief (30 minutes)

**When:** January 20-26, 2025 (or when manuscript ready)

**Prerequisites:**
- ✅ All DOIs obtained
- ✅ Manuscript finalized
- ✅ All links tested

**Steps:**

1. **Go to:** https://www.editorialmanager.com/dib/default.aspx
2. **Create account** or sign in
3. **Click:** "Submit New Manuscript"
4. **Article type:** Data Article
5. **Upload:** Your Word manuscript
6. **Fill form:**
   - Title
   - Abstract (copy from manuscript)
   - Keywords (from manuscript)
   - Authors (you + ORCID)
   - Data repository link (Zenodo URL)
   - Code repository link (GitHub URL)
7. **Upload files:**
   - Manuscript (.docx)
   - Declaration of Competing Interest (include in manuscript)
   - Cover letter (optional but recommended)
8. **Review** everything
9. **Submit!** 🎉
10. **Save tracking number**

**Output:**
- Manuscript submitted
- Tracking number received

**Time:** 30 minutes

**Expected:** Desk review within 3-5 days

---

## 📅 RECOMMENDED TIMELINE

### Week 1 (Dec 29 - Jan 5)

**Sunday, Dec 29** (TODAY or tomorrow):
- ✅ Action 1: Get ORCID (10 min)
- ✅ Action 2: Update CITATION.cff (5 min)
- ✅ Action 3: Commit guides (2 min)

**Monday, Dec 30**:
- ✅ Action 4: Zenodo upload (2-3 hours) ← BIG ONE

**Tuesday, Dec 31**:
- ✅ Action 5: GitHub release (1 hour)
- ✅ Action 6: Update docs with DOIs (30 min)

**Thursday, Jan 2-3** (after New Year):
- Review everything
- Test all DOI links
- Buffer time

### Week 2-3 (Jan 6-19)

**Week of Jan 6**:
- ✅ Action 7: Finalize manuscript (1 hour)
- Internal review and polish

**Week of Jan 13**:
- Final proofreading
- Prepare cover letter
- Test all links again

### Week 4 (Jan 20-26)

**Monday, Jan 20**:
- Final review

**Friday, Jan 24-26**:
- ✅ Action 8: Submit to DIB! 🚀

**Target Submission:** January 26, 2025

---

## ✅ COMPLETION CHECKLIST

### Phase 1: Setup (TODAY)
- [ ] Get ORCID (10 min)
- [ ] Update CITATION.cff with ORCID (5 min)
- [ ] Commit all new guides (2 min)
- [ ] **Total:** ~20 minutes

### Phase 2: DOIs (This Week)
- [ ] Upload data to Zenodo (2-3 hours)
- [ ] Create GitHub Release (1 hour)
- [ ] Obtain Data DOI
- [ ] Obtain Code DOI
- [ ] **Total:** ~3-4 hours

### Phase 3: Documentation (Next Week)
- [ ] Update CITATION.cff with data DOI (10 min)
- [ ] Update README.md with badges (5 min)
- [ ] Update DATA_AVAILABILITY.md (5 min)
- [ ] Update DIB_MANUSCRIPT_DRAFT.md (10 min)
- [ ] Commit all changes
- [ ] **Total:** ~30 minutes

### Phase 4: Manuscript (Week 2)
- [ ] Finalize manuscript in Word (1 hour)
- [ ] Proofread and spell-check (30 min)
- [ ] Test all DOI links (10 min)
- [ ] Prepare cover letter (20 min)
- [ ] **Total:** ~2 hours

### Phase 5: Submission (Week 3-4)
- [ ] Create DIB account (5 min)
- [ ] Submit manuscript (25 min)
- [ ] **Total:** ~30 minutes

---

## 💡 TIPS FOR SUCCESS

### For ORCID:
✅ Use your institutional email (jj.cruza@up.edu.pe)
✅ Set privacy to "Everyone" can see
✅ Add your affiliation (Universidad del Pacífico)
✅ Save your ORCID in multiple places!

### For Zenodo:
✅ Read the entire guide before starting
✅ Use "Sign in with ORCID" option
✅ Write rich description (250+ words)
✅ Test DOI link immediately after publish
✅ Download citation (BibTeX) for backup

### For GitHub Release:
✅ Enable Zenodo integration FIRST
✅ Wait 10-30 min for DOI assignment
✅ Use comprehensive release notes
✅ Tag as v1.0.0 (semantic versioning)

### For DIB Submission:
✅ Test all DOI links before submitting
✅ Spell-check everything
✅ Keep tracking number safe
✅ Respond promptly to editor emails

---

## 🆘 IF YOU GET STUCK

### Zenodo Issues:
- **Guide:** ZENODO_UPLOAD_GUIDE.md (page 13-14: Troubleshooting)
- **Email:** info@zenodo.org
- **Expected response:** 24-48 hours

### GitHub Issues:
- **Guide:** GITHUB_RELEASE_GUIDE.md (page 11-12: Troubleshooting)
- **Docs:** https://docs.github.com
- **Community:** https://github.community

### ORCID Issues:
- **Guide:** ORCID_SETUP_GUIDE.md (page 5: Troubleshooting)
- **Email:** support@orcid.org

### DIB Issues:
- **Email:** dib-me@elsevier.com
- **Support:** https://service.elsevier.com

---

## 🎯 SUCCESS METRICS

**After completing all actions:**

✅ **ORCID registered** - Permanent researcher ID
✅ **Data on Zenodo** - With permanent DOI
✅ **Code on GitHub** - With release and DOI
✅ **All docs updated** - DOIs everywhere
✅ **Manuscript ready** - Formatted in Word
✅ **Submitted to DIB** - Tracking number received

**Expected outcome:** Acceptance in 4-6 weeks! 🎉

---

## 📊 PROGRESS TRACKING

| Action | Status | Date Done | DOI/Output |
|--------|--------|-----------|------------|
| 1. Get ORCID | ⏳ Pending | ___ | ORCID: ____________ |
| 2. Update CITATION.cff | ⏳ Pending | ___ | ✅ File updated |
| 3. Commit guides | ⏳ Pending | ___ | ✅ Pushed to GitHub |
| 4. Zenodo upload | ⏳ Pending | ___ | Data DOI: __________ |
| 5. GitHub release | ⏳ Pending | ___ | Code DOI: __________ |
| 6. Update docs | ⏳ Pending | ___ | ✅ All files updated |
| 7. Finalize manuscript | ⏳ Pending | ___ | ✅ Word doc ready |
| 8. Submit to DIB | ⏳ Pending | ___ | Tracking #: ________ |

---

**Start Here:** Get your ORCID (Action 1) - Takes only 10 minutes!

**Document:** ORCID_SETUP_GUIDE.md

**You've got this!** 💪

---

**Created:** December 28, 2024
**Version:** 1.0
**Status:** Ready to execute
