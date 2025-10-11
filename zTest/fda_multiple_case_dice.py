# pip install nibabel numpy pandas openpyxl matplotlib seaborn scikit-learn
import nibabel as nib
import numpy as np
import pandas as pd
import os
from datetime import datetime
import glob
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import roc_curve, auc
from sklearn.preprocessing import label_binarize
import warnings
warnings.filterwarnings('ignore')

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
    'save_detailed_stats': True,        # Save detailed statistics CSV file
    
    # Visualization Options
    'create_plots': True,               # Generate visualization plots
    'save_individual_plots': True,      # Save individual plot files
    'create_combined_figure': True,     # Create one combined figure with all plots
    'plot_dpi': 300,                   # Plot resolution (300 DPI for publication quality)
    'plot_style': 'seaborn-v0_8',     # Plot style
}

# Label mapping configuration
LABEL_MAPPING = {
    0: 0,  # background
    1: 0,  # noise -> background
    2: 2,  # left kidney
    3: 1   # right kidney
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

def calculate_regression_metrics(y_true, y_pred):
    """Calculate comprehensive regression metrics for numerical comparison."""
    if len(y_true) == 0 or len(y_pred) == 0:
        return {}
    
    # Ensure arrays are the same length and remove NaN values
    mask = ~(np.isnan(y_true) | np.isnan(y_pred))
    y_true_clean = np.array(y_true)[mask]
    y_pred_clean = np.array(y_pred)[mask]
    
    if len(y_true_clean) == 0:
        return {}
    
    # Basic error metrics
    errors = y_pred_clean - y_true_clean
    abs_errors = np.abs(errors)
    
    metrics = {}
    
    # Mean Absolute Error (MAE)
    metrics['MAE'] = np.mean(abs_errors)
    
    # Mean Squared Error (MSE)
    metrics['MSE'] = np.mean(errors**2)
    
    # Root Mean Squared Error (RMSE)
    metrics['RMSE'] = np.sqrt(metrics['MSE'])
    
    # Mean Absolute Percentage Error (MAPE) - avoid division by zero
    non_zero_mask = y_true_clean != 0
    if np.any(non_zero_mask):
        mape_values = np.abs(errors[non_zero_mask] / y_true_clean[non_zero_mask]) * 100
        metrics['MAPE'] = np.mean(mape_values)
    else:
        metrics['MAPE'] = np.nan
    
    # Symmetric Mean Absolute Percentage Error (SMAPE)
    denominator = (np.abs(y_true_clean) + np.abs(y_pred_clean)) / 2
    non_zero_denom = denominator != 0
    if np.any(non_zero_denom):
        smape_values = np.abs(errors[non_zero_denom] / denominator[non_zero_denom]) * 100
        metrics['SMAPE'] = np.mean(smape_values)
    else:
        metrics['SMAPE'] = np.nan
    
    # R-squared (coefficient of determination)
    ss_res = np.sum(errors**2)
    ss_tot = np.sum((y_true_clean - np.mean(y_true_clean))**2)
    if ss_tot != 0:
        metrics['R_squared'] = 1 - (ss_res / ss_tot)
    else:
        metrics['R_squared'] = np.nan
    
    # Pearson correlation coefficient
    if len(y_true_clean) > 1:
        correlation_matrix = np.corrcoef(y_true_clean, y_pred_clean)
        metrics['Correlation'] = correlation_matrix[0, 1] if not np.isnan(correlation_matrix[0, 1]) else 0
    else:
        metrics['Correlation'] = np.nan
    
    # Mean Bias Error (MBE) - systematic bias
    metrics['MBE'] = np.mean(errors)
    
    # Normalized RMSE (NRMSE) - RMSE normalized by the range of true values
    y_range = np.max(y_true_clean) - np.min(y_true_clean)
    if y_range != 0:
        metrics['NRMSE'] = metrics['RMSE'] / y_range * 100  # as percentage
    else:
        metrics['NRMSE'] = np.nan
    
    # Index of Agreement (Willmott's d)
    numerator = np.sum((y_pred_clean - y_true_clean)**2)
    denominator = np.sum((np.abs(y_pred_clean - np.mean(y_true_clean)) + 
                         np.abs(y_true_clean - np.mean(y_true_clean)))**2)
    if denominator != 0:
        metrics['Index_of_Agreement'] = 1 - (numerator / denominator)
    else:
        metrics['Index_of_Agreement'] = np.nan
    
    return metrics

def calculate_comprehensive_statistics(df):
    """Calculate comprehensive statistics for FDA evaluation."""
    successful_cases = df[df['Status'] == 'Success'] if 'Status' in df.columns else df
    
    if len(successful_cases) == 0:
        return pd.DataFrame()
    
    stats_data = []
    
    # Basic case information
    stats_data.append(['CASE SUMMARY', '', '', '', '', ''])
    stats_data.append(['Total Cases', len(df), '', '', '', ''])
    if 'Status' in df.columns:
        stats_data.append(['Successful Cases', len(successful_cases), '', '', '', ''])
        stats_data.append(['Failed Cases', len(df[df['Status'] == 'Failed']), '', '', '', ''])
        stats_data.append(['Success Rate (%)', round((len(successful_cases) / len(df)) * 100, 2), '', '', '', ''])
    stats_data.append(['', '', '', '', '', ''])
    
    # Dice Score Statistics
    dice_metrics = ['Dice_Left_Kidney', 'Dice_Right_Kidney']
    if any(col in successful_cases.columns for col in dice_metrics):
        stats_data.append(['DICE COEFFICIENT ANALYSIS', '', '', '', '', ''])
        stats_data.append(['Metric', 'Mean', 'Std Dev', 'Min', 'Max', 'Median'])
        
        for metric in dice_metrics:
            if metric in successful_cases.columns:
                values = successful_cases[metric].dropna()
                if len(values) > 0:
                    kidney_name = metric.replace('Dice_', '')
                    stats_data.append([
                        kidney_name,
                        round(values.mean(), 4),
                        round(values.std(), 4),
                        round(values.min(), 4),
                        round(values.max(), 4),
                        round(values.median(), 4)
                    ])
        
        # Overall kidney dice (average of both kidneys)
        if all(col in successful_cases.columns for col in dice_metrics):
            overall_dice = successful_cases[dice_metrics].mean(axis=1)
            stats_data.append([
                'Overall_Kidneys',
                round(overall_dice.mean(), 4),
                round(overall_dice.std(), 4),
                round(overall_dice.min(), 4),
                round(overall_dice.max(), 4),
                round(overall_dice.median(), 4)
            ])
        
        stats_data.append(['', '', '', '', '', ''])
    
    # Volume Statistics - FDA (Ground Truth)
    fda_vol_metrics = ['FDA_Left_Kidney_Vol_cm3', 'FDA_Right_Kidney_Vol_cm3']
    if any(col in successful_cases.columns for col in fda_vol_metrics):
        stats_data.append(['FDA VOLUMES (Ground Truth) - cm³', '', '', '', '', ''])
        stats_data.append(['Metric', 'Mean', 'Std Dev', 'Min', 'Max', 'Median'])
        
        for metric in fda_vol_metrics:
            if metric in successful_cases.columns:
                values = successful_cases[metric].dropna()
                if len(values) > 0:
                    kidney_name = metric.replace('FDA_', '').replace('_Vol_cm3', '')
                    stats_data.append([
                        kidney_name,
                        round(values.mean(), 2),
                        round(values.std(), 2),
                        round(values.min(), 2),
                        round(values.max(), 2),
                        round(values.median(), 2)
                    ])
        
        # Total kidney volume (both kidneys combined)
        if all(col in successful_cases.columns for col in fda_vol_metrics):
            total_fda = successful_cases[fda_vol_metrics].sum(axis=1)
            stats_data.append([
                'Total_Kidneys',
                round(total_fda.mean(), 2),
                round(total_fda.std(), 2),
                round(total_fda.min(), 2),
                round(total_fda.max(), 2),
                round(total_fda.median(), 2)
            ])
        
        stats_data.append(['', '', '', '', '', ''])
    
    # Volume Statistics - AIRA (Predicted)
    aira_vol_metrics = ['AIRA_Left_Kidney_Vol_cm3', 'AIRA_Right_Kidney_Vol_cm3']
    if any(col in successful_cases.columns for col in aira_vol_metrics):
        stats_data.append(['AIRA VOLUMES (Predicted) - cm³', '', '', '', '', ''])
        stats_data.append(['Metric', 'Mean', 'Std Dev', 'Min', 'Max', 'Median'])
        
        for metric in aira_vol_metrics:
            if metric in successful_cases.columns:
                values = successful_cases[metric].dropna()
                if len(values) > 0:
                    kidney_name = metric.replace('AIRA_', '').replace('_Vol_cm3', '')
                    stats_data.append([
                        kidney_name,
                        round(values.mean(), 2),
                        round(values.std(), 2),
                        round(values.min(), 2),
                        round(values.max(), 2),
                        round(values.median(), 2)
                    ])
        
        # Total kidney volume (both kidneys combined)
        if all(col in successful_cases.columns for col in aira_vol_metrics):
            total_aira = successful_cases[aira_vol_metrics].sum(axis=1)
            stats_data.append([
                'Total_Kidneys',
                round(total_aira.mean(), 2),
                round(total_aira.std(), 2),
                round(total_aira.min(), 2),
                round(total_aira.max(), 2),
                round(total_aira.median(), 2)
            ])
        
        stats_data.append(['', '', '', '', '', ''])
    
    # Volume Differences (Absolute)
    diff_metrics = ['Left_Kidney_Diff_cm3', 'Right_Kidney_Diff_cm3']
    if any(col in successful_cases.columns for col in diff_metrics):
        stats_data.append(['VOLUME DIFFERENCES (AIRA - FDA) - cm³', '', '', '', '', ''])
        stats_data.append(['Metric', 'Mean', 'Std Dev', 'Min', 'Max', 'Median'])
        
        for metric in diff_metrics:
            if metric in successful_cases.columns:
                values = successful_cases[metric].dropna()
                if len(values) > 0:
                    kidney_name = metric.replace('_Diff_cm3', '')
                    stats_data.append([
                        kidney_name,
                        round(values.mean(), 2),
                        round(values.std(), 2),
                        round(values.min(), 2),
                        round(values.max(), 2),
                        round(values.median(), 2)
                    ])
        
        stats_data.append(['', '', '', '', '', ''])
    
    # Volume Differences (Percentage)
    perc_metrics = ['Left_Kidney_Diff_%', 'Right_Kidney_Diff_%']
    if any(col in successful_cases.columns for col in perc_metrics):
        stats_data.append(['VOLUME DIFFERENCES (AIRA - FDA) - %', '', '', '', '', ''])
        stats_data.append(['Metric', 'Mean', 'Std Dev', 'Min', 'Max', 'Median'])
        
        for metric in perc_metrics:
            if metric in successful_cases.columns:
                values = successful_cases[metric].dropna()
                if len(values) > 0:
                    kidney_name = metric.replace('_Diff_%', '')
                    stats_data.append([
                        kidney_name,
                        round(values.mean(), 2),
                        round(values.std(), 2),
                        round(values.min(), 2),
                        round(values.max(), 2),
                        round(values.median(), 2)
                    ])
        
        stats_data.append(['', '', '', '', '', ''])
    
    # Agreement Analysis (Clinical Thresholds)
    stats_data.append(['CLINICAL AGREEMENT ANALYSIS', '', '', '', '', ''])
    stats_data.append(['Threshold', 'Cases Meeting Criteria', 'Percentage', '', '', ''])
    
    # Dice coefficient thresholds
    for threshold in [0.7, 0.8, 0.85, 0.9]:
        for metric in dice_metrics:
            if metric in successful_cases.columns:
                meeting_criteria = (successful_cases[metric] >= threshold).sum()
                percentage = (meeting_criteria / len(successful_cases)) * 100
                kidney_name = metric.replace('Dice_', '')
                stats_data.append([
                    f'{kidney_name} Dice ≥ {threshold}',
                    meeting_criteria,
                    f'{percentage:.1f}%',
                    '', '', ''
                ])
    
    # Volume difference thresholds (absolute)
    for threshold in [5, 10, 15, 20]:  # cm³
        for metric in diff_metrics:
            if metric in successful_cases.columns:
                meeting_criteria = (np.abs(successful_cases[metric]) <= threshold).sum()
                percentage = (meeting_criteria / len(successful_cases)) * 100
                kidney_name = metric.replace('_Diff_cm3', '')
                stats_data.append([
                    f'{kidney_name} |Diff| ≤ {threshold} cm³',
                    meeting_criteria,
                    f'{percentage:.1f}%',
                    '', '', ''
                ])
    
    # Volume difference thresholds (percentage)
    for threshold in [5, 10, 15, 20]:  # %
        for metric in perc_metrics:
            if metric in successful_cases.columns:
                meeting_criteria = (np.abs(successful_cases[metric]) <= threshold).sum()
                percentage = (meeting_criteria / len(successful_cases)) * 100
                kidney_name = metric.replace('_Diff_%', '')
                stats_data.append([
                    f'{kidney_name} |Diff| ≤ {threshold}%',
                    meeting_criteria,
                    f'{percentage:.1f}%',
                    '', '', ''
                ])
    
    stats_data.append(['', '', '', '', '', ''])
    
    # AI/ML Regression Metrics Analysis
    regression_pairs = [
        ('FDA_Left_Kidney_Vol_cm3', 'AIRA_Left_Kidney_Vol_cm3', 'Left Kidney Volume'),
        ('FDA_Right_Kidney_Vol_cm3', 'AIRA_Right_Kidney_Vol_cm3', 'Right Kidney Volume')
    ]
    
    stats_data.append(['AI/ML REGRESSION METRICS', '', '', '', '', ''])
    stats_data.append(['Metric', 'Left Kidney', 'Right Kidney', '', '', ''])
    
    # Calculate metrics for each pair
    all_metrics = {}
    for fda_col, aira_col, label in regression_pairs:
        if fda_col in successful_cases.columns and aira_col in successful_cases.columns:
            fda_vals = successful_cases[fda_col].dropna()
            aira_vals = successful_cases[aira_col].dropna()
            
            # Ensure same length arrays
            min_len = min(len(fda_vals), len(aira_vals))
            if min_len > 0:
                fda_vals = fda_vals.iloc[:min_len]
                aira_vals = aira_vals.iloc[:min_len]
                
                metrics = calculate_regression_metrics(fda_vals.values, aira_vals.values)
                kidney_side = 'Left' if 'Left' in label else 'Right'
                all_metrics[kidney_side] = metrics
    
    # Display metrics in organized rows
    metric_names = [
        ('MAE', 'Mean Absolute Error (cm³)'),
        ('MSE', 'Mean Squared Error (cm³²)'),
        ('RMSE', 'Root Mean Squared Error (cm³)'),
        ('MAPE', 'Mean Absolute Percentage Error (%)'),
        ('SMAPE', 'Symmetric MAPE (%)'),
        ('MBE', 'Mean Bias Error (cm³)'),
        ('NRMSE', 'Normalized RMSE (%)'),
        ('R_squared', 'R-squared'),
        ('Correlation', 'Pearson Correlation'),
        ('Index_of_Agreement', 'Index of Agreement')
    ]
    
    for metric_key, metric_name in metric_names:
        left_val = all_metrics.get('Left', {}).get(metric_key, 'N/A')
        right_val = all_metrics.get('Right', {}).get(metric_key, 'N/A')
        
        if isinstance(left_val, float) and not np.isnan(left_val):
            left_val = f'{left_val:.4f}' if abs(left_val) < 1000 else f'{left_val:.2f}'
        elif isinstance(left_val, float) and np.isnan(left_val):
            left_val = 'N/A'
            
        if isinstance(right_val, float) and not np.isnan(right_val):
            right_val = f'{right_val:.4f}' if abs(right_val) < 1000 else f'{right_val:.2f}'
        elif isinstance(right_val, float) and np.isnan(right_val):
            right_val = 'N/A'
        
        stats_data.append([metric_name, left_val, right_val, '', '', ''])
    
    stats_data.append(['', '', '', '', '', ''])
    
    # Model Performance Classification
    stats_data.append(['MODEL PERFORMANCE ASSESSMENT', '', '', '', '', ''])
    stats_data.append(['Metric', 'Left Kidney', 'Right Kidney', 'Interpretation', '', ''])
    
    # Performance thresholds and interpretations
    performance_assessments = []
    
    for kidney_side in ['Left', 'Right']:
        if kidney_side in all_metrics:
            metrics = all_metrics[kidney_side]
            assessments = []
            
            # R-squared assessment
            r2 = metrics.get('R_squared', np.nan)
            if not np.isnan(r2):
                if r2 >= 0.9:
                    r2_assessment = 'Excellent'
                elif r2 >= 0.8:
                    r2_assessment = 'Good'
                elif r2 >= 0.6:
                    r2_assessment = 'Moderate'
                else:
                    r2_assessment = 'Poor'
                assessments.append(f'R²: {r2_assessment}')
            
            # Correlation assessment
            corr = metrics.get('Correlation', np.nan)
            if not np.isnan(corr):
                if abs(corr) >= 0.9:
                    corr_assessment = 'Very Strong'
                elif abs(corr) >= 0.7:
                    corr_assessment = 'Strong'
                elif abs(corr) >= 0.5:
                    corr_assessment = 'Moderate'
                else:
                    corr_assessment = 'Weak'
                assessments.append(f'Corr: {corr_assessment}')
            
            # MAPE assessment
            mape = metrics.get('MAPE', np.nan)
            if not np.isnan(mape):
                if mape <= 5:
                    mape_assessment = 'Excellent'
                elif mape <= 10:
                    mape_assessment = 'Good'
                elif mape <= 20:
                    mape_assessment = 'Acceptable'
                else:
                    mape_assessment = 'Poor'
                assessments.append(f'MAPE: {mape_assessment}')
            
            performance_assessments.append('; '.join(assessments))
        else:
            performance_assessments.append('N/A')
    
    stats_data.append(['Overall Assessment', 
                      performance_assessments[0] if len(performance_assessments) > 0 else 'N/A',
                      performance_assessments[1] if len(performance_assessments) > 1 else 'N/A',
                      'R²≥0.9: Excellent, ≥0.8: Good', '', ''])
    stats_data.append(['', '', '', 'MAPE≤5%: Excellent, ≤10%: Good', '', ''])
    
    stats_data.append(['', '', '', '', '', ''])
    
    # Bland-Altman Analysis Summary
    stats_data.append(['BLAND-ALTMAN ANALYSIS', '', '', '', '', ''])
    stats_data.append(['Metric', 'Left Kidney', 'Right Kidney', '', '', ''])
    
    for kidney_side in ['Left', 'Right']:
        if kidney_side in all_metrics:
            metrics = all_metrics[kidney_side]
            
            # Mean difference (bias)
            bias = metrics.get('MBE', np.nan)
            
            # Limits of agreement (approximate, would need individual data for exact calculation)
            rmse = metrics.get('RMSE', np.nan)
            if not np.isnan(rmse):
                # Approximate 95% limits of agreement as ±1.96 * SD of differences
                # Using RMSE as approximation for SD of differences
                loa_upper = 1.96 * rmse
                loa_lower = -1.96 * rmse
            else:
                loa_upper = loa_lower = np.nan
    
    bias_left = all_metrics.get('Left', {}).get('MBE', np.nan)
    bias_right = all_metrics.get('Right', {}).get('MBE', np.nan)
    
    bias_left_str = f'{bias_left:.2f}' if not np.isnan(bias_left) else 'N/A'
    bias_right_str = f'{bias_right:.2f}' if not np.isnan(bias_right) else 'N/A'
    
    stats_data.append(['Mean Bias (cm³)', bias_left_str, bias_right_str, '', '', ''])
    
    # Convert to DataFrame
    stats_df = pd.DataFrame(stats_data, columns=['Metric', 'Value1', 'Value2', 'Value3', 'Value4', 'Value5'])
    return stats_df

def create_roc_curves(df, results_dir, timestamp, config):
    """Create ROC curves for Dice coefficient thresholds."""
    if not config.get('create_plots', False):
        return []
    
    successful_cases = df[df['Status'] == 'Success'] if 'Status' in df.columns else df
    
    if len(successful_cases) < 5:  # Need sufficient cases for meaningful ROC
        return []
    
    try:
        plt.style.use(config.get('plot_style', 'default'))
    except:
        pass
    
    plot_files = []
    
    # ROC curves for different Dice thresholds
    dice_columns = ['Dice_Right_Kidney', 'Dice_Left_Kidney']
    thresholds = [0.7, 0.8, 0.85, 0.9]  # Reduced for better legend fit
    
    fig, axes = plt.subplots(1, 2, figsize=(15, 6))  # Larger figure
    fig.suptitle('AUC-ROC Curves for Dice Coefficient Thresholds', fontsize=16, fontweight='bold', y=0.98)
    
    for idx, dice_col in enumerate(dice_columns):
        if dice_col not in successful_cases.columns:
            continue
            
        ax = axes[idx]
        kidney_name = dice_col.replace('Dice_', '').replace('_', ' ')
        
        dice_values = successful_cases[dice_col].dropna()
        
        for threshold in thresholds:
            # Create binary classification (above/below threshold)
            y_true = (dice_values >= threshold).astype(int)
            y_scores = dice_values.values
            
            if len(np.unique(y_true)) < 2:  # Need both classes
                continue
                
            fpr, tpr, _ = roc_curve(y_true, y_scores)
            roc_auc = auc(fpr, tpr)
            
            ax.plot(fpr, tpr, linewidth=2.5, 
                   label=f'Dice ≥ {threshold} (AUC = {roc_auc:.3f})')
        
        ax.plot([0, 1], [0, 1], 'k--', linewidth=1.5, alpha=0.6, label='Random Classifier')
        ax.set_xlim([0.0, 1.0])
        ax.set_ylim([0.0, 1.05])
        ax.set_xlabel('False Positive Rate', fontsize=12, fontweight='bold')
        ax.set_ylabel('True Positive Rate', fontsize=12, fontweight='bold')
        ax.set_title(f'{kidney_name} AUC-ROC Analysis', fontsize=14, fontweight='bold', pad=20)
        ax.legend(loc="lower right", fontsize=10, frameon=True, fancybox=True, shadow=True)
        ax.grid(True, alpha=0.3)
        ax.tick_params(labelsize=10)
    
    plt.tight_layout()
    
    if config.get('save_individual_plots', True):
        roc_file = os.path.join(results_dir, f'ROC_Curves_{timestamp}.png')
        plt.savefig(roc_file, dpi=config.get('plot_dpi', 300), bbox_inches='tight')
        plot_files.append(roc_file)
    
    plt.close()
    return plot_files

def create_bland_altman_plots(df, results_dir, timestamp, config):
    """Create Bland-Altman plots for volume agreement analysis."""
    if not config.get('create_plots', False):
        return []
    
    successful_cases = df[df['Status'] == 'Success'] if 'Status' in df.columns else df
    
    if len(successful_cases) < 3:
        return []
    
    try:
        plt.style.use(config.get('plot_style', 'default'))
    except:
        pass
    
    plot_files = []
    
    # Volume comparison pairs
    volume_pairs = [
        ('FDA_Right_Kidney_Vol_cm3', 'AIRA_Right_Kidney_Vol_cm3', 'Right Kidney'),
        ('FDA_Left_Kidney_Vol_cm3', 'AIRA_Left_Kidney_Vol_cm3', 'Left Kidney')
    ]
    
    fig, axes = plt.subplots(1, 2, figsize=(16, 7))  # Larger figure
    fig.suptitle('Bland-Altman Plots: Volume Agreement Analysis', fontsize=16, fontweight='bold', y=0.95)
    
    for idx, (fda_col, aira_col, kidney_name) in enumerate(volume_pairs):
        if fda_col not in successful_cases.columns or aira_col not in successful_cases.columns:
            continue
        
        ax = axes[idx]
        
        fda_vals = successful_cases[fda_col].dropna()
        aira_vals = successful_cases[aira_col].dropna()
        
        # Ensure same length
        min_len = min(len(fda_vals), len(aira_vals))
        fda_vals = fda_vals.iloc[:min_len]
        aira_vals = aira_vals.iloc[:min_len]
        
        # Bland-Altman calculations
        mean_vals = (fda_vals + aira_vals) / 2
        diff_vals = aira_vals - fda_vals
        
        mean_diff = np.mean(diff_vals)
        std_diff = np.std(diff_vals)
        
        # 95% limits of agreement
        upper_loa = mean_diff + 1.96 * std_diff
        lower_loa = mean_diff - 1.96 * std_diff
        
        # Scatter plot
        ax.scatter(mean_vals, diff_vals, alpha=0.7, s=60, edgecolors='black', linewidth=0.8, c='steelblue')
        
        # Mean difference line
        ax.axhline(mean_diff, color='red', linestyle='-', linewidth=2.5, 
                   label=f'Bias: {mean_diff:.2f} cm³')
        
        # Limits of agreement
        ax.axhline(upper_loa, color='red', linestyle='--', linewidth=2,
                   label=f'+1.96 SD: {upper_loa:.2f} cm³')
        ax.axhline(lower_loa, color='red', linestyle='--', linewidth=2,
                   label=f'-1.96 SD: {lower_loa:.2f} cm³')
        
        # Zero line
        ax.axhline(0, color='black', linestyle='-', linewidth=1.5, alpha=0.7, label='Perfect Agreement')
        
        ax.set_xlabel('Mean of FDA and AIRA Volumes (cm³)', fontsize=12, fontweight='bold')
        ax.set_ylabel('Difference: AIRA - FDA (cm³)', fontsize=12, fontweight='bold')
        ax.set_title(f'{kidney_name} Bland-Altman Analysis', fontsize=14, fontweight='bold', pad=20)
        ax.legend(fontsize=10, loc='best', frameon=True, fancybox=True, shadow=True)
        ax.grid(True, alpha=0.3)
        ax.tick_params(labelsize=10)
        
        # Add text with statistics in a better location
        textstr = f'n = {len(diff_vals)}\nBias = {mean_diff:.2f} cm³\nSD = {std_diff:.2f} cm³\n95% LoA: [{lower_loa:.2f}, {upper_loa:.2f}] cm³'
        props = dict(boxstyle='round', facecolor='lightblue', alpha=0.9, edgecolor='black')
        # Position text box to avoid overlap
        text_x = 0.02 if mean_diff > 0 else 0.98
        text_ha = 'left' if mean_diff > 0 else 'right'
        ax.text(text_x, 0.98, textstr, transform=ax.transAxes, fontsize=10,
                verticalalignment='top', horizontalalignment=text_ha, bbox=props)
    
    plt.tight_layout()
    
    if config.get('save_individual_plots', True):
        bland_file = os.path.join(results_dir, f'Bland_Altman_Plots_{timestamp}.png')
        plt.savefig(bland_file, dpi=config.get('plot_dpi', 300), bbox_inches='tight')
        plot_files.append(bland_file)
    
    plt.close()
    return plot_files

def create_correlation_plots(df, results_dir, timestamp, config):
    """Create correlation and scatter plots for volume comparison."""
    if not config.get('create_plots', False):
        return []
    
    successful_cases = df[df['Status'] == 'Success'] if 'Status' in df.columns else df
    
    if len(successful_cases) < 3:
        return []
    
    try:
        plt.style.use(config.get('plot_style', 'default'))
    except:
        pass
    
    plot_files = []
    
    # Volume comparison pairs
    volume_pairs = [
        ('FDA_Right_Kidney_Vol_cm3', 'AIRA_Right_Kidney_Vol_cm3', 'Right Kidney'),
        ('FDA_Left_Kidney_Vol_cm3', 'AIRA_Left_Kidney_Vol_cm3', 'Left Kidney')
    ]
    
    fig, axes = plt.subplots(1, 2, figsize=(16, 7))  # Larger figure
    fig.suptitle('Volume Correlation Analysis: FDA vs AIRA', fontsize=16, fontweight='bold', y=0.95)
    
    for idx, (fda_col, aira_col, kidney_name) in enumerate(volume_pairs):
        if fda_col not in successful_cases.columns or aira_col not in successful_cases.columns:
            continue
        
        ax = axes[idx]
        
        fda_vals = successful_cases[fda_col].dropna()
        aira_vals = successful_cases[aira_col].dropna()
        
        # Ensure same length
        min_len = min(len(fda_vals), len(aira_vals))
        fda_vals = fda_vals.iloc[:min_len]
        aira_vals = aira_vals.iloc[:min_len]
        
        # Scatter plot
        ax.scatter(fda_vals, aira_vals, alpha=0.7, s=80, edgecolors='black', linewidth=0.8, c='steelblue')
        
        # Perfect correlation line (y=x)
        min_val = min(min(fda_vals), min(aira_vals))
        max_val = max(max(fda_vals), max(aira_vals))
        ax.plot([min_val, max_val], [min_val, max_val], 'r--', linewidth=2.5, 
                alpha=0.8, label='Perfect Agreement (y=x)')
        
        # Regression line
        z = np.polyfit(fda_vals, aira_vals, 1)
        p = np.poly1d(z)
        sorted_fda = fda_vals.sort_values()
        ax.plot(sorted_fda, p(sorted_fda), "g-", linewidth=2.5, alpha=0.8,
                label=f'Best Fit (y={z[0]:.3f}x+{z[1]:.1f})')
        
        # Calculate metrics
        correlation = np.corrcoef(fda_vals, aira_vals)[0, 1]
        
        # Calculate R²
        ss_res = np.sum((aira_vals - p(fda_vals))**2)
        ss_tot = np.sum((aira_vals - np.mean(aira_vals))**2)
        r_squared = 1 - (ss_res / ss_tot) if ss_tot != 0 else 0
        
        ax.set_xlabel('FDA Ground Truth Volume (cm³)', fontsize=12, fontweight='bold')
        ax.set_ylabel('AIRA Predicted Volume (cm³)', fontsize=12, fontweight='bold')
        ax.set_title(f'{kidney_name} Volume Correlation', fontsize=14, fontweight='bold', pad=20)
        ax.legend(fontsize=11, loc='best', frameon=True, fancybox=True, shadow=True)
        ax.grid(True, alpha=0.3)
        ax.tick_params(labelsize=10)
        
        # Add statistics text with better formatting
        textstr = f'Pearson r = {correlation:.4f}\nR² = {r_squared:.4f}\nn = {len(fda_vals)} cases'
        props = dict(boxstyle='round', facecolor='lightyellow', alpha=0.9, edgecolor='black')
        ax.text(0.05, 0.95, textstr, transform=ax.transAxes, fontsize=11, fontweight='bold',
                verticalalignment='top', bbox=props)
    
    plt.tight_layout()
    
    if config.get('save_individual_plots', True):
        corr_file = os.path.join(results_dir, f'Correlation_Plots_{timestamp}.png')
        plt.savefig(corr_file, dpi=config.get('plot_dpi', 300), bbox_inches='tight')
        plot_files.append(corr_file)
    
    plt.close()
    return plot_files

def create_performance_summary_plot(df, results_dir, timestamp, config):
    """Create a comprehensive performance summary visualization."""
    if not config.get('create_plots', False):
        return []
    
    successful_cases = df[df['Status'] == 'Success'] if 'Status' in df.columns else df
    
    if len(successful_cases) < 3:
        return []
    
    try:
        plt.style.use(config.get('plot_style', 'default'))
    except:
        pass
    
    plot_files = []
    
    fig, axes = plt.subplots(2, 2, figsize=(16, 14))  # Larger figure with more height
    fig.suptitle('FDA vs AIRA: Comprehensive Performance Summary', fontsize=16, fontweight='bold', y=0.98)
    
    # 1. Dice Coefficient Distribution
    ax1 = axes[0, 0]
    dice_cols = ['Dice_Right_Kidney', 'Dice_Left_Kidney']
    dice_data = []
    dice_labels = []
    
    for col in dice_cols:
        if col in successful_cases.columns:
            dice_data.append(successful_cases[col].dropna())
            dice_labels.append(col.replace('Dice_', '').replace('_', ' '))
    
    if dice_data:
        bp1 = ax1.boxplot(dice_data, labels=dice_labels, patch_artist=True, 
                         boxprops=dict(facecolor='lightblue', alpha=0.7),
                         medianprops=dict(color='red', linewidth=2),
                         flierprops=dict(marker='o', markerfacecolor='red', alpha=0.5))
        ax1.set_ylabel('Dice Coefficient', fontsize=12, fontweight='bold')
        ax1.set_title('Dice Coefficient Distribution', fontsize=14, fontweight='bold', pad=15)
        ax1.grid(True, alpha=0.3)
        ax1.axhline(y=0.85, color='red', linestyle='--', linewidth=2, alpha=0.8, label='Clinical Threshold (0.85)')
        ax1.legend(fontsize=10)
        ax1.tick_params(labelsize=10)
    
    # 2. Volume Error Distribution
    ax2 = axes[0, 1]
    error_cols = ['Right_Kidney_Diff_%', 'Left_Kidney_Diff_%']
    error_data = []
    error_labels = []
    
    for col in error_cols:
        if col in successful_cases.columns:
            error_data.append(successful_cases[col].dropna())
            error_labels.append(col.replace('_Diff_%', '').replace('_', ' '))
    
    if error_data:
        ax2.boxplot(error_data, labels=error_labels, patch_artist=True,
                   boxprops=dict(facecolor='lightcoral', alpha=0.7))
        ax2.set_ylabel('Volume Error (%)')
        ax2.set_title('Volume Error Distribution')
        ax2.grid(True, alpha=0.3)
        ax2.axhline(y=0, color='black', linestyle='-', alpha=0.5)
        ax2.axhline(y=10, color='red', linestyle='--', alpha=0.7, label='±10% Threshold')
        ax2.axhline(y=-10, color='red', linestyle='--', alpha=0.7)
        ax2.legend()
    
    # 3. Case Success Overview
    ax3 = axes[1, 0]
    if 'Status' in df.columns:
        status_counts = df['Status'].value_counts()
        colors = ['lightgreen' if s == 'Success' else 'lightcoral' for s in status_counts.index]
        wedges, texts, autotexts = ax3.pie(status_counts.values, labels=status_counts.index, 
                                          autopct='%1.1f%%', colors=colors, startangle=90)
        ax3.set_title('Case Processing Success Rate')
    
    # 4. Clinical Agreement Summary
    ax4 = axes[1, 1]
    agreement_data = []
    agreement_labels = []
    
    # High Dice agreement (≥0.85)
    for dice_col in dice_cols:
        if dice_col in successful_cases.columns:
            high_dice = (successful_cases[dice_col] >= 0.85).sum()
            total_cases = len(successful_cases)
            agreement_data.append((high_dice / total_cases) * 100)
            kidney_name = dice_col.replace('Dice_', '').replace('_', ' ')
            agreement_labels.append(f'{kidney_name}\nDice ≥ 0.85')
    
    # Volume agreement (≤10% error)
    for error_col in error_cols:
        if error_col in successful_cases.columns:
            good_volume = (np.abs(successful_cases[error_col]) <= 10).sum()
            total_cases = len(successful_cases)
            agreement_data.append((good_volume / total_cases) * 100)
            kidney_name = error_col.replace('_Diff_%', '').replace('_', ' ')
            agreement_labels.append(f'{kidney_name}\n|Error| ≤ 10%')
    
    if agreement_data:
        bars = ax4.bar(agreement_labels, agreement_data, 
                      color=['lightblue', 'lightgreen', 'orange', 'pink'][:len(agreement_data)])
        ax4.set_ylabel('Agreement Rate (%)')
        ax4.set_title('Clinical Agreement Thresholds')
        ax4.set_ylim(0, 100)
        ax4.grid(True, alpha=0.3, axis='y')
        
        # Add value labels on bars
        for bar, value in zip(bars, agreement_data):
            ax4.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1,
                    f'{value:.1f}%', ha='center', va='bottom', fontweight='bold')
    
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])  # Add padding for suptitle
    
    if config.get('save_individual_plots', True):
        summary_file = os.path.join(results_dir, f'Performance_Summary_{timestamp}.png')
        plt.savefig(summary_file, dpi=config.get('plot_dpi', 300), bbox_inches='tight')
        plot_files.append(summary_file)
    
    plt.close()
    return plot_files

def create_all_visualizations(df, results_dir, timestamp, config):
    """Create all visualization plots and return list of created files."""
    if not config.get('create_plots', False):
        return []
    
    print("\nCreating visualization plots...")
    
    plot_files = []
    
    try:
        # Individual plot functions
        plot_files.extend(create_roc_curves(df, results_dir, timestamp, config))
        plot_files.extend(create_bland_altman_plots(df, results_dir, timestamp, config))
        plot_files.extend(create_correlation_plots(df, results_dir, timestamp, config))
        plot_files.extend(create_performance_summary_plot(df, results_dir, timestamp, config))
        
        print(f"✓ Created {len(plot_files)} visualization plots")
        
    except Exception as e:
        print(f"⚠ Warning: Could not create some plots. Reason: {e}")
        print("  Make sure matplotlib, seaborn, and scikit-learn are installed:")
        print("  pip install matplotlib seaborn scikit-learn")
    
    return plot_files

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
        class_names = ['Background', 'Right_Kidney', 'Left_Kidney']  # Index 0=Background, 1=Right, 2=Left
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
    
    # Create results directory with timestamp subdirectory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    base_results_dir = os.path.join(script_dir, 'results')
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    results_dir = os.path.join(base_results_dir, f'FDA_Analysis_{timestamp}')
    os.makedirs(results_dir, exist_ok=True)
    
    # Output files in timestamped subdirectory
    output_file = os.path.join(results_dir, f'FDA_AIRA_Results_{timestamp}.{CONFIG["save_format"]}')
    stats_file = os.path.join(results_dir, f'FDA_AIRA_Statistics_{timestamp}.csv')
    
    print("="*70)
    print("FDA vs AIRA - Multi-Case Analysis")
    print("="*70)
    print(f"Dataset directory: {base_dir}")
    print(f"Results directory: {os.path.relpath(results_dir)}")
    print(f"Analysis timestamp: {timestamp}")
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
    
    # Calculate comprehensive statistics
    if CONFIG['save_detailed_stats']:
        print("\nCalculating comprehensive statistics...")
        stats_df = calculate_comprehensive_statistics(df)
        if len(stats_df) > 0:
            stats_df.to_csv(stats_file, index=False)
            print(f"✓ Detailed statistics saved to: {os.path.basename(stats_file)}")
    
    # Create visualizations
    plot_files = create_all_visualizations(df, results_dir, timestamp, CONFIG)
    
    # Save based on format
    if CONFIG['save_format'] == 'csv':
        df.to_csv(output_file, index=False)
        print(f"\n✓ Results saved to: {os.path.basename(output_file)}")
    
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
        
        print(f"\n✓ Results saved to: {os.path.basename(output_file)}")
    
    # Print summary
    print("\n" + "="*70)
    print("SUMMARY")
    print("="*70)
    successful_cases = df[df['Status'] == 'Success'] if 'Status' in df.columns else df
    print(f"Total cases: {len(df)}")
    if 'Status' in df.columns:
        print(f"Successful: {len(successful_cases)}")
        print(f"Failed: {len(df[df['Status'] == 'Failed'])}")
        print(f"Success rate: {(len(successful_cases) / len(df)) * 100:.1f}%")
    
    if len(successful_cases) > 0:
        print("\nDICE COEFFICIENTS:")
        if 'Dice_Left_Kidney' in successful_cases.columns:
            left_dice = successful_cases['Dice_Left_Kidney']
            print(f"  Left Kidney:  {left_dice.mean():.4f} ± {left_dice.std():.4f} (range: {left_dice.min():.4f}-{left_dice.max():.4f})")
        if 'Dice_Right_Kidney' in successful_cases.columns:
            right_dice = successful_cases['Dice_Right_Kidney']
            print(f"  Right Kidney: {right_dice.mean():.4f} ± {right_dice.std():.4f} (range: {right_dice.min():.4f}-{right_dice.max():.4f})")
        
        # Overall dice
        if 'Dice_Left_Kidney' in successful_cases.columns and 'Dice_Right_Kidney' in successful_cases.columns:
            overall_dice = successful_cases[['Dice_Left_Kidney', 'Dice_Right_Kidney']].mean(axis=1)
            print(f"  Overall:      {overall_dice.mean():.4f} ± {overall_dice.std():.4f} (range: {overall_dice.min():.4f}-{overall_dice.max():.4f})")
        
        print("\nVOLUME ANALYSIS:")
        if 'FDA_Left_Kidney_Vol_cm3' in successful_cases.columns:
            fda_left = successful_cases['FDA_Left_Kidney_Vol_cm3']
            print(f"  FDA Left Kidney:  {fda_left.mean():.1f} ± {fda_left.std():.1f} cm³")
        if 'FDA_Right_Kidney_Vol_cm3' in successful_cases.columns:
            fda_right = successful_cases['FDA_Right_Kidney_Vol_cm3']
            print(f"  FDA Right Kidney: {fda_right.mean():.1f} ± {fda_right.std():.1f} cm³")
        if 'AIRA_Left_Kidney_Vol_cm3' in successful_cases.columns:
            aira_left = successful_cases['AIRA_Left_Kidney_Vol_cm3']
            print(f"  AIRA Left Kidney:  {aira_left.mean():.1f} ± {aira_left.std():.1f} cm³")
        if 'AIRA_Right_Kidney_Vol_cm3' in successful_cases.columns:
            aira_right = successful_cases['AIRA_Right_Kidney_Vol_cm3']
            print(f"  AIRA Right Kidney: {aira_right.mean():.1f} ± {aira_right.std():.1f} cm³")
        
        print("\nVOLUME DIFFERENCES (AIRA - FDA):")
        if 'Left_Kidney_Diff_cm3' in successful_cases.columns:
            left_diff = successful_cases['Left_Kidney_Diff_cm3']
            print(f"  Left Kidney:  {left_diff.mean():.2f} ± {left_diff.std():.2f} cm³", end='')
            if 'Left_Kidney_Diff_%' in successful_cases.columns:
                left_diff_perc = successful_cases['Left_Kidney_Diff_%']
                print(f" ({left_diff_perc.mean():.2f} ± {left_diff_perc.std():.2f}%)")
            else:
                print()
        if 'Right_Kidney_Diff_cm3' in successful_cases.columns:
            right_diff = successful_cases['Right_Kidney_Diff_cm3']
            print(f"  Right Kidney: {right_diff.mean():.2f} ± {right_diff.std():.2f} cm³", end='')
            if 'Right_Kidney_Diff_%' in successful_cases.columns:
                right_diff_perc = successful_cases['Right_Kidney_Diff_%']
                print(f" ({right_diff_perc.mean():.2f} ± {right_diff_perc.std():.2f}%)")
            else:
                print()
        
        print("\nCLINICAL AGREEMENT:")
        # High Dice threshold (≥0.85)
        if 'Dice_Left_Kidney' in successful_cases.columns:
            high_dice_left = (successful_cases['Dice_Left_Kidney'] >= 0.85).sum()
            print(f"  Left Kidney Dice ≥ 0.85: {high_dice_left}/{len(successful_cases)} ({(high_dice_left/len(successful_cases))*100:.1f}%)")
        if 'Dice_Right_Kidney' in successful_cases.columns:
            high_dice_right = (successful_cases['Dice_Right_Kidney'] >= 0.85).sum()
            print(f"  Right Kidney Dice ≥ 0.85: {high_dice_right}/{len(successful_cases)} ({(high_dice_right/len(successful_cases))*100:.1f}%)")
        
        # Volume agreement (≤10% difference)
        if 'Left_Kidney_Diff_%' in successful_cases.columns:
            good_vol_left = (np.abs(successful_cases['Left_Kidney_Diff_%']) <= 10).sum()
            print(f"  Left Kidney |Diff| ≤ 10%: {good_vol_left}/{len(successful_cases)} ({(good_vol_left/len(successful_cases))*100:.1f}%)")
        if 'Right_Kidney_Diff_%' in successful_cases.columns:
            good_vol_right = (np.abs(successful_cases['Right_Kidney_Diff_%']) <= 10).sum()
            print(f"  Right Kidney |Diff| ≤ 10%: {good_vol_right}/{len(successful_cases)} ({(good_vol_right/len(successful_cases))*100:.1f}%)")
        
        print("\nAI/ML REGRESSION METRICS:")
        # Calculate and display key ML metrics
        regression_pairs = [
            ('FDA_Left_Kidney_Vol_cm3', 'AIRA_Left_Kidney_Vol_cm3', 'Left Kidney'),
            ('FDA_Right_Kidney_Vol_cm3', 'AIRA_Right_Kidney_Vol_cm3', 'Right Kidney')
        ]
        
        for fda_col, aira_col, label in regression_pairs:
            if fda_col in successful_cases.columns and aira_col in successful_cases.columns:
                fda_vals = successful_cases[fda_col].dropna()
                aira_vals = successful_cases[aira_col].dropna()
                
                min_len = min(len(fda_vals), len(aira_vals))
                if min_len > 0:
                    fda_vals = fda_vals.iloc[:min_len]
                    aira_vals = aira_vals.iloc[:min_len]
                    
                    metrics = calculate_regression_metrics(fda_vals.values, aira_vals.values)
                    
                    mae = metrics.get('MAE', np.nan)
                    rmse = metrics.get('RMSE', np.nan)
                    mape = metrics.get('MAPE', np.nan)
                    r2 = metrics.get('R_squared', np.nan)
                    corr = metrics.get('Correlation', np.nan)
                    
                    print(f"  {label}:")
                    if not np.isnan(mae):
                        print(f"    MAE: {mae:.2f} cm³")
                    if not np.isnan(rmse):
                        print(f"    RMSE: {rmse:.2f} cm³")
                    if not np.isnan(mape):
                        print(f"    MAPE: {mape:.1f}%")
                    if not np.isnan(r2):
                        print(f"    R²: {r2:.4f}")
                    if not np.isnan(corr):
                        print(f"    Correlation: {corr:.4f}")
    
    print("="*70)
    print("GENERATED FILES")
    print("="*70)
    print(f"Results saved in: {os.path.relpath(results_dir)}")
    print(f"📊 Main Results: {os.path.basename(output_file)}")
    if CONFIG['save_detailed_stats']:
        print(f"📈 Statistics: {os.path.basename(stats_file)}")
    if plot_files:
        print(f"📉 Visualizations: {len(plot_files)} plots created")
        for plot_file in plot_files:
            print(f"   • {os.path.basename(plot_file)}")
    print("="*70)

if __name__ == "__main__":
    main()