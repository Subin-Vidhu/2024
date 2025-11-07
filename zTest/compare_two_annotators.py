#!/usr/bin/env python3
"""
Compare Two Annotators - Inter-Observer Agreement Analysis
===========================================================

This script compares segmentation masks from two different annotators
to calculate inter-observer agreement metrics (Dice scores, volumes, etc.)

Simple to use for comparing any two ground truth annotations.

Usage:
    python compare_two_annotators.py

Author: Medical AI Validation Team
Date: 2025-11-07
"""

import os
import sys
import numpy as np
import nibabel as nib
import pandas as pd
from datetime import datetime

# ============================================================================
# CONFIGURATION - EDIT THESE PATHS
# ============================================================================

# Annotator 1 Ground Truth
ANNOTATOR_1_PATH = r'C:/Users/Subin-PC/Downloads/Telegram Desktop/dice_run/dice_run/test/071/N-071_Updated_AS.nii'
ANNOTATOR_1_NAME = 'Annotator_1'

# Annotator 2 Ground Truth  
ANNOTATOR_2_PATH = r'C:/Users/Subin-PC/Downloads/Telegram Desktop/dice_run/dice_run/test/071/N-071_Updated_GM.nii'
ANNOTATOR_2_NAME = 'Annotator_2'

# Case identifier (for reporting)
CASE_ID = 'N-071'

# Output directory for results
OUTPUT_DIR = r'd:\2024\zTest\results\annotator_comparison'

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
    """
    Reorient target_img to match the orientation of reference_img.
    Critical for proper spatial alignment.
    """
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
    Calculate Dice coefficient (Sørensen-Dice index) between two binary masks.
    
    Formula: Dice = 2 * |A ∩ B| / (|A| + |B|)
    
    References:
    - Dice, L.R. (1945). Ecology 26(3): 297-302
    - Zou et al. (2004). Academic Radiology 11(2): 178-189
    """
    # Input validation
    if y_true.shape != y_pred.shape:
        raise ValueError("Masks must have identical shapes")
    
    # Convert to binary masks
    y_true_bin = y_true.astype(np.bool_)
    y_pred_bin = y_pred.astype(np.bool_)
    
    # Calculate components
    intersection = np.sum(y_true_bin & y_pred_bin)
    sum_true = np.sum(y_true_bin)
    sum_pred = np.sum(y_pred_bin)
    
    # Handle edge cases
    if sum_true == 0 and sum_pred == 0:
        return 1.0  # Perfect agreement on empty regions
    elif sum_true == 0 or sum_pred == 0:
        return 0.0  # No overlap possible
    
    # Dice formula with numerical stability
    dice = (2.0 * intersection + epsilon) / (sum_true + sum_pred + epsilon)
    
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

def check_spatial_overlap(mask1, mask2, class_label):
    """Check spatial overlap and return metrics."""
    mask1_bin = (mask1 == class_label).astype(np.uint8)
    mask2_bin = (mask2 == class_label).astype(np.uint8)
    
    if np.sum(mask1_bin) == 0 or np.sum(mask2_bin) == 0:
        return None
    
    # Calculate centers of mass
    coords1 = np.argwhere(mask1_bin)
    coords2 = np.argwhere(mask2_bin)
    
    center1 = coords1.mean(axis=0)
    center2 = coords2.mean(axis=0)
    
    distance = np.linalg.norm(center1 - center2)
    overlap_voxels = np.sum(mask1_bin * mask2_bin)
    
    return {
        'center1': center1,
        'center2': center2,
        'distance': distance,
        'overlap_voxels': overlap_voxels,
        'volume1': np.sum(mask1_bin),
        'volume2': np.sum(mask2_bin)
    }

# ============================================================================
# MAIN COMPARISON FUNCTION
# ============================================================================

def compare_two_annotators():
    """Main function to compare two annotators."""
    
    print("=" * 80)
    print("INTER-OBSERVER AGREEMENT ANALYSIS")
    print("Comparing Two Annotators")
    print("=" * 80)
    print(f"Case ID: {CASE_ID}")
    print(f"Annotator 1: {ANNOTATOR_1_NAME}")
    print(f"Annotator 2: {ANNOTATOR_2_NAME}")
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)
    
    # Load both annotations
    print("\n📂 Loading annotations...")
    print(f"  Loading {ANNOTATOR_1_NAME}...")
    img1 = load_nifti(ANNOTATOR_1_PATH)
    print(f"    ✓ Shape: {img1.shape}")
    print(f"    ✓ Orientation: {get_orientation_string(img1)}")
    
    print(f"  Loading {ANNOTATOR_2_NAME}...")
    img2 = load_nifti(ANNOTATOR_2_PATH)
    print(f"    ✓ Shape: {img2.shape}")
    print(f"    ✓ Orientation: {get_orientation_string(img2)}")
    
    # Check and correct orientation if needed
    print("\n🔄 Checking spatial alignment...")
    orientation1 = get_orientation_string(img1)
    orientation2 = get_orientation_string(img2)
    
    if orientation1 != orientation2:
        print(f"  ⚠️  Orientation mismatch: {orientation1} vs {orientation2}")
        print(f"  Reorienting {ANNOTATOR_2_NAME} to match {ANNOTATOR_1_NAME}...")
        img2 = reorient_to_match(img1, img2)
        print(f"    ✓ Reorientation complete")
    else:
        print(f"  ✓ Orientations match: {orientation1}")
    
    # Get data arrays
    data1 = img1.get_fdata()
    data2 = img2.get_fdata()
    
    # Shape validation
    if data1.shape != data2.shape:
        raise ValueError(f"Shape mismatch: {data1.shape} vs {data2.shape}")
    print(f"  ✓ Shapes match: {data1.shape}")
    
    # Get voxel information
    voxel_volume_mm3, voxel_dims = get_voxel_volume(img1)
    print(f"\n📏 Voxel Information:")
    print(f"  Dimensions: {voxel_dims[0]:.2f} × {voxel_dims[1]:.2f} × {voxel_dims[2]:.2f} mm")
    print(f"  Volume: {voxel_volume_mm3:.2f} mm³")
    
    # Inspect labels
    print(f"\n🏷️  Label Analysis:")
    labels1 = np.unique(data1)
    labels2 = np.unique(data2)
    print(f"  {ANNOTATOR_1_NAME} labels: {labels1}")
    print(f"  {ANNOTATOR_2_NAME} labels: {labels2}")
    
    # Calculate Dice scores
    print("\n" + "=" * 80)
    print("DICE COEFFICIENT (Inter-Observer Agreement)")
    print("=" * 80)
    
    # IMPORTANT: Radiologist's perspective (viewing from front of patient)
    # Label 1 (lower X ~155) = RIGHT kidney (patient's right)
    # Label 2 (higher X ~360) = LEFT kidney (patient's left)
    class_names = ['Background', 'Right Kidney', 'Left Kidney']
    num_classes = len(class_names)
    
    dice_scores = multi_class_dice(data1, data2, num_classes)
    
    print(f"\n{'Class':<20} {'Dice Score':<15} {'Agreement':<20}")
    print("-" * 55)
    
    for i, (class_name, dice) in enumerate(zip(class_names, dice_scores)):
        # Classify agreement level
        if dice >= 0.95:
            agreement = "Excellent"
        elif dice >= 0.90:
            agreement = "Very Good"
        elif dice >= 0.85:
            agreement = "Good"
        elif dice >= 0.75:
            agreement = "Moderate"
        else:
            agreement = "Poor"
        
        print(f"{class_name:<20} {dice:<15.4f} {agreement:<20}")
    
    # Mean Dice (excluding background)
    kidney_dice = dice_scores[1:]
    mean_kidney_dice = np.mean(kidney_dice)
    print("-" * 55)
    print(f"{'Mean (Kidneys)':<20} {mean_kidney_dice:<15.4f}")
    print("=" * 80)
    
    # Volume Analysis
    print("\n" + "=" * 80)
    print("VOLUME ANALYSIS")
    print("=" * 80)
    
    volumes1 = calculate_volumes(data1, voxel_volume_mm3, num_classes)
    volumes2 = calculate_volumes(data2, voxel_volume_mm3, num_classes)
    
    print(f"\n{'Class':<20} {ANNOTATOR_1_NAME:<18} {ANNOTATOR_2_NAME:<18} {'Diff (cm³)':<15} {'Diff (%)':<15}")
    print("-" * 95)
    
    for i, class_name in enumerate(class_names):
        vol1 = volumes1[i]
        vol2 = volumes2[i]
        diff_cm3 = vol2 - vol1
        diff_pct = ((vol2 - vol1) / vol1 * 100) if vol1 > 0 else 0
        
        print(f"{class_name:<20} {vol1:<18.2f} {vol2:<18.2f} {diff_cm3:<+15.2f} {diff_pct:<+15.2f}")
    
    print("=" * 80)
    
    # Spatial Overlap Analysis
    print("\n" + "=" * 80)
    print("SPATIAL OVERLAP ANALYSIS")
    print("=" * 80)
    
    for class_idx, class_name in enumerate(class_names):
        if class_idx == 0:  # Skip background
            continue
        
        overlap_info = check_spatial_overlap(data1, data2, class_idx)
        
        if overlap_info:
            print(f"\n{class_name}:")
            print(f"  {ANNOTATOR_1_NAME} center: {overlap_info['center1'].astype(int)}")
            print(f"  {ANNOTATOR_2_NAME} center: {overlap_info['center2'].astype(int)}")
            print(f"  Distance between centers: {overlap_info['distance']:.2f} voxels")
            print(f"  Overlapping voxels: {overlap_info['overlap_voxels']:,}")
            print(f"  {ANNOTATOR_1_NAME} voxels: {overlap_info['volume1']:,}")
            print(f"  {ANNOTATOR_2_NAME} voxels: {overlap_info['volume2']:,}")
            
            if overlap_info['overlap_voxels'] == 0:
                print(f"  ⚠️  WARNING: No spatial overlap detected!")
        else:
            print(f"\n{class_name}: One or both annotators did not segment this structure")
    
    print("\n" + "=" * 80)
    
    # Generate Summary Report
    print("\n" + "=" * 80)
    print("SUMMARY REPORT")
    print("=" * 80)
    
    # Create results dictionary
    results = {
        'Case_ID': CASE_ID,
        'Annotator_1': ANNOTATOR_1_NAME,
        'Annotator_2': ANNOTATOR_2_NAME,
        'Dice_Background': dice_scores[0],
        'Dice_Left_Kidney': dice_scores[1],
        'Dice_Right_Kidney': dice_scores[2],
        'Mean_Dice_Kidneys': mean_kidney_dice,
        'Left_Kidney_Vol_A1_cm3': volumes1[1],
        'Left_Kidney_Vol_A2_cm3': volumes2[1],
        'Right_Kidney_Vol_A1_cm3': volumes1[2],
        'Right_Kidney_Vol_A2_cm3': volumes2[2],
    }
    
    # Clinical interpretation
    print("\n📊 Clinical Interpretation:")
    if mean_kidney_dice >= 0.95:
        print("  ✅ EXCELLENT inter-observer agreement (Dice ≥ 0.95)")
        print("  Annotations are highly consistent - minimal variability")
    elif mean_kidney_dice >= 0.90:
        print("  ✅ VERY GOOD inter-observer agreement (Dice ≥ 0.90)")
        print("  Annotations show strong consistency")
    elif mean_kidney_dice >= 0.85:
        print("  ✓ GOOD inter-observer agreement (Dice ≥ 0.85)")
        print("  Acceptable for clinical use")
    elif mean_kidney_dice >= 0.75:
        print("  ⚠️  MODERATE inter-observer agreement (Dice 0.75-0.85)")
        print("  Some variability present - review recommended")
    else:
        print("  ❌ POOR inter-observer agreement (Dice < 0.75)")
        print("  Significant variability - annotations may need review")
    
    # Save results
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    # Create CSV in the exact format from the example
    csv_filename = f'Annotator_Comparison_{CASE_ID}_{timestamp}.csv'
    csv_path = os.path.join(OUTPUT_DIR, csv_filename)
    
    # Extract patient number from case ID (e.g., N-071 -> 71)
    patient_num = CASE_ID.split('-')[-1] if '-' in CASE_ID else CASE_ID
    
    # Get filenames only (not full paths)
    mask1_filename = os.path.basename(ANNOTATOR_1_PATH)
    mask2_filename = os.path.basename(ANNOTATOR_2_PATH)
    
    # Create 4 rows as per the format
    csv_data = []
    
    # Row 1: Right Kidney (Radiologist's perspective: Label 1 = RIGHT kidney)
    csv_data.append({
        'Patient': patient_num,
        'Mask1': mask1_filename,
        'Mask2': mask2_filename,
        'Organ': 'Right Kidney',
        'DiceCoefficient': round(dice_scores[1], 6),  # Label 1 = Right kidney (radiologist view)
        'Mask1_Volume_mm3': round(volumes1[1] * 1000, 2),  # Convert cm³ to mm³
        'Mask2_Volume_mm3': round(volumes2[1] * 1000, 2),
        'Mask1_Volume_cm3': round(volumes1[1], 2),
        'Mask2_Volume_cm3': round(volumes2[1], 2),
        'DiffPercent': f"{abs((volumes2[1] - volumes1[1]) / volumes1[1] * 100):.2f}%" if volumes1[1] > 0 else "0.00%",
        'LargerMask': 'Mask1' if volumes1[1] > volumes2[1] else 'Mask2',
        'Error': ''
    })
    
    # Row 2: Left Kidney (Radiologist's perspective: Label 2 = LEFT kidney)
    csv_data.append({
        'Patient': patient_num,
        'Mask1': mask1_filename,
        'Mask2': mask2_filename,
        'Organ': 'Left Kidney',
        'DiceCoefficient': round(dice_scores[2], 6),  # Label 2 = Left kidney (radiologist view)
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
    # Calculate Dice for both kidneys combined
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
    
    # Row 4: Average (mean of Right + Left Dice scores)
    # dice_scores[1] = Right kidney, dice_scores[2] = Left kidney (radiologist view)
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
    
    # Create DataFrame and save
    df = pd.DataFrame(csv_data)
    df.to_csv(csv_path, index=False)
    print(f"\n💾 CSV Results saved to: {csv_path}")
    
    # Save detailed report
    report_filename = f'Annotator_Comparison_Report_{CASE_ID}_{timestamp}.txt'
    report_path = os.path.join(OUTPUT_DIR, report_filename)
    
    with open(report_path, 'w') as f:
        f.write("=" * 80 + "\n")
        f.write("INTER-OBSERVER AGREEMENT ANALYSIS REPORT\n")
        f.write("=" * 80 + "\n\n")
        f.write(f"Case ID: {CASE_ID}\n")
        f.write(f"Annotator 1: {ANNOTATOR_1_NAME}\n")
        f.write(f"  Path: {ANNOTATOR_1_PATH}\n")
        f.write(f"Annotator 2: {ANNOTATOR_2_NAME}\n")
        f.write(f"  Path: {ANNOTATOR_2_PATH}\n")
        f.write(f"Analysis Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        f.write("DICE COEFFICIENTS:\n")
        f.write("-" * 80 + "\n")
        for i, class_name in enumerate(class_names):
            f.write(f"  {class_name}: {dice_scores[i]:.4f}\n")
        f.write(f"  Mean (Kidneys Only): {mean_kidney_dice:.4f}\n\n")
        
        f.write("VOLUME COMPARISON:\n")
        f.write("-" * 80 + "\n")
        for i, class_name in enumerate(class_names):
            f.write(f"  {class_name}:\n")
            f.write(f"    {ANNOTATOR_1_NAME}: {volumes1[i]:.2f} cm³\n")
            f.write(f"    {ANNOTATOR_2_NAME}: {volumes2[i]:.2f} cm³\n")
            if volumes1[i] > 0:
                diff_pct = ((volumes2[i] - volumes1[i]) / volumes1[i]) * 100
                f.write(f"    Difference: {volumes2[i] - volumes1[i]:+.2f} cm³ ({diff_pct:+.2f}%)\n")
            f.write("\n")
    
    print(f"💾 Detailed report saved to: {report_path}")
    
    print("\n" + "=" * 80)
    print("✅ ANALYSIS COMPLETE")
    print("=" * 80)
    
    return results

# ============================================================================
# MAIN EXECUTION
# ============================================================================

if __name__ == "__main__":
    try:
        results = compare_two_annotators()
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
