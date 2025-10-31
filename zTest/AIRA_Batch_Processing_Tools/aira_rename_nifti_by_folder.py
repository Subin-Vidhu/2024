#!/usr/bin/env python3
"""
AIRA NIfTI File Renamer
=======================
Scans subfolders and renames NIfTI files to match their folder name pattern:
    aira_{folder_name}.nii

Example:
    Folder: N-071
    File:   image1.nii  →  aira_N-071.nii

Author: Medical AI Validation Team
Date: 2025-10-30
"""

import os
import re
import shutil

# =====================================================================
# CONFIGURATION
# =====================================================================
ROOT_PATH = r"D:\__SHARED__\AIRA_FDA_SET_2_LIVE\AIRA_SET_2\LPI"
PREFIX = "AIRA_"     # all renamed files will start with this
DRY_RUN = False       # set True to preview without renaming

# =====================================================================
# FUNCTIONS
# =====================================================================

def is_nifti_file(filename):
    return filename.lower().endswith(".nii") or filename.lower().endswith(".nii.gz")

def already_named_correctly(filename, folder_name):
    """Check if file already follows the pattern aira_{folder_name}.nii"""
    base = os.path.basename(filename).lower()
    return re.match(rf"^{PREFIX.lower()}{re.escape(folder_name.lower())}", base) is not None

def rename_nifti_files(root_path):
    print("=" * 80)
    print(f"Scanning for NIfTI files under:\n{root_path}")
    print("=" * 80)

    renamed_count = 0
    skipped_count = 0

    for dirpath, _, filenames in os.walk(root_path):
        folder_name = os.path.basename(dirpath)
        nifti_files = [f for f in filenames if is_nifti_file(f)]

        for old_name in nifti_files:
            old_path = os.path.join(dirpath, old_name)
            ext = ".nii.gz" if old_name.lower().endswith(".nii.gz") else ".nii"
            new_name = f"{PREFIX}{folder_name}{ext}"
            new_path = os.path.join(dirpath, new_name)

            if already_named_correctly(old_name, folder_name):
                print(f"⏩ Skipping (already correct): {old_name}")
                skipped_count += 1
                continue

            if old_path == new_path:
                continue  # same path, nothing to do

            print(f"🔄 Renaming: {old_name} → {new_name}")
            if not DRY_RUN:
                shutil.move(old_path, new_path)
            renamed_count += 1

    print("\n" + "=" * 80)
    print(f"✅ Done! Renamed {renamed_count} file(s), skipped {skipped_count} already-correct file(s).")
    if DRY_RUN:
        print("💡 (Dry run only — no files actually renamed.)")
    print("=" * 80)

# =====================================================================
# MAIN
# =====================================================================

if __name__ == "__main__":
    rename_nifti_files(ROOT_PATH)
