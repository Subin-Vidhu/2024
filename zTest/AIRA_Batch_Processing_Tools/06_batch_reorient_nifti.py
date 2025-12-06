#!/usr/bin/env python3
"""
Batch NIfTI Orientation Converter

This script reorients all NIfTI files in a specified folder to a target orientation.
- Files are saved with AIRA_ prefix using folder name
- Original files are preserved (no overwriting)
- Supports both .nii and .nii.gz formats
- Can search recursively through subfolders
- Saves files in int16 format for exact integer labels (important for segmentation masks)
- Generates a summary report
"""

import os
import glob
import nibabel as nib
import numpy as np
from pathlib import Path

# ============================================================================
# USER CONFIGURATION - MODIFY THESE PARAMETERS
# ============================================================================

# Input folder containing NIfTI files
# INPUT_FOLDER = r"d:\__SHARED__\AIRA_FDA_SET_2_LIVE"
# INPUT_FOLDER = r"K:\AIRA_FDA_Models\DATA\batch_storage"
INPUT_FOLDER = r"g:\ARAMIS_RENAL_FULL_DATASET_W_FDA_AND_UROKUL\ARAMIS_RENAL_FULL_DATASET"

# File pattern to match - looks for files with specific name pattern
# Examples: "aira_mask_processed.nii", "aira_mask_processed.nii.gz", "*_mask.nii", "case_*.nii"
# FILE_PATTERN = "aira_mask_processed.nii"
# FILE_PATTERN = "mask_model_checkpoint_664_0.6738_processed.nii"
# FILE_PATTERN = "img.nii" # img -> LAS, mask -> LPS
FILE_PATTERN = "mask.nii" # img -> LAS, mask -> LPS

# Target orientation (standard medical imaging orientations)
# Common options: "RAS", "LPI", "LPS", "RPI", "ASL", etc.
# R=Right, L=Left, A=Anterior, P=Posterior, S=Superior, I=Inferior
# TARGET_ORIENTATION = "LAS"
TARGET_ORIENTATION = "LPS"

# Search recursively in subfolders?
RECURSIVE_SEARCH = True  # Changed to True to search in subfolders like A-089(N195)/

# Skip files already in target orientation?
SKIP_IF_ALREADY_ORIENTED = True

# Suffix to add to reoriented files (before extension)
OUTPUT_SUFFIX = "_reoriented"

# Create backup of original files? (suffix: _backup)
CREATE_BACKUP = False

# ============================================================================
# PROCESSING FUNCTIONS
# ============================================================================

def get_orientation_string(img):
    """
    Get the orientation of a NIfTI image as a 3-letter string (e.g., 'RAS', 'LPI').
    
    Parameters:
    -----------
    img : nibabel image
        The NIfTI image
    
    Returns:
    --------
    orientation : str
        3-letter orientation code
    """
    try:
        axcodes = nib.aff2axcodes(img.affine)
        orientation = ''.join(axcodes)
        return orientation
    except Exception as e:
        print(f"    ⚠️  Could not determine orientation: {e}")
        return "UNKNOWN"


def reorient_to_target(source_img, target_orientation):
    """
    Reorient a NIfTI image to the target orientation.
    
    Parameters:
    -----------
    source_img : nibabel image
        The source NIfTI image to reorient
    target_orientation : str
        Target orientation code (e.g., 'LPI', 'RAS')
    
    Returns:
    --------
    reoriented_img : nibabel image
        The reoriented image, or original if reorientation fails
    success : bool
        Whether reorientation was successful
    """
    try:
        # Get current orientation
        current_orientation = get_orientation_string(source_img)
        
        # Check if already in target orientation
        if current_orientation == target_orientation:
            return source_img, True, "already_oriented"
        
        # Reorient the image
        reoriented_img = nib.as_closest_canonical(source_img)
        reoriented_img = nib.funcs.as_closest_canonical(source_img)
        
        # More precise reorientation
        current_ornt = nib.io_orientation(source_img.affine)
        target_ornt = nib.orientations.axcodes2ornt(target_orientation)
        transform = nib.orientations.ornt_transform(current_ornt, target_ornt)
        
        # Apply transformation
        reoriented_data = nib.orientations.apply_orientation(source_img.get_fdata(), transform)
        reoriented_affine = source_img.affine @ nib.orientations.inv_ornt_aff(transform, source_img.shape)
        
        # Convert to int16 for exact integer labels (important for segmentation masks)
        # Round first to handle any floating-point precision issues
        reoriented_data_int16 = np.round(reoriented_data).astype(np.int16)
        
        # Create new image with int16 data type
        reoriented_img = nib.Nifti1Image(reoriented_data_int16, reoriented_affine, source_img.header)
        
        # Set data type in header to int16
        reoriented_img.set_data_dtype(np.int16)
        
        # Verify the orientation
        final_orientation = get_orientation_string(reoriented_img)
        
        if final_orientation == target_orientation:
            return reoriented_img, True, "reoriented"
        else:
            print(f"    ⚠️  Expected {target_orientation}, got {final_orientation}")
            return reoriented_img, False, "orientation_mismatch"
            
    except Exception as e:
        print(f"    ❌ Reorientation failed: {e}")
        return source_img, False, "error"


def process_file(input_path, target_orientation, output_suffix, skip_if_oriented, create_backup):
    """
    Process a single NIfTI file.
    
    Parameters:
    -----------
    input_path : str
        Path to input NIfTI file
    target_orientation : str
        Target orientation
    output_suffix : str
        Suffix to add to output filename
    skip_if_oriented : bool
        Skip if already in target orientation
    create_backup : bool
        Create backup of original file
    
    Returns:
    --------
    result : dict
        Processing result information
    """
    result = {
        'file': os.path.basename(input_path),
        'path': input_path,
        'status': 'pending',
        'original_orientation': None,
        'final_orientation': None,
        'output_path': None,
        'message': ''
    }
    
    try:
        # Load the image
        img = nib.load(input_path)
        original_orientation = get_orientation_string(img)
        result['original_orientation'] = original_orientation
        
        print(f"\n{'='*70}")
        print(f"Processing: {os.path.basename(input_path)}")
        print(f"{'='*70}")
        print(f"  Current orientation: {original_orientation}")
        print(f"  Target orientation:  {target_orientation}")
        
        # Check if already oriented
        if skip_if_oriented and original_orientation == target_orientation:
            print(f"  ✓ Already in {target_orientation} orientation - SKIPPING")
            result['status'] = 'skipped'
            result['final_orientation'] = original_orientation
            result['message'] = 'Already in target orientation'
            return result
        
        # Reorient the image
        print(f"  🔄 Reorienting to {target_orientation}...")
        reoriented_img, success, status_msg = reorient_to_target(img, target_orientation)
        
        if not success and status_msg == "error":
            result['status'] = 'failed'
            result['message'] = 'Reorientation error'
            return result
        
        final_orientation = get_orientation_string(reoriented_img)
        result['final_orientation'] = final_orientation
        
        # Generate output path using parent folder name with AIRA_ prefix
        path_obj = Path(input_path)
        parent_folder_name = path_obj.parent.name  # Get the folder name (e.g., "A-089(N195)")
        
        # Clean the folder name: replace parentheses with underscores for safer filenames
        clean_folder_name = parent_folder_name.replace('(', '_').replace(')', '_')
        
        # Always save as .nii format with AIRA_ prefix
        # output_filename = f"AIRA_{clean_folder_name}.nii"
        # output_filename = f"AIRA_img_{clean_folder_name}.nii"
        output_filename = f"AIRA_mask_{clean_folder_name}.nii"
        output_path = path_obj.parent / output_filename
        result['output_path'] = str(output_path)
        
        # Create backup if requested
        if create_backup:
            backup_filename = f"AIRA_{clean_folder_name}_backup.nii"
            backup_path = path_obj.parent / backup_filename
            print(f"  📋 Creating backup: {backup_filename}")
            nib.save(img, backup_path)
        
        # Ensure data is int16 before saving (for segmentation masks)
        if reoriented_img.get_data_dtype() != np.int16:
            reoriented_data = reoriented_img.get_fdata()
            reoriented_data_int16 = np.round(reoriented_data).astype(np.int16)
            reoriented_img = nib.Nifti1Image(reoriented_data_int16, reoriented_img.affine, reoriented_img.header)
            reoriented_img.set_data_dtype(np.int16)
        
        # Save the reoriented image
        print(f"  💾 Saving to: {output_filename} (int16 format)")
        nib.save(reoriented_img, output_path)
        
        # Verify by reloading
        verify_img = nib.load(output_path)
        verify_orientation = get_orientation_string(verify_img)
        verify_dtype = verify_img.get_data_dtype()
        print(f"  📊 Data type: {verify_dtype}")
        
        if verify_orientation == target_orientation:
            print(f"  ✅ SUCCESS - Verified orientation: {verify_orientation}")
            result['status'] = 'success'
            result['message'] = f'Reoriented {original_orientation} → {verify_orientation}'
        else:
            print(f"  ⚠️  WARNING - Expected {target_orientation}, got {verify_orientation}")
            result['status'] = 'warning'
            result['message'] = f'Orientation mismatch: expected {target_orientation}, got {verify_orientation}'
        
    except Exception as e:
        print(f"  ❌ ERROR: {e}")
        result['status'] = 'failed'
        result['message'] = str(e)
    
    return result


def find_nifti_files(input_folder, file_pattern, recursive):
    """
    Find all NIfTI files matching the pattern.
    
    Parameters:
    -----------
    input_folder : str
        Root folder to search
    file_pattern : str
        File pattern (e.g., "*.nii")
    recursive : bool
        Search recursively
    
    Returns:
    --------
    file_list : list
        List of file paths
    """
    if recursive:
        # Recursive search
        pattern = os.path.join(input_folder, "**", file_pattern)
        files = glob.glob(pattern, recursive=True)
    else:
        # Non-recursive search
        pattern = os.path.join(input_folder, file_pattern)
        files = glob.glob(pattern)
    
    return sorted(files)


def print_summary(results):
    """
    Print processing summary.
    
    Parameters:
    -----------
    results : list
        List of result dictionaries
    """
    print("\n" + "="*70)
    print("PROCESSING SUMMARY")
    print("="*70)
    
    total = len(results)
    success = sum(1 for r in results if r['status'] == 'success')
    skipped = sum(1 for r in results if r['status'] == 'skipped')
    warning = sum(1 for r in results if r['status'] == 'warning')
    failed = sum(1 for r in results if r['status'] == 'failed')
    
    print(f"\nTotal files processed: {total}")
    print(f"  ✅ Success: {success}")
    print(f"  ⏭️  Skipped: {skipped}")
    print(f"  ⚠️  Warning: {warning}")
    print(f"  ❌ Failed: {failed}")
    
    # Detailed results
    if success > 0:
        print(f"\n✅ Successfully Reoriented ({success}):")
        for r in results:
            if r['status'] == 'success':
                print(f"  • {r['file']}: {r['original_orientation']} → {r['final_orientation']}")
    
    if skipped > 0:
        print(f"\n⏭️  Skipped (Already Oriented) ({skipped}):")
        for r in results:
            if r['status'] == 'skipped':
                print(f"  • {r['file']}: {r['original_orientation']}")
    
    if warning > 0:
        print(f"\n⚠️  Warnings ({warning}):")
        for r in results:
            if r['status'] == 'warning':
                print(f"  • {r['file']}: {r['message']}")
    
    if failed > 0:
        print(f"\n❌ Failed ({failed}):")
        for r in results:
            if r['status'] == 'failed':
                print(f"  • {r['file']}: {r['message']}")
    
    print("\n" + "="*70)


# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    """Main execution function."""
    
    print("="*70)
    print("BATCH NIFTI ORIENTATION CONVERTER")
    print("="*70)
    
    # Validate input folder
    if not os.path.exists(INPUT_FOLDER):
        print(f"\n❌ ERROR: Input folder does not exist: {INPUT_FOLDER}")
        return
    
    print(f"\n📁 Input folder: {INPUT_FOLDER}")
    print(f"🔍 File pattern: {FILE_PATTERN}")
    print(f"🎯 Target orientation: {TARGET_ORIENTATION}")
    print(f"🔄 Recursive search: {RECURSIVE_SEARCH}")
    print(f"⏭️  Skip if already oriented: {SKIP_IF_ALREADY_ORIENTED}")
    print(f"📝 Output suffix: {OUTPUT_SUFFIX}")
    print(f"💾 Create backup: {CREATE_BACKUP}")
    
    # Find files
    print(f"\n🔍 Searching for files...")
    files = find_nifti_files(INPUT_FOLDER, FILE_PATTERN, RECURSIVE_SEARCH)
    
    if not files:
        print(f"\n⚠️  No files found matching pattern: {FILE_PATTERN}")
        return
    
    print(f"✓ Found {len(files)} file(s)")
    
    # Process each file
    results = []
    for file_path in files:
        result = process_file(
            file_path, 
            TARGET_ORIENTATION, 
            OUTPUT_SUFFIX, 
            SKIP_IF_ALREADY_ORIENTED,
            CREATE_BACKUP
        )
        results.append(result)
    
    # Print summary
    print_summary(results)
    
    print("\n🎉 Processing complete!")


if __name__ == "__main__":
    main()
