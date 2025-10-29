#!/usr/bin/env python3
"""
Verification script to confirm all remap_labels functions now use int16
"""

import os
import re

def check_file(filepath):
    """Check if a file has the correct int16 implementation."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check for remap_labels function
    if 'def remap_labels' not in content:
        return None  # No remap_labels function
    
    # Check for the buggy float return
    if 'return remapped_data.astype(float)' in content:
        return False  # Still has the bug
    
    # Check for int16 usage
    if 'np.int16' in content and 'return remapped_data' in content:
        return True  # Fixed with int16
    
    return None  # Different implementation

def main():
    """Verify all Python files in zTest folder."""
    ztest_folder = r"d:\2024\zTest"
    
    print("="*70)
    print("VERIFYING INT16 FIX ACROSS ALL FILES")
    print("="*70)
    
    files_with_remap = []
    fixed_files = []
    buggy_files = []
    
    for filename in os.listdir(ztest_folder):
        if filename.endswith('.py'):
            filepath = os.path.join(ztest_folder, filename)
            result = check_file(filepath)
            
            if result is not None:
                files_with_remap.append(filename)
                if result:
                    fixed_files.append(filename)
                    print(f"✅ {filename:50s} - FIXED (uses int16)")
                else:
                    buggy_files.append(filename)
                    print(f"❌ {filename:50s} - BUGGY (uses float)")
    
    print("\n" + "="*70)
    print("SUMMARY")
    print("="*70)
    print(f"Total files with remap_labels function: {len(files_with_remap)}")
    print(f"Fixed files (using int16): {len(fixed_files)}")
    print(f"Buggy files (using float): {len(buggy_files)}")
    
    if buggy_files:
        print("\n⚠️  FILES STILL NEEDING FIX:")
        for f in buggy_files:
            print(f"   - {f}")
    else:
        print("\n🎉 ALL FILES SUCCESSFULLY FIXED!")
    
    print("\n" + "="*70)
    print("FIXED FILES LIST:")
    print("="*70)
    for f in sorted(fixed_files):
        print(f"  ✓ {f}")
    
    return len(buggy_files) == 0

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
