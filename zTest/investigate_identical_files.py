import os
import numpy as np
import nibabel as nib
import pandas as pd

# Dataset paths
DATASET_PATHS = {
    'FDA_ORIGINAL': r'c:\Users\Subin-PC\Downloads\Telegram Desktop\OneDrive_1_10-8-2025',
    'GT01_AS': r'C:\Users\Subin-PC\Downloads\Telegram Desktop\GT01 - 5 Test Cases',
    'GT02_GM': r'C:\Users\Subin-PC\Downloads\Telegram Desktop\GT02 - 5 Test Cases'
}

def load_nifti_safe(file_path):
    """Load NIfTI file safely."""
    try:
        if not os.path.exists(file_path):
            return None
        img = nib.load(file_path)
        return img
    except Exception as e:
        print(f"Error loading {file_path}: {e}")
        return None

def analyze_file_identity():
    """Investigate if MC (FDA) and GT1 files are identical."""
    print("="*70)
    print("INVESTIGATING MC vs GT1 PERFECT DICE SCORES")
    print("="*70)
    
    # Test cases that showed perfect agreement
    test_cases = ['N-072', 'N-073', 'N-085', 'N-088', 'N-090']
    
    for case_id in test_cases:
        print(f"\nAnalyzing {case_id}:")
        print("-" * 40)
        
        # Load MC (FDA) file
        case_folder = os.path.join(DATASET_PATHS['FDA_ORIGINAL'], case_id)
        mc_patterns = [
            os.path.join(case_folder, case_id, f'{case_id}_MC.nii'),
            os.path.join(case_folder, case_id, f'{case_id}_MC.nii.gz'),
            os.path.join(case_folder, case_id, f'{case_id}_Updated_MC.nii'),
            os.path.join(case_folder, case_id, f'{case_id}_Updated_MC.nii.gz')
        ]
        
        mc_path = None
        for pattern in mc_patterns:
            if os.path.exists(pattern):
                mc_path = pattern
                break
        
        # Load GT1 (AS) file
        gt1_path = os.path.join(DATASET_PATHS['GT01_AS'], f'{case_id}_AS.nii')
        
        if mc_path and os.path.exists(gt1_path):
            print(f"MC file:  {mc_path}")
            print(f"GT1 file: {gt1_path}")
            
            # Load both files
            mc_img = load_nifti_safe(mc_path)
            gt1_img = load_nifti_safe(gt1_path)
            
            if mc_img is not None and gt1_img is not None:
                mc_data = mc_img.get_fdata()
                gt1_data = gt1_img.get_fdata()
                
                # Check file properties
                print(f"MC shape:  {mc_data.shape}")
                print(f"GT1 shape: {gt1_data.shape}")
                print(f"MC affine shape: {mc_img.affine.shape}")
                print(f"GT1 affine shape: {gt1_img.affine.shape}")
                
                # Check if shapes match
                if mc_data.shape == gt1_data.shape:
                    print("✓ Shapes match")
                    
                    # Check if data is identical
                    identical_check = np.allclose(mc_data, gt1_data, rtol=1e-10, atol=1e-10)
                    print(f"Data identical (strict): {identical_check}")
                    
                    # Check exact equality
                    exact_equal = np.array_equal(mc_data, gt1_data)
                    print(f"Data exactly equal: {exact_equal}")
                    
                    # Check differences
                    diff = np.abs(mc_data - gt1_data)
                    max_diff = np.max(diff)
                    mean_diff = np.mean(diff)
                    print(f"Max difference: {max_diff}")
                    print(f"Mean difference: {mean_diff}")
                    
                    # Check unique values
                    mc_unique = np.unique(mc_data)
                    gt1_unique = np.unique(gt1_data)
                    print(f"MC unique values: {mc_unique}")
                    print(f"GT1 unique values: {gt1_unique}")
                    
                    # Check affine matrices
                    affine_identical = np.allclose(mc_img.affine, gt1_img.affine)
                    print(f"Affine matrices identical: {affine_identical}")
                    
                    # File size comparison
                    mc_size = os.path.getsize(mc_path)
                    gt1_size = os.path.getsize(gt1_path)
                    print(f"MC file size: {mc_size} bytes")
                    print(f"GT1 file size: {gt1_size} bytes")
                    print(f"File sizes identical: {mc_size == gt1_size}")
                    
                    # Check if files are literally the same file (different paths to same file)
                    try:
                        mc_stat = os.stat(mc_path)
                        gt1_stat = os.stat(gt1_path)
                        same_inode = mc_stat.st_ino == gt1_stat.st_ino
                        print(f"Same inode (hard link): {same_inode}")
                    except:
                        print("Could not check inode")
                    
                    # Hash comparison (if files are small enough)
                    if mc_size < 100*1024*1024:  # Less than 100MB
                        import hashlib
                        
                        with open(mc_path, 'rb') as f:
                            mc_hash = hashlib.md5(f.read()).hexdigest()
                        
                        with open(gt1_path, 'rb') as f:
                            gt1_hash = hashlib.md5(f.read()).hexdigest()
                        
                        print(f"MC MD5:  {mc_hash}")
                        print(f"GT1 MD5: {gt1_hash}")
                        print(f"Hash identical: {mc_hash == gt1_hash}")
                    
                    # If data is identical, this explains the perfect Dice score
                    if exact_equal:
                        print("🚨 CONCLUSION: Files are IDENTICAL - this explains Dice = 1.0")
                        print("   This suggests GT1_AS might be a copy of the FDA reference")
                    else:
                        print("ℹ️  Files are different but very similar")
                        
                else:
                    print("✗ Shapes don't match")
            else:
                print("✗ Could not load one or both files")
        else:
            print(f"✗ Files not found:")
            print(f"   MC: {mc_path}")
            print(f"   GT1: {gt1_path}")

def check_directory_structure():
    """Check the directory structure to understand file organization."""
    print("\n" + "="*70)
    print("DIRECTORY STRUCTURE ANALYSIS")
    print("="*70)
    
    # Check FDA directory
    print("\nFDA_ORIGINAL directory structure:")
    if os.path.exists(DATASET_PATHS['FDA_ORIGINAL']):
        case_folders = [f for f in os.listdir(DATASET_PATHS['FDA_ORIGINAL']) if f.startswith('N-')]
        for case_folder in sorted(case_folders)[:3]:  # First 3 cases
            case_path = os.path.join(DATASET_PATHS['FDA_ORIGINAL'], case_folder)
            print(f"\n{case_folder}/")
            if os.path.isdir(case_path):
                for item in os.listdir(case_path):
                    item_path = os.path.join(case_path, item)
                    if os.path.isdir(item_path):
                        print(f"  {item}/")
                        for subitem in os.listdir(item_path):
                            print(f"    {subitem}")
                    else:
                        print(f"  {item}")
    
    # Check GT01 directory
    print(f"\nGT01_AS directory structure:")
    if os.path.exists(DATASET_PATHS['GT01_AS']):
        files = [f for f in os.listdir(DATASET_PATHS['GT01_AS']) if f.endswith('.nii')]
        for file in sorted(files):
            print(f"  {file}")
    
    # Check GT02 directory
    print(f"\nGT02_GM directory structure:")
    if os.path.exists(DATASET_PATHS['GT02_GM']):
        files = [f for f in os.listdir(DATASET_PATHS['GT02_GM']) if f.endswith('.nii')]
        for file in sorted(files):
            print(f"  {file}")

if __name__ == "__main__":
    analyze_file_identity()
    check_directory_structure()
    
    print("\n" + "="*70)
    print("SUMMARY")
    print("="*70)
    print("If MC and GT1 files are identical, this indicates:")
    print("1. GT1_AS annotations might be copies of FDA reference annotations")
    print("2. This would invalidate the inter-reader agreement analysis")
    print("3. True independent annotation from Reader AS may be missing")
    print("4. The study design needs to be reconsidered")
    print("="*70)