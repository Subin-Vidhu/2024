# 📋 File Summary & Recommendations for Your Task

**Date:** November 2025  
**Your Task:** Convert masks with labels (2=left, 3=right) to (1=right, 2=left) and detect orientation

---

## 🎯 Your Current Requirement

**Input Masks:**
- Label 0 = Background
- Label 2 = Left Kidney
- Label 3 = Right Kidney

**Desired Output:**
- Label 0 = Background  
- Label 1 = Right Kidney (converted from label 3)
- Label 2 = Left Kidney (stays as label 2)

**Also Need:** Detect orientation of masks

---

## 📂 Complete File Inventory & What Each Does

### **⭐ RECOMMENDED FOR YOUR TASK**

#### 1. **`process_new_aira_masks.py`** ⭐ **BEST MATCH**
**Purpose:** Complete preprocessing pipeline - reorientation + label remapping  
**Date:** October 29, 2025  
**Lines:** 581

**What it does:**
- ✅ Finds masks in subfolders recursively
- ✅ Detects orientation of each mask
- ✅ Reorients masks to match reference (if provided)
- ✅ Remaps labels (currently maps AIRA labels 2→2, 3→1)
- ✅ Handles floating-point precision issues
- ✅ Batch processes entire folder structures
- ✅ Creates backups
- ✅ Saves processed files with `_processed` suffix

**Current Label Mapping:**
```python
LABEL_MAPPING_AIRA = {
    0: 0,  # Background → Background
    1: 0,  # Noise → Background
    2: 2,  # AIRA label 2 → Left Kidney (2)
    3: 1   # AIRA label 3 → Right Kidney (1)
}
```

**⚠️ NOTE:** This mapping matches your requirement EXACTLY! (3→1, 2→2)

**How to use:**
1. Edit configuration at top:
   ```python
   NEW_AIRA_PATH = r"path\to\your\folder\with\subfolders"
   GROUND_TRUTH_REFERENCE_PATH = r"path\to\reference\for\orientation"  # Optional
   ```
2. Run: `python process_new_aira_masks.py`
3. Output: Processed files saved in same folders with `_processed.nii` suffix

**Pros:**
- ✅ Handles subfolders automatically
- ✅ Detects orientation
- ✅ Can reorient to match reference
- ✅ Robust label remapping
- ✅ Batch processing

**Cons:**
- ⚠️ Needs reference GT for reorientation (optional though)

---

#### 2. **`batch_reorient_nifti.py`** 
**Purpose:** Batch reorientation to target orientation  
**Date:** Recent  
**Lines:** 375

**What it does:**
- ✅ Finds NIfTI files recursively in subfolders
- ✅ Detects current orientation
- ✅ Reorients to target orientation (e.g., "LPS", "RAS")
- ✅ Saves reoriented files
- ✅ Can skip files already in target orientation

**How to use:**
1. Edit configuration:
   ```python
   INPUT_FOLDER = r"path\to\your\folder"
   FILE_PATTERN = "*.nii"  # or specific pattern
   TARGET_ORIENTATION = "LPS"  # or "RAS", "LPI", etc.
   RECURSIVE_SEARCH = True
   ```
2. Run: `python batch_reorient_nifti.py`

**Use Case:** If you only need reorientation (no label remapping)

---

### **🔍 ANALYSIS & VALIDATION TOOLS**

#### 3. **`comprehensive_mask_analysis.py`**
**Purpose:** Detailed analysis of mask files  
**Date:** October 2025  
**Lines:** 202

**What it does:**
- ✅ Loads and analyzes mask files
- ✅ Shows unique values, distributions
- ✅ Detects floating-point precision issues
- ✅ Applies label remapping and shows results
- ✅ Volume analysis

**Use Case:** Check your masks before/after processing

---

#### 4. **`validate_labels.py`**
**Purpose:** Validate label mappings  
**Date:** October 2025  
**Lines:** 204

**What it does:**
- ✅ Validates label remapping logic
- ✅ Checks for correct assignments
- ✅ Tests with synthetic data

**Use Case:** Verify your label mapping is correct

---

#### 5. **`check_labels_temp.py`**
**Purpose:** Quick label checking script  
**Date:** Recent  
**Lines:** 53

**What it does:**
- ✅ Loads two masks
- ✅ Shows unique values
- ✅ Shows label counts
- ✅ Spatial location analysis (X-coordinates)

**Use Case:** Quick check of labels in masks

---

### **📊 DICE SCORE CALCULATION SCRIPTS**

#### 6. **`batch_compare_annotators.py`** ⭐ **LATEST (Nov 7, 2025)**
**Purpose:** Batch comparison of two annotators  
**Lines:** 556

**What it does:**
- ✅ Batch processes folders
- ✅ Compares two annotators
- ✅ Calculates Dice scores
- ✅ Generates CSV reports
- ✅ Uses radiologist's view convention (Label 1=Right, Label 2=Left)

**Label Convention:** Radiologist's view (Label 1=Right, Label 2=Left)

---

#### 7. **`compare_two_annotators.py`**
**Purpose:** Single case annotator comparison  
**Date:** November 7, 2025  
**Lines:** 492

**What it does:**
- ✅ Single case comparison
- ✅ Detailed console output
- ✅ CSV + text report
- ✅ Same label convention as batch script

---

#### 8. **`fda_multiple_case_dice.py`** ⭐ **FDA-COMPLIANT**
**Purpose:** FDA-compliant batch validation  
**Date:** October 29, 2025  
**Lines:** 1921

**What it does:**
- ✅ FDA-compliant Dice calculation
- ✅ Enhanced metrics
- ✅ Excel reports
- ✅ Statistical validation

**Label Convention:** Anatomical (Label 1=Left, Label 2=Right)

---

#### 9. **`fda_single_case_dice.py`**
**Purpose:** Single case FDA validation  
**Date:** October 29, 2025  
**Lines:** 297

**What it does:**
- ✅ Single case analysis
- ✅ Spatial overlap analysis
- ✅ Volume comparison

---

#### 10. **`fda_multi_reader_analysis.py`** ⭐ **MOST COMPREHENSIVE**
**Purpose:** Multi-reader inter-observer agreement  
**Date:** October 21, 2025  
**Lines:** 1510

**What it does:**
- ✅ Multi-reader validation (3+ annotators)
- ✅ FDA AI/ML SaMD compliance
- ✅ Statistical validation
- ✅ Advanced visualizations
- ✅ Excel reports

---

### **🛠️ UTILITY SCRIPTS**

#### 11. **`check_file_format.py`**
**Purpose:** Check NIfTI file format  
**Lines:** 49

**What it does:**
- ✅ Validates NIfTI file format
- ✅ Checks data types

---

#### 12. **`validate_anatomy.py`**
**Purpose:** Validate anatomical correctness  
**Lines:** 146

**What it does:**
- ✅ Checks anatomical validity
- ✅ Validates spatial relationships

---

#### 13. **`validate_file_naming.py`**
**Purpose:** Validate file naming conventions  
**Lines:** 249

**What it does:**
- ✅ Checks file naming patterns
- ✅ Validates naming conventions

---

### **📁 ARCHIVE & CLEANUP**

#### 14. **`create_mask_archive.py`**
**Purpose:** Create archive of masks  
**Lines:** 297

#### 15. **`create_processed_mask_archive.py`**
**Purpose:** Archive processed masks  
**Lines:** 362

#### 16. **`cleanup_aira_folders.py`**
**Purpose:** Clean up AIRA folders  
**Lines:** 301

---

### **🧪 TEST SCRIPTS**

#### 17. **`test_corrected_mapping.py`**
**Purpose:** Test label mapping corrections  
**Lines:** 120

#### 18. **`test_int16_functionality.py`**
**Purpose:** Test int16 functionality  
**Lines:** 147

#### 19. **`test_comprehensive_functionality.py`**
**Purpose:** Comprehensive functionality tests  
**Lines:** 142

---

## 🎯 RECOMMENDED SOLUTION FOR YOUR TASK

### **Option 1: Use Existing Script (EASIEST)** ⭐

**Use `process_new_aira_masks.py`** - It already does exactly what you need!

**Steps:**
1. Open `process_new_aira_masks.py`
2. Edit these lines at the top:
   ```python
   NEW_AIRA_PATH = r"D:\path\to\your\folder\with\subfolders"
   GROUND_TRUTH_REFERENCE_PATH = r"path\to\reference"  # Optional - for reorientation
   ```
3. The label mapping is already correct:
   ```python
   LABEL_MAPPING_AIRA = {
       0: 0,  # Background
       1: 0,  # Noise → Background (if present)
       2: 2,  # Left Kidney (stays 2)
       3: 1   # Right Kidney → becomes 1 ✓
   }
   ```
4. Run: `python process_new_aira_masks.py`
5. Output: Files saved as `*_processed.nii` in same folders

**What it will do:**
- ✅ Find all `.nii` files in subfolders
- ✅ Detect orientation of each file
- ✅ Reorient to match reference (if provided)
- ✅ Remap labels: 3→1, 2→2
- ✅ Save processed files

---

### **Option 2: Create Custom Script (MORE CONTROL)**

If you want more control or don't need reorientation, I can create a custom script that:
- Finds all masks in subfolders
- Detects orientation
- Remaps labels (3→1, 2→2)
- Saves processed files

**Would you like me to create this?**

---

## 📝 Quick Reference: What Each Script Does

| Script | Purpose | Orientation Detection | Label Remapping | Batch Processing |
|--------|---------|----------------------|-----------------|------------------|
| `process_new_aira_masks.py` | ⭐ Complete preprocessing | ✅ Yes | ✅ Yes | ✅ Yes |
| `batch_reorient_nifti.py` | Reorientation only | ✅ Yes | ❌ No | ✅ Yes |
| `comprehensive_mask_analysis.py` | Analysis only | ❌ No | ✅ Yes (test) | ❌ No |
| `batch_compare_annotators.py` | Dice comparison | ✅ Yes | ❌ No | ✅ Yes |
| `fda_multiple_case_dice.py` | FDA validation | ✅ Yes | ✅ Yes | ✅ Yes |

---

## 🔧 Your Specific Label Mapping

**Current:** `{0: Background, 2: Left Kidney, 3: Right Kidney}`  
**Desired:** `{0: Background, 1: Right Kidney, 2: Left Kidney}`

**Mapping Required:**
```python
LABEL_MAPPING = {
    0: 0,  # Background stays
    2: 2,  # Left Kidney stays as 2
    3: 1   # Right Kidney → becomes 1
}
```

**Note:** If your masks have label 1 (noise), you may want:
```python
LABEL_MAPPING = {
    0: 0,  # Background
    1: 0,  # Noise → Background (if present)
    2: 2,  # Left Kidney
    3: 1   # Right Kidney → 1
}
```

---

## ✅ RECOMMENDATION

**Use `process_new_aira_masks.py`** - It's perfect for your needs!

1. It handles subfolders automatically
2. Detects orientation
3. Has the exact label mapping you need (3→1, 2→2)
4. Batch processes everything
5. Creates backups
6. Handles edge cases

**Just edit the paths and run it!**

---

**Last Updated:** November 2025  
**Status:** ✅ Ready to use

