#!/usr/bin/env python3
"""
Batch Rename NIfTI Files Across Multiple Folders
=================================================

This script renames files in case folders using customizable naming patterns.
Supports folder-name-based renaming with prefix/suffix options.

Examples:
- aira_mask_processed.nii → AIRA_N-071.nii
- aira_mask_processed.nii → AIRA_A-089_N195_.nii

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
ROOT_PATH = r"D:\__SHARED__\AIRA_FDA_SET_2_LIVE"

# File renaming configuration
RENAME_CONFIG = {
    # Source filename → Target naming pattern
    "aira_mask_processed.nii": "AIRA_{folder_name}.nii",
    
    # Add more rename rules here:
    # "aira_mask.nii": "AIRA_original_{folder_name}.nii",
    # "some_file.nii": "PREFIX_{folder_name}_SUFFIX.nii",
}

# Folder name cleaning options
CLEAN_FOLDER_NAME = True  # Clean folder name (remove/replace special chars)
REPLACE_PARENTHESES = True  # Replace ( and ) with underscores
REMOVE_SPACES = True  # Replace spaces with underscores

# Safety options
DRY_RUN = False  # Set to False to actually rename files
CREATE_BACKUP = True  # Create backup before renaming
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

def generate_new_filename(pattern, folder_name):
    """
    Generate new filename from pattern.
    
    Supported placeholders:
    - {folder_name}: Original folder name (cleaned if CLEAN_FOLDER_NAME=True)
    - {folder_name_original}: Original folder name (uncleaned)
    """
    if CLEAN_FOLDER_NAME:
        folder_name_cleaned = clean_folder_name(folder_name)
    else:
        folder_name_cleaned = folder_name
    
    # Replace placeholders
    new_filename = pattern.replace('{folder_name}', folder_name_cleaned)
    new_filename = new_filename.replace('{folder_name_original}', folder_name)
    
    return new_filename

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
    
    for source_filename, pattern in rename_config.items():
        source_path = os.path.join(folder_path, source_filename)
        
        # Check if source file exists
        if not os.path.exists(source_path):
            results.append({
                'source': source_filename,
                'target': None,
                'status': 'not_found',
                'message': 'Source file not found'
            })
            continue
        
        # Generate new filename
        new_filename = generate_new_filename(pattern, folder_name)
        target_path = os.path.join(folder_path, new_filename)
        
        # Check if target already exists
        if os.path.exists(target_path) and source_path != target_path:
            results.append({
                'source': source_filename,
                'target': new_filename,
                'status': 'conflict',
                'message': 'Target file already exists'
            })
            continue
        
        # Check if source and target are the same
        if source_filename == new_filename:
            results.append({
                'source': source_filename,
                'target': new_filename,
                'status': 'skip',
                'message': 'Source and target are identical'
            })
            continue
        
        # Perform rename
        if not dry_run:
            try:
                # Create backup if requested
                if CREATE_BACKUP:
                    backup_path = source_path + '.backup'
                    shutil.copy2(source_path, backup_path)
                
                # Rename file
                os.rename(source_path, target_path)
                
                results.append({
                    'source': source_filename,
                    'target': new_filename,
                    'status': 'success',
                    'message': 'Renamed successfully'
                })
            except Exception as e:
                results.append({
                    'source': source_filename,
                    'target': new_filename,
                    'status': 'error',
                    'message': f'Error: {str(e)}'
                })
        else:
            # Dry run - just report what would happen
            results.append({
                'source': source_filename,
                'target': new_filename,
                'status': 'would_rename',
                'message': 'Would rename (dry run)'
            })
    
    return results

def print_results(case_name, results):
    """Print results for a single case."""
    if not VERBOSE:
        # Only print if there are actionable items
        actionable = [r for r in results if r['status'] in ['success', 'would_rename', 'error', 'conflict']]
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
            color = ''
        elif status == 'would_rename':
            indicator = '→'
            color = ''
        elif status == 'error':
            indicator = '✗'
            color = ''
        elif status == 'conflict':
            indicator = '⚠'
            color = ''
        elif status == 'skip':
            indicator = '○'
            color = ''
        elif status == 'not_found':
            indicator = '○'
            color = ''
        else:
            indicator = '?'
            color = ''
        
        if status in ['success', 'would_rename']:
            print(f"  {indicator} {source:<35} → {target}")
        else:
            print(f"  {indicator} {source:<35} - {message}")

def print_summary(all_results):
    """Print overall summary."""
    print("\n" + "="*80)
    print("SUMMARY")
    print("="*80)
    
    # Count by status
    status_counts = {
        'success': 0,
        'would_rename': 0,
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
    else:
        if status_counts['success'] > 0:
            print(f"  ✓ Successfully renamed: {status_counts['success']}")
    
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
            print(f"✓ Backup files created with .backup extension")

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
    print("="*80)
    
    print(f"\nRename rules:")
    for source, pattern in RENAME_CONFIG.items():
        print(f"  {source:<35} → {pattern}")
    
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
