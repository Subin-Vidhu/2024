#!/usr/bin/env python3
"""
Comprehensive mask analysis script to check all files and remapping issues
"""

import os
import numpy as np
import nibabel as nib

# Paths for N-072 case
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

def remap_labels(data, label_mapping, use_rounding=True):
    """Remap labels with optional rounding for floating-point issues. Returns int16 for clean integer labels."""
    if use_rounding:
        # Round to nearest integer first to handle floating-point precision issues
        data_rounded = np.round(data).astype(np.int16)
        print(f"    After rounding - unique values: {np.unique(data_rounded)}")
    else:
        data_rounded = np.round(data).astype(np.int16)
    
    remapped_data = np.zeros_like(data_rounded, dtype=np.int16)
    for original_label, new_label in label_mapping.items():
        mask = (data_rounded == original_label)
        remapped_data[mask] = new_label
        count = np.sum(mask)
        if count > 0:
            print(f"    Mapping {original_label} -> {new_label}: {count} voxels")
    
    return remapped_data  # Return as int16 for clean integer labels

def analyze_mask_detailed(file_path, name):
    """Detailed analysis of a mask file."""
    print(f"\n{'='*60}")
    print(f"ANALYZING: {name}")
    print(f"File: {file_path}")
    print(f"{'='*60}")
    
    if not os.path.exists(file_path):
        print("❌ File not found!")
        return None
    
    try:
        # Load image
        img = nib.load(file_path)
        data = img.get_fdata()
        
        print(f"📊 Basic Info:")
        print(f"    Shape: {data.shape}")
        print(f"    Data type: {data.dtype}")
        print(f"    Min value: {data.min()}")
        print(f"    Max value: {data.max()}")
        
        # Check for floating-point precision issues
        unique_vals = np.unique(data)
        print(f"\n🔍 Original Values Analysis:")
        print(f"    Unique values: {unique_vals}")
        print(f"    Number of unique values: {len(unique_vals)}")
        
        # Check if values are exactly integers
        non_integer_values = []
        for val in unique_vals:
            if abs(val - round(val)) > 1e-10:
                non_integer_values.append(val)
        
        if non_integer_values:
            print(f"    ⚠️  Non-integer values found: {non_integer_values}")
        else:
            print(f"    ✅ All values are integers")
        
        # Show value distribution
        print(f"\n📈 Value Distribution:")
        unique_vals, counts = np.unique(data, return_counts=True)
        for val, count in zip(unique_vals, counts):
            percentage = (count / data.size) * 100
            print(f"    Label {val}: {count:,} voxels ({percentage:.3f}%)")
        
        # Apply remapping with rounding
        print(f"\n🔄 Remapping Analysis:")
        print(f"    Label mapping: {LABEL_MAPPING}")
        
        remapped_data = remap_labels(data, LABEL_MAPPING, use_rounding=True)
        
        # Check remapped results
        unique_remapped = np.unique(remapped_data)
        print(f"    Final remapped labels: {unique_remapped}")
        
        print(f"\n📊 Final Distribution:")
        for label in unique_remapped:
            count = np.sum(remapped_data == label)
            percentage = (count / remapped_data.size) * 100
            class_name = ["Background", "Right Kidney", "Left Kidney"][int(label)] if label < 3 else f"Unknown({label})"
            print(f"    {class_name} (label {label}): {count:,} voxels ({percentage:.3f}%)")
        
        return remapped_data
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def check_all_cases():
    """Check all available cases."""
    cases = ['N-072', 'N-073', 'N-085', 'N-088', 'N-090']
    base_path = r'c:\Users\Subin-PC\Downloads\Telegram Desktop\OneDrive_1_10-8-2025'
    
    print("🔍 CHECKING ALL CASES FOR LABEL ISSUES")
    print("="*80)
    
    for case in cases:
        print(f"\n🏥 CASE: {case}")
        print("-" * 40)
        
        # Check FDA ground truth
        fda_path = f'{base_path}\\{case}\\{case}\\{case}_MC.nii'
        if os.path.exists(fda_path):
            try:
                img = nib.load(fda_path)
                data = img.get_fdata()
                unique_vals = np.unique(data)
                
                # Apply remapping
                data_rounded = np.round(data).astype(int)
                remapped_data = np.zeros_like(data_rounded)
                for orig, new in LABEL_MAPPING.items():
                    remapped_data[data_rounded == orig] = new
                
                final_labels = np.unique(remapped_data)
                
                print(f"  FDA {case}:")
                print(f"    Original: {unique_vals}")
                print(f"    After remapping: {final_labels}")
                print(f"    Has Right Kidney (label 1): {1 in final_labels}")
                print(f"    Has Left Kidney (label 2): {2 in final_labels}")
                
            except Exception as e:
                print(f"  FDA {case}: Error - {e}")
        else:
            print(f"  FDA {case}: File not found")
        
        # Check AIRA prediction
        aira_path = f'{base_path}\\{case}\\mask.nii'
        if os.path.exists(aira_path):
            try:
                img = nib.load(aira_path)
                data = img.get_fdata()
                unique_vals = np.unique(data)
                
                # Apply remapping
                data_rounded = np.round(data).astype(int)
                remapped_data = np.zeros_like(data_rounded)
                for orig, new in LABEL_MAPPING.items():
                    remapped_data[data_rounded == orig] = new
                
                final_labels = np.unique(remapped_data)
                
                print(f"  AIRA {case}:")
                print(f"    Original: {unique_vals}")
                print(f"    After remapping: {final_labels}")
                print(f"    Has Right Kidney (label 1): {1 in final_labels}")
                print(f"    Has Left Kidney (label 2): {2 in final_labels}")
                
            except Exception as e:
                print(f"  AIRA {case}: Error - {e}")
        else:
            print(f"  AIRA {case}: File not found")

# Run comprehensive analysis
print("🎯 COMPREHENSIVE MASK ANALYSIS")
print("="*80)

# First, detailed analysis of N-072
files_to_analyze = [
    (fda_path, "FDA Ground Truth N-072"),
    (aira_path, "AIRA Prediction N-072"),
    (as_path, "AS Reader N-072"),
    (gm_path, "GM Reader N-072")
]

analyzed_data = {}
for file_path, name in files_to_analyze:
    data = analyze_mask_detailed(file_path, name)
    if data is not None:
        analyzed_data[name] = data

# Then check all cases quickly
check_all_cases()

print(f"\n{'='*80}")
print("ANALYSIS COMPLETED")
print(f"{'='*80}")