"""
Quick analysis script to find mixed GT usage patterns in WCG file
"""
import pandas as pd
import re

# Load WCG file
df = pd.read_csv('66017_WCG_DICE_16Dec2025.csv')

# Clean data
df['Patient'] = df['Patient'].str.strip()
df['Organ'] = df['Organ'].str.strip()

# Extract GT version
df['GT_Version'] = df['Mask2'].str.extract(r'(GT0[12])', flags=re.IGNORECASE)[0].str.upper()

# Find patients with mixed GT usage
patient_gt = df.groupby('Patient')['GT_Version'].unique()
mixed_patients = [p for p, v in patient_gt.items() if len(v) > 1]

print('=' * 80)
print(f'MIXED GT USAGE ANALYSIS - {len(mixed_patients)} CASES FOUND')
print('=' * 80)
print()

for patient in sorted(mixed_patients):
    patient_data = df[df['Patient'] == patient][['Patient', 'Organ', 'DiceCoefficient', 'GT_Version', 'Mask2']]
    print(f'{patient}:')
    for _, row in patient_data.iterrows():
        print(f'  {row["Organ"]:<15} -> {row["GT_Version"]}  (DICE: {row["DiceCoefficient"]:.6f})')
    print()

print('=' * 80)
print('SUMMARY')
print('=' * 80)
print(f'Total unique patients in WCG: {df["Patient"].nunique()}')
print(f'Patients using only GT01: {sum(1 for p, v in patient_gt.items() if len(v) == 1 and "GT01" in v)}')
print(f'Patients using only GT02: {sum(1 for p, v in patient_gt.items() if len(v) == 1 and "GT02" in v)}')
print(f'Patients using MIXED (GT01 + GT02): {len(mixed_patients)}')
print()
print(f'Percentage of mixed cases: {len(mixed_patients) / df["Patient"].nunique() * 100:.1f}%')
