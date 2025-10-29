#!/usr/bin/env python3
"""
Test script to verify int16 fix works correctly in all main analysis files
"""

import os
import sys
import numpy as np
import nibabel as nib

# Test the remap_labels function from each file
print("="*70)
print("TESTING INT16 FUNCTIONALITY IN ALL ANALYSIS FILES")
print("="*70)

# Import remap_labels from each file
sys.path.insert(0, r'd:\2024\zTest')

test_results = {}

# Test data - create a simple array with floating point precision issues
test_data = np.array([
    [0.0, 0.999999, 1.000001, 2.0],
    [2.999999, 3.000001, 0.5, 1.5],
    [2.1, 2.9, 3.1, 0.1]
])

# Label mapping for testing
LABEL_MAPPING_AIRA = {0: 0, 1: 0, 2: 2, 3: 1}

print("\n📋 TEST DATA:")
print(f"Original data:\n{test_data}")
print(f"Unique values: {np.unique(test_data)}")

# Test 1: fda_multiple_case_dice.py
print("\n" + "="*70)
print("TEST 1: fda_multiple_case_dice.py")
print("="*70)
try:
    from fda_multiple_case_dice import remap_labels as remap1
    result1 = remap1(test_data.copy(), LABEL_MAPPING_AIRA)
    print(f"✓ Import successful")
    print(f"  Result dtype: {result1.dtype}")
    print(f"  Result unique values: {np.unique(result1)}")
    print(f"  Is int16: {result1.dtype == np.int16}")
    test_results['fda_multiple_case_dice'] = result1.dtype == np.int16
except Exception as e:
    print(f"✗ Error: {e}")
    test_results['fda_multiple_case_dice'] = False

# Test 2: fda_single_case_dice.py
print("\n" + "="*70)
print("TEST 2: fda_single_case_dice.py")
print("="*70)
try:
    from fda_single_case_dice import remap_labels as remap2
    result2 = remap2(test_data.copy(), LABEL_MAPPING_AIRA)
    print(f"✓ Import successful")
    print(f"  Result dtype: {result2.dtype}")
    print(f"  Result unique values: {np.unique(result2)}")
    print(f"  Is int16: {result2.dtype == np.int16}")
    test_results['fda_single_case_dice'] = result2.dtype == np.int16
except Exception as e:
    print(f"✗ Error: {e}")
    test_results['fda_single_case_dice'] = False

# Test 3: fda_multi_reader_analysis.py
print("\n" + "="*70)
print("TEST 3: fda_multi_reader_analysis.py")
print("="*70)
try:
    from fda_multi_reader_analysis import remap_labels as remap3
    result3 = remap3(test_data.copy(), LABEL_MAPPING_AIRA)
    print(f"✓ Import successful")
    print(f"  Result dtype: {result3.dtype}")
    print(f"  Result unique values: {np.unique(result3)}")
    print(f"  Is int16: {result3.dtype == np.int16}")
    test_results['fda_multi_reader_analysis'] = result3.dtype == np.int16
except Exception as e:
    print(f"✗ Error: {e}")
    test_results['fda_multi_reader_analysis'] = False

# Test 4: process_new_aira_masks.py
print("\n" + "="*70)
print("TEST 4: process_new_aira_masks.py")
print("="*70)
try:
    from process_new_aira_masks import remap_labels as remap4
    result4 = remap4(test_data.copy(), LABEL_MAPPING_AIRA)
    print(f"✓ Import successful")
    print(f"  Result dtype: {result4.dtype}")
    print(f"  Result unique values: {np.unique(result4)}")
    print(f"  Is int16: {result4.dtype == np.int16}")
    test_results['process_new_aira_masks'] = result4.dtype == np.int16
except Exception as e:
    print(f"✗ Error: {e}")
    test_results['process_new_aira_masks'] = False

# Test 5: Test exact integer values (no floating point precision issues)
print("\n" + "="*70)
print("TEST 5: Verify Exact Integer Values")
print("="*70)
print("Testing that remapped values are EXACT integers (not 0.9999... or 2.0001...)")

test_data_float = np.array([0.996078, 1.0, 2.000000118])
expected_result = np.array([0, 1, 2], dtype=np.int16)

try:
    from fda_multiple_case_dice import remap_labels
    # Use a simple mapping
    simple_mapping = {0: 0, 1: 1, 2: 2}
    result = remap_labels(test_data_float, simple_mapping)
    
    print(f"Input (with precision issues): {test_data_float}")
    print(f"Output: {result}")
    print(f"Output dtype: {result.dtype}")
    
    # Check if all values are exact integers
    all_exact = all(abs(val - round(val)) < 1e-10 for val in result.flatten())
    print(f"All values are exact integers: {all_exact}")
    
    test_results['exact_integers'] = all_exact and result.dtype == np.int16
except Exception as e:
    print(f"✗ Error: {e}")
    test_results['exact_integers'] = False

# Final summary
print("\n" + "="*70)
print("TEST SUMMARY")
print("="*70)

all_passed = True
for test_name, passed in test_results.items():
    status = "✅ PASS" if passed else "❌ FAIL"
    print(f"{status} - {test_name}")
    if not passed:
        all_passed = False

print("\n" + "="*70)
if all_passed:
    print("🎉 ALL TESTS PASSED - int16 fix working correctly!")
else:
    print("⚠️  SOME TESTS FAILED - review output above")
print("="*70)

sys.exit(0 if all_passed else 1)
