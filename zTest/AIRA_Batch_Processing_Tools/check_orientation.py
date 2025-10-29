#!/usr/bin/env python3
"""
Check Orientation of NIfTI Files Across Multiple Folders
=========================================================

This script scans all case folders and reports the orientation of specific
NIfTI files (e.g., aira_mask.nii, aira_mask_processed.nii).

Useful for:
- Verifying orientation consistency across dataset
- Comparing before/after preprocessing
- Quality control checks

Author: Medical AI Validation Team
Date: 2025-10-29
"""

import os
import glob
import nibabel as nib
from pathlib import Path
from collections import Counter
import warnings
warnings.filterwarnings('ignore')

# ============================================================================
# CONFIGURATION
# ============================================================================

# Root folder containing case subfolders
ROOT_PATH = r"D:\__SHARED__\AIRA_FDA_SET_2_LIVE"

# Files to check (can be modified)
FILES_TO_CHECK = [
    "aira_mask.nii",
    "aira_mask_processed.nii"
]

# ============================================================================
# FUNCTIONS
# ============================================================================

def get_orientation_string(img):
    """Get orientation string from NIfTI image."""
    try:
        orientation = nib.orientations.aff2axcodes(img.affine)
        return ''.join(orientation)
    except Exception as e:
        return f"Error: {e}"

def get_image_info(file_path):
    """Get detailed information about a NIfTI image."""
    try:
        img = nib.load(file_path)
        orientation = get_orientation_string(img)
        shape = img.shape
        dtype = img.get_data_dtype()
        return {
            'orientation': orientation,
            'shape': shape,
            'dtype': str(dtype),
            'status': 'Success'
        }
    except Exception as e:
        return {
            'orientation': 'N/A',
            'shape': 'N/A',
            'dtype': 'N/A',
            'status': f'Error: {str(e)[:50]}'
        }

def find_case_folders(root_path):
    """Find all case folders in the root path."""
    case_folders = []
    
    # Get all immediate subdirectories
    for item in os.listdir(root_path):
        item_path = os.path.join(root_path, item)
        if os.path.isdir(item_path):
            case_folders.append(item_path)
    
    return sorted(case_folders)

def check_orientations(root_path, files_to_check):
    """Check orientations of specified files across all case folders."""
    
    print("=" * 80)
    print("ORIENTATION CHECK - NIfTI FILES")
    print("=" * 80)
    print(f"Root path: {root_path}")
    print(f"Files to check: {', '.join(files_to_check)}")
    print("=" * 80)
    
    # Find all case folders
    case_folders = find_case_folders(root_path)
    print(f"\n🔍 Found {len(case_folders)} case folders\n")
    
    # Results storage
    results = {filename: {} for filename in files_to_check}
    
    # Check each case folder
    for case_folder in case_folders:
        case_name = os.path.basename(case_folder)
        
        for filename in files_to_check:
            file_path = os.path.join(case_folder, filename)
            
            if os.path.exists(file_path):
                info = get_image_info(file_path)
                results[filename][case_name] = info
            else:
                results[filename][case_name] = {
                    'orientation': 'N/A',
                    'shape': 'N/A',
                    'dtype': 'N/A',
                    'status': 'File not found'
                }
    
    return results, case_folders

def print_detailed_results(results, case_folders):
    """Print detailed results for each file type."""
    
    for filename in results.keys():
        print("\n" + "=" * 80)
        print(f"FILE: {filename}")
        print("=" * 80)
        
        file_results = results[filename]
        
        # Count statistics
        orientations = [info['orientation'] for info in file_results.values() 
                       if info['status'] == 'Success']
        orientation_counts = Counter(orientations)
        
        found_count = sum(1 for info in file_results.values() 
                         if info['status'] != 'File not found')
        success_count = sum(1 for info in file_results.values() 
                           if info['status'] == 'Success')
        
        print(f"\nStatistics:")
        print(f"  Total folders: {len(case_folders)}")
        print(f"  Files found: {found_count}")
        print(f"  Successfully loaded: {success_count}")
        print(f"  Missing: {len(case_folders) - found_count}")
        
        if orientation_counts:
            print(f"\nOrientation distribution:")
            for orientation, count in orientation_counts.most_common():
                percentage = (count / success_count) * 100
                print(f"  {orientation}: {count} files ({percentage:.1f}%)")
        
        print(f"\nDetailed results:")
        print(f"{'Case ID':<20} {'Orientation':<12} {'Shape':<20} {'Status':<30}")
        print("-" * 80)
        
        for case_name in sorted(file_results.keys()):
            info = file_results[case_name]
            shape_str = str(info['shape']) if info['shape'] != 'N/A' else 'N/A'
            status_str = info['status']
            
            # Color coding based on status
            if info['status'] == 'Success':
                status_indicator = '✓'
            elif info['status'] == 'File not found':
                status_indicator = '○'
            else:
                status_indicator = '✗'
            
            print(f"{case_name:<20} {info['orientation']:<12} {shape_str:<20} "
                  f"{status_indicator} {status_str}")

def print_comparison(results):
    """Print side-by-side comparison if multiple files are checked."""
    
    if len(results) < 2:
        return
    
    print("\n" + "=" * 80)
    print("SIDE-BY-SIDE COMPARISON")
    print("=" * 80)
    
    filenames = list(results.keys())
    file1, file2 = filenames[0], filenames[1]
    
    # Get all case names
    all_cases = sorted(set(results[file1].keys()) | set(results[file2].keys()))
    
    print(f"\n{'Case ID':<20} {file1:<30} {file2:<30}")
    print("-" * 80)
    
    mismatches = []
    
    for case_name in all_cases:
        info1 = results[file1].get(case_name, {'orientation': 'N/A', 'status': 'N/A'})
        info2 = results[file2].get(case_name, {'orientation': 'N/A', 'status': 'N/A'})
        
        orient1 = info1['orientation'] if info1['status'] == 'Success' else 'N/A'
        orient2 = info2['orientation'] if info2['status'] == 'Success' else 'N/A'
        
        # Check for mismatches
        if orient1 != 'N/A' and orient2 != 'N/A' and orient1 != orient2:
            indicator = '⚠️  CHANGED'
            mismatches.append(case_name)
        elif orient1 == orient2 and orient1 != 'N/A':
            indicator = '✓ Same'
        else:
            indicator = '○ N/A'
        
        print(f"{case_name:<20} {orient1:<30} {orient2:<30} {indicator}")
    
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    
    if mismatches:
        print(f"\n✓ Orientation changes detected in {len(mismatches)} cases:")
        for case in mismatches:
            info1 = results[file1][case]
            info2 = results[file2][case]
            print(f"  {case}: {info1['orientation']} → {info2['orientation']}")
    else:
        print("\n✓ All files have consistent orientations (no changes detected)")

def print_summary(results):
    """Print overall summary."""
    
    print("\n" + "=" * 80)
    print("OVERALL SUMMARY")
    print("=" * 80)
    
    for filename in results.keys():
        file_results = results[filename]
        
        success_count = sum(1 for info in file_results.values() 
                           if info['status'] == 'Success')
        
        if success_count > 0:
            orientations = [info['orientation'] for info in file_results.values() 
                           if info['status'] == 'Success']
            orientation_counts = Counter(orientations)
            most_common = orientation_counts.most_common(1)[0]
            
            print(f"\n{filename}:")
            print(f"  Most common orientation: {most_common[0]} "
                  f"({most_common[1]}/{success_count} files)")
            
            if len(orientation_counts) > 1:
                print(f"  ⚠️  WARNING: Multiple orientations detected!")
                for orientation, count in orientation_counts.items():
                    print(f"    {orientation}: {count} files")
            else:
                print(f"  ✓ All files have consistent orientation")

# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    """Main execution function."""
    
    # Check orientations
    results, case_folders = check_orientations(ROOT_PATH, FILES_TO_CHECK)
    
    # Print detailed results
    print_detailed_results(results, case_folders)
    
    # Print comparison if checking multiple files
    if len(FILES_TO_CHECK) > 1:
        print_comparison(results)
    
    # Print summary
    print_summary(results)
    
    print("\n" + "=" * 80)
    print("✅ ORIENTATION CHECK COMPLETED")
    print("=" * 80)

if __name__ == "__main__":
    main()
