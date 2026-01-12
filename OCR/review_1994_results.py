"""
Review script for 1994 OCR results.
"""
import pandas as pd
from pathlib import Path

# Get all 1994 CSVs
csv_files = sorted(Path('OCR/output/table_1/1994').glob('*.csv'))

print('=' * 70)
print('OCR RESULTS REVIEW - 1994 (12 PDFs)')
print('=' * 70)
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
print('-' * 70)
total_rows = sum(r['rows'] for r in results)
total_cols_avg = sum(r['cols'] for r in results) / len(results)
total_missing = sum(r['missing_values'] for r in results)
total_cells = sum(r['total_cells'] for r in results)

print(f'Total PDFs processed: {len(results)}')
print(f'Total sectors extracted: {total_rows}')
print(f'Average columns per file: {total_cols_avg:.1f}')
print(f'Missing values: {total_missing} / {total_cells} ({100*total_missing/total_cells:.1f}%)')
print()

# Show details for each file
print('DETAILED BREAKDOWN:')
print('-' * 70)
header = f"{'Week':<8} {'Filename':<22} {'Rows':<8} {'Cols':<8} {'Missing %':<12}"
print(header)
print('-' * 70)

for r in results:
    missing_pct = 100 * r['missing_values'] / r['total_cells']
    row = f"{r['week']:<8} {r['filename']:<22} {r['rows']:<8} {r['cols']:<8} {missing_pct:<12.1f}"
    print(row)

print()

# Check sector consistency
print('SECTOR CONSISTENCY CHECK:')
print('-' * 70)
all_sectors = {}
for r in results:
    week = r['week']
    for sector in r['sectors']:
        if sector not in all_sectors:
            all_sectors[sector] = []
        all_sectors[sector].append(week)

print(f'Unique sectors found: {len(all_sectors)}')
print()
print('Sector appearances across weeks:')
for sector, weeks in sorted(all_sectors.items()):
    print(f'  {sector:<40} appears in {len(weeks)}/12 weeks')

print()
print()

# Show sample from first file
print('SAMPLE DATA FROM WEEK 03 (ns-03-1994.csv):')
print('=' * 70)
sample_df = pd.read_csv('OCR/output/table_1/1994/ns-03-1994.csv', sep=';', encoding='utf-8-sig')
print(sample_df.iloc[:5, :8].to_string(index=False))

print()
print()
print('Review complete! Check the results above.')
