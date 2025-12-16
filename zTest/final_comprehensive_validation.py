"""
FINAL COMPREHENSIVE VALIDATION
Handles case ID matching using filenames to determine A/N prefix
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
print("COMPREHENSIVE VALIDATION: ALL 119 CASES vs FDA REFERENCE")
print("=" * 90)

# Extract full case ID with A/N prefix from filenames
def get_case_id_from_filename(filename):
    """Extract A-XXX or N-XXX from filename"""
    if pd.isna(filename):
        return None
    match = re.search(r'([AN])-?(\d+)', str(filename), re.IGNORECASE)
    if match:
        prefix = match.group(1).upper()
        number = match.group(2)
        return f"{prefix}-{number}"
    return None

# Process kidney rows
our_kidney = our_df[our_df['Organ'].str.contains('Kidney', na=False)].copy()
fda_kidney = fda_df[fda_df['Organ'].str.contains('Kidney', na=False)].copy()

# Get CaseID from GT01/Mask1 filenames
our_kidney['CaseID'] = our_kidney['GT01_File'].apply(get_case_id_from_filename)
fda_kidney['CaseID'] = fda_kidney['Mask1'].apply(get_case_id_from_filename)

# Also try from Mask2 if Mask1 didn't work (for cases where FDA swapped order)
fda_kidney.loc[fda_kidney['CaseID'].isna(), 'CaseID'] = fda_kidney.loc[fda_kidney['CaseID'].isna(), 'Mask2'].apply(get_case_id_from_filename)

print(f"\nDataset Overview:")
print(f"  Our total rows: {len(our_df)}")
print(f"  FDA total rows: {len(fda_df)}")
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

print(f"  Matched kidney measurements: {len(merged)}")

if len(merged) < 200:
    print("\n⚠️ WARNING: Expected ~238 matches (119 cases × 2 kidneys)")
    print(f"   Only matched {len(merged)} measurements")
    
    # Check what's missing
    our_cases = set(our_kidney_unique['CaseID'].dropna())
    fda_cases = set(fda_kidney_unique['CaseID'].dropna())
    missing_in_fda = our_cases - fda_cases
    missing_in_ours = fda_cases - our_cases
    
    if missing_in_fda:
        print(f"\n   Cases in our data but not in FDA: {len(missing_in_fda)}")
        print(f"   Examples: {sorted(list(missing_in_fda))[:10]}")
    if missing_in_ours:
        print(f"\n   Cases in FDA but not in ours: {len(missing_in_ours)}")
        print(f"   Examples: {sorted(list(missing_in_ours))[:10]}")

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
print("VALIDATION RESULTS: CRITICAL FORMULAS")
print("=" * 90)

# 1. Dice Coefficient
dice_match = np.isclose(merged['Dice_ours'], merged['Dice_fda'], atol=1e-6)
dice_match_count = dice_match.sum()
dice_total = len(merged)

print(f"\n✅ DICE COEFFICIENT (Boolean Logic Formula):")
print(f"   • Formula: 2 × |A ∩ B| / (|A| + |B|)")
print(f"   • Matches: {dice_match_count}/{dice_total} ({dice_match_count/dice_total*100:.2f}%)")
print(f"   • Status: {('✅ PERFECT - All values match FDA!' if dice_match_count == dice_total else '❌ MISMATCH')}")

# 2. DiffPercent
valid_diff = merged[~merged['DiffPct_ours'].isna() & ~merged['DiffPct_fda'].isna()]
diffpct_match = np.isclose(valid_diff['DiffPct_ours'], valid_diff['DiffPct_fda'], atol=0.01)
diffpct_match_count = diffpct_match.sum()
diffpct_total = len(valid_diff)

print(f"\n✅ DIFFPERCENT (Maximum Volume Formula):")
print(f"   • Formula: |Vol1 - Vol2| / max(Vol1, Vol2) × 100")
print(f"   • Matches: {diffpct_match_count}/{diffpct_total} ({diffpct_match_count/diffpct_total*100:.2f}%)")
print(f"   • Status: {('✅ PERFECT - All values match FDA!' if diffpct_match_count == diffpct_total else '❌ MISMATCH')}")

# 3. Average
our_avg = our_df[our_df['Organ'].str.contains('Average', na=False)].copy()
fda_avg = fda_df[fda_df['Organ'].str.contains('Average', na=False)].copy()

our_avg['CaseID'] = our_avg['GT01_File'].apply(get_case_id_from_filename)
fda_avg['CaseID'] = fda_avg['Mask1'].apply(get_case_id_from_filename)
fda_avg.loc[fda_avg['CaseID'].isna(), 'CaseID'] = fda_avg.loc[fda_avg['CaseID'].isna(), 'Mask2'].apply(get_case_id_from_filename)

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

print(f"\n✅ AVERAGE (Arithmetic Mean Formula):")
print(f"   • Formula: (Dice_Right + Dice_Left) / 2")
print(f"   • Matches: {avg_match_count}/{avg_total} ({avg_match_count/avg_total*100:.2f}%)")
print(f"   • Status: {('✅ PERFECT - All values match FDA!' if avg_match_count == avg_total else '❌ MISMATCH')}")

print("\n" + "=" * 90)
print("FINAL VALIDATION SUMMARY")
print("=" * 90)

all_perfect = (
    dice_match_count == dice_total and
    diffpct_match_count == diffpct_total and
    avg_match_count == avg_total
)

if all_perfect:
    print("\n🎉 🎉 🎉 SUCCESS! ALL FORMULAS VALIDATED! 🎉 🎉 🎉")
    print("\n" + "✅" * 30)
    print("\n✅ VALIDATION COMPLETE:")
    print(f"   • Dice Coefficient:  {dice_match_count}/{dice_total} measurements (100% match)")
    print(f"   • DiffPercent:       {diffpct_match_count}/{diffpct_total} measurements (100% match)")
    print(f"   • Average:           {avg_match_count}/{avg_total} cases (100% match)")
    
    print("\n✅ CONFIRMED FDA FORMULAS:")
    print("   1. Dice = 2 × |A ∩ B| / (|A| + |B|)  [Boolean logic implementation]")
    print("   2. DiffPercent = |Vol1 - Vol2| / max(Vol1, Vol2) × 100")
    print("   3. Average = (Dice_Right + Dice_Left) / 2  [Arithmetic mean]")
    
    print("\n✅ CODE STATUS: PRODUCTION-READY")
    print("   All calculations match FDA reference data exactly.")
    print("   The script can be used with confidence for validation studies.")
    
    print("\n" + "✅" * 30)
else:
    print("\n⚠️ PARTIAL VALIDATION")
    print(f"\n   • Dice Coefficient: {dice_match_count}/{dice_total} {'✅' if dice_match_count == dice_total else '❌'}")
    print(f"   • DiffPercent: {diffpct_match_count}/{diffpct_total} {'✅' if diffpct_match_count == diffpct_total else '❌'}")
    print(f"   • Average: {avg_match_count}/{avg_total} {'✅' if avg_match_count == avg_total else '❌'}")
    
    if dice_match_count < dice_total or diffpct_match_count < diffpct_total or avg_match_count < avg_total:
        print("\n⚠️ Some metrics don't match. This may be due to:")
        print("   • Different case sets between our run and FDA data")
        print("   • Rounding differences")
        print("   • File ordering differences")

print("\n" + "=" * 90)
print(f"Validation completed for {len(merged)} kidney measurements from {avg_total} cases")
print("=" * 90 + "\n")
