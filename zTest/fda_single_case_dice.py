# pip install nibabel numpy
import nibabel as nib
import numpy as np

# IMPORTANT DISCOVERY (2024-10-21):
# During comprehensive multi-reader analysis, we discovered that GT1_AS files
# are IDENTICAL to FDA_MC files (verified via MD5 hash). This means GT1_AS
# represents duplicate annotations, not independent reader annotations.
# True independent readers are: FDA_MC and GT02_GM only.
# AIRA performance: ~0.908 Dice after proper spatial reorientation and label mapping.

def load_nifti(file_path):
    """Load a NIfTI file and return the image object."""
    nifti_img = nib.load(file_path)
    return nifti_img

def get_orientation_string(img):
    """Get the orientation string for a NIfTI image."""
    ornt = nib.orientations.io_orientation(img.affine)
    return ''.join(nib.orientations.ornt2axcodes(ornt))

def get_voxel_volume(img):
    """Calculate the volume of a single voxel in mm³."""
    # Get voxel dimensions from the affine matrix
    voxel_dims = np.abs(img.header.get_zooms()[:3])
    voxel_volume = np.prod(voxel_dims)
    return voxel_volume, voxel_dims

def reorient_to_match(target_img, source_img):
    """Reorient source_img to match the orientation of target_img."""
    reoriented_data = source_img.as_reoriented(nib.orientations.ornt_transform(nib.orientations.io_orientation(source_img.affine),nib.orientations.io_orientation(target_img.affine)))
    return reoriented_data

def remap_labels(data, label_mapping):
    """
    Remap labels according to specified mapping with robust handling.
    Handles floating-point precision issues by rounding to nearest integer first.
    
    Parameters:
    -----------
    data : numpy array
        The data array with original labels
    label_mapping : dict
        Dictionary mapping old labels to new labels, e.g., {1: 2, 2: 3}
    
    Returns:
    --------
    remapped_data : numpy array
        Data array with remapped labels (int16 for clean integer labels)
    """
    # Handle floating-point precision issues by rounding to nearest integer
    data_rounded = np.round(data).astype(np.int16)
    
    # Create output array with int16 dtype
    remapped_data = np.zeros_like(data_rounded, dtype=np.int16)
    
    # Apply mapping
    for original_label, new_label in label_mapping.items():
        mask = (data_rounded == original_label)
        remapped_data[mask] = new_label
    
    return remapped_data  # Return as int16 for clean integer labels

def dice_coefficient(y_true, y_pred, epsilon=1e-6):
    """Compute the Dice coefficient between two numpy arrays."""
    intersection = np.sum(y_true * y_pred)
    union = np.sum(y_true) + np.sum(y_pred)
    if np.sum(y_true) == 0 and np.sum(y_pred) == 0:
        return 1.0  # Perfect match if both are completely absent
    return (2. * intersection + epsilon) / (union + epsilon)

def multi_class_dice(y_true, y_pred, num_classes, class_names=None):
    """Compute the Dice coefficient for each class and return the mean."""
    dice_scores = []
    for c in range(num_classes):
        y_true_c = (y_true == c).astype(np.float32)
        y_pred_c = (y_pred == c).astype(np.float32)
        dice_score = dice_coefficient(y_true_c, y_pred_c)
        dice_scores.append(dice_score)
        
        if class_names and c < len(class_names):
            print(f'Dice Score for {class_names[c]} (class {c}): {dice_score:.4f}')
        else:
            print(f'Dice Score for class {c}: {dice_score:.4f}')
    return dice_scores

def inspect_labels_with_volume(data, img, name="Image"):
    """Inspect unique labels in the data with volume calculations."""
    unique_labels = np.unique(data)
    voxel_volume_mm3, voxel_dims = get_voxel_volume(img)
    
    print(f"\n{name} - Voxel dimensions: {voxel_dims[0]:.2f} x {voxel_dims[1]:.2f} x {voxel_dims[2]:.2f} mm")
    print(f"{name} - Voxel volume: {voxel_volume_mm3:.2f} mm³")
    print(f"\n{name} - Unique labels and volumes:")
    print(f"{'Label':<10} {'Voxel Count':<15} {'Volume (mm³)':<15} {'Volume (cm³)':<15}")
    print("-" * 60)
    
    for label in unique_labels:
        count = np.sum(data == label)
        volume_mm3 = count * voxel_volume_mm3
        volume_cm3 = volume_mm3 / 1000.0
        print(f"{int(label):<10} {count:<15} {volume_mm3:<15.2f} {volume_cm3:<15.2f}")
    
    return unique_labels

def check_spatial_overlap(y_true, y_pred, class_label, class_name="Class"):
    """Check if there's any spatial overlap between masks."""
    true_mask = (y_true == class_label).astype(np.uint8)
    pred_mask = (y_pred == class_label).astype(np.uint8)
    
    if np.sum(true_mask) == 0 or np.sum(pred_mask) == 0:
        print(f"  {class_name}: One or both masks are empty")
        return
    
    # Get bounding boxes
    true_coords = np.argwhere(true_mask)
    pred_coords = np.argwhere(pred_mask)
    
    true_center = true_coords.mean(axis=0)
    pred_center = pred_coords.mean(axis=0)
    
    true_min = true_coords.min(axis=0)
    true_max = true_coords.max(axis=0)
    pred_min = pred_coords.min(axis=0)
    pred_max = pred_coords.max(axis=0)
    
    distance = np.linalg.norm(true_center - pred_center)
    overlap_voxels = np.sum(true_mask * pred_mask)
    
    print(f"  {class_name}:")
    print(f"    Ground truth center: {true_center.astype(int)}")
    print(f"    Predicted center: {pred_center.astype(int)}")
    print(f"    Distance between centers: {distance:.2f} voxels")
    print(f"    Ground truth bounds: {true_min} to {true_max}")
    print(f"    Predicted bounds: {pred_min} to {pred_max}")
    print(f"    Overlapping voxels: {overlap_voxels}")
    
    if overlap_voxels == 0:
        print(f"    ⚠️ WARNING: No spatial overlap! Kidneys may be swapped or misaligned.")

# Paths to the NIfTI files
ground_truth_path = r'c:\Users\Subin-PC\Downloads\Telegram Desktop\OneDrive_1_10-8-2025\N-072\N-072\N-072_MC.nii'
predicted_path = r'c:\Users\Subin-PC\Downloads\Telegram Desktop\OneDrive_1_10-8-2025\N-072\mask.nii'

# Load the NIfTI files
ground_truth_img = load_nifti(ground_truth_path)
predicted_img = load_nifti(predicted_path)

# Print orientations
print("\n" + "="*60)
print("ORIENTATION INFORMATION")
print("="*60)
print(f"Ground Truth orientation: {get_orientation_string(ground_truth_img)}")
print(f"Predicted orientation (original): {get_orientation_string(predicted_img)}")

# Check if the orientation of the predicted image matches the ground truth
reoriented = False
if not np.allclose(ground_truth_img.affine, predicted_img.affine):
    print("\n⚠️  The orientation of the predicted image is different from the ground truth.")
    print("   Reorienting the predicted image to match the ground truth...")
    predicted_img = reorient_to_match(ground_truth_img, predicted_img)
    reoriented = True
    print(f"   Predicted orientation (after reorientation): {get_orientation_string(predicted_img)}")
else:
    print("\n✓  Orientations match - no reorientation needed")
print("="*60)

# Get the data arrays
ground_truth = ground_truth_img.get_fdata()
predicted = predicted_img.get_fdata()

# Ensure the shapes are the same
assert ground_truth.shape == predicted.shape, "Shape mismatch between ground truth and prediction."

# Inspect labels in both images with volume information
print("="*60)
inspect_labels_with_volume(ground_truth, ground_truth_img, "Ground Truth")
print("\n")
inspect_labels_with_volume(predicted, predicted_img, "Predicted (Original)")
print("="*60)

# Define label mapping for the predicted image (AIRA)
# Based on spatial analysis and our comprehensive investigation:
# Ground truth (human readers): {0: background, 1: left kidney, 2: right kidney}
# AIRA original labels: {0: background, 1: noise, 2: left kidney, 3: right kidney}
# BUT spatially AIRA is different: label 2 is at RIGHT kidney location, label 3 is at LEFT kidney location
# Therefore we need to remap AIRA to match human reader spatial convention:
label_mapping = {
    0: 0,  # background stays as background
    1: 0,  # noise (only few voxels) -> treat as background
    2: 2,  # AIRA label 2 (spatially RIGHT kidney) -> ground truth right kidney (2)
    3: 1   # AIRA label 3 (spatially LEFT kidney) -> ground truth left kidney (1)
}

print(f"\nApplying label mapping to predicted image: {label_mapping}")
predicted = remap_labels(predicted, label_mapping)

# Save the final processed image (reoriented + remapped)
import os
predicted_dir = os.path.dirname(predicted_path)
predicted_filename = os.path.basename(predicted_path)
predicted_name, predicted_ext = os.path.splitext(predicted_filename)
if predicted_ext == '.gz':
    predicted_name, _ = os.path.splitext(predicted_name)
    predicted_ext = '.nii.gz'

# Create output filename
remapped_filename = f"{predicted_name}_remapped{predicted_ext}"
remapped_path = os.path.join(predicted_dir, remapped_filename)

# Save final processed image (includes reorientation if needed + label mapping)
predicted_remapped_img = nib.Nifti1Image(predicted, predicted_img.affine, predicted_img.header)
nib.save(predicted_remapped_img, remapped_path)
print(f"✓ Saved processed image (reoriented + remapped) to: {remapped_path}")

# Verify the remapping with volume information
print("\nAfter remapping:")
inspect_labels_with_volume(predicted, predicted_img, "Predicted (Remapped)")
print("="*60)

# Check spatial overlap for each kidney
print("\nSpatial Overlap Analysis:")
print("-"*60)
check_spatial_overlap(ground_truth, predicted, 1, "Left Kidney (label 1)")
check_spatial_overlap(ground_truth, predicted, 2, "Right Kidney (label 2)")
print("="*60)

# Number of classes and class names (based on ground truth)
num_classes = 3
class_names = ['Background', 'Left Kidney', 'Right Kidney']

# Compute the Dice scores for each class
print("\nDice Scores:")
print("-"*60)
dice_scores = multi_class_dice(ground_truth, predicted, num_classes, class_names)

# Compute and print the mean Dice score (excluding background)
dice_scores_no_bg = dice_scores[1:]  # Exclude background
mean_dice_score = np.mean(dice_scores)
mean_dice_score_no_bg = np.mean(dice_scores_no_bg)

print("-"*60)
print(f'Mean Dice Score (all classes): {mean_dice_score:.4f}')
print(f'Mean Dice Score (excluding background): {mean_dice_score_no_bg:.4f}')
print("="*60)

# Volume comparison table
print("\n" + "="*80)
print("VOLUME COMPARISON SUMMARY")
print("="*80)

voxel_volume_mm3, _ = get_voxel_volume(ground_truth_img)

# Calculate volumes for each class
print(f"\n{'Class':<20} {'GT Voxels':<15} {'GT Volume (cm³)':<18} {'Pred Voxels':<15} {'Pred Volume (cm³)':<18} {'Difference (cm³)':<18}")
print("-"*110)

for c in range(num_classes):
    gt_count = np.sum(ground_truth == c)
    pred_count = np.sum(predicted == c)
    
    gt_volume_cm3 = (gt_count * voxel_volume_mm3) / 1000.0
    pred_volume_cm3 = (pred_count * voxel_volume_mm3) / 1000.0
    diff_volume_cm3 = pred_volume_cm3 - gt_volume_cm3
    
    if class_names and c < len(class_names):
        class_name = class_names[c]
    else:
        class_name = f"Class {c}"
    
    print(f"{class_name:<20} {gt_count:<15} {gt_volume_cm3:<18.2f} {pred_count:<15} {pred_volume_cm3:<18.2f} {diff_volume_cm3:<+18.2f}")

# Calculate percentage differences for kidneys only
print("\n" + "-"*110)
print("Volume Difference Analysis (Kidneys Only):")
print("-"*110)
print(f"{'Class':<20} {'Absolute Diff (cm³)':<25} {'Relative Diff (%)':<25} {'Dice Score':<15}")
print("-"*110)

for c in range(1, num_classes):  # Skip background
    gt_count = np.sum(ground_truth == c)
    pred_count = np.sum(predicted == c)
    
    gt_volume_cm3 = (gt_count * voxel_volume_mm3) / 1000.0
    pred_volume_cm3 = (pred_count * voxel_volume_mm3) / 1000.0
    
    abs_diff = abs(pred_volume_cm3 - gt_volume_cm3)
    rel_diff = ((pred_volume_cm3 - gt_volume_cm3) / gt_volume_cm3) * 100 if gt_volume_cm3 > 0 else 0
    
    if class_names and c < len(class_names):
        class_name = class_names[c]
    else:
        class_name = f"Class {c}"
    
    print(f"{class_name:<20} {abs_diff:<25.2f} {rel_diff:<+25.2f} {dice_scores[c]:<15.4f}")

print("="*80)