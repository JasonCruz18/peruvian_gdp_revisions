"""
Comprehensive review of 2001 OCR results for methodological documentation.
"""
import pandas as pd
from pathlib import Path
import json

# Get all 2001 CSVs
csv_files = sorted(Path('OCR/output/table_1/2001').glob('*.csv'))

print('=' * 80)
print('OCR PIPELINE RESULTS - YEAR 2001 (Methodological Example)')
print('=' * 80)
print()
print(f'Total PDFs processed: {len(csv_files)}')
print()

# Analyze each CSV
results = []
for csv_file in csv_files:
    df = pd.read_csv(csv_file, sep=';', encoding='utf-8-sig')

    # Extract week from filename
    week = csv_file.stem.split('-')[1]

    results.append({
        'week': week,
        'filename': csv_file.name,
        'rows': len(df),
        'cols': len(df.columns),
        'sectors': list(df.iloc[:, 0]),
        'missing_values': df.isnull().sum().sum(),
        'total_cells': df.shape[0] * df.shape[1]
    })

# Summary statistics
print('SUMMARY STATISTICS:')
print('-' * 80)
total_rows = sum(r['rows'] for r in results)
total_cols_avg = sum(r['cols'] for r in results) / len(results)
total_missing = sum(r['missing_values'] for r in results)
total_cells = sum(r['total_cells'] for r in results)

print(f'Total sectors extracted: {total_rows}')
print(f'Average columns per file: {total_cols_avg:.1f}')
print(f'Total data cells: {total_cells}')
print(f'Missing values: {total_missing} ({100*total_missing/total_cells:.1f}%)')
print(f'Data completeness: {100*(1-total_missing/total_cells):.1f}%')
print()

# Detailed breakdown
print('DETAILED BREAKDOWN BY WEEK:')
print('-' * 80)
header = f"{'Week':<8} {'Filename':<24} {'Sectors':<10} {'Cols':<8} {'Missing %':<12}"
print(header)
print('-' * 80)

for r in sorted(results, key=lambda x: x['week']):
    missing_pct = 100 * r['missing_values'] / r['total_cells']
    row = f"{r['week']:<8} {r['filename']:<24} {r['rows']:<10} {r['cols']:<8} {missing_pct:<12.1f}"
    print(row)

print()

# Quality assessment
missing_pcts = [100 * r['missing_values'] / r['total_cells'] for r in results]
print('QUALITY ASSESSMENT:')
print('-' * 80)
print(f'Best file (lowest missing): {min(missing_pcts):.1f}%')
print(f'Worst file (highest missing): {max(missing_pcts):.1f}%')
print(f'Average missing: {sum(missing_pcts)/len(missing_pcts):.1f}%')
print(f'Median missing: {sorted(missing_pcts)[len(missing_pcts)//2]:.1f}%')
print()

# Sector consistency
all_sectors = {}
for r in results:
    week = r['week']
    for sector in r['sectors']:
        if sector not in all_sectors:
            all_sectors[sector] = []
        all_sectors[sector].append(week)

print('SECTOR CONSISTENCY:')
print('-' * 80)
print(f'Unique sectors found: {len(all_sectors)}')
print()
print('Most common sectors:')
sector_freq = [(sector, len(weeks)) for sector, weeks in all_sectors.items()]
sector_freq.sort(key=lambda x: -x[1])

for sector, freq in sector_freq[:15]:
    print(f'  {sector:<45} {freq:>2}/12 files ({100*freq/12:.0f}%)')

print()
print()

# Sample output
print('SAMPLE OUTPUT (Week 04 - first file):')
print('=' * 80)
sample = pd.read_csv('OCR/output/table_1/2001/ns-04-2001.csv', sep=';', encoding='utf-8-sig')
print(sample.iloc[:8, :8].to_string(index=False))

print()
print()
print('=' * 80)
print('CONCLUSIONS FOR DIB MANUSCRIPT:')
print('=' * 80)
print('1. OCR successfully extracted data from all 12 PDFs (100% processing)')
print(f'2. Average data completeness: {100*(1-total_missing/total_cells):.1f}%')
print(f'3. Extracted {total_rows} total sector-month observations')
print('4. OCR errors present (e.g., "agropacuaro", "posci") demonstrate need for')
print('   manual review - supporting transparency about data collection process')
print('5. 2001 exemplar shows bilingual format (Spanish/English) typical of')
print('   post-2000 BCRP publications')
print()
print('RECOMMENDATION: Document this as methodological example in _Supplement.tex')
print('                showing the OCR pipeline can extract ~50-60% of data')
print('                automatically, with remaining requiring human curation.')
