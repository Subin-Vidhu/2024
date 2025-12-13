#!/usr/bin/env python3
"""
Compare AIRA vs FDA Annotators from CSV Data
============================================

This script compares AIRA volume predictions with FDA annotator volumes
using pre-calculated CSV data. It generates separate comparisons for:
- AIRA vs Annotator 1 (GT01)
- AIRA vs Annotator 2 (GT02)

The script includes:
- Volume comparisons (absolute and percentage differences)
- Inter-annotator agreement metrics from FDA CSV (Dice scores between GT01 and GT02)
- Comprehensive statistics and summary reports

Usage:
    python compare_aira_vs_annotators_from_csv.py

Author: Medical AI Validation Team
Date: 2025-11-07
"""

import os
import sys
import re
import numpy as np
import pandas as pd
from datetime import datetime
from scipy import stats

# ============================================================================
# CONFIGURATION
# ============================================================================

# Paths to CSV files
FDA_CSV_PATH = r'd:\2024\zTest\FDA_trial_cases\CSV_data\FDA-team-both-annotators.csv'
AIRA_CSV_PATH = r'd:\2024\zTest\FDA_trial_cases\CSV_data\AIRA_Volume_Values.csv'

# Output directory
OUTPUT_DIR = r'd:\2024\zTest\results\aira_vs_annotators_csv'

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def extract_case_id(mask_name):
    """
    Extract case ID from mask filename.
    Handles various formats: N-001, A-003, N-001_GT01.nii, etc.
    """
    if pd.isna(mask_name) or mask_name == '':
        return None
    
    # Remove file extension
    name = str(mask_name).replace('.nii', '').replace('.gz', '')
    
    # Extract case ID pattern (N-XXX or A-XXX)
    match = re.search(r'([NA]-\d+)', name)
    if match:
        return match.group(1)
    
    return None

def normalize_case_id(case_id):
    """Normalize case ID to standard format."""
    if pd.isna(case_id) or case_id == '':
        return None
    
    case_id = str(case_id).strip()
    # Ensure format is N-XXX or A-XXX
    match = re.search(r'([NA]-\d+)', case_id)
    if match:
        return match.group(1)
    
    return case_id

def calculate_volume_difference(true_vol, pred_vol):
    """Calculate absolute volume difference in cm³."""
    if pd.isna(true_vol) or pd.isna(pred_vol):
        return np.nan
    return pred_vol - true_vol

def calculate_volume_percentage_diff(true_vol, pred_vol, min_volume_threshold=0.1):
    """
    Calculate volume percentage difference.
    
    Formula: ((pred - true) / true) * 100
    """
    if pd.isna(true_vol) or pd.isna(pred_vol):
        return np.nan
    
    if true_vol < min_volume_threshold:
        if pred_vol < min_volume_threshold:
            return 0.0
        else:
            return np.nan  # Cannot calculate percentage for very small volumes
    
    return ((pred_vol - true_vol) / true_vol) * 100

def calculate_regression_metrics(y_true, y_pred):
    """Calculate comprehensive regression metrics."""
    # Remove NaN values
    mask = ~(np.isnan(y_true) | np.isnan(y_pred))
    y_true_clean = np.array(y_true)[mask]
    y_pred_clean = np.array(y_pred)[mask]
    
    if len(y_true_clean) == 0:
        return {}
    
    errors = y_pred_clean - y_true_clean
    abs_errors = np.abs(errors)
    
    metrics = {}
    metrics['MAE'] = np.mean(abs_errors)
    metrics['MSE'] = np.mean(errors**2)
    metrics['RMSE'] = np.sqrt(metrics['MSE'])
    metrics['MBE'] = np.mean(errors)  # Mean Bias Error
    
    # MAPE
    non_zero_mask = y_true_clean != 0
    if np.any(non_zero_mask):
        mape_values = np.abs(errors[non_zero_mask] / y_true_clean[non_zero_mask]) * 100
        metrics['MAPE'] = np.mean(mape_values)
    else:
        metrics['MAPE'] = np.nan
    
    # R-squared
    ss_res = np.sum(errors**2)
    ss_tot = np.sum((y_true_clean - np.mean(y_true_clean))**2)
    if ss_tot != 0:
        metrics['R_squared'] = 1 - (ss_res / ss_tot)
    else:
        metrics['R_squared'] = np.nan
    
    # Correlation
    if len(y_true_clean) > 1:
        correlation_matrix = np.corrcoef(y_true_clean, y_pred_clean)
        metrics['Correlation'] = correlation_matrix[0, 1] if not np.isnan(correlation_matrix[0, 1]) else 0
    else:
        metrics['Correlation'] = np.nan
    
    return metrics

def calculate_confidence_intervals(data, confidence=0.95):
    """Calculate confidence intervals."""
    data_clean = np.array(data)[~np.isnan(data)]
    if len(data_clean) < 2:
        return {'mean': np.nan, 'lower_ci': np.nan, 'upper_ci': np.nan, 'n': len(data_clean)}
    
    mean_val = np.mean(data_clean)
    sem = stats.sem(data_clean)
    alpha = 1 - confidence
    dof = len(data_clean) - 1
    t_critical = stats.t.ppf(1 - alpha/2, dof)
    margin_error = t_critical * sem
    
    return {
        'mean': mean_val,
        'lower_ci': mean_val - margin_error,
        'upper_ci': mean_val + margin_error,
        'n': len(data_clean)
    }

# ============================================================================
# CSV PARSING FUNCTIONS
# ============================================================================

def parse_fda_csv(fda_csv_path):
    """
    Parse FDA CSV and extract volumes for GT01 and GT02.
    
    Returns:
    --------
    dict: {
        case_id: {
            'gt01': {'right': vol, 'left': vol, 'right_mm3': vol, 'left_mm3': vol},
            'gt02': {'right': vol, 'left': vol, 'right_mm3': vol, 'left_mm3': vol},
            'inter_annotator_dice': {'right': dice, 'left': dice, 'average': dice},
            'inter_annotator_diff_percent': {'right': diff%, 'left': diff%}
        }
    }
    """
    print(f"Reading FDA CSV: {fda_csv_path}")
    df = pd.read_csv(fda_csv_path)
    
    fda_data = {}
    
    for idx, row in df.iterrows():
        # Skip empty rows or summary rows
        if pd.isna(row.get('Mask1')) or pd.isna(row.get('Organ')):
            continue
        
        organ = str(row['Organ']).strip()
        
        # Extract case ID from Mask1 (should be consistent)
        case_id = extract_case_id(row['Mask1'])
        if not case_id:
            continue
        
        # Normalize case ID
        case_id = normalize_case_id(case_id)
        
        # Initialize case data if not exists
        if case_id not in fda_data:
            fda_data[case_id] = {
                'gt01': {'right': None, 'left': None, 'right_mm3': None, 'left_mm3': None},
                'gt02': {'right': None, 'left': None, 'right_mm3': None, 'left_mm3': None},
                'inter_annotator_dice': {'right': None, 'left': None, 'average': None},
                'inter_annotator_diff_percent': {'right': None, 'left': None}
            }
        
        # Determine which mask is GT01 and which is GT02
        mask1_name = str(row['Mask1'])
        mask2_name = str(row['Mask2'])
        
        # Check which mask contains GT01
        is_gt01_first = 'GT01' in mask1_name or 'gt01' in mask1_name.lower()
        
        # Extract volumes (in mL which is cm³)
        vol1_mL = row.get('Mask1_Volume_mL')
        vol2_mL = row.get('Mask2_Volume_mL')
        vol1_mm3 = row.get('Mask1_Volume_mm3')
        vol2_mm3 = row.get('Mask2_Volume_mm3')
        
        # Extract Dice coefficient
        dice = row.get('DiceCoefficient')
        
        # Extract percentage difference
        diff_percent_str = str(row.get('DiffPercent', ''))
        diff_percent = None
        if diff_percent_str and diff_percent_str != 'nan' and diff_percent_str != '':
            try:
                diff_percent = float(diff_percent_str.replace('%', ''))
            except:
                pass
        
        # Process based on organ type
        if 'Right Kidney' in organ:
            if is_gt01_first:
                fda_data[case_id]['gt01']['right'] = vol1_mL
                fda_data[case_id]['gt01']['right_mm3'] = vol1_mm3
                fda_data[case_id]['gt02']['right'] = vol2_mL
                fda_data[case_id]['gt02']['right_mm3'] = vol2_mm3
            else:
                fda_data[case_id]['gt01']['right'] = vol2_mL
                fda_data[case_id]['gt01']['right_mm3'] = vol2_mm3
                fda_data[case_id]['gt02']['right'] = vol1_mL
                fda_data[case_id]['gt02']['right_mm3'] = vol1_mm3
            
            if not pd.isna(dice):
                fda_data[case_id]['inter_annotator_dice']['right'] = dice
            if diff_percent is not None:
                fda_data[case_id]['inter_annotator_diff_percent']['right'] = diff_percent
                
        elif 'Left Kidney' in organ:
            if is_gt01_first:
                fda_data[case_id]['gt01']['left'] = vol1_mL
                fda_data[case_id]['gt01']['left_mm3'] = vol1_mm3
                fda_data[case_id]['gt02']['left'] = vol2_mL
                fda_data[case_id]['gt02']['left_mm3'] = vol2_mm3
            else:
                fda_data[case_id]['gt01']['left'] = vol2_mL
                fda_data[case_id]['gt01']['left_mm3'] = vol2_mm3
                fda_data[case_id]['gt02']['left'] = vol1_mL
                fda_data[case_id]['gt02']['left_mm3'] = vol1_mm3
            
            if not pd.isna(dice):
                fda_data[case_id]['inter_annotator_dice']['left'] = dice
            if diff_percent is not None:
                fda_data[case_id]['inter_annotator_diff_percent']['left'] = diff_percent
                
        elif 'Average' in organ:
            if not pd.isna(dice):
                fda_data[case_id]['inter_annotator_dice']['average'] = dice
    
    print(f"✓ Parsed {len(fda_data)} cases from FDA CSV")
    return fda_data

def parse_aira_csv(aira_csv_path):
    """
    Parse AIRA CSV and extract volumes.
    
    Returns:
    --------
    dict: {
        case_id: {'right': vol, 'left': vol}
    }
    """
    print(f"Reading AIRA CSV: {aira_csv_path}")
    df = pd.read_csv(aira_csv_path)
    
    aira_data = {}
    
    for idx, row in df.iterrows():
        case_id = normalize_case_id(row.get('Name'))
        if not case_id:
            continue
        
        right_vol = row.get('Right Kidney Volume')
        left_vol = row.get('Left Kidney Volume')
        
        aira_data[case_id] = {
            'right': right_vol,
            'left': left_vol
        }
    
    print(f"✓ Parsed {len(aira_data)} cases from AIRA CSV")
    return aira_data

# ============================================================================
# COMPARISON FUNCTIONS
# ============================================================================

def create_comparison_dataframe(aira_data, fda_data, annotator='gt01'):
    """
    Create comparison DataFrame for AIRA vs specified annotator.
    
    Parameters:
    -----------
    aira_data : dict
        AIRA volume data
    fda_data : dict
        FDA annotator data
    annotator : str
        'gt01' or 'gt02'
    
    Returns:
    --------
    pd.DataFrame: Comparison results
    """
    comparison_rows = []
    
    # Get all unique case IDs
    all_case_ids = set(aira_data.keys()) | set(fda_data.keys())
    
    for case_id in sorted(all_case_ids):
        aira_vols = aira_data.get(case_id, {})
        fda_vols = fda_data.get(case_id, {}).get(annotator, {})
        inter_metrics = fda_data.get(case_id, {}).get('inter_annotator_dice', {})
        inter_diff = fda_data.get(case_id, {}).get('inter_annotator_diff_percent', {})
        
        # Right Kidney
        aira_right = aira_vols.get('right')
        fda_right = fda_vols.get('right')
        
        right_diff = calculate_volume_difference(fda_right, aira_right) if (fda_right is not None and aira_right is not None) else np.nan
        right_diff_percent = calculate_volume_percentage_diff(fda_right, aira_right) if (fda_right is not None and aira_right is not None) else np.nan
        
        # Left Kidney
        aira_left = aira_vols.get('left')
        fda_left = fda_vols.get('left')
        
        left_diff = calculate_volume_difference(fda_left, aira_left) if (fda_left is not None and aira_left is not None) else np.nan
        left_diff_percent = calculate_volume_percentage_diff(fda_left, aira_left) if (fda_left is not None and aira_left is not None) else np.nan
        
        # Both Kidneys
        aira_total = (aira_right if aira_right is not None else 0) + (aira_left if aira_left is not None else 0)
        fda_total = (fda_right if fda_right is not None else 0) + (fda_left if fda_left is not None else 0)
        total_diff = aira_total - fda_total if (fda_total > 0 or aira_total > 0) else np.nan
        total_diff_percent = calculate_volume_percentage_diff(fda_total, aira_total) if fda_total > 0 else np.nan
        
        row = {
            'Case_ID': case_id,
            'AIRA_Right_Kidney_Vol_cm3': round(aira_right, 2) if aira_right is not None else '',
            'FDA_Right_Kidney_Vol_cm3': round(fda_right, 2) if fda_right is not None else '',
            'Right_Kidney_Diff_cm3': round(right_diff, 2) if not np.isnan(right_diff) else '',
            'Right_Kidney_Diff_%': round(right_diff_percent, 2) if not np.isnan(right_diff_percent) else '',
            'AIRA_Left_Kidney_Vol_cm3': round(aira_left, 2) if aira_left is not None else '',
            'FDA_Left_Kidney_Vol_cm3': round(fda_left, 2) if fda_left is not None else '',
            'Left_Kidney_Diff_cm3': round(left_diff, 2) if not np.isnan(left_diff) else '',
            'Left_Kidney_Diff_%': round(left_diff_percent, 2) if not np.isnan(left_diff_percent) else '',
            'AIRA_Total_Kidney_Vol_cm3': round(aira_total, 2) if aira_total > 0 else '',
            'FDA_Total_Kidney_Vol_cm3': round(fda_total, 2) if fda_total > 0 else '',
            'Total_Kidney_Diff_cm3': round(total_diff, 2) if not np.isnan(total_diff) else '',
            'Total_Kidney_Diff_%': round(total_diff_percent, 2) if not np.isnan(total_diff_percent) else '',
            # Inter-annotator metrics (GT01 vs GT02)
            'Inter_Annotator_Dice_Right': round(inter_metrics.get('right'), 6) if inter_metrics.get('right') is not None else '',
            'Inter_Annotator_Dice_Left': round(inter_metrics.get('left'), 6) if inter_metrics.get('left') is not None else '',
            'Inter_Annotator_Dice_Average': round(inter_metrics.get('average'), 6) if inter_metrics.get('average') is not None else '',
            'Inter_Annotator_Diff_%_Right': round(inter_diff.get('right'), 2) if inter_diff.get('right') is not None else '',
            'Inter_Annotator_Diff_%_Left': round(inter_diff.get('left'), 2) if inter_diff.get('left') is not None else '',
        }
        
        comparison_rows.append(row)
    
    df = pd.DataFrame(comparison_rows)
    return df

def create_summary_statistics(df, annotator_name):
    """Create summary statistics DataFrame."""
    stats_rows = []
    
    # Filter rows with valid data
    valid_df = df[
        (df['AIRA_Right_Kidney_Vol_cm3'] != '') & 
        (df['FDA_Right_Kidney_Vol_cm3'] != '')
    ].copy()
    
    if len(valid_df) == 0:
        return pd.DataFrame()
    
    # Convert to numeric
    numeric_cols = [
        'AIRA_Right_Kidney_Vol_cm3', 'FDA_Right_Kidney_Vol_cm3', 'Right_Kidney_Diff_cm3', 'Right_Kidney_Diff_%',
        'AIRA_Left_Kidney_Vol_cm3', 'FDA_Left_Kidney_Vol_cm3', 'Left_Kidney_Diff_cm3', 'Left_Kidney_Diff_%',
        'AIRA_Total_Kidney_Vol_cm3', 'FDA_Total_Kidney_Vol_cm3', 'Total_Kidney_Diff_cm3', 'Total_Kidney_Diff_%'
    ]
    
    for col in numeric_cols:
        valid_df[col] = pd.to_numeric(valid_df[col], errors='coerce')
    
    stats_rows.append(['SUMMARY STATISTICS', '', '', ''])
    stats_rows.append(['Metric', 'Right Kidney', 'Left Kidney', 'Both Kidneys'])
    stats_rows.append(['', '', '', ''])
    
    # Volume Statistics
    stats_rows.append(['VOLUME STATISTICS (cm³)', '', '', ''])
    
    # Right Kidney
    right_aira = valid_df['AIRA_Right_Kidney_Vol_cm3'].dropna()
    right_fda = valid_df['FDA_Right_Kidney_Vol_cm3'].dropna()
    right_diff = valid_df['Right_Kidney_Diff_cm3'].dropna()
    right_diff_pct = valid_df['Right_Kidney_Diff_%'].dropna()
    
    stats_rows.append(['Mean AIRA Volume', f"{right_aira.mean():.2f}", 
                      f"{valid_df['AIRA_Left_Kidney_Vol_cm3'].dropna().mean():.2f}",
                      f"{valid_df['AIRA_Total_Kidney_Vol_cm3'].dropna().mean():.2f}"])
    stats_rows.append(['Mean FDA Volume', f"{right_fda.mean():.2f}",
                      f"{valid_df['FDA_Left_Kidney_Vol_cm3'].dropna().mean():.2f}",
                      f"{valid_df['FDA_Total_Kidney_Vol_cm3'].dropna().mean():.2f}"])
    stats_rows.append(['Mean Difference', f"{right_diff.mean():.2f}",
                      f"{valid_df['Left_Kidney_Diff_cm3'].dropna().mean():.2f}",
                      f"{valid_df['Total_Kidney_Diff_cm3'].dropna().mean():.2f}"])
    stats_rows.append(['Mean Diff %', f"{right_diff_pct.mean():.2f}%",
                      f"{valid_df['Left_Kidney_Diff_%'].dropna().mean():.2f}%",
                      f"{valid_df['Total_Kidney_Diff_%'].dropna().mean():.2f}%"])
    stats_rows.append(['Std Dev Diff', f"{right_diff.std():.2f}",
                      f"{valid_df['Left_Kidney_Diff_cm3'].dropna().std():.2f}",
                      f"{valid_df['Total_Kidney_Diff_cm3'].dropna().std():.2f}"])
    stats_rows.append(['', '', '', ''])
    
    # Regression Metrics
    stats_rows.append(['REGRESSION METRICS', '', '', ''])
    
    # Right Kidney
    right_metrics = calculate_regression_metrics(right_fda, right_aira)
    left_metrics = calculate_regression_metrics(
        valid_df['FDA_Left_Kidney_Vol_cm3'].dropna(),
        valid_df['AIRA_Left_Kidney_Vol_cm3'].dropna()
    )
    total_metrics = calculate_regression_metrics(
        valid_df['FDA_Total_Kidney_Vol_cm3'].dropna(),
        valid_df['AIRA_Total_Kidney_Vol_cm3'].dropna()
    )
    
    metric_names = ['MAE (cm³)', 'RMSE (cm³)', 'MAPE (%)', 'R²', 'Correlation', 'MBE (cm³)']
    metric_keys = ['MAE', 'RMSE', 'MAPE', 'R_squared', 'Correlation', 'MBE']
    
    for name, key in zip(metric_names, metric_keys):
        right_val = right_metrics.get(key, np.nan)
        left_val = left_metrics.get(key, np.nan)
        total_val = total_metrics.get(key, np.nan)
        
        right_str = f"{right_val:.4f}" if not np.isnan(right_val) else "N/A"
        left_str = f"{left_val:.4f}" if not np.isnan(left_val) else "N/A"
        total_str = f"{total_val:.4f}" if not np.isnan(total_val) else "N/A"
        
        stats_rows.append([name, right_str, left_str, total_str])
    
    stats_rows.append(['', '', '', ''])
    
    # Agreement Analysis
    stats_rows.append(['CLINICAL AGREEMENT', '', '', ''])
    
    # Volume agreement (≤10% difference)
    right_agreement = (np.abs(right_diff_pct) <= 10).sum()
    left_agreement = (np.abs(valid_df['Left_Kidney_Diff_%'].dropna()) <= 10).sum()
    total_agreement = (np.abs(valid_df['Total_Kidney_Diff_%'].dropna()) <= 10).sum()
    
    right_rate = (right_agreement / len(right_diff_pct)) * 100 if len(right_diff_pct) > 0 else 0
    left_rate = (left_agreement / len(valid_df['Left_Kidney_Diff_%'].dropna())) * 100 if len(valid_df['Left_Kidney_Diff_%'].dropna()) > 0 else 0
    total_rate = (total_agreement / len(valid_df['Total_Kidney_Diff_%'].dropna())) * 100 if len(valid_df['Total_Kidney_Diff_%'].dropna()) > 0 else 0
    
    stats_rows.append(['|Diff| ≤ 10%', f"{right_agreement}/{len(right_diff_pct)} ({right_rate:.1f}%)",
                      f"{left_agreement}/{len(valid_df['Left_Kidney_Diff_%'].dropna())} ({left_rate:.1f}%)",
                      f"{total_agreement}/{len(valid_df['Total_Kidney_Diff_%'].dropna())} ({total_rate:.1f}%)"])
    
    stats_rows.append(['', '', '', ''])
    
    # Inter-Annotator Metrics Summary
    inter_dice_right = valid_df['Inter_Annotator_Dice_Right'].dropna()
    inter_dice_left = valid_df['Inter_Annotator_Dice_Left'].dropna()
    inter_dice_avg = valid_df['Inter_Annotator_Dice_Average'].dropna()
    
    if len(inter_dice_right) > 0:
        stats_rows.append(['INTER-ANNOTATOR AGREEMENT (GT01 vs GT02)', '', '', ''])
        stats_rows.append(['Mean Dice - Right', f"{inter_dice_right.mean():.6f}", '', ''])
        stats_rows.append(['Mean Dice - Left', '', f"{inter_dice_left.mean():.6f}", ''])
        stats_rows.append(['Mean Dice - Average', '', '', f"{inter_dice_avg.mean():.6f}"])
        stats_rows.append(['', '', '', ''])
    
    # Confidence Intervals
    stats_rows.append(['95% CONFIDENCE INTERVALS', '', '', ''])
    
    right_ci = calculate_confidence_intervals(right_diff_pct)
    left_ci = calculate_confidence_intervals(valid_df['Left_Kidney_Diff_%'].dropna())
    total_ci = calculate_confidence_intervals(valid_df['Total_Kidney_Diff_%'].dropna())
    
    if not np.isnan(right_ci['mean']):
        stats_rows.append(['Diff % CI - Right', 
                          f"[{right_ci['lower_ci']:.2f}, {right_ci['upper_ci']:.2f}]%", '', ''])
    if not np.isnan(left_ci['mean']):
        stats_rows.append(['Diff % CI - Left', '', 
                          f"[{left_ci['lower_ci']:.2f}, {left_ci['upper_ci']:.2f}]%", ''])
    if not np.isnan(total_ci['mean']):
        stats_rows.append(['Diff % CI - Total', '', '', 
                          f"[{total_ci['lower_ci']:.2f}, {total_ci['upper_ci']:.2f}]%"])
    
    stats_df = pd.DataFrame(stats_rows, columns=['Metric', 'Right Kidney', 'Left Kidney', 'Both Kidneys'])
    return stats_df

# ============================================================================
# MAIN PROCESSING
# ============================================================================

def main():
    """Main processing function."""
    print("=" * 80)
    print("AIRA vs FDA ANNOTATORS COMPARISON (FROM CSV DATA)")
    print("=" * 80)
    print(f"FDA CSV: {FDA_CSV_PATH}")
    print(f"AIRA CSV: {AIRA_CSV_PATH}")
    print(f"Output Directory: {OUTPUT_DIR}")
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)
    
    # Create output directory
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # Parse CSV files
    print("\n📂 Parsing CSV files...")
    fda_data = parse_fda_csv(FDA_CSV_PATH)
    aira_data = parse_aira_csv(AIRA_CSV_PATH)
    
    # Find matching cases
    matching_cases = set(aira_data.keys()) & set(fda_data.keys())
    print(f"\n✓ Found {len(matching_cases)} matching cases")
    
    if len(matching_cases) == 0:
        print("❌ ERROR: No matching cases found between AIRA and FDA CSVs!")
        print("   Please check case ID formats in both files.")
        return
    
    # Create comparisons
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    print("\n" + "=" * 80)
    print("GENERATING COMPARISONS")
    print("=" * 80)
    
    # AIRA vs GT01
    print("\n📊 Creating AIRA vs GT01 comparison...")
    df_gt01 = create_comparison_dataframe(aira_data, fda_data, annotator='gt01')
    stats_gt01 = create_summary_statistics(df_gt01, 'GT01')
    
    gt01_output = os.path.join(OUTPUT_DIR, f'AIRA_vs_GT01_{timestamp}.csv')
    gt01_stats_output = os.path.join(OUTPUT_DIR, f'AIRA_vs_GT01_Statistics_{timestamp}.csv')
    
    df_gt01.to_csv(gt01_output, index=False)
    stats_gt01.to_csv(gt01_stats_output, index=False)
    
    print(f"✓ Saved: {os.path.basename(gt01_output)}")
    print(f"✓ Saved: {os.path.basename(gt01_stats_output)}")
    
    # AIRA vs GT02
    print("\n📊 Creating AIRA vs GT02 comparison...")
    df_gt02 = create_comparison_dataframe(aira_data, fda_data, annotator='gt02')
    stats_gt02 = create_summary_statistics(df_gt02, 'GT02')
    
    gt02_output = os.path.join(OUTPUT_DIR, f'AIRA_vs_GT02_{timestamp}.csv')
    gt02_stats_output = os.path.join(OUTPUT_DIR, f'AIRA_vs_GT02_Statistics_{timestamp}.csv')
    
    df_gt02.to_csv(gt02_output, index=False)
    stats_gt02.to_csv(gt02_stats_output, index=False)
    
    print(f"✓ Saved: {os.path.basename(gt02_output)}")
    print(f"✓ Saved: {os.path.basename(gt02_stats_output)}")
    
    # Print summary
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"Total matching cases: {len(matching_cases)}")
    print(f"\n📁 Output files saved to: {OUTPUT_DIR}")
    print(f"   • AIRA_vs_GT01_{timestamp}.csv")
    print(f"   • AIRA_vs_GT01_Statistics_{timestamp}.csv")
    print(f"   • AIRA_vs_GT02_{timestamp}.csv")
    print(f"   • AIRA_vs_GT02_Statistics_{timestamp}.csv")
    print("=" * 80)
    
    # Print quick statistics
    print("\n📈 QUICK STATISTICS")
    print("-" * 80)
    
    # GT01 comparison
    valid_gt01 = df_gt01[
        (df_gt01['AIRA_Right_Kidney_Vol_cm3'] != '') & 
        (df_gt01['FDA_Right_Kidney_Vol_cm3'] != '')
    ].copy()
    
    if len(valid_gt01) > 0:
        for col in ['Right_Kidney_Diff_%', 'Left_Kidney_Diff_%']:
            valid_gt01[col] = pd.to_numeric(valid_gt01[col], errors='coerce')
        
        print("\nAIRA vs GT01:")
        print(f"  Right Kidney Mean Diff: {valid_gt01['Right_Kidney_Diff_%'].mean():.2f}%")
        print(f"  Left Kidney Mean Diff:  {valid_gt01['Left_Kidney_Diff_%'].mean():.2f}%")
    
    # GT02 comparison
    valid_gt02 = df_gt02[
        (df_gt02['AIRA_Right_Kidney_Vol_cm3'] != '') & 
        (df_gt02['FDA_Right_Kidney_Vol_cm3'] != '')
    ].copy()
    
    if len(valid_gt02) > 0:
        for col in ['Right_Kidney_Diff_%', 'Left_Kidney_Diff_%']:
            valid_gt02[col] = pd.to_numeric(valid_gt02[col], errors='coerce')
        
        print("\nAIRA vs GT02:")
        print(f"  Right Kidney Mean Diff: {valid_gt02['Right_Kidney_Diff_%'].mean():.2f}%")
        print(f"  Left Kidney Mean Diff:  {valid_gt02['Left_Kidney_Diff_%'].mean():.2f}%")
    
    print("\n✅ Processing complete!")
    print("=" * 80)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n❌ FATAL ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

