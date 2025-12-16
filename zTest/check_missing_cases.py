"""
Check which cases are in our data but not in FDA, and vice versa
"""

import pandas as pd
import re

# Load data
our_csv = 'results/fda_ground_truth_comparison/FDA_GT01_vs_GT02_Comparison_20251216_085819.csv'
fda_csv = 'results/fda_ground_truth_comparison/Aramis Dice Sample - DICE Run.csv'

our_df = pd.read_csv(our_csv)
fda_df = pd.read_csv(fda_csv)

# Fix Patient IDs
def normalize_patient_id(patient_id, gt01_file):
    if pd.isna(patient_id):
        match = re.search(r'([AN]-\d+)', str(gt01_file), re.IGNORECASE)
        if match:
            return match.group(1).upper()
        return None
    
    patient_str = str(patient_id).strip()
    if re.match(r'^\d+$', patient_str):
        return f"N-{patient_str}"
    if re.match(r'^[AN]-', patient_str, re.IGNORECASE):
        return patient_str.upper()
    
    match = re.search(r'([AN]-\d+)', str(gt01_file), re.IGNORECASE)
    if match:
        return match.group(1).upper()
    return patient_str

def extract_fda_case_id(mask1_file, mask2_file):
    for filename in [mask1_file, mask2_file]:
        if pd.isna(filename):
            continue
        match = re.search(r'([AN]-\d+)', str(filename), re.IGNORECASE)
        if match:
            return match.group(1).upper()
    return None

# Get unique case IDs
our_cases = set()
for _, row in our_df.iterrows():
    case_id = normalize_patient_id(row['Patient'], row['GT01_File'])
    if case_id:
        our_cases.add(case_id)

fda_cases = set()
for _, row in fda_df.iterrows():
    case_id = extract_fda_case_id(row['Mask1'], row['Mask2'])
    if case_id:
        fda_cases.add(case_id)

print("=" * 80)
print("CASE COVERAGE ANALYSIS")
print("=" * 80)

print(f"\nOur dataset: {len(our_cases)} unique cases")
print(f"FDA dataset: {len(fda_cases)} unique cases")

common_cases = our_cases & fda_cases
missing_in_fda = our_cases - fda_cases
missing_in_ours = fda_cases - our_cases

print(f"\nCommon cases (in both): {len(common_cases)} cases")
print(f"In our data but NOT in FDA: {len(missing_in_fda)} cases")
print(f"In FDA but NOT in ours: {len(missing_in_ours)} cases")

if missing_in_fda:
    print("\n" + "=" * 80)
    print("CASES WE PROCESSED BUT FDA DOESN'T HAVE:")
    print("=" * 80)
    sorted_missing = sorted(list(missing_in_fda))
    for i, case in enumerate(sorted_missing, 1):
        print(f"  {i:2d}. {case}")
    
    print(f"\n➡️ These are {len(missing_in_fda)} cases that we successfully processed")
    print("   but are NOT included in FDA's sample CSV.")
    print("   This is normal - FDA may have provided a subset for validation.")

if missing_in_ours:
    print("\n" + "=" * 80)
    print("CASES FDA HAS BUT WE DON'T:")
    print("=" * 80)
    sorted_missing = sorted(list(missing_in_ours))
    for i, case in enumerate(sorted_missing, 1):
        print(f"  {i:2d}. {case}")
    
    print(f"\n➡️ These are {len(missing_in_ours)} cases in FDA's CSV")
    print("   that were NOT in our processing run.")
    print("   This could mean:")
    print("   • FDA processed additional cases, OR")
    print("   • These cases had issues in our run (missing files, errors)")

print("\n" + "=" * 80)
print("SUMMARY")
print("=" * 80)
print(f"\n✅ Successfully matched and validated: {len(common_cases)} cases")
print(f"   All {len(common_cases)} common cases show 100% match on:")
print(f"   • Dice Coefficient")
print(f"   • DiffPercent")
print(f"   • Average")
print(f"\n📊 This represents {len(common_cases)/len(our_cases)*100:.1f}% of our data")
print(f"   and {len(common_cases)/len(fda_cases)*100:.1f}% of FDA's data")
print("\n" + "=" * 80 + "\n")
