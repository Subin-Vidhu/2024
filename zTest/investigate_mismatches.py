import pandas as pd
import numpy as np

# Load data
our_csv = 'results/fda_ground_truth_comparison/FDA_GT01_vs_GT02_Comparison_20251216_085819.csv'
fda_csv = 'results/fda_ground_truth_comparison/Aramis Dice Sample - DICE Run.csv'

our_df = pd.read_csv(our_csv)
fda_df = pd.read_csv(fda_csv)

# Check Case 010 - First LargerMask mismatch
print("INVESTIGATING CASE 010 (LargerMask Mismatch)")
print("=" * 70)

our_010 = our_df[our_df['Patient'] == '010']
fda_010 = fda_df[fda_df['Mask1'].str.contains('010', na=False)]

print("\nOUR DATA (Case 010):")
print(our_010[['Organ', 'GT01_File', 'GT02_File', 'GT01_Volume_cm3', 'GT02_Volume_cm3', 'LargerMask']].to_string(index=False))

print("\nFDA DATA (Case 010):")
print(fda_010[['Organ', 'Mask1', 'Mask2', 'Mask1_Volume_mL', 'Mask2_Volume_mL', 'LargerMask']].head(2).to_string(index=False))

print("\n" + "=" * 70)
print("INVESTIGATING FILE NAME ORDER")
print("=" * 70)

# Check if file names are swapped
print("\nCase 010 Files:")
print(f"Our GT01: {our_010.iloc[0]['GT01_File']}")
print(f"Our GT02: {our_010.iloc[0]['GT02_File']}")
print(f"FDA Mask1: {fda_010.iloc[0]['Mask1']}")
print(f"FDA Mask2: {fda_010.iloc[0]['Mask2']}")

print("\nVolume Comparison:")
print(f"Our GT01 Right: {our_010.iloc[0]['GT01_Volume_cm3']} cm³")
print(f"Our GT02 Right: {our_010.iloc[0]['GT02_Volume_cm3']} cm³")
print(f"FDA Mask1 Right: {fda_010.iloc[0]['Mask1_Volume_mL']} mL")
print(f"FDA Mask2 Right: {fda_010.iloc[0]['Mask2_Volume_mL']} mL")

# Check if volumes match cross-ways
our_gt01_vol = float(our_010.iloc[0]['GT01_Volume_cm3'])
our_gt02_vol = float(our_010.iloc[0]['GT02_Volume_cm3'])
fda_mask1_vol = float(fda_010.iloc[0]['Mask1_Volume_mL'])
fda_mask2_vol = float(fda_010.iloc[0]['Mask2_Volume_mL'])

print("\n" + "=" * 70)
print("VOLUME MATCH ANALYSIS")
print("=" * 70)

if np.isclose(our_gt01_vol, fda_mask1_vol, atol=0.1):
    print("✅ Our GT01 matches FDA Mask1")
elif np.isclose(our_gt01_vol, fda_mask2_vol, atol=0.1):
    print("⚠️ Our GT01 matches FDA Mask2 (FILES SWAPPED!)")

if np.isclose(our_gt02_vol, fda_mask2_vol, atol=0.1):
    print("✅ Our GT02 matches FDA Mask2")
elif np.isclose(our_gt02_vol, fda_mask1_vol, atol=0.1):
    print("⚠️ Our GT02 matches FDA Mask1 (FILES SWAPPED!)")

print("\n" + "=" * 70)
print("CHECKING MULTIPLE CASES FOR FILE NAME PATTERN")
print("=" * 70)

# Check several cases
for case_id in ['010', '015', '016', '023', '024']:
    our_case = our_df[our_df['Patient'] == case_id]
    fda_case = fda_df[fda_df['Mask1'].str.contains(case_id, na=False)]
    
    if len(our_case) == 0 or len(fda_case) == 0:
        continue
    
    print(f"\nCase {case_id}:")
    print(f"  Our: {our_case.iloc[0]['GT01_File']} vs {our_case.iloc[0]['GT02_File']}")
    print(f"  FDA: {fda_case.iloc[0]['Mask1']} vs {fda_case.iloc[0]['Mask2']}")
    
    # Check if files contain GT01/GT02 in swapped order
    our_gt01_file = str(our_case.iloc[0]['GT01_File'])
    our_gt02_file = str(our_case.iloc[0]['GT02_File'])
    fda_mask1_file = str(fda_case.iloc[0]['Mask1'])
    fda_mask2_file = str(fda_case.iloc[0]['Mask2'])
    
    if 'GT02' in our_gt01_file or 'GT01' in our_gt02_file:
        print("  ⚠️ WARNING: Our file names may be swapped!")
    
    if 'GT02' in fda_mask1_file or 'GT01' in fda_mask2_file:
        print("  ⚠️ WARNING: FDA file names may be swapped!")
