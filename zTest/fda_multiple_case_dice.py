# pip install nibabel numpy pandas openpyxl
import nibabel as nib
import numpy as np
import pandas as pd
import os
from datetime import datetime
import glob

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
        'overlap_voxels': overlap_voxels,
        'true_center': true_center,
        'pred_center': pred_center
    }

def process_single_case(ground_truth_path, predicted_path, case_id, label_mapping):
    """Process a single case and return results."""
    print(f"\nProcessing {case_id}...")
    print("="*60)
    
    results = {
        'Case_ID': case_id,
        'Status': 'Failed',
        'Error_Message': None
    }
    
    try:
        # Load images
        ground_truth_img = load_nifti(ground_truth_path)
        predicted_img = load_nifti(predicted_path)
        
        if ground_truth_img is None or predicted_img is None:
            results['Error_Message'] = 'Failed to load NIfTI files'
            return results
        
        # Store orientations
        results['FDA_Orientation'] = get_orientation_string(ground_truth_img)
        results['AIRA_Orientation_Original'] = get_orientation_string(predicted_img)
        
        # Reorient if needed
        reoriented = False
        if not np.allclose(ground_truth_img.affine, predicted_img.affine):
            predicted_img = reorient_to_match(ground_truth_img, predicted_img)
            reoriented = True
            results['Reoriented'] = 'Yes'
        else:
            results['Reoriented'] = 'No'
        
        # Get data arrays
        ground_truth = ground_truth_img.get_fdata()
        predicted = predicted_img.get_fdata()
        
        # Check shape match
        if ground_truth.shape != predicted.shape:
            results['Error_Message'] = f'Shape mismatch: FDA={ground_truth.shape}, AIRA={predicted.shape}'
            return results
        
        results['Image_Shape'] = str(ground_truth.shape)
        
        # Get voxel information
        voxel_volume_mm3, voxel_dims = get_voxel_volume(ground_truth_img)
        results['Voxel_Dimensions_mm'] = f"{voxel_dims[0]:.2f}x{voxel_dims[1]:.2f}x{voxel_dims[2]:.2f}"
        results['Voxel_Volume_mm3'] = round(voxel_volume_mm3, 2)
        
        # Get original labels
        fda_labels = get_unique_labels(ground_truth)
        aira_labels_original = get_unique_labels(predicted)
        
        results['FDA_Unique_Labels'] = str(sorted(fda_labels.keys()))
        results['AIRA_Unique_Labels_Original'] = str(sorted(aira_labels_original.keys()))
        
        # Apply label mapping
        predicted = remap_labels(predicted, label_mapping)
        aira_labels_remapped = get_unique_labels(predicted)
        results['AIRA_Unique_Labels_Remapped'] = str(sorted(aira_labels_remapped.keys()))
        
        # Calculate Dice scores
        num_classes = 3
        class_names = ['Background', 'Left_Kidney', 'Right_Kidney']
        dice_scores = multi_class_dice(ground_truth, predicted, num_classes)
        
        for i, class_name in enumerate(class_names):
            results[f'Dice_{class_name}'] = round(dice_scores[i], 4)
        
        results['Mean_Dice_All_Classes'] = round(np.mean(dice_scores), 4)
        results['Mean_Dice_Kidneys_Only'] = round(np.mean(dice_scores[1:]), 4)
        
        # Calculate volumes for each class
        for c in range(num_classes):
            class_name = class_names[c]
            
            fda_count = np.sum(ground_truth == c)
            aira_count = np.sum(predicted == c)
            
            fda_volume_cm3 = (fda_count * voxel_volume_mm3) / 1000.0
            aira_volume_cm3 = (aira_count * voxel_volume_mm3) / 1000.0
            
            results[f'FDA_{class_name}_Voxels'] = int(fda_count)
            results[f'FDA_{class_name}_Volume_cm3'] = round(fda_volume_cm3, 2)
            results[f'AIRA_{class_name}_Voxels'] = int(aira_count)
            results[f'AIRA_{class_name}_Volume_cm3'] = round(aira_volume_cm3, 2)
            results[f'{class_name}_Volume_Diff_cm3'] = round(aira_volume_cm3 - fda_volume_cm3, 2)
            
            if fda_volume_cm3 > 0:
                rel_diff = ((aira_volume_cm3 - fda_volume_cm3) / fda_volume_cm3) * 100
                results[f'{class_name}_Volume_Diff_Percent'] = round(rel_diff, 2)
            else:
                results[f'{class_name}_Volume_Diff_Percent'] = None
        
        # Spatial alignment for kidneys
        for c, kidney_name in [(1, 'Left_Kidney'), (2, 'Right_Kidney')]:
            alignment = check_spatial_alignment(ground_truth, predicted, c)
            if alignment:
                results[f'{kidney_name}_Center_Distance_Voxels'] = round(alignment['center_distance'], 2)
                results[f'{kidney_name}_Overlap_Voxels'] = int(alignment['overlap_voxels'])
            else:
                results[f'{kidney_name}_Center_Distance_Voxels'] = None
                results[f'{kidney_name}_Overlap_Voxels'] = None
        
        results['Status'] = 'Success'
        print(f"✓ Successfully processed {case_id}")
        
    except Exception as e:
        results['Error_Message'] = str(e)
        print(f"✗ Error processing {case_id}: {e}")
    
    return results

def find_case_files(base_dir):
    """Find all case folders and their ground truth and predicted files."""
    cases = []
    
    # Get all N-xxx folders
    case_folders = glob.glob(os.path.join(base_dir, 'N-*'))
    
    for case_folder in sorted(case_folders):
        case_id = os.path.basename(case_folder)
        
        # Look for ground truth file (pattern: N-xxx_MC.nii or N-xxx_MC.nii.gz)
        gt_patterns = [
            os.path.join(case_folder, case_id, f'{case_id}_MC.nii'),
            os.path.join(case_folder, case_id, f'{case_id}_MC.nii.gz'),
            os.path.join(case_folder, f'{case_id}_MC.nii'),
            os.path.join(case_folder, f'{case_id}_MC.nii.gz')
        ]
        
        ground_truth_path = None
        for pattern in gt_patterns:
            if os.path.exists(pattern):
                ground_truth_path = pattern
                break
        
        # Look for predicted file (pattern: mask.nii or mask.nii.gz)
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
            print(f"Found: {case_id}")
        else:
            print(f"Skipping {case_id}: Missing files (GT={ground_truth_path is not None}, Pred={predicted_path is not None})")
    
    return cases

def main():
    # Base directory containing all case folders
    base_dir = r'c:\Users\Subin-PC\Downloads\Telegram Desktop\OneDrive_1_10-8-2025\test'
    
    # Output Excel file path
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_excel = os.path.join(base_dir, f'FDA_AIRA_Analysis_Results_{timestamp}.xlsx')
    
    # Label mapping (adjust based on your data)
    label_mapping = {
        0: 0,  # background
        1: 0,  # noise -> background
        2: 2,  # right kidney
        3: 1   # left kidney
    }
    
    print("="*60)
    print("FDA vs AIRA - Multi-Case Analysis")
    print("="*60)
    print(f"Base directory: {base_dir}")
    print(f"Label mapping: {label_mapping}")
    print("="*60)
    
    # Find all cases
    print("\nSearching for case files...")
    cases = find_case_files(base_dir)
    print(f"\nFound {len(cases)} cases to process")
    
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
            label_mapping
        )
        all_results.append(result)
    
    # Create DataFrame
    df = pd.DataFrame(all_results)
    
    # Reorder columns for better readability
    column_order = [
        'Case_ID', 'Status', 'Error_Message',
        'Image_Shape', 'Voxel_Dimensions_mm', 'Voxel_Volume_mm3',
        'FDA_Orientation', 'AIRA_Orientation_Original', 'Reoriented',
        'FDA_Unique_Labels', 'AIRA_Unique_Labels_Original', 'AIRA_Unique_Labels_Remapped',
        
        # Dice Scores
        'Dice_Background', 'Dice_Left_Kidney', 'Dice_Right_Kidney',
        'Mean_Dice_All_Classes', 'Mean_Dice_Kidneys_Only',
        
        # Background volumes
        'FDA_Background_Voxels', 'FDA_Background_Volume_cm3',
        'AIRA_Background_Voxels', 'AIRA_Background_Volume_cm3',
        'Background_Volume_Diff_cm3', 'Background_Volume_Diff_Percent',
        
        # Left Kidney volumes
        'FDA_Left_Kidney_Voxels', 'FDA_Left_Kidney_Volume_cm3',
        'AIRA_Left_Kidney_Voxels', 'AIRA_Left_Kidney_Volume_cm3',
        'Left_Kidney_Volume_Diff_cm3', 'Left_Kidney_Volume_Diff_Percent',
        'Left_Kidney_Center_Distance_Voxels', 'Left_Kidney_Overlap_Voxels',
        
        # Right Kidney volumes
        'FDA_Right_Kidney_Voxels', 'FDA_Right_Kidney_Volume_cm3',
        'AIRA_Right_Kidney_Voxels', 'AIRA_Right_Kidney_Volume_cm3',
        'Right_Kidney_Volume_Diff_cm3', 'Right_Kidney_Volume_Diff_Percent',
        'Right_Kidney_Center_Distance_Voxels', 'Right_Kidney_Overlap_Voxels'
    ]
    
    # Reorder columns (keep any extra columns at the end)
    existing_columns = [col for col in column_order if col in df.columns]
    extra_columns = [col for col in df.columns if col not in column_order]
    df = df[existing_columns + extra_columns]
    
    # Save to Excel with multiple sheets
    with pd.ExcelWriter(output_excel, engine='openpyxl') as writer:
        # Main results sheet
        df.to_excel(writer, sheet_name='All_Results', index=False)
        
        # Summary statistics sheet
        successful_cases = df[df['Status'] == 'Success']
        if len(successful_cases) > 0:
            summary_data = {
                'Metric': [
                    'Total Cases',
                    'Successful Cases',
                    'Failed Cases',
                    '',
                    'Mean Dice - Left Kidney',
                    'Mean Dice - Right Kidney',
                    'Mean Dice - Kidneys Only',
                    '',
                    'Mean FDA Left Kidney Volume (cm³)',
                    'Mean AIRA Left Kidney Volume (cm³)',
                    'Mean Left Kidney Volume Diff (cm³)',
                    'Mean Left Kidney Volume Diff (%)',
                    '',
                    'Mean FDA Right Kidney Volume (cm³)',
                    'Mean AIRA Right Kidney Volume (cm³)',
                    'Mean Right Kidney Volume Diff (cm³)',
                    'Mean Right Kidney Volume Diff (%)',
                ],
                'Value': [
                    len(df),
                    len(successful_cases),
                    len(df[df['Status'] == 'Failed']),
                    '',
                    round(successful_cases['Dice_Left_Kidney'].mean(), 4),
                    round(successful_cases['Dice_Right_Kidney'].mean(), 4),
                    round(successful_cases['Mean_Dice_Kidneys_Only'].mean(), 4),
                    '',
                    round(successful_cases['FDA_Left_Kidney_Volume_cm3'].mean(), 2),
                    round(successful_cases['AIRA_Left_Kidney_Volume_cm3'].mean(), 2),
                    round(successful_cases['Left_Kidney_Volume_Diff_cm3'].mean(), 2),
                    round(successful_cases['Left_Kidney_Volume_Diff_Percent'].mean(), 2),
                    '',
                    round(successful_cases['FDA_Right_Kidney_Volume_cm3'].mean(), 2),
                    round(successful_cases['AIRA_Right_Kidney_Volume_cm3'].mean(), 2),
                    round(successful_cases['Right_Kidney_Volume_Diff_cm3'].mean(), 2),
                    round(successful_cases['Right_Kidney_Volume_Diff_Percent'].mean(), 2),
                ]
            }
            summary_df = pd.DataFrame(summary_data)
            summary_df.to_excel(writer, sheet_name='Summary', index=False)
        
        # Failed cases sheet (if any)
        failed_cases = df[df['Status'] == 'Failed']
        if len(failed_cases) > 0:
            failed_cases.to_excel(writer, sheet_name='Failed_Cases', index=False)
    
    print("\n" + "="*60)
    print("ANALYSIS COMPLETE")
    print("="*60)
    print(f"Total cases processed: {len(cases)}")
    print(f"Successful: {len(successful_cases)}")
    print(f"Failed: {len(df[df['Status'] == 'Failed'])}")
    print(f"\nResults saved to: {output_excel}")
    print("="*60)
    
    # Print summary statistics
    if len(successful_cases) > 0:
        print("\nSUMMARY STATISTICS:")
        print("-"*60)
        print(f"Mean Dice Score (Kidneys Only): {successful_cases['Mean_Dice_Kidneys_Only'].mean():.4f}")
        print(f"Mean Left Kidney Dice: {successful_cases['Dice_Left_Kidney'].mean():.4f}")
        print(f"Mean Right Kidney Dice: {successful_cases['Dice_Right_Kidney'].mean():.4f}")
        print(f"\nMean Left Kidney Volume Diff: {successful_cases['Left_Kidney_Volume_Diff_cm3'].mean():.2f} cm³ ({successful_cases['Left_Kidney_Volume_Diff_Percent'].mean():.2f}%)")
        print(f"Mean Right Kidney Volume Diff: {successful_cases['Right_Kidney_Volume_Diff_cm3'].mean():.2f} cm³ ({successful_cases['Right_Kidney_Volume_Diff_Percent'].mean():.2f}%)")
        print("="*60)

if __name__ == "__main__":
    main()