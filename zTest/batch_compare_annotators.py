#!/usr/bin/env python3
"""
Batch Compare Two Annotators - Inter-Observer Agreement Analysis
=================================================================

This script processes multiple cases and compares segmentation masks from 
two different annotators to calculate inter-observer agreement metrics.

IMPORTANT - LABEL CONVENTION (RADIOLOGIST'S PERSPECTIVE):
----------------------------------------------------------
This script uses the RADIOLOGIST'S VIEWING PERSPECTIVE:
  - Label 1 = RIGHT kidney (patient's right side, left side of screen)
  - Label 2 = LEFT kidney (patient's left side, right side of screen)

This is OPPOSITE to the anatomical convention used in FDA scripts where:
  - Label 1 = LEFT kidney (anatomical left)
  - Label 2 = RIGHT kidney (anatomical right)

WHY THE DIFFERENCE?
When radiologists view medical images, they look at the patient from the front,
so left and right are flipped from the patient's anatomical perspective.
In LPI orientation, lower X coordinates are on the patient's RIGHT side.

DICE COEFFICIENT CALCULATION:
This script uses the FDA-COMPLIANT enhanced dice coefficient with:
  - Boolean logic operations (&) for intersection
  - Explicit binary mask conversion
  - Proper edge case handling
  - Value clamping to [0,1] range
This matches the implementation in fda_multiple_case_dice.py (FDA compliant version).

Usage:
    python batch_compare_annotators.py

Author: Medical AI Validation Team
Date: 2025-11-07
"""

import os
import sys
import glob
import numpy as np
import nibabel as nib
import pandas as pd
from datetime import datetime

# ============================================================================
# CONFIGURATION - EDIT THESE PATHS
# ============================================================================

# Root directory containing case folders
BATCH_ROOT_DIR = r'c:\Users\Subin-PC\Downloads\Telegram Desktop\dice_run\dice_run'

# Naming patterns for the two annotators' files
# Use wildcards (*) for flexible matching
ANNOTATOR_1_PATTERN = '*_AS.nii'  # Files ending with _AS.nii
ANNOTATOR_2_PATTERN = '*_GM.nii'  # Files ending with _GM.nii

# Output directory for results
OUTPUT_DIR = r'd:\2024\zTest\results\batch_annotator_comparison'

# ============================================================================
# CORE FUNCTIONS (Same as single case script)
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
    
    Uses boolean logic operations for more accurate intersection calculation
    compared to simple multiplication. This implementation matches the enhanced
    version in fda_multiple_case_dice.py.
    
    Formula: Dice = 2 * |A ∩ B| / (|A| + |B|)
    
    References:
    - Dice, L.R. (1945). Ecology 26(3): 297-302
    - Zou et al. (2004). Academic Radiology 11(2): 178-189
    - Taha & Hanbury (2015). BMC Medical Imaging 15: 29
    
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
    
    # Convert to binary masks with explicit casting for FDA compliance
    y_true_bin = y_true.astype(np.bool_)
    y_pred_bin = y_pred.astype(np.bool_)
    
    # Calculate components using logical operations for accuracy
    intersection = np.sum(y_true_bin & y_pred_bin)
    sum_true = np.sum(y_true_bin)
    sum_pred = np.sum(y_pred_bin)
    
    # Handle edge cases per FDA requirements
    if sum_true == 0 and sum_pred == 0:
        return 1.0  # Perfect agreement on empty regions
    elif sum_true == 0 or sum_pred == 0:
        return 0.0  # No overlap possible
    
    # Standard Sørensen-Dice formula with numerical stability
    dice = (2.0 * intersection + epsilon) / (sum_true + sum_pred + epsilon)
    
    # Ensure valid range [0,1]
    return np.clip(dice, 0.0, 1.0)

def multi_class_dice(mask1, mask2, num_classes=3):
    """Compute Dice coefficient for each class."""
    dice_scores = []
    for c in range(num_classes):
        mask1_c = (mask1 == c).astype(np.float32)
        mask2_c = (mask2 == c).astype(np.float32)
        dice_score = dice_coefficient(mask1_c, mask2_c)
        dice_scores.append(dice_score)
    return dice_scores

def calculate_volumes(data, voxel_volume_mm3, num_classes=3):
    """Calculate volume for each class in cm³."""
    volumes = []
    for c in range(num_classes):
        count = np.sum(data == c)
        volume_cm3 = (count * voxel_volume_mm3) / 1000.0
        volumes.append(volume_cm3)
    return volumes

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

def find_annotator_files(case_folder, pattern1, pattern2):
    """Find annotator files in a case folder based on patterns."""
    # Search for files matching the patterns
    files1 = glob.glob(os.path.join(case_folder, pattern1))
    files2 = glob.glob(os.path.join(case_folder, pattern2))
    
    if len(files1) == 0:
        return None, None, f"Annotator 1 file not found (pattern: {pattern1})"
    if len(files2) == 0:
        return None, None, f"Annotator 2 file not found (pattern: {pattern2})"
    
    if len(files1) > 1:
        return None, None, f"Multiple Annotator 1 files found: {files1}"
    if len(files2) > 1:
        return None, None, f"Multiple Annotator 2 files found: {files2}"
    
    return files1[0], files2[0], None

def process_single_case(case_id, annotator1_path, annotator2_path):
    """
    Process a single case and return CSV rows.
    Returns: (list of CSV row dicts, error_message or None)
    """
    try:
        # Load both annotations
        img1 = load_nifti(annotator1_path)
        img2 = load_nifti(annotator2_path)
        
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
        
        # Calculate Dice scores
        # =====================================================================
        # IMPORTANT: RADIOLOGIST'S PERSPECTIVE (VIEWING FROM FRONT)
        # =====================================================================
        # This differs from FDA scripts which use anatomical convention!
        #
        # In LPI orientation with radiologist viewing from front:
        #   - Lower X coordinates (~155) = Patient's RIGHT side = Label 1
        #   - Higher X coordinates (~360) = Patient's LEFT side = Label 2
        #
        # Therefore:
        #   - Label 1 = RIGHT kidney (patient's right, radiologist's left on screen)
        #   - Label 2 = LEFT kidney (patient's left, radiologist's right on screen)
        #
        # NOTE: FDA scripts use opposite convention (Label 1=Left, Label 2=Right)
        # based on anatomical naming. Both are correct in their respective contexts.
        # =====================================================================
        class_names = ['Background', 'Right Kidney', 'Left Kidney']
        num_classes = len(class_names)
        
        dice_scores = multi_class_dice(data1, data2, num_classes)
        
        # Calculate volumes
        volumes1 = calculate_volumes(data1, voxel_volume_mm3, num_classes)
        volumes2 = calculate_volumes(data2, voxel_volume_mm3, num_classes)
        
        # Extract patient number and filenames
        patient_num = case_id.split('-')[-1] if '-' in case_id else case_id
        mask1_filename = os.path.basename(annotator1_path)
        mask2_filename = os.path.basename(annotator2_path)
        
        # Create CSV rows
        csv_data = []
        
        # Row 1: Right Kidney
        # Using Label 1 which corresponds to RIGHT kidney (radiologist's perspective)
        # This is the kidney at lower X coordinate (~155) = patient's right side
        csv_data.append({
            'Patient': patient_num,
            'Mask1': mask1_filename,
            'Mask2': mask2_filename,
            'Organ': 'Right Kidney',
            'DiceCoefficient': round(dice_scores[1], 6),
            'Mask1_Volume_mm3': round(volumes1[1] * 1000, 2),
            'Mask2_Volume_mm3': round(volumes2[1] * 1000, 2),
            'Mask1_Volume_cm3': round(volumes1[1], 2),
            'Mask2_Volume_cm3': round(volumes2[1], 2),
            'DiffPercent': f"{abs((volumes2[1] - volumes1[1]) / volumes1[1] * 100):.2f}%" if volumes1[1] > 0 else "0.00%",
            'LargerMask': 'Mask1' if volumes1[1] > volumes2[1] else 'Mask2',
            'Error': ''
        })
        
        # Row 2: Left Kidney (Label 2 from radiologist's perspective)
        csv_data.append({
            'Patient': patient_num,
            'Mask1': mask1_filename,
            'Mask2': mask2_filename,
            'Organ': 'Left Kidney',
            'DiceCoefficient': round(dice_scores[2], 6),
            'Mask1_Volume_mm3': round(volumes1[2] * 1000, 2),
            'Mask2_Volume_mm3': round(volumes2[2] * 1000, 2),
            'Mask1_Volume_cm3': round(volumes1[2], 2),
            'Mask2_Volume_cm3': round(volumes2[2], 2),
            'DiffPercent': f"{abs((volumes2[2] - volumes1[2]) / volumes1[2] * 100):.2f}%" if volumes1[2] > 0 else "0.00%",
            'LargerMask': 'Mask1' if volumes1[2] > volumes2[2] else 'Mask2',
            'Error': ''
        })
        
        # Row 3: Both Kidneys (combined)
        both_kidneys_vol1 = volumes1[1] + volumes1[2]
        both_kidneys_vol2 = volumes2[1] + volumes2[2]
        both_kidneys_mask1 = ((data1 == 1) | (data1 == 2)).astype(np.float32)
        both_kidneys_mask2 = ((data2 == 1) | (data2 == 2)).astype(np.float32)
        both_kidneys_dice = dice_coefficient(both_kidneys_mask1, both_kidneys_mask2)
        
        csv_data.append({
            'Patient': patient_num,
            'Mask1': mask1_filename,
            'Mask2': mask2_filename,
            'Organ': 'Both Kidneys',
            'DiceCoefficient': round(both_kidneys_dice, 6),
            'Mask1_Volume_mm3': round(both_kidneys_vol1 * 1000, 2),
            'Mask2_Volume_mm3': round(both_kidneys_vol2 * 1000, 2),
            'Mask1_Volume_cm3': round(both_kidneys_vol1, 2),
            'Mask2_Volume_cm3': round(both_kidneys_vol2, 2),
            'DiffPercent': f"{abs((both_kidneys_vol2 - both_kidneys_vol1) / both_kidneys_vol1 * 100):.2f}%" if both_kidneys_vol1 > 0 else "0.00%",
            'LargerMask': 'Mask1' if both_kidneys_vol1 > both_kidneys_vol2 else 'Mask2',
            'Error': ''
        })
        
        # Row 4: Average
        # Calculate mean of Right (Label 1) and Left (Label 2) kidney Dice scores
        avg_dice = (dice_scores[1] + dice_scores[2]) / 2
        csv_data.append({
            'Patient': patient_num,
            'Mask1': mask1_filename,
            'Mask2': mask2_filename,
            'Organ': f'{patient_num} Average',
            'DiceCoefficient': round(avg_dice, 6),
            'Mask1_Volume_mm3': '',
            'Mask2_Volume_mm3': '',
            'Mask1_Volume_cm3': '',
            'Mask2_Volume_cm3': '',
            'DiffPercent': '',
            'LargerMask': '',
            'Error': ''
        })
        
        return csv_data, None
        
    except Exception as e:
        error_msg = f"Error processing case: {str(e)}"
        return None, error_msg

# ============================================================================
# MAIN BATCH PROCESSING
# ============================================================================

def batch_process_all_cases():
    """Process all cases in batch mode."""
    
    print("=" * 80)
    print("BATCH INTER-OBSERVER AGREEMENT ANALYSIS")
    print("=" * 80)
    print(f"Root directory: {BATCH_ROOT_DIR}")
    print(f"Annotator 1 pattern: {ANNOTATOR_1_PATTERN}")
    print(f"Annotator 2 pattern: {ANNOTATOR_2_PATTERN}")
    print(f"Output directory: {OUTPUT_DIR}")
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)
    
    # Create output directory
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # Find all case folders
    print("\n🔍 Scanning for case folders...")
    case_folders = find_case_folders(BATCH_ROOT_DIR)
    
    if not case_folders:
        print("❌ No case folders found!")
        return
    
    print(f"✓ Found {len(case_folders)} case folders: {[c[0] for c in case_folders]}")
    
    # Process each case
    all_csv_data = []
    successful_cases = []
    failed_cases = []
    
    print("\n" + "=" * 80)
    print("PROCESSING CASES")
    print("=" * 80)
    
    for case_id, case_path in case_folders:
        print(f"\n📂 Processing: {case_id}")
        print(f"   Path: {case_path}")
        
        # Find annotator files
        ann1_path, ann2_path, error = find_annotator_files(
            case_path, ANNOTATOR_1_PATTERN, ANNOTATOR_2_PATTERN
        )
        
        if error:
            print(f"   ❌ {error}")
            failed_cases.append((case_id, error))
            
            # Add error rows to CSV
            patient_num = case_id.split('-')[-1] if '-' in case_id else case_id
            for organ in ['Right Kidney', 'Left Kidney', 'Both Kidneys', f'{patient_num} Average']:
                all_csv_data.append({
                    'Patient': patient_num,
                    'Mask1': '',
                    'Mask2': '',
                    'Organ': organ,
                    'DiceCoefficient': '',
                    'Mask1_Volume_mm3': '',
                    'Mask2_Volume_mm3': '',
                    'Mask1_Volume_cm3': '',
                    'Mask2_Volume_cm3': '',
                    'DiffPercent': '',
                    'LargerMask': '',
                    'Error': error if organ == 'Right Kidney' else ''
                })
            continue
        
        print(f"   ✓ Found Annotator 1: {os.path.basename(ann1_path)}")
        print(f"   ✓ Found Annotator 2: {os.path.basename(ann2_path)}")
        
        # Process the case
        csv_rows, error = process_single_case(case_id, ann1_path, ann2_path)
        
        if error:
            print(f"   ❌ {error}")
            failed_cases.append((case_id, error))
            
            # Add error rows
            patient_num = case_id.split('-')[-1] if '-' in case_id else case_id
            for organ in ['Right Kidney', 'Left Kidney', 'Both Kidneys', f'{patient_num} Average']:
                all_csv_data.append({
                    'Patient': patient_num,
                    'Mask1': os.path.basename(ann1_path),
                    'Mask2': os.path.basename(ann2_path),
                    'Organ': organ,
                    'DiceCoefficient': '',
                    'Mask1_Volume_mm3': '',
                    'Mask2_Volume_mm3': '',
                    'Mask1_Volume_cm3': '',
                    'Mask2_Volume_cm3': '',
                    'DiffPercent': '',
                    'LargerMask': '',
                    'Error': error if organ == 'Right Kidney' else ''
                })
        else:
            print(f"   ✅ Success!")
            print(f"      Right Kidney Dice: {csv_rows[0]['DiceCoefficient']:.6f}")
            print(f"      Left Kidney Dice:  {csv_rows[1]['DiceCoefficient']:.6f}")
            print(f"      Average Dice:      {csv_rows[3]['DiceCoefficient']:.6f}")
            successful_cases.append(case_id)
            all_csv_data.extend(csv_rows)
    
    # Save combined CSV
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    csv_filename = f'Batch_Annotator_Comparison_{timestamp}.csv'
    csv_path = os.path.join(OUTPUT_DIR, csv_filename)
    
    df = pd.DataFrame(all_csv_data)
    df.to_csv(csv_path, index=False)
    
    # Summary
    print("\n" + "=" * 80)
    print("BATCH PROCESSING SUMMARY")
    print("=" * 80)
    print(f"Total cases processed: {len(case_folders)}")
    print(f"✅ Successful: {len(successful_cases)}")
    print(f"❌ Failed: {len(failed_cases)}")
    
    if successful_cases:
        print(f"\n✅ Successful cases: {', '.join(successful_cases)}")
    
    if failed_cases:
        print(f"\n❌ Failed cases:")
        for case_id, error in failed_cases:
            print(f"   {case_id}: {error}")
    
    print(f"\n💾 Results saved to: {csv_path}")
    print(f"\n📊 CSV contains {len(all_csv_data)} rows ({len(all_csv_data)//4} cases × 4 rows)")
    
    print("\n" + "=" * 80)
    print("✅ BATCH PROCESSING COMPLETE")
    print("=" * 80)
    
    return csv_path

# ============================================================================
# MAIN EXECUTION
# ============================================================================

if __name__ == "__main__":
    try:
        csv_path = batch_process_all_cases()
        
        print("\n🎯 Batch processing completed successfully!")
        print(f"\nTo view the results:")
        print(f"  Excel: Open {csv_path}")
        print(f"  Python: pd.read_csv(r'{csv_path}')")
        
        sys.exit(0)
        
    except Exception as e:
        print(f"\n❌ FATAL ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
