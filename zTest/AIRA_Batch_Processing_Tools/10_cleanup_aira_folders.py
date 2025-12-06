#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Cleanup Script - Remove unnecessary files from AIRA case folders

This script removes all files except:
- aira_mask.nii (original AIRA mask)
- AIRA_{folder_name}.nii (processed/reoriented mask)

Useful for cleaning up intermediate processing files, backups, and duplicates.
"""

import os
import glob
from pathlib import Path

# ============================================================================
# USER CONFIGURATION - MODIFY THESE PARAMETERS
# ============================================================================

# Root folder containing case subfolders
# INPUT_FOLDER = r"K:/AIRA_FDA_Models/DATA/batch_storage"
INPUT_FOLDER = r"g:\ARAMIS_RENAL_FULL_DATASET_W_FDA_AND_UROKUL\ARAMIS_RENAL_FULL_DATASET"

# Search recursively in subfolders?
RECURSIVE_SEARCH = True

# Files to KEEP (all others will be deleted)
# Use patterns: exact filenames or wildcards
KEEP_PATTERNS = [
    "img.nii", "mask.nii"
]
# KEEP_PATTERNS = [
#     "aira_mask.nii",           # Original AIRA mask (exact match only)
#     "AIRA_*.nii",               # Processed/reoriented masks starting with AIRA_ (e.g., AIRA_A-089_N195_.nii)
#     "img.nii.gz",
#     "metadata.json",
#     "mask_model_checkpoint_664_0.6738.nii.gz"
# ]

# Dry run mode - if True, only shows what would be deleted without actually deleting
DRY_RUN = False  # Set to False to actually delete files

# ============================================================================
# PROCESSING FUNCTIONS
# ============================================================================

def should_keep_file(filename, keep_patterns):
    """
    Check if a file should be kept based on the keep patterns.
    Uses case-sensitive matching to ensure AIRA_*.nii doesn't match aira_*.nii
    
    Parameters:
    -----------
    filename : str
        The filename to check
    keep_patterns : list
        List of patterns to keep (can include wildcards)
    
    Returns:
    --------
    bool : True if file should be kept, False if it should be deleted
    """
    import re
    
    for pattern in keep_patterns:
        # Convert glob pattern to regex pattern (case-sensitive)
        # Replace * with .* and escape special regex characters
        regex_pattern = pattern.replace('.', '\\.').replace('*', '.*')
        regex_pattern = f'^{regex_pattern}$'  # Match entire filename
        
        if re.match(regex_pattern, filename):
            return True
    return False


def scan_folder(folder_path):
    """
    Scan a folder and identify files to keep vs delete.
    
    Parameters:
    -----------
    folder_path : str
        Path to the folder to scan
    
    Returns:
    --------
    dict : Dictionary with 'keep' and 'delete' file lists
    """
    result = {
        'folder': folder_path,
        'keep': [],
        'delete': []
    }
    
    try:
        files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
        
        for filename in files:
            full_path = os.path.join(folder_path, filename)
            
            if should_keep_file(filename, KEEP_PATTERNS):
                result['keep'].append(filename)
            else:
                result['delete'].append(filename)
    
    except Exception as e:
        print(f"  ⚠️  Error scanning {folder_path}: {e}")
    
    return result


def find_case_folders(root_folder, recursive):
    """
    Find all case folders to process.
    
    Parameters:
    -----------
    root_folder : str
        Root folder to search
    recursive : bool
        Search recursively
    
    Returns:
    --------
    list : List of folder paths
    """
    folders = []
    
    if recursive:
        # Find all subdirectories
        for dirpath, dirnames, filenames in os.walk(root_folder):
            # Check if this folder contains any .nii files
            nii_files = [f for f in filenames if f.endswith('.nii') or f.endswith('.nii.gz')]
            if nii_files:
                folders.append(dirpath)
    else:
        # Only check immediate subdirectories
        folders = [os.path.join(root_folder, d) for d in os.listdir(root_folder) 
                   if os.path.isdir(os.path.join(root_folder, d))]
    
    return sorted(folders)


def delete_files(file_list, dry_run=True):
    """
    Delete files from the list.
    
    Parameters:
    -----------
    file_list : list
        List of file paths to delete
    dry_run : bool
        If True, only simulate deletion
    
    Returns:
    --------
    dict : Statistics about deletion
    """
    stats = {
        'attempted': len(file_list),
        'success': 0,
        'failed': 0,
        'total_size': 0
    }
    
    for file_path in file_list:
        try:
            file_size = os.path.getsize(file_path)
            stats['total_size'] += file_size
            
            if not dry_run:
                os.remove(file_path)
                stats['success'] += 1
            else:
                stats['success'] += 1  # In dry run, count as success
                
        except Exception as e:
            print(f"    ❌ Failed to delete {os.path.basename(file_path)}: {e}")
            stats['failed'] += 1
    
    return stats


def format_size(size_bytes):
    """Format bytes to human-readable size."""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} TB"


# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    """Main execution function."""
    
    print("="*70)
    print("AIRA CASE FOLDER CLEANUP SCRIPT")
    print("="*70)
    
    # Validate input folder
    if not os.path.exists(INPUT_FOLDER):
        print(f"\n❌ ERROR: Input folder does not exist: {INPUT_FOLDER}")
        return
    
    print(f"\n📁 Root folder: {INPUT_FOLDER}")
    print(f"🔄 Recursive search: {RECURSIVE_SEARCH}")
    print(f"🛡️  Dry run mode: {DRY_RUN}")
    print(f"\n📋 Files to KEEP:")
    for pattern in KEEP_PATTERNS:
        print(f"  ✓ {pattern}")
    
    if DRY_RUN:
        print("\n⚠️  DRY RUN MODE - No files will be deleted (simulation only)")
    else:
        print("\n🔥 LIVE MODE - Files will be permanently deleted!")
        response = input("\nAre you sure you want to continue? (yes/no): ")
        if response.lower() != 'yes':
            print("❌ Operation cancelled")
            return
    
    # Find case folders
    print(f"\n🔍 Scanning for case folders...")
    folders = find_case_folders(INPUT_FOLDER, RECURSIVE_SEARCH)
    
    if not folders:
        print(f"\n⚠️  No folders found")
        return
    
    print(f"✓ Found {len(folders)} folder(s) to process\n")
    
    # Process each folder
    all_results = []
    total_keep = 0
    total_delete = 0
    total_size = 0
    
    for folder in folders:
        print(f"\n{'='*70}")
        print(f"Folder: {os.path.basename(folder)}")
        print(f"Path: {folder}")
        print(f"{'='*70}")
        
        result = scan_folder(folder)
        
        print(f"\n📊 Analysis:")
        print(f"  ✅ Files to KEEP: {len(result['keep'])}")
        for filename in result['keep']:
            file_path = os.path.join(folder, filename)
            file_size = os.path.getsize(file_path) if os.path.exists(file_path) else 0
            print(f"    • {filename} ({format_size(file_size)})")
        
        print(f"\n  🗑️  Files to DELETE: {len(result['delete'])}")
        delete_size = 0
        for filename in result['delete']:
            file_path = os.path.join(folder, filename)
            file_size = os.path.getsize(file_path) if os.path.exists(file_path) else 0
            delete_size += file_size
            print(f"    • {filename} ({format_size(file_size)})")
        
        if result['delete']:
            print(f"\n  💾 Space to be freed: {format_size(delete_size)}")
            
            # Delete files
            delete_paths = [os.path.join(folder, f) for f in result['delete']]
            stats = delete_files(delete_paths, DRY_RUN)
            
            if DRY_RUN:
                print(f"  ℹ️  Would delete {stats['success']} file(s)")
            else:
                print(f"  ✅ Deleted {stats['success']} file(s)")
                if stats['failed'] > 0:
                    print(f"  ⚠️  Failed to delete {stats['failed']} file(s)")
            
            total_delete += len(result['delete'])
            total_size += delete_size
        else:
            print(f"  ✓ No files to delete")
        
        total_keep += len(result['keep'])
        all_results.append(result)
    
    # Print summary
    print("\n" + "="*70)
    print("CLEANUP SUMMARY")
    print("="*70)
    
    print(f"\nFolders processed: {len(folders)}")
    print(f"Files to keep: {total_keep}")
    print(f"Files to delete: {total_delete}")
    print(f"Space to be freed: {format_size(total_size)}")
    
    if DRY_RUN:
        print("\n⚠️  DRY RUN COMPLETED - No files were actually deleted")
        print("💡 To actually delete files, set DRY_RUN = False in the script")
    else:
        print("\n✅ CLEANUP COMPLETED")
    
    print("="*70)


if __name__ == "__main__":
    main()
