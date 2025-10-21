#!/usr/bin/env python3
"""
Debug script to check label values in multi-reader analysis
"""

import os
import numpy as np
import nibabel as nib

# Paths
case_id = "N-072"
fda_path = r"c:\Users\Subin-PC\Downloads\Telegram Desktop\OneDrive_1_10-8-2025\N-072\N-072\N-072_MC.nii"
aira_path = r"c:\Users\Subin-PC\Downloads\Telegram Desktop\OneDrive_1_10-8-2025\N-072\mask.nii"
as_path = r"C:\Users\Subin-PC\Downloads\Telegram Desktop\GT01 - 5 Test Cases\N-072_AS.nii"
gm_path = r"C:\Users\Subin-PC\Downloads\Telegram Desktop\GT02 - 5 Test Cases\N-072_GM.nii"

# Label mapping
LABEL_MAPPING = {
    0: 0,  # Background -> Background
    1: 0,  # Other -> Background  
    2: 2,  # Original label 2 -> Left Kidney (our label 2)
    3: 1   # Original label 3 -> Right Kidney (our label 1)
}

def analyze_labels(file_path, name):
    """Analyze label distribution in a file."""
    print(f"\n{name}: {file_path}")
    
    if not os.path.exists(file_path):
        print("  File not found!")
        return None
    
    try:
        img = nib.load(file_path)
        data = img.get_fdata()
        
        print(f"  Shape: {data.shape}")
        print(f"  Data type: {data.dtype}")
        
        unique_labels = np.unique(data)
        print(f"  Original labels: {unique_labels}")
        
        for label in unique_labels:
            count = np.sum(data == label)
            percentage = (count / data.size) * 100
            print(f"    Label {label}: {count} voxels ({percentage:.2f}%)")
        
        # Apply label mapping
        remapped_data = np.zeros_like(data)
        for original_label, new_label in LABEL_MAPPING.items():
            remapped_data[data == original_label] = new_label
        
        unique_remapped = np.unique(remapped_data)
        print(f"  After remapping: {unique_remapped}")
        
        for label in unique_remapped:
            count = np.sum(remapped_data == label)
            percentage = (count / remapped_data.size) * 100
            print(f"    Label {label}: {count} voxels ({percentage:.2f}%)")
        
        return remapped_data
        
    except Exception as e:
        print(f"  Error: {e}")
        return None

def calculate_dice(data1, data2, class_label):
    """Calculate Dice coefficient for a specific class."""
    mask1 = (data1 == class_label)
    mask2 = (data2 == class_label)
    
    intersection = np.logical_and(mask1, mask2).sum()
    volume1 = mask1.sum()
    volume2 = mask2.sum()
    
    if volume1 == 0 and volume2 == 0:
        return 1.0
    elif volume1 == 0 or volume2 == 0:
        return 0.0
    
    dice = (2.0 * intersection) / (volume1 + volume2)
    return dice

# Analyze all files
print("="*60)
print("MULTI-READER LABEL ANALYSIS DEBUG")
print("="*60)

fda_data = analyze_labels(fda_path, "FDA Ground Truth")
aira_data = analyze_labels(aira_path, "AIRA Prediction")
as_data = analyze_labels(as_path, "AS Reader")
gm_data = analyze_labels(gm_path, "GM Reader")

# Calculate Dice coefficients if all data loaded successfully
if all(data is not None for data in [fda_data, aira_data, as_data, gm_data]):
    print("\n" + "="*60)
    print("DICE COEFFICIENT CALCULATIONS")
    print("="*60)
    
    class_names = ["Background", "Right Kidney", "Left Kidney"]
    
    comparisons = [
        ("FDA vs AIRA", fda_data, aira_data),
        ("FDA vs AS", fda_data, as_data),
        ("FDA vs GM", fda_data, gm_data),
        ("AS vs GM", as_data, gm_data)
    ]
    
    for comp_name, data1, data2 in comparisons:
        print(f"\n{comp_name}:")
        
        # Check if shapes match
        if data1.shape != data2.shape:
            print(f"  Shape mismatch: {data1.shape} vs {data2.shape}")
            continue
        
        for class_idx, class_name in enumerate(class_names):
            dice = calculate_dice(data1, data2, class_idx)
            print(f"  {class_name}: {dice:.4f}")
        
        # Overall kidney dice
        right_dice = calculate_dice(data1, data2, 1)
        left_dice = calculate_dice(data1, data2, 2)
        mean_kidney_dice = (right_dice + left_dice) / 2
        print(f"  Mean Kidneys: {mean_kidney_dice:.4f}")

print("\n" + "="*60)
print("DEBUG ANALYSIS COMPLETED")
print("="*60)