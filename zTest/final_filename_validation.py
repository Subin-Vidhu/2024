"""
CORRECTED VALIDATION: Extract case IDs directly from filenames
This handles both A and N cases that may be missing prefixes in Patient column
Uses shared utilities from fda_utils.py for consistency across scripts
"""

import pandas as pd
import numpy as np
from fda_utils import (
    extract_case_from_filename,
    parse_diffpercent,
    load_and_prepare_kidney_data,
    load_and_prepare_average_data,
    validate_dice_match,
    validate_diffpercent_match,
    print_validation_summary
)

# Load data
our_csv = 'results/fda_ground_truth_comparison/FDA_GT01_vs_GT02_Comparison_20251216_085819.csv'
fda_csv = 'results/fda_ground_truth_comparison/Aramis Dice Sample - DICE Run.csv'

our_df = pd.read_csv(our_csv)
fda_df = pd.read_csv(fda_csv)

print("=" * 90)
print("COMPREHENSIVE VALIDATION: Using Filenames for Case ID Extraction")
print("=" * 90)

# Process kidney rows using shared utility
our_kidney = load_and_prepare_kidney_data(our_csv, case_id_source='filename')
fda_kidney = load_and_prepare_kidney_data(fda_csv, case_id_source='filename')

print(f"\nDataset Overview:")
print(f"  Our kidney rows: {len(our_kidney)}")
print(f"  FDA kidney rows: {len(fda_kidney)}")
print(f"  Our unique cases: {our_kidney['CaseID'].nunique()}")
print(f"  FDA unique cases: {fda_kidney['CaseID'].nunique()}")

# Check for any missing case IDs
our_missing = our_kidney[our_kidney['CaseID'].isna()]
fda_missing = fda_kidney[fda_kidney['CaseID'].isna()]

if len(our_missing) > 0:
    print(f"\n  ⚠️ Warning: {len(our_missing)} rows in our data have no case ID")
if len(fda_missing) > 0:
    print(f"  ⚠️ Warning: {len(fda_missing)} rows in FDA data have no case ID")

# Remove duplicates
our_kidney_unique = our_kidney.drop_duplicates(subset=['CaseID', 'Organ'])
fda_kidney_unique = fda_kidney.drop_duplicates(subset=['CaseID', 'Organ'])

print(f"  Our unique kidney measurements: {len(our_kidney_unique)}")
print(f"  FDA unique kidney measurements: {len(fda_kidney_unique)}")

# Merge on CaseID and Organ
merged = pd.merge(
    our_kidney_unique[['CaseID', 'Organ', 'DiceCoefficient', 'DiffPercent']],
    fda_kidney_unique[['CaseID', 'Organ', 'DiceCoefficient', 'DiffPercent']],
    on=['CaseID', 'Organ'],
    suffixes=('_ours', '_fda'),
    how='inner'
)

print(f"  ✅ Successfully matched: {len(merged)} kidney measurements")

# Coverage analysis
our_cases = set(our_kidney_unique['CaseID'].dropna())
fda_cases = set(fda_kidney_unique['CaseID'].dropna())
common_cases = our_cases & fda_cases
missing_in_fda = our_cases - fda_cases
missing_in_ours = fda_cases - our_cases

print(f"\n  Coverage:")
print(f"    Common cases: {len(common_cases)}")
print(f"    In our data only: {len(missing_in_fda)} cases")
print(f"    In FDA only: {len(missing_in_ours)} cases")

if missing_in_fda:
    print(f"\n    Cases we have but FDA doesn't: {sorted(list(missing_in_fda))}")
if missing_in_ours:
    print(f"\n    Cases FDA has but we don't: {sorted(list(missing_in_ours))}")

# Parse values using shared utility
merged['Dice_ours'] = pd.to_numeric(merged['DiceCoefficient_ours'], errors='coerce')
merged['Dice_fda'] = pd.to_numeric(merged['DiceCoefficient_fda'], errors='coerce')
merged['DiffPct_ours'] = merged['DiffPercent_ours'].apply(parse_diffpercent)
merged['DiffPct_fda'] = merged['DiffPercent_fda'].apply(parse_diffpercent)

print("\n" + "=" * 90)
print("VALIDATION RESULTS")
print("=" * 90)

# 1. Dice Coefficient (using shared validation)
dice_match = validate_dice_match(merged['Dice_ours'], merged['Dice_fda'])
dice_match_count = dice_match.sum()
dice_total = len(merged)

print(f"\n1. DICE COEFFICIENT:")
print(f"   Matches: {dice_match_count}/{dice_total} ({dice_match_count/dice_total*100:.2f}%)")
print(f"   {'✅ PERFECT' if dice_match_count == dice_total else '❌ MISMATCH'}")

if dice_match_count < dice_total:
    mismatches = merged[~dice_match].head(3)
    print("\n   First 3 mismatches:")
    for _, row in mismatches.iterrows():
        print(f"     {row['CaseID']} - {row['Organ']}: {row['Dice_ours']:.6f} vs {row['Dice_fda']:.6f}")

# 2. DiffPercent (using shared validation)
valid_diff = merged[~merged['DiffPct_ours'].isna() & ~merged['DiffPct_fda'].isna()]
diffpct_match = validate_diffpercent_match(valid_diff['DiffPct_ours'], valid_diff['DiffPct_fda'])
diffpct_match_count = diffpct_match.sum()
diffpct_total = len(valid_diff)

print(f"\n2. DIFFPERCENT:")
print(f"   Matches: {diffpct_match_count}/{diffpct_total} ({diffpct_match_count/diffpct_total*100:.2f}%)")
print(f"   {'✅ PERFECT' if diffpct_match_count == diffpct_total else '❌ MISMATCH'}")

if diffpct_match_count < diffpct_total:
    mismatches = valid_diff[~diffpct_match].head(3)
    print("\n   First 3 mismatches:")
    for _, row in mismatches.iterrows():
        print(f"     {row['CaseID']} - {row['Organ']}: {row['DiffPct_ours']:.2f}% vs {row['DiffPct_fda']:.2f}%")

# 3. Average (using shared utility)
our_avg = load_and_prepare_average_data(our_csv, case_id_source='filename')
fda_avg = load_and_prepare_average_data(fda_csv, case_id_source='filename')

merged_avg = pd.merge(
    our_avg[['CaseID', 'DiceCoefficient']],
    fda_avg[['CaseID', 'DiceCoefficient']],
    on='CaseID',
    suffixes=('_ours', '_fda'),
    how='inner'
)

merged_avg['Dice_ours'] = pd.to_numeric(merged_avg['DiceCoefficient_ours'], errors='coerce')
merged_avg['Dice_fda'] = pd.to_numeric(merged_avg['DiceCoefficient_fda'], errors='coerce')

avg_match = validate_dice_match(merged_avg['Dice_ours'], merged_avg['Dice_fda'])
avg_match_count = avg_match.sum()
avg_total = len(merged_avg)

print(f"\n3. AVERAGE:")
print(f"   Matches: {avg_match_count}/{avg_total} ({avg_match_count/avg_total*100:.2f}%)")
print(f"   {'✅ PERFECT' if avg_match_count == avg_total else '❌ MISMATCH'}")

if avg_match_count < avg_total:
    mismatches = merged_avg[~avg_match].head(3)
    print("\n   First 3 mismatches:")
    for _, row in mismatches.iterrows():
        print(f"     {row['CaseID']}: {row['Dice_ours']:.6f} vs {row['Dice_fda']:.6f}")

# Print summary using shared utility
print_validation_summary(
    dice_match_count, diffpct_match_count, avg_match_count,
    dice_total, diffpct_total, avg_total,
    len(common_cases)
)
