#!/usr/bin/env python3
"""
Comprehensive test of all main FDA analysis scripts
"""

import os
import sys

print("="*70)
print("COMPREHENSIVE FDA ANALYSIS SCRIPTS TEST")
print("="*70)

# Test files that exist
test_cases = [
    {
        'name': 'N-092 (New AIRA)',
        'gt': r'C:\Users\Subin-PC\Downloads\Telegram Desktop\GT01 - 5 Test Cases\N-072_AS.nii',  # Using similar case
        'pred': r'D:\__SHARED__\AIRA_FDA_SET_2_LIVE\test\N-092\aira_mask_processed.nii'
    }
]

# Verify files exist
print("\n📁 Checking test files...")
for case in test_cases:
    gt_exists = os.path.exists(case['gt'])
    pred_exists = os.path.exists(case['pred'])
    print(f"\n{case['name']}:")
    print(f"  GT: {'✓' if gt_exists else '✗'} {case['gt']}")
    print(f"  Pred: {'✓' if pred_exists else '✗'} {case['pred']}")

# Test the main scripts can import and have int16
print("\n" + "="*70)
print("TESTING SCRIPT IMPORTS AND INT16 FUNCTIONALITY")
print("="*70)

sys.path.insert(0, r'd:\2024\zTest')

test_results = {}

# Test 1: Can we import the scripts?
print("\n1. Import Test:")
try:
    import fda_multiple_case_dice
    print("  ✓ fda_multiple_case_dice imported")
    test_results['import_multiple'] = True
except Exception as e:
    print(f"  ✗ fda_multiple_case_dice failed: {e}")
    test_results['import_multiple'] = False

try:
    import fda_single_case_dice
    print("  ✓ fda_single_case_dice imported")
    test_results['import_single'] = True
except Exception as e:
    print(f"  ✗ fda_single_case_dice failed: {e}")
    test_results['import_single'] = False

try:
    import fda_multi_reader_analysis
    print("  ✓ fda_multi_reader_analysis imported")
    test_results['import_multi_reader'] = True
except Exception as e:
    print(f"  ✗ fda_multi_reader_analysis failed: {e}")
    test_results['import_multi_reader'] = False

# Test 2: Do the remap functions return int16?
print("\n2. Int16 Return Type Test:")
import numpy as np

test_data = np.array([[0.0, 1.0, 2.0], [3.0, 0.5, 1.5]])
label_mapping = {0: 0, 1: 0, 2: 2, 3: 1}

if test_results.get('import_multiple'):
    result = fda_multiple_case_dice.remap_labels(test_data.copy(), label_mapping)
    is_int16 = result.dtype == np.int16
    print(f"  {'✓' if is_int16 else '✗'} fda_multiple_case_dice returns int16: {result.dtype}")
    test_results['int16_multiple'] = is_int16

if test_results.get('import_single'):
    result = fda_single_case_dice.remap_labels(test_data.copy(), label_mapping)
    is_int16 = result.dtype == np.int16
    print(f"  {'✓' if is_int16 else '✗'} fda_single_case_dice returns int16: {result.dtype}")
    test_results['int16_single'] = is_int16

if test_results.get('import_multi_reader'):
    result = fda_multi_reader_analysis.remap_labels(test_data.copy(), label_mapping)
    is_int16 = result.dtype == np.int16
    print(f"  {'✓' if is_int16 else '✗'} fda_multi_reader_analysis returns int16: {result.dtype}")
    test_results['int16_multi_reader'] = is_int16

# Test 3: Test with actual floating-point precision issues
print("\n3. Floating-Point Precision Test:")
print("   Testing with values like 0.996078 and 2.000000118...")

problem_data = np.array([0.996078, 1.0, 2.000000118, 2.9999999])
simple_mapping = {0: 0, 1: 1, 2: 2, 3: 3}

if test_results.get('import_multiple'):
    result = fda_multiple_case_dice.remap_labels(problem_data, simple_mapping)
    unique_vals = np.unique(result)
    all_exact = all(abs(v - round(v)) < 1e-10 for v in unique_vals)
    print(f"  {'✓' if all_exact else '✗'} fda_multiple_case_dice - exact integers: {unique_vals}")
    test_results['precision_multiple'] = all_exact

# Test 4: Check processed mask files have exact integers
print("\n4. Processed Mask Files Test:")
import nibabel as nib

mask_file = r'D:\__SHARED__\AIRA_FDA_SET_2_LIVE\test\N-092\aira_mask_processed.nii'
if os.path.exists(mask_file):
    img = nib.load(mask_file)
    data = img.get_fdata()
    unique_vals = np.unique(data)
    all_exact = all(abs(v - round(v)) < 1e-10 for v in unique_vals)
    print(f"  {'✓' if all_exact else '✗'} N-092 processed mask has exact integers")
    print(f"      Unique values: {unique_vals}")
    test_results['processed_mask'] = all_exact
else:
    print(f"  ✗ Processed mask not found")
    test_results['processed_mask'] = False

# Final Summary
print("\n" + "="*70)
print("TEST SUMMARY")
print("="*70)

total_tests = len(test_results)
passed_tests = sum(1 for v in test_results.values() if v)

for test_name, passed in test_results.items():
    status = "✅ PASS" if passed else "❌ FAIL"
    print(f"{status} - {test_name}")

print(f"\nResults: {passed_tests}/{total_tests} tests passed")

if passed_tests == total_tests:
    print("\n🎉 ALL TESTS PASSED - Scripts working correctly with int16 fix!")
    sys.exit(0)
else:
    print("\n⚠️  SOME TESTS FAILED - Review output above")
    sys.exit(1)
