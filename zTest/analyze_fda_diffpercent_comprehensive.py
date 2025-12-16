"""
Comprehensive analysis of DiffPercent formula across all 119 cases
Comparing FDA's CSV with our calculations to identify the pattern
"""

import pandas as pd
import numpy as np

# Load both CSV files
our_df = pd.read_csv('results/fda_ground_truth_comparison/FDA_GT01_vs_GT02_Comparison_20251216_083930.csv')
fda_df = pd.read_csv('results/fda_ground_truth_comparison/Aramis Dice Sample - DICE Run.csv')

print("=" * 80)
print("FDA vs Our DiffPercent Formula Analysis - All 119 Cases")
print("=" * 80)

# Filter out Average rows and summary rows
our_kidney_rows = our_df[our_df['Organ'].str.contains('Kidney', na=False)].copy()
fda_kidney_rows = fda_df[fda_df['Organ'].str.contains('Kidney', na=False)].copy()

print(f"\nOur kidney rows: {len(our_kidney_rows)}")
print(f"FDA kidney rows: {len(fda_kidney_rows)}")

# Extract case IDs for matching
def extract_case_id(filename):
    """Extract case ID from filename"""
    import re
    # Match patterns like N-001, A-003, N-227, etc.
    match = re.search(r'([AN]-?\d+)', str(filename))
    if match:
        return match.group(1)
    return None

our_kidney_rows['CaseID'] = our_kidney_rows['Patient'].apply(extract_case_id)
fda_kidney_rows['CaseID'] = fda_kidney_rows['Mask1'].apply(extract_case_id)

# Merge on CaseID and Organ
merged = pd.merge(
    our_kidney_rows[['CaseID', 'Organ', 'DiceCoefficient', 'GT01_Volume_mm3', 'GT02_Volume_mm3', 'DiffPercent', 'LargerMask']],
    fda_kidney_rows[['CaseID', 'Organ', 'DiceCoefficient', 'Mask1_Volume_mm3', 'Mask2_Volume_mm3', 'DiffPercent', 'LargerMask']],
    on=['CaseID', 'Organ'],
    suffixes=('_ours', '_fda')
)

print(f"\nMatched rows: {len(merged)}")

# Calculate different DiffPercent formulas
def calc_diffpercent_methods(row):
    vol1 = row['Mask1_Volume_mm3']
    vol2 = row['Mask2_Volume_mm3']
    
    # Method 1: Average (what we currently use)
    avg = (vol1 + vol2) / 2
    method1 = abs(vol1 - vol2) / avg * 100 if avg > 0 else 0
    
    # Method 2: Larger volume
    max_vol = max(vol1, vol2)
    method2 = abs(vol1 - vol2) / max_vol * 100 if max_vol > 0 else 0
    
    # Method 3: Vol1 (Mask1)
    method3 = abs(vol1 - vol2) / vol1 * 100 if vol1 > 0 else 0
    
    # Method 4: Vol2 (Mask2)
    method4 = abs(vol1 - vol2) / vol2 * 100 if vol2 > 0 else 0
    
    return method1, method2, method3, method4

merged[['Method1_Avg', 'Method2_Max', 'Method3_Vol1', 'Method4_Vol2']] = merged.apply(
    lambda row: pd.Series(calc_diffpercent_methods(row)), axis=1
)

# Compare each method with FDA's values
merged['Method1_Match'] = np.isclose(merged['Method1_Avg'], merged['DiffPercent_fda'], atol=0.01)
merged['Method2_Match'] = np.isclose(merged['Method2_Max'], merged['DiffPercent_fda'], atol=0.01)
merged['Method3_Match'] = np.isclose(merged['Method3_Vol1'], merged['DiffPercent_fda'], atol=0.01)
merged['Method4_Match'] = np.isclose(merged['Method4_Vol2'], merged['DiffPercent_fda'], atol=0.01)

# Count matches for each method
print("\n" + "=" * 80)
print("DIFFPERCENT FORMULA MATCH SUMMARY")
print("=" * 80)

for method in ['Method1', 'Method2', 'Method3', 'Method4']:
    match_count = merged[f'{method}_Match'].sum()
    match_pct = match_count / len(merged) * 100
    method_name = {
        'Method1': 'Average: |Vol1-Vol2| / ((Vol1+Vol2)/2) × 100',
        'Method2': 'Maximum: |Vol1-Vol2| / max(Vol1,Vol2) × 100',
        'Method3': 'Vol1: |Vol1-Vol2| / Vol1 × 100',
        'Method4': 'Vol2: |Vol1-Vol2| / Vol2 × 100'
    }[method]
    
    print(f"\n{method_name}")
    print(f"  Matches: {match_count}/{len(merged)} ({match_pct:.1f}%)")

# Find cases where methods differ
print("\n" + "=" * 80)
print("CASES WHERE FORMULAS DIFFER")
print("=" * 80)

mismatch_cases = merged[~merged['Method2_Match']].copy()

if len(mismatch_cases) > 0:
    print(f"\nFound {len(mismatch_cases)} cases where Method2 (Max) doesn't match FDA")
    print("\nFirst 10 mismatches:")
    for idx, row in mismatch_cases.head(10).iterrows():
        print(f"\n{row['CaseID']} - {row['Organ']}:")
        print(f"  FDA DiffPercent: {row['DiffPercent_fda']:.2f}%")
        print(f"  Our DiffPercent (Avg): {row['DiffPercent_ours']:.2f}%")
        print(f"  Method1 (Avg): {row['Method1_Avg']:.2f}%")
        print(f"  Method2 (Max): {row['Method2_Max']:.2f}%")
        print(f"  Vol1: {row['Mask1_Volume_mm3']:.2f} mm³")
        print(f"  Vol2: {row['Mask2_Volume_mm3']:.2f} mm³")
        print(f"  LargerMask (FDA): {row['LargerMask_fda']}")
else:
    print("\n✅ ALL CASES MATCH! Method2 (Max) is the correct formula.")

# Check if Method2 matches 100%
if merged['Method2_Match'].all():
    print("\n" + "=" * 80)
    print("🎯 CONCLUSION: FDA uses Method2 (Maximum)")
    print("=" * 80)
    print("\nFormula: |Vol1 - Vol2| / max(Vol1, Vol2) × 100")
    print("\nThis formula calculates the difference as a percentage of the LARGER volume.")
    print("This is why cases 001-002 matched both formulas (volumes were nearly equal),")
    print("but case 003 revealed the difference (volumes differ by ~10%).")
    
# Detailed comparison for first 5 cases
print("\n" + "=" * 80)
print("DETAILED COMPARISON - FIRST 5 CASES")
print("=" * 80)

for case_id in ['N-001', 'N-002', 'A-003', 'A-004', 'N-005']:
    case_data = merged[merged['CaseID'] == case_id]
    if len(case_data) == 0:
        continue
    
    print(f"\n{'=' * 40}")
    print(f"CASE {case_id}")
    print(f"{'=' * 40}")
    
    for _, row in case_data.iterrows():
        print(f"\n{row['Organ']}:")
        print(f"  Dice (Ours): {row['DiceCoefficient_ours']:.6f}")
        print(f"  Dice (FDA):  {row['DiceCoefficient_fda']:.6f}")
        print(f"  Match: {'✅' if np.isclose(row['DiceCoefficient_ours'], row['DiceCoefficient_fda'], atol=0.000001) else '❌'}")
        
        print(f"\n  Volume1: {row['Mask1_Volume_mm3']:.2f} mm³")
        print(f"  Volume2: {row['Mask2_Volume_mm3']:.2f} mm³")
        print(f"  Larger: {row['LargerMask_fda']}")
        
        print(f"\n  DiffPercent (Ours): {row['DiffPercent_ours']:.2f}%")
        print(f"  DiffPercent (FDA):  {row['DiffPercent_fda']:.2f}%")
        print(f"  Method1 (Avg):      {row['Method1_Avg']:.2f}% {'✅' if row['Method1_Match'] else '❌'}")
        print(f"  Method2 (Max):      {row['Method2_Max']:.2f}% {'✅' if row['Method2_Match'] else '❌'}")

print("\n" + "=" * 80)
print("ANALYSIS COMPLETE")
print("=" * 80)
