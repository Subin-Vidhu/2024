import os
import csv
import nibabel as nib
import numpy as np

def load_nifti(file_path):
    """Load a NIfTI file and return the image object."""
    nifti_img = nib.load(file_path)
    return nifti_img

def reorient_to_match(target_img, source_img):
    """Reorient source_img to match the orientation of target_img."""
    reoriented_data = source_img.as_reoriented(nib.orientations.ornt_transform(nib.orientations.io_orientation(source_img.affine), nib.orientations.io_orientation(target_img.affine)))
    return reoriented_data

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
    return dice_scores

def process_cases(ground_truth_dir, predicted_dir, output_csv, num_classes):
    cases = os.listdir(ground_truth_dir)
    results = []

    for case in cases:
        case_id = os.path.splitext(case)[0]
        gt_path = os.path.join(ground_truth_dir, case)
        pred_path = os.path.join(predicted_dir, case.replace('_gt', '_pred'))  # Assumes pattern is correct

        try:
            # Check if files exist
            if not os.path.exists(gt_path) or not os.path.exists(pred_path):
                print(f"Skipping {case_id}: corresponding prediction file not found.")
                continue

            # Load the NIfTI files
            ground_truth_img = load_nifti(gt_path)
            predicted_img = load_nifti(pred_path)

            # Check if the orientation of the predicted image matches the ground truth
            if not np.allclose(ground_truth_img.affine, predicted_img.affine):
                print(f"The orientation of the predicted image for {case_id} is different from the ground truth. Reorienting the predicted image to match the ground truth.")
                predicted_img = reorient_to_match(ground_truth_img, predicted_img)

            # Get the data arrays
            ground_truth = ground_truth_img.get_fdata()
            predicted = predicted_img.get_fdata()

            # Ensure the shapes are the same
            if ground_truth.shape != predicted.shape:
                print(f"Shape mismatch between ground truth and prediction for {case_id}. Skipping case.")
                continue

            # Compute the Dice scores for each class
            dice_scores = multi_class_dice(ground_truth, predicted, num_classes)

            # Print the Dice scores along with the case name
            print(f"Case {case_id} Dice Scores:")
            for class_idx, score in enumerate(dice_scores):
                print(f'  Class {class_idx}: {score:.4f}')

            # Collect results with scores formatted to 4 decimal places
            result = [case_id] + [f'{score:.4f}' for score in dice_scores]
            results.append(result)

        except Exception as e:
            print(f"An error occurred while processing {case_id}: {e}")

    try:
        # Write results to CSV
        header = ['Case_ID'] + [f'Class_{i}_Dice' for i in range(num_classes)]
        with open(output_csv, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(header)
            writer.writerows(results)
    except Exception as e:
        print(f"An error occurred while writing results to CSV: {e}")

# Parameters
ground_truth_dir = r'e:\AJU AND SUJISHNA\METRICS\ground_truth'
predicted_dir = r'e:\AJU AND SUJISHNA\METRICS\predictions'
output_csv = r'D:\2024\zTest\dice_scores.csv'
num_classes = 4

# Process cases and save results to CSV
process_cases(ground_truth_dir, predicted_dir, output_csv, num_classes)