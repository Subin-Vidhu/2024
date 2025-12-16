#!/usr/bin/env python3
"""
Analyze Case 003 DiffPercent calculation
"""

print("="*80)
print("CASE 003 - DIFFPERCENT ANALYSIS")
print("="*80)

# From our CSV
our_right_vol1 = 23.71  # cm³
our_right_vol2 = 21.51  # cm³
our_right_diff = "9.73%"

our_left_vol1 = 106.93  # cm³
our_left_vol2 = 100.26  # cm³
our_left_diff = "6.44%"

print("\nOUR VALUES (from CSV):")
print(f"Right Kidney:")
print(f"  GT01: {our_right_vol1} cm³")
print(f"  GT02: {our_right_vol2} cm³")
print(f"  DiffPercent shown: {our_right_diff}")

print(f"\nLeft Kidney:")
print(f"  GT01: {our_left_vol1} cm³")
print(f"  GT02: {our_left_vol2} cm³")
print(f"  DiffPercent shown: {our_left_diff}")

# Calculate what FDA should show
print("\n" + "="*80)
print("RECALCULATING DIFFPERCENT:")
print("="*80)

# Right Kidney
print(f"\nRight Kidney:")
print(f"  Formula: |Vol1 - Vol2| / ((Vol1 + Vol2) / 2) × 100")
right_diff_calc = abs(our_right_vol1 - our_right_vol2) / ((our_right_vol1 + our_right_vol2) / 2) * 100
print(f"  Calculation: |{our_right_vol1} - {our_right_vol2}| / (({our_right_vol1} + {our_right_vol2}) / 2) × 100")
print(f"  = |{our_right_vol1 - our_right_vol2:.2f}| / {(our_right_vol1 + our_right_vol2) / 2:.2f} × 100")
print(f"  = {abs(our_right_vol1 - our_right_vol2):.2f} / {(our_right_vol1 + our_right_vol2) / 2:.2f} × 100")
print(f"  = {right_diff_calc:.4f}%")
print(f"  Rounded to 2 decimals: {right_diff_calc:.2f}%")
print(f"  Our CSV shows: {our_right_diff}")
print(f"  Match: {'✓ YES' if our_right_diff == f'{right_diff_calc:.2f}%' else '✗ NO'}")

# Left Kidney
print(f"\nLeft Kidney:")
print(f"  Formula: |Vol1 - Vol2| / ((Vol1 + Vol2) / 2) × 100")
left_diff_calc = abs(our_left_vol1 - our_left_vol2) / ((our_left_vol1 + our_left_vol2) / 2) * 100
print(f"  Calculation: |{our_left_vol1} - {our_left_vol2}| / (({our_left_vol1} + {our_left_vol2}) / 2) × 100")
print(f"  = |{our_left_vol1 - our_left_vol2:.2f}| / {(our_left_vol1 + our_left_vol2) / 2:.2f} × 100")
print(f"  = {abs(our_left_vol1 - our_left_vol2):.2f} / {(our_left_vol1 + our_left_vol2) / 2:.2f} × 100")
print(f"  = {left_diff_calc:.4f}%")
print(f"  Rounded to 2 decimals: {left_diff_calc:.2f}%")
print(f"  Our CSV shows: {our_left_diff}")
print(f"  Match: {'✓ YES' if our_left_diff == f'{left_diff_calc:.2f}%' else '✗ NO'}")

print("\n" + "="*80)
print("QUESTION: What DiffPercent did FDA show for Case 003?")
print("="*80)
print("\nPlease share FDA's values for Case 003 so we can compare.")
print("Expected format:")
print("  A-003_GT01.nii  A-003_GT02.nii  Right Kidney  [dice]  [vol1]  [vol2]  ...  [diff%]")
print("  A-003_GT01.nii  A-003_GT02.nii  Left Kidney   [dice]  [vol1]  [vol2]  ...  [diff%]")
print("="*80)
