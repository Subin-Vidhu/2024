"""
Comprehensive validation of ALL cases against FDA reference data
Compares every metric across the entire dataset
"""

import pandas as pd
import numpy as np
import re

# Load both CSV files
print("Loading CSV files...")
our_csv = 'results/fda_ground_truth_comparison/FDA_GT01_vs_GT02_Comparison_20251216_085819.csv'
fda_csv = 'results/fda_ground_truth_comparison/Aramis Dice Sample - DICE Run.csv'

our_df = pd.read_csv(our_csv)
fda_df = pd.read_csv(fda_csv)

print(f"Our CSV: {len(our_df)} rows")
print(f"FDA CSV: {len(fda_df)} rows")

# Extract case IDs
def extract_case_id_from_filename(filename):
    """Extract case ID from filename"""
    if pd.isna(filename):
        return None
    match = re.search(r'[AN]-?(\d+)', str(filename))
    if match:
        return match.group(1)
    return None

def normalize_case_id(patient_id):
    """Normalize patient ID"""
    if pd.isna(patient_id):
        return None
    match = re.search(r'(\d+)', str(patient_id))
    if match:
        return match.group(1)
    return None

# Filter to kidney rows only (exclude Average and error rows)
our_kidney = our_df[our_df['Organ'].str.contains('Kidney', na=False)].copy()
fda_kidney = fda_df[fda_df['Organ'].str.contains('Kidney', na=False)].copy()

print(f"\nOur kidney rows: {len(our_kidney)}")
print(f"FDA kidney rows: {len(fda_kidney)}")

# Add normalized case IDs
our_kidney['CaseID'] = our_kidney['Patient'].apply(normalize_case_id)
fda_kidney['CaseID'] = fda_kidney['Mask1'].apply(extract_case_id_from_filename)

# Remove duplicates
our_kidney_unique = our_kidney.drop_duplicates(subset=['CaseID', 'Organ'])
fda_kidney_unique = fda_kidney.drop_duplicates(subset=['CaseID', 'Organ'])

print(f"\nAfter deduplication:")
print(f"Our unique kidney rows: {len(our_kidney_unique)}")
print(f"FDA unique kidney rows: {len(fda_kidney_unique)}")

# Merge on CaseID and Organ
merged = pd.merge(
    our_kidney_unique[['CaseID', 'Organ', 'DiceCoefficient', 'GT01_Volume_mm3', 'GT02_Volume_mm3', 
                       'GT01_Volume_cm3', 'GT02_Volume_cm3', 'DiffPercent', 'LargerMask']],
    fda_kidney_unique[['CaseID', 'Organ', 'DiceCoefficient', 'Mask1_Volume_mm3', 'Mask2_Volume_mm3',
                       'Mask1_Volume_mL', 'Mask2_Volume_mL', 'DiffPercent', 'LargerMask']],
    on=['CaseID', 'Organ'],
    suffixes=('_ours', '_fda'),
    how='inner'
)

print(f"\nMatched rows: {len(merged)}")

if len(merged) == 0:
    print("\n❌ ERROR: No rows matched! Check case ID extraction logic.")
    import sys
    sys.exit(1)

# Parse numeric values
def parse_diffpercent(val):
    if pd.isna(val):
        return np.nan
    if isinstance(val, str):
        return float(val.strip('%'))
    return float(val)

merged['DiffPercent_ours_numeric'] = merged['DiffPercent_ours'].apply(parse_diffpercent)
merged['DiffPercent_fda_numeric'] = merged['DiffPercent_fda'].apply(parse_diffpercent)

# Convert Dice to numeric
merged['Dice_ours'] = pd.to_numeric(merged['DiceCoefficient_ours'], errors='coerce')
merged['Dice_fda'] = pd.to_numeric(merged['DiceCoefficient_fda'], errors='coerce')

# Convert volumes to numeric
merged['Vol1_ours'] = pd.to_numeric(merged['GT01_Volume_mm3'], errors='coerce')
merged['Vol1_fda'] = pd.to_numeric(merged['Mask1_Volume_mm3'], errors='coerce')
merged['Vol2_ours'] = pd.to_numeric(merged['GT02_Volume_mm3'], errors='coerce')
merged['Vol2_fda'] = pd.to_numeric(merged['Mask2_Volume_mm3'], errors='coerce')

print("\n" + "=" * 80)
print("COMPREHENSIVE VALIDATION RESULTS")
print("=" * 80)

# 1. DICE COEFFICIENT COMPARISON
print("\n1. DICE COEFFICIENT VALIDATION")
print("-" * 80)
dice_match = np.isclose(merged['Dice_ours'], merged['Dice_fda'], atol=1e-6, rtol=0)
dice_match_count = dice_match.sum()
dice_total = len(merged)
dice_match_pct = (dice_match_count / dice_total * 100) if dice_total > 0 else 0

print(f"Total comparisons: {dice_total}")
print(f"Exact matches (within 1e-6): {dice_match_count}")
print(f"Match rate: {dice_match_pct:.2f}%")

if dice_match_count == dice_total:
    print("✅ PERFECT MATCH - All Dice coefficients match FDA exactly!")
else:
    print(f"❌ MISMATCH - {dice_total - dice_match_count} cases don't match")
    mismatches = merged[~dice_match].head(5)
    print("\nFirst 5 mismatches:")
    for idx, row in mismatches.iterrows():
        print(f"  Case {row['CaseID']} - {row['Organ']}: Ours={row['Dice_ours']:.6f}, FDA={row['Dice_fda']:.6f}")

# 2. VOLUME COMPARISON (mm³)
print("\n2. VOLUME VALIDATION (mm³)")
print("-" * 80)

# Mask1/GT01 Volume
vol1_match = np.isclose(merged['Vol1_ours'], merged['Vol1_fda'], atol=0.01, rtol=0)
vol1_match_count = vol1_match.sum()
vol1_match_pct = (vol1_match_count / dice_total * 100) if dice_total > 0 else 0

print(f"GT01/Mask1 Volume:")
print(f"  Matches (within 0.01 mm³): {vol1_match_count}/{dice_total} ({vol1_match_pct:.2f}%)")

# Mask2/GT02 Volume
vol2_match = np.isclose(merged['Vol2_ours'], merged['Vol2_fda'], atol=0.01, rtol=0)
vol2_match_count = vol2_match.sum()
vol2_match_pct = (vol2_match_count / dice_total * 100) if dice_total > 0 else 0

print(f"GT02/Mask2 Volume:")
print(f"  Matches (within 0.01 mm³): {vol2_match_count}/{dice_total} ({vol2_match_pct:.2f}%)")

if vol1_match_count == dice_total and vol2_match_count == dice_total:
    print("✅ PERFECT MATCH - All volumes match FDA exactly!")
else:
    print(f"❌ MISMATCH - Some volumes don't match")
    if vol1_match_count < dice_total:
        mismatches = merged[~vol1_match].head(3)
        print("\nFirst 3 GT01/Mask1 volume mismatches:")
        for idx, row in mismatches.iterrows():
            print(f"  Case {row['CaseID']} - {row['Organ']}: Ours={row['Vol1_ours']:.2f}, FDA={row['Vol1_fda']:.2f}")

# 3. DIFFPERCENT COMPARISON
print("\n3. DIFFPERCENT VALIDATION")
print("-" * 80)

# Filter out N/A values
valid_diffpercent = merged[~merged['DiffPercent_ours_numeric'].isna() & 
                           ~merged['DiffPercent_fda_numeric'].isna()]

diffpercent_match = np.isclose(valid_diffpercent['DiffPercent_ours_numeric'], 
                                valid_diffpercent['DiffPercent_fda_numeric'], 
                                atol=0.01, rtol=0)
diffpercent_match_count = diffpercent_match.sum()
diffpercent_total = len(valid_diffpercent)
diffpercent_match_pct = (diffpercent_match_count / diffpercent_total * 100) if diffpercent_total > 0 else 0

print(f"Total comparisons: {diffpercent_total}")
print(f"Matches (within 0.01%): {diffpercent_match_count}")
print(f"Match rate: {diffpercent_match_pct:.2f}%")

if diffpercent_match_count == diffpercent_total:
    print("✅ PERFECT MATCH - All DiffPercent values match FDA exactly!")
else:
    print(f"❌ MISMATCH - {diffpercent_total - diffpercent_match_count} cases don't match")
    mismatches = valid_diffpercent[~diffpercent_match].head(5)
    print("\nFirst 5 mismatches:")
    for idx, row in mismatches.iterrows():
        print(f"  Case {row['CaseID']} - {row['Organ']}: Ours={row['DiffPercent_ours_numeric']:.2f}%, FDA={row['DiffPercent_fda_numeric']:.2f}%")

# 4. LARGERMASK COMPARISON
print("\n4. LARGERMASK VALIDATION")
print("-" * 80)

largermask_match = (merged['LargerMask_ours'] == merged['LargerMask_fda'])
largermask_match_count = largermask_match.sum()
largermask_match_pct = (largermask_match_count / dice_total * 100) if dice_total > 0 else 0

print(f"Total comparisons: {dice_total}")
print(f"Exact matches: {largermask_match_count}")
print(f"Match rate: {largermask_match_pct:.2f}%")

if largermask_match_count == dice_total:
    print("✅ PERFECT MATCH - All LargerMask values match FDA exactly!")
else:
    print(f"❌ MISMATCH - {dice_total - largermask_match_count} cases don't match")
    mismatches = merged[~largermask_match].head(5)
    print("\nFirst 5 mismatches:")
    for idx, row in mismatches.iterrows():
        print(f"  Case {row['CaseID']} - {row['Organ']}: Ours={row['LargerMask_ours']}, FDA={row['LargerMask_fda']}")

# 5. AVERAGE ROW VALIDATION
print("\n5. AVERAGE ROW VALIDATION")
print("-" * 80)

our_avg = our_df[our_df['Organ'].str.contains('Average', na=False)].copy()
fda_avg = fda_df[fda_df['Organ'].str.contains('Average', na=False)].copy()

our_avg['CaseID'] = our_avg['Patient'].apply(normalize_case_id)
fda_avg['CaseID'] = fda_avg['Mask1'].apply(extract_case_id_from_filename)

merged_avg = pd.merge(
    our_avg[['CaseID', 'DiceCoefficient']],
    fda_avg[['CaseID', 'DiceCoefficient']],
    on='CaseID',
    suffixes=('_ours', '_fda')
)

merged_avg['Dice_ours'] = pd.to_numeric(merged_avg['DiceCoefficient_ours'], errors='coerce')
merged_avg['Dice_fda'] = pd.to_numeric(merged_avg['DiceCoefficient_fda'], errors='coerce')

avg_match = np.isclose(merged_avg['Dice_ours'], merged_avg['Dice_fda'], atol=1e-6, rtol=0)
avg_match_count = avg_match.sum()
avg_total = len(merged_avg)
avg_match_pct = (avg_match_count / avg_total * 100) if avg_total > 0 else 0

print(f"Total average rows: {avg_total}")
print(f"Exact matches (within 1e-6): {avg_match_count}")
print(f"Match rate: {avg_match_pct:.2f}%")

if avg_match_count == avg_total:
    print("✅ PERFECT MATCH - All Average values match FDA exactly!")
else:
    print(f"❌ MISMATCH - {avg_total - avg_match_count} cases don't match")
    mismatches = merged_avg[~avg_match].head(5)
    print("\nFirst 5 mismatches:")
    for idx, row in mismatches.iterrows():
        print(f"  Case {row['CaseID']}: Ours={row['Dice_ours']:.6f}, FDA={row['Dice_fda']:.6f}")

# FINAL SUMMARY
print("\n" + "=" * 80)
print("FINAL SUMMARY")
print("=" * 80)

all_perfect = (
    dice_match_count == dice_total and
    vol1_match_count == dice_total and
    vol2_match_count == dice_total and
    diffpercent_match_count == diffpercent_total and
    largermask_match_count == dice_total and
    avg_match_count == avg_total
)

print(f"\n{'✅ ALL METRICS MATCH PERFECTLY!' if all_perfect else '⚠️ SOME DISCREPANCIES FOUND'}")
print(f"\nValidation Summary:")
print(f"  Dice Coefficient:  {dice_match_count}/{dice_total} ({dice_match_pct:.1f}%)")
print(f"  Volume (Mask1):    {vol1_match_count}/{dice_total} ({vol1_match_pct:.1f}%)")
print(f"  Volume (Mask2):    {vol2_match_count}/{dice_total} ({vol2_match_pct:.1f}%)")
print(f"  DiffPercent:       {diffpercent_match_count}/{diffpercent_total} ({diffpercent_match_pct:.1f}%)")
print(f"  LargerMask:        {largermask_match_count}/{dice_total} ({largermask_match_pct:.1f}%)")
print(f"  Average:           {avg_match_count}/{avg_total} ({avg_match_pct:.1f}%)")

print(f"\nTotal matched kidney measurements: {dice_total}")
print(f"Total matched average rows: {avg_total}")

if all_perfect:
    print("\n🎉 SUCCESS! Our calculations match FDA's reference data 100%!")
    print("All formulas are correctly implemented and validated.")
else:
    print("\n⚠️ Some metrics don't match. Review the mismatches above.")

print("\n" + "=" * 80)
