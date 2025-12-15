#!/usr/bin/env python3
"""
Analyze findings from AIRA vs Annotators comparison
Extract cases with >10%, >15%, >20%, and >25% differences
"""

import pandas as pd
import os
from glob import glob

# Find the most recent Excel file
result_dir = r'd:\2024\zTest\results\aira_vs_annotators_csv'
excel_files = glob(os.path.join(result_dir, 'AIRA_vs_Annotators_*.xlsx'))
latest_file = max(excel_files, key=os.path.getctime)

print("=" * 100)
print("FINDINGS: CASES WITH SIGNIFICANT VOLUME DIFFERENCES")
print("=" * 100)
print(f"Analyzing: {os.path.basename(latest_file)}\n")

def analyze_differences(df, scenario_name):
    """Analyze and report cases with significant differences"""
    
    print("\n" + "=" * 100)
    print(f"SCENARIO: {scenario_name}")
    print("=" * 100)
    
    # Convert percentage columns to numeric
    for col in ['Right_Kidney_Diff_%', 'Left_Kidney_Diff_%', 'Total_Kidney_Diff_%']:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
    
    # Filter valid rows (has data)
    valid_df = df[
        (df['AIRA_Right_Kidney_Vol_cm3'] != '') & 
        (df['FDA_Right_Kidney_Vol_cm3'] != '')
    ].copy()
    
    if len(valid_df) == 0:
        print("No valid data found!")
        return
    
    thresholds = [10, 15, 20, 25]
    
    for threshold in thresholds:
        print(f"\n{'─' * 100}")
        print(f"Cases with >{threshold}% Difference:")
        print(f"{'─' * 100}")
        
        # Right Kidney
        right_cases = valid_df[abs(valid_df['Right_Kidney_Diff_%']) > threshold]
        print(f"\n  RIGHT KIDNEY (>{threshold}%):")
        if len(right_cases) > 0:
            print(f"    Total Cases: {len(right_cases)}")
            print(f"    Case IDs:")
            for idx, row in right_cases.iterrows():
                diff_pct = row['Right_Kidney_Diff_%']
                aira_vol = row['AIRA_Right_Kidney_Vol_cm3']
                fda_vol = row['FDA_Right_Kidney_Vol_cm3']
                print(f"      • {row['Case_ID']:<25} | Diff: {diff_pct:>7.2f}% | AIRA: {aira_vol:>7.2f} cm³ | FDA: {fda_vol:>7.2f} cm³")
        else:
            print(f"    No cases found with >{threshold}% difference")
        
        # Left Kidney
        left_cases = valid_df[abs(valid_df['Left_Kidney_Diff_%']) > threshold]
        print(f"\n  LEFT KIDNEY (>{threshold}%):")
        if len(left_cases) > 0:
            print(f"    Total Cases: {len(left_cases)}")
            print(f"    Case IDs:")
            for idx, row in left_cases.iterrows():
                diff_pct = row['Left_Kidney_Diff_%']
                aira_vol = row['AIRA_Left_Kidney_Vol_cm3']
                fda_vol = row['FDA_Left_Kidney_Vol_cm3']
                print(f"      • {row['Case_ID']:<25} | Diff: {diff_pct:>7.2f}% | AIRA: {aira_vol:>7.2f} cm³ | FDA: {fda_vol:>7.2f} cm³")
        else:
            print(f"    No cases found with >{threshold}% difference")
        
        # Total (Both Kidneys)
        total_cases = valid_df[abs(valid_df['Total_Kidney_Diff_%']) > threshold]
        print(f"\n  BOTH KIDNEYS COMBINED (>{threshold}%):")
        if len(total_cases) > 0:
            print(f"    Total Cases: {len(total_cases)}")
            print(f"    Case IDs:")
            for idx, row in total_cases.iterrows():
                diff_pct = row['Total_Kidney_Diff_%']
                aira_vol = row['AIRA_Total_Kidney_Vol_cm3']
                fda_vol = row['FDA_Total_Kidney_Vol_cm3']
                print(f"      • {row['Case_ID']:<25} | Diff: {diff_pct:>7.2f}% | AIRA: {aira_vol:>7.2f} cm³ | FDA: {fda_vol:>7.2f} cm³")
        else:
            print(f"    No cases found with >{threshold}% difference")

# Read and analyze both scenarios
print("\nReading Excel file...")

# AIRA vs GT01
df_gt01 = pd.read_excel(latest_file, sheet_name='AIRA_vs_GT01')
analyze_differences(df_gt01, "AIRA vs GT01 (Annotator 1)")

# AIRA vs GT02
df_gt02 = pd.read_excel(latest_file, sheet_name='AIRA_vs_GT02')
analyze_differences(df_gt02, "AIRA vs GT02 (Annotator 2)")

print("\n" + "=" * 100)
print("SUMMARY STATISTICS")
print("=" * 100)

def print_summary(df, scenario_name):
    """Print summary statistics"""
    valid_df = df[
        (df['AIRA_Right_Kidney_Vol_cm3'] != '') & 
        (df['FDA_Right_Kidney_Vol_cm3'] != '')
    ].copy()
    
    for col in ['Right_Kidney_Diff_%', 'Left_Kidney_Diff_%', 'Total_Kidney_Diff_%']:
        if col in valid_df.columns:
            valid_df[col] = pd.to_numeric(valid_df[col], errors='coerce')
    
    print(f"\n{scenario_name}:")
    print(f"  Total cases analyzed: {len(valid_df)}")
    
    for kidney, col in [('Right Kidney', 'Right_Kidney_Diff_%'), 
                        ('Left Kidney', 'Left_Kidney_Diff_%'),
                        ('Both Kidneys', 'Total_Kidney_Diff_%')]:
        diffs = abs(valid_df[col].dropna())
        print(f"\n  {kidney}:")
        print(f"    Mean Absolute Diff: {diffs.mean():.2f}%")
        print(f"    Cases >10%: {(diffs > 10).sum()} ({(diffs > 10).sum()/len(diffs)*100:.1f}%)")
        print(f"    Cases >15%: {(diffs > 15).sum()} ({(diffs > 15).sum()/len(diffs)*100:.1f}%)")
        print(f"    Cases >20%: {(diffs > 20).sum()} ({(diffs > 20).sum()/len(diffs)*100:.1f}%)")
        print(f"    Cases >25%: {(diffs > 25).sum()} ({(diffs > 25).sum()/len(diffs)*100:.1f}%)")

print_summary(df_gt01, "AIRA vs GT01")
print_summary(df_gt02, "AIRA vs GT02")

print("\n" + "=" * 100)
print("Analysis Complete!")
print("=" * 100)
