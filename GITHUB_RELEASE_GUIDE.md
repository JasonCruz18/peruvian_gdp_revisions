# GitHub Release Guide - Peru GDP RTD v1.0.0

**Purpose:** Create GitHub Release v1.0.0 and obtain a code DOI via Zenodo-GitHub integration.

**Estimated Time:** 1-2 hours

---

## Prerequisites

- [ ] GitHub repository exists and is public
- [ ] All code committed and pushed to `main` branch
- [ ] Zenodo data DOI obtained (from previous step)
- [ ] GitHub account access
- [ ] Zenodo account (same as data upload)

---

## Step 1: Enable Zenodo-GitHub Integration

### Why This Matters:
GitHub-Zenodo integration automatically creates a DOI for your code when you create a release.

### Process:

1. [ ] Log in to **Zenodo** (https://zenodo.org)
2. [ ] Click your **username** (top right) → **"GitHub"**
3. [ ] Click **"Sync now"** to fetch latest repositories
4. [ ] Find **"peru_gdp_revisions"** in the list
5. [ ] Toggle the **switch to ON** (green)
6. [ ] You'll see: "Enabled. Waiting for first release."

### Important Notes:
- Repository **must be public** on GitHub
- Integration works for **releases only**, not regular commits
- Each release gets its own DOI version
- Concept DOI (version-independent) is also created

**Time:** 10 minutes

**Troubleshooting:**
- If repo doesn't appear: Make sure it's public and click "Sync now"
- If toggle doesn't work: Disconnect and reconnect GitHub integration

---

## Step 2: Prepare Release Notes

Before creating the release, draft comprehensive release notes.

### Create `RELEASE_NOTES_v1.0.0.md`:

```markdown
# Peru GDP RTD v1.0.0 - Initial Public Release

**Release Date:** December 28, 2024
**DOI:** [Will be assigned by Zenodo upon release]
**Data DOI:** https://doi.org/10.5281/zenodo.XXXXXXX (replace with your Zenodo data DOI)

---

## Overview

This is the first public release of the Peru GDP Real-Time Dataset (RTD) project. The codebase provides a fully automated pipeline for constructing real-time databases of Peru's GDP growth rates from publicly available Central Bank (BCRP) Weekly Reports.

**Status:** Production-ready (v1.0.0)

---

## What's Included

### Core Features

✅ **6-Stage Data Pipeline:**
1. PDF download via web scraping (Selenium)
2. PDF shortening (keyword-based page extraction)
3. Vintage construction (70+ cleaning functions)
4. RTD concatenation (multi-year aggregation)
5. Metadata handling (base-year adjustments)
6. Releases conversion (revision sequence tracking)

✅ **Dual Format Outputs:**
- Vintage format (columns = release dates)
- Releases format (columns = revision sequences)

✅ **Timestamp-Based Incremental Processing:**
- Smart dependency tracking (like Make/CMake)
- No manual record management
- Self-healing pipeline (auto-rebuilds missing outputs)

✅ **Comprehensive Documentation:**
- 6 detailed markdown guides (50,000+ words)
- 35-page LaTeX technical supplement
- 7 tutorial Jupyter notebooks
- FAQ with 100+ questions
- Architecture documentation

✅ **Production Quality:**
- Type hints throughout
- Configuration-driven (YAML)
- Test suite (7 smoke tests)
- CI/CD via GitHub Actions
- Cross-platform (Windows/macOS/Linux)

---

## Dataset Published

The output dataset from this pipeline is published separately on Zenodo:

**Title:** Peru GDP Real-Time Dataset (1994-present)
**Data DOI:** https://doi.org/10.5281/zenodo.XXXXXXX (replace)
**Files:** 16 CSV files (vintages + releases formats)
**Size:** ~17 MB
**License:** CC-BY-4.0

---

## Installation

### Quick Start (pip):
```bash
git clone https://github.com/[username]/peru_gdp_revisions.git
cd peru_gdp_revisions
pip install -e .
python scripts/update_rtd.py
```

### Conda Environment:
```bash
git clone https://github.com/[username]/peru_gdp_revisions.git
cd peru_gdp_revisions
conda env create -f environment.yml
conda activate gdp_revisions
python scripts/update_rtd.py
```

**System Requirements:**
- Python 3.10+
- Java 8+ (for Tabula-py)
- 2 GB disk space
- Internet connection

---

## Major Changes Since Development

This is the initial public release. Key milestones achieved:

### December 2024: v1.0.0 Release Preparation
- ✅ Repository restructuring (modular architecture)
- ✅ Timestamp-based processing (replaced record files)
- ✅ Comprehensive documentation (6 guides)
- ✅ Test suite implementation
- ✅ CI/CD setup (GitHub Actions)
- ✅ Data in Brief submission preparation

### November 2024: Pipeline Refinement
- ✅ Metadata handler enhancements (base-year tracking)
- ✅ Releases converter implementation
- ✅ Benchmark dataset generation
- ✅ Quality validation module

### October 2024: Core Development
- ✅ PDF processor implementation
- ✅ 70+ cleaning functions
- ✅ Vintage construction system
- ✅ Configuration management (Pydantic)

### September 2024: Initial Development
- ✅ Web scraper implementation (Selenium)
- ✅ Project structure design
- ✅ Requirements specification

---

## Breaking Changes

⚠️ **None** (initial release)

Future versions will document breaking changes here.

---

## Known Limitations

1. **Pre-2002 Data Gaps:** Limited digital archive availability for earliest years
2. **Base-Year Structural Breaks:** Methodological changes (1990, 1994, 2007) create discontinuities
   - Mitigated with sentinel values in `by_adjusted_*` datasets
3. **Manual ORCID Placeholder:** `CITATION.cff` contains placeholder ORCID
   - Update with your ORCID: https://orcid.org

---

## Dependencies

**Core (Python 3.10+):**
- pandas >= 2.0.0
- numpy >= 1.24.0
- pyyaml >= 6.0
- selenium >= 4.0.0
- tabula-py >= 2.8.0
- PyMuPDF >= 1.23.0
- requests >= 2.31.0

**Development:**
- pytest >= 7.4.0
- black >= 23.0.0
- isort >= 5.12.0
- flake8 >= 6.0.0

See `requirements.txt` or `environment.yml` for complete list.

---

## Testing

Run the test suite:
```bash
pytest tests/
```

**Coverage:** 7 smoke tests covering critical path

**CI Status:** [![Tests](https://github.com/[username]/peru_gdp_revisions/actions/workflows/tests.yml/badge.svg)](https://github.com/[username]/peru_gdp_revisions/actions)

---

## Documentation

📖 **Read the Docs:**
- [README.md](README.md) - Quick start and overview
- [docs/INSTALLATION.md](docs/INSTALLATION.md) - Detailed installation guide
- [docs/USAGE.md](docs/USAGE.md) - Usage examples and CLI reference
- [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) - System design and architecture
- [docs/DATA_AVAILABILITY.md](docs/DATA_AVAILABILITY.md) - AEA-compliant data statement
- [docs/CONTRIBUTING.md](docs/CONTRIBUTING.md) - Contribution guidelines
- [FAQ.md](FAQ.md) - Frequently asked questions

📓 **Tutorials:**
- [notebooks/new_gdp_rtd.ipynb](notebooks/new_gdp_rtd.ipynb) - Main tutorial notebook
- Additional 6 tutorial notebooks in `notebooks/`

📄 **Technical Supplement:**
- [_Supplement.tex](_Supplement.tex) - 35-page LaTeX technical documentation

---

## Citation

If you use this code in your research, please cite both the code and the data:

### Code Citation (this release):
```bibtex
@software{peru_gdp_rtd_code_2024,
  author       = {[Your Name]},
  title        = {Peru GDP RTD: Code Repository},
  year         = {2024},
  publisher    = {Zenodo},
  version      = {1.0.0},
  doi          = {[Zenodo will assign]},
  url          = {https://github.com/[username]/peru_gdp_revisions}
}
```

### Data Citation:
```bibtex
@dataset{peru_gdp_rtd_data_2024,
  author       = {[Your Name]},
  title        = {Peru GDP Real-Time Dataset (1994-present)},
  year         = {2024},
  publisher    = {Zenodo},
  version      = {1.0.0},
  doi          = {10.5281/zenodo.XXXXXXX},  # Replace with actual DOI
  url          = {https://doi.org/10.5281/zenodo.XXXXXXX}
}
```

---

## License

**Code:** MIT License
**Data:** CC-BY-4.0 (see data repository)

See [LICENSE](LICENSE) for details.

---

## Contributing

Contributions welcome! Please see [CONTRIBUTING.md](docs/CONTRIBUTING.md) for guidelines.

**Ways to Contribute:**
- 🐛 Report bugs via [Issues](https://github.com/[username]/peru_gdp_revisions/issues)
- 💡 Suggest features
- 📖 Improve documentation
- 🔧 Submit pull requests

---

## Acknowledgments

Data sourced from the **Banco Central de Reserva del Perú (BCRP)**. We thank the BCRP for maintaining the Weekly Reports archive and making economic data publicly accessible.

**Developed at:** [Your Institution]
**Funding:** [Optional: Add funding acknowledgments]

---

## Related Publications

**Forthcoming:**
- "Rationality and Nowcasting on Peruvian GDP Revisions" (in preparation)

---

## Contact

- **Email:** [your.email@institution.edu]
- **ORCID:** [Your ORCID]
- **GitHub:** [@yourusername](https://github.com/yourusername)
- **Issues:** https://github.com/[username]/peru_gdp_revisions/issues

---

## What's Next (v1.1.0 Roadmap)

Future enhancements being considered:

- [ ] Interactive dashboard improvements
- [ ] Additional data formats (Excel, JSON)
- [ ] API endpoint for real-time data access
- [ ] Extended coverage (pre-1994 if sources available)
- [ ] Multi-country support (Colombia, Chile)

**Feedback welcome!** Open an issue to discuss priorities.

---

**Release Date:** December 28, 2024
**Release Type:** Major (1.0.0)
**Status:** Stable
```

Save this content to use in the GitHub release description.

**Time:** 20 minutes

---

## Step 3: Create Git Tag (Recommended)

Tags help organize releases. Create v1.0.0 tag:

### Via Command Line:
```bash
# Make sure all changes are committed
git status

# Create annotated tag
git tag -a v1.0.0 -m "Release v1.0.0 - Initial Public Release"

# Push tag to GitHub
git push origin v1.0.0
```

### Verify Tag:
```bash
git tag
git show v1.0.0
```

**Alternative:** Create tag during GitHub release creation (Step 4)

**Time:** 5 minutes

---

## Step 4: Create GitHub Release

### Process:

1. [ ] Go to your GitHub repository
2. [ ] Click **"Releases"** (right sidebar) or navigate to:
   ```
   https://github.com/[username]/peru_gdp_revisions/releases
   ```
3. [ ] Click **"Draft a new release"** (green button)

### Fill Release Form:

#### Tag Version:
- [ ] **Tag:** `v1.0.0`
- [ ] **Target:** `main` branch
- [ ] If tag doesn't exist, GitHub will create it automatically

#### Release Title:
```
Peru GDP RTD v1.0.0 - Initial Public Release
```

#### Release Description:
- [ ] Paste the content from `RELEASE_NOTES_v1.0.0.md` (created in Step 2)
- [ ] **Replace** `[username]` with your GitHub username
- [ ] **Replace** `XXXXXXX` in Zenodo data DOI with actual ID
- [ ] **Add** your name, email, ORCID where indicated

#### Attach Files (Optional but Recommended):

GitHub automatically creates source code archives, but you can attach additional files:

- [ ] Click **"Attach binaries by dropping them here or selecting them"**
- [ ] Upload (optional):
  - `environment.yml` (if not in repo root)
  - `requirements.txt` (if not in repo root)
  - Pre-built documentation PDF (if available)

#### Pre-release Checkbox:
- [ ] **Leave unchecked** (this is a stable release)

#### Set as Latest Release:
- [ ] **Check** "Set as the latest release"

**Time:** 15 minutes

---

## Step 5: Publish Release

### Final Checks:

- [ ] Tag version is `v1.0.0`
- [ ] Title is descriptive
- [ ] Release notes are comprehensive
- [ ] All links work (check preview)
- [ ] Zenodo data DOI is correct
- [ ] Email/ORCID updated
- [ ] No typos

### Publish:

1. [ ] Click green **"Publish release"** button
2. [ ] GitHub creates the release immediately
3. [ ] **Zenodo automatically archives** within a few minutes

### What Happens Next:

1. **GitHub:** Release appears at `/releases`
2. **Zenodo:** Receives webhook → Creates new deposit
3. **DOI Assignment:** Zenodo assigns DOI within 5-10 minutes
4. **Email Notification:** You'll receive email from Zenodo with DOI

**Time:** 5 minutes + 10 minutes wait for Zenodo

---

## Step 6: Retrieve Code DOI from Zenodo

### After Publishing GitHub Release:

1. [ ] Wait ~10 minutes for Zenodo processing
2. [ ] Check email for Zenodo notification
3. [ ] Log in to **Zenodo** → Click **"Upload"** → **"My uploads"**
4. [ ] Find the new deposit: **"peru_gdp_revisions v1.0.0"** or similar
5. [ ] Click on the title to view deposit page

### Copy DOI Information:

- [ ] **Version DOI:** Specific to v1.0.0 (e.g., `10.5281/zenodo.7654321`)
- [ ] **Concept DOI:** Version-independent (e.g., `10.5281/zenodo.7654320`)
  - Use concept DOI in citations (automatically resolves to latest version)

### Verify DOI:
- [ ] Click DOI link → Should resolve to Zenodo page
- [ ] Check that files are correct (GitHub automatically packages source code)
- [ ] Download citation (BibTeX, JSON, etc.)

**Time:** 15 minutes

---

## Step 7: Update Repository with DOIs

Now that you have both DOIs (data + code), update your repository:

### Files to Update:

#### 1. `CITATION.cff`

Find and replace the DOI placeholders:

```yaml
cff-version: 1.2.0
title: "Peru GDP Real-Time Dataset: Code Repository"
message: "If you use this software, please cite both the code and the data"
authors:
  - family-names: "[Your Family Name]"
    given-names: "[Your Given Names]"
    orcid: "https://orcid.org/0000-0000-0000-0000"  # REPLACE with your real ORCID
references:
  - type: dataset
    title: "Peru GDP Real-Time Dataset (1994-present)"
    authors:
      - family-names: "[Your Family Name]"
        given-names: "[Your Given Names]"
    year: 2024
    doi: 10.5281/zenodo.XXXXXXX  # REPLACE with data DOI
repository-code: "https://github.com/[username]/peru_gdp_revisions"
url: "https://github.com/[username]/peru_gdp_revisions"
license: MIT
version: 1.0.0
date-released: "2024-12-28"
```

#### 2. `README.md`

Add DOI badges at the top:

```markdown
# Peru GDP Real-Time Dataset

[![Data DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.XXXXXXX.svg)](https://doi.org/10.5281/zenodo.XXXXXXX)
[![Code DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.YYYYYYY.svg)](https://doi.org/10.5281/zenodo.YYYYYYY)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

[Rest of README...]
```

Replace:
- `XXXXXXX` with data DOI
- `YYYYYYY` with code DOI

#### 3. `docs/DATA_AVAILABILITY.md`

Update the DOI placeholders:

```markdown
## Code

The code repository for this project is publicly available on GitHub with a
permanent DOI via Zenodo:

**Repository:** https://github.com/[username]/peru_gdp_revisions
**DOI:** https://doi.org/10.5281/zenodo.YYYYYYY

## Data

The processed datasets are available on Zenodo:

**Data DOI:** https://doi.org/10.5281/zenodo.XXXXXXX
```

#### 4. `ZENODO_README.md`

Update the DOI field:

```markdown
**DOI:** https://doi.org/10.5281/zenodo.XXXXXXX
```

### Commit and Push:

```bash
git add CITATION.cff README.md docs/DATA_AVAILABILITY.md ZENODO_README.md
git commit -m "docs: add Zenodo DOIs for data and code"
git push origin main
```

**Time:** 20 minutes

---

## Step 8: Verification Checklist

### Verify Everything Works:

- [ ] **GitHub Release:** Visible at `https://github.com/[username]/peru_gdp_revisions/releases/tag/v1.0.0`
- [ ] **Zenodo Code Record:** Accessible via code DOI
- [ ] **Zenodo Data Record:** Accessible via data DOI
- [ ] **DOI Resolution:** Both DOIs resolve correctly
- [ ] **GitHub Badges:** Display correctly in README.md
- [ ] **CITATION.cff:** Valid (check with https://citation-file-format.github.io/cff-initializer-javascript/)
- [ ] **Cross-Links:** Zenodo records link to GitHub, GitHub links to Zenodo
- [ ] **Downloads Work:** Can download source code from Zenodo

**Time:** 10 minutes

---

## Troubleshooting

### "Zenodo didn't create a DOI after release"

**Solution:**
1. Check Zenodo upload page → Refresh
2. Verify GitHub-Zenodo integration is enabled (green toggle)
3. Wait longer (can take up to 30 minutes during high traffic)
4. Check Zenodo status page: https://status.zenodo.org
5. Contact Zenodo support if > 1 hour: info@zenodo.org

### "Wrong files in Zenodo deposit"

**Cause:** Zenodo archives entire GitHub repository at release tag

**Solution:**
- This is expected behavior (source code archive)
- If you need different files, create manual Zenodo upload
- Or exclude files with `.gitattributes` (advanced)

### "Can't edit Zenodo metadata after publishing"

**Solution:**
- Zenodo allows minor metadata edits (title, description, keywords)
- Click "Edit" button on Zenodo deposit page
- For major changes, create new version

### "DOI badge not displaying"

**Solution:**
- Check DOI is correct in badge URL
- Verify image URL format: `https://zenodo.org/badge/DOI/10.5281/zenodo.XXXXXXX.svg`
- Clear browser cache
- Verify on GitHub (may take a few minutes to update)

---

## Next Steps

✅ **Task 3 Complete:** GitHub Release v1.0.0 with code DOI created!

### Proceed to:
- **Task 4:** Complete DIB Article Template (now have both DOIs!)
- **Task 5:** Register/verify ORCID and update CITATION.cff
- **Task 6:** Create DATA_DICTIONARY.md

---

## Resources

- **GitHub Releases Docs:** https://docs.github.com/en/repositories/releasing-projects-on-github
- **Zenodo-GitHub Integration:** https://docs.github.com/en/repositories/archiving-a-github-repository/referencing-and-citing-content
- **Making Your Code Citable:** https://guides.github.com/activities/citable-code/
- **Zenodo Help:** https://help.zenodo.org

---

**Document Version:** 1.0
**Last Updated:** December 28, 2024
