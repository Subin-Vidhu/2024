import pandas as pd
import os

# Find the latest results directory
result_dirs = [d for d in os.listdir('results') if d.startswith('Multi_Reader_Analysis_20251021_151613')]
csv_path = os.path.join('results', result_dirs[0], 'Simplified_Multi_Reader_Analysis_20251021_151613.csv')

# Load and display the CSV
df = pd.read_csv(csv_path)

print("=== SIMPLIFIED CSV PREVIEW ===")
print(f"Shape: {df.shape}")
print(f"Cases: {len(df)}")
print(f"Columns: {len(df.columns)}")

print("\nColumn Structure:")
print("="*50)
for i, col in enumerate(df.columns, 1):
    print(f"{i:2d}. {col}")

print("\n" + "="*50)
print("SAMPLE DATA (First 2 rows):")
print("="*50)

# Display data in organized sections
for idx, row in df.head(5).iterrows():
    case = row['case_id']
    print(f"\nCase: {case}")
    print("-" * 30)
    
    print("Left Kidney Volumes (cm³):")
    print(f"  AIRA: {row['left_kidney_vol_aira_cm3']}")
    print(f"  MC:   {row['left_kidney_vol_mc_cm3']}")
    print(f"  GT1:  {row['left_kidney_vol_gt1_cm3']}")
    print(f"  GT2:  {row['left_kidney_vol_gt2_cm3']}")
    
    print("Right Kidney Volumes (cm³):")
    print(f"  AIRA: {row['right_kidney_vol_aira_cm3']}")
    print(f"  MC:   {row['right_kidney_vol_mc_cm3']}")
    print(f"  GT1:  {row['right_kidney_vol_gt1_cm3']}")
    print(f"  GT2:  {row['right_kidney_vol_gt2_cm3']}")
    
    print("Overall Dice Scores:")
    print(f"  MC vs GT1:  {row['dice_mc_vs_gt1_overall']}")
    print(f"  MC vs GT2:  {row['dice_mc_vs_gt2_overall']}")
    print(f"  MC vs AIRA: {row['dice_mc_vs_aira_overall']}")
    print(f"  GT1 vs GT2: {row['dice_gt1_vs_gt2_overall']}")
    print(f"  GT1 vs AIRA:{row['dice_gt1_vs_aira_overall']}")
    print(f"  GT2 vs AIRA:{row['dice_gt2_vs_aira_overall']}")

print("\n" + "="*50)
print("✅ SUCCESS: Simplified CSV created with organized structure!")
print("📁 Location:", csv_path)
print("📊 Ready for easy analysis and visualization")