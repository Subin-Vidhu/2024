#!/usr/bin/env python3
"""
Check Orientation of NIfTI Files in Nested Subfolders
======================================================

This script recursively scans nested subfolder structures and reports
the orientation of all NIfTI files found within each subfolder.

Useful for:
- Exploring deeply nested folder structures
- Finding all NIfTI files regardless of depth
- Analyzing orientation distribution across complex hierarchies

Author: Medical AI Validation Team
Date: 2025-10-29
"""

import os
import glob
import nibabel as nib
import pydicom
from pathlib import Path
from collections import Counter, defaultdict
import warnings
warnings.filterwarnings('ignore')

# ============================================================================
# CONFIGURATION
# ============================================================================

# Root folder to scan
ROOT_PATH = r"D:\__SHARED__\AIRA_FDA_SET_2_LIVE\Original_Images"

# File patterns to search for (can specify multiple)
FILE_PATTERNS = [
    "*.nii",
    "*.nii.gz",
    "*.dcm"  # DICOM files
]

# Display options
SHOW_DETAILED_FILES = True  # Show each file found (set False for DICOM to avoid spam)
SHOW_FOLDER_SUMMARY = True  # Show summary per subfolder
SHOW_OVERALL_STATS = True   # Show overall statistics
MAX_DISPLAY_DEPTH = None    # None = unlimited, or set to number (e.g., 3)
MAX_FILES_PER_FOLDER = 3    # Max files to display per folder (for DICOM)

# ============================================================================
# FUNCTIONS
# ============================================================================

def get_dicom_orientation(dcm):
    """
    Extract and interpret DICOM orientation from Image Orientation Patient tag.
    
    Returns a readable orientation string similar to NIfTI convention.
    """
    try:
        if not hasattr(dcm, 'ImageOrientationPatient'):
            return "No IOP"
        
        iop = dcm.ImageOrientationPatient
        
        # IOP contains 6 values: [row_x, row_y, row_z, col_x, col_y, col_z]
        # These are direction cosines for row and column directions
        
        # Get the primary direction for rows
        row_cosines = iop[:3]
        col_cosines = iop[3:]
        
        # Determine dominant axis for row direction
        row_abs = [abs(x) for x in row_cosines]
        row_max_idx = row_abs.index(max(row_abs))
        row_dir = ['R' if row_cosines[0] < 0 else 'L',
                   'A' if row_cosines[1] < 0 else 'P',
                   'F' if row_cosines[2] < 0 else 'H'][row_max_idx]
        
        # Determine dominant axis for column direction
        col_abs = [abs(x) for x in col_cosines]
        col_max_idx = col_abs.index(max(col_abs))
        col_dir = ['R' if col_cosines[0] < 0 else 'L',
                   'A' if col_cosines[1] < 0 else 'P',
                   'F' if col_cosines[2] < 0 else 'H'][col_max_idx]
        
        # The slice direction (through-plane) is perpendicular to row and column
        # We can determine it from cross product, but for simplicity:
        # If row and col are in x-y plane, slice is in z
        axes_used = {row_max_idx, col_max_idx}
        slice_idx = (set([0, 1, 2]) - axes_used).pop() if len(axes_used) == 2 else 2
        
        # Determine slice direction from Image Position Patient if available
        slice_dir = 'S'  # Default
        if hasattr(dcm, 'ImagePositionPatient'):
            # Use IOP to determine if it's I->S or S->I
            # This is simplified - actual calculation is more complex
            slice_dir = ['LR'[int(row_cosines[0] >= 0)],
                        'PA'[int(row_cosines[1] >= 0)],
                        'FH'[int(row_cosines[2] >= 0)]][slice_idx]
        
        # Return compact representation
        return f"{row_dir}{col_dir}{slice_dir}"
    
    except Exception as e:
        return "Error"

def get_orientation_string(img):
    """Get orientation string from NIfTI image."""
    try:
        orientation = nib.orientations.aff2axcodes(img.affine)
        return ''.join(orientation)
    except Exception as e:
        return f"Error"

def get_image_info(file_path):
    """Get detailed information about a NIfTI or DICOM image."""
    file_ext = os.path.splitext(file_path)[1].lower()
    
    try:
        if file_ext == '.dcm':
            # DICOM file
            dcm = pydicom.dcmread(file_path, stop_before_pixels=True)
            
            # Get orientation from Image Orientation Patient tag
            orientation_str = get_dicom_orientation(dcm)
            
            # Get Image Orientation Patient raw values for detailed info
            iop_raw = "N/A"
            if hasattr(dcm, 'ImageOrientationPatient'):
                iop = dcm.ImageOrientationPatient
                iop_raw = f"[{iop[0]:.2f}, {iop[1]:.2f}, {iop[2]:.2f}, {iop[3]:.2f}, {iop[4]:.2f}, {iop[5]:.2f}]"
            
            # Get basic info
            shape_str = f"({dcm.Rows}, {dcm.Columns})" if hasattr(dcm, 'Rows') else "N/A"
            dtype = "DICOM"
            
            return {
                'orientation': orientation_str,
                'iop_raw': iop_raw,
                'shape': shape_str,
                'dtype': dtype,
                'size_mb': os.path.getsize(file_path) / (1024 * 1024),
                'status': 'Success',
                'modality': dcm.Modality if hasattr(dcm, 'Modality') else 'Unknown'
            }
        else:
            # NIfTI file
            img = nib.load(file_path)
            orientation = get_orientation_string(img)
            shape = img.shape
            dtype = img.get_data_dtype()
            return {
                'orientation': orientation,
                'shape': shape,
                'dtype': str(dtype),
                'size_mb': os.path.getsize(file_path) / (1024 * 1024),
                'status': 'Success',
                'modality': 'NIfTI'
            }
    except Exception as e:
        return {
            'orientation': 'N/A',
            'shape': 'N/A',
            'dtype': 'N/A',
            'size_mb': 0,
            'status': f'Error: {str(e)[:50]}',
            'modality': 'Unknown'
        }

def get_relative_path(full_path, root_path):
    """Get path relative to root."""
    try:
        return os.path.relpath(full_path, root_path)
    except:
        return full_path

def get_folder_depth(folder_path, root_path):
    """Calculate folder depth relative to root."""
    rel_path = get_relative_path(folder_path, root_path)
    if rel_path == '.':
        return 0
    return len(Path(rel_path).parts)

def find_all_nifti_files(root_path, file_patterns):
    """
    Recursively find all NIfTI files in nested subfolders.
    
    Returns:
    --------
    dict: {folder_path: [list of nifti files in that folder]}
    """
    folder_files = defaultdict(list)
    
    print(f"\n🔍 Scanning: {root_path}")
    print(f"   Patterns: {', '.join(file_patterns)}")
    
    # Walk through all directories
    for root, dirs, files in os.walk(root_path):
        # Check each file pattern
        for pattern in file_patterns:
            # Use glob to match pattern in current directory
            search_pattern = os.path.join(root, pattern)
            matched_files = glob.glob(search_pattern)
            
            if matched_files:
                folder_files[root].extend(matched_files)
    
    return folder_files

def scan_and_analyze(root_path, file_patterns):
    """Main scanning and analysis function."""
    
    print("=" * 80)
    print("NESTED FOLDER ORIENTATION CHECK")
    print("=" * 80)
    print(f"Root path: {root_path}")
    print("=" * 80)
    
    # Find all files
    folder_files = find_all_nifti_files(root_path, file_patterns)
    
    if not folder_files:
        print("\n⚠️  No NIfTI files found in the specified directory!")
        print("\n" + "=" * 80)
        print("✅ SCAN COMPLETED (No files found)")
        print("=" * 80)
        return {}, Counter()
    
    total_folders = len(folder_files)
    total_files = sum(len(files) for files in folder_files.values())
    
    print(f"\n✓ Found {total_files} NIfTI files in {total_folders} subfolders")
    
    # Analyze each folder
    all_results = {}
    orientation_counts = Counter()
    
    for folder_path in sorted(folder_files.keys()):
        files = folder_files[folder_path]
        folder_name = os.path.basename(folder_path)
        rel_path = get_relative_path(folder_path, root_path)
        depth = get_folder_depth(folder_path, root_path)
        
        # Skip if depth exceeds max display depth
        if MAX_DISPLAY_DEPTH is not None and depth > MAX_DISPLAY_DEPTH:
            continue
        
        # Analyze each file in this folder
        folder_results = {}
        
        for file_path in files:
            file_name = os.path.basename(file_path)
            info = get_image_info(file_path)
            folder_results[file_name] = info
            
            # Count orientations
            if info['status'] == 'Success':
                orientation_counts[info['orientation']] += 1
        
        all_results[folder_path] = folder_results
        
        # Print detailed results for this folder
        if SHOW_DETAILED_FILES:
            print(f"\n{'─' * 80}")
            print(f"📁 Folder: {rel_path}")
            print(f"   Depth: {depth} | Files: {len(files)}")
            print(f"{'─' * 80}")
            
            displayed_count = 0
            for file_name, info in folder_results.items():
                if MAX_FILES_PER_FOLDER and displayed_count >= MAX_FILES_PER_FOLDER:
                    remaining = len(folder_results) - displayed_count
                    if remaining > 0:
                        print(f"  ... and {remaining} more files")
                    break
                
                if info['status'] == 'Success':
                    status_icon = '✓'
                    size_str = f"{info['size_mb']:.2f} MB"
                    shape_str = str(info['shape'])
                    modality = info.get('modality', 'Unknown')
                    iop_raw = info.get('iop_raw', '')
                    
                    print(f"  {status_icon} {file_name}")
                    print(f"     Modality: {modality:<8} | Orientation: {info['orientation']:<6} | "
                          f"Shape: {shape_str:<15}")
                    if iop_raw and iop_raw != 'N/A':
                        print(f"     Image Orientation Patient: {iop_raw}")
                else:
                    status_icon = '✗'
                    print(f"  {status_icon} {file_name}")
                    print(f"     Status: {info['status']}")
                
                displayed_count += 1
        
        # Print folder summary
        if SHOW_FOLDER_SUMMARY and not SHOW_DETAILED_FILES:
            folder_orientations = [info['orientation'] for info in folder_results.values() 
                                 if info['status'] == 'Success']
            folder_modalities = [info.get('modality', 'Unknown') for info in folder_results.values()
                                if info['status'] == 'Success']
            
            if folder_orientations:
                orientation_summary = Counter(folder_orientations)
                modality_summary = Counter(folder_modalities)
                
                orient_str = ', '.join([f"{o}({c})" for o, c in orientation_summary.items()])
                modality_str = ', '.join([f"{m}({c})" for m, c in modality_summary.items()])
                
                print(f"\n📁 {rel_path:<40} | Files: {len(files):<4} | {modality_str} | {orient_str}")
    
    # Print overall statistics
    if SHOW_OVERALL_STATS:
        print("\n" + "=" * 80)
        print("OVERALL STATISTICS")
        print("=" * 80)
        
        success_count = sum(1 for results in all_results.values() 
                          for info in results.values() 
                          if info['status'] == 'Success')
        error_count = total_files - success_count
        
        print(f"\nTotal subfolders scanned: {total_folders}")
        print(f"Total NIfTI files found: {total_files}")
        print(f"Successfully analyzed: {success_count}")
        if error_count > 0:
            print(f"Errors encountered: {error_count}")
        
        if orientation_counts:
            print(f"\nOrientation distribution:")
            for orientation, count in orientation_counts.most_common():
                percentage = (count / success_count) * 100
                bar_length = int(percentage / 2)
                bar = '█' * bar_length
                print(f"  {orientation:<6} : {count:>4} files ({percentage:>5.1f}%) {bar}")
        
        # Calculate total size
        total_size_mb = sum(info['size_mb'] for results in all_results.values() 
                          for info in results.values() 
                          if info['status'] == 'Success')
        total_size_gb = total_size_mb / 1024
        print(f"\nTotal size: {total_size_gb:.2f} GB ({total_size_mb:.1f} MB)")
    
    return all_results, orientation_counts

def print_tree_structure(root_path, folder_files):
    """Print a tree-like structure of folders and file counts."""
    print("\n" + "=" * 80)
    print("FOLDER TREE STRUCTURE")
    print("=" * 80)
    
    sorted_folders = sorted(folder_files.keys())
    
    for folder_path in sorted_folders:
        files = folder_files[folder_path]
        rel_path = get_relative_path(folder_path, root_path)
        depth = get_folder_depth(folder_path, root_path)
        
        if MAX_DISPLAY_DEPTH is not None and depth > MAX_DISPLAY_DEPTH:
            continue
        
        indent = "  " * depth
        folder_name = os.path.basename(folder_path) if depth > 0 else "ROOT"
        file_count = len(files)
        
        print(f"{indent}📁 {folder_name} ({file_count} file{'s' if file_count != 1 else ''})")

# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    """Main execution function."""
    
    # Check if root path exists
    if not os.path.exists(ROOT_PATH):
        print(f"❌ Error: Path does not exist: {ROOT_PATH}")
        return
    
    if not os.path.isdir(ROOT_PATH):
        print(f"❌ Error: Path is not a directory: {ROOT_PATH}")
        return
    
    # Scan and analyze
    results, orientation_counts = scan_and_analyze(ROOT_PATH, FILE_PATTERNS)
    
    # Print tree structure (optional)
    # Uncomment to enable:
    # folder_files = find_all_nifti_files(ROOT_PATH, FILE_PATTERNS)
    # print_tree_structure(ROOT_PATH, folder_files)
    
    print("\n" + "=" * 80)
    print("✅ SCAN COMPLETED")
    print("=" * 80)

if __name__ == "__main__":
    main()
