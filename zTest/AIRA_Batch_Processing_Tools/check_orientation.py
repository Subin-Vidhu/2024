#!/usr/bin/env python3
"""
Check Orientation of NIfTI Files Across Multiple Folders (Recursive)
====================================================================

Now supports:
- Nested case folders (not just top-level)
- Both folder naming styles (e.g., N-071, A-089(N195))
- Automatic skipping of irrelevant folders

Author: Medical AI Validation Team
Date: 2025-10-30
"""

import os
import nibabel as nib
from pathlib import Path
from collections import Counter
import warnings
warnings.filterwarnings('ignore')

# ============================================================================
# CONFIGURATION
# ============================================================================

# ROOT_PATH = r"D:\__SHARED__\AIRA_FDA_SET_2_LIVE\AIRA_SET_2\LPI"
ROOT_PATH = r"G:\AIRA_Models_RESULTS\batch_storage"

FILES_TO_CHECK = [
    # "aira_mask_processed.nii",
    # "aira_mask.nii",  # Add more as needed
    "img.nii.gz"
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
    """
    Recursively find all folders that contain any of the target NIfTI files.
    Handles nested structures automatically.
    """
    case_folders = []

    for dirpath, dirnames, filenames in os.walk(root_path):
        if any(f in filenames for f in FILES_TO_CHECK):
            case_folders.append(dirpath)

    return sorted(case_folders)

def check_orientations(root_path, files_to_check):
    """Check orientations of specified files across all case folders."""
    print("=" * 80)
    print("ORIENTATION CHECK - NIfTI FILES (Recursive Search)")
    print("=" * 80)
    print(f"Root path: {root_path}")
    print(f"Files to check: {', '.join(files_to_check)}")
    print("=" * 80)

    case_folders = find_case_folders(root_path)
    print(f"\n🔍 Found {len(case_folders)} case folders with relevant NIfTI files\n")

    results = {filename: {} for filename in files_to_check}

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
        orientations = [info['orientation'] for info in file_results.values() if info['status'] == 'Success']
        orientation_counts = Counter(orientations)

        found_count = sum(1 for info in file_results.values() if info['status'] != 'File not found')
        success_count = sum(1 for info in file_results.values() if info['status'] == 'Success')

        print(f"\nStatistics:")
        print(f"  Total folders: {len(case_folders)}")
        print(f"  Files found: {found_count}")
        print(f"  Successfully loaded: {success_count}")
        print(f"  Missing: {len(case_folders) - found_count}")

        if orientation_counts:
            print(f"\nOrientation distribution:")
            for orientation, count in orientation_counts.most_common():
                percentage = (count / success_count) * 100 if success_count else 0
                print(f"  {orientation}: {count} files ({percentage:.1f}%)")

        print(f"\nDetailed results:")
        print(f"{'Case ID':<25} {'Orientation':<12} {'Shape':<20} {'Status':<30}")
        print("-" * 80)

        for case_name, info in sorted(file_results.items()):
            shape_str = str(info['shape']) if info['shape'] != 'N/A' else 'N/A'
            status_indicator = '✓' if info['status'] == 'Success' else ('○' if info['status'] == 'File not found' else '✗')
            print(f"{case_name:<25} {info['orientation']:<12} {shape_str:<20} {status_indicator} {info['status']}")

def print_summary(results):
    """Print overall summary."""
    print("\n" + "=" * 80)
    print("OVERALL SUMMARY")
    print("=" * 80)

    for filename, file_results in results.items():
        success_count = sum(1 for info in file_results.values() if info['status'] == 'Success')
        if success_count == 0:
            continue

        orientations = [info['orientation'] for info in file_results.values() if info['status'] == 'Success']
        orientation_counts = Counter(orientations)
        most_common = orientation_counts.most_common(1)[0]

        print(f"\n{filename}:")
        print(f"  Most common orientation: {most_common[0]} ({most_common[1]}/{success_count} files)")
        if len(orientation_counts) > 1:
            print(f"  ⚠️  WARNING: Multiple orientations detected!")
            for orientation, count in orientation_counts.items():
                print(f"    {orientation}: {count} files")
        else:
            print(f"  ✓ All files have consistent orientation")

# ============================================================================
# MAIN
# ============================================================================

def main():
    results, case_folders = check_orientations(ROOT_PATH, FILES_TO_CHECK)
    print_detailed_results(results, case_folders)
    print_summary(results)
    print("\n" + "=" * 80)
    print("✅ ORIENTATION CHECK COMPLETED")
    print("=" * 80)

if __name__ == "__main__":
    main()
