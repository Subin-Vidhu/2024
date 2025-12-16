#!/usr/bin/env python3
"""
Analyze FDA's DiffPercent formula for Case 003
"""

print("="*80)
print("CASE 003 - DIFFPERCENT FORMULA ANALYSIS")
print("="*80)

# Volumes (in cm³)
vol1 = 23.71
vol2 = 21.51

print("\nRIGHT KIDNEY:")
print(f"  GT01 Volume: {vol1} cm³")
print(f"  GT02 Volume: {vol2} cm³")
print(f"  FDA shows: 9.28%")
print(f"  We show: 9.73%")

print("\n" + "-"*80)
print("Testing different formulas:")
print("-"*80)

# Method 1: Relative to average (what we use)
method1 = abs(vol1 - vol2) / ((vol1 + vol2) / 2) * 100
print(f"\nMethod 1: |Vol1 - Vol2| / ((Vol1 + Vol2) / 2) × 100")
print(f"  = |{vol1} - {vol2}| / (({vol1} + {vol2}) / 2) × 100")
print(f"  = {abs(vol1 - vol2):.2f} / {(vol1 + vol2) / 2:.2f} × 100")
print(f"  = {method1:.4f}%")
print(f"  Rounded: {method1:.2f}%")
print(f"  Match FDA? {'✓ YES' if abs(method1 - 9.28) < 0.01 else '✗ NO'}")

# Method 2: Relative to Vol1 (larger volume)
method2 = abs(vol1 - vol2) / vol1 * 100
print(f"\nMethod 2: |Vol1 - Vol2| / Vol1 × 100")
print(f"  = |{vol1} - {vol2}| / {vol1} × 100")
print(f"  = {abs(vol1 - vol2):.2f} / {vol1} × 100")
print(f"  = {method2:.4f}%")
print(f"  Rounded: {method2:.2f}%")
print(f"  Match FDA? {'✓ YES' if abs(method2 - 9.28) < 0.01 else '✗ NO'}")

# Method 3: Relative to Vol2 (smaller volume)
method3 = abs(vol1 - vol2) / vol2 * 100
print(f"\nMethod 3: |Vol1 - Vol2| / Vol2 × 100")
print(f"  = |{vol1} - {vol2}| / {vol2} × 100")
print(f"  = {abs(vol1 - vol2):.2f} / {vol2} × 100")
print(f"  = {method3:.4f}%")
print(f"  Rounded: {method3:.2f}%")
print(f"  Match FDA? {'✓ YES' if abs(method3 - 9.28) < 0.01 else '✗ NO'}")

# Method 4: Relative to larger volume (max)
method4 = abs(vol1 - vol2) / max(vol1, vol2) * 100
print(f"\nMethod 4: |Vol1 - Vol2| / max(Vol1, Vol2) × 100")
print(f"  = |{vol1} - {vol2}| / max({vol1}, {vol2}) × 100")
print(f"  = {abs(vol1 - vol2):.2f} / {max(vol1, vol2)} × 100")
print(f"  = {method4:.4f}%")
print(f"  Rounded: {method4:.2f}%")
print(f"  Match FDA? {'✓ YES' if abs(method4 - 9.28) < 0.01 else '✗ NO'}")

print("\n" + "="*80)

# LEFT KIDNEY
vol1 = 106.93
vol2 = 100.26

print("\nLEFT KIDNEY:")
print(f"  GT01 Volume: {vol1} cm³")
print(f"  GT02 Volume: {vol2} cm³")
print(f"  FDA shows: 6.24%")
print(f"  We show: 6.44%")

print("\n" + "-"*80)
print("Testing different formulas:")
print("-"*80)

# Method 1: Relative to average (what we use)
method1 = abs(vol1 - vol2) / ((vol1 + vol2) / 2) * 100
print(f"\nMethod 1: |Vol1 - Vol2| / ((Vol1 + Vol2) / 2) × 100")
print(f"  = {method1:.4f}%")
print(f"  Rounded: {method1:.2f}%")
print(f"  Match FDA? {'✓ YES' if abs(method1 - 6.24) < 0.01 else '✗ NO'}")

# Method 2: Relative to Vol1 (larger volume)
method2 = abs(vol1 - vol2) / vol1 * 100
print(f"\nMethod 2: |Vol1 - Vol2| / Vol1 × 100")
print(f"  = {method2:.4f}%")
print(f"  Rounded: {method2:.2f}%")
print(f"  Match FDA? {'✓ YES' if abs(method2 - 6.24) < 0.01 else '✗ NO'}")

# Method 3: Relative to Vol2 (smaller volume)
method3 = abs(vol1 - vol2) / vol2 * 100
print(f"\nMethod 3: |Vol1 - Vol2| / Vol2 × 100")
print(f"  = {method3:.4f}%")
print(f"  Rounded: {method3:.2f}%")
print(f"  Match FDA? {'✓ YES' if abs(method3 - 6.24) < 0.01 else '✗ NO'}")

# Method 4: Relative to larger volume (max)
method4 = abs(vol1 - vol2) / max(vol1, vol2) * 100
print(f"\nMethod 4: |Vol1 - Vol2| / max(Vol1, Vol2) × 100")
print(f"  = {method4:.4f}%")
print(f"  Rounded: {method4:.2f}%")
print(f"  Match FDA? {'✓ YES' if abs(method4 - 6.24) < 0.01 else '✗ NO'}")

print("\n" + "="*80)
print("CONCLUSION")
print("="*80)
