#!/usr/bin/env python3
"""
Compare Average row format between Cases 001, 002, and 003
"""

print("="*80)
print("COMPARING AVERAGE ROW FORMAT")
print("="*80)

cases = {
    '001': {
        'right_dice': 0.999840,
        'left_dice': 0.997481,
        'our_avg': 0.998661
    },
    '002': {
        'right_dice': 0.995908,
        'left_dice': 0.999122,
        'our_avg': 0.997515
    },
    '003': {
        'right_dice': 0.931077,
        'left_dice': 0.967775,
        'our_avg': 0.949426
    }
}

for case_id, data in cases.items():
    print(f"\n{'='*80}")
    print(f"CASE {case_id}")
    print(f"{'='*80}")
    
    right = data['right_dice']
    left = data['left_dice']
    our_avg = data['our_avg']
    
    # Calculate arithmetic mean
    arithmetic_mean = (right + left) / 2
    
    print(f"\nRight Kidney Dice: {right:.6f}")
    print(f"Left Kidney Dice:  {left:.6f}")
    print(f"\nArithmetic Mean: ({right:.6f} + {left:.6f}) / 2")
    print(f"               = {arithmetic_mean:.6f}")
    print(f"\nOur CSV shows:   {our_avg:.6f}")
    print(f"Difference:      {abs(arithmetic_mean - our_avg):.10f}")
    print(f"Match: {'✓ YES' if abs(arithmetic_mean - our_avg) < 0.000001 else '✗ NO'}")

print("\n" + "="*80)
print("CONCLUSION")
print("="*80)
print("\nAll three cases use the same formula:")
print("  Average = (Dice_Right + Dice_Left) / 2")
print("\nAll calculations are CORRECT and consistent!")
print("="*80)
