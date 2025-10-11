# pip install nibabel numpy pandas openpyxl
import nibabel as nib
import numpy as np
import pandas as pd
import os
from datetime import datetime
import glob

# ============================================================================
# CONFIGURATION SECTION - Customize what to include in the output
# ============================================================================

CONFIG = {
    # Basic Information
    'include_case_info': True,          # Case ID, Status, Error messages
    'include_image_properties': False,  # Image shape, voxel dimensions
    'include_orientation_info': False,  # Orientation strings, reorientation status
    'include_label_info': False,        # Unique labels before/after remapping
    
    # Dice Scores
    'include_dice_scores': True,        # Individual class Dice scores
    'include_mean_dice': False,          # Mean Dice scores
    'include_background_dice': False,   # Background Dice score
    
    # Volumes - FDA (Ground Truth)
    'include_fda_volumes': True,        # FDA volumes for kidneys
    'include_fda_voxel_counts': False,  # FDA voxel counts
    'include_fda_background': False,    # FDA background volumes
    
    # Volumes - AIRA (Predicted)
    'include_aira_volumes': True,       # AIRA volumes for kidneys
    'include_aira_voxel_counts': False, # AIRA voxel counts
    'include_aira_background': False,   # AIRA background volumes
    
    # Volume Differences
    'include_volume_differences': True, # Absolute differences in cm³
    'include_volume_percentages': True, # Percentage differences
    
    # Spatial Analysis
    'include_spatial_metrics': False,    # Center distances, overlap voxels
    
    # Output Format
    'save_format': 'csv',              # 'xlsx' or 'csv' (xlsx recommended for multiple sheets)
    'create_summary_sheet': True,       # Create summary statistics sheet
    'create_failed_sheet': True,        # Create sheet for failed cases
}

# Label mapping configuration
LABEL_MAPPING = {
    0: 0,  # background
    1: 0,  # noise -> background
    2: 2,  # right kidney
    3: 1   # left kidney
}

# ============================================================================
# Core Functions
# ============================================================================

def load_nifti(file_path):
    """Load a NIfTI file and return the image object."""
    try:
        nifti_img = nib.load(file_path)
        return nifti_img
    except Exception as e:
        print(f"Error loading {file_path}: {e}")
        return None

def get_orientation_string(img):
    """Get the orientation string for a NIfTI image."""
    ornt = nib.orientations.io_orientation(img.affine)
    return ''.join(nib.orientations.ornt2axcodes(ornt))

def get_voxel_volume(img):
    """Calculate the volume of a single voxel in mm³."""
    voxel_dims = np.abs(img.header.get_zooms()[:3])
    voxel_volume = np.prod(voxel_dims)
    return voxel_volume, voxel_dims

def reorient_to_match(target_img, source_img):
    """Reorient source_img to match the orientation of target_img."""
    reoriented_data = source_img.as_reoriented(
        nib.orientations.ornt_transform(
            nib.orientations.io_orientation(source_img.affine),
            nib.orientations.io_orientation(target_img.affine)
        )
    )
    return reoriented_data

def remap_labels(data, label_mapping):
    """Remap labels in the data array according to the provided mapping."""
    remapped_data = np.zeros_like(data)
    for old_label, new_label in label_mapping.items():
        remapped_data[data == old_label] = new_label
    return remapped_data

def dice_coefficient(y_true, y_pred, epsilon=1e-6):
    """Compute the Dice coefficient between two numpy arrays."""
    intersection = np.sum(y_true * y_pred)
    union = np.sum(y_true) + np.sum(y_pred)
    if np.sum(y_true) == 0 and np.sum(y_pred) == 0:
        return 1.0
    return (2. * intersection + epsilon) / (union + epsilon)

def multi_class_dice(y_true, y_pred, num_classes):
    """Compute the Dice coefficient for each class."""
    dice_scores = []
    for c in range(num_classes):
        y_true_c = (y_true == c).astype(np.float32)
        y_pred_c = (y_pred == c).astype(np.float32)
        dice_score = dice_coefficient(y_true_c, y_pred_c)
        dice_scores.append(dice_score)
    return dice_scores

def get_unique_labels(data):
    """Get unique labels and their counts."""
    unique_labels = np.unique(data)
    label_counts = {int(label): int(np.sum(data == label)) for label in unique_labels}
    return label_counts

def check_spatial_alignment(y_true, y_pred, class_label):
    """Check spatial alignment and return metrics."""
    true_mask = (y_true == class_label).astype(np.uint8)
    pred_mask = (y_pred == class_label).astype(np.uint8)
    
    if np.sum(true_mask) == 0 or np.sum(pred_mask) == 0:
        return None
    
    true_coords = np.argwhere(true_mask)
    pred_coords = np.argwhere(pred_mask)
    
    true_center = true_coords.mean(axis=0)
    pred_center = pred_coords.mean(axis=0)
    
    distance = np.linalg.norm(true_center - pred_center)
    overlap_voxels = np.sum(true_mask * pred_mask)
    
    return {
        'center_distance': distance,
        'overlap_voxels': overlap_voxels
    }

def process_single_case(ground_truth_path, predicted_path, case_id, label_mapping, config):
    """Process a single case and return results based on configuration."""
    print(f"Processing {case_id}...", end=' ')
    
    results = {}
    
    # Always include basic info
    if config['include_case_info']:
        results['Case_ID'] = case_id
        results['Status'] = 'Failed'
    
    try:
        # Load images
        ground_truth_img = load_nifti(ground_truth_path)
        predicted_img = load_nifti(predicted_path)
        
        if ground_truth_img is None or predicted_img is None:
            if config['include_case_info']:
                results['Error_Message'] = 'Failed to load NIfTI files'
            print("✗ Failed to load")
            return results
        
        # Orientation info
        if config['include_orientation_info']:
            results['FDA_Orientation'] = get_orientation_string(ground_truth_img)
            results['AIRA_Orientation'] = get_orientation_string(predicted_img)
        
        # Reorient if needed
        if not np.allclose(ground_truth_img.affine, predicted_img.affine):
            predicted_img = reorient_to_match(ground_truth_img, predicted_img)
            if config['include_orientation_info']:
                results['Reoriented'] = 'Yes'
        else:
            if config['include_orientation_info']:
                results['Reoriented'] = 'No'
        
        # Get data arrays
        ground_truth = ground_truth_img.get_fdata()
        predicted = predicted_img.get_fdata()
        
        # Check shape match
        if ground_truth.shape != predicted.shape:
            if config['include_case_info']:
                results['Error_Message'] = f'Shape mismatch'
            print("✗ Shape mismatch")
            return results
        
        if config['include_image_properties']:
            results['Image_Shape'] = str(ground_truth.shape)
            voxel_volume_mm3, voxel_dims = get_voxel_volume(ground_truth_img)
            results['Voxel_Size_mm'] = f"{voxel_dims[0]:.2f}x{voxel_dims[1]:.2f}x{voxel_dims[2]:.2f}"
        else:
            voxel_volume_mm3, _ = get_voxel_volume(ground_truth_img)
        
        # Get original labels
        if config['include_label_info']:
            fda_labels = get_unique_labels(ground_truth)
            aira_labels_original = get_unique_labels(predicted)
            results['FDA_Labels'] = str(sorted(fda_labels.keys()))
            results['AIRA_Labels_Original'] = str(sorted(aira_labels_original.keys()))
        
        # Apply label mapping
        predicted = remap_labels(predicted, label_mapping)
        
        if config['include_label_info']:
            aira_labels_remapped = get_unique_labels(predicted)
            results['AIRA_Labels_Remapped'] = str(sorted(aira_labels_remapped.keys()))
        
        # Calculate Dice scores
        num_classes = 3
        class_names = ['Background', 'Left_Kidney', 'Right_Kidney']
        dice_scores = multi_class_dice(ground_truth, predicted, num_classes)
        
        if config['include_dice_scores']:
            if config['include_background_dice']:
                results['Dice_Background'] = round(dice_scores[0], 4)
            results['Dice_Left_Kidney'] = round(dice_scores[1], 4)
            results['Dice_Right_Kidney'] = round(dice_scores[2], 4)
        
        if config['include_mean_dice']:
            results['Mean_Dice_Kidneys'] = round(np.mean(dice_scores[1:]), 4)
        
        # Calculate volumes for each class
        for c in range(num_classes):
            class_name = class_names[c]
            
            # Skip background if not configured
            if c == 0 and not (config['include_fda_background'] or config['include_aira_background']):
                continue
            
            fda_count = np.sum(ground_truth == c)
            aira_count = np.sum(predicted == c)
            
            fda_volume_cm3 = (fda_count * voxel_volume_mm3) / 1000.0
            aira_volume_cm3 = (aira_count * voxel_volume_mm3) / 1000.0
            
            # FDA volumes
            if config['include_fda_volumes'] and (c > 0 or config['include_fda_background']):
                if config['include_fda_voxel_counts']:
                    results[f'FDA_{class_name}_Voxels'] = int(fda_count)
                results[f'FDA_{class_name}_Vol_cm3'] = round(fda_volume_cm3, 2)
            
            # AIRA volumes
            if config['include_aira_volumes'] and (c > 0 or config['include_aira_background']):
                if config['include_aira_voxel_counts']:
                    results[f'AIRA_{class_name}_Voxels'] = int(aira_count)
                results[f'AIRA_{class_name}_Vol_cm3'] = round(aira_volume_cm3, 2)
            
            # Volume differences (only for kidneys or if background is included)
            if c > 0 or config['include_fda_background']:
                if config['include_volume_differences']:
                    results[f'{class_name}_Diff_cm3'] = round(aira_volume_cm3 - fda_volume_cm3, 2)
                
                if config['include_volume_percentages'] and fda_volume_cm3 > 0:
                    rel_diff = ((aira_volume_cm3 - fda_volume_cm3) / fda_volume_cm3) * 100
                    results[f'{class_name}_Diff_%'] = round(rel_diff, 2)
        
        # Spatial alignment for kidneys
        if config['include_spatial_metrics']:
            for c, kidney_name in [(1, 'Left_Kidney'), (2, 'Right_Kidney')]:
                alignment = check_spatial_alignment(ground_truth, predicted, c)
                if alignment:
                    results[f'{kidney_name}_Center_Dist'] = round(alignment['center_distance'], 2)
                    results[f'{kidney_name}_Overlap'] = int(alignment['overlap_voxels'])
        
        if config['include_case_info']:
            results['Status'] = 'Success'
        print("✓")
        
    except Exception as e:
        if config['include_case_info']:
            results['Error_Message'] = str(e)
        print(f"✗ Error: {e}")
    
    return results

def find_case_files(base_dir):
    """Find all case folders and their ground truth and predicted files."""
    cases = []
    
    # Get all N-xxx folders
    case_folders = glob.glob(os.path.join(base_dir, 'N-*'))
    
    for case_folder in sorted(case_folders):
        case_id = os.path.basename(case_folder)
        
        # Look for ground truth file
        gt_patterns = [
            os.path.join(case_folder, case_id, f'{case_id}_MC.nii'),
            os.path.join(case_folder, case_id, f'{case_id}_MC.nii.gz'),
            os.path.join(case_folder, case_id, f'{case_id}_Updated_MC.nii'),
            os.path.join(case_folder, case_id, f'{case_id}_Updated_MC.nii.gz'),
            os.path.join(case_folder, f'{case_id}_MC.nii'),
            os.path.join(case_folder, f'{case_id}_MC.nii.gz'),
            os.path.join(case_folder, f'{case_id}_Updated_MC.nii'),
            os.path.join(case_folder, f'{case_id}_Updated_MC.nii.gz')
        ]
        
        ground_truth_path = None
        for pattern in gt_patterns:
            if os.path.exists(pattern):
                ground_truth_path = pattern
                break
        
        # Look for predicted file
        pred_patterns = [
            os.path.join(case_folder, 'mask.nii'),
            os.path.join(case_folder, 'mask.nii.gz')
        ]
        
        predicted_path = None
        for pattern in pred_patterns:
            if os.path.exists(pattern):
                predicted_path = pattern
                break
        
        if ground_truth_path and predicted_path:
            cases.append({
                'case_id': case_id,
                'ground_truth': ground_truth_path,
                'predicted': predicted_path
            })
    
    return cases

def main():
    # Base directory containing all case folders
    base_dir = r'c:\Users\Subin-PC\Downloads\Telegram Desktop\OneDrive_1_10-8-2025'
    
    # Output file in current working directory
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_file = f'FDA_AIRA_Results_{timestamp}.{CONFIG["save_format"]}'
    
    print("="*70)
    print("FDA vs AIRA - Multi-Case Analysis")
    print("="*70)
    print(f"Dataset directory: {base_dir}")
    print(f"Output file: {output_file}")
    print(f"Label mapping: {LABEL_MAPPING}")
    print("="*70)
    
    # Find all cases
    print("\nSearching for cases...")
    cases = find_case_files(base_dir)
    print(f"Found {len(cases)} cases\n")
    
    if len(cases) == 0:
        print("No cases found. Please check the directory structure.")
        return
    
    # Process all cases
    all_results = []
    for case_info in cases:
        result = process_single_case(
            case_info['ground_truth'],
            case_info['predicted'],
            case_info['case_id'],
            LABEL_MAPPING,
            CONFIG
        )
        all_results.append(result)
    
    # Create DataFrame
    df = pd.DataFrame(all_results)
    
    # Save based on format
    if CONFIG['save_format'] == 'csv':
        df.to_csv(output_file, index=False)
        print(f"\n✓ Results saved to: {output_file}")
    
    else:  # xlsx
        with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
            # Main results sheet
            df.to_excel(writer, sheet_name='Results', index=False)
            
            # Summary statistics sheet
            if CONFIG['create_summary_sheet']:
                successful_cases = df[df['Status'] == 'Success'] if 'Status' in df.columns else df
                if len(successful_cases) > 0:
                    summary_data = []
                    summary_data.append(['Metric', 'Value'])
                    summary_data.append(['Total Cases', len(df)])
                    if 'Status' in df.columns:
                        summary_data.append(['Successful Cases', len(successful_cases)])
                        summary_data.append(['Failed Cases', len(df[df['Status'] == 'Failed'])])
                    summary_data.append(['', ''])
                    
                    if 'Mean_Dice_Kidneys' in successful_cases.columns:
                        summary_data.append(['Mean Dice (Kidneys)', round(successful_cases['Mean_Dice_Kidneys'].mean(), 4)])
                    if 'Dice_Left_Kidney' in successful_cases.columns:
                        summary_data.append(['Mean Dice - Left Kidney', round(successful_cases['Dice_Left_Kidney'].mean(), 4)])
                    if 'Dice_Right_Kidney' in successful_cases.columns:
                        summary_data.append(['Mean Dice - Right Kidney', round(successful_cases['Dice_Right_Kidney'].mean(), 4)])
                    
                    if 'FDA_Left_Kidney_Vol_cm3' in successful_cases.columns:
                        summary_data.append(['', ''])
                        summary_data.append(['Mean FDA Left Kidney (cm³)', round(successful_cases['FDA_Left_Kidney_Vol_cm3'].mean(), 2)])
                        summary_data.append(['Mean AIRA Left Kidney (cm³)', round(successful_cases['AIRA_Left_Kidney_Vol_cm3'].mean(), 2)])
                        if 'Left_Kidney_Diff_cm3' in successful_cases.columns:
                            summary_data.append(['Mean Left Kidney Diff (cm³)', round(successful_cases['Left_Kidney_Diff_cm3'].mean(), 2)])
                        if 'Left_Kidney_Diff_%' in successful_cases.columns:
                            summary_data.append(['Mean Left Kidney Diff (%)', round(successful_cases['Left_Kidney_Diff_%'].mean(), 2)])
                    
                    if 'FDA_Right_Kidney_Vol_cm3' in successful_cases.columns:
                        summary_data.append(['', ''])
                        summary_data.append(['Mean FDA Right Kidney (cm³)', round(successful_cases['FDA_Right_Kidney_Vol_cm3'].mean(), 2)])
                        summary_data.append(['Mean AIRA Right Kidney (cm³)', round(successful_cases['AIRA_Right_Kidney_Vol_cm3'].mean(), 2)])
                        if 'Right_Kidney_Diff_cm3' in successful_cases.columns:
                            summary_data.append(['Mean Right Kidney Diff (cm³)', round(successful_cases['Right_Kidney_Diff_cm3'].mean(), 2)])
                        if 'Right_Kidney_Diff_%' in successful_cases.columns:
                            summary_data.append(['Mean Right Kidney Diff (%)', round(successful_cases['Right_Kidney_Diff_%'].mean(), 2)])
                    
                    summary_df = pd.DataFrame(summary_data[1:], columns=summary_data[0])
                    summary_df.to_excel(writer, sheet_name='Summary', index=False)
            
            # Failed cases sheet (if any)
            if CONFIG['create_failed_sheet'] and 'Status' in df.columns:
                failed_cases = df[df['Status'] == 'Failed']
                if len(failed_cases) > 0:
                    failed_cases.to_excel(writer, sheet_name='Failed_Cases', index=False)
        
        print(f"\n✓ Results saved to: {output_file}")
    
    # Print summary
    print("\n" + "="*70)
    print("SUMMARY")
    print("="*70)
    successful_cases = df[df['Status'] == 'Success'] if 'Status' in df.columns else df
    print(f"Total cases: {len(df)}")
    if 'Status' in df.columns:
        print(f"Successful: {len(successful_cases)}")
        print(f"Failed: {len(df[df['Status'] == 'Failed'])}")
    
    if len(successful_cases) > 0:
        if 'Mean_Dice_Kidneys' in successful_cases.columns:
            print(f"\nMean Dice (Kidneys): {successful_cases['Mean_Dice_Kidneys'].mean():.4f}")
        if 'Left_Kidney_Diff_cm3' in successful_cases.columns:
            print(f"Mean Left Kidney Diff: {successful_cases['Left_Kidney_Diff_cm3'].mean():.2f} cm³", end='')
            if 'Left_Kidney_Diff_%' in successful_cases.columns:
                print(f" ({successful_cases['Left_Kidney_Diff_%'].mean():.2f}%)")
            else:
                print()
        if 'Right_Kidney_Diff_cm3' in successful_cases.columns:
            print(f"Mean Right Kidney Diff: {successful_cases['Right_Kidney_Diff_cm3'].mean():.2f} cm³", end='')
            if 'Right_Kidney_Diff_%' in successful_cases.columns:
                print(f" ({successful_cases['Right_Kidney_Diff_%'].mean():.2f}%)")
            else:
                print()
    print("="*70)

if __name__ == "__main__":
    main()