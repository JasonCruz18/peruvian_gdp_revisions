# DOI Assignment Guide - Zenodo Integration

Step-by-step guide to assign a DOI (Digital Object Identifier) to your Peru GDP RTD repository using Zenodo for academic citation and reproducibility.

---

## What is Zenodo?

**Zenodo** is a research data repository that:
- Provides permanent DOIs for code and datasets
- Is free and open-source
- Integrates with GitHub
- Is trusted by journals and funding agencies
- Ensures long-term preservation (minimum 20 years)

**Why you need a DOI:**
- Required for journal submission (data availability statements)
- Makes your work citable
- Ensures reproducibility
- Increases visibility and impact

---

## Prerequisites

Before starting, ensure:

1. ✅ Your repository is on GitHub
2. ✅ CI/CD tests are passing (all tests green)
3. ✅ You're ready to create a release (v1.0.0)
4. ✅ You have a GitHub account
5. ✅ You have cleaned up any sensitive data

---

## Step-by-Step Guide

### Step 1: Create a Zenodo Account

1. Go to **https://zenodo.org/**
2. Click **"Sign up"** in the top right
3. Choose **"Sign up with GitHub"** (recommended)
   - This allows automatic integration
4. Authorize Zenodo to access your GitHub account
5. Complete your profile:
   - Full name
   - Affiliation (Universidad del Pacífico - CIUP)
   - ORCID (if you have one - recommended)

**Time required:** 5 minutes

---

### Step 2: Link Your GitHub Repository to Zenodo

1. Log in to Zenodo: https://zenodo.org/
2. Click your profile name (top right) → **"GitHub"**
3. You'll see a list of your GitHub repositories
4. Find **"JasonCruz18/peru_gdp_revisions"** (or peruvian_gdp_revisions)
5. Toggle the switch **ON** next to your repository
   - This enables automatic DOI creation for releases

**Important:** Once enabled, Zenodo will automatically create a DOI for **each GitHub release** you create.

**Time required:** 2 minutes

---

### Step 3: Create a GitHub Release

Now that Zenodo is watching your repository, create a release:

1. Go to your GitHub repository:
   ```
   https://github.com/JasonCruz18/peru_gdp_revisions
   ```

2. Click **"Releases"** (right sidebar)

3. Click **"Create a new release"** or **"Draft a new release"**

4. Fill in the release information:

   **Tag version:**
   ```
   v1.0.0
   ```

   **Release title:**
   ```
   Peru GDP Real-Time Dataset v1.0.0 - Initial Release
   ```

   **Description:** (Copy and adapt from CHANGELOG.md)
   ```markdown
   ## Peru GDP Real-Time Dataset Construction Pipeline v1.0.0

   First stable release of the automated pipeline for constructing real-time datasets of Peruvian GDP revisions from BCRP Weekly Reports.

   ### 🎯 Key Features

   - **Automated data collection** from BCRP Weekly Reports (1992-present)
   - **Real-Time Dataset (RTD)** construction with vintage tracking
   - **70+ cleaning functions** for data standardization
   - **Base-year adjustment** handling (1990, 1994, 2007)
   - **Multiple output formats** (RTD, releases, benchmark)
   - Reproducible code pipeline for dataset construction
   - **Complete documentation** and tutorial notebooks
   - **CI/CD pipeline** with cross-platform testing

   ### 📊 Generated Datasets

   - Monthly GDP growth rates (vintage format)
   - Quarterly/Annual GDP growth rates
   - Releases format (1st, 2nd, 3rd releases)
   - Benchmark datasets
   - Base-year adjusted RTDs

   ### 📚 Documentation

   - Installation guide (pip and conda)
   - Usage guide with examples
   - Architecture documentation
   - 6 tutorial notebooks
   - FAQ and troubleshooting
   - Data availability statement (journal submission ready)

   ### 🧪 Testing

   - Smoke tests for all modules
   - Tested on Ubuntu, Windows, macOS
   - Python 3.10, 3.11, 3.12 support

   ### 📄 Citation

   See CITATION.cff for citation information.

   ### 🔗 Links

   - Repository: https://github.com/JasonCruz18/peru_gdp_revisions
   - Documentation: https://github.com/JasonCruz18/peru_gdp_revisions/tree/main/docs
   - Main pipeline: Run `python scripts/update_rtd.py`

   ---

   **Author:** Jason Cruz (Universidad del Pacífico - CIUP)
   **License:** MIT
   ```

5. **Optional:** Attach binary files if needed (usually not necessary for code)

6. Click **"Publish release"**

**Time required:** 10 minutes

---

### Step 4: Verify DOI Creation on Zenodo

After creating the GitHub release:

1. Wait 5-10 minutes for Zenodo to process the release

2. Go to Zenodo: https://zenodo.org/

3. Click your profile → **"My Uploads"** or **"GitHub"**

4. You should see your release listed with a DOI badge:
   ```
   DOI: 10.5281/zenodo.XXXXXXX
   ```

5. Click on the entry to see the full Zenodo record

6. Verify that all files are included:
   - Source code (automatically archived)
   - LICENSE
   - README.md
   - CITATION.cff
   - All documentation

**Time required:** 5 minutes

---

### Step 5: Add DOI Badge to README

Once you have the DOI, add it to your README.md:

1. On your Zenodo record page, look for **"DOI"** badge options

2. Copy the Markdown badge code:
   ```markdown
   [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.XXXXXXX.svg)](https://doi.org/10.5281/zenodo.XXXXXXX)
   ```

3. Edit your README.md and add the badge at the top:
   ```markdown
   # Peru GDP Real-Time Dataset Construction Pipeline

   [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.XXXXXXX.svg)](https://doi.org/10.5281/zenodo.XXXXXXX)
   [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
   [![Tests](https://github.com/JasonCruz18/peru_gdp_revisions/workflows/Tests/badge.svg)](https://github.com/JasonCruz18/peru_gdp_revisions/actions)

   [Rest of README...]
   ```

4. Commit and push the changes

**Time required:** 2 minutes

---

### Step 6: Update CITATION.cff with DOI

Update your CITATION.cff file with the DOI:

```yaml
cff-version: 1.2.0
message: "If you use this software or dataset, please cite it as below."
type: software
title: "Peru GDP Real-Time Dataset Construction Pipeline"
version: "1.0.0"
doi: 10.5281/zenodo.XXXXXXX  # ← Add this line
date-released: "2025-12-16"
# ... rest of file
```

Commit and push this change.

**Time required:** 2 minutes

---

### Step 7: Update DATA_AVAILABILITY.md

Update the DOI section in docs/DATA_AVAILABILITY.md:

```markdown
### DOI (Digital Object Identifier)

**Code**: [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.XXXXXXX.svg)](https://doi.org/10.5281/zenodo.XXXXXXX)
**Paper**: [Journal DOI - To be assigned upon publication]
```

**Time required:** 1 minute

---

## Concept DOI vs. Version DOI

Zenodo provides **two types of DOIs**:

1. **Concept DOI** (10.5281/zenodo.AAAAAAA)
   - Always points to the latest version
   - Use this in your paper and general documentation
   - Example: `10.5281/zenodo.1234567`

2. **Version DOI** (10.5281/zenodo.BBBBBBB)
   - Points to a specific version (e.g., v1.0.0)
   - Use this when citing a specific version
   - Example: `10.5281/zenodo.1234568` (for v1.0.0)

**Which one to use?**
- **In your paper:** Use the **Concept DOI** (readers get the latest version)
- **In specific citations:** Use the **Version DOI** if you need to reference a specific version

---

## Future Releases

Once Zenodo is linked, creating new releases is easy:

1. Make changes to your code
2. Merge to main branch
3. Create a new GitHub release (e.g., v1.1.0)
4. Zenodo **automatically** creates a new DOI version
5. Update CITATION.cff with the new version

The **Concept DOI remains the same** and always points to the latest version.

---

## Zenodo Metadata

On your Zenodo record, you can edit metadata:

1. Go to your upload on Zenodo
2. Click **"Edit"**
3. Add/update:
   - **Communities:** Join relevant communities (e.g., "Economics", "Data Science")
   - **Keywords:** Add tags like "GDP", "real-time data", "Peru", "revisions"
   - **Description:** Enhanced description (auto-populated from GitHub)
   - **Related identifiers:** Link to your paper DOI when published
   - **Contributors:** Add co-authors
   - **Funding:** Add grant information if applicable

---

## Troubleshooting

### Issue: "Repository not showing in Zenodo GitHub list"

**Solution:**
1. Check that you authorized Zenodo to access your GitHub account
2. Refresh the Zenodo GitHub page
3. Check GitHub → Settings → Applications → Zenodo (ensure access granted)

### Issue: "DOI not created after release"

**Solution:**
1. Wait 15-30 minutes (Zenodo processes releases asynchronously)
2. Check that the toggle is ON in Zenodo GitHub settings
3. Create a new release if the first one didn't trigger

### Issue: "Want to update Zenodo record after release"

**Solution:**
1. Go to Zenodo upload
2. Click "New version"
3. Update files and metadata
4. Publish new version

---

## Citation Format with DOI

Once you have the DOI, use this citation format:

**BibTeX:**
```bibtex
@software{cruz2025gdp_pipeline,
  author = {Cruz, Jason},
  title = {Peru GDP Real-Time Dataset Construction Pipeline},
  year = {2025},
  version = {1.0.0},
  doi = {10.5281/zenodo.XXXXXXX},
  url = {https://doi.org/10.5281/zenodo.XXXXXXX}
}
```

**APA:**
```
Cruz, J. (2025). Peru GDP Real-Time Dataset Construction Pipeline (Version 1.0.0) [Computer software]. Zenodo. https://doi.org/10.5281/zenodo.XXXXXXX
```

---

## Checklist

Before creating a release:

- [ ] All tests passing on CI/CD
- [ ] README.md is up to date
- [ ] CHANGELOG.md documents all changes
- [ ] LICENSE file included
- [ ] CITATION.cff is complete
- [ ] No sensitive data in repository
- [ ] Documentation is complete
- [ ] Code is clean and commented
- [ ] Version number follows semantic versioning (v1.0.0)

After creating a release:

- [ ] DOI created on Zenodo
- [ ] DOI badge added to README.md
- [ ] DOI added to CITATION.cff
- [ ] DATA_AVAILABILITY.md updated with DOI
- [ ] Citation information tested

---

## Resources

- **Zenodo Help:** https://help.zenodo.org/
- **GitHub-Zenodo Integration:** https://docs.github.com/en/repositories/archiving-a-github-repository/referencing-and-citing-content
- **Zenodo API:** https://developers.zenodo.org/ (for advanced automation)
- **CITATION.cff Specification:** https://citation-file-format.github.io/

---

## Summary Timeline

| Step | Task | Time |
|------|------|------|
| 1 | Create Zenodo account | 5 min |
| 2 | Link GitHub repository | 2 min |
| 3 | Create GitHub release | 10 min |
| 4 | Verify DOI creation | 5 min |
| 5 | Add DOI badge to README | 2 min |
| 6 | Update CITATION.cff | 2 min |
| 7 | Update DATA_AVAILABILITY.md | 1 min |
| **Total** | | **~30 minutes** |

---

**Author:** Jason Cruz
**Last Updated:** December 16, 2025
**Repository:** https://github.com/JasonCruz18/peru_gdp_revisions
