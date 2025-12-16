#!/usr/bin/env python3
"""
Analyze why DiffPercent values differ between FDA and our calculations
"""

print("="*80)
print("ANALYZING VOLUME DIFFERENCE PERCENTAGE CALCULATIONS")
print("="*80)

# Case 001 - Right Kidney
print("\n" + "="*80)
print("CASE 001 - RIGHT KIDNEY")
print("="*80)

fda_vol1 = 130066.43
fda_vol2 = 130108.07
our_vol1 = 130066.42
our_vol2 = 130108.07

print(f"\nFDA Volumes:")
print(f"  GT01: {fda_vol1:.2f} mm³")
print(f"  GT02: {fda_vol2:.2f} mm³")
print(f"  FDA shows: 0.03%")

print(f"\nOur Volumes:")
print(f"  GT01: {our_vol1:.2f} mm³")
print(f"  GT02: {our_vol2:.2f} mm³")

# Method 1: Absolute difference / Average
method1_fda = abs(fda_vol1 - fda_vol2) / ((fda_vol1 + fda_vol2) / 2) * 100
method1_ours = abs(our_vol1 - our_vol2) / ((our_vol1 + our_vol2) / 2) * 100

print(f"\nMethod 1: |Vol1 - Vol2| / ((Vol1 + Vol2) / 2) × 100")
print(f"  FDA calculation:  {method1_fda:.4f}%")
print(f"  Our calculation:  {method1_ours:.4f}%")
print(f"  Rounded to 2 decimals:")
print(f"    FDA: {method1_fda:.2f}%")
print(f"    Ours: {method1_ours:.2f}%")

# Method 2: Absolute difference / Vol1
method2_fda = abs(fda_vol1 - fda_vol2) / fda_vol1 * 100
method2_ours = abs(our_vol1 - our_vol2) / our_vol1 * 100

print(f"\nMethod 2: |Vol1 - Vol2| / Vol1 × 100")
print(f"  FDA calculation:  {method2_fda:.4f}%")
print(f"  Our calculation:  {method2_ours:.4f}%")

# Method 3: Absolute difference / Vol2
method3_fda = abs(fda_vol1 - fda_vol2) / fda_vol2 * 100
method3_ours = abs(our_vol1 - our_vol2) / our_vol2 * 100

print(f"\nMethod 3: |Vol1 - Vol2| / Vol2 × 100")
print(f"  FDA calculation:  {method3_fda:.4f}%")
print(f"  Our calculation:  {method3_ours:.4f}%")

# Case 001 - Left Kidney
print("\n" + "="*80)
print("CASE 001 - LEFT KIDNEY")
print("="*80)

fda_vol1 = 118639.53
fda_vol2 = 118061.81
our_vol1 = 118639.53
our_vol2 = 118061.81

print(f"\nFDA Volumes:")
print(f"  GT01: {fda_vol1:.2f} mm³")
print(f"  GT02: {fda_vol2:.2f} mm³")
print(f"  FDA shows: 0.49%")

print(f"\nOur Volumes:")
print(f"  GT01: {our_vol1:.2f} mm³")
print(f"  GT02: {our_vol2:.2f} mm³")

# Method 1: Absolute difference / Average
method1 = abs(fda_vol1 - fda_vol2) / ((fda_vol1 + fda_vol2) / 2) * 100

print(f"\nMethod 1: |Vol1 - Vol2| / ((Vol1 + Vol2) / 2) × 100")
print(f"  Calculation: |{fda_vol1} - {fda_vol2}| / (({fda_vol1} + {fda_vol2}) / 2) × 100")
print(f"  Result: {method1:.4f}%")
print(f"  Rounded: {method1:.2f}%")
print(f"  FDA shows: 0.49%")
print(f"  Match: {'✓ YES' if abs(method1 - 0.49) < 0.01 else '✗ NO'}")

# Case 002 - Right Kidney
print("\n" + "="*80)
print("CASE 002 - RIGHT KIDNEY")
print("="*80)

fda_vol1 = 201287.7
fda_vol2 = 199944.24
our_vol1 = 201287.70
our_vol2 = 199944.25

print(f"\nFDA Volumes:")
print(f"  GT01: {fda_vol1:.2f} mm³")
print(f"  GT02: {fda_vol2:.2f} mm³")
print(f"  FDA shows: 0.67%")

print(f"\nOur Volumes:")
print(f"  GT01: {our_vol1:.2f} mm³")
print(f"  GT02: {our_vol2:.2f} mm³")

# Method 1
method1 = abs(fda_vol1 - fda_vol2) / ((fda_vol1 + fda_vol2) / 2) * 100

print(f"\nMethod 1: |Vol1 - Vol2| / ((Vol1 + Vol2) / 2) × 100")
print(f"  Result: {method1:.4f}%")
print(f"  Rounded: {method1:.2f}%")
print(f"  FDA shows: 0.67%")
print(f"  Match: {'✓ YES' if abs(method1 - 0.67) < 0.01 else '✗ NO'}")

# Case 002 - Left Kidney  
print("\n" + "="*80)
print("CASE 002 - LEFT KIDNEY")
print("="*80)

fda_vol1 = 192727.24
fda_vol2 = 192388.93
our_vol1 = 192727.25
our_vol2 = 192388.94

print(f"\nFDA Volumes:")
print(f"  GT01: {fda_vol1:.2f} mm³")
print(f"  GT02: {fda_vol2:.2f} mm³")
print(f"  FDA shows: 0.18%")

print(f"\nOur Volumes:")
print(f"  GT01: {our_vol1:.2f} mm³")
print(f"  GT02: {our_vol2:.2f} mm³")

# Method 1
method1 = abs(fda_vol1 - fda_vol2) / ((fda_vol1 + fda_vol2) / 2) * 100

print(f"\nMethod 1: |Vol1 - Vol2| / ((Vol1 + Vol2) / 2) × 100")
print(f"  Result: {method1:.4f}%")
print(f"  Rounded: {method1:.2f}%")
print(f"  FDA shows: 0.18%")
print(f"  Match: {'✓ YES' if abs(method1 - 0.18) < 0.01 else '✗ NO'}")

print("\n" + "="*80)
print("CONCLUSION")
print("="*80)
print("\nFDA uses the same formula as us:")
print("  DiffPercent = |Vol1 - Vol2| / ((Vol1 + Vol2) / 2) × 100")
print("\nThe tiny differences (0.01 mm³) in volumes cause identical")
print("percentage differences when rounded to 2 decimal places.")
print("\nOur calculations MATCH FDA's approach perfectly!")
print("="*80)
