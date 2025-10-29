#!/usr/bin/env python3
"""
Test the corrected label mapping approach
"""

import os
import numpy as np
import nibabel as nib

# Label mappings
LABEL_MAPPING_AIRA = {
    0: 0,  # Background -> Background
    1: 0,  # Noise (few voxels) -> Background
    2: 2,  # AIRA label 2 (spatially right kidney) -> GT right kidney (2)
    3: 1   # AIRA label 3 (spatially left kidney) -> GT left kidney (1)
}

LABEL_MAPPING_HUMAN = {
    0: 0,  # Background -> Background
    1: 1,  # Left Kidney -> Left Kidney
    2: 2   # Right Kidney -> Right Kidney
}

def remap_labels(data, label_mapping):
    """Remap labels with robust handling. Returns int16 for clean integer labels."""
    data_rounded = np.round(data).astype(np.int16)
    remapped_data = np.zeros_like(data_rounded, dtype=np.int16)
    
    for original_label, new_label in label_mapping.items():
        mask = (data_rounded == original_label)
        remapped_data[mask] = new_label
    
    return remapped_data  # Return as int16 for clean integer labels

def test_case_n072():
    """Test the remapping on N-072 case."""
    print("🧪 TESTING CORRECTED LABEL MAPPING - N-072")
    print("="*60)
    
    # Load files
    fda_path = r"c:\Users\Subin-PC\Downloads\Telegram Desktop\OneDrive_1_10-8-2025\N-072\N-072\N-072_MC.nii"
    aira_path = r"c:\Users\Subin-PC\Downloads\Telegram Desktop\OneDrive_1_10-8-2025\N-072\mask.nii"
    
    fda_img = nib.load(fda_path)
    aira_img = nib.load(aira_path)
    
    fda_data = fda_img.get_fdata()
    aira_data = aira_img.get_fdata()
    
    print("📋 BEFORE REMAPPING:")
    print(f"  FDA labels: {np.unique(fda_data)}")
    print(f"  AIRA labels: {np.unique(aira_data)}")
    
    # Apply mappings
    fda_remapped = remap_labels(fda_data, LABEL_MAPPING_HUMAN)
    aira_remapped = remap_labels(aira_data, LABEL_MAPPING_AIRA)
    
    print("\n📋 AFTER REMAPPING:")
    print(f"  FDA labels: {np.unique(fda_remapped)}")
    print(f"  AIRA labels: {np.unique(aira_remapped)}")
    
    # Check kidney presence
    print("\n🫘 KIDNEY PRESENCE CHECK:")
    print(f"  FDA - Left Kidney (1): {1 in np.unique(fda_remapped)}")
    print(f"  FDA - Right Kidney (2): {2 in np.unique(fda_remapped)}")
    print(f"  AIRA - Left Kidney (1): {1 in np.unique(aira_remapped)}")
    print(f"  AIRA - Right Kidney (2): {2 in np.unique(aira_remapped)}")
    
    # Calculate Dice coefficients
    print("\n🎯 DICE COEFFICIENT CALCULATION:")
    
    def dice_coefficient(y_true, y_pred, class_label):
        mask1 = (y_true == class_label)
        mask2 = (y_pred == class_label)
        
        intersection = np.logical_and(mask1, mask2).sum()
        volume1 = mask1.sum()
        volume2 = mask2.sum()
        
        if volume1 == 0 and volume2 == 0:
            return 1.0
        elif volume1 == 0 or volume2 == 0:
            return 0.0
        
        dice = (2.0 * intersection) / (volume1 + volume2)
        return dice
    
    # Calculate for each kidney
    left_dice = dice_coefficient(fda_remapped, aira_remapped, 1)
    right_dice = dice_coefficient(fda_remapped, aira_remapped, 2)
    mean_dice = (left_dice + right_dice) / 2
    
    print(f"  Left Kidney (1) Dice: {left_dice:.4f}")
    print(f"  Right Kidney (2) Dice: {right_dice:.4f}")
    print(f"  Mean Kidney Dice: {mean_dice:.4f}")
    
    # Volume analysis
    voxel_volume = np.prod(fda_img.header.get_zooms()[:3]) / 1000.0  # cm³
    
    print("\n📊 VOLUME ANALYSIS:")
    for label, name in [(1, "Left Kidney"), (2, "Right Kidney")]:
        fda_count = np.sum(fda_remapped == label)
        aira_count = np.sum(aira_remapped == label)
        
        fda_vol = fda_count * voxel_volume
        aira_vol = aira_count * voxel_volume
        
        diff_abs = aira_vol - fda_vol
        diff_rel = (diff_abs / fda_vol * 100) if fda_vol > 0 else 0
        
        print(f"  {name}:")
        print(f"    FDA: {fda_vol:.2f} cm³")
        print(f"    AIRA: {aira_vol:.2f} cm³")
        print(f"    Diff: {diff_abs:+.2f} cm³ ({diff_rel:+.1f}%)")
    
    print("="*60)
    print("✅ CORRECTED MAPPING TEST COMPLETED")

if __name__ == "__main__":
    test_case_n072()