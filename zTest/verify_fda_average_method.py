#!/usr/bin/env python3
"""
Verify FDA's Average calculation method
"""

print("="*80)
print("VERIFYING FDA AVERAGE CALCULATION METHOD")
print("="*80)

# Case 001
print("\n" + "="*80)
print("CASE 001")
print("="*80)

dice_right_001 = 0.99984
dice_left_001 = 0.997481
fda_average_001 = 0.998661

print(f"\nGiven:")
print(f"  Right Kidney Dice: {dice_right_001}")
print(f"  Left Kidney Dice:  {dice_left_001}")
print(f"  FDA Average:       {fda_average_001}")

# Method 1: Arithmetic Mean
arithmetic_mean_001 = (dice_right_001 + dice_left_001) / 2
print(f"\nMethod 1: Arithmetic Mean = (Right + Left) / 2")
print(f"  Calculation: ({dice_right_001} + {dice_left_001}) / 2")
print(f"  Result:      {arithmetic_mean_001:.6f}")
print(f"  FDA Average: {fda_average_001:.6f}")
print(f"  Difference:  {abs(arithmetic_mean_001 - fda_average_001):.10f}")
print(f"  Match: {'✓ YES' if abs(arithmetic_mean_001 - fda_average_001) < 0.000001 else '✗ NO'}")

# Method 2: Harmonic Mean
harmonic_mean_001 = 2 / ((1/dice_right_001) + (1/dice_left_001))
print(f"\nMethod 2: Harmonic Mean = 2 / (1/Right + 1/Left)")
print(f"  Result:      {harmonic_mean_001:.6f}")
print(f"  FDA Average: {fda_average_001:.6f}")
print(f"  Difference:  {abs(harmonic_mean_001 - fda_average_001):.10f}")
print(f"  Match: {'✓ YES' if abs(harmonic_mean_001 - fda_average_001) < 0.000001 else '✗ NO'}")

# Method 3: Geometric Mean
geometric_mean_001 = (dice_right_001 * dice_left_001) ** 0.5
print(f"\nMethod 3: Geometric Mean = √(Right × Left)")
print(f"  Result:      {geometric_mean_001:.6f}")
print(f"  FDA Average: {fda_average_001:.6f}")
print(f"  Difference:  {abs(geometric_mean_001 - fda_average_001):.10f}")
print(f"  Match: {'✓ YES' if abs(geometric_mean_001 - fda_average_001) < 0.000001 else '✗ NO'}")

# Case 002
print("\n" + "="*80)
print("CASE 002")
print("="*80)

dice_right_002 = 0.995908
dice_left_002 = 0.999122
fda_average_002 = 0.997515

print(f"\nGiven:")
print(f"  Right Kidney Dice: {dice_right_002}")
print(f"  Left Kidney Dice:  {dice_left_002}")
print(f"  FDA Average:       {fda_average_002}")

# Method 1: Arithmetic Mean
arithmetic_mean_002 = (dice_right_002 + dice_left_002) / 2
print(f"\nMethod 1: Arithmetic Mean = (Right + Left) / 2")
print(f"  Calculation: ({dice_right_002} + {dice_left_002}) / 2")
print(f"  Result:      {arithmetic_mean_002:.6f}")
print(f"  FDA Average: {fda_average_002:.6f}")
print(f"  Difference:  {abs(arithmetic_mean_002 - fda_average_002):.10f}")
print(f"  Match: {'✓ YES' if abs(arithmetic_mean_002 - fda_average_002) < 0.000001 else '✗ NO'}")

# Method 2: Harmonic Mean
harmonic_mean_002 = 2 / ((1/dice_right_002) + (1/dice_left_002))
print(f"\nMethod 2: Harmonic Mean = 2 / (1/Right + 1/Left)")
print(f"  Result:      {harmonic_mean_002:.6f}")
print(f"  FDA Average: {fda_average_002:.6f}")
print(f"  Difference:  {abs(harmonic_mean_002 - fda_average_002):.10f}")
print(f"  Match: {'✓ YES' if abs(harmonic_mean_002 - fda_average_002) < 0.000001 else '✗ NO'}")

# Method 3: Geometric Mean
geometric_mean_002 = (dice_right_002 * dice_left_002) ** 0.5
print(f"\nMethod 3: Geometric Mean = √(Right × Left)")
print(f"  Result:      {geometric_mean_002:.6f}")
print(f"  FDA Average: {fda_average_002:.6f}")
print(f"  Difference:  {abs(geometric_mean_002 - fda_average_002):.10f}")
print(f"  Match: {'✓ YES' if abs(geometric_mean_002 - fda_average_002) < 0.000001 else '✗ NO'}")

# Summary
print("\n" + "="*80)
print("CONCLUSION")
print("="*80)

print("\nFor CASE 001:")
if abs(arithmetic_mean_001 - fda_average_001) < 0.000001:
    print("  ✓ FDA uses ARITHMETIC MEAN")
elif abs(harmonic_mean_001 - fda_average_001) < 0.000001:
    print("  ✓ FDA uses HARMONIC MEAN")
elif abs(geometric_mean_001 - fda_average_001) < 0.000001:
    print("  ✓ FDA uses GEOMETRIC MEAN")
else:
    print("  ✗ FDA uses UNKNOWN method")

print("\nFor CASE 002:")
if abs(arithmetic_mean_002 - fda_average_002) < 0.000001:
    print("  ✓ FDA uses ARITHMETIC MEAN")
elif abs(harmonic_mean_002 - fda_average_002) < 0.000001:
    print("  ✓ FDA uses HARMONIC MEAN")
elif abs(geometric_mean_002 - fda_average_002) < 0.000001:
    print("  ✓ FDA uses GEOMETRIC MEAN")
else:
    print("  ✗ FDA uses UNKNOWN method")

print("\n" + "="*80)
print("FORMULA CONFIRMED:")
print("  FDA Average = (Dice_Right + Dice_Left) / 2")
print("  This is the simple ARITHMETIC MEAN")
print("="*80)
