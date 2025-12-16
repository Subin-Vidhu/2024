"""
Fixed comprehensive validation preserving A/N prefix
"""

import pandas as pd
import numpy as np
import re

# Load data
our_csv = 'results/fda_ground_truth_comparison/FDA_GT01_vs_GT02_Comparison_20251216_085819.csv'
fda_csv = 'results/fda_ground_truth_comparison/Aramis Dice Sample - DICE Run.csv'

our_df = pd.read_csv(our_csv)
fda_df = pd.read_csv(fda_csv)

print("=" * 80)
print("FINAL COMPREHENSIVE VALIDATION REPORT (FIXED)")
print("=" * 80)

# Extract case IDs with A/N prefix preserved
def extract_case_id_with_prefix(val):
    """Extract case ID preserving A/N prefix"""
    if pd.isna(val):
        return None
    match = re.search(r'([AN]-?\d+)', str(val), re.IGNORECASE)
    if match:
        # Normalize: ensure format is A-XXX or N-XXX
        case_str = match.group(1).upper()
        if '-' not in case_str and len(case_str) > 1:
            # Insert dash: A005 -> A-005
            case_str = case_str[0] + '-' + case_str[1:]
        return case_str
    # If no prefix, just get number
    match = re.search(r'(\d+)', str(val))
    return match.group(1) if match else None

# Process kidney rows
our_kidney = our_df[our_df['Organ'].str.contains('Kidney', na=False)].copy()
fda_kidney = fda_df[fda_df['Organ'].str.contains('Kidney', na=False)].copy()

print(f"\nDataset Size:")
print(f"  Our kidney rows: {len(our_kidney)}")
print(f"  FDA kidney rows: {len(fda_kidney)}")

# Extract CaseIDs with prefix
our_kidney['CaseID'] = our_kidney['Patient'].apply(extract_case_id_with_prefix)
fda_kidney['CaseID'] = fda_kidney['Mask1'].apply(extract_case_id_with_prefix)

# Remove duplicates
our_kidney_unique = our_kidney.drop_duplicates(subset=['CaseID', 'Organ'])
fda_kidney_unique = fda_kidney.drop_duplicates(subset=['CaseID', 'Organ'])

# Merge
merged = pd.merge(
    our_kidney_unique[['CaseID', 'Organ', 'DiceCoefficient', 'DiffPercent']],
    fda_kidney_unique[['CaseID', 'Organ', 'DiceCoefficient', 'DiffPercent']],
    on=['CaseID', 'Organ'],
    suffixes=('_ours', '_fda'),
    how='inner'
)

print(f"  Matched kidney measurements: {len(merged)}")

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

print("\n" + "=" * 80)
print("CRITICAL METRICS VALIDATION")
print("=" * 80)

# 1. Dice Coefficient
dice_match = np.isclose(merged['Dice_ours'], merged['Dice_fda'], atol=1e-6)
dice_match_count = dice_match.sum()
dice_total = len(merged)

print(f"\n1. DICE COEFFICIENT:")
print(f"   Matches: {dice_match_count}/{dice_total} ({dice_match_count/dice_total*100:.2f}%)")
print(f"   Status: {'✅ PERFECT' if dice_match_count == dice_total else '❌ MISMATCH'}")

# 2. DiffPercent
valid_diff = merged[~merged['DiffPct_ours'].isna() & ~merged['DiffPct_fda'].isna()]
diffpct_match = np.isclose(valid_diff['DiffPct_ours'], valid_diff['DiffPct_fda'], atol=0.01)
diffpct_match_count = diffpct_match.sum()
diffpct_total = len(valid_diff)

print(f"\n2. DIFFPERCENT (Maximum Formula):")
print(f"   Matches: {diffpct_match_count}/{diffpct_total} ({diffpct_match_count/diffpct_total*100:.2f}%)")
print(f"   Status: {'✅ PERFECT' if diffpct_match_count == diffpct_total else '❌ MISMATCH'}")

# 3. Average (with proper case ID handling)
our_avg = our_df[our_df['Organ'].str.contains('Average', na=False)].copy()
fda_avg = fda_df[fda_df['Organ'].str.contains('Average', na=False)].copy()

our_avg['CaseID'] = our_avg['Patient'].apply(extract_case_id_with_prefix)
fda_avg['CaseID'] = fda_avg['Mask1'].apply(extract_case_id_with_prefix)

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

print(f"\n3. AVERAGE (Arithmetic Mean):")
print(f"   Matches: {avg_match_count}/{avg_total} ({avg_match_count/avg_total*100:.2f}%)")
print(f"   Status: {'✅ PERFECT' if avg_match_count == avg_total else '❌ MISMATCH'}")

if avg_match_count < avg_total:
    mismatches = merged_avg[~avg_match].head(5)
    print("\n   First 5 mismatches:")
    for _, row in mismatches.iterrows():
        diff = abs(row['Dice_ours'] - row['Dice_fda'])
        print(f"     Case {row['CaseID']}: {row['Dice_ours']:.6f} vs {row['Dice_fda']:.6f} (diff: {diff:.6f})")

print("\n" + "=" * 80)
print("FINAL VERDICT")
print("=" * 80)

critical_perfect = (
    dice_match_count == dice_total and
    diffpct_match_count == diffpct_total and
    avg_match_count == avg_total
)

if critical_perfect:
    print("\n🎉 SUCCESS! ALL CRITICAL METRICS MATCH PERFECTLY!")
    print("\n✅ Validated Metrics (100% Match):")
    print(f"   • Dice Coefficient: {dice_match_count}/{dice_total} measurements")
    print(f"   • DiffPercent: {diffpct_match_count}/{diffpct_total} measurements")
    print(f"   • Average: {avg_match_count}/{avg_total} cases")
    
    print("\n✅ Our implementation correctly uses:")
    print("   1. FDA's Dice coefficient formula (boolean logic)")
    print("   2. FDA's DiffPercent formula (|Vol1-Vol2| / max(Vol1,Vol2) × 100)")
    print("   3. FDA's Average calculation ((Dice_Right + Dice_Left) / 2)")
    
    print("\n✅ FORMULAS ARE VALIDATED AND PRODUCTION-READY!")
else:
    print("\n⚠️ SOME MISMATCHES FOUND")
    print(f"\n   • Dice Coefficient: {dice_match_count}/{dice_total} {'✅' if dice_match_count == dice_total else '❌'}")
    print(f"   • DiffPercent: {diffpct_match_count}/{diffpct_total} {'✅' if diffpct_match_count == diffpct_total else '❌'}")
    print(f"   • Average: {avg_match_count}/{avg_total} {'✅' if avg_match_count == avg_total else '❌'}")

print(f"\n{'='*80}\n")
