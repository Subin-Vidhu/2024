#!/usr/bin/env python3
"""
Check the unique values in the processed AIRA masks
"""

import os
import numpy as np
import nibabel as nib

# Path to processed masks
PROCESSED_PATH = r"D:\__SHARED__\AIRA_FDA_SET_2_LIVE\test"

def check_processed_mask(case_folder):
    """Check unique values in a processed mask."""
    processed_file = os.path.join(PROCESSED_PATH, case_folder, "aira_mask_processed.nii")
    
    if not os.path.exists(processed_file):
        print(f"{case_folder}: Processed file not found")
        return
    
    print(f"\n{'='*60}")
    print(f"Checking: {case_folder}")
    print(f"{'='*60}")
    
    # Load the processed mask
    img = nib.load(processed_file)
    data = img.get_fdata()
    
    unique_vals = np.unique(data)
    
    print(f"Data type: {data.dtype}")
    print(f"Shape: {data.shape}")
    print(f"Unique values: {unique_vals}")
    print(f"Number of unique values: {len(unique_vals)}")
    
    # Check if values are exactly integers
    print(f"\nDetailed value analysis:")
    for val in unique_vals[:20]:  # Show first 20 values
        count = np.sum(data == val)
        is_integer = abs(val - round(val)) < 1e-10
        print(f"  Value: {val:.15f} | Count: {count:,} | Integer-like: {is_integer}")
    
    # Check for non-integer values
    non_integer_vals = []
    for val in unique_vals:
        if abs(val - round(val)) > 1e-10:
            non_integer_vals.append(val)
    
    if non_integer_vals:
        print(f"\n⚠️  WARNING: Non-integer values found!")
        print(f"Non-integer values: {non_integer_vals[:10]}")
    else:
        print(f"\n✓ All values are integers or integer-like")

# Check all cases
cases = ['A-089(N195)', 'A-092(N210)', 'N-071', 'N-092', 'N-094']

for case in cases:
    check_processed_mask(case)

print(f"\n{'='*60}")
print("ANALYSIS COMPLETE")
print(f"{'='*60}")
