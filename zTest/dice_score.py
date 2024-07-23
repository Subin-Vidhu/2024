import nibabel as nib
import numpy as np

def load_nifti(file_path):
    """Load a NIfTI file and return the image object."""
    nifti_img = nib.load(file_path)
    return nifti_img

def reorient_to_match(target_img, source_img):
    """Reorient source_img to match the orientation of target_img."""
    source_data = source_img.get_fdata()
    reoriented_data = nib.orientations.apply_orientation(source_data, nib.orientations.io_orientation(target_img.affine))
    return nib.Nifti1Image(reoriented_data, target_img.affine)

def dice_coefficient(y_true, y_pred, epsilon=1e-6):
    """Compute the Dice coefficient between two numpy arrays."""
    intersection = np.sum(y_true * y_pred)
    union = np.sum(y_true) + np.sum(y_pred)
    if np.sum(y_true) == 0 and np.sum(y_pred) == 0:
        return 1.0  # Perfect match if both are completely absent
    return (2. * intersection + epsilon) / (union + epsilon)

def multi_class_dice(y_true, y_pred, num_classes):
    """Compute the Dice coefficient for each class and return the mean."""
    dice_scores = []
    for c in range(num_classes):
        y_true_c = (y_true == c).astype(np.float32)
        y_pred_c = (y_pred == c).astype(np.float32)
        dice_score = dice_coefficient(y_true_c, y_pred_c)
        dice_scores.append(dice_score)
        print(f'Dice Score for class {c}: {dice_score:.4f}')
    return dice_scores

# Paths to the NIfTI files
ground_truth_path = 'd:\__SHARED__\Antony\Dice_Score\SU9\SU9_512_Model_296.nii'
predicted_path = 'd:\__SHARED__\Antony\Dice_Score\SU9\SU9_512_Model.nii'

# Load the NIfTI files
ground_truth_img = load_nifti(ground_truth_path)
predicted_img = load_nifti(predicted_path)

# Check if the orientation of the predicted image matches the ground truth
if not np.allclose(ground_truth_img.affine, predicted_img.affine):
    print("The orientation of the predicted image is different from the ground truth. Reorienting the predicted image to match the ground truth.")
    predicted_img = reorient_to_match(ground_truth_img, predicted_img)

# Get the data arrays
ground_truth = ground_truth_img.get_fdata()
predicted = predicted_img.get_fdata()

# Ensure the shapes are the same
assert ground_truth.shape == predicted.shape, "Shape mismatch between ground truth and prediction."

# Number of classes
num_classes = 4

# Compute the Dice scores for each class
dice_scores = multi_class_dice(ground_truth, predicted, num_classes)

# Compute and print the mean Dice score
mean_dice_score = np.mean(dice_scores)
print(f'Mean Dice Score: {mean_dice_score:.4f}')
