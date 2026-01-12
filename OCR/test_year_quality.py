"""
Test OCR quality on sample PDFs from different years.
"""
import sys
sys.path.insert(0, '.')

from pathlib import Path
from OCR.ocr_config.settings import load_settings
from OCR.ocr_processors.image_preprocessor import ImagePreprocessor
from OCR.ocr_processors.table_extractor import extract_upper_table
from OCR.ocr_processors.ocr_engine import run_ocr_with_validation
from OCR.ocr_processors.csv_converter import convert_ocr_to_csv
import pandas as pd

# Test years (mid to late period)
test_cases = [
    ('OCR/raw/2005/ns_04_2005.pdf', 2005),
    ('OCR/raw/2008/ns_04_2008.pdf', 2008),
    ('OCR/raw/2010/ns_04_2010.pdf', 2010),
    ('OCR/raw/2011/ns_04_2011.pdf', 2011),
    ('OCR/raw/2012/ns_04_2012.pdf', 2012),
]

# Load settings
settings = load_settings('OCR/ocr_config/config.yaml')

# Initialize preprocessor
preprocessor = ImagePreprocessor(
    target_dpi=settings.preprocessing.target_dpi,
    apply_clahe=settings.preprocessing.contrast_enhancement,
    clahe_clip_limit=settings.preprocessing.clahe_clip_limit
)

print('=' * 70)
print('OCR QUALITY TEST - MID TO LATE PERIOD (2005-2012)')
print('=' * 70)
print()

results = []

for pdf_path, year in test_cases:
    if not Path(pdf_path).exists():
        print(f'{year}: PDF not found - SKIP')
        continue

    print(f'Testing {year} - {Path(pdf_path).name}...')

    try:
        # Preprocess
        preprocessed_image = preprocessor.preprocess_for_ocr(
            str(pdf_path),
            page_num=0,
            save_intermediate=False
        )

        # Extract table
        table_region = extract_upper_table(preprocessed_image)

        # Run OCR
        ocr_result = run_ocr_with_validation(
            table_region,
            language=settings.tesseract.language,
            psm=settings.tesseract.psm,
            oem=settings.tesseract.oem
        )

        # Convert to CSV
        output_csv = f'OCR/output/test_{year}.csv'
        df = convert_ocr_to_csv(ocr_result['text'], output_csv, table_type='table_1')

        # Calculate quality metrics
        missing_pct = 100 * df.isnull().sum().sum() / (df.shape[0] * df.shape[1])

        result = {
            'year': year,
            'confidence': ocr_result['confidence'],
            'sectors': len(df),
            'columns': len(df.columns),
            'missing_pct': missing_pct,
            'text_length': len(ocr_result['text']),
            'status': 'SUCCESS'
        }

        print(f'  Confidence: {result["confidence"]:.1f}%')
        print(f'  Sectors: {result["sectors"]}')
        print(f'  Missing: {result["missing_pct"]:.1f}%')
        print()

    except Exception as e:
        result = {
            'year': year,
            'status': 'FAILED',
            'error': str(e)
        }
        print(f'  FAILED: {e}')
        print()

    results.append(result)

# Summary
print()
print('=' * 70)
print('SUMMARY - BEST TO WORST')
print('=' * 70)

successful = [r for r in results if r['status'] == 'SUCCESS']
successful.sort(key=lambda x: (-x['confidence'], x['missing_pct']))

header = f"{'Year':<8} {'Confidence':<12} {'Sectors':<10} {'Missing %':<12} {'Quality':<15}"
print(header)
print('-' * 70)

for r in successful:
    # Quality rating
    if r['confidence'] > 80 and r['missing_pct'] < 10:
        quality = 'EXCELLENT'
    elif r['confidence'] > 70 and r['missing_pct'] < 15:
        quality = 'GOOD'
    elif r['confidence'] > 60 and r['missing_pct'] < 20:
        quality = 'FAIR'
    else:
        quality = 'POOR'

    row = f"{r['year']:<8} {r['confidence']:<12.1f} {r['sectors']:<10} {r['missing_pct']:<12.1f} {quality:<15}"
    print(row)

print()
print('RECOMMENDATION:')
if successful:
    best = successful[0]
    print(f"  Best year for OCR demonstration: {best['year']}")
    print(f"  Confidence: {best['confidence']:.1f}%, Missing: {best['missing_pct']:.1f}%, Sectors: {best['sectors']}")
print()
