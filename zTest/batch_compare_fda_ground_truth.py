#!/usr/bin/env python3
"""
FDA Ground Truth Batch Comparison - GT01 vs GT02
=================================================

This script processes all 119 FDA trial cases and compares GT01 vs GT02 
annotator segmentation masks to calculate inter-observer agreement metrics.

Directory Structure:
--------------------
J:\FDA_GROUND_TRUTH_TRIAL_119\Aramis Truther Masks\Aramis Truther Masks\
    001\
        N-001-GT01.nii
        N-001-GT02.nii
    002\
        N-002-GT01.nii
        N-002-GT02.nii
    A-005\
        A-005-GT01.nii
        A-005-GT02.nii
    ...

LABEL CONVENTION (RADIOLOGIST'S PERSPECTIVE):
----------------------------------------------
This script uses the RADIOLOGIST'S VIEWING PERSPECTIVE:
  - Label 1 = RIGHT kidney (patient's right side)
  - Label 2 = LEFT kidney (patient's left side)

DICE COEFFICIENT CALCULATION:
------------------------------
Uses FDA-COMPLIANT enhanced dice coefficient with:
  - Boolean logic operations (&) for intersection
  - Explicit binary mask conversion
  - Proper edge case handling
  - Value clamping to [0,1] range

"BOTH KIDNEYS" CALCULATION:
----------------------------
Row 3 (Both Kidneys) uses the UNION METHOD:
  - Combines all kidney voxels: (Right ∪ Left) for both annotators
  - Then calculates Dice on the combined regions
  - Formula: Dice = 2 × |A_Both ∩ B_Both| / (|A_Both| + |B_Both|)

OUTPUT:
-------
Single CSV file with 4 rows per case:
  1. Right Kidney Dice + volumes
  2. Left Kidney Dice + volumes
  3. Both Kidneys Dice + volumes
  4. Average (same as Both Kidneys using union method)

Usage:
    python batch_compare_fda_ground_truth.py

Author: Medical AI Validation Team
Date: 2025-12-16
"""

import os
import sys
import glob
import re
import numpy as np
import nibabel as nib
import pandas as pd
from datetime import datetime

# ============================================================================
# CONFIGURATION - EDIT THESE PATHS
# ============================================================================

# Root directory containing case folders
BATCH_ROOT_DIR = r'J:\FDA_GROUND_TRUTH_TRIAL_119\Aramis Truther Masks\Aramis Truther Masks'

# Output directory for results
OUTPUT_DIR = r'd:\2024\zTest\results\fda_ground_truth_comparison'

# ============================================================================
# DEBUG MODE CONFIGURATION
# ============================================================================
# Set to None to process all cases
# Set to a number (5, 10, 20, etc.) to process only that many cases for debugging
MAX_CASES_TO_PROCESS = 10  # Change to 5, 10, or any number for testing

# Set to True to print detailed file search information
DEBUG_FILE_SEARCH = True

# ============================================================================
# CORE FUNCTIONS
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
    
    Uses boolean logic operations for accurate intersection calculation.
    
    Formula: Dice = 2 * |A ∩ B| / (|A| + |B|)
    
    Parameters:
    -----------
    y_true : numpy array
        First binary mask
    y_pred : numpy array
        Second binary mask
    epsilon : float
        Small value for numerical stability
    
    Returns:
    --------
    float : Dice coefficient in range [0, 1]
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

# ============================================================================
# BATCH PROCESSING FUNCTIONS
# ============================================================================

def find_case_folders(root_dir):
    """Find all case folders in the root directory."""
    if not os.path.exists(root_dir):
        print(f"❌ ERROR: Directory not found: {root_dir}")
        return []
    
    case_folders = []
    for item in os.listdir(root_dir):
        item_path = os.path.join(root_dir, item)
        if os.path.isdir(item_path):
            case_folders.append((item, item_path))
    
    return sorted(case_folders)

def find_gt_files(case_folder, case_id):
    """
    Find GT01 and GT02 files in a case folder with flexible naming.
    
    Handles various naming patterns:
    - Standard: N-001-GT01.nii, A-005-GT02.nii
    - Missing dash: N-227 GT02.nii
    - Extra text: A-075 2.5 GT01v4 .nii
    - Case variations: GT01, gt01, GT1, etc.
    """
    if not os.path.exists(case_folder):
        return None, None, f"Folder not found: {case_folder}"
    
    # Get all .nii files in the folder
    all_files = [f for f in os.listdir(case_folder) if f.lower().endswith('.nii')]
    
    if DEBUG_FILE_SEARCH:
        print(f"    Files in {case_id}: {all_files}")
    
    # Flexible regex patterns for GT01 and GT02
    # Matches: GT01, gt01, GT1, GT 01, GT01v4, etc.
    gt01_pattern = re.compile(r'GT\s*0?1(?:v\d+)?', re.IGNORECASE)
    gt02_pattern = re.compile(r'GT\s*0?2(?:v\d+)?', re.IGNORECASE)
    
    gt01_files = []
    gt02_files = []
    
    for filename in all_files:
        # Check if file belongs to this case (handle missing dashes)
        # Extract case number from filename (handles N-001, A-005, or just 001)
        case_match = re.search(r'([AN]-?\d+|\d+)', filename, re.IGNORECASE)
        if case_match:
            file_case_id = case_match.group(1)
            # Normalize both IDs (remove dashes, remove A/N prefix, keep just numbers)
            normalized_file_case = re.sub(r'[AN-]', '', file_case_id, flags=re.IGNORECASE)
            normalized_target_case = re.sub(r'[AN-]', '', case_id, flags=re.IGNORECASE)
            
            if normalized_file_case != normalized_target_case:
                continue  # File doesn't belong to this case
        
        # Check for GT01 or GT02 pattern
        if gt01_pattern.search(filename):
            gt01_files.append(os.path.join(case_folder, filename))
        elif gt02_pattern.search(filename):
            gt02_files.append(os.path.join(case_folder, filename))
    
    if DEBUG_FILE_SEARCH:
        print(f"    GT01 candidates: {[os.path.basename(f) for f in gt01_files]}")
        print(f"    GT02 candidates: {[os.path.basename(f) for f in gt02_files]}")
    
    # Validate results
    if len(gt01_files) == 0:
        return None, None, f"GT01 file not found (searched {len(all_files)} files)"
    if len(gt02_files) == 0:
        return None, None, f"GT02 file not found (searched {len(all_files)} files)"
    
    if len(gt01_files) > 1:
        return None, None, f"Multiple GT01 files found: {[os.path.basename(f) for f in gt01_files]}"
    if len(gt02_files) > 1:
        return None, None, f"Multiple GT02 files found: {[os.path.basename(f) for f in gt02_files]}"
    
    return gt01_files[0], gt02_files[0], None

def process_single_case(case_id, gt01_path, gt02_path):
    """
    Process a single case and return CSV rows.
    Returns: (list of CSV row dicts, error_message or None)
    """
    try:
        # Load both annotations
        img1 = load_nifti(gt01_path)
        img2 = load_nifti(gt02_path)
        
        # Check and correct orientation if needed
        orientation1 = get_orientation_string(img1)
        orientation2 = get_orientation_string(img2)
        
        if orientation1 != orientation2:
            img2 = reorient_to_match(img1, img2)
        
        # Get data arrays
        data1 = img1.get_fdata()
        data2 = img2.get_fdata()
        
        # Shape validation
        if data1.shape != data2.shape:
            return None, f"Shape mismatch: {data1.shape} vs {data2.shape}"
        
        # Get voxel information
        voxel_volume_mm3, _ = get_voxel_volume(img1)
        
        # Extract individual kidney masks
        # Label 1 = Right Kidney, Label 2 = Left Kidney (Radiologist's perspective)
        right_kidney_mask1 = (data1 == 1).astype(np.float32)
        right_kidney_mask2 = (data2 == 1).astype(np.float32)
        
        left_kidney_mask1 = (data1 == 2).astype(np.float32)
        left_kidney_mask2 = (data2 == 2).astype(np.float32)
        
        # Both kidneys using UNION method
        both_kidneys_mask1 = ((data1 == 1) | (data1 == 2)).astype(np.float32)
        both_kidneys_mask2 = ((data2 == 1) | (data2 == 2)).astype(np.float32)
        
        # Calculate Dice scores
        dice_right = dice_coefficient(right_kidney_mask1, right_kidney_mask2)
        dice_left = dice_coefficient(left_kidney_mask1, left_kidney_mask2)
        dice_both = dice_coefficient(both_kidneys_mask1, both_kidneys_mask2)
        
        # Calculate volumes
        def calculate_volume(mask, voxel_vol):
            """Calculate volume in both mm³ and cm³."""
            voxel_count = np.sum(mask > 0)
            vol_mm3 = voxel_count * voxel_vol
            vol_cm3 = vol_mm3 / 1000.0
            return vol_mm3, vol_cm3
        
        # Right kidney volumes
        right_vol_mm3_gt01, right_vol_cm3_gt01 = calculate_volume(right_kidney_mask1, voxel_volume_mm3)
        right_vol_mm3_gt02, right_vol_cm3_gt02 = calculate_volume(right_kidney_mask2, voxel_volume_mm3)
        
        # Left kidney volumes
        left_vol_mm3_gt01, left_vol_cm3_gt01 = calculate_volume(left_kidney_mask1, voxel_volume_mm3)
        left_vol_mm3_gt02, left_vol_cm3_gt02 = calculate_volume(left_kidney_mask2, voxel_volume_mm3)
        
        # Both kidneys volumes
        both_vol_mm3_gt01, both_vol_cm3_gt01 = calculate_volume(both_kidneys_mask1, voxel_volume_mm3)
        both_vol_mm3_gt02, both_vol_cm3_gt02 = calculate_volume(both_kidneys_mask2, voxel_volume_mm3)
        
        # Calculate volume differences
        def calc_diff_percent(vol1, vol2):
            """Calculate percentage difference."""
            if vol1 == 0 and vol2 == 0:
                return "0.00%"
            if vol1 == 0 or vol2 == 0:
                return "N/A"
            diff = abs(vol1 - vol2) / ((vol1 + vol2) / 2) * 100
            return f"{diff:.2f}%"
        
        def larger_mask(vol1, vol2):
            """Determine which mask is larger."""
            if abs(vol1 - vol2) < 1e-6:
                return "Equal"
            return "GT01" if vol1 > vol2 else "GT02"
        
        right_diff = calc_diff_percent(right_vol_cm3_gt01, right_vol_cm3_gt02)
        left_diff = calc_diff_percent(left_vol_cm3_gt01, left_vol_cm3_gt02)
        both_diff = calc_diff_percent(both_vol_cm3_gt01, both_vol_cm3_gt02)
        
        right_larger = larger_mask(right_vol_cm3_gt01, right_vol_cm3_gt02)
        left_larger = larger_mask(left_vol_cm3_gt01, left_vol_cm3_gt02)
        both_larger = larger_mask(both_vol_cm3_gt01, both_vol_cm3_gt02)
        
        # Get filenames
        gt01_filename = os.path.basename(gt01_path)
        gt02_filename = os.path.basename(gt02_path)
        
        # Create CSV rows (4 rows per case)
        rows = [
            # Row 1: Right Kidney
            {
                'Patient': case_id,
                'GT01_File': gt01_filename,
                'GT02_File': gt02_filename,
                'Organ': 'Right Kidney',
                'DiceCoefficient': f"{dice_right:.6f}",
                'GT01_Volume_mm3': f"{right_vol_mm3_gt01:.2f}",
                'GT02_Volume_mm3': f"{right_vol_mm3_gt02:.2f}",
                'GT01_Volume_cm3': f"{right_vol_cm3_gt01:.2f}",
                'GT02_Volume_cm3': f"{right_vol_cm3_gt02:.2f}",
                'DiffPercent': right_diff,
                'LargerMask': right_larger,
                'Error': ''
            },
            # Row 2: Left Kidney
            {
                'Patient': case_id,
                'GT01_File': gt01_filename,
                'GT02_File': gt02_filename,
                'Organ': 'Left Kidney',
                'DiceCoefficient': f"{dice_left:.6f}",
                'GT01_Volume_mm3': f"{left_vol_mm3_gt01:.2f}",
                'GT02_Volume_mm3': f"{left_vol_mm3_gt02:.2f}",
                'GT01_Volume_cm3': f"{left_vol_cm3_gt01:.2f}",
                'GT02_Volume_cm3': f"{left_vol_cm3_gt02:.2f}",
                'DiffPercent': left_diff,
                'LargerMask': left_larger,
                'Error': ''
            },
            # Row 3: Both Kidneys
            {
                'Patient': case_id,
                'GT01_File': gt01_filename,
                'GT02_File': gt02_filename,
                'Organ': 'Both Kidneys',
                'DiceCoefficient': f"{dice_both:.6f}",
                'GT01_Volume_mm3': f"{both_vol_mm3_gt01:.2f}",
                'GT02_Volume_mm3': f"{both_vol_mm3_gt02:.2f}",
                'GT01_Volume_cm3': f"{both_vol_cm3_gt01:.2f}",
                'GT02_Volume_cm3': f"{both_vol_cm3_gt02:.2f}",
                'DiffPercent': both_diff,
                'LargerMask': both_larger,
                'Error': ''
            },
            # Row 4: Average (using union method - same as Both Kidneys)
            {
                'Patient': case_id,
                'GT01_File': gt01_filename,
                'GT02_File': gt02_filename,
                'Organ': 'XXX Average',
                'DiceCoefficient': f"{dice_both:.6f}",
                'GT01_Volume_mm3': f"{both_vol_mm3_gt01:.2f}",
                'GT02_Volume_mm3': f"{both_vol_mm3_gt02:.2f}",
                'GT01_Volume_cm3': f"{both_vol_cm3_gt01:.2f}",
                'GT02_Volume_cm3': f"{both_vol_cm3_gt02:.2f}",
                'DiffPercent': both_diff,
                'LargerMask': both_larger,
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
    """Main batch processing function."""
    print("=" * 80)
    print("FDA GROUND TRUTH BATCH COMPARISON (GT01 vs GT02)")
    print("=" * 80)
    print(f"Root Directory: {BATCH_ROOT_DIR}")
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
    
    # Find all case folders
    print("\n📂 Scanning for case folders...")
    case_folders = find_case_folders(BATCH_ROOT_DIR)
    
    if not case_folders:
        print("❌ No case folders found!")
        return
    
    print(f"✓ Found {len(case_folders)} case folders")
    
    # Limit cases if in debug mode
    if MAX_CASES_TO_PROCESS is not None:
        original_count = len(case_folders)
        case_folders = case_folders[:MAX_CASES_TO_PROCESS]
        print(f"⚠️  Limited to first {len(case_folders)} cases (out of {original_count})")
    
    # Process each case
    print(f"\n{'='*80}")
    print("PROCESSING CASES")
    print(f"{'='*80}\n")
    
    all_rows = []
    success_count = 0
    error_count = 0
    error_cases = []
    
    for idx, (case_id, case_folder) in enumerate(case_folders, 1):
        print(f"[{idx}/{len(case_folders)}] Processing case: {case_id}")
        
        # Find GT files
        gt01_path, gt02_path, find_error = find_gt_files(case_folder, case_id)
        
        if find_error:
            print(f"  ⚠️  {find_error}")
            error_count += 1
            error_cases.append((case_id, find_error))
            # Add error row
            all_rows.append({
                'Patient': case_id,
                'GT01_File': '',
                'GT02_File': '',
                'Organ': 'ERROR',
                'DiceCoefficient': '',
                'GT01_Volume_mm3': '',
                'GT02_Volume_mm3': '',
                'GT01_Volume_cm3': '',
                'GT02_Volume_cm3': '',
                'DiffPercent': '',
                'LargerMask': '',
                'Error': find_error
            })
            continue
        
        # Process the case
        rows, process_error = process_single_case(case_id, gt01_path, gt02_path)
        
        if process_error:
            print(f"  ❌ {process_error}")
            error_count += 1
            error_cases.append((case_id, process_error))
            # Add error row
            all_rows.append({
                'Patient': case_id,
                'GT01_File': os.path.basename(gt01_path),
                'GT02_File': os.path.basename(gt02_path),
                'Organ': 'ERROR',
                'DiceCoefficient': '',
                'GT01_Volume_mm3': '',
                'GT02_Volume_mm3': '',
                'GT01_Volume_cm3': '',
                'GT02_Volume_cm3': '',
                'DiffPercent': '',
                'LargerMask': '',
                'Error': process_error
            })
        else:
            all_rows.extend(rows)
            # Print dice scores
            dice_right = rows[0]['DiceCoefficient']
            dice_left = rows[1]['DiceCoefficient']
            dice_both = rows[2]['DiceCoefficient']
            print(f"  ✓ Dice: Right={dice_right}, Left={dice_left}, Both={dice_both}")
            success_count += 1
    
    # Save results to CSV
    print(f"\n{'='*80}")
    print("SAVING RESULTS")
    print(f"{'='*80}\n")
    
    if all_rows:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_filename = f"FDA_GT01_vs_GT02_Comparison_{timestamp}.csv"
        output_path = os.path.join(OUTPUT_DIR, output_filename)
        
        df = pd.DataFrame(all_rows)
        df.to_csv(output_path, index=False)
        
        print(f"✓ Results saved to: {output_path}")
        print(f"\nTotal rows in CSV: {len(df)}")
    else:
        print("❌ No results to save!")
    
    # Print summary
    print(f"\n{'='*80}")
    print("SUMMARY")
    print(f"{'='*80}")
    print(f"Total cases processed: {len(case_folders)}")
    print(f"Successful: {success_count}")
    print(f"Errors: {error_count}")
    
    if error_cases:
        print(f"\nCases with errors:")
        for case_id, error_msg in error_cases:
            print(f"  - {case_id}: {error_msg}")
    
    print(f"\n{'='*80}")
    print("✅ BATCH PROCESSING COMPLETE")
    print(f"{'='*80}\n")

if __name__ == "__main__":
    main()
