#!/usr/bin/env python3
"""
Re-check Cases 001 and 002 with both formulas
"""

print("="*80)
print("RECHECKING CASES 001 & 002 WITH BOTH FORMULAS")
print("="*80)

cases = {
    '001 Right': {'vol1': 130066.43, 'vol2': 130108.07, 'fda': 0.03},
    '001 Left': {'vol1': 118639.53, 'vol2': 118061.81, 'fda': 0.49},
    '002 Right': {'vol1': 201287.7, 'vol2': 199944.24, 'fda': 0.67},
    '002 Left': {'vol1': 192727.24, 'vol2': 192388.93, 'fda': 0.18},
}

for case_name, data in cases.items():
    print(f"\n{'='*80}")
    print(f"CASE {case_name}")
    print(f"{'='*80}")
    
    vol1 = data['vol1']
    vol2 = data['vol2']
    fda_percent = data['fda']
    
    # Method 1: Average
    method1 = abs(vol1 - vol2) / ((vol1 + vol2) / 2) * 100
    
    # Method 2: Larger volume
    method2 = abs(vol1 - vol2) / max(vol1, vol2) * 100
    
    print(f"  Volumes: {vol1:.2f} vs {vol2:.2f} mm³")
    print(f"  FDA shows: {fda_percent:.2f}%")
    print(f"\n  Method 1 (Average):  {method1:.2f}%  {'✓' if abs(method1 - fda_percent) < 0.01 else '✗'}")
    print(f"  Method 2 (Max):      {method2:.2f}%  {'✓' if abs(method2 - fda_percent) < 0.01 else '✗'}")

print("\n" + "="*80)
print("CONCLUSION:")
print("="*80)
print("\nFor Cases 001 and 002:")
print("  Both formulas give nearly IDENTICAL results")
print("  because the volumes are very similar (< 2% difference)")
print("\nFor Case 003:")
print("  Volumes differ by ~10%, so formulas give different results")
print("  FDA appears to use: |Vol1 - Vol2| / max(Vol1, Vol2) × 100")
print("\nRECOMMENDATION:")
print("  Update our formula to use max(Vol1, Vol2) as denominator")
print("  This will match FDA for all cases")
print("="*80)
