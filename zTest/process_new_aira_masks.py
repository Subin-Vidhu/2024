#!/usr/bin/env python3
"""
Process New AIRA Masks - Apply All Required Preprocessing
=========================================================

This script processes new AIRA masks from SET_2_LIVE folder and applies:
1. Spatial reorientation to match ground truth
2. Label remapping (AIRA convention → Human convention)
3. Floating-point precision handling

The processed masks will be saved in the same folder structure with
all transformations applied to match ground truth masks.

Author: Medical AI Validation Team
Date: 2025-10-29
"""

import os
import sys
import glob
import numpy as np
import nibabel as nib
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# ============================================================================
# CONFIGURATION
# ============================================================================

# New AIRA masks location
NEW_AIRA_PATH = r"D:\__SHARED__\AIRA_FDA_SET_2_LIVE"

# Ground truth reference (from original FDA dataset)
# These are used as reference for orientation
GROUND_TRUTH_REFERENCE_PATH = r'c:\Users\Subin-PC\Downloads\Telegram Desktop\OneDrive_1_10-8-2025'

# AIRA Label Mapping (same as original analysis)
# AIRA uses: 0=Background, 1=Noise, 2=Left?, 3=Right?
# But spatially: label 2 is at RIGHT kidney location, label 3 is at LEFT kidney location
# So we remap to match human convention: 0=Background, 1=Left Kidney, 2=Right Kidney
LABEL_MAPPING_AIRA = {
    0: 0,  # Background → Background
    1: 0,  # Noise (few voxels) → Background
    2: 2,  # AIRA label 2 (spatially RIGHT kidney) → GT right kidney (2)
    3: 1   # AIRA label 3 (spatially LEFT kidney) → GT left kidney (1)
}

# Output configuration
OUTPUT_SUFFIX = "_processed"  # Suffix for processed files
CREATE_BACKUP = True  # Create backup of original files

# ============================================================================
# CORE PREPROCESSING FUNCTIONS
# ============================================================================

def load_nifti(file_path):
    """
    Load a NIfTI file safely with error handling.
    Handles both .nii and .nii.gz files, including files with .gz extension that aren't actually gzipped.
    """
    try:
        if not os.path.exists(file_path):
            print(f"  ✗ File not found: {file_path}")
            return None
        
        # Try to load the file normally
        try:
            img = nib.load(file_path)
            return img
        except Exception as gz_error:
            # If it fails and has .gz extension, it might be a .nii file misnamed as .nii.gz
            if file_path.endswith('.nii.gz'):
                print(f"    ⚠️  .nii.gz file appears to not be gzipped, trying to rename...")
                
                # Create a temporary .nii filename
                temp_nii_path = file_path[:-3]  # Remove .gz extension
                
                # Try renaming and loading
                try:
                    import shutil
                    shutil.copy2(file_path, temp_nii_path)
                    img = nib.load(temp_nii_path)
                    
                    # If successful, permanently rename the file
                    backup_path = file_path + '.backup'
                    shutil.move(file_path, backup_path)
                    shutil.move(temp_nii_path, file_path[:-3])
                    
                    print(f"    ✓ File was not gzipped - renamed to .nii format")
                    print(f"    ✓ Original backed up as: {os.path.basename(backup_path)}")
                    
                    # Reload from the new path
                    img = nib.load(file_path[:-3])
                    return img
                    
                except Exception as rename_error:
                    # Clean up temp file if it exists
                    if os.path.exists(temp_nii_path):
                        os.remove(temp_nii_path)
                    raise gz_error  # Re-raise original error
            else:
                raise gz_error
                
    except Exception as e:
        print(f"  ✗ Error loading {file_path}: {e}")
        return None

def get_orientation_string(img):
    """Get the orientation string for a NIfTI image."""
    try:
        ornt = nib.orientations.io_orientation(img.affine)
        return ''.join(nib.orientations.ornt2axcodes(ornt))
    except Exception as e:
        print(f"  ⚠️  Could not determine orientation: {e}")
        return None

def reorient_to_match(reference_img, target_img):
    """
    Reorient target_img to match the orientation of reference_img.
    
    This is the CRITICAL step that fixed the 0.0000 Dice issue.
    """
    try:
        # Get orientation transformation
        target_ornt = nib.orientations.io_orientation(target_img.affine)
        ref_ornt = nib.orientations.io_orientation(reference_img.affine)
        
        # Calculate transformation
        ornt_transform = nib.orientations.ornt_transform(target_ornt, ref_ornt)
        
        # Apply reorientation
        reoriented_img = target_img.as_reoriented(ornt_transform)
        
        return reoriented_img
    except Exception as e:
        print(f"  ✗ Error during reorientation: {e}")
        return None

def remap_labels(data, label_mapping):
    """
    Remap labels according to specified mapping with robust handling.
    Handles floating-point precision issues by rounding to nearest integer first.
    
    Parameters:
    -----------
    data : numpy array
        The data array with original labels
    label_mapping : dict
        Dictionary mapping old labels to new labels
    
    Returns:
    --------
    remapped_data : numpy array
        Data array with remapped labels (as integers)
    """
    # Handle floating-point precision issues by rounding to nearest integer
    data_rounded = np.round(data).astype(np.int16)
    
    # Create output array as int16 (sufficient for label values 0-3)
    remapped_data = np.zeros_like(data_rounded, dtype=np.int16)
    
    # Apply mapping
    for original_label, new_label in label_mapping.items():
        mask = (data_rounded == original_label)
        remapped_data[mask] = new_label
    
    return remapped_data  # Return as int16 for clean integer labels

def get_voxel_volume(img):
    """Calculate the volume of a single voxel in mm³."""
    voxel_dims = np.abs(img.header.get_zooms()[:3])
    voxel_volume = np.prod(voxel_dims)
    return voxel_volume, voxel_dims

# ============================================================================
# PROCESSING FUNCTIONS
# ============================================================================

def find_aira_cases():
    """Find all case folders in the new AIRA path."""
    if not os.path.exists(NEW_AIRA_PATH):
        print(f"❌ ERROR: Path does not exist: {NEW_AIRA_PATH}")
        return []
    
    # Look for case folders (assuming they start with 'N-' or similar pattern)
    case_folders = []
    
    for item in os.listdir(NEW_AIRA_PATH):
        item_path = os.path.join(NEW_AIRA_PATH, item)
        if os.path.isdir(item_path):
            case_folders.append((item, item_path))
    
    return sorted(case_folders)

def find_aira_mask_in_folder(folder_path):
    """Find AIRA mask file in a folder (mask.nii or mask.nii.gz)."""
    # First, check direct patterns in the folder - prioritize .nii.gz
    direct_patterns = [
        'mask.nii.gz',
        'mask.nii',
        '*_AIRA.nii.gz',
        '*_AIRA.nii',
        '*_prediction.nii.gz',
        '*_prediction.nii',
    ]
    
    for pattern in direct_patterns:
        full_pattern = os.path.join(folder_path, pattern)
        files = glob.glob(full_pattern)
        if files:
            # Print found files for debugging
            print(f"    Found mask file: {os.path.basename(files[0])}")
            return files[0]
    
    # Search for any .nii.gz files first, then .nii files
    for extension in ['*.nii.gz', '*.nii']:
        full_pattern = os.path.join(folder_path, extension)
        files = glob.glob(full_pattern)
        if files:
            print(f"    Found NIfTI file: {os.path.basename(files[0])}")
            return files[0]
    
    # If not found in root, search recursively in subdirectories
    print(f"    Searching subdirectories...")
    for root, dirs, files in os.walk(folder_path):
        # Check .nii.gz files first
        for file in files:
            if file.lower().endswith('.nii.gz'):
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, folder_path)
                print(f"    Found NIfTI file: {rel_path}")
                return full_path
        
        # Then check .nii files
        for file in files:
            if file.lower().endswith('.nii') and not file.lower().endswith('.nii.gz'):
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, folder_path)
                print(f"    Found NIfTI file: {rel_path}")
                return full_path
    
    return None

def find_reference_gt(case_id):
    """Find reference ground truth for a case to get orientation."""
    if not os.path.exists(GROUND_TRUTH_REFERENCE_PATH):
        return None
    
    # Try to find the case folder
    case_folder = os.path.join(GROUND_TRUTH_REFERENCE_PATH, case_id)
    
    if os.path.exists(case_folder):
        # Look for MC file
        mc_patterns = [
            os.path.join(case_folder, case_id, f'{case_id}_MC.nii'),
            os.path.join(case_folder, case_id, f'{case_id}_MC.nii.gz'),
            os.path.join(case_folder, case_id, f'{case_id}_Updated_MC.nii'),
            os.path.join(case_folder, case_id, f'{case_id}_Updated_MC.nii.gz')
        ]
        
        for pattern in mc_patterns:
            if os.path.exists(pattern):
                return pattern
    
    return None

def process_single_case(case_id, aira_mask_path, reference_gt_path=None):
    """
    Process a single AIRA mask with all required preprocessing.
    
    Steps:
    1. Load AIRA mask
    2. Load reference GT (if available) for orientation
    3. Reorient AIRA to match GT orientation
    4. Remap labels
    5. Save processed mask
    
    Returns:
    --------
    dict with processing results
    """
    print(f"\n{'='*60}")
    print(f"Processing: {case_id}")
    print(f"{'='*60}")
    
    result = {
        'case_id': case_id,
        'status': 'Failed',
        'original_path': aira_mask_path,
        'processed_path': None,
        'original_orientation': None,
        'final_orientation': None,
        'reorientation_applied': False,
        'original_labels': None,
        'remapped_labels': None,
        'error': None
    }
    
    # 1. Load AIRA mask
    print(f"  📂 Loading AIRA mask: {os.path.basename(aira_mask_path)}")
    aira_img = load_nifti(aira_mask_path)
    
    if aira_img is None:
        result['error'] = "Failed to load AIRA mask"
        return result
    
    # Get original properties
    aira_data = aira_img.get_fdata()
    original_orientation = get_orientation_string(aira_img)
    original_labels = np.unique(aira_data)
    
    result['original_orientation'] = original_orientation
    result['original_labels'] = original_labels.tolist()
    
    print(f"    Shape: {aira_data.shape}")
    print(f"    Data type: {aira_data.dtype}")
    print(f"    Orientation: {original_orientation}")
    print(f"    Original unique values: {original_labels}")
    
    # Check if values are exactly integers
    non_integer_values = []
    for val in original_labels:
        if abs(val - round(val)) > 1e-10:
            non_integer_values.append(val)
    
    if non_integer_values:
        print(f"    ⚠️  WARNING: Non-integer values detected: {non_integer_values}")
        print(f"    These will be rounded during label remapping")
    else:
        print(f"    ✓ All values are integer-like")
    
    # 2. Load reference GT for orientation (if available)
    reference_img = None
    if reference_gt_path and os.path.exists(reference_gt_path):
        print(f"  📂 Loading reference GT: {os.path.basename(reference_gt_path)}")
        reference_img = load_nifti(reference_gt_path)
        
        if reference_img:
            ref_orientation = get_orientation_string(reference_img)
            print(f"    Reference orientation: {ref_orientation}")
    
    # 3. Apply spatial reorientation (if reference available)
    processed_img = aira_img
    
    if reference_img is not None:
        ref_orientation = get_orientation_string(reference_img)
        
        if original_orientation != ref_orientation:
            print(f"  🔄 Applying reorientation: {original_orientation} → {ref_orientation}")
            reoriented_img = reorient_to_match(reference_img, aira_img)
            
            if reoriented_img is not None:
                processed_img = reoriented_img
                result['reorientation_applied'] = True
                result['final_orientation'] = ref_orientation
                print(f"    ✓ Reorientation successful")
            else:
                print(f"    ✗ Reorientation failed, using original orientation")
                result['final_orientation'] = original_orientation
        else:
            print(f"  ℹ️  Orientation matches reference, no reorientation needed")
            result['final_orientation'] = original_orientation
    else:
        print(f"  ⚠️  No reference GT found, skipping reorientation")
        result['final_orientation'] = original_orientation
    
    # 4. Apply label remapping
    print(f"  🏷️  Applying label remapping")
    processed_data = processed_img.get_fdata()
    
    # Show detailed stats before remapping
    unique_before = np.unique(processed_data)
    print(f"    Unique values before remapping: {unique_before}")
    
    # Check for floating point precision issues
    data_rounded = np.round(processed_data)
    unique_rounded = np.unique(data_rounded)
    
    if not np.array_equal(unique_before, unique_rounded):
        print(f"    ⚠️  Values changed after rounding: {unique_rounded}")
    
    remapped_data = remap_labels(processed_data, LABEL_MAPPING_AIRA)
    remapped_labels = np.unique(remapped_data)
    
    result['remapped_labels'] = remapped_labels.tolist()
    
    print(f"    Original labels: {original_labels}")
    print(f"    After processing: {unique_before}")
    print(f"    After remapping: {remapped_labels}")
    print(f"    Mapping applied: {LABEL_MAPPING_AIRA}")
    
    # 5. Show volume analysis
    voxel_vol, voxel_dims = get_voxel_volume(processed_img)
    print(f"\n  📊 Volume Analysis:")
    print(f"    Voxel dimensions: {voxel_dims[0]:.2f} × {voxel_dims[1]:.2f} × {voxel_dims[2]:.2f} mm")
    
    for label in remapped_labels:
        if label == 0:
            continue  # Skip background
        count = np.sum(remapped_data == label)
        volume_cm3 = (count * voxel_vol) / 1000.0
        
        kidney_name = "Left Kidney" if label == 1 else "Right Kidney" if label == 2 else f"Class {label}"
        print(f"    {kidney_name}: {count:,} voxels = {volume_cm3:.2f} cm³")
    
    # 6. Create processed NIfTI image
    # Save as int16 to preserve exact integer values
    processed_nifti = nib.Nifti1Image(
        remapped_data.astype(np.int16),  # Use int16 for clean integer labels
        processed_img.affine,
        processed_img.header
    )
    
    # Update header to reflect integer data type
    processed_nifti.set_data_dtype(np.int16)
    
    # Update header description
    description = f"Processed AIRA - Remapped + Reoriented - {datetime.now().strftime('%Y%m%d')}"
    processed_nifti.header['descrip'] = description.encode('ascii')[:79]
    
    # 7. Save processed mask
    # Generate output filename
    base_dir = os.path.dirname(aira_mask_path)
    original_filename = os.path.basename(aira_mask_path)
    name_without_ext = original_filename.replace('.nii.gz', '').replace('.nii', '')
    output_filename = f"{name_without_ext}{OUTPUT_SUFFIX}.nii"
    output_path = os.path.join(base_dir, output_filename)
    
    try:
        print(f"\n  💾 Saving processed mask: {output_filename}")
        nib.save(processed_nifti, output_path)
        
        file_size_mb = os.path.getsize(output_path) / (1024 * 1024)
        print(f"    ✓ Saved successfully ({file_size_mb:.2f} MB)")
        
        result['processed_path'] = output_path
        result['status'] = 'Success'
        
    except Exception as e:
        print(f"    ✗ Error saving file: {e}")
        result['error'] = f"Save failed: {e}"
        return result
    
    # 8. Create backup if requested
    if CREATE_BACKUP:
        backup_filename = f"{name_without_ext}_original_backup.nii"
        backup_path = os.path.join(base_dir, backup_filename)
        
        if not os.path.exists(backup_path):
            try:
                import shutil
                shutil.copy2(aira_mask_path, backup_path)
                print(f"  💾 Backup created: {backup_filename}")
            except Exception as e:
                print(f"  ⚠️  Backup failed: {e}")
    
    print(f"\n  ✅ Processing complete for {case_id}")
    
    return result

# ============================================================================
# MAIN PROCESSING
# ============================================================================

def process_all_new_aira_masks():
    """Process all new AIRA masks in the specified folder."""
    print("="*70)
    print("PROCESS NEW AIRA MASKS - COMPLETE PREPROCESSING PIPELINE")
    print("="*70)
    print(f"Input path: {NEW_AIRA_PATH}")
    print(f"Reference GT path: {GROUND_TRUTH_REFERENCE_PATH}")
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*70)
    
    # Find all cases
    print("\n🔍 Scanning for AIRA cases...")
    case_folders = find_aira_cases()
    
    if not case_folders:
        print("❌ No case folders found!")
        return
    
    print(f"✓ Found {len(case_folders)} case folders")
    
    # Process each case
    results = []
    successful = 0
    failed = 0
    
    for case_id, case_path in case_folders:
        # Find AIRA mask in this folder
        aira_mask_path = find_aira_mask_in_folder(case_path)
        
        if aira_mask_path is None:
            print(f"\n⚠️  {case_id}: No AIRA mask found in folder")
            results.append({
                'case_id': case_id,
                'status': 'Failed',
                'error': 'AIRA mask not found'
            })
            failed += 1
            continue
        
        # Find reference GT
        reference_gt_path = find_reference_gt(case_id)
        
        if reference_gt_path is None:
            print(f"\n⚠️  {case_id}: No reference GT found (will process without reorientation)")
        
        # Process the case
        result = process_single_case(case_id, aira_mask_path, reference_gt_path)
        results.append(result)
        
        if result['status'] == 'Success':
            successful += 1
        else:
            failed += 1
    
    # Summary
    print("\n" + "="*70)
    print("PROCESSING SUMMARY")
    print("="*70)
    print(f"Total cases: {len(case_folders)}")
    print(f"✓ Successful: {successful}")
    print(f"✗ Failed: {failed}")
    
    print(f"\nPreprocessing applied:")
    print(f"  • Spatial reorientation (when reference GT available)")
    print(f"  • Label remapping: {LABEL_MAPPING_AIRA}")
    print(f"  • Floating-point precision handling")
    
    print(f"\nOutput files saved with suffix: '{OUTPUT_SUFFIX}.nii'")
    if CREATE_BACKUP:
        print(f"Original files backed up with suffix: '_original_backup.nii'")
    
    # Detailed results table
    print("\n" + "="*70)
    print("DETAILED RESULTS")
    print("="*70)
    
    for result in results:
        print(f"\n{result['case_id']}:")
        print(f"  Status: {result['status']}")
        
        if result['status'] == 'Success':
            print(f"  Original orientation: {result['original_orientation']}")
            print(f"  Final orientation: {result['final_orientation']}")
            print(f"  Reorientation applied: {result['reorientation_applied']}")
            print(f"  Original labels: {result['original_labels']}")
            print(f"  Remapped labels: {result['remapped_labels']}")
            print(f"  Output: {os.path.basename(result['processed_path'])}")
        else:
            print(f"  Error: {result['error']}")
    
    print("\n" + "="*70)
    print("✅ PROCESSING COMPLETED")
    print("="*70)
    
    return results

# ============================================================================
# MAIN EXECUTION
# ============================================================================

if __name__ == "__main__":
    try:
        results = process_all_new_aira_masks()
        
        print("\n🎯 All preprocessing steps completed!")
        print("\nThe processed masks are now ready for FDA analysis with:")
        print("  ✓ Correct spatial orientation (matching ground truth)")
        print("  ✓ Correct label mapping (human reader convention)")
        print("  ✓ Robust floating-point handling")
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
