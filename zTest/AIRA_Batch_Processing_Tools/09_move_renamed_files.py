#!/usr/bin/env python3
"""
Move Renamed Files to Collection Folder
========================================
Moves all renamed AIRA files (AIRA_*.nii) from case folders to a single collection folder.
Files are MOVED (not copied) from their original locations.

Author: Medical AI Validation Team
Date: 2025-12-03
"""

import os
import shutil

# ============================================================================
# CONFIGURATION
# ============================================================================

root_dir = r"K:\AIRA_FDA_Models\DATA\batch_storage"
# output_dir = os.path.join(root_dir, "ARAMIS_RAS_LPI")
output_dir = os.path.join(root_dir, "ARAMIS_RAI_LPS")

# ============================================================================
# MAIN PROCESSING
# ============================================================================

# Create output directory if not exists
os.makedirs(output_dir, exist_ok=True)

moved_count = 0
missing_count = 0

print("="*70)
print("MOVE RENAMED FILES TO COLLECTION FOLDER")
print("="*70)
print(f"Source directory: {root_dir}")
print(f"Destination directory: {output_dir}")
print("="*70)
print()

for folder in os.listdir(root_dir):
    folder_path = os.path.join(root_dir, folder)

    # Skip non-directories
    if not os.path.isdir(folder_path):
        continue

    # Skip output folder itself
    if folder == "ARAMIS_RAS_LPI":
        continue
    if folder == "ARAMIS_RAI_LPS":
        continue
    
    # Construct expected filename: AIRA_<folder>.nii
    expected_file = f"AIRA_{folder}.nii"
    file_path = os.path.join(folder_path, expected_file)
    dest_path = os.path.join(output_dir, expected_file)

    if os.path.exists(file_path):
        try:
            print(f"Moving: {expected_file}")
            shutil.move(file_path, dest_path)
            print(f"  ✓ Moved to: {output_dir}")
            moved_count += 1
        except Exception as e:
            print(f"  ✗ Error moving {expected_file}: {e}")
    else:
        print(f"Missing: {expected_file} in {folder_path}")
        missing_count += 1

print()
print("="*70)
print("SUMMARY")
print("="*70)
print(f"Files moved: {moved_count}")
print(f"Files missing: {missing_count}")
print(f"Destination: {output_dir}")
print("="*70)
