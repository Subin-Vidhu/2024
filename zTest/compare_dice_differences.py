#!/usr/bin/env python3
"""
Compare FDA's Dice values with our calculated values to identify differences.
"""

# FDA's values
fda_data = {
    '001': {
        'Right': {'dice': 0.99984, 'vol1_mm3': 130066.43, 'vol2_mm3': 130108.07},
        'Left': {'dice': 0.997481, 'vol1_mm3': 118639.53, 'vol2_mm3': 118061.81},
        'Average': {'dice': 0.998661}
    },
    '002': {
        'Right': {'dice': 0.995908, 'vol1_mm3': 201287.7, 'vol2_mm3': 199944.24},
        'Left': {'dice': 0.999122, 'vol1_mm3': 192727.24, 'vol2_mm3': 192388.93},
        'Average': {'dice': 0.997515}
    }
}

# Our values
our_data = {
    '001': {
        'Right': {'dice': 0.999840, 'vol1_mm3': 130066.42, 'vol2_mm3': 130108.07},
        'Left': {'dice': 0.997481, 'vol1_mm3': 118639.53, 'vol2_mm3': 118061.81},
        'Both': {'dice': 0.998716},
        'Average': {'dice': 0.998716}
    },
    '002': {
        'Right': {'dice': 0.995908, 'vol1_mm3': 201287.70, 'vol2_mm3': 199944.25},
        'Left': {'dice': 0.999122, 'vol1_mm3': 192727.25, 'vol2_mm3': 192388.94},
        'Both': {'dice': 0.997482},
        'Average': {'dice': 0.997482}
    }
}

print("="*80)
print("COMPARISON: FDA VALUES vs OUR VALUES")
print("="*80)

for case_id in ['001', '002']:
    print(f"\n{'='*80}")
    print(f"CASE {case_id}")
    print(f"{'='*80}")
    
    fda = fda_data[case_id]
    ours = our_data[case_id]
    
    # Compare Right Kidney
    print(f"\nRight Kidney:")
    print(f"  FDA Dice:  {fda['Right']['dice']:.6f}")
    print(f"  Our Dice:  {ours['Right']['dice']:.6f}")
    print(f"  Difference: {abs(fda['Right']['dice'] - ours['Right']['dice']):.6f}")
    print(f"  Match: {'✓ YES' if abs(fda['Right']['dice'] - ours['Right']['dice']) < 0.000001 else '✗ NO'}")
    
    print(f"\n  FDA Vol1:  {fda['Right']['vol1_mm3']:.2f} mm³")
    print(f"  Our Vol1:  {ours['Right']['vol1_mm3']:.2f} mm³")
    print(f"  Vol1 Diff: {abs(fda['Right']['vol1_mm3'] - ours['Right']['vol1_mm3']):.2f} mm³")
    
    print(f"\n  FDA Vol2:  {fda['Right']['vol2_mm3']:.2f} mm³")
    print(f"  Our Vol2:  {ours['Right']['vol2_mm3']:.2f} mm³")
    print(f"  Vol2 Diff: {abs(fda['Right']['vol2_mm3'] - ours['Right']['vol2_mm3']):.2f} mm³")
    
    # Compare Left Kidney
    print(f"\nLeft Kidney:")
    print(f"  FDA Dice:  {fda['Left']['dice']:.6f}")
    print(f"  Our Dice:  {ours['Left']['dice']:.6f}")
    print(f"  Difference: {abs(fda['Left']['dice'] - ours['Left']['dice']):.6f}")
    print(f"  Match: {'✓ YES' if abs(fda['Left']['dice'] - ours['Left']['dice']) < 0.000001 else '✗ NO'}")
    
    print(f"\n  FDA Vol1:  {fda['Left']['vol1_mm3']:.2f} mm³")
    print(f"  Our Vol1:  {ours['Left']['vol1_mm3']:.2f} mm³")
    print(f"  Vol1 Diff: {abs(fda['Left']['vol1_mm3'] - ours['Left']['vol1_mm3']):.2f} mm³")
    
    print(f"\n  FDA Vol2:  {fda['Left']['vol2_mm3']:.2f} mm³")
    print(f"  Our Vol2:  {ours['Left']['vol2_mm3']:.2f} mm³")
    print(f"  Vol2 Diff: {abs(fda['Left']['vol2_mm3'] - ours['Left']['vol2_mm3']):.2f} mm³")
    
    # Compare Average
    print(f"\nAverage Dice:")
    print(f"  FDA Average: {fda['Average']['dice']:.6f}")
    print(f"  Our Average: {ours['Average']['dice']:.6f} (Union method - Both Kidneys)")
    print(f"  Difference:  {abs(fda['Average']['dice'] - ours['Average']['dice']):.6f}")
    print(f"  Match: {'✓ YES' if abs(fda['Average']['dice'] - ours['Average']['dice']) < 0.000001 else '✗ NO'}")
    
    # Calculate what FDA's average method is
    fda_calculated_avg = (fda['Right']['dice'] + fda['Left']['dice']) / 2
    print(f"\n  FDA Average if calculated as (Right+Left)/2: {fda_calculated_avg:.6f}")
    print(f"  FDA provided Average:                        {fda['Average']['dice']:.6f}")
    print(f"  Match: {'✓ YES (Arithmetic Mean)' if abs(fda_calculated_avg - fda['Average']['dice']) < 0.000001 else '✗ NO (Different method)'}")

print("\n" + "="*80)
print("ANALYSIS SUMMARY")
print("="*80)

print("\n1. DICE SCORES:")
print("   - Right and Left kidney Dice scores: ✓ MATCH perfectly")
print("   - Volumes: ✓ MATCH (minor rounding differences < 0.1 mm³)")

print("\n2. AVERAGE CALCULATION METHOD:")
print("   - FDA uses: Arithmetic Mean = (Dice_Right + Dice_Left) / 2")
print("   - We use:   Union Method = Dice of combined kidney masks")
print("   - These give DIFFERENT values!")

print("\n3. VOLUME DIFFERENCES:")
print("   - Very minor differences (< 0.1 mm³)")
print("   - Likely due to floating-point precision or rounding")

print("\n4. RECOMMENDATION:")
print("   - Change 'XXX Average' row to use arithmetic mean")
print("   - Keep 'Both Kidneys' row with union method")
print("   - This matches FDA's convention")

print("\n" + "="*80)
