"""
Compare two DICE CSV files to identify differences and changes.

This script loads two CSV files and performs detailed comparison:
- Identifies new rows
- Identifies removed rows
- Identifies rows with changed values
- Provides summary statistics
"""

import pandas as pd
import os
from datetime import datetime
from pathlib import Path


def load_csv_file(filepath):
    """Load CSV file with error handling."""
    try:
        df = pd.read_csv(filepath)
        return df
    except FileNotFoundError:
        print(f"❌ File not found: {filepath}")
        return None
    except Exception as e:
        print(f"❌ Error loading {filepath}: {e}")
        return None


def create_row_key(row):
    """Create unique key for each row based on Patient and Organ."""
    return f"{row['Patient']}_{row['Organ']}"


def compare_dice_files(file1, file2, output_dir='results/comparisons'):
    """
    Compare two DICE CSV files and generate detailed report.
    
    Args:
        file1: Path to first CSV file
        file2: Path to second CSV file
        output_dir: Directory to save reports
    """
    print("\n" + "="*80)
    print("DICE CSV FILE COMPARISON")
    print("="*80)
    
    # Load files
    print(f"\n📂 Loading File 1: {Path(file1).name}")
    df1 = load_csv_file(file1)
    
    print(f"📂 Loading File 2: {Path(file2).name}")
    df2 = load_csv_file(file2)
    
    if df1 is None or df2 is None:
        print("\n❌ Failed to load files. Exiting.")
        return
    
    print(f"\n✅ File 1 loaded: {len(df1)} rows")
    print(f"✅ File 2 loaded: {len(df2)} rows")
    
    # Create row key mappings (dict instead of column)
    keys1_dict = {create_row_key(row): idx for idx, (_, row) in enumerate(df1.iterrows())}
    keys2_dict = {create_row_key(row): idx for idx, (_, row) in enumerate(df2.iterrows())}
    
    # Find unique rows
    keys1 = set(keys1_dict.keys())
    keys2 = set(keys2_dict.keys())
    
    only_in_file1 = keys1 - keys2
    only_in_file2 = keys2 - keys1
    common_keys = keys1 & keys2
    
    print(f"\n📊 COMPARISON SUMMARY")
    print(f"   • Rows only in File 1: {len(only_in_file1)}")
    print(f"   • Rows only in File 2: {len(only_in_file2)}")
    print(f"   • Common rows: {len(common_keys)}")
    
    # Analyze changes in common rows
    changed_rows = []
    for key in common_keys:
        idx1 = keys1_dict[key]
        idx2 = keys2_dict[key]
        row1 = df1.iloc[idx1]
        row2 = df2.iloc[idx2]
        
        # Compare columns
        changes = {}
        for col in df1.columns:
            try:
                # Try numeric comparison
                val1 = pd.to_numeric(row1[col], errors='coerce')
                val2 = pd.to_numeric(row2[col], errors='coerce')
                
                if pd.notna(val1) and pd.notna(val2):
                    if abs(val1 - val2) > 1e-6:  # Account for floating point precision
                        changes[col] = (val1, val2)
                elif val1 != val2:  # String/non-numeric comparison
                    changes[col] = (row1[col], row2[col])
            except:
                if row1[col] != row2[col]:
                    changes[col] = (row1[col], row2[col])
        
        if changes:
            changed_rows.append({
                'patient': row1['Patient'],
                'organ': row1['Organ'],
                'changes': changes
            })
    
    print(f"   • Rows with changed values: {len(changed_rows)}")
    
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    # Generate detailed report
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_file = os.path.join(output_dir, f"DICE_Comparison_{timestamp}.txt")
    
    with open(report_file, 'w') as f:
        f.write("="*80 + "\n")
        f.write("DETAILED DICE CSV COMPARISON REPORT\n")
        f.write("="*80 + "\n\n")
        
        f.write(f"File 1: {Path(file1).name}\n")
        f.write(f"File 2: {Path(file2).name}\n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        # Summary
        f.write("SUMMARY\n")
        f.write("-" * 80 + "\n")
        f.write(f"Total rows in File 1: {len(df1)}\n")
        f.write(f"Total rows in File 2: {len(df2)}\n")
        f.write(f"Rows only in File 1:  {len(only_in_file1)}\n")
        f.write(f"Rows only in File 2:  {len(only_in_file2)}\n")
        f.write(f"Common rows:          {len(common_keys)}\n")
        f.write(f"Rows with changes:    {len(changed_rows)}\n\n")
        
        # Rows only in File 1
        if only_in_file1:
            f.write("ROWS ONLY IN FILE 1 (REMOVED)\n")
            f.write("-" * 80 + "\n")
            for key in sorted(only_in_file1):
                row = df1.iloc[keys1_dict[key]]
                f.write(f"  • {row['Patient']} - {row['Organ']}\n")
            f.write("\n")
        
        # Rows only in File 2
        if only_in_file2:
            f.write("ROWS ONLY IN FILE 2 (ADDED)\n")
            f.write("-" * 80 + "\n")
            for key in sorted(only_in_file2):
                row = df2.iloc[keys2_dict[key]]
                f.write(f"  • {row['Patient']} - {row['Organ']}\n")
            f.write("\n")
        
        # Changed rows
        if changed_rows:
            f.write("ROWS WITH CHANGED VALUES\n")
            f.write("-" * 80 + "\n")
            for item in sorted(changed_rows, key=lambda x: (x['patient'], x['organ'])):
                patient = item['patient']
                organ = item['organ']
                changes = item['changes']
                
                f.write(f"\n  {patient} - {organ}\n")
                for col, (val1, val2) in sorted(changes.items()):
                    f.write(f"    • {col}:\n")
                    f.write(f"      File 1: {val1}\n")
                    f.write(f"      File 2: {val2}\n")
        
        else:
            f.write("NO ROWS WITH VALUE CHANGES\n")
            f.write("-" * 80 + "\n\n")
    
    print(f"\n💾 Report saved to: {report_file}")
    
    # Generate CSV summary
    summary_file = os.path.join(output_dir, f"DICE_Changes_Summary_{timestamp}.csv")
    
    summary_data = []
    
    # Added rows
    for key in sorted(only_in_file2):
        row = df2.iloc[keys2_dict[key]]
        summary_data.append({
            'Patient': row['Patient'],
            'Organ': row['Organ'],
            'ChangeType': 'ADDED',
            'Column': '',
            'OldValue': '',
            'NewValue': ''
        })
    
    # Removed rows
    for key in sorted(only_in_file1):
        row = df1.iloc[keys1_dict[key]]
        summary_data.append({
            'Patient': row['Patient'],
            'Organ': row['Organ'],
            'ChangeType': 'REMOVED',
            'Column': '',
            'OldValue': '',
            'NewValue': ''
        })
    
    # Changed values
    for item in sorted(changed_rows, key=lambda x: (x['patient'], x['organ'])):
        for col, (val1, val2) in sorted(item['changes'].items()):
            summary_data.append({
                'Patient': item['patient'],
                'Organ': item['organ'],
                'ChangeType': 'MODIFIED',
                'Column': col,
                'OldValue': val1,
                'NewValue': val2
            })
    
    if summary_data:
        summary_df = pd.DataFrame(summary_data)
        summary_df.to_csv(summary_file, index=False)
        print(f"📊 Summary CSV saved to: {summary_file}")
    
    print("\n" + "="*80)
    print("✅ COMPARISON COMPLETE")
    print("="*80 + "\n")


if __name__ == "__main__":
    # Files to compare
    file1 = r"data to compare\dice_score_bw_gt1_and_gt2\66017_WCG_DICE_17Dec2025.csv"
    file2 = r"data to compare\dice_score_bw_gt1_and_gt2\66017_WCG_DICE_17FEB2026.csv"
    
    # Check if files exist
    if not os.path.exists(file1):
        print(f"❌ File not found: {file1}")
        print(f"   Current directory: {os.getcwd()}")
    elif not os.path.exists(file2):
        print(f"❌ File not found: {file2}")
        print(f"   Current directory: {os.getcwd()}")
    else:
        compare_dice_files(file1, file2)
