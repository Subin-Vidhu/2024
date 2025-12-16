"""
FINAL VALIDATION: Properly handling N-prefix (missing) and A-prefix (present)
"""

import pandas as pd
import numpy as np
import re

# Load data
our_csv = 'results/fda_ground_truth_comparison/FDA_GT01_vs_GT02_Comparison_20251216_085819.csv'
fda_csv = 'results/fda_ground_truth_comparison/Aramis Dice Sample - DICE Run.csv'

our_df = pd.read_csv(our_csv)
fda_df = pd.read_csv(fda_csv)

print("=" * 90)
print("COMPREHENSIVE VALIDATION: ALL CASES vs FDA REFERENCE")
print("=" * 90)

# Fix Patient IDs: Add N- prefix to numeric-only IDs, keep A- as-is
def normalize_patient_id(patient_id, gt01_file):
    """
    Normalize patient ID to match FDA format:
    - If patient_id is just numbers (e.g., '001'), add 'N-' prefix
    - If patient_id already has A- prefix, keep it
    - Use filename as fallback
    """
    if pd.isna(patient_id):
        # Extract from filename
        match = re.search(r'([AN]-\d+)', str(gt01_file), re.IGNORECASE)
        if match:
            return match.group(1).upper()
        return None
    
    patient_str = str(patient_id).strip()
    
    # Check if it's just numbers
    if re.match(r'^\d+$', patient_str):
        return f"N-{patient_str}"
    
    # Already has prefix (A-xxx)
    if re.match(r'^[AN]-', patient_str, re.IGNORECASE):
        return patient_str.upper()
    
    # Fallback: extract from filename
    match = re.search(r'([AN]-\d+)', str(gt01_file), re.IGNORECASE)
    if match:
        return match.group(1).upper()
    
    return patient_str

# Process kidney rows
our_kidney = our_df[our_df['Organ'].str.contains('Kidney', na=False)].copy()
fda_kidney = fda_df[fda_df['Organ'].str.contains('Kidney', na=False)].copy()

# Normalize case IDs
our_kidney['CaseID'] = our_kidney.apply(lambda row: normalize_patient_id(row['Patient'], row['GT01_File']), axis=1)

# Extract FDA case IDs from Mask1 (or Mask2 if swapped)
def extract_fda_case_id(mask1_file, mask2_file):
    """Extract case ID from FDA mask files"""
    for filename in [mask1_file, mask2_file]:
        if pd.isna(filename):
            continue
        match = re.search(r'([AN]-\d+)', str(filename), re.IGNORECASE)
        if match:
            return match.group(1).upper()
    return None

fda_kidney['CaseID'] = fda_kidney.apply(lambda row: extract_fda_case_id(row['Mask1'], row['Mask2']), axis=1)

print(f"\nDataset Overview:")
print(f"  Our kidney rows: {len(our_kidney)}")
print(f"  FDA kidney rows: {len(fda_kidney)}")
print(f"  Our unique cases: {our_kidney['CaseID'].nunique()}")
print(f"  FDA unique cases: {fda_kidney['CaseID'].nunique()}")

# Remove duplicates
our_kidney_unique = our_kidney.drop_duplicates(subset=['CaseID', 'Organ'])
fda_kidney_unique = fda_kidney.drop_duplicates(subset=['CaseID', 'Organ'])

print(f"  Our unique kidney measurements: {len(our_kidney_unique)}")
print(f"  FDA unique kidney measurements: {len(fda_kidney_unique)}")

# Merge
merged = pd.merge(
    our_kidney_unique[['CaseID', 'Organ', 'DiceCoefficient', 'DiffPercent']],
    fda_kidney_unique[['CaseID', 'Organ', 'DiceCoefficient', 'DiffPercent']],
    on=['CaseID', 'Organ'],
    suffixes=('_ours', '_fda'),
    how='inner'
)

print(f"  ✅ Successfully matched: {len(merged)} kidney measurements")

# Check coverage
our_cases = set(our_kidney_unique['CaseID'].dropna())
fda_cases = set(fda_kidney_unique['CaseID'].dropna())
common_cases = our_cases & fda_cases
missing_in_fda = our_cases - fda_cases
missing_in_ours = fda_cases - our_cases

print(f"\n  Coverage Analysis:")
print(f"    Common cases: {len(common_cases)}")
if missing_in_fda:
    print(f"    In our data but not FDA: {len(missing_in_fda)} cases")
if missing_in_ours:
    print(f"    In FDA but not ours: {len(missing_in_ours)} cases")

# Parse values
def parse_diffpercent(val):
    if pd.isna(val):
        return np.nan
    if isinstance(val, str):
        return float(val.strip('%'))
    return float(val)

merged['Dice_ours'] = pd.to_numeric(merged['DiceCoefficient_ours'], errors='coerce')
merged['Dice_fda'] = pd.to_numeric(merged['DiceCoefficient_fda'], errors='coerce')
merged['DiffPct_ours'] = merged['DiffPercent_ours'].apply(parse_diffpercent)
merged['DiffPct_fda'] = merged['DiffPercent_fda'].apply(parse_diffpercent)

print("\n" + "=" * 90)
print("VALIDATION RESULTS")
print("=" * 90)

# 1. Dice Coefficient
dice_match = np.isclose(merged['Dice_ours'], merged['Dice_fda'], atol=1e-6)
dice_match_count = dice_match.sum()
dice_total = len(merged)

print(f"\n1. DICE COEFFICIENT:")
print(f"   Formula: 2 × |A ∩ B| / (|A| + |B|)")
print(f"   Matches: {dice_match_count}/{dice_total} ({dice_match_count/dice_total*100:.2f}%)")
print(f"   {'✅ PERFECT MATCH' if dice_match_count == dice_total else '❌ MISMATCH'}")

# 2. DiffPercent
valid_diff = merged[~merged['DiffPct_ours'].isna() & ~merged['DiffPct_fda'].isna()]
diffpct_match = np.isclose(valid_diff['DiffPct_ours'], valid_diff['DiffPct_fda'], atol=0.01)
diffpct_match_count = diffpct_match.sum()
diffpct_total = len(valid_diff)

print(f"\n2. DIFFPERCENT:")
print(f"   Formula: |Vol1 - Vol2| / max(Vol1, Vol2) × 100")
print(f"   Matches: {diffpct_match_count}/{diffpct_total} ({diffpct_match_count/diffpct_total*100:.2f}%)")
print(f"   {'✅ PERFECT MATCH' if diffpct_match_count == diffpct_total else '❌ MISMATCH'}")

# 3. Average
our_avg = our_df[our_df['Organ'].str.contains('Average', na=False)].copy()
fda_avg = fda_df[fda_df['Organ'].str.contains('Average', na=False)].copy()

our_avg['CaseID'] = our_avg.apply(lambda row: normalize_patient_id(row['Patient'], row['GT01_File']), axis=1)
fda_avg['CaseID'] = fda_avg.apply(lambda row: extract_fda_case_id(row['Mask1'], row['Mask2']), axis=1)

merged_avg = pd.merge(
    our_avg[['CaseID', 'DiceCoefficient']],
    fda_avg[['CaseID', 'DiceCoefficient']],
    on='CaseID',
    suffixes=('_ours', '_fda'),
    how='inner'
)

merged_avg['Dice_ours'] = pd.to_numeric(merged_avg['DiceCoefficient_ours'], errors='coerce')
merged_avg['Dice_fda'] = pd.to_numeric(merged_avg['DiceCoefficient_fda'], errors='coerce')

avg_match = np.isclose(merged_avg['Dice_ours'], merged_avg['Dice_fda'], atol=1e-6)
avg_match_count = avg_match.sum()
avg_total = len(merged_avg)

print(f"\n3. AVERAGE:")
print(f"   Formula: (Dice_Right + Dice_Left) / 2")
print(f"   Matches: {avg_match_count}/{avg_total} ({avg_match_count/avg_total*100:.2f}%)")
print(f"   {'✅ PERFECT MATCH' if avg_match_count == avg_total else '❌ MISMATCH'}")

print("\n" + "=" * 90)
print("FINAL SUMMARY")
print("=" * 90)

all_perfect = (
    dice_match_count == dice_total and
    diffpct_match_count == diffpct_total and
    avg_match_count == avg_total
)

if all_perfect:
    print("\n" + "🎉" * 30)
    print("\n✅ SUCCESS! ALL FORMULAS MATCH FDA 100%!")
    print("\n" + "✅" * 30)
    print(f"\n   • Dice Coefficient:  {dice_match_count}/{dice_total} measurements ✅")
    print(f"   • DiffPercent:       {diffpct_match_count}/{diffpct_total} measurements ✅")
    print(f"   • Average:           {avg_match_count}/{avg_total} cases ✅")
    
    print("\n✅ VALIDATED FORMULAS:")
    print("   1. Dice = 2 × |A ∩ B| / (|A| + |B|)")
    print("   2. DiffPercent = |Vol1 - Vol2| / max(Vol1, Vol2) × 100")
    print("   3. Average = (Dice_Right + Dice_Left) / 2")
    
    print("\n✅ CODE IS PRODUCTION-READY!")
    print("\n" + "🎉" * 30)
else:
    print(f"\n⚠️ VALIDATION RESULTS:")
    print(f"   • Dice Coefficient: {dice_match_count}/{dice_total} {'✅' if dice_match_count == dice_total else '❌'}")
    print(f"   • DiffPercent: {diffpct_match_count}/{diffpct_total} {'✅' if diffpct_match_count == diffpct_total else '❌'}")
    print(f"   • Average: {avg_match_count}/{avg_total} {'✅' if avg_match_count == avg_total else '❌'}")

print("\n" + "=" * 90)
print(f"Validated {len(merged)} kidney measurements from {len(common_cases)} cases")
print("=" * 90 + "\n")
