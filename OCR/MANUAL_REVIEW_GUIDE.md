# Manual Review Guide for OCR Outputs

**Comprehensive guide for manually verifying and correcting OCR-generated CSV files.**

---

## When is Manual Review Needed?

The OCR pipeline automatically flags outputs for manual review when:

1. **Low OCR confidence** (< 85%)
2. **Validation errors detected:**
   - Missing expected columns
   - Incorrect or missing sector names
   - Non-numeric values in data columns
   - Unrealistic values (> 500% or < -100%)
3. **High proportion of missing values** (> 10%)

---

## Review Workflow Overview

```
1. Check needs_review.txt
      ↓
2. Open review package for each flagged file
      ↓
3. Compare PDF with CSV
      ↓
4. Correct errors in CSV
      ↓
5. Save corrected CSV to output folder
      ↓
6. Delete review folder
      ↓
7. Verify corrections
```

---

## Step-by-Step Instructions

### Step 1: Identify Files Needing Review

```bash
# Check the needs-review list
cat OCR/needs_review.txt

# Or view in editor
notepad OCR/needs_review.txt
```

**Example output:**
```
Files Needing Manual Review
================================================================================

Total files: 3

ns_11_1994.pdf
  Confidence: 78%
  Issues:
    - Missing columns
    - Unclear sector names in rows 3-4

ns_15_1994.pdf
  Confidence: 81%
  Issues:
    - Digit misrecognition in mining sector

...
```

### Step 2: Open Review Package

For each flagged file, navigate to its review folder:
```
OCR/review/YYYY/ns_XX_YYYY/
├── original.pdf           # Scanned source document
├── preprocessed.png       # After image preprocessing
├── ocr_output.csv         # OCR result needing correction
└── issues.txt             # Detailed issues report
```

**Example:** For `ns_11_1994.pdf`, open:
- `OCR/review/1994/ns_11_1994/`

### Step 3: Compare PDF with CSV

1. **Open original.pdf** in a PDF viewer
2. **Open ocr_output.csv** in Excel or text editor
3. **Compare side-by-side:**
   - Check sector names in first two columns
   - Verify numeric values column by column
   - Look for missing or transposed digits

**Pro tip:** Use dual monitors or split-screen for easier comparison

### Step 4: Common OCR Errors to Look For

#### A. Digit Misrecognition

| OCR Error | Should Be | Context |
|-----------|-----------|---------|
| O (letter) | 0 (zero) | In numeric values: `1O.5` → `10.5` |
| l (lowercase L) | 1 (one) | In numeric values: `l2.3` → `12.3` |
| S (letter) | 5 (five) | At end of number: `9.S` → `9.5` |
| B (letter) | 8 (eight) | In numeric values: `B.4` → `8.4` |
| Z (letter) | 2 (two) | Less common: `Z.5` → `2.5` |

**Example from actual table:**
```csv
# OCR output (WRONG):
pesca;fishing;-29.B;-26.4;-lO.5;12.S

# Corrected:
pesca;fishing;-29.8;-26.4;-10.5;12.5
```

#### B. Missing Decimal Points

**Problem:** OCR sometimes misses decimal points, especially in faded scans

```csv
# WRONG:
agropecuario;agriculture;37;36;42

# CORRECT:
agropecuario;agriculture;3.7;3.6;4.2
```

**How to detect:** Values > 100 are unusual for monthly/quarterly growth rates

#### C. Transposed or Missing Digits

**Problem:** Digits can be misread or completely missed

```csv
# WRONG (transposed 96 → 69):
manufactura;manufacturing;-3.5;-2.3;69.8

# CORRECT:
manufactura;manufacturing;-3.5;-2.3;96.8
```

#### D. Sector Name Errors

**Problem:** Spanish sector names with accents or special characters

```csv
# WRONG:
minena;mining;...           # Should be "mineria"
construcciOn;construction;  # Should be "construccion"
electncidad;electricity;    # Should be "electricidad"

# CORRECT:
mineria e hidrocarburos;mining and fuel;...
construccion;construction;...
electricidad y agua;electricity and water;...
```

#### E. Column Misalignment

**Problem:** OCR sometimes merges or splits columns incorrectly

```csv
# WRONG (values shifted):
sectores_economicos;economic_sectors;1992_ene;1992_feb
agropecuario agriculture;and livestock;3.7;3.6

# CORRECT:
sectores_economicos;economic_sectors;1992_ene;1992_feb
agropecuario;agriculture and livestock;3.7;3.6
```

#### F. Missing Negative Signs

**Problem:** Negative signs can be lost, especially for small fonts

```csv
# WRONG (should be negative):
pesca;fishing;29.8;26.4;55.9

# CORRECT:
pesca;fishing;-29.8;-26.4;-55.9
```

**How to detect:** Check if values seem unrealistic (fishing sector with consistent huge growth)

---

### Step 5: Correction Workflow

#### Using Excel (Recommended)

1. **Open CSV in Excel:**
   ```
   File → Open → Select "ocr_output.csv"
   ```

2. **Check delimiter:**
   - Should be semicolon (;)
   - Excel may auto-detect or ask

3. **Correction checklist:**
   - [ ] First column: Spanish sector names correct
   - [ ] Second column: English sector names correct
   - [ ] Remaining columns: All numeric values
   - [ ] No missing decimal points
   - [ ] No digit misrecognitions (O→0, l→1, etc.)
   - [ ] Negative signs present where needed
   - [ ] No column misalignments

4. **Save corrected version:**
   ```
   File → Save As → CSV (Semicolon delimited) (*.csv)
   ```

#### Using Text Editor (Advanced)

For quick fixes, use VS Code, Notepad++, or similar:

1. **Open ocr_output.csv**
2. **Use Find & Replace for systematic errors:**
   ```
   Find:    ;O\.     (semicolon + O + decimal)
   Replace: ;0.      (semicolon + 0 + decimal)

   Find:    ;l(\d)   (semicolon + l + digit)
   Replace: ;1$1     (semicolon + 1 + digit)
   ```

3. **Manually fix unique errors**
4. **Save with UTF-8 encoding**

---

### Step 6: Save Corrected CSV

**Important:** Save to the correct output location!

```bash
# Correct location format:
OCR/output/table_1/YYYY/ns-XX-YYYY.csv
# OR
OCR/output/table_2/YYYY/ns-XX-YYYY.csv
```

**Example for ns_11_1994.pdf (Table 1):**
```
Source:      OCR/review/1994/ns_11_1994/ocr_output.csv
Destination: OCR/output/table_1/1994/ns-11-1994.csv
```

**Note the filename change:** `ns_11_1994` → `ns-11-1994` (underscore → hyphen)

---

### Step 7: Delete Review Folder

After saving corrected CSV:

```bash
# Delete review folder for this file
rm -rf OCR/review/1994/ns_11_1994/

# Or manually delete in file explorer
```

**Why delete?** Signals that review is complete and prevents re-flagging

---

### Step 8: Verify Corrections

Run verification to ensure corrections are valid:

```bash
# Option 1: Verify specific file
python OCR/ocr_processors/validator.py OCR/output/table_1/1994/ns-11-1994.csv

# Option 2: Verify all outputs
python scripts/run_ocr_pipeline.py --verify
```

**Expected output:**
```
✓ Validation passed

Confidence Scores:
  OCR: 78.0%
  Combined: 88.0%  # Improved after manual correction
  Status: PASS
```

---

## Quality Control Checklist

Before marking a file as reviewed, verify:

- [ ] **All sector names present:**
  - agropecuario / agriculture and livestock
  - pesca / fishing
  - mineria e hidrocarburos / mining and fuel
  - manufactura / manufacturing
  - electricidad y agua / electricity and water
  - construccion / construction
  - comercio / commerce
  - otros servicios / other services
  - pbi / gdp

- [ ] **Numeric columns:**
  - All values are numbers (no letters)
  - Decimal points present where needed
  - Negative signs correct
  - No unrealistic outliers (check: -100% to +500% range)

- [ ] **Column structure:**
  - First column: Spanish sector names (semicolon)
  - Second column: English sector names (semicolon)
  - Remaining columns: Numeric data (semicolon-separated)

- [ ] **File naming:**
  - Saved to correct output folder (table_1 or table_2)
  - Filename uses hyphens: ns-XX-YYYY.csv

---

## Tips for Efficient Review

### 1. Prioritize by Confidence

Review lowest-confidence files first:
```bash
# Sort needs_review.txt by confidence
sort -t: -k2 -n OCR/needs_review.txt
```

### 2. Batch Similar Years

Process files from the same year together to spot patterns:
```bash
# Review all 1994 files at once
ls OCR/review/1994/
```

### 3. Use Excel Formulas for Validation

Create a validation column in Excel:
```excel
# Flag non-numeric values in column C
=IF(ISNUMBER(C2), "OK", "ERROR")

# Flag unrealistic values
=IF(OR(C2>500, C2<-100), "OUTLIER", "OK")
```

### 4. Keep Original PDF Open

Don't close the PDF - you may need to check multiple times

### 5. Document Patterns

If you notice systematic OCR errors (e.g., all 'O' should be '0'), note them for potential pipeline improvements

---

## Troubleshooting

### Problem: Excel Changes Formatting

**Symptom:** Dates become dates (1994_ene → 1/1994), decimals change

**Solution:**
1. Open Excel
2. File → Open (don't double-click CSV)
3. Select "Text Import Wizard"
4. Choose "Delimited" → Semicolon
5. Set all columns as "Text" format
6. Complete import
7. Save as CSV (Semicolon delimited)

### Problem: Can't Read PDF (Too Blurry)

**Solution:**
1. Check `preprocessed.png` in review folder
2. If preprocessing improved quality, reference that
3. If still unclear, note in issues and flag for re-scan
4. Make best-effort correction based on context

### Problem: Entire Row Missing

**Solution:**
1. Check if sector is in PDF
2. If yes, add manually:
   ```csv
   pesca;fishing;-29.8;-26.4;...
   ```
3. Match column structure to other rows

### Problem: Extra Columns or Rows

**Solution:**
1. Check against PDF to determine correct structure
2. Remove spurious columns/rows
3. Ensure row count matches expected sectors (8 + GDP = 9 rows)

---

## Examples

### Example 1: Complete Review of ns_11_1994.pdf

**Initial issues.txt:**
```
Issues Detected (3):
  1. Column 'sectores_economicos' has wrong name: 'sectores economicos'
  2. Missing Spanish sector: construccion
  3. Unrealistic values > 500% detected
```

**Review process:**

1. **Open files:**
   - `original.pdf` shows clear table
   - `ocr_output.csv` has errors

2. **Identified errors:**
   - Header: `sectores economicos` (space) → `sectores_economicos` (underscore)
   - Row 6 missing: construccion / construction
   - manufactura row: `5O2.3` → `50.2` (O→0, extra digit?)

3. **Corrections made:**
   ```csv
   # Fixed header
   sectores_economicos;economic_sectors;...

   # Added missing row
   construccion;construction;27.7;12.8;28.8;...

   # Fixed unrealistic value
   manufactura;manufacturing;-3.5;-2.3;50.2;...  # was 5O2.3
   ```

4. **Saved to:** `OCR/output/table_1/1994/ns-11-1994.csv`

5. **Verified:** ✓ All checks passed

6. **Deleted:** `OCR/review/1994/ns_11_1994/`

---

### Example 2: Systematic Digit Error

**Problem:** All 'O' (letter O) should be '0' (zero) in one column

**Solution using Find & Replace in Excel:**

1. Select the problematic column
2. Ctrl+H (Find & Replace)
3. Find: `O`
4. Replace: `0`
5. Options: Match case ✓
6. Replace All

**Result:** All 47 instances corrected instantly

---

## Recording Your Work

### Create a Review Log (Optional)

Keep track of corrections for documentation:

```
review_log.txt:

2026-01-07:
- ns_11_1994.pdf: Fixed O→0 errors (5 instances), added missing construccion row
- ns_15_1994.pdf: Corrected transposed digits in mining sector (96.8 not 69.8)
- ns_22_1994.pdf: Fixed missing negative signs in pesca sector

Total reviewed: 3 files
Time: ~45 minutes
```

---

## Summary

**Efficient manual review workflow:**

1. ✓ Check `needs_review.txt` for flagged files
2. ✓ Open review package (PDF + CSV + issues)
3. ✓ Compare and identify errors systematically
4. ✓ Correct using Excel or text editor
5. ✓ Save to correct output location with proper filename
6. ✓ Delete review folder
7. ✓ Verify corrections
8. ✓ Move to next file

**Expected time:** 15-30 minutes per file (depending on error severity)

**Target:** ~5-10% of 228 PDFs = 12-23 files needing review = 3-6 hours total

---

## Need Help?

- **Technical issues:** Check OCR/README.md troubleshooting section
- **Validation errors:** Review error messages in `issues.txt`
- **Unclear scans:** Reference `preprocessed.png` for enhanced version
- **Questions:** Contact jj.cruza@up.edu.pe

---

**Remember:** Manual review is a normal and expected part of OCR workflows. Your corrections ensure the highest quality dataset for publication!
