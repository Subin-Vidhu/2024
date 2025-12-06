#!/usr/bin/env python3
"""
Batch Rename NIfTI Files Across Multiple Folders
=================================================

This script renames files in case folders using customizable naming patterns.
Supports folder-name-based renaming with prefix/suffix options.
Modified to delete existing target files before renaming.

Examples:
- AIRA_img_3591092024.nii → img.nii
- AIRA_mask_3591092024.nii → mask.nii

Author: Medical AI Validation Team
Date: 2025-10-29
"""

import os
import shutil
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# ============================================================================
# CONFIGURATION
# ============================================================================

# Root folder containing case subfolders
# ROOT_PATH = r"K:/AIRA_FDA_Models/DATA/batch_storage"
ROOT_PATH = r"g:\ARAMIS_RENAL_FULL_DATASET_W_FDA_AND_UROKUL\ARAMIS_RENAL_FULL_DATASET"

# File renaming configuration
RENAME_CONFIG = {
    # Source filename pattern → Target filename
    "AIRA_img_{folder_name}.nii": "img.nii",
    "AIRA_mask_{folder_name}.nii": "mask.nii"
    
    # Add more rename rules here:
    # "AIRA_{folder_name}.nii": "image.nii",
    # "some_file_{folder_name}.nii": "output.nii",
}

# Folder name cleaning options
CLEAN_FOLDER_NAME = False  # Set to False since we're using exact folder names
REPLACE_PARENTHESES = True  # Replace ( and ) with underscores
REMOVE_SPACES = True  # Replace spaces with underscores

# Safety options
DRY_RUN = False  # Set to False to actually rename files
CREATE_BACKUP = True  # Create backup before deleting/renaming
DELETE_EXISTING = True  # Delete existing target files before renaming
VERBOSE = True  # Show detailed output

# ============================================================================
# FUNCTIONS
# ============================================================================

def clean_folder_name(folder_name):
    """
    Clean folder name for use in filename.
    
    Examples:
    - "A-089(N195)" → "A-089_N195_"
    - "N-071" → "N-071"
    - "Some Folder Name" → "Some_Folder_Name"
    """
    cleaned = folder_name
    
    if REPLACE_PARENTHESES:
        cleaned = cleaned.replace('(', '_').replace(')', '_')
    
    if REMOVE_SPACES:
        cleaned = cleaned.replace(' ', '_')
    
    return cleaned

def generate_source_filename(pattern, folder_name):
    """
    Generate source filename from pattern using folder name.
    
    Supported placeholders:
    - {folder_name}: Folder name (cleaned if CLEAN_FOLDER_NAME=True)
    - {folder_name_original}: Original folder name (uncleaned)
    """
    if CLEAN_FOLDER_NAME:
        folder_name_cleaned = clean_folder_name(folder_name)
    else:
        folder_name_cleaned = folder_name
    
    # Replace placeholders
    source_filename = pattern.replace('{folder_name}', folder_name_cleaned)
    source_filename = source_filename.replace('{folder_name_original}', folder_name)
    
    return source_filename

def find_case_folders(root_path):
    """Find all case folders in the root path."""
    case_folders = []
    
    for item in os.listdir(root_path):
        item_path = os.path.join(root_path, item)
        if os.path.isdir(item_path):
            case_folders.append(item_path)
    
    return sorted(case_folders)

def rename_files_in_folder(folder_path, rename_config, dry_run=True):
    """
    Rename files in a single folder according to configuration.
    
    Returns:
    --------
    dict: Results of the renaming operation
    """
    folder_name = os.path.basename(folder_path)
    results = []
    
    for source_pattern, target_filename in rename_config.items():
        # Generate actual source filename using folder name
        source_filename = generate_source_filename(source_pattern, folder_name)
        source_path = os.path.join(folder_path, source_filename)
        target_path = os.path.join(folder_path, target_filename)
        
        # Check if source file exists
        if not os.path.exists(source_path):
            results.append({
                'source': source_filename,
                'target': target_filename,
                'status': 'not_found',
                'message': 'Source file not found'
            })
            continue
        
        # Check if source and target are the same
        if source_filename == target_filename:
            results.append({
                'source': source_filename,
                'target': target_filename,
                'status': 'skip',
                'message': 'Source and target are identical'
            })
            continue
        
        # Check if target already exists
        target_exists = os.path.exists(target_path)
        
        # Perform rename
        if not dry_run:
            try:
                # Backup source file if requested
                if CREATE_BACKUP:
                    backup_path = source_path + '.backup'
                    if os.path.exists(backup_path):
                        os.remove(backup_path)  # Remove old backup if exists
                    shutil.copy2(source_path, backup_path)
                
                # If target exists, backup and delete it first
                if target_exists and DELETE_EXISTING:
                    if CREATE_BACKUP:
                        target_backup_path = target_path + '.replaced_backup'
                        if os.path.exists(target_backup_path):
                            os.remove(target_backup_path)  # Remove old backup if exists
                        shutil.copy2(target_path, target_backup_path)
                    
                    # Delete existing target file
                    os.remove(target_path)
                    
                    # Now rename source to target
                    os.rename(source_path, target_path)
                    
                    results.append({
                        'source': source_filename,
                        'target': target_filename,
                        'status': 'replaced',
                        'message': 'Deleted existing target and renamed'
                    })
                elif target_exists and not DELETE_EXISTING:
                    results.append({
                        'source': source_filename,
                        'target': target_filename,
                        'status': 'conflict',
                        'message': 'Target exists (set DELETE_EXISTING=True to replace)'
                    })
                else:
                    # Target doesn't exist, just rename
                    os.rename(source_path, target_path)
                    
                    results.append({
                        'source': source_filename,
                        'target': target_filename,
                        'status': 'success',
                        'message': 'Renamed successfully'
                    })
                
            except Exception as e:
                results.append({
                    'source': source_filename,
                    'target': target_filename,
                    'status': 'error',
                    'message': f'Error: {str(e)}'
                })
        else:
            # Dry run - just report what would happen
            if target_exists and DELETE_EXISTING:
                results.append({
                    'source': source_filename,
                    'target': target_filename,
                    'status': 'would_replace',
                    'message': 'Would delete existing target and rename (dry run)'
                })
            elif target_exists and not DELETE_EXISTING:
                results.append({
                    'source': source_filename,
                    'target': target_filename,
                    'status': 'conflict',
                    'message': 'Target exists (set DELETE_EXISTING=True)'
                })
            else:
                results.append({
                    'source': source_filename,
                    'target': target_filename,
                    'status': 'would_rename',
                    'message': 'Would rename (dry run)'
                })
    
    return results

def print_results(case_name, results):
    """Print results for a single case."""
    if not VERBOSE:
        # Only print if there are actionable items
        actionable = [r for r in results if r['status'] in ['success', 'replaced', 'would_rename', 'would_replace', 'error', 'conflict']]
        if not actionable:
            return
    
    print(f"\n{'='*80}")
    print(f"Case: {case_name}")
    print(f"{'='*80}")
    
    for result in results:
        status = result['status']
        source = result['source']
        target = result['target'] if result['target'] else 'N/A'
        message = result['message']
        
        # Status indicators
        if status == 'success':
            indicator = '✓'
        elif status == 'replaced':
            indicator = '⟳'
        elif status == 'would_rename':
            indicator = '→'
        elif status == 'would_replace':
            indicator = '⟳'
        elif status == 'error':
            indicator = '✗'
        elif status == 'conflict':
            indicator = '⚠'
        elif status == 'skip':
            indicator = '○'
        elif status == 'not_found':
            indicator = '○'
        else:
            indicator = '?'
        
        if status in ['success', 'replaced', 'would_rename', 'would_replace']:
            print(f"  {indicator} {source:<45} → {target}")
            if status in ['replaced', 'would_replace']:
                print(f"     {'':45}   (deleting existing target first)")
        else:
            print(f"  {indicator} {source:<45} - {message}")

def print_summary(all_results):
    """Print overall summary."""
    print("\n" + "="*80)
    print("SUMMARY")
    print("="*80)
    
    # Count by status
    status_counts = {
        'success': 0,
        'replaced': 0,
        'would_rename': 0,
        'would_replace': 0,
        'error': 0,
        'conflict': 0,
        'skip': 0,
        'not_found': 0
    }
    
    for case_results in all_results.values():
        for result in case_results:
            status = result['status']
            if status in status_counts:
                status_counts[status] += 1
    
    total_cases = len(all_results)
    total_files = sum(len(results) for results in all_results.values())
    
    print(f"\nTotal cases processed: {total_cases}")
    print(f"Total rename operations: {total_files}")
    print(f"\nStatus breakdown:")
    
    if DRY_RUN:
        if status_counts['would_rename'] > 0:
            print(f"  → Would rename: {status_counts['would_rename']}")
        if status_counts['would_replace'] > 0:
            print(f"  ⟳ Would delete & replace: {status_counts['would_replace']}")
    else:
        if status_counts['success'] > 0:
            print(f"  ✓ Successfully renamed: {status_counts['success']}")
        if status_counts['replaced'] > 0:
            print(f"  ⟳ Deleted & replaced: {status_counts['replaced']}")
    
    if status_counts['error'] > 0:
        print(f"  ✗ Errors: {status_counts['error']}")
    if status_counts['conflict'] > 0:
        print(f"  ⚠ Conflicts (target exists): {status_counts['conflict']}")
    if status_counts['skip'] > 0:
        print(f"  ○ Skipped (same name): {status_counts['skip']}")
    if status_counts['not_found'] > 0:
        print(f"  ○ Not found: {status_counts['not_found']}")
    
    # Show what would happen
    if DRY_RUN:
        print(f"\n{'⚠'*40}")
        print("DRY RUN MODE - No files were actually renamed")
        print("Set DRY_RUN = False to perform actual renaming")
        print(f"{'⚠'*40}")
    else:
        print(f"\n✓ Files have been renamed")
        if CREATE_BACKUP:
            print(f"✓ Source backups: .backup extension")
            print(f"✓ Replaced file backups: .replaced_backup extension")

# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    """Main execution function."""
    
    print("="*80)
    print("BATCH FILE RENAMING TOOL")
    print("="*80)
    print(f"Root path: {ROOT_PATH}")
    print(f"Mode: {'DRY RUN' if DRY_RUN else 'LIVE RENAME'}")
    print(f"Backup: {'Enabled' if CREATE_BACKUP else 'Disabled'}")
    print(f"Delete Existing: {'Enabled' if DELETE_EXISTING else 'Disabled'}")
    print("="*80)
    
    print(f"\nRename rules:")
    for source, pattern in RENAME_CONFIG.items():
        print(f"  {source:<45} → {pattern}")
    
    print(f"\nFolder name cleaning:")
    print(f"  Clean folder name: {CLEAN_FOLDER_NAME}")
    print(f"  Replace parentheses: {REPLACE_PARENTHESES}")
    print(f"  Remove spaces: {REMOVE_SPACES}")
    
    # Find all case folders
    case_folders = find_case_folders(ROOT_PATH)
    print(f"\n🔍 Found {len(case_folders)} case folders")
    
    # Process each folder
    all_results = {}
    
    for folder_path in case_folders:
        case_name = os.path.basename(folder_path)
        results = rename_files_in_folder(folder_path, RENAME_CONFIG, dry_run=DRY_RUN)
        all_results[case_name] = results
        
        # Print results for this case
        print_results(case_name, results)
    
    # Print summary
    print_summary(all_results)
    
    print("\n" + "="*80)
    print("✅ BATCH RENAMING COMPLETED")
    print("="*80)

if __name__ == "__main__":
    main()