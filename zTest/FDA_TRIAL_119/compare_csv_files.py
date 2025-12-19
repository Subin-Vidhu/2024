"""
Compare two CSV files containing DICE scores and volumes.
Identifies rows with different values between WCG and FDA datasets.
Matches based on exact mask filenames to ensure correct comparison.
"""

import pandas as pd
import numpy as np
import re
from pathlib import Path
from datetime import datetime

def normalize_mask_name(mask_name):
    """
    Normalize mask names for comparison by removing spaces and standardizing format.
    Examples: 'A-003_GT01.nii' -> 'A-003_GT01.nii'
            'A-003-GT01.nii' -> 'A-003_GT01.nii'
            'N-001-GT01.nii' -> 'N-001_GT01.nii'
            'A-075_GT01 .nii' -> 'A-075_GT01.nii'
            'A-085 GT02.nii' -> 'A-085_GT02.nii'
    """
    mask_name = str(mask_name).strip()
    # Remove extra spaces within the name
    mask_name = ' '.join(mask_name.split())
    # Replace any separator (hyphen, underscore, or space) before GT with underscore for consistency
    # This handles A-003-GT01, A-003_GT01, and A-003 GT01 formats
    mask_name = re.sub(r'[-_ ]GT', '_GT', mask_name)
    return mask_name

def extract_patient_from_mask(mask_name):
    """
    Extract patient ID from mask filename.
    Examples: 'A-003_GT01.nii' -> 'A-003'
              'N-001_GT01.nii' -> 'N-001'
              'A-075_GT01 .nii' -> 'A-075'
    """
    mask_name = normalize_mask_name(mask_name)
    # Extract patient ID (everything before _GT)
    match = re.match(r'([A-Z]-\d+)', mask_name)
    if match:
        return match.group(1)
    return mask_name.split('_')[0] if '_' in mask_name else mask_name

def load_and_prepare_wcg_data(wcg_file):
    """Load WCG CSV file and prepare for comparison."""
    df = pd.read_csv(wcg_file)
    print(f"\nWCG file columns: {df.columns.tolist()}")
    print(f"WCG file shape: {df.shape}")
    
    # Normalize mask names
    df['Mask1_Normalized'] = df['Mask1'].apply(normalize_mask_name)
    df['Mask2_Normalized'] = df['Mask2'].apply(normalize_mask_name)
    
    # Extract patient ID from mask names
    df['Patient_From_Mask'] = df['Mask1'].apply(extract_patient_from_mask)
    
    # Create a composite key for matching based on sorted mask names and organ
    # Sorting handles cases where GT01/GT02 order is swapped between files
    df['Match_Key'] = df.apply(lambda row: '|'.join(sorted([row['Mask1_Normalized'], row['Mask2_Normalized']])) + '|' + row['Organ'].strip(), axis=1)
    
    # Store which mask is GT01 and which is GT02 for proper value comparison
    df['Is_Mask1_GT01'] = df['Mask1_Normalized'].str.contains('GT01', na=False)
    
    return df

def load_and_prepare_fda_data(fda_file):
    """Load FDA CSV file and prepare for comparison."""
    df = pd.read_csv(fda_file)
    print(f"\nFDA file columns: {df.columns.tolist()}")
    print(f"FDA file shape: {df.shape}")
    
    # Filter out average rows (rows where Organ contains "Average")
    df = df[~df['Organ'].str.contains('Average', na=False)].copy()
    print(f"FDA file shape after removing average rows: {df.shape}")
    
    # Map column names to match WCG format
    column_mapping = {
        'GT01_File': 'Mask1',
        'GT02_File': 'Mask2',
        'GT01_Volume_cm3': 'Mask1_Volume_mL',  # cm3 = mL
        'GT02_Volume_cm3': 'Mask2_Volume_mL'
    }
    
    for old_col, new_col in column_mapping.items():
        if old_col in df.columns:
            df[new_col] = df[old_col]
    
    # Normalize mask names
    df['Mask1_Normalized'] = df['Mask1'].apply(normalize_mask_name)
    df['Mask2_Normalized'] = df['Mask2'].apply(normalize_mask_name)
    
    # Extract patient ID from mask names
    df['Patient_From_Mask'] = df['Mask1'].apply(extract_patient_from_mask)
    
    # Create a composite key for matching based on sorted mask names and organ
    # Sorting handles cases where GT01/GT02 order is swapped between files
    df['Match_Key'] = df.apply(lambda row: '|'.join(sorted([row['Mask1_Normalized'], row['Mask2_Normalized']])) + '|' + row['Organ'].strip(), axis=1)
    
    # Store which mask is GT01 and which is GT02 for proper value comparison
    df['Is_Mask1_GT01'] = df['Mask1_Normalized'].str.contains('GT01', na=False)
    
    return df

def compare_values(wcg_df, fda_df, tolerance=0.001):
    """
    Compare values between WCG and FDA datasets.
    
    Parameters:
    - tolerance: Relative tolerance for floating point comparisons (default 0.1%)
    """
    comparison_columns = ['DiceCoefficient', 'Mask1_Volume_mL', 'Mask2_Volume_mL']
    
    differences = []
    matched_count = 0
    unmatched_wcg = []
    unmatched_fda = []
    
    # Create sets for tracking matches
    wcg_keys = set(wcg_df['Match_Key'])
    fda_keys = set(fda_df['Match_Key'])
    
    print(f"\nWCG unique keys: {len(wcg_keys)}")
    print(f"FDA unique keys: {len(fda_keys)}")
    print(f"\nKeys in WCG but not in FDA: {len(wcg_keys - fda_keys)}")
    print(f"Keys in FDA but not in WCG: {len(fda_keys - wcg_keys)}")
    
    # Compare matching rows
    for idx, wcg_row in wcg_df.iterrows():
        match_key = wcg_row['Match_Key']
        
        # Find matching FDA row
        fda_match = fda_df[fda_df['Match_Key'] == match_key]
        
        if fda_match.empty:
            unmatched_wcg.append({
                'Match_Key': match_key,
                'Patient': wcg_row['Patient'],
                'Mask1': wcg_row['Mask1'],
                'Mask2': wcg_row['Mask2'],
                'Organ': wcg_row['Organ'],
                'Reason': 'No matching row in FDA file'
            })
            continue
        
        fda_row = fda_match.iloc[0]
        matched_count += 1
        
        # Check if mask order is swapped between WCG and FDA
        # If WCG has GT02,GT01 and FDA has GT01,GT02, we need to swap volume comparison
        wcg_mask1_is_gt01 = wcg_row['Is_Mask1_GT01']
        fda_mask1_is_gt01 = fda_row['Is_Mask1_GT01']
        masks_swapped = (wcg_mask1_is_gt01 != fda_mask1_is_gt01)
        
        # Compare each column
        row_differences = []
        for col in comparison_columns:
            if col not in wcg_row or col not in fda_row:
                continue
                
            wcg_val = wcg_row[col]
            # If masks are swapped, swap the volume columns for comparison
            if masks_swapped and 'Volume' in col:
                if col == 'Mask1_Volume_mL':
                    fda_val = fda_row['Mask2_Volume_mL']
                elif col == 'Mask2_Volume_mL':
                    fda_val = fda_row['Mask1_Volume_mL']
                else:
                    fda_val = fda_row[col]
            else:
                fda_val = fda_row[col]
            
            # Handle NaN values
            if pd.isna(wcg_val) and pd.isna(fda_val):
                continue
            if pd.isna(wcg_val) or pd.isna(fda_val):
                row_differences.append({
                    'Column': col,
                    'WCG_Value': wcg_val,
                    'FDA_Value': fda_val,
                    'Difference': 'One value is NaN'
                })
                continue
            
            # Calculate relative difference for numeric values
            try:
                wcg_val_float = float(wcg_val)
                fda_val_float = float(fda_val)
                
                # Calculate relative difference
                if wcg_val_float != 0:
                    rel_diff = abs((fda_val_float - wcg_val_float) / wcg_val_float)
                else:
                    rel_diff = abs(fda_val_float - wcg_val_float)
                
                if rel_diff > tolerance:
                    abs_diff = abs(fda_val_float - wcg_val_float)
                    row_differences.append({
                        'Column': col,
                        'WCG_Value': wcg_val_float,
                        'FDA_Value': fda_val_float,
                        'Absolute_Diff': abs_diff,
                        'Relative_Diff_%': rel_diff * 100
                    })
            except (ValueError, TypeError):
                # For non-numeric values, do direct comparison
                if str(wcg_val).strip() != str(fda_val).strip():
                    row_differences.append({
                        'Column': col,
                        'WCG_Value': wcg_val,
                        'FDA_Value': fda_val,
                        'Difference': 'Values differ'
                    })
        
        if row_differences:
            differences.append({
                'Match_Key': match_key,
                'Patient': wcg_row['Patient'],
                'Organ': wcg_row['Organ'],
                'WCG_Mask1': wcg_row['Mask1'],
                'WCG_Mask2': wcg_row['Mask2'],
                'FDA_Mask1': fda_row['Mask1'],
                'FDA_Mask2': fda_row['Mask2'],
                'Masks_Swapped': masks_swapped,
                'Differences': row_differences
            })
        elif masks_swapped:
            # Mask order swapped but values match - this is OK, just note it for info
            differences.append({
                'Match_Key': match_key,
                'Patient': wcg_row['Patient'],
                'Organ': wcg_row['Organ'],
                'WCG_Mask1': wcg_row['Mask1'],
                'WCG_Mask2': wcg_row['Mask2'],
                'FDA_Mask1': fda_row['Mask1'],
                'FDA_Mask2': fda_row['Mask2'],
                'Masks_Swapped': masks_swapped,
                'Differences': [{'Note': 'GT01/GT02 order swapped but values correctly matched'}]
            })
    
    # Find unmatched FDA rows
    for idx, fda_row in fda_df.iterrows():
        match_key = fda_row['Match_Key']
        if match_key not in wcg_keys:
            unmatched_fda.append({
                'Match_Key': match_key,
                'Patient': fda_row['Patient'],
                'Mask1': fda_row['Mask1'],
                'Mask2': fda_row['Mask2'],
                'Organ': fda_row['Organ'],
                'Reason': 'No matching row in WCG file'
            })
    
    # Check for potential swapped values in unmatched rows
    # Look for same patient with different filenames
    potential_swaps = []
    for wcg_unmatch in unmatched_wcg:
        wcg_patient = wcg_unmatch['Patient']
        wcg_organ = wcg_unmatch['Organ']
        
        # Find if this patient exists in FDA unmatched with opposite organ
        opposite_organ = 'Left Kidney' if wcg_organ == 'Right Kidney' else 'Right Kidney'
        for fda_unmatch in unmatched_fda:
            if fda_unmatch['Patient'] == wcg_patient or fda_unmatch['Patient'] == wcg_patient.replace('A-', '').replace('N-', '').lstrip('0'):
                # Same patient found - check if values suggest organ swap
                wcg_match_row = wcg_df[(wcg_df['Patient'] == wcg_patient) & (wcg_df['Organ'] == wcg_organ)].iloc[0]
                fda_match_rows = fda_df[
                    (fda_df['Patient'].str.contains(wcg_patient.replace('A-', '').replace('N-', '').lstrip('0'), na=False)) &
                    (fda_df['Organ'] == wcg_organ)
                ]
                if not fda_match_rows.empty:
                    fda_match_row = fda_match_rows.iloc[0]
                    
                    # Check if dice coefficients match
                    if abs(float(wcg_match_row['DiceCoefficient']) - float(fda_match_row['DiceCoefficient'])) < 0.0001:
                        potential_swaps.append({
                            'WCG_Patient': wcg_patient,
                            'FDA_Patient': fda_match_row['Patient'],
                            'Organ': wcg_organ,
                            'WCG_Masks': f"{wcg_match_row['Mask1']} vs {wcg_match_row['Mask2']}",
                            'FDA_Masks': f"{fda_match_row['Mask1']} vs {fda_match_row['Mask2']}",
                            'DiceCoefficient': wcg_match_row['DiceCoefficient'],
                            'WCG_Vol1': wcg_match_row['Mask1_Volume_mL'],
                            'WCG_Vol2': wcg_match_row['Mask2_Volume_mL'],
                            'FDA_Vol1': fda_match_row['Mask1_Volume_mL'],
                            'FDA_Vol2': fda_match_row['Mask2_Volume_mL'],
                            'Values_Match': (abs(float(wcg_match_row['Mask1_Volume_mL']) - float(fda_match_row['Mask1_Volume_mL'])) < 0.01 and
                                           abs(float(wcg_match_row['Mask2_Volume_mL']) - float(fda_match_row['Mask2_Volume_mL'])) < 0.01)
                        })
    
    return {
        'differences': differences,
        'matched_count': matched_count,
        'unmatched_wcg': unmatched_wcg,
        'unmatched_fda': unmatched_fda,
        'potential_swaps': potential_swaps
    }

def save_comparison_results(results, output_dir, wcg_df, fda_df):
    """Save comparison results to CSV files and text report."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Create output directory if it doesn't exist
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Save differences to CSV
    if results['differences']:
        diff_records = []
        for diff in results['differences']:
            for d in diff['Differences']:
                record = {
                    'Patient': diff['Patient'],
                    'Organ': diff['Organ'],
                    'WCG_Mask1': diff['WCG_Mask1'],
                    'WCG_Mask2': diff['WCG_Mask2'],
                    'FDA_Mask1': diff['FDA_Mask1'],
                    'FDA_Mask2': diff['FDA_Mask2'],
                    'Masks_Swapped': diff.get('Masks_Swapped', False)
                }
                if 'Note' in d:
                    record['Note'] = d['Note']
                    record['Column'] = 'N/A'
                    record['WCG_Value'] = 'N/A'
                    record['FDA_Value'] = 'N/A'
                elif 'Column' in d:
                    record['Column'] = d['Column']
                    record['WCG_Value'] = d['WCG_Value']
                    record['FDA_Value'] = d['FDA_Value']
                    if 'Absolute_Diff' in d:
                        record['Absolute_Diff'] = d['Absolute_Diff']
                        record['Relative_Diff_%'] = d['Relative_Diff_%']
                    else:
                        record['Note'] = d.get('Difference', '')
                diff_records.append(record)
        
        diff_df = pd.DataFrame(diff_records)
        diff_file = output_path / f"Value_Differences_{timestamp}.csv"
        diff_df.to_csv(diff_file, index=False)
        print(f"\nDifferences saved to: {diff_file}")
    
    # Save unmatched rows
    if results['unmatched_wcg']:
        unmatched_wcg_df = pd.DataFrame(results['unmatched_wcg'])
        unmatched_wcg_file = output_path / f"Unmatched_WCG_Rows_{timestamp}.csv"
        unmatched_wcg_df.to_csv(unmatched_wcg_file, index=False)
        print(f"Unmatched WCG rows saved to: {unmatched_wcg_file}")
    
    if results['unmatched_fda']:
        unmatched_fda_df = pd.DataFrame(results['unmatched_fda'])
        unmatched_fda_file = output_path / f"Unmatched_FDA_Rows_{timestamp}.csv"
        unmatched_fda_df.to_csv(unmatched_fda_file, index=False)
        print(f"Unmatched FDA rows saved to: {unmatched_fda_file}")
    
    # Create summary report
    report_file = output_path / f"Comparison_Report_{timestamp}.txt"
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write("=" * 80 + "\n")
        f.write("CSV COMPARISON REPORT\n")
        f.write("=" * 80 + "\n\n")
        f.write(f"Report Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        f.write(f"Total matched rows: {results['matched_count']}\n")
        f.write(f"Rows with differences: {len(results['differences'])}\n")
        f.write(f"Unmatched WCG rows: {len(results['unmatched_wcg'])}\n")
        f.write(f"Unmatched FDA rows: {len(results['unmatched_fda'])}\n\n")
        
        if results['differences']:
            f.write("\n" + "=" * 80 + "\n")
            f.write("ROWS WITH MASK ORDER DIFFERENCES (GT01/GT02 SWAPPED)\n")
            f.write("=" * 80 + "\n")
            f.write("Note: These are NOT data issues - just different mask ordering.\n")
            f.write("      Values were correctly matched after reordering.\n")
            f.write("=" * 80 + "\n\n")
            
            for i, diff in enumerate(results['differences'], 1):
                f.write(f"\n{i}. Patient: {diff['Patient']}, Organ: {diff['Organ']}\n")
                f.write(f"   WCG Masks: {diff['WCG_Mask1']} vs {diff['WCG_Mask2']}\n")
                f.write(f"   FDA Masks: {diff['FDA_Mask1']} vs {diff['FDA_Mask2']}\n")
                
                if diff.get('Masks_Swapped', False):
                    f.write("   ** NOTE: GT01/GT02 mask order is SWAPPED between WCG and FDA files **\n")
                    f.write("            Volume comparison was adjusted accordingly.\n")
                
                f.write("   Differences:\n")
                for d in diff['Differences']:
                    if 'Note' in d:
                        f.write(f"      - {d['Note']}\n")
                    elif 'Column' in d:
                        f.write(f"      - {d['Column']}:\n")
                        f.write(f"          WCG: {d['WCG_Value']}\n")
                        f.write(f"          FDA: {d['FDA_Value']}\n")
                        if 'Relative_Diff_%' in d:
                            f.write(f"          Difference: {d['Absolute_Diff']:.6f} ({d['Relative_Diff_%']:.4f}%)\n")
        
        # Add unmatched rows details
        if results['unmatched_wcg']:
            f.write("\n" + "=" * 80 + "\n")
            f.write("UNMATCHED WCG ROWS (in WCG but not in FDA)\n")
            f.write("=" * 80 + "\n\n")
            for i, row in enumerate(results['unmatched_wcg'], 1):
                f.write(f"{i}. Patient: {row['Patient']}, Organ: {row['Organ']}\n")
                f.write(f"   Masks: {row['Mask1']} vs {row['Mask2']}\n\n")
        
        if results['unmatched_fda']:
            f.write("\n" + "=" * 80 + "\n")
            f.write("UNMATCHED FDA ROWS (in FDA but not in WCG)\n")
            f.write("=" * 80 + "\n\n")
            for i, row in enumerate(results['unmatched_fda'], 1):
                f.write(f"{i}. Patient: {row['Patient']}, Organ: {row['Organ']}\n")
                f.write(f"   Masks: {row['Mask1']} vs {row['Mask2']}\n\n")
        
        # Detect organ swaps (where same patient has opposite kidney labels)
        organ_swaps = []
        print(f"\nDEBUG: Checking {len(results['unmatched_wcg'])} unmatched WCG rows for organ swaps...")
        for wcg_unmatch in results['unmatched_wcg']:
            wcg_patient = wcg_unmatch['Patient']
            wcg_patient_num = wcg_patient.replace('A-', '').replace('N-', '').lstrip('0')
            print(f"DEBUG: WCG patient {wcg_patient} -> extracted number: '{wcg_patient_num}'")
            
            # Get WCG rows for this patient (both kidneys)
            wcg_patient_rows = wcg_df[wcg_df['Patient'] == wcg_patient]
            print(f"DEBUG: Found {len(wcg_patient_rows)} WCG rows for {wcg_patient}")
            if len(wcg_patient_rows) != 2:
                continue
                
            # Look for same patient in FDA unmatched with potentially swapped organs
            fda_patient_rows = fda_df[fda_df['Patient'].str.contains(wcg_patient_num, na=False)]
            print(f"DEBUG: Found {len(fda_patient_rows)} FDA rows matching '{wcg_patient_num}'")
            if len(fda_patient_rows) < 2:
                continue
            
            # Check if values match when organs are swapped
            wcg_right = wcg_patient_rows[wcg_patient_rows['Organ'] == 'Right Kidney'].iloc[0] if len(wcg_patient_rows[wcg_patient_rows['Organ'] == 'Right Kidney']) > 0 else None
            wcg_left = wcg_patient_rows[wcg_patient_rows['Organ'] == 'Left Kidney'].iloc[0] if len(wcg_patient_rows[wcg_patient_rows['Organ'] == 'Left Kidney']) > 0 else None
            fda_right = fda_patient_rows[fda_patient_rows['Organ'] == 'Right Kidney'].iloc[0] if len(fda_patient_rows[fda_patient_rows['Organ'] == 'Right Kidney']) > 0 else None
            fda_left = fda_patient_rows[fda_patient_rows['Organ'] == 'Left Kidney'].iloc[0] if len(fda_patient_rows[fda_patient_rows['Organ'] == 'Left Kidney']) > 0 else None
            
            if wcg_right is not None and wcg_left is not None and fda_right is not None and fda_left is not None:
                # Check if WCG Right matches FDA Left AND WCG Left matches FDA Right (organ swap)
                dice_right_to_left = abs(float(wcg_right['DiceCoefficient']) - float(fda_left['DiceCoefficient']))
                dice_left_to_right = abs(float(wcg_left['DiceCoefficient']) - float(fda_right['DiceCoefficient']))
                
                vol_right_to_left_1 = abs(float(wcg_right['Mask1_Volume_mL']) - float(fda_left['Mask1_Volume_mL']))
                vol_right_to_left_2 = abs(float(wcg_right['Mask2_Volume_mL']) - float(fda_left['Mask2_Volume_mL']))
                vol_left_to_right_1 = abs(float(wcg_left['Mask1_Volume_mL']) - float(fda_right['Mask1_Volume_mL']))
                vol_left_to_right_2 = abs(float(wcg_left['Mask2_Volume_mL']) - float(fda_right['Mask2_Volume_mL']))
                
                print(f"DEBUG: Checking value matches:")
                print(f"  dice_right_to_left={dice_right_to_left}, dice_left_to_right={dice_left_to_right}")
                print(f"  vol_right_to_left: {vol_right_to_left_1}, {vol_right_to_left_2}")
                print(f"  vol_left_to_right: {vol_left_to_right_1}, {vol_left_to_right_2}")
                
                # If values match when swapped (tolerance 0.01)
                if (dice_right_to_left < 0.0001 and dice_left_to_right < 0.0001 and
                    vol_right_to_left_1 < 0.01 and vol_right_to_left_2 < 0.01 and
                    vol_left_to_right_1 < 0.01 and vol_left_to_right_2 < 0.01):
                    print(f"DEBUG: ORGAN SWAP DETECTED for {wcg_patient}!")
                    
                    organ_swaps.append({
                        'WCG_Patient': wcg_patient,
                        'FDA_Patient': fda_right['Patient'],
                        'WCG_Right_Dice': float(wcg_right['DiceCoefficient']),
                        'WCG_Left_Dice': float(wcg_left['DiceCoefficient']),
                        'FDA_Right_Dice': float(fda_right['DiceCoefficient']),
                        'FDA_Left_Dice': float(fda_left['DiceCoefficient']),
                        'WCG_Right_Vols': f"{wcg_right['Mask1_Volume_mL']}, {wcg_right['Mask2_Volume_mL']}",
                        'WCG_Left_Vols': f"{wcg_left['Mask1_Volume_mL']}, {wcg_left['Mask2_Volume_mL']}",
                        'FDA_Right_Vols': f"{fda_right['Mask1_Volume_mL']}, {fda_right['Mask2_Volume_mL']}",
                        'FDA_Left_Vols': f"{fda_left['Mask1_Volume_mL']}, {fda_left['Mask2_Volume_mL']}",
                        'WCG_Masks': f"{wcg_right['Mask1']} vs {wcg_right['Mask2']}",
                        'FDA_Masks': f"{fda_right['Mask1']} vs {fda_right['Mask2']}"
                    })
                    break  # Only report once per patient
        
        if organ_swaps:
            f.write("\n" + "=" * 80 + "\n")
            f.write("!!! CRITICAL: LEFT/RIGHT KIDNEY ORGAN SWAP DETECTED !!!\n")
            f.write("=" * 80 + "\n\n")
            for i, swap in enumerate(organ_swaps, 1):
                f.write(f"{i}. Patient: {swap['WCG_Patient']} (WCG) / {swap['FDA_Patient']} (FDA)\n")
                f.write(f"   ** LEFT and RIGHT kidney labels are SWAPPED between files **\n\n")
                f.write(f"   WCG Right Kidney values MATCH FDA Left Kidney:\n")
                f.write(f"      - Dice: {swap['WCG_Right_Dice']} (WCG) vs {swap['FDA_Left_Dice']} (FDA)\n")
                f.write(f"      - Volumes: {swap['WCG_Right_Vols']} (WCG) vs {swap['FDA_Left_Vols']} (FDA)\n\n")
                f.write(f"   WCG Left Kidney values MATCH FDA Right Kidney:\n")
                f.write(f"      - Dice: {swap['WCG_Left_Dice']} (WCG) vs {swap['FDA_Right_Dice']} (FDA)\n")
                f.write(f"      - Volumes: {swap['WCG_Left_Vols']} (WCG) vs {swap['FDA_Right_Vols']} (FDA)\n\n")
                f.write(f"   File names:\n")
                f.write(f"      - WCG: {swap['WCG_Masks']}\n")
                f.write(f"      - FDA: {swap['FDA_Masks']}\n\n")
                f.write(f"   CONCLUSION: The numerical values are IDENTICAL but the organ\n")
                f.write(f"               labels (Left/Right) need to be corrected in one of the files.\n\n")
        
        # Add potential organ swaps or different filename matches
        if results.get('potential_swaps'):
            f.write("\n" + "=" * 80 + "\n")
            f.write("POTENTIAL MATCHES WITH DIFFERENT FILENAMES\n")
            f.write("(Same patient/organ but different GT01 filename)\n")
            f.write("=" * 80 + "\n\n")
            for i, swap in enumerate(results['potential_swaps'], 1):
                f.write(f"{i}. Patient: {swap['WCG_Patient']} (WCG) / {swap['FDA_Patient']} (FDA)\n")
                f.write(f"   Organ: {swap['Organ']}\n")
                f.write(f"   WCG Masks: {swap['WCG_Masks']}\n")
                f.write(f"   FDA Masks: {swap['FDA_Masks']}\n")
                f.write(f"   DiceCoefficient: {swap['DiceCoefficient']}\n")
                f.write(f"   WCG Volumes: {swap['WCG_Vol1']}, {swap['WCG_Vol2']}\n")
                f.write(f"   FDA Volumes: {swap['FDA_Vol1']}, {swap['FDA_Vol2']}\n")
                if swap['Values_Match']:
                    f.write(f"   ✓ VALUES MATCH - Different filename but same data\n\n")
                else:
                    f.write(f"   ** POTENTIAL ORGAN SWAP - Check if Left/Right kidneys are swapped **\n\n")
    
    print(f"Summary report saved to: {report_file}")
    
    return report_file

def main():
    """Main function to run the comparison."""
    # Define file paths
    base_dir = Path(__file__).parent
    data_dir = base_dir / "data to compare" / "dice_score_bw_gt1_and_gt2"
    
    wcg_file = data_dir / "66017_WCG_DICE_17Dec2025.csv"
    fda_file = data_dir / "FDA_GT01_vs_GT02_Comparison_20251216_100032.csv"
    output_dir = base_dir / "results" / "csv_comparison"
    
    print("=" * 80)
    print("CSV FILE COMPARISON")
    print("=" * 80)
    print(f"\nWCG File: {wcg_file}")
    print(f"FDA File: {fda_file}")
    print("\nMatching Strategy: Exact mask filename matching")
    
    # Check if files exist
    if not wcg_file.exists():
        print(f"\nError: WCG file not found: {wcg_file}")
        return
    if not fda_file.exists():
        print(f"\nError: FDA file not found: {fda_file}")
        return
    
    # Load and prepare data
    print("\n" + "-" * 80)
    print("Loading and preparing data...")
    print("-" * 80)
    
    wcg_df = load_and_prepare_wcg_data(wcg_file)
    fda_df = load_and_prepare_fda_data(fda_file)
    
    # Compare values
    print("\n" + "-" * 80)
    print("Comparing values...")
    print("-" * 80)
    
    results = compare_values(wcg_df, fda_df, tolerance=0.001)  # 0.1% tolerance
    
    # Display summary
    print("\n" + "=" * 80)
    print("COMPARISON SUMMARY")
    print("=" * 80)
    print(f"\nTotal matched rows: {results['matched_count']}")
    print(f"Rows with differences: {len(results['differences'])}")
    print(f"Unmatched WCG rows: {len(results['unmatched_wcg'])}")
    print(f"Unmatched FDA rows: {len(results['unmatched_fda'])}")
    if results.get('potential_swaps'):
        print(f"Potential matches with different filenames: {len(results['potential_swaps'])}")
    
    # Display sample differences
    if results['differences']:
        print("\n" + "-" * 80)
        print("SAMPLE DIFFERENCES (first 5):")
        print("-" * 80)
        for i, diff in enumerate(results['differences'][:5], 1):
            print(f"\n{i}. Patient: {diff['Patient']}, Organ: {diff['Organ']}")
            print(f"   WCG: {diff['WCG_Mask1']} vs {diff['WCG_Mask2']}")
            print(f"   FDA: {diff['FDA_Mask1']} vs {diff['FDA_Mask2']}")
            if diff.get('Masks_Swapped', False):
                print(f"   ⚠️ Masks swapped - values adjusted for comparison")
            for d in diff['Differences']:
                if 'Note' in d:
                    print(f"   {d['Note']}")
                elif 'Column' in d:
                    print(f"   {d['Column']}: WCG={d['WCG_Value']}, FDA={d['FDA_Value']}", end='')
                    if 'Relative_Diff_%' in d:
                        print(f" (diff: {d['Relative_Diff_%']:.4f}%)")
                    else:
                        print()
    else:
        print("\n✓ All matched rows have identical values!")
    
    # Save results
    print("\n" + "-" * 80)
    print("Saving results...")
    print("-" * 80)
    
    report_file = save_comparison_results(results, output_dir, wcg_df, fda_df)
    
    print("\n" + "=" * 80)
    print("COMPARISON COMPLETE")
    print("=" * 80)
    
    if results['differences']:
        print(f"\n⚠ Found {len(results['differences'])} rows with differences.")
        print(f"Please review the detailed report at: {report_file}")
    else:
        print("\n✓ All values match successfully!")
    
    # Show unmatched summary
    if results['unmatched_wcg'] or results['unmatched_fda']:
        print(f"\n⚠ Found unmatched rows:")
        if results['unmatched_wcg']:
            print(f"   - {len(results['unmatched_wcg'])} rows in WCG file not found in FDA")
        if results['unmatched_fda']:
            print(f"   - {len(results['unmatched_fda'])} rows in FDA file not found in WCG")

if __name__ == "__main__":
    main()
