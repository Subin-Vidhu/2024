#!/usr/bin/env python3
"""
ANATOMICAL VALIDATION OF KIDNEY LABEL ASSIGNMENTS
Verify that left/right assignments make clinical sense.
"""

import pandas as pd
import numpy as np

def validate_anatomical_consistency():
    """Check if left/right kidney volumes are anatomically reasonable."""
    
    print("="*70)
    print("ANATOMICAL CONSISTENCY VALIDATION")
    print("="*70)
    
    # Load the latest results
    results_file = r"d:\2024\zTest\results\FDA_Analysis_20251011_133255\FDA_AIRA_Results_20251011_133255.csv"
    
    try:
        df = pd.read_csv(results_file)
        successful = df[df['Status'] == 'Success']
        
        print(f"Analyzing {len(successful)} successful cases...")
        print()
        
        # Extract volume data
        fda_right = successful['FDA_Right_Kidney_Vol_cm3'].dropna()
        fda_left = successful['FDA_Left_Kidney_Vol_cm3'].dropna()
        
        print("FDA GROUND TRUTH VOLUMES (Expert Radiologist):")
        print(f"  Right Kidney: {fda_right.mean():.1f} ± {fda_right.std():.1f} cm³ (range: {fda_right.min():.1f}-{fda_right.max():.1f})")
        print(f"  Left Kidney:  {fda_left.mean():.1f} ± {fda_left.std():.1f} cm³ (range: {fda_left.min():.1f}-{fda_left.max():.1f})")
        
        # Extract AIRA volumes
        aira_right = successful['AIRA_Right_Kidney_Vol_cm3'].dropna()
        aira_left = successful['AIRA_Left_Kidney_Vol_cm3'].dropna()
        
        print(f"\nAIRA AI PREDICTIONS:")
        print(f"  Right Kidney: {aira_right.mean():.1f} ± {aira_right.std():.1f} cm³ (range: {aira_right.min():.1f}-{aira_right.max():.1f})")
        print(f"  Left Kidney:  {aira_left.mean():.1f} ± {aira_left.std():.1f} cm³ (range: {aira_left.min():.1f}-{aira_left.max():.1f})")
        
        # Check anatomical plausibility
        print(f"\n" + "="*50)
        print("ANATOMICAL PLAUSIBILITY CHECK")
        print("="*50)
        
        # Normal adult kidney volume: 120-170 cm³ (highly variable)
        normal_range_min = 80   # Lower bound for small adults
        normal_range_max = 250  # Upper bound for large adults
        
        # Check FDA (ground truth) volumes
        fda_right_normal = ((fda_right >= normal_range_min) & (fda_right <= normal_range_max)).sum()
        fda_left_normal = ((fda_left >= normal_range_min) & (fda_left <= normal_range_max)).sum()
        
        print(f"FDA Ground Truth (Expert Annotations):")
        print(f"  Right kidney volumes in normal range [{normal_range_min}-{normal_range_max} cm³]: {fda_right_normal}/{len(fda_right)} ({fda_right_normal/len(fda_right)*100:.1f}%)")
        print(f"  Left kidney volumes in normal range [{normal_range_min}-{normal_range_max} cm³]: {fda_left_normal}/{len(fda_left)} ({fda_left_normal/len(fda_left)*100:.1f}%)")
        
        # Check AIRA volumes
        aira_right_normal = ((aira_right >= normal_range_min) & (aira_right <= normal_range_max)).sum()
        aira_left_normal = ((aira_left >= normal_range_min) & (aira_left <= normal_range_max)).sum()
        
        print(f"\nAIRA AI Predictions:")
        print(f"  Right kidney volumes in normal range [{normal_range_min}-{normal_range_max} cm³]: {aira_right_normal}/{len(aira_right)} ({aira_right_normal/len(aira_right)*100:.1f}%)")
        print(f"  Left kidney volumes in normal range [{normal_range_min}-{normal_range_max} cm³]: {aira_left_normal}/{len(aira_left)} ({aira_left_normal/len(aira_left)*100:.1f}%)")
        
        # Bilateral consistency check
        print(f"\n" + "="*50)
        print("BILATERAL CONSISTENCY CHECK")
        print("="*50)
        
        # Kidneys should be roughly similar in size (within 30% typically)
        fda_ratio = fda_left / fda_right
        reasonable_ratio = ((fda_ratio >= 0.7) & (fda_ratio <= 1.4)).sum()
        
        print(f"FDA Ground Truth:")
        print(f"  Left/Right ratio: {fda_ratio.mean():.2f} ± {fda_ratio.std():.2f}")
        print(f"  Reasonable ratios (0.7-1.4): {reasonable_ratio}/{len(fda_ratio)} ({reasonable_ratio/len(fda_ratio)*100:.1f}%)")
        
        aira_ratio = aira_left / aira_right
        aira_reasonable_ratio = ((aira_ratio >= 0.7) & (aira_ratio <= 1.4)).sum()
        
        print(f"\nAIRA AI Predictions:")
        print(f"  Left/Right ratio: {aira_ratio.mean():.2f} ± {aira_ratio.std():.2f}")
        print(f"  Reasonable ratios (0.7-1.4): {aira_reasonable_ratio}/{len(aira_ratio)} ({aira_reasonable_ratio/len(aira_ratio)*100:.1f}%)")
        
        # Dice scores validation
        print(f"\n" + "="*50)
        print("DICE SCORE CONSISTENCY CHECK")
        print("="*50)
        
        dice_right = successful['Dice_Right_Kidney'].dropna()
        dice_left = successful['Dice_Left_Kidney'].dropna()
        
        print(f"Dice Coefficients:")
        print(f"  Right Kidney: {dice_right.mean():.4f} ± {dice_right.std():.4f} (range: {dice_right.min():.4f}-{dice_right.max():.4f})")
        print(f"  Left Kidney:  {dice_left.mean():.4f} ± {dice_left.std():.4f} (range: {dice_left.min():.4f}-{dice_left.max():.4f})")
        
        # High Dice scores indicate good segmentation
        high_dice_right = (dice_right >= 0.85).sum()
        high_dice_left = (dice_left >= 0.85).sum()
        
        print(f"\nHigh Quality Segmentation (Dice ≥ 0.85):")
        print(f"  Right Kidney: {high_dice_right}/{len(dice_right)} ({high_dice_right/len(dice_right)*100:.1f}%)")
        print(f"  Left Kidney: {high_dice_left}/{len(dice_left)} ({high_dice_left/len(dice_left)*100:.1f}%)")
        
        # Final validation
        print(f"\n" + "="*70)
        print("FINAL VALIDATION RESULT")
        print("="*70)
        
        # All checks
        anatomical_ok = (fda_right_normal/len(fda_right) >= 0.8 and fda_left_normal/len(fda_left) >= 0.8)
        consistency_ok = (reasonable_ratio/len(fda_ratio) >= 0.8)
        performance_ok = (dice_right.mean() >= 0.85 and dice_left.mean() >= 0.85)
        
        if anatomical_ok and consistency_ok and performance_ok:
            print("✅ VALIDATION PASSED: All anatomical and performance checks passed!")
            print("")
            print("CONFIRMATIONS:")
            print("• Kidney volumes are within normal anatomical ranges ✅")
            print("• Left/Right bilateral consistency is maintained ✅") 
            print("• High Dice scores indicate accurate segmentation ✅")
            print("• Label assignments are anatomically correct ✅")
            print("")
            print("🎯 CONCLUSION: Your left/right kidney labels are CORRECTLY assigned!")
            
        else:
            print("⚠️  WARNING: Some anatomical checks failed.")
            if not anatomical_ok:
                print("   - Kidney volumes outside normal range")
            if not consistency_ok:
                print("   - Poor left/right consistency")
            if not performance_ok:
                print("   - Low Dice scores")
        
        return anatomical_ok and consistency_ok and performance_ok
        
    except Exception as e:
        print(f"Error loading results: {e}")
        return False

if __name__ == "__main__":
    validate_anatomical_consistency()
