#!/usr/bin/env python3
"""
Quick test to verify the default LPI orientation logic works correctly
"""

import nibabel as nib
import numpy as np

def get_orientation_string(img):
    """Get orientation string from NIfTI image."""
    return nib.orientations.aff2axcodes(img.affine)

def test_orientation_conversion():
    """Test that we can convert RAS to LPI programmatically"""
    print("=" * 70)
    print("Testing Default LPI Orientation Conversion")
    print("=" * 70)
    
    # Create a dummy NIfTI image in RAS orientation
    data = np.zeros((10, 10, 10), dtype=np.int16)
    data[5, 5, 5] = 1  # Add a marker voxel
    
    # Create RAS affine
    affine = np.array([
        [1,  0,  0,  0],
        [0,  1,  0,  0],
        [0,  0,  1,  0],
        [0,  0,  0,  1]
    ])
    
    img = nib.Nifti1Image(data, affine)
    original_orientation = ''.join(get_orientation_string(img))
    print(f"\n✓ Created test image with orientation: {original_orientation}")
    
    # Convert to LPI
    DEFAULT_ORIENTATION = 'LPI'
    print(f"\n🔄 Converting {original_orientation} → {DEFAULT_ORIENTATION}...")
    
    try:
        target_ornt = nib.orientations.axcodes2ornt(DEFAULT_ORIENTATION)
        current_ornt = nib.orientations.io_orientation(img.affine)
        ornt_transform = nib.orientations.ornt_transform(current_ornt, target_ornt)
        processed_img = img.as_reoriented(ornt_transform)
        
        final_orientation = ''.join(get_orientation_string(processed_img))
        print(f"✓ Conversion successful!")
        print(f"  Final orientation: {final_orientation}")
        
        if final_orientation == DEFAULT_ORIENTATION:
            print(f"\n✅ TEST PASSED: Orientation correctly converted to {DEFAULT_ORIENTATION}")
        else:
            print(f"\n❌ TEST FAILED: Expected {DEFAULT_ORIENTATION}, got {final_orientation}")
            
    except Exception as e:
        print(f"❌ TEST FAILED: {e}")
    
    print("\n" + "=" * 70)

if __name__ == "__main__":
    test_orientation_conversion()
