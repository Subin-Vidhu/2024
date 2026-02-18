"""
Compare two DICE CSV files to identify differences and changes.
IMPROVED VERSION - Focuses on actual value changes only.

This script loads two CSV files and performs detailed comparison:
- Identifies new rows
- Identifies removed rows  
- Identifies rows with changed NUMERIC values
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


def compare_dice_files_improved(file1, file2, output_dir='results/comparisons'):
    """
    Compare two DICE CSV files and generate detailed report.
    Improved version that focuses on actual numeric value changes.
    
    Args:
        file1: Path to first CSV file
        file2: Path to second CSV file
        output_dir: Directory to save reports
    """
    print("\n" + "="*80)
    print("DICE CSV FILE COMPARISON (IMPROVED)")
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
    
    # Create row key mappings
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
    
    # Identify numeric columns
    numeric_cols = df1.select_dtypes(include=['number']).columns.tolist()
    print(f"   • Numeric columns detected: {numeric_cols}")
    
    # Analyze changes in common rows - ONLY compare numeric columns
    changed_rows = []
    for key in common_keys:
        idx1 = keys1_dict[key]
        idx2 = keys2_dict[key]
        row1 = df1.iloc[idx1]
        row2 = df2.iloc[idx2]
        
        # Compare ONLY numeric columns
        changes = {}
        for col in numeric_cols:
            val1 = row1[col]
            val2 = row2[col]
            
            # Check for any difference in numeric values
            if pd.notna(val1) and pd.notna(val2):
                if abs(float(val1) - float(val2)) > 1e-10:  # Account for floating point precision
                    changes[col] = (val1, val2)
        
        if changes:
            changed_rows.append({
                'patient': row1['Patient'],
                'organ': row1['Organ'],
                'changes': changes
            })
    
    print(f"   • Rows with numeric value changes: {len(changed_rows)}")
    
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    # Generate detailed report
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_file = os.path.join(output_dir, f"DICE_Comparison_Detailed_{timestamp}.txt")
    
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
        f.write(f"Rows with value changes: {len(changed_rows)}\n\n")
        
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
            f.write("ROWS WITH CHANGED NUMERIC VALUES\n")
            f.write("-" * 80 + "\n")
            for item in sorted(changed_rows, key=lambda x: (x['patient'], x['organ'])):
                patient = item['patient']
                organ = item['organ']
                changes = item['changes']
                
                f.write(f"\n  {patient} - {organ}\n")
                for col, (val1, val2) in sorted(changes.items()):
                    diff = abs(float(val2) - float(val1))
                    pct_change = (diff / abs(float(val1)) * 100) if float(val1) != 0 else 0
                    f.write(f"    • {col}:\n")
                    f.write(f"      File 1: {val1}\n")
                    f.write(f"      File 2: {val2}\n")
                    f.write(f"      Change: {diff:+.6f} ({pct_change:+.2f}%)\n")
        else:
            f.write("NO ROWS WITH NUMERIC VALUE CHANGES\n")
            f.write("-" * 80 + "\n\n")
    
    print(f"\n💾 Detailed report saved to: {report_file}")
    
    # Generate CSV summary - improved to show only real changes
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
            'NewValue': '',
            'Change_Absolute': '',
            'Change_Percent': ''
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
            'NewValue': '',
            'Change_Absolute': '',
            'Change_Percent': ''
        })
    
    # Changed values
    for item in sorted(changed_rows, key=lambda x: (x['patient'], x['organ'])):
        for col, (val1, val2) in sorted(item['changes'].items()):
            diff = abs(float(val2) - float(val1))
            pct_change = (diff / abs(float(val1)) * 100) if float(val1) != 0 else 0
            summary_data.append({
                'Patient': item['patient'],
                'Organ': item['organ'],
                'ChangeType': 'MODIFIED',
                'Column': col,
                'OldValue': val1,
                'NewValue': val2,
                'Change_Absolute': f"{diff:+.6f}",
                'Change_Percent': f"{pct_change:+.2f}%"
            })
    
    if summary_data:
        summary_df = pd.DataFrame(summary_data)
        summary_df.to_csv(summary_file, index=False)
        print(f"📊 Summary CSV saved to: {summary_file}")
    
    # Print summary of changes to console
    print(f"\n📋 CHANGE DETAILS:")
    
    if only_in_file1:
        print(f"\n❌ REMOVED {len(only_in_file1)} rows from File 1:")
        for key in sorted(only_in_file1):
            row = df1.iloc[keys1_dict[key]]
            print(f"   • {row['Patient']} - {row['Organ']}")
    
    if only_in_file2:
        print(f"\n✅ ADDED {len(only_in_file2)} rows in File 2:")
        for key in sorted(only_in_file2):
            row = df2.iloc[keys2_dict[key]]
            print(f"   • {row['Patient']} - {row['Organ']}")
    
    if changed_rows:
        print(f"\n🔄 MODIFIED {len(changed_rows)} rows with value changes:")
        for item in changed_rows[:10]:  # Show first 10
            print(f"   • {item['patient']} - {item['organ']}")
            for col in list(item['changes'].keys())[:2]:  # Show first 2 changed columns
                val1, val2 = item['changes'][col]
                print(f"     - {col}: {val1} → {val2}")
        if len(changed_rows) > 10:
            print(f"   ... and {len(changed_rows) - 10} more")
    
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
        compare_dice_files_improved(file1, file2)
