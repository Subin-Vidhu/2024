#!/usr/bin/env python3
"""
AIRA vs Ground Truth Comparison
================================

This script compares AIRA model predictions against GT01 and GT02 annotators
for all 119 FDA trial cases.

Uses shared utilities from fda_utils.py for consistent case ID extraction.

Directory Structure:
--------------------
AIRA Masks:
    K:\AIRA_FDA_Models\DATA\batch_storage\ARAMIS_RAS_LPI\ARAMIS_AIRA_Mask\
        AIRA_N-001.nii
        AIRA_A-005.nii
        AIRA_A-088_N-191.nii  (dual-labeled cases)
        ...

Ground Truth:
    J:\FDA_GROUND_TRUTH_TRIAL_119\Aramis Truther Masks\Aramis Truther Masks\
        001\
            N-001-GT01.nii
            N-001-GT02.nii
        A-005\
            A-005-GT01.nii
            A-005-GT02.nii
        ...

SPECIAL CASE HANDLING:
----------------------
Dual-labeled AIRA files (A-088_N-191, A-089_N-195, A-090_N-207, A-092_N-210):
  1. Try to find GT files using A-prefix first (A-088)
  2. If not found, try N-prefix (N-191)
  3. If neither found, use fallback N-088, N-089, N-090, N-092

LABEL CONVENTION (RADIOLOGIST'S PERSPECTIVE):
----------------------------------------------
  - Label 1 = RIGHT kidney (patient's right side)
  - Label 2 = LEFT kidney (patient's left side)

FORMULAS (FDA CONVENTION):
---------------------------
  - Dice Coefficient: 2 × |A ∩ B| / (|A| + |B|)
  - DiffPercent: |Vol1 - Vol2| / max(Vol1, Vol2) × 100
  - Average: (Dice_Right + Dice_Left) / 2

OUTPUT:
-------
Single Excel file with 2 sheets:
  - Sheet 1: AIRA vs GT01 comparisons
  - Sheet 2: AIRA vs GT02 comparisons
Each sheet has 3 rows per case (Right Kidney, Left Kidney, Average)

Usage:
    python compare_aira_vs_ground_truth.py

Author: Medical AI Validation Team
Date: 2025-12-16
"""

import os
import sys
import re
import numpy as np
import nibabel as nib
import pandas as pd
from datetime import datetime
from fda_utils import extract_case_from_filename

# ============================================================================
# CONFIGURATION - EDIT THESE PATHS
# ============================================================================

# AIRA masks directory
AIRA_MASKS_DIR = r'K:\AIRA_FDA_Models\DATA\batch_storage\ARAMIS_RAS_LPI\ARAMIS_AIRA_Mask'

# Ground Truth root directory
GT_ROOT_DIR = r'J:\FDA_GROUND_TRUTH_TRIAL_119\Aramis Truther Masks\Aramis Truther Masks'

# Output directory for results
OUTPUT_DIR = r'D:\2024\zTest\FDA_TRIAL_119\results\aira_vs_ground_truth'

# ============================================================================
# DEBUG MODE CONFIGURATION
# ============================================================================
# Set to None to process all cases
# Set to a number (5, 10, 20, etc.) to process only that many cases for debugging
MAX_CASES_TO_PROCESS = None  # Change to 5, 10, or any number for testing

# Set to True to print detailed file search information
DEBUG_FILE_SEARCH = False

# Special case mappings for dual-labeled files
DUAL_LABEL_FALLBACKS = {
    'A-088': 'N-088',
    'A-089': 'N-089',
    'A-090': 'N-090',
    'A-092': 'N-092'
}

# ============================================================================
# CORE FUNCTIONS (from batch_compare_fda_ground_truth.py)
# ============================================================================

def load_nifti(file_path):
    """Load a NIfTI file and return the image object."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    return nib.load(file_path)

def get_orientation_string(img):
    """Get the orientation string for a NIfTI image."""
    ornt = nib.orientations.io_orientation(img.affine)
    return ''.join(nib.orientations.ornt2axcodes(ornt))

def reorient_to_match(reference_img, target_img):
    """Reorient target_img to match the orientation of reference_img."""
    target_ornt = nib.orientations.io_orientation(target_img.affine)
    ref_ornt = nib.orientations.io_orientation(reference_img.affine)
    ornt_transform = nib.orientations.ornt_transform(target_ornt, ref_ornt)
    reoriented_img = target_img.as_reoriented(ornt_transform)
    return reoriented_img

def get_voxel_volume(img):
    """Calculate the volume of a single voxel in mm³."""
    voxel_dims = np.abs(img.header.get_zooms()[:3])
    voxel_volume = np.prod(voxel_dims)
    return voxel_volume, voxel_dims

def dice_coefficient(y_true, y_pred, epsilon=1e-6):
    """
    FDA-compliant Dice coefficient calculation.
    
    Formula: Dice = 2 * |A ∩ B| / (|A| + |B|)
    """
    if y_true.shape != y_pred.shape:
        raise ValueError("Masks must have identical shapes")
    
    # Convert to binary masks with explicit casting
    y_true_bin = y_true.astype(np.bool_)
    y_pred_bin = y_pred.astype(np.bool_)
    
    # Calculate using logical operations
    intersection = np.sum(y_true_bin & y_pred_bin)
    sum_true = np.sum(y_true_bin)
    sum_pred = np.sum(y_pred_bin)
    
    # Handle edge cases
    if sum_true == 0 and sum_pred == 0:
        return 1.0  # Perfect agreement on empty regions
    elif sum_true == 0 or sum_pred == 0:
        return 0.0  # No overlap possible
    
    # Standard Sørensen-Dice formula
    dice = (2.0 * intersection + epsilon) / (sum_true + sum_pred + epsilon)
    
    return np.clip(dice, 0.0, 1.0)

def calc_diff_percent(vol1, vol2):
    """Calculate percentage difference using FDA convention.
    
    FDA Formula: |Vol1 - Vol2| / max(Vol1, Vol2) × 100
    """
    if vol1 == 0 and vol2 == 0:
        return "0.00%"
    if vol1 == 0 or vol2 == 0:
        return "N/A"
    # FDA convention: use maximum volume as denominator
    max_vol = max(vol1, vol2)
    diff = abs(vol1 - vol2) / max_vol * 100
    return f"{diff:.2f}%"

def larger_mask(vol1, vol2):
    """Determine which mask is larger (FDA convention)."""
    if abs(vol1 - vol2) < 1e-6:
        return "Equal"
    return "Mask1" if vol1 > vol2 else "Mask2"

def calculate_volume(mask, voxel_vol):
    """Calculate volume in both mm³ and cm³."""
    voxel_count = np.sum(mask > 0)
    vol_mm3 = voxel_count * voxel_vol
    vol_cm3 = vol_mm3 / 1000.0
    return vol_mm3, vol_cm3

# ============================================================================
# AIRA-SPECIFIC FUNCTIONS
# ============================================================================

def find_aira_files(aira_dir):
    """Find all AIRA mask files and extract case IDs."""
    if not os.path.exists(aira_dir):
        print(f"❌ ERROR: AIRA directory not found: {aira_dir}")
        return []
    
    aira_files = []
    for filename in os.listdir(aira_dir):
        if filename.startswith('AIRA_') and filename.endswith('.nii'):
            filepath = os.path.join(aira_dir, filename)
            aira_files.append((filename, filepath))
    
    return sorted(aira_files)

def extract_case_ids_from_aira(filename):
    """
    Extract case ID(s) from AIRA filename.
    
    Examples:
        'AIRA_N-001.nii' -> ['N-001']
        'AIRA_A-005.nii' -> ['A-005']
        'AIRA_A-088_N-191.nii' -> ['A-088', 'N-191']
    
    Returns:
        list: List of case IDs (primary first, secondary if dual-labeled)
    """
    # Remove 'AIRA_' prefix and '.nii' suffix
    core = filename.replace('AIRA_', '').replace('.nii', '')
    
    # Split by underscore for dual-labeled cases
    parts = core.split('_')
    
    case_ids = []
    for part in parts:
        # Extract case ID pattern (A-### or N-###)
        match = re.search(r'([AN]-\d+)', part, re.IGNORECASE)
        if match:
            case_ids.append(match.group(1).upper())
    
    return case_ids

def find_gt_file(case_id, gt_root, gt_type='GT01'):
    """
    Find GT01 or GT02 file for a given case ID.
    
    Parameters:
    -----------
    case_id : str
        Case ID like 'N-001' or 'A-005'
    gt_root : str
        Root directory containing case folders
    gt_type : str
        'GT01' or 'GT02'
    
    Returns:
    --------
    tuple: (gt_filepath, error_message or None)
    """
    # Extract case number (remove A/N prefix)
    case_num = re.sub(r'[AN]-?', '', case_id, flags=re.IGNORECASE)
    
    # Possible folder names
    possible_folders = [
        case_id,  # e.g., 'N-001' or 'A-005'
        case_num,  # e.g., '001' or '005'
        f"N-{case_num}",
        f"A-{case_num}",
    ]
    
    for folder_name in possible_folders:
        case_folder = os.path.join(gt_root, folder_name)
        
        if not os.path.exists(case_folder):
            continue
        
        # Look for GT file in this folder
        all_files = [f for f in os.listdir(case_folder) if f.lower().endswith('.nii')]
        
        # Pattern for GT01 or GT02
        gt_pattern = re.compile(rf'GT\s*0?{gt_type[-1]}(?:v\d+)?', re.IGNORECASE)
        
        gt_files = []
        for filename in all_files:
            if gt_pattern.search(filename):
                gt_files.append(os.path.join(case_folder, filename))
        
        if len(gt_files) == 1:
            return gt_files[0], None
        elif len(gt_files) > 1:
            return None, f"Multiple {gt_type} files found in {folder_name}"
    
    return None, f"{gt_type} file not found for case {case_id}"

def find_gt_files_with_fallback(aira_filename, gt_root):
    """
    Find GT01 and GT02 files for an AIRA case, handling dual-labeled cases.
    
    For dual-labeled cases (A-088_N-191):
      1. Try A-prefix first (A-088)
      2. Try N-prefix second (N-191)
      3. Try fallback (N-088, N-089, N-090, N-092)
    
    Returns:
    --------
    tuple: (case_id_used, gt01_path, gt02_path, error_message or None)
    """
    case_ids = extract_case_ids_from_aira(aira_filename)
    
    if DEBUG_FILE_SEARCH:
        print(f"    AIRA file: {aira_filename}")
        print(f"    Extracted IDs: {case_ids}")
    
    # Try each case ID in order
    for case_id in case_ids:
        gt01_path, gt01_error = find_gt_file(case_id, gt_root, 'GT01')
        gt02_path, gt02_error = find_gt_file(case_id, gt_root, 'GT02')
        
        if gt01_path and gt02_path:
            if DEBUG_FILE_SEARCH:
                print(f"    ✓ Found GT files using: {case_id}")
            return case_id, gt01_path, gt02_path, None
    
    # Try fallback for special dual-labeled cases
    primary_case_id = case_ids[0] if case_ids else None
    if primary_case_id in DUAL_LABEL_FALLBACKS:
        fallback_id = DUAL_LABEL_FALLBACKS[primary_case_id]
        if DEBUG_FILE_SEARCH:
            print(f"    Trying fallback: {fallback_id}")
        
        gt01_path, gt01_error = find_gt_file(fallback_id, gt_root, 'GT01')
        gt02_path, gt02_error = find_gt_file(fallback_id, gt_root, 'GT02')
        
        if gt01_path and gt02_path:
            if DEBUG_FILE_SEARCH:
                print(f"    ✓ Found GT files using fallback: {fallback_id}")
            return fallback_id, gt01_path, gt02_path, None
    
    # No GT files found
    error_msg = f"GT files not found for any of: {', '.join(case_ids)}"
    if primary_case_id in DUAL_LABEL_FALLBACKS:
        error_msg += f" (tried fallback: {DUAL_LABEL_FALLBACKS[primary_case_id]})"
    
    return case_ids[0] if case_ids else 'UNKNOWN', None, None, error_msg

# ============================================================================
# COMPARISON FUNCTIONS
# ============================================================================

def compare_masks(case_id, aira_path, gt_path, aira_filename, gt_filename, comparison_type):
    """
    Compare AIRA mask against GT mask (GT01 or GT02).
    
    Parameters:
    -----------
    case_id : str
        Case identifier
    aira_path : str
        Path to AIRA mask file
    gt_path : str
        Path to GT mask file
    aira_filename : str
        AIRA filename for CSV
    gt_filename : str
        GT filename for CSV
    comparison_type : str
        'AIRA_vs_GT01' or 'AIRA_vs_GT02'
    
    Returns:
    --------
    tuple: (list of CSV row dicts, error_message or None)
    """
    try:
        # Load both masks
        aira_img = load_nifti(aira_path)
        gt_img = load_nifti(gt_path)
        
        # Check and correct orientation if needed
        orientation_aira = get_orientation_string(aira_img)
        orientation_gt = get_orientation_string(gt_img)
        
        if orientation_aira != orientation_gt:
            gt_img = reorient_to_match(aira_img, gt_img)
        
        # Get data arrays
        aira_data = aira_img.get_fdata()
        gt_data = gt_img.get_fdata()
        
        # Shape validation
        if aira_data.shape != gt_data.shape:
            return None, f"Shape mismatch: AIRA {aira_data.shape} vs GT {gt_data.shape}"
        
        # Get voxel information
        voxel_volume_mm3, _ = get_voxel_volume(aira_img)
        
        # Extract individual kidney masks
        # Label 1 = Right Kidney, Label 2 = Left Kidney (Radiologist's perspective)
        right_kidney_aira = (aira_data == 1).astype(np.float32)
        right_kidney_gt = (gt_data == 1).astype(np.float32)
        
        left_kidney_aira = (aira_data == 2).astype(np.float32)
        left_kidney_gt = (gt_data == 2).astype(np.float32)
        
        # Calculate Dice scores
        dice_right = dice_coefficient(right_kidney_aira, right_kidney_gt)
        dice_left = dice_coefficient(left_kidney_aira, left_kidney_gt)
        
        # Calculate volumes
        right_vol_mm3_aira, right_vol_cm3_aira = calculate_volume(right_kidney_aira, voxel_volume_mm3)
        right_vol_mm3_gt, right_vol_cm3_gt = calculate_volume(right_kidney_gt, voxel_volume_mm3)
        
        left_vol_mm3_aira, left_vol_cm3_aira = calculate_volume(left_kidney_aira, voxel_volume_mm3)
        left_vol_mm3_gt, left_vol_cm3_gt = calculate_volume(left_kidney_gt, voxel_volume_mm3)
        
        # Calculate differences
        right_diff = calc_diff_percent(right_vol_cm3_aira, right_vol_cm3_gt)
        left_diff = calc_diff_percent(left_vol_cm3_aira, left_vol_cm3_gt)
        
        right_larger = larger_mask(right_vol_cm3_aira, right_vol_cm3_gt)
        left_larger = larger_mask(left_vol_cm3_aira, left_vol_cm3_gt)
        
        # Calculate arithmetic mean for average (FDA convention)
        dice_average = (dice_right + dice_left) / 2
        
        # Create CSV rows (3 rows per case - matching FDA format)
        rows = [
            # Row 1: Right Kidney
            {
                'Patient': case_id,
                'AIRA_File': aira_filename,
                'GT_File': gt_filename,
                'Organ': 'Right Kidney',
                'DiceCoefficient': f"{dice_right:.6f}",
                'AIRA_Volume_mm3': f"{right_vol_mm3_aira:.2f}",
                'GT_Volume_mm3': f"{right_vol_mm3_gt:.2f}",
                'AIRA_Volume_cm3': f"{right_vol_cm3_aira:.2f}",
                'GT_Volume_cm3': f"{right_vol_cm3_gt:.2f}",
                'DiffPercent': right_diff,
                'LargerMask': right_larger,
                'Error': ''
            },
            # Row 2: Left Kidney
            {
                'Patient': case_id,
                'AIRA_File': aira_filename,
                'GT_File': gt_filename,
                'Organ': 'Left Kidney',
                'DiceCoefficient': f"{dice_left:.6f}",
                'AIRA_Volume_mm3': f"{left_vol_mm3_aira:.2f}",
                'GT_Volume_mm3': f"{left_vol_mm3_gt:.2f}",
                'AIRA_Volume_cm3': f"{left_vol_cm3_aira:.2f}",
                'GT_Volume_cm3': f"{left_vol_cm3_gt:.2f}",
                'DiffPercent': left_diff,
                'LargerMask': left_larger,
                'Error': ''
            },
            # Row 3: Average (FDA convention: arithmetic mean of Right and Left Dice)
            {
                'Patient': case_id,
                'AIRA_File': aira_filename,
                'GT_File': gt_filename,
                'Organ': f'{case_id} Average',
                'DiceCoefficient': f"{dice_average:.6f}",
                'AIRA_Volume_mm3': '',
                'GT_Volume_mm3': '',
                'AIRA_Volume_cm3': '',
                'GT_Volume_cm3': '',
                'DiffPercent': '',
                'LargerMask': '',
                'Error': ''
            }
        ]
        
        return rows, None
        
    except Exception as e:
        error_msg = f"ERROR: {str(e)}"
        return None, error_msg

# ============================================================================
# MAIN PROCESSING
# ============================================================================

def main():
    """Main processing function."""
    print("=" * 80)
    print("AIRA vs GROUND TRUTH COMPARISON")
    print("=" * 80)
    print(f"AIRA Directory: {AIRA_MASKS_DIR}")
    print(f"GT Directory: {GT_ROOT_DIR}")
    print(f"Output Directory: {OUTPUT_DIR}")
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    if MAX_CASES_TO_PROCESS is not None:
        print(f"\n⚠️  DEBUG MODE: Processing only {MAX_CASES_TO_PROCESS} cases")
    else:
        print(f"\n✓ Processing ALL cases")
    
    if DEBUG_FILE_SEARCH:
        print(f"✓ Debug file search: ENABLED")
    
    print("=" * 80)
    
    # Create output directory
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # Find all AIRA files
    print("\n📂 Scanning for AIRA mask files...")
    aira_files = find_aira_files(AIRA_MASKS_DIR)
    
    if not aira_files:
        print("❌ No AIRA files found!")
        return
    
    print(f"✓ Found {len(aira_files)} AIRA mask files")
    
    # Limit cases if in debug mode
    if MAX_CASES_TO_PROCESS is not None:
        original_count = len(aira_files)
        aira_files = aira_files[:MAX_CASES_TO_PROCESS]
        print(f"⚠️  Limited to first {len(aira_files)} cases (out of {original_count})")
    
    # Process each case
    print(f"\n{'='*80}")
    print("PROCESSING CASES")
    print(f"{'='*80}\n")
    
    aira_vs_gt01_rows = []
    aira_vs_gt02_rows = []
    success_count = 0
    error_count = 0
    error_cases = []
    
    for idx, (aira_filename, aira_path) in enumerate(aira_files, 1):
        print(f"[{idx}/{len(aira_files)}] Processing: {aira_filename}")
        
        # Find corresponding GT files
        case_id, gt01_path, gt02_path, find_error = find_gt_files_with_fallback(
            aira_filename, GT_ROOT_DIR
        )
        
        if find_error:
            print(f"  ⚠️  {find_error}")
            error_count += 1
            error_cases.append((aira_filename, find_error))
            
            # Add error rows to both sheets
            error_row = {
                'Patient': case_id,
                'AIRA_File': aira_filename,
                'GT_File': '',
                'Organ': 'ERROR',
                'DiceCoefficient': '',
                'AIRA_Volume_mm3': '',
                'GT_Volume_mm3': '',
                'AIRA_Volume_cm3': '',
                'GT_Volume_cm3': '',
                'DiffPercent': '',
                'LargerMask': '',
                'Error': find_error
            }
            aira_vs_gt01_rows.append(error_row.copy())
            aira_vs_gt02_rows.append(error_row.copy())
            continue
        
        # Compare AIRA vs GT01
        gt01_filename = os.path.basename(gt01_path)
        rows_gt01, error_gt01 = compare_masks(
            case_id, aira_path, gt01_path, 
            aira_filename, gt01_filename, 
            'AIRA_vs_GT01'
        )
        
        # Compare AIRA vs GT02
        gt02_filename = os.path.basename(gt02_path)
        rows_gt02, error_gt02 = compare_masks(
            case_id, aira_path, gt02_path, 
            aira_filename, gt02_filename, 
            'AIRA_vs_GT02'
        )
        
        if error_gt01 or error_gt02:
            print(f"  ❌ GT01 Error: {error_gt01}" if error_gt01 else "")
            print(f"  ❌ GT02 Error: {error_gt02}" if error_gt02 else "")
            error_count += 1
            error_cases.append((aira_filename, error_gt01 or error_gt02))
            
            # Add error rows
            if error_gt01:
                aira_vs_gt01_rows.append({
                    'Patient': case_id,
                    'AIRA_File': aira_filename,
                    'GT_File': gt01_filename if gt01_path else '',
                    'Organ': 'ERROR',
                    'DiceCoefficient': '',
                    'AIRA_Volume_mm3': '',
                    'GT_Volume_mm3': '',
                    'AIRA_Volume_cm3': '',
                    'GT_Volume_cm3': '',
                    'DiffPercent': '',
                    'LargerMask': '',
                    'Error': error_gt01
                })
            
            if error_gt02:
                aira_vs_gt02_rows.append({
                    'Patient': case_id,
                    'AIRA_File': aira_filename,
                    'GT_File': gt02_filename if gt02_path else '',
                    'Organ': 'ERROR',
                    'DiceCoefficient': '',
                    'AIRA_Volume_mm3': '',
                    'GT_Volume_mm3': '',
                    'AIRA_Volume_cm3': '',
                    'GT_Volume_cm3': '',
                    'DiffPercent': '',
                    'LargerMask': '',
                    'Error': error_gt02
                })
        else:
            aira_vs_gt01_rows.extend(rows_gt01)
            aira_vs_gt02_rows.extend(rows_gt02)
            
            # Print dice scores
            dice_right_gt01 = rows_gt01[0]['DiceCoefficient']
            dice_left_gt01 = rows_gt01[1]['DiceCoefficient']
            dice_avg_gt01 = rows_gt01[2]['DiceCoefficient']
            
            dice_right_gt02 = rows_gt02[0]['DiceCoefficient']
            dice_left_gt02 = rows_gt02[1]['DiceCoefficient']
            dice_avg_gt02 = rows_gt02[2]['DiceCoefficient']
            
            print(f"  ✓ vs GT01: Right={dice_right_gt01}, Left={dice_left_gt01}, Avg={dice_avg_gt01}")
            print(f"  ✓ vs GT02: Right={dice_right_gt02}, Left={dice_left_gt02}, Avg={dice_avg_gt02}")
            success_count += 1
    
    # Save results to Excel
    print(f"\n{'='*80}")
    print("SAVING RESULTS")
    print(f"{'='*80}\n")
    
    if aira_vs_gt01_rows or aira_vs_gt02_rows:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_filename = f"AIRA_vs_Ground_Truth_{timestamp}.xlsx"
        output_path = os.path.join(OUTPUT_DIR, output_filename)
        
        # Create Excel writer
        with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
            # Sheet 1: AIRA vs GT01
            df_gt01 = pd.DataFrame(aira_vs_gt01_rows)
            df_gt01.to_excel(writer, sheet_name='AIRA_vs_GT01', index=False)
            
            # Sheet 2: AIRA vs GT02
            df_gt02 = pd.DataFrame(aira_vs_gt02_rows)
            df_gt02.to_excel(writer, sheet_name='AIRA_vs_GT02', index=False)
        
        print(f"✓ Results saved to: {output_path}")
        print(f"\nSheet 1 (AIRA_vs_GT01): {len(df_gt01)} rows")
        print(f"Sheet 2 (AIRA_vs_GT02): {len(df_gt02)} rows")
    else:
        print("❌ No results to save!")
    
    # Print summary
    print(f"\n{'='*80}")
    print("SUMMARY")
    print(f"{'='*80}")
    print(f"Total AIRA cases processed: {len(aira_files)}")
    print(f"Successful: {success_count}")
    print(f"Errors: {error_count}")
    
    if error_cases:
        print(f"\nCases with errors:")
        for aira_file, error_msg in error_cases:
            print(f"  - {aira_file}: {error_msg}")
    
    print(f"\n{'='*80}")
    print("✅ COMPARISON COMPLETE")
    print(f"{'='*80}\n")

if __name__ == "__main__":
    main()
