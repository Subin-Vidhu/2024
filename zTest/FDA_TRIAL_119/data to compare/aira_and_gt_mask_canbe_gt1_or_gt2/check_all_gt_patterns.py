import pandas as pd

# Load WCG data
wcg_df = pd.read_csv('66017_WCG_DICE_16Dec2025.csv')

print("="*80)
print("COMPLETE GT USAGE ANALYSIS FOR ALL PATIENTS")
print("="*80)

# Total patients
total_patients = wcg_df['Patient'].nunique()
print(f"\nTotal patients in WCG dataset: {total_patients}")

# Extract GT version from Mask2 column
wcg_df['GroundTruth'] = wcg_df['Mask2'].str.extract(r'_(GT\d+)\.nii')[0]

# Group by patient and analyze GT usage
gt_usage = wcg_df.groupby('Patient')['GroundTruth'].apply(lambda x: sorted(set(x)))

# Categorize patients
mixed_gt_patients = []
only_gt01_patients = []
only_gt02_patients = []

for patient, gts in gt_usage.items():
    if len(gts) > 1:
        mixed_gt_patients.append(patient)
    elif gts == ['GT01']:
        only_gt01_patients.append(patient)
    elif gts == ['GT02']:
        only_gt02_patients.append(patient)

print("\n" + "="*80)
print("CATEGORY BREAKDOWN")
print("="*80)

print(f"\n1. Patients with MIXED GT usage (using both GT01 and GT02):")
print(f"   Count: {len(mixed_gt_patients)}")
print(f"   Percentage: {len(mixed_gt_patients)/total_patients*100:.1f}%")
print(f"   Patients: {', '.join(mixed_gt_patients)}")

print(f"\n2. Patients using ONLY GT01:")
print(f"   Count: {len(only_gt01_patients)}")
print(f"   Percentage: {len(only_gt01_patients)/total_patients*100:.1f}%")
if len(only_gt01_patients) <= 20:
    print(f"   Patients: {', '.join(only_gt01_patients)}")
else:
    print(f"   First 20: {', '.join(only_gt01_patients[:20])}")
    print(f"   ... and {len(only_gt01_patients)-20} more")

print(f"\n3. Patients using ONLY GT02:")
print(f"   Count: {len(only_gt02_patients)}")
print(f"   Percentage: {len(only_gt02_patients)/total_patients*100:.1f}%")
if len(only_gt02_patients) <= 20:
    print(f"   Patients: {', '.join(only_gt02_patients)}")
else:
    print(f"   First 20: {', '.join(only_gt02_patients[:20])}")
    print(f"   ... and {len(only_gt02_patients)-20} more")

# Detailed breakdown for mixed GT patients
print("\n" + "="*80)
print("DETAILED MIXED GT PATIENT BREAKDOWN")
print("="*80)

for patient in sorted(mixed_gt_patients):
    patient_data = wcg_df[wcg_df['Patient'] == patient]
    print(f"\n{patient}:")
    for _, row in patient_data.iterrows():
        print(f"  - {row['Organ']:15s} -> {row['GroundTruth']} (DICE: {row['DiceCoefficient']:.6f})")

# Summary statistics
print("\n" + "="*80)
print("SUMMARY STATISTICS")
print("="*80)
print(f"\nTotal entries in WCG: {len(wcg_df)}")
print(f"Total patients: {total_patients}")
print(f"Entries per patient (avg): {len(wcg_df)/total_patients:.1f}")
print(f"\nMixed GT patients: {len(mixed_gt_patients)} ({len(mixed_gt_patients)/total_patients*100:.1f}%)")
print(f"Single GT patients: {len(only_gt01_patients) + len(only_gt02_patients)} ({(len(only_gt01_patients) + len(only_gt02_patients))/total_patients*100:.1f}%)")

print("\n" + "="*80)
print("VALIDATION COMPLETE")
print("="*80)
