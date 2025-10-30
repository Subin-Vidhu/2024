#!/usr/bin/env python3
"""
Simplified NIfTI Orientation Checker
------------------------------------
Scans subfolders, finds AIRA_*.nii (or fixed files), and prints one clean line
per case with orientation and shape info.
"""

import os
import nibabel as nib
from collections import Counter
import warnings
warnings.filterwarnings("ignore")

# ============================================================================
# CONFIGURATION
# ============================================================================

ROOT_PATH = r"D:\__SHARED__\AIRA_FDA_SET_2_LIVE\AIRA_SET_2\LPS"
FIXED_FILES = ["aira_mask_processed.nii"]
DYNAMIC_PREFIX = "AIRA_"

# ============================================================================
# FUNCTIONS
# ============================================================================

def get_orientation_string(img):
    try:
        return "".join(nib.orientations.aff2axcodes(img.affine))
    except Exception as e:
        return f"Error: {e}"

def get_image_info(file_path):
    try:
        img = nib.load(file_path)
        return (
            "".join(nib.orientations.aff2axcodes(img.affine)),
            str(img.shape),
            str(img.get_data_dtype()),
            "Success",
        )
    except Exception as e:
        return ("N/A", "N/A", "N/A", f"Error: {str(e)[:60]}")

def find_case_files(root_path):
    """Find subfolders containing .nii files with AIRA_ prefix or fixed names."""
    case_data = {}
    for dirpath, _, filenames in os.walk(root_path):
        if dirpath != root_path and "AIRA_SET_2" in os.path.basename(dirpath):
            continue

        nii_files = [f for f in filenames if f.lower().endswith(".nii")]
        selected_files = [f for f in nii_files if f in FIXED_FILES or f.startswith(DYNAMIC_PREFIX)]

        if selected_files:
            case_name = os.path.basename(dirpath)
            case_data[case_name] = {"path": dirpath, "files": selected_files}
    return case_data

# ============================================================================
# MAIN
# ============================================================================

def main():
    print("=" * 90)
    print(f"Scanning: {ROOT_PATH}")
    print("=" * 90)

    case_data = find_case_files(ROOT_PATH)
    print(f"Found {len(case_data)} case folders.\n")

    # Print table header
    print(f"{'Case':<20} {'File':<30} {'Orientation':<10} {'Shape':<20} {'Status'}")
    print("-" * 90)

    all_orientations = []

    for case_name, data in sorted(case_data.items()):
        for filename in sorted(data["files"]):
            file_path = os.path.join(data["path"], filename)
            orientation, shape, dtype, status = get_image_info(file_path)

            # Collect orientation for summary
            if status == "Success":
                all_orientations.append(orientation)

            print(f"{case_name:<20} {filename:<30} {orientation:<10} {shape:<20} {status}")

    # Summary
    print("\n" + "=" * 90)
    print("SUMMARY")
    print("=" * 90)
    if all_orientations:
        counts = Counter(all_orientations)
        for o, c in counts.items():
            print(f"{o}: {c} files")
        print(f"\nTotal successfully loaded: {len(all_orientations)}")
    else:
        print("No successful loads.")

    print("\n✅ Done!")

if __name__ == "__main__":
    main()
