"""
DICE Score Comparison Tool
===========================
This script compares DICE coefficient values between:
1. WCG team's CSV file (66017_WCG_DICE_16Dec2025.csv)
2. AIRA vs GT01 predictions (AIRA_vs_GT01.csv)
3. AIRA vs GT02 predictions (AIRA_vs_GT02.csv)

The WCG file contains comparisons with either GT01 or GT02 for each patient-organ pair.
This script identifies which GT version was used and compares with the corresponding AIRA file.

Author: Generated for FDA Trial 119 Analysis
Date: December 19, 2025
"""

import pandas as pd
import numpy as np
import re
from pathlib import Path
from typing import Tuple, Dict, List
import sys


class DiceScoreComparator:
    """Compare DICE scores across different CSV files with intelligent matching."""
    
    def __init__(self, wcg_file: str, aira_gt01_file: str, aira_gt02_file: str, 
                 tolerance: float = 0.000001):
        """
        Initialize the comparator with file paths.
        
        Args:
            wcg_file: Path to WCG team's DICE CSV file
            aira_gt01_file: Path to AIRA vs GT01 predictions
            aira_gt02_file: Path to AIRA vs GT02 predictions
            tolerance: Tolerance for floating point comparison (default: 0.000001)
        """
        self.wcg_file = wcg_file
        self.aira_gt01_file = aira_gt01_file
        self.aira_gt02_file = aira_gt02_file
        self.tolerance = tolerance
        
        # Storage for loaded data
        self.wcg_df = None
        self.aira_gt01_df = None
        self.aira_gt02_df = None
        
        # Results storage
        self.matches = []
        self.mismatches = []
        self.missing_in_wcg = []
        self.missing_in_aira = []
        self.errors = []
        
    def normalize_patient_id(self, patient_id: str) -> str:
        """
        Normalize patient ID by removing extra spaces and standardizing format.
        
        Args:
            patient_id: Raw patient ID string
            
        Returns:
            Normalized patient ID
        """
        if pd.isna(patient_id):
            return ""
        return str(patient_id).strip()
    
    def normalize_organ_name(self, organ: str) -> str:
        """
        Normalize organ name for consistent matching.
        
        Args:
            organ: Raw organ name
            
        Returns:
            Normalized organ name
        """
        if pd.isna(organ):
            return ""
        return str(organ).strip().lower()
    
    def extract_gt_version(self, mask_file: str) -> str:
        """
        Extract GT version (GT01 or GT02) from mask filename.
        
        Args:
            mask_file: Filename of the GT mask
            
        Returns:
            'GT01', 'GT02', or 'UNKNOWN'
        """
        if pd.isna(mask_file):
            return 'UNKNOWN'
        
        mask_str = str(mask_file).upper()
        
        # Check for GT01 pattern
        if 'GT01' in mask_str or 'GT_01' in mask_str or 'GT 01' in mask_str:
            return 'GT01'
        # Check for GT02 pattern
        elif 'GT02' in mask_str or 'GT_02' in mask_str or 'GT 02' in mask_str:
            return 'GT02'
        else:
            return 'UNKNOWN'
    
    def load_data(self):
        """Load all CSV files and perform initial preprocessing."""
        print("Loading CSV files...")
        
        try:
            # Load WCG file
            self.wcg_df = pd.read_csv(self.wcg_file)
            print(f"  ✓ Loaded WCG file: {len(self.wcg_df)} rows")
            
            # Load AIRA files
            self.aira_gt01_df = pd.read_csv(self.aira_gt01_file)
            print(f"  ✓ Loaded AIRA vs GT01: {len(self.aira_gt01_df)} rows")
            
            self.aira_gt02_df = pd.read_csv(self.aira_gt02_file)
            print(f"  ✓ Loaded AIRA vs GT02: {len(self.aira_gt02_df)} rows")
            
            # Normalize patient IDs and organ names
            self._normalize_dataframes()
            
            # Add GT version to WCG dataframe
            self.wcg_df['GT_Version'] = self.wcg_df['Mask2'].apply(self.extract_gt_version)
            
            print("\nData loaded and preprocessed successfully!")
            return True
            
        except Exception as e:
            print(f"✗ Error loading files: {e}")
            self.errors.append(f"File loading error: {e}")
            return False
    
    def _normalize_dataframes(self):
        """Normalize patient IDs and organ names in all dataframes."""
        # WCG normalization
        self.wcg_df['Patient_Normalized'] = self.wcg_df['Patient'].apply(
            self.normalize_patient_id
        )
        self.wcg_df['Organ_Normalized'] = self.wcg_df['Organ'].apply(
            self.normalize_organ_name
        )
        
        # AIRA GT01 normalization
        self.aira_gt01_df['Patient_Normalized'] = self.aira_gt01_df['Patient'].apply(
            self.normalize_patient_id
        )
        self.aira_gt01_df['Organ_Normalized'] = self.aira_gt01_df['Organ'].apply(
            self.normalize_organ_name
        )
        
        # AIRA GT02 normalization
        self.aira_gt02_df['Patient_Normalized'] = self.aira_gt02_df['Patient'].apply(
            self.normalize_patient_id
        )
        self.aira_gt02_df['Organ_Normalized'] = self.aira_gt02_df['Organ'].apply(
            self.normalize_organ_name
        )
    
    def filter_average_rows(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Filter out average rows (e.g., 'A-003 Average') from dataframe.
        
        Args:
            df: DataFrame to filter
            
        Returns:
            Filtered DataFrame
        """
        return df[~df['Organ_Normalized'].str.contains('average', na=False)]
    
    def filter_error_rows(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Filter out error rows from dataframe.
        
        Args:
            df: DataFrame to filter
            
        Returns:
            Filtered DataFrame
        """
        return df[df['Organ_Normalized'] != 'error']
    
    def compare_dice_values(self, wcg_value: float, aira_value: float) -> Tuple[bool, float]:
        """
        Compare two DICE coefficient values within tolerance.
        
        Args:
            wcg_value: DICE value from WCG file
            aira_value: DICE value from AIRA file
            
        Returns:
            Tuple of (match_result, difference)
        """
        if pd.isna(wcg_value) or pd.isna(aira_value):
            return False, np.nan
        
        diff = abs(wcg_value - aira_value)
        match = diff <= self.tolerance
        
        return match, diff
    
    def perform_comparison(self):
        """Main comparison logic."""
        print("\n" + "="*80)
        print("STARTING COMPARISON")
        print("="*80)
        
        # Filter out average and error rows from AIRA files
        aira_gt01_filtered = self.filter_average_rows(self.aira_gt01_df)
        aira_gt01_filtered = self.filter_error_rows(aira_gt01_filtered)
        
        aira_gt02_filtered = self.filter_average_rows(self.aira_gt02_df)
        aira_gt02_filtered = self.filter_error_rows(aira_gt02_filtered)
        
        print(f"\nFiltered AIRA_vs_GT01: {len(aira_gt01_filtered)} valid rows")
        print(f"Filtered AIRA_vs_GT02: {len(aira_gt02_filtered)} valid rows")
        print(f"WCG file rows: {len(self.wcg_df)}")
        
        # Iterate through WCG rows
        for idx, wcg_row in self.wcg_df.iterrows():
            patient = wcg_row['Patient_Normalized']
            organ = wcg_row['Organ_Normalized']
            wcg_dice = wcg_row['DiceCoefficient']
            gt_version = wcg_row['GT_Version']
            
            # Skip if GT version couldn't be determined
            if gt_version == 'UNKNOWN':
                self.errors.append({
                    'patient': patient,
                    'organ': organ,
                    'error': f"Could not determine GT version from: {wcg_row['Mask2']}"
                })
                continue
            
            # Select appropriate AIRA dataframe
            if gt_version == 'GT01':
                aira_df = aira_gt01_filtered
                aira_file_name = 'AIRA_vs_GT01'
            else:
                aira_df = aira_gt02_filtered
                aira_file_name = 'AIRA_vs_GT02'
            
            # Find matching row in AIRA file
            aira_match = aira_df[
                (aira_df['Patient_Normalized'] == patient) & 
                (aira_df['Organ_Normalized'] == organ)
            ]
            
            if len(aira_match) == 0:
                # No match found in AIRA file
                self.missing_in_aira.append({
                    'patient': patient,
                    'organ': organ,
                    'gt_version': gt_version,
                    'wcg_dice': wcg_dice,
                    'aira_file': aira_file_name
                })
            elif len(aira_match) == 1:
                # Exact match found - compare DICE values
                aira_dice = aira_match.iloc[0]['DiceCoefficient']
                match_result, diff = self.compare_dice_values(wcg_dice, aira_dice)
                
                comparison_data = {
                    'patient': patient,
                    'organ': organ,
                    'gt_version': gt_version,
                    'wcg_dice': wcg_dice,
                    'aira_dice': aira_dice,
                    'difference': diff,
                    'wcg_row': idx,
                    'aira_file': aira_file_name
                }
                
                if match_result:
                    self.matches.append(comparison_data)
                else:
                    self.mismatches.append(comparison_data)
            else:
                # Multiple matches found (should be rare)
                self.errors.append({
                    'patient': patient,
                    'organ': organ,
                    'error': f"Multiple matches found in {aira_file_name}: {len(aira_match)} rows"
                })
        
        # Check for entries in AIRA files that are not in WCG
        self._find_missing_in_wcg(aira_gt01_filtered, 'GT01')
        self._find_missing_in_wcg(aira_gt02_filtered, 'GT02')
    
    def _find_missing_in_wcg(self, aira_df: pd.DataFrame, gt_version: str):
        """
        Find entries in AIRA file that are not in WCG file.
        
        Args:
            aira_df: AIRA dataframe to check
            gt_version: GT version string ('GT01' or 'GT02')
        """
        for idx, aira_row in aira_df.iterrows():
            patient = aira_row['Patient_Normalized']
            organ = aira_row['Organ_Normalized']
            
            # Look for this combination in WCG with the same GT version
            wcg_match = self.wcg_df[
                (self.wcg_df['Patient_Normalized'] == patient) & 
                (self.wcg_df['Organ_Normalized'] == organ) &
                (self.wcg_df['GT_Version'] == gt_version)
            ]
            
            if len(wcg_match) == 0:
                self.missing_in_wcg.append({
                    'patient': patient,
                    'organ': organ,
                    'gt_version': gt_version,
                    'aira_dice': aira_row['DiceCoefficient'],
                    'aira_file': f'AIRA_vs_{gt_version}'
                })
    
    def generate_report(self) -> str:
        """
        Generate a comprehensive comparison report.
        
        Returns:
            Formatted report string
        """
        report_lines = []
        report_lines.append("\n" + "="*80)
        report_lines.append("DICE SCORE COMPARISON REPORT")
        report_lines.append("="*80)
        report_lines.append(f"Comparison Tolerance: ±{self.tolerance}")
        report_lines.append("")
        
        # Summary statistics
        report_lines.append("SUMMARY")
        report_lines.append("-" * 80)
        total_comparisons = len(self.matches) + len(self.mismatches)
        report_lines.append(f"Total Comparisons Attempted: {total_comparisons}")
        report_lines.append(f"  ✓ Matches (within tolerance): {len(self.matches)}")
        report_lines.append(f"  ✗ Mismatches (exceeds tolerance): {len(self.mismatches)}")
        report_lines.append(f"  ? Missing in AIRA files: {len(self.missing_in_aira)}")
        report_lines.append(f"  ? Missing in WCG file: {len(self.missing_in_wcg)}")
        report_lines.append(f"  ⚠ Errors encountered: {len(self.errors)}")
        
        if total_comparisons > 0:
            match_percentage = (len(self.matches) / total_comparisons) * 100
            report_lines.append(f"\nMatch Rate: {match_percentage:.2f}%")
        
        # Detailed mismatch report
        if self.mismatches:
            report_lines.append("\n" + "="*80)
            report_lines.append("MISMATCHES (DICE values differ beyond tolerance)")
            report_lines.append("="*80)
            for i, mm in enumerate(self.mismatches, 1):
                report_lines.append(f"\n{i}. Patient: {mm['patient']}, Organ: {mm['organ']}")
                report_lines.append(f"   GT Version: {mm['gt_version']}")
                report_lines.append(f"   WCG DICE:  {mm['wcg_dice']:.6f}")
                report_lines.append(f"   AIRA DICE: {mm['aira_dice']:.6f}")
                report_lines.append(f"   Difference: {mm['difference']:.6f}")
                report_lines.append(f"   Source: {mm['aira_file']}")
        
        # Missing in AIRA files
        if self.missing_in_aira:
            report_lines.append("\n" + "="*80)
            report_lines.append("MISSING IN AIRA FILES (present in WCG but not in AIRA)")
            report_lines.append("="*80)
            for i, miss in enumerate(self.missing_in_aira, 1):
                report_lines.append(f"\n{i}. Patient: {miss['patient']}, Organ: {miss['organ']}")
                report_lines.append(f"   GT Version: {miss['gt_version']}")
                report_lines.append(f"   WCG DICE: {miss['wcg_dice']:.6f}")
                report_lines.append(f"   Expected in: {miss['aira_file']}")
        
        # Missing in WCG file
        if self.missing_in_wcg:
            report_lines.append("\n" + "="*80)
            report_lines.append("MISSING IN WCG FILE (present in AIRA but not in WCG)")
            report_lines.append("="*80)
            for i, miss in enumerate(self.missing_in_wcg, 1):
                report_lines.append(f"\n{i}. Patient: {miss['patient']}, Organ: {miss['organ']}")
                report_lines.append(f"   GT Version: {miss['gt_version']}")
                report_lines.append(f"   AIRA DICE: {miss['aira_dice']:.6f}")
                report_lines.append(f"   Source: {miss['aira_file']}")
        
        # Errors
        if self.errors:
            report_lines.append("\n" + "="*80)
            report_lines.append("ERRORS AND WARNINGS")
            report_lines.append("="*80)
            for i, err in enumerate(self.errors, 1):
                if isinstance(err, dict):
                    if 'patient' in err:
                        report_lines.append(f"\n{i}. Patient: {err.get('patient', 'N/A')}, "
                                          f"Organ: {err.get('organ', 'N/A')}")
                    report_lines.append(f"   Error: {err.get('error', str(err))}")
                else:
                    report_lines.append(f"\n{i}. {err}")
        
        # Success message
        if not self.mismatches and not self.missing_in_aira and not self.missing_in_wcg and not self.errors:
            report_lines.append("\n" + "="*80)
            report_lines.append("✓ ALL DICE SCORES MATCH PERFECTLY!")
            report_lines.append("="*80)
        
        report_lines.append("\n" + "="*80)
        report_lines.append("END OF REPORT")
        report_lines.append("="*80 + "\n")
        
        return "\n".join(report_lines)
    
    def save_detailed_results(self, output_dir: str = "."):
        """
        Save detailed comparison results to CSV files.
        
        Args:
            output_dir: Directory to save output files
        """
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        # Save matches
        if self.matches:
            matches_df = pd.DataFrame(self.matches)
            matches_file = output_path / "comparison_matches.csv"
            matches_df.to_csv(matches_file, index=False)
            print(f"✓ Saved matches to: {matches_file}")
        
        # Save mismatches
        if self.mismatches:
            mismatches_df = pd.DataFrame(self.mismatches)
            mismatches_file = output_path / "comparison_mismatches.csv"
            mismatches_df.to_csv(mismatches_file, index=False)
            print(f"✓ Saved mismatches to: {mismatches_file}")
        
        # Save missing entries
        if self.missing_in_aira:
            missing_aira_df = pd.DataFrame(self.missing_in_aira)
            missing_aira_file = output_path / "missing_in_aira.csv"
            missing_aira_df.to_csv(missing_aira_file, index=False)
            print(f"✓ Saved missing in AIRA to: {missing_aira_file}")
        
        if self.missing_in_wcg:
            missing_wcg_df = pd.DataFrame(self.missing_in_wcg)
            missing_wcg_file = output_path / "missing_in_wcg.csv"
            missing_wcg_df.to_csv(missing_wcg_file, index=False)
            print(f"✓ Saved missing in WCG to: {missing_wcg_file}")
        
        # Save errors
        if self.errors:
            errors_df = pd.DataFrame(self.errors)
            errors_file = output_path / "comparison_errors.csv"
            errors_df.to_csv(errors_file, index=False)
            print(f"✓ Saved errors to: {errors_file}")
    
    def run(self, save_results: bool = True, output_dir: str = "."):
        """
        Run the complete comparison workflow.
        
        Args:
            save_results: Whether to save detailed results to CSV files
            output_dir: Directory to save output files
            
        Returns:
            True if comparison was successful, False otherwise
        """
        # Load data
        if not self.load_data():
            return False
        
        # Perform comparison
        self.perform_comparison()
        
        # Generate and print report
        report = self.generate_report()
        print(report)
        
        # Save report to file
        report_path = Path(output_dir) / "comparison_report.txt"
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report)
        print(f"✓ Report saved to: {report_path}")
        
        # Save detailed results
        if save_results:
            self.save_detailed_results(output_dir)
        
        return True


def main():
    """Main entry point for the script."""
    # Define file paths
    base_dir = Path(__file__).parent
    wcg_file = base_dir / "66017_WCG_DICE_16Dec2025.csv"
    aira_gt01_file = base_dir / "AIRA_vs_GT01.csv"
    aira_gt02_file = base_dir / "AIRA_vs_GT02.csv"
    
    # Check if files exist
    for filepath in [wcg_file, aira_gt01_file, aira_gt02_file]:
        if not filepath.exists():
            print(f"✗ Error: File not found: {filepath}")
            sys.exit(1)
    
    print("="*80)
    print("FDA TRIAL 119 - DICE SCORE COMPARISON TOOL")
    print("="*80)
    print(f"\nInput Files:")
    print(f"  - WCG File: {wcg_file.name}")
    print(f"  - AIRA vs GT01: {aira_gt01_file.name}")
    print(f"  - AIRA vs GT02: {aira_gt02_file.name}")
    
    # Create comparator and run
    comparator = DiceScoreComparator(
        wcg_file=str(wcg_file),
        aira_gt01_file=str(aira_gt01_file),
        aira_gt02_file=str(aira_gt02_file),
        tolerance=0.000001  # Very tight tolerance for exact matches
    )
    
    success = comparator.run(save_results=True, output_dir=str(base_dir))
    
    if success:
        print("\n✓ Comparison completed successfully!")
        sys.exit(0)
    else:
        print("\n✗ Comparison failed!")
        sys.exit(1)


if __name__ == "__main__":
    main()
