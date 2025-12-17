#!/usr/bin/env python3
"""
Hausdorff Distance Computation for FDA Trial 119
=================================================

This script computes Hausdorff distances (HD and HD95) between segmentation masks
for inter-observer agreement and AIRA model validation.

Hausdorff Distance measures the maximum surface distance between two masks:
- HD: Maximum distance from any point on one surface to nearest point on other surface
- HD95: 95th percentile (more robust to outliers)

Uses shared utilities from fda_utils.py and reuses file-finding logic from existing scripts.

Output:
-------
Single Excel file with 3 sheets:
  - Sheet 1: GT01 vs GT02 (inter-observer agreement)
  - Sheet 2: AIRA vs GT01
  - Sheet 3: AIRA vs GT02

Each sheet contains:
  - Left Kidney HD and HD95
  - Right Kidney HD and HD95
  - Summary statistics (mean, median, thresholds)

Usage:
    python compute_hausdorff_distances.py

Author: Medical AI Validation Team
Date: 2025-12-16
"""

import os
import sys
import re
import numpy as np
import nibabel as nib
import pandas as pd
from datetime import datetime
from scipy import ndimage
from scipy.spatial import distance
from fda_utils import extract_case_from_filename

# ============================================================================
# CONFIGURATION
# ============================================================================

# Ground Truth root directory
GT_ROOT_DIR = r'J:\FDA_GROUND_TRUTH_TRIAL_119\Aramis Truther Masks\Aramis Truther Masks'

# AIRA masks directory
AIRA_MASKS_DIR = r'K:\AIRA_FDA_Models\DATA\batch_storage\ARAMIS_RAS_LPI\ARAMIS_AIRA_Mask'

# Output directory
OUTPUT_DIR = r'D:\2024\zTest\FDA_TRIAL_119\results\hausdorff_distances'

# ============================================================================
# DEBUG MODE
# ============================================================================
MAX_CASES_TO_PROCESS = None  # Set to 5, 10 for testing, None for all
DEBUG_MODE = False

# Special case mappings for dual-labeled files
DUAL_LABEL_FALLBACKS = {
    'A-088': 'N-088',
    'A-089': 'N-089',
    'A-090': 'N-090',
    'A-092': 'N-092'
}

# ============================================================================
# HAUSDORFF DISTANCE FUNCTIONS
# ============================================================================

def load_nifti(file_path):
    """Load a NIfTI file and return the image object."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    return nib.load(file_path)

def get_orientation_string(img):
    """Get the orientation string for a NIfTI image."""
    ornt = nib.orientations.io_orientation(img.affine)
    return ''.join(nib.orientations.ornt2axcodes(ornt))

def reorient_to_match(reference_img, target_img):
    """Reorient target_img to match the orientation of reference_img."""
    target_ornt = nib.orientations.io_orientation(target_img.affine)
    ref_ornt = nib.orientations.io_orientation(reference_img.affine)
    ornt_transform = nib.orientations.ornt_transform(target_ornt, ref_ornt)
    reoriented_img = target_img.as_reoriented(ornt_transform)
    return reoriented_img

def surface_points_from_mask(mask):
    """
    Extract surface voxel coordinates from binary mask.
    Surface = mask & ~eroded(mask)
    
    Returns:
    --------
    coords : np.ndarray (N, 3)
        Surface voxel indices
    """
    if not np.any(mask):
        return np.array([]).reshape(0, 3)
    
    structure = ndimage.generate_binary_structure(3, 1)
    eroded = ndimage.binary_erosion(mask, structure=structure, iterations=1)
    boundary = mask & (~eroded)
    coords = np.argwhere(boundary)
    return coords

def voxel_indices_to_world(coords, zooms):
    """
    Convert voxel indices to physical coordinates (mm).
    
    Parameters:
    -----------
    coords : np.ndarray (N, 3)
        Voxel indices [i, j, k]
    zooms : np.ndarray (3,)
        Voxel spacing [z_spacing, y_spacing, x_spacing]
    
    Returns:
    --------
    world_coords : np.ndarray (N, 3)
        Physical coordinates in mm
    """
    if coords.size == 0:
        return coords
    return coords.astype(float) * zooms.reshape((1, 3))

def hausdorff_distance_from_pointsets(A_pts, B_pts):
    """
    Compute symmetric Hausdorff distance and HD95.
    
    Parameters:
    -----------
    A_pts : np.ndarray (N, 3)
        Surface points from mask A (in mm)
    B_pts : np.ndarray (M, 3)
        Surface points from mask B (in mm)
    
    Returns:
    --------
    hd : float
        Hausdorff distance (mm)
    hd95 : float
        95th percentile Hausdorff distance (mm)
    """
    if A_pts.size == 0 or B_pts.size == 0:
        return np.nan, np.nan
    
    # Compute distance matrix
    D = distance.cdist(A_pts, B_pts, metric='euclidean')
    
    # Directed distances
    minAtoB = D.min(axis=1)  # For each point in A, min distance to B
    minBtoA = D.min(axis=0)  # For each point in B, min distance to A
    
    # Hausdorff distance: max of max directed distances
    hd = max(minAtoB.max(), minBtoA.max())
    
    # HD95: 95th percentile (more robust to outliers)
    hd95 = max(np.percentile(minAtoB, 95), np.percentile(minBtoA, 95))
    
    return float(hd), float(hd95)

def compute_hausdorff_for_kidneys(mask1_data, mask2_data, zooms):
    """
    Compute Hausdorff distances for left and right kidneys separately.
    
    Parameters:
    -----------
    mask1_data : np.ndarray
        First mask (label 1=right, label 2=left)
    mask2_data : np.ndarray
        Second mask (label 1=right, label 2=left)
    zooms : np.ndarray (3,)
        Voxel spacing
    
    Returns:
    --------
    dict with keys: right_hd, right_hd95, left_hd, left_hd95, 
                    right_msg, left_msg
    """
    results = {
        'right_hd': np.nan,
        'right_hd95': np.nan,
        'right_msg': '',
        'left_hd': np.nan,
        'left_hd95': np.nan,
        'left_msg': ''
    }
    
    # Extract right kidney (label 1)
    right_mask1 = (mask1_data == 1).astype(bool)
    right_mask2 = (mask2_data == 1).astype(bool)
    
    # Extract left kidney (label 2)
    left_mask1 = (mask1_data == 2).astype(bool)
    left_mask2 = (mask2_data == 2).astype(bool)
    
    # Process right kidney
    if not np.any(right_mask1) and not np.any(right_mask2):
        results['right_msg'] = 'Both masks empty'
    elif not np.any(right_mask1):
        results['right_msg'] = 'Mask1 empty'
    elif not np.any(right_mask2):
        results['right_msg'] = 'Mask2 empty'
    else:
        # Get surface points
        right_pts1_idx = surface_points_from_mask(right_mask1)
        right_pts2_idx = surface_points_from_mask(right_mask2)
        
        if right_pts1_idx.size == 0:
            results['right_msg'] = 'Mask1 has no surface points'
        elif right_pts2_idx.size == 0:
            results['right_msg'] = 'Mask2 has no surface points'
        else:
            # Convert to world coordinates
            right_pts1_mm = voxel_indices_to_world(right_pts1_idx, zooms)
            right_pts2_mm = voxel_indices_to_world(right_pts2_idx, zooms)
            
            # Compute Hausdorff
            hd, hd95 = hausdorff_distance_from_pointsets(right_pts1_mm, right_pts2_mm)
            results['right_hd'] = hd
            results['right_hd95'] = hd95
    
    # Process left kidney
    if not np.any(left_mask1) and not np.any(left_mask2):
        results['left_msg'] = 'Both masks empty'
    elif not np.any(left_mask1):
        results['left_msg'] = 'Mask1 empty'
    elif not np.any(left_mask2):
        results['left_msg'] = 'Mask2 empty'
    else:
        # Get surface points
        left_pts1_idx = surface_points_from_mask(left_mask1)
        left_pts2_idx = surface_points_from_mask(left_mask2)
        
        if left_pts1_idx.size == 0:
            results['left_msg'] = 'Mask1 has no surface points'
        elif left_pts2_idx.size == 0:
            results['left_msg'] = 'Mask2 has no surface points'
        else:
            # Convert to world coordinates
            left_pts1_mm = voxel_indices_to_world(left_pts1_idx, zooms)
            left_pts2_mm = voxel_indices_to_world(left_pts2_idx, zooms)
            
            # Compute Hausdorff
            hd, hd95 = hausdorff_distance_from_pointsets(left_pts1_mm, left_pts2_mm)
            results['left_hd'] = hd
            results['left_hd95'] = hd95
    
    return results

# ============================================================================
# FILE FINDING FUNCTIONS (from existing scripts)
# ============================================================================

def find_case_folders(root_dir):
    """Find all case folders in the root directory."""
    if not os.path.exists(root_dir):
        print(f"❌ ERROR: Directory not found: {root_dir}")
        return []
    
    case_folders = []
    for item in os.listdir(root_dir):
        item_path = os.path.join(root_dir, item)
        if os.path.isdir(item_path):
            case_folders.append((item, item_path))
    
    return sorted(case_folders)

def find_gt_file(case_id, gt_root, gt_type='GT01'):
    """Find GT01 or GT02 file for a given case ID."""
    case_num = re.sub(r'[AN]-?', '', case_id, flags=re.IGNORECASE)
    
    possible_folders = [case_id, case_num, f"N-{case_num}", f"A-{case_num}"]
    
    for folder_name in possible_folders:
        case_folder = os.path.join(gt_root, folder_name)
        
        if not os.path.exists(case_folder):
            continue
        
        all_files = [f for f in os.listdir(case_folder) if f.lower().endswith('.nii')]
        gt_pattern = re.compile(rf'GT\s*0?{gt_type[-1]}(?:v\d+)?', re.IGNORECASE)
        
        gt_files = [os.path.join(case_folder, f) for f in all_files if gt_pattern.search(f)]
        
        if len(gt_files) == 1:
            return gt_files[0], None
        elif len(gt_files) > 1:
            return None, f"Multiple {gt_type} files found"
    
    return None, f"{gt_type} file not found"

def find_aira_files(aira_dir):
    """Find all AIRA mask files."""
    if not os.path.exists(aira_dir):
        return []
    
    aira_files = []
    for filename in os.listdir(aira_dir):
        if filename.startswith('AIRA_') and filename.endswith('.nii'):
            filepath = os.path.join(aira_dir, filename)
            aira_files.append((filename, filepath))
    
    return sorted(aira_files)

def extract_case_ids_from_aira(filename):
    """Extract case ID(s) from AIRA filename."""
    core = filename.replace('AIRA_', '').replace('.nii', '')
    parts = core.split('_')
    
    case_ids = []
    for part in parts:
        match = re.search(r'([AN]-\d+)', part, re.IGNORECASE)
        if match:
            case_ids.append(match.group(1).upper())
    
    return case_ids

def find_gt_files_with_fallback(aira_filename, gt_root):
    """Find GT files for AIRA case with fallback for dual-labeled cases."""
    case_ids = extract_case_ids_from_aira(aira_filename)
    
    # Try each case ID
    for case_id in case_ids:
        gt01_path, _ = find_gt_file(case_id, gt_root, 'GT01')
        gt02_path, _ = find_gt_file(case_id, gt_root, 'GT02')
        
        if gt01_path and gt02_path:
            return case_id, gt01_path, gt02_path, None
    
    # Try fallback
    primary_case_id = case_ids[0] if case_ids else None
    if primary_case_id in DUAL_LABEL_FALLBACKS:
        fallback_id = DUAL_LABEL_FALLBACKS[primary_case_id]
        gt01_path, _ = find_gt_file(fallback_id, gt_root, 'GT01')
        gt02_path, _ = find_gt_file(fallback_id, gt_root, 'GT02')
        
        if gt01_path and gt02_path:
            return fallback_id, gt01_path, gt02_path, None
    
    return case_ids[0] if case_ids else 'UNKNOWN', None, None, "GT files not found"

# ============================================================================
# PROCESSING FUNCTIONS
# ============================================================================

def process_gt01_vs_gt02(case_folders):
    """Process GT01 vs GT02 comparisons."""
    print("\n" + "="*80)
    print("PROCESSING: GT01 vs GT02")
    print("="*80 + "\n")
    
    rows = []
    
    for idx, (case_id, case_folder) in enumerate(case_folders, 1):
        print(f"[{idx}/{len(case_folders)}] Processing case: {case_id}")
        
        # Find GT files
        gt01_path, gt01_error = find_gt_file(case_id, GT_ROOT_DIR, 'GT01')
        gt02_path, gt02_error = find_gt_file(case_id, GT_ROOT_DIR, 'GT02')
        
        if gt01_error or gt02_error:
            error_msg = gt01_error or gt02_error
            print(f"  ⚠️  {error_msg}")
            rows.append({
                'Patient': case_id,
                'Mask1_File': '',
                'Mask2_File': '',
                'Organ': 'Right Kidney',
                'HD_mm': np.nan,
                'HD95_mm': np.nan,
                'Message': error_msg
            })
            rows.append({
                'Patient': case_id,
                'Mask1_File': '',
                'Mask2_File': '',
                'Organ': 'Left Kidney',
                'HD_mm': np.nan,
                'HD95_mm': np.nan,
                'Message': error_msg
            })
            continue
        
        try:
            # Load masks
            img1 = load_nifti(gt01_path)
            img2 = load_nifti(gt02_path)
            
            # Check orientation
            if get_orientation_string(img1) != get_orientation_string(img2):
                img2 = reorient_to_match(img1, img2)
            
            data1 = img1.get_fdata()
            data2 = img2.get_fdata()
            
            if data1.shape != data2.shape:
                error_msg = f"Shape mismatch: {data1.shape} vs {data2.shape}"
                print(f"  ❌ {error_msg}")
                rows.append({
                    'Patient': case_id,
                    'Mask1_File': os.path.basename(gt01_path),
                    'Mask2_File': os.path.basename(gt02_path),
                    'Organ': 'Right Kidney',
                    'HD_mm': np.nan,
                    'HD95_mm': np.nan,
                    'Message': error_msg
                })
                rows.append({
                    'Patient': case_id,
                    'Mask1_File': os.path.basename(gt01_path),
                    'Mask2_File': os.path.basename(gt02_path),
                    'Organ': 'Left Kidney',
                    'HD_mm': np.nan,
                    'HD95_mm': np.nan,
                    'Message': error_msg
                })
                continue
            
            # Get voxel spacing
            zooms = np.array(img1.header.get_zooms()[:3], dtype=float)
            
            # Compute Hausdorff distances
            results = compute_hausdorff_for_kidneys(data1, data2, zooms)
            
            # Add right kidney row
            rows.append({
                'Patient': case_id,
                'Mask1_File': os.path.basename(gt01_path),
                'Mask2_File': os.path.basename(gt02_path),
                'Organ': 'Right Kidney',
                'HD_mm': results['right_hd'],
                'HD95_mm': results['right_hd95'],
                'Message': results['right_msg']
            })
            
            # Add left kidney row
            rows.append({
                'Patient': case_id,
                'Mask1_File': os.path.basename(gt01_path),
                'Mask2_File': os.path.basename(gt02_path),
                'Organ': 'Left Kidney',
                'HD_mm': results['left_hd'],
                'HD95_mm': results['left_hd95'],
                'Message': results['left_msg']
            })
            
            print(f"  ✓ Right: HD={results['right_hd']:.2f}mm, HD95={results['right_hd95']:.2f}mm" if not np.isnan(results['right_hd']) else f"  ⚠️  Right: {results['right_msg']}")
            print(f"  ✓ Left: HD={results['left_hd']:.2f}mm, HD95={results['left_hd95']:.2f}mm" if not np.isnan(results['left_hd']) else f"  ⚠️  Left: {results['left_msg']}")
            
        except Exception as e:
            error_msg = f"ERROR: {str(e)}"
            print(f"  ❌ {error_msg}")
            rows.append({
                'Patient': case_id,
                'Mask1_File': os.path.basename(gt01_path) if gt01_path else '',
                'Mask2_File': os.path.basename(gt02_path) if gt02_path else '',
                'Organ': 'Right Kidney',
                'HD_mm': np.nan,
                'HD95_mm': np.nan,
                'Message': error_msg
            })
            rows.append({
                'Patient': case_id,
                'Mask1_File': os.path.basename(gt01_path) if gt01_path else '',
                'Mask2_File': os.path.basename(gt02_path) if gt02_path else '',
                'Organ': 'Left Kidney',
                'HD_mm': np.nan,
                'HD95_mm': np.nan,
                'Message': error_msg
            })
    
    return rows

def process_aira_vs_gt(aira_files, gt_type='GT01'):
    """Process AIRA vs GT01 or GT02 comparisons."""
    print("\n" + "="*80)
    print(f"PROCESSING: AIRA vs {gt_type}")
    print("="*80 + "\n")
    
    rows = []
    
    for idx, (aira_filename, aira_path) in enumerate(aira_files, 1):
        print(f"[{idx}/{len(aira_files)}] Processing: {aira_filename}")
        
        # Find GT files
        case_id, gt01_path, gt02_path, find_error = find_gt_files_with_fallback(aira_filename, GT_ROOT_DIR)
        gt_path = gt01_path if gt_type == 'GT01' else gt02_path
        
        if find_error or not gt_path:
            error_msg = find_error or f"{gt_type} file not found"
            print(f"  ⚠️  {error_msg}")
            rows.append({
                'Patient': case_id,
                'AIRA_File': aira_filename,
                'GT_File': '',
                'Organ': 'Right Kidney',
                'HD_mm': np.nan,
                'HD95_mm': np.nan,
                'Message': error_msg
            })
            rows.append({
                'Patient': case_id,
                'AIRA_File': aira_filename,
                'GT_File': '',
                'Organ': 'Left Kidney',
                'HD_mm': np.nan,
                'HD95_mm': np.nan,
                'Message': error_msg
            })
            continue
        
        try:
            # Load masks
            aira_img = load_nifti(aira_path)
            gt_img = load_nifti(gt_path)
            
            # Check orientation
            if get_orientation_string(aira_img) != get_orientation_string(gt_img):
                gt_img = reorient_to_match(aira_img, gt_img)
            
            aira_data = aira_img.get_fdata()
            gt_data = gt_img.get_fdata()
            
            if aira_data.shape != gt_data.shape:
                error_msg = f"Shape mismatch: AIRA {aira_data.shape} vs GT {gt_data.shape}"
                print(f"  ❌ {error_msg}")
                rows.append({
                    'Patient': case_id,
                    'AIRA_File': aira_filename,
                    'GT_File': os.path.basename(gt_path),
                    'Organ': 'Right Kidney',
                    'HD_mm': np.nan,
                    'HD95_mm': np.nan,
                    'Message': error_msg
                })
                rows.append({
                    'Patient': case_id,
                    'AIRA_File': aira_filename,
                    'GT_File': os.path.basename(gt_path),
                    'Organ': 'Left Kidney',
                    'HD_mm': np.nan,
                    'HD95_mm': np.nan,
                    'Message': error_msg
                })
                continue
            
            # Get voxel spacing
            zooms = np.array(aira_img.header.get_zooms()[:3], dtype=float)
            
            # Compute Hausdorff distances
            results = compute_hausdorff_for_kidneys(aira_data, gt_data, zooms)
            
            # Add right kidney row
            rows.append({
                'Patient': case_id,
                'AIRA_File': aira_filename,
                'GT_File': os.path.basename(gt_path),
                'Organ': 'Right Kidney',
                'HD_mm': results['right_hd'],
                'HD95_mm': results['right_hd95'],
                'Message': results['right_msg']
            })
            
            # Add left kidney row
            rows.append({
                'Patient': case_id,
                'AIRA_File': aira_filename,
                'GT_File': os.path.basename(gt_path),
                'Organ': 'Left Kidney',
                'HD_mm': results['left_hd'],
                'HD95_mm': results['left_hd95'],
                'Message': results['left_msg']
            })
            
            print(f"  ✓ Right: HD={results['right_hd']:.2f}mm, HD95={results['right_hd95']:.2f}mm" if not np.isnan(results['right_hd']) else f"  ⚠️  Right: {results['right_msg']}")
            print(f"  ✓ Left: HD={results['left_hd']:.2f}mm, HD95={results['left_hd95']:.2f}mm" if not np.isnan(results['left_hd']) else f"  ⚠️  Left: {results['left_msg']}")
            
        except Exception as e:
            error_msg = f"ERROR: {str(e)}"
            print(f"  ❌ {error_msg}")
            rows.append({
                'Patient': case_id,
                'AIRA_File': aira_filename,
                'GT_File': os.path.basename(gt_path) if gt_path else '',
                'Organ': 'Right Kidney',
                'HD_mm': np.nan,
                'HD95_mm': np.nan,
                'Message': error_msg
            })
            rows.append({
                'Patient': case_id,
                'AIRA_File': aira_filename,
                'GT_File': os.path.basename(gt_path) if gt_path else '',
                'Organ': 'Left Kidney',
                'HD_mm': np.nan,
                'HD95_mm': np.nan,
                'Message': error_msg
            })
    
    return rows

def add_statistics_sheet(writer, df_gt, df_aira_gt01, df_aira_gt02):
    """Add statistics summary sheet to Excel file."""
    stats_rows = []
    
    # Helper function to compute stats for a dataframe
    def compute_stats(df, comparison_name):
        stats = []
        
        for organ in ['Right Kidney', 'Left Kidney']:
            organ_df = df[df['Organ'] == organ]
            
            # HD statistics
            hd_values = pd.to_numeric(organ_df['HD_mm'], errors='coerce').dropna()
            hd95_values = pd.to_numeric(organ_df['HD95_mm'], errors='coerce').dropna()
            
            if len(hd_values) > 0:
                stats.append({
                    'Comparison': comparison_name,
                    'Organ': organ,
                    'Metric': 'HD (mm)',
                    'Count': len(hd_values),
                    'Mean': hd_values.mean(),
                    'Median': hd_values.median(),
                    'Std': hd_values.std(),
                    'Min': hd_values.min(),
                    'Max': hd_values.max(),
                    'HD>15mm': (hd_values > 15).sum(),
                    'HD>20mm': (hd_values > 20).sum(),
                    'HD>25mm': (hd_values > 25).sum()
                })
            
            if len(hd95_values) > 0:
                stats.append({
                    'Comparison': comparison_name,
                    'Organ': organ,
                    'Metric': 'HD95 (mm)',
                    'Count': len(hd95_values),
                    'Mean': hd95_values.mean(),
                    'Median': hd95_values.median(),
                    'Std': hd95_values.std(),
                    'Min': hd95_values.min(),
                    'Max': hd95_values.max(),
                    'HD95>15mm': (hd95_values > 15).sum(),
                    'HD95>20mm': (hd95_values > 20).sum(),
                    'HD95>25mm': (hd95_values > 25).sum()
                })
        
        return stats
    
    # Compute stats for each comparison
    stats_rows.extend(compute_stats(df_gt, 'GT01_vs_GT02'))
    stats_rows.extend(compute_stats(df_aira_gt01, 'AIRA_vs_GT01'))
    stats_rows.extend(compute_stats(df_aira_gt02, 'AIRA_vs_GT02'))
    
    # Create dataframe
    stats_df = pd.DataFrame(stats_rows)
    
    # Write to Excel
    stats_df.to_excel(writer, sheet_name='Statistics', index=False)
    
    # Add detailed case lists for high HD values
    add_high_hd_cases_sheet(writer, df_gt, df_aira_gt01, df_aira_gt02)

def add_high_hd_cases_sheet(writer, df_gt, df_aira_gt01, df_aira_gt02):
    """Add sheets listing specific cases with high Hausdorff distances (HD and HD95)."""
    
    # Helper function to extract high HD cases
    def extract_high_hd_cases(df, comparison_name, threshold=15.0):
        cases = []
        
        for _, row in df.iterrows():
            hd = pd.to_numeric(row.get('HD_mm'), errors='coerce')
            hd95 = pd.to_numeric(row.get('HD95_mm'), errors='coerce')
            
            if pd.notna(hd) and hd > threshold:
                cases.append({
                    'Comparison': comparison_name,
                    'Patient': row.get('Patient', ''),
                    'Organ': row.get('Organ', ''),
                    'HD_mm': hd,
                    'HD95_mm': hd95 if pd.notna(hd95) else np.nan,
                    'Severity': 'Very High (>25mm)' if hd > 25 else 'High (>20mm)' if hd > 20 else 'Moderate (>15mm)',
                    'File1': row.get('Mask1_File', row.get('AIRA_File', '')),
                    'File2': row.get('Mask2_File', row.get('GT_File', '')),
                    'Message': row.get('Message', '')
                })
        
        return cases
    
    # Helper function to extract high HD95 cases
    def extract_high_hd95_cases(df, comparison_name, threshold=10.0):
        cases = []
        
        for _, row in df.iterrows():
            hd = pd.to_numeric(row.get('HD_mm'), errors='coerce')
            hd95 = pd.to_numeric(row.get('HD95_mm'), errors='coerce')
            
            if pd.notna(hd95) and hd95 > threshold:
                cases.append({
                    'Comparison': comparison_name,
                    'Patient': row.get('Patient', ''),
                    'Organ': row.get('Organ', ''),
                    'HD_mm': hd if pd.notna(hd) else np.nan,
                    'HD95_mm': hd95,
                    'Severity': 'Very High (>15mm)' if hd95 > 15 else 'High (>12mm)' if hd95 > 12 else 'Moderate (>10mm)',
                    'File1': row.get('Mask1_File', row.get('AIRA_File', '')),
                    'File2': row.get('Mask2_File', row.get('GT_File', '')),
                    'Message': row.get('Message', '')
                })
        
        return cases
    
    # Extract HD cases (threshold: 15mm)
    hd_case_rows = []
    hd_case_rows.extend(extract_high_hd_cases(df_gt, 'GT01_vs_GT02', threshold=15.0))
    hd_case_rows.extend(extract_high_hd_cases(df_aira_gt01, 'AIRA_vs_GT01', threshold=15.0))
    hd_case_rows.extend(extract_high_hd_cases(df_aira_gt02, 'AIRA_vs_GT02', threshold=15.0))
    
    if hd_case_rows:
        # Sort by HD descending
        hd_case_rows = sorted(hd_case_rows, key=lambda x: x['HD_mm'], reverse=True)
        cases_df = pd.DataFrame(hd_case_rows)
        cases_df.to_excel(writer, sheet_name='High_HD_Cases', index=False)
    else:
        empty_df = pd.DataFrame([{'Message': 'No cases with HD > 15mm found'}])
        empty_df.to_excel(writer, sheet_name='High_HD_Cases', index=False)
    
    # Extract HD95 cases (threshold: 10mm)
    hd95_case_rows = []
    hd95_case_rows.extend(extract_high_hd95_cases(df_gt, 'GT01_vs_GT02', threshold=10.0))
    hd95_case_rows.extend(extract_high_hd95_cases(df_aira_gt01, 'AIRA_vs_GT01', threshold=10.0))
    hd95_case_rows.extend(extract_high_hd95_cases(df_aira_gt02, 'AIRA_vs_GT02', threshold=10.0))
    
    if hd95_case_rows:
        # Sort by HD95 descending
        hd95_case_rows = sorted(hd95_case_rows, key=lambda x: x['HD95_mm'], reverse=True)
        cases_hd95_df = pd.DataFrame(hd95_case_rows)
        cases_hd95_df.to_excel(writer, sheet_name='High_HD95_Cases', index=False)
    else:
        empty_df = pd.DataFrame([{'Message': 'No cases with HD95 > 10mm found'}])
        empty_df.to_excel(writer, sheet_name='High_HD95_Cases', index=False)

# ============================================================================
# MAIN FUNCTION
# ============================================================================

def main():
    """Main processing function."""
    print("=" * 80)
    print("HAUSDORFF DISTANCE COMPUTATION - FDA TRIAL 119")
    print("=" * 80)
    print(f"GT Directory: {GT_ROOT_DIR}")
    print(f"AIRA Directory: {AIRA_MASKS_DIR}")
    print(f"Output Directory: {OUTPUT_DIR}")
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    if MAX_CASES_TO_PROCESS is not None:
        print(f"\n⚠️  DEBUG MODE: Processing only {MAX_CASES_TO_PROCESS} cases")
    else:
        print(f"\n✓ Processing ALL cases")
    
    print("=" * 80)
    
    # Create output directory
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # Find case folders
    print("\n📂 Scanning for case folders...")
    case_folders = find_case_folders(GT_ROOT_DIR)
    aira_files = find_aira_files(AIRA_MASKS_DIR)
    
    if not case_folders:
        print("❌ No GT case folders found!")
        return
    
    if not aira_files:
        print("❌ No AIRA files found!")
        return
    
    print(f"✓ Found {len(case_folders)} GT case folders")
    print(f"✓ Found {len(aira_files)} AIRA mask files")
    
    # Limit if in debug mode
    if MAX_CASES_TO_PROCESS is not None:
        case_folders = case_folders[:MAX_CASES_TO_PROCESS]
        aira_files = aira_files[:MAX_CASES_TO_PROCESS]
        print(f"⚠️  Limited to {MAX_CASES_TO_PROCESS} cases")
    
    # Process each comparison type
    gt_rows = process_gt01_vs_gt02(case_folders)
    aira_gt01_rows = process_aira_vs_gt(aira_files, 'GT01')
    aira_gt02_rows = process_aira_vs_gt(aira_files, 'GT02')
    
    # Save results
    print("\n" + "="*80)
    print("SAVING RESULTS")
    print("="*80 + "\n")
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_filename = f"Hausdorff_Distances_{timestamp}.xlsx"
    output_path = os.path.join(OUTPUT_DIR, output_filename)
    
    with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
        # Sheet 1: GT01 vs GT02
        df_gt = pd.DataFrame(gt_rows)
        df_gt.to_excel(writer, sheet_name='GT01_vs_GT02', index=False)
        
        # Sheet 2: AIRA vs GT01
        df_aira_gt01 = pd.DataFrame(aira_gt01_rows)
        df_aira_gt01.to_excel(writer, sheet_name='AIRA_vs_GT01', index=False)
        
        # Sheet 3: AIRA vs GT02
        df_aira_gt02 = pd.DataFrame(aira_gt02_rows)
        df_aira_gt02.to_excel(writer, sheet_name='AIRA_vs_GT02', index=False)
        
        # Sheet 4: Statistics
        add_statistics_sheet(writer, df_gt, df_aira_gt01, df_aira_gt02)
    
    print(f"✓ Results saved to: {output_path}")
    print(f"\n  Sheet 1 (GT01_vs_GT02): {len(df_gt)} rows")
    print(f"  Sheet 2 (AIRA_vs_GT01): {len(df_aira_gt01)} rows")
    print(f"  Sheet 3 (AIRA_vs_GT02): {len(df_aira_gt02)} rows")
    print(f"  Sheet 4 (Statistics): Summary metrics")
    print(f"  Sheet 5 (High_HD_Cases): Cases with HD > 15mm (with patient IDs)")
    print(f"  Sheet 6 (High_HD95_Cases): Cases with HD95 > 10mm (with patient IDs)")
    
    print("\n" + "="*80)
    print("✅ HAUSDORFF DISTANCE COMPUTATION COMPLETE")
    print("="*80 + "\n")

if __name__ == "__main__":
    main()
