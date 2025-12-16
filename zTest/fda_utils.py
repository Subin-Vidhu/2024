"""
FDA Ground Truth Utilities
===========================

Shared utilities for FDA ground truth analysis scripts.
Ensures consistent case ID extraction and data handling across all scripts.
"""

import re
import pandas as pd
import numpy as np


def extract_case_from_filename(filename):
    """
    Extract case ID from filename (most reliable method).
    
    Handles both A-prefix (abnormal) and N-prefix (normal) cases.
    
    Examples:
        'N-001-GT01.nii' -> 'N-001'
        'A-005-GT02.nii' -> 'A-005'
        'N-227 GT01.nii' -> 'N-227'
    
    Parameters:
    -----------
    filename : str or pd.NA
        Filename to extract case ID from
    
    Returns:
    --------
    str or None : Case ID in format 'X-###' (uppercase), or None if not found
    """
    if pd.isna(filename):
        return None
    match = re.search(r'([AN]-\d+)', str(filename), re.IGNORECASE)
    if match:
        return match.group(1).upper()
    return None


def parse_diffpercent(val):
    """
    Parse DiffPercent value from various formats.
    
    Handles:
        - String percentages: "5.23%" -> 5.23
        - Numeric values: 5.23 -> 5.23
        - NaN/None -> np.nan
    
    Parameters:
    -----------
    val : str, float, or None
        DiffPercent value to parse
    
    Returns:
    --------
    float : Numeric percentage value or np.nan
    """
    if pd.isna(val):
        return np.nan
    if isinstance(val, str):
        return float(val.strip('%'))
    return float(val)


def validate_dice_match(dice_ours, dice_fda, tolerance=1e-6):
    """
    Check if two Dice coefficient values match within tolerance.
    
    Parameters:
    -----------
    dice_ours : array-like
        Our calculated Dice values
    dice_fda : array-like
        FDA reference Dice values
    tolerance : float
        Absolute tolerance for comparison (default: 1e-6)
    
    Returns:
    --------
    np.ndarray : Boolean array of matches
    """
    return np.isclose(dice_ours, dice_fda, atol=tolerance)


def validate_diffpercent_match(diff_ours, diff_fda, tolerance=0.01):
    """
    Check if two DiffPercent values match within tolerance.
    
    Parameters:
    -----------
    diff_ours : array-like
        Our calculated DiffPercent values
    diff_fda : array-like
        FDA reference DiffPercent values
    tolerance : float
        Absolute tolerance for percentage comparison (default: 0.01%)
    
    Returns:
    --------
    np.ndarray : Boolean array of matches
    """
    return np.isclose(diff_ours, diff_fda, atol=tolerance)


def load_and_prepare_kidney_data(csv_path, case_id_source='filename'):
    """
    Load CSV and prepare kidney measurement data with case IDs.
    
    Parameters:
    -----------
    csv_path : str
        Path to CSV file
    case_id_source : str
        Method to extract case ID:
        - 'filename': Extract from GT01_File/Mask1 (recommended)
        - 'patient': Use Patient column directly
    
    Returns:
    --------
    pd.DataFrame : Prepared dataframe with CaseID column
    """
    df = pd.read_csv(csv_path)
    kidney_df = df[df['Organ'].str.contains('Kidney', na=False)].copy()
    
    if case_id_source == 'filename':
        # Try GT01_File first, then Mask1
        if 'GT01_File' in kidney_df.columns:
            kidney_df['CaseID'] = kidney_df['GT01_File'].apply(extract_case_from_filename)
        elif 'Mask1' in kidney_df.columns:
            kidney_df['CaseID'] = kidney_df['Mask1'].apply(extract_case_from_filename)
            # Fallback to Mask2 if Mask1 didn't have it
            kidney_df.loc[kidney_df['CaseID'].isna(), 'CaseID'] = \
                kidney_df.loc[kidney_df['CaseID'].isna(), 'Mask2'].apply(extract_case_from_filename)
    else:
        kidney_df['CaseID'] = kidney_df['Patient']
    
    return kidney_df


def load_and_prepare_average_data(csv_path, case_id_source='filename'):
    """
    Load CSV and prepare average Dice data with case IDs.
    
    Parameters:
    -----------
    csv_path : str
        Path to CSV file
    case_id_source : str
        Method to extract case ID ('filename' or 'patient')
    
    Returns:
    --------
    pd.DataFrame : Prepared dataframe with CaseID column
    """
    df = pd.read_csv(csv_path)
    avg_df = df[df['Organ'].str.contains('Average', na=False)].copy()
    
    if case_id_source == 'filename':
        if 'GT01_File' in avg_df.columns:
            avg_df['CaseID'] = avg_df['GT01_File'].apply(extract_case_from_filename)
        elif 'Mask1' in avg_df.columns:
            avg_df['CaseID'] = avg_df['Mask1'].apply(extract_case_from_filename)
            avg_df.loc[avg_df['CaseID'].isna(), 'CaseID'] = \
                avg_df.loc[avg_df['CaseID'].isna(), 'Mask2'].apply(extract_case_from_filename)
    else:
        avg_df['CaseID'] = avg_df['Patient']
    
    return avg_df


def print_validation_summary(dice_matches, diff_matches, avg_matches, 
                            dice_total, diff_total, avg_total, common_cases):
    """
    Print formatted validation summary.
    
    Parameters:
    -----------
    dice_matches : int
        Number of Dice coefficient matches
    diff_matches : int
        Number of DiffPercent matches
    avg_matches : int
        Number of Average matches
    dice_total : int
        Total Dice measurements
    diff_total : int
        Total DiffPercent measurements
    avg_total : int
        Total Average measurements
    common_cases : int
        Number of cases validated
    """
    print("\n" + "=" * 90)
    print("FINAL SUMMARY")
    print("=" * 90)
    
    all_perfect = (
        dice_matches == dice_total and
        diff_matches == diff_total and
        avg_matches == avg_total
    )
    
    if all_perfect:
        print("\n" + "🎉" * 30)
        print("\n✅ SUCCESS! ALL FORMULAS MATCH FDA 100%!")
        print("\n" + "✅" * 30)
        print(f"\n   • Dice Coefficient:  {dice_matches}/{dice_total} measurements")
        print(f"   • DiffPercent:       {diff_matches}/{diff_total} measurements")
        print(f"   • Average:           {avg_matches}/{avg_total} cases")
        print(f"\n   Validated across {common_cases} cases")
        print("\n✅ CODE IS PRODUCTION-READY!")
        print("\n" + "🎉" * 30)
    else:
        print(f"\n   • Dice Coefficient: {dice_matches}/{dice_total} {'✅' if dice_matches == dice_total else '❌'}")
        print(f"   • DiffPercent: {diff_matches}/{diff_total} {'✅' if diff_matches == diff_total else '❌'}")
        print(f"   • Average: {avg_matches}/{avg_total} {'✅' if avg_matches == avg_total else '❌'}")
    
    print("\n" + "=" * 90 + "\n")
