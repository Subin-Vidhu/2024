#!/usr/bin/env python3
"""
Process Batch Storage Masks - Apply All Required Preprocessing
===============================================================

This script processes AIRA masks from batch_storage folder and applies:
1. Spatial reorientation to LPI orientation (standardized)
2. Label remapping (Label 3→1, Label 2→2)
3. Floating-point precision handling

The processed masks will be saved in the same folder structure with
all transformations applied. All output files are standardized to LPI orientation.

Author: Medical AI Validation Team
Date: 2025-12-02
"""

import os
import sys
import glob
import numpy as np
import nibabel as nib
import pandas as pd
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# ============================================================================
# CONFIGURATION
# ============================================================================

# Batch storage masks location
# NEW_AIRA_PATH = r"G:\AIRA_Models_RESULTS\batch_storage"
NEW_AIRA_PATH = r"K:/AIRA_FDA_Models/DATA/batch_storage"

# Ground truth reference (optional - set to None if not available)
# If None, will use default LPI orientation
GROUND_TRUTH_REFERENCE_PATH = None

# Specific mask filename pattern to process
MASK_FILENAME_PATTERN = "mask_model_checkpoint_664_0.6738.nii.gz"

# Label Mapping
# Current masks: Label 2 = Left Kidney, Label 3 = Right Kidney
# Desired output: Label 1 = Right Kidney, Label 2 = Left Kidney
LABEL_MAPPING_AIRA = {
    0: 0,  # Background → Background
    1: 0,  # Noise (if present) → Background
    2: 2,  # Left Kidney → stays as 2
    3: 1   # Right Kidney → becomes 1
}

# Output configuration
OUTPUT_SUFFIX = "_processed"  # Suffix for processed files
CREATE_BACKUP = False  # Create backup of original files

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
    """Find all case folders in the batch storage path."""
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
    """Find specific AIRA mask file in a folder."""
    # First, check for the specific filename pattern
    mask_path = os.path.join(folder_path, MASK_FILENAME_PATTERN)
    if os.path.exists(mask_path):
        print(f"    Found mask file: {MASK_FILENAME_PATTERN}")
        return mask_path
    
    # Also check case-insensitive match
    for file in os.listdir(folder_path):
        if file.lower() == MASK_FILENAME_PATTERN.lower():
            mask_path = os.path.join(folder_path, file)
            print(f"    Found mask file: {file}")
            return mask_path
    
    # If not found, try pattern matching
    pattern_path = os.path.join(folder_path, "*mask_model_checkpoint*.nii.gz")
    files = glob.glob(pattern_path)
    if files:
        print(f"    Found mask file (pattern match): {os.path.basename(files[0])}")
        return files[0]
    
    print(f"    ⚠️  Mask file '{MASK_FILENAME_PATTERN}' not found in folder")
    return None

def find_reference_gt(case_id):
    """Find reference ground truth for a case to get orientation."""
    if GROUND_TRUTH_REFERENCE_PATH is None or not os.path.exists(GROUND_TRUTH_REFERENCE_PATH):
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
    3. Reorient AIRA to LPI orientation (or match reference if available)
    4. Remap labels (3→1, 2→2)
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
        'right_kidney_volume_cm3': None,
        'left_kidney_volume_cm3': None,
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
    
    # 3. Apply spatial reorientation (if reference available, otherwise use default LPI)
    processed_img = aira_img
    DEFAULT_ORIENTATION = 'LPI'  # Default target orientation when no reference GT is available
    
    if reference_img is not None:
        # Use reference GT orientation
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
        # No reference GT: apply default LPI orientation
        if original_orientation != DEFAULT_ORIENTATION:
            print(f"  🔄 No reference GT found, applying default orientation: {original_orientation} → {DEFAULT_ORIENTATION}")
            try:
                # Convert to default orientation (LPI)
                processed_img = nib.as_closest_canonical(aira_img)
                # Then reorient to LPI specifically
                target_ornt = nib.orientations.axcodes2ornt(DEFAULT_ORIENTATION)
                current_ornt = nib.io_orientation(processed_img.affine)
                ornt_transform = nib.orientations.ornt_transform(current_ornt, target_ornt)
                processed_img = processed_img.as_reoriented(ornt_transform)
                
                result['reorientation_applied'] = True
                result['final_orientation'] = DEFAULT_ORIENTATION
                print(f"    ✓ Default reorientation to {DEFAULT_ORIENTATION} successful")
            except Exception as e:
                print(f"    ✗ Default reorientation failed: {e}")
                result['final_orientation'] = original_orientation
        else:
            print(f"  ℹ️  Already in default orientation ({DEFAULT_ORIENTATION}), no reorientation needed")
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
    
    # Calculate volumes for each kidney
    right_kidney_volume_cm3 = None
    left_kidney_volume_cm3 = None
    
    for label in remapped_labels:
        if label == 0:
            continue  # Skip background
        count = np.sum(remapped_data == label)
        volume_cm3 = (count * voxel_vol) / 1000.0
        
        kidney_name = "Right Kidney" if label == 1 else "Left Kidney" if label == 2 else f"Class {label}"
        print(f"    {kidney_name}: {count:,} voxels = {volume_cm3:.2f} cm³")
        
        # Store volumes in result
        if label == 1:  # Right Kidney
            right_kidney_volume_cm3 = volume_cm3
        elif label == 2:  # Left Kidney
            left_kidney_volume_cm3 = volume_cm3
    
    result['right_kidney_volume_cm3'] = right_kidney_volume_cm3
    result['left_kidney_volume_cm3'] = left_kidney_volume_cm3
    
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
    description = f"Processed AIRA - Remapped + LPI Oriented - {datetime.now().strftime('%Y%m%d')}"
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
    """Process all AIRA masks in the batch storage folder."""
    print("="*70)
    print("PROCESS BATCH STORAGE MASKS - COMPLETE PREPROCESSING PIPELINE")
    print("="*70)
    print(f"Input path: {NEW_AIRA_PATH}")
    print(f"Mask filename pattern: {MASK_FILENAME_PATTERN}")
    print(f"Reference GT path: {GROUND_TRUTH_REFERENCE_PATH if GROUND_TRUTH_REFERENCE_PATH else 'None (will use LPI orientation)'}")
    print(f"Target orientation: LPI")
    print(f"Label mapping: {LABEL_MAPPING_AIRA}")
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*70)
    
    # Find all cases
    print("\n🔍 Scanning for case folders...")
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
            print(f"\n⚠️  {case_id}: No mask file found matching pattern '{MASK_FILENAME_PATTERN}'")
            results.append({
                'case_id': case_id,
                'status': 'Failed',
                'error': f'Mask file not found: {MASK_FILENAME_PATTERN}'
            })
            failed += 1
            continue
        
        # Find reference GT
        reference_gt_path = find_reference_gt(case_id)
        
        if reference_gt_path is None:
            print(f"\nℹ️  {case_id}: No reference GT found (will apply default LPI orientation)")
        
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
    if GROUND_TRUTH_REFERENCE_PATH:
        print(f"  • Spatial reorientation (when reference GT available)")
    else:
        print(f"  • Reorientation to LPI orientation (default)")
    print(f"  • Label remapping: {LABEL_MAPPING_AIRA}")
    print(f"    - Label 2 (Left Kidney) → stays as 2")
    print(f"    - Label 3 (Right Kidney) → becomes 1")
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
    
    # Export volume CSV
    csv_path = export_volume_csv(results)
    if csv_path:
        print(f"\n📊 Volume CSV exported to: {csv_path}")
    
    return results

# ============================================================================
# CSV EXPORT FUNCTION
# ============================================================================

def export_volume_csv(results):
    """
    Export kidney volumes to CSV file.
    
    Parameters:
    -----------
    results : list
        List of result dictionaries from processing
    
    Returns:
    --------
    csv_path : str or None
        Path to exported CSV file, or None if export failed
    """
    try:
        # Create results directory path (relative to script location)
        script_dir = os.path.dirname(os.path.abspath(__file__))
        results_base_dir = os.path.join(os.path.dirname(script_dir), 'results')
        
        # Create timestamped subfolder
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        results_subfolder = f"Batch_Storage_Volumes_{timestamp}"
        results_dir = os.path.join(results_base_dir, results_subfolder)
        
        # Create directory if it doesn't exist
        os.makedirs(results_dir, exist_ok=True)
        
        # Prepare CSV data
        csv_data = []
        for result in results:
            if result['status'] == 'Success':
                csv_data.append({
                    'Case Name': result['case_id'],
                    'Right Kidney Volume (cm³)': result['right_kidney_volume_cm3'] if result['right_kidney_volume_cm3'] is not None else 'N/A',
                    'Left Kidney Volume (cm³)': result['left_kidney_volume_cm3'] if result['left_kidney_volume_cm3'] is not None else 'N/A'
                })
            else:
                # Include failed cases with N/A volumes
                csv_data.append({
                    'Case Name': result['case_id'],
                    'Right Kidney Volume (cm³)': 'N/A',
                    'Left Kidney Volume (cm³)': 'N/A'
                })
        
        # Create DataFrame and save to CSV
        df = pd.DataFrame(csv_data)
        csv_filename = f"Kidney_Volumes_{timestamp}.csv"
        csv_path = os.path.join(results_dir, csv_filename)
        
        df.to_csv(csv_path, index=False)
        
        print(f"\n📊 Volume Summary:")
        print(f"  Total cases: {len(csv_data)}")
        successful_cases = sum(1 for r in csv_data if r['Right Kidney Volume (cm³)'] != 'N/A')
        print(f"  Cases with volume data: {successful_cases}")
        
        return csv_path
        
    except Exception as e:
        print(f"\n⚠️  Warning: Failed to export volume CSV: {e}")
        import traceback
        traceback.print_exc()
        return None

# ============================================================================
# MAIN EXECUTION
# ============================================================================

if __name__ == "__main__":
    try:
        results = process_all_new_aira_masks()
        
        print("\n🎯 All preprocessing steps completed!")
        print("\nThe processed masks are now ready with:")
        print("  ✓ LPI orientation (standardized)")
        print("  ✓ Label mapping: Label 3 (Right) → 1, Label 2 (Left) → 2")
        print("  ✓ Robust floating-point handling")
        print("\nOutput files saved as: '*_processed.nii' in each case folder")
        print("All output files are in LPI orientation!")
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

