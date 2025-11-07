# 📘 REFERENCE GUIDE - Kidney Segmentation Dice Score Analysis
## zTest Folder - Label Conventions & Code Documentation

**Created:** November 7, 2025  
**Purpose:** Master reference for all dice score calculation codes and label conventions  
**⚠️ READ THIS FIRST before using any scripts in this folder**

---

## 📋 Table of Contents
1. [Label Convention Summary](#label-convention-summary)
2. [Script Inventory & Usage](#script-inventory--usage)
3. [Dice Coefficient Implementations](#dice-coefficient-implementations)
4. [Recent Changes & Fixes](#recent-changes--fixes)
5. [Quick Reference Table](#quick-reference-table)

---

## 🏷️ Label Convention Summary

### Two Different Label Conventions Used:

#### **Convention A: Anatomical (FDA Scripts)**
**Used in:** `fda_single_case_dice.py`, `fda_multiple_case_dice.py` (older scripts)
```
Label 0 = Background
Label 1 = LEFT Kidney (anatomical left)
Label 2 = RIGHT Kidney (anatomical right)
```
**Rationale:** Standard anatomical naming convention

---

#### **Convention B: Radiologist's View (Annotator Comparison Scripts)**
**Used in:** `compare_two_annotators.py`, `batch_compare_annotators.py` (current scripts)
```
Label 0 = Background
Label 1 = RIGHT Kidney (patient's right side, left on screen)
Label 2 = LEFT Kidney (patient's left side, right on screen)
```
**Rationale:** Radiologists view images from the front of the patient, so left/right are flipped
**Spatial verification:** In LPI orientation, lower X coordinates (~155) = patient's right side

---

## 📂 Script Inventory & Usage

### **1. Annotator Comparison Scripts (CURRENT - USE THESE)**

#### `batch_compare_annotators.py` ⭐ **RECOMMENDED**
**Purpose:** Batch processing for comparing two annotators across multiple cases  
**Label Convention:** Radiologist's View (Label 1 = Right, Label 2 = Left)  
**Dice Method:** FDA-compliant with boolean logic operations  
**Date:** November 7, 2025 (Latest)

**Features:**
- ✅ Processes entire folders automatically
- ✅ Generates single CSV with all cases
- ✅ 4 rows per case: Right Kidney, Left Kidney, Both Kidneys, Average
- ✅ Both "Both Kidneys" and "Average" use UNION method
- ✅ Volumes in both mm³ and cm³
- ✅ Radiologist's perspective documented

**Configuration:**
```python
BATCH_ROOT_DIR = r'c:\Users\Subin-PC\Downloads\Telegram Desktop\dice_run\dice_run'
ANNOTATOR_1_PATTERN = '*_AS.nii'
ANNOTATOR_2_PATTERN = '*_GM.nii'
OUTPUT_DIR = r'd:\2024\zTest\results\batch_annotator_comparison'
```

**CSV Output Format:**
| Column | Description |
|--------|-------------|
| Patient | Case number (e.g., 071) |
| Mask1 | Annotator 1 filename |
| Mask2 | Annotator 2 filename |
| Organ | Right Kidney / Left Kidney / Both Kidneys / XXX Average |
| DiceCoefficient | Dice score (6 decimals) |
| Mask1_Volume_mm3 | Annotator 1 volume in mm³ |
| Mask2_Volume_mm3 | Annotator 2 volume in mm³ |
| Mask1_Volume_cm3 | Annotator 1 volume in cm³ |
| Mask2_Volume_cm3 | Annotator 2 volume in cm³ |
| DiffPercent | Volume difference % (e.g., "1.92%") |
| LargerMask | Mask1 or Mask2 |
| Error | Error message if any |

**Usage:**
```bash
# Edit the configuration paths at the top of the file
python batch_compare_annotators.py
```

---

#### `compare_two_annotators.py`
**Purpose:** Single case comparison between two annotators  
**Label Convention:** Radiologist's View (Label 1 = Right, Label 2 = Left)  
**Dice Method:** FDA-compliant with boolean logic operations  
**Date:** November 7, 2025

**Features:**
- ✅ Single case processing
- ✅ Detailed console output with spatial analysis
- ✅ CSV + text report generation
- ✅ Same label convention as batch script

**Configuration:**
```python
ANNOTATOR_1_PATH = r'path\to\annotator1\mask.nii'
ANNOTATOR_2_PATH = r'path\to\annotator2\mask.nii'
CASE_ID = 'N-071'
OUTPUT_DIR = r'd:\2024\zTest\results\annotator_comparison'
```

**Usage:**
```bash
# Edit the three paths at the top of the file
python compare_two_annotators.py
```

---

### **2. FDA Analysis Scripts (AIRA AI Validation)**

#### `fda_multi_reader_analysis.py` ⭐ **MOST COMPREHENSIVE**
**Purpose:** Multi-reader inter-observer agreement analysis for FDA submission  
**Label Convention:** Mixed (Human: Label 1 = Left, AIRA: remapped)  
**Dice Method:** FDA-compliant enhanced version (BEST implementation)  
**Date:** October 21, 2025  
**Lines:** 1510

**Features:**
- ✅ Multi-reader validation (3+ annotators)
- ✅ FDA AI/ML SaMD compliance
- ✅ Statistical validation (power analysis, confidence intervals)
- ✅ Advanced visualizations
- ✅ Excel reports
- ✅ AIRA AI performance analysis

**Label Mappings:**
```python
# Human readers (FDA, AS, GM):
LABEL_MAPPING_HUMAN = {
    0: 0,  # Background
    1: 1,  # LEFT Kidney
    2: 2   # RIGHT Kidney
}

# AIRA (needs remapping due to spatial mismatch):
LABEL_MAPPING_AIRA = {
    0: 0,  # Background
    1: 0,  # Noise → Background
    2: 2,  # AIRA label 2 (spatially RIGHT) → GT right (2)
    3: 1   # AIRA label 3 (spatially LEFT) → GT left (1)
}
```

---

#### `fda_multiple_case_dice.py` ⭐ **FDA-COMPLIANT (BEST DICE)**
**Purpose:** Batch FDA validation with enhanced metrics  
**Label Convention:** Anatomical (Label 1 = Left, Label 2 = Right)  
**Dice Method:** FDA-compliant enhanced with boolean logic ✅ **BEST**  
**Date:** October 29, 2025 (Int16 fix applied)  
**Lines:** 1921

**Features:**
- ✅ **Enhanced Dice coefficient** (boolean logic, explicit casting, value clamping)
- ✅ FDA compliance features (confidence intervals, power analysis)
- ✅ Int16 fix for exact integer labels
- ✅ Batch processing
- ✅ Excel report generation

**Dice Implementation (GOLD STANDARD):**
```python
def dice_coefficient(y_true, y_pred, epsilon=1e-6):
    """FDA-compliant Dice coefficient calculation."""
    # Input validation
    if y_true.shape != y_pred.shape:
        raise ValueError("Ground truth and prediction must have identical shapes")
    
    # Convert to binary masks with explicit casting
    y_true_bin = y_true.astype(np.bool_)
    y_pred_bin = y_pred.astype(np.bool_)
    
    # Calculate using logical operations for accuracy
    intersection = np.sum(y_true_bin & y_pred_bin)  # Boolean AND
    sum_true = np.sum(y_true_bin)
    sum_pred = np.sum(y_pred_bin)
    
    # Handle edge cases per FDA requirements
    if sum_true == 0 and sum_pred == 0:
        return 1.0  # Perfect agreement on empty regions
    elif sum_true == 0 or sum_pred == 0:
        return 0.0  # No overlap possible
    
    # Standard Sørensen-Dice formula with numerical stability
    dice = (2.0 * intersection + epsilon) / (sum_true + sum_pred + epsilon)
    
    return np.clip(dice, 0.0, 1.0)  # Ensure valid range [0,1]
```

---

#### `fda_single_case_dice.py`
**Purpose:** Single case FDA validation  
**Label Convention:** Anatomical (Label 1 = Left, Label 2 = Right)  
**Dice Method:** Simple (multiplication-based) ⚠️ Less robust  
**Date:** October 29, 2025 (Int16 fix applied)  
**Lines:** 297

**Features:**
- ✅ Single case analysis
- ✅ Spatial overlap analysis
- ✅ Volume comparison
- ✅ Int16 fix applied
- ⚠️ Uses simpler Dice calculation

**Dice Implementation (SIMPLE):**
```python
def dice_coefficient(y_true, y_pred, epsilon=1e-6):
    """Simple Dice coefficient."""
    intersection = np.sum(y_true * y_pred)  # Multiplication
    union = np.sum(y_true) + np.sum(y_pred)
    if np.sum(y_true) == 0 and np.sum(y_pred) == 0:
        return 1.0
    return (2. * intersection + epsilon) / (union + epsilon)
```

---

### **3. Older Scripts (Reference Only)**

#### `dice_score_single_case.py`
**Status:** ⚠️ OUTDATED (October 11, 2025)  
**Issues:** No orientation handling, no label remapping, no int16 fix  
**Use:** Reference only, do not use for new analysis

#### `dice_score_multiple.py`
**Status:** ⚠️ VERY OUTDATED (August 20, 2024)  
**Issues:** Pre-dates all major fixes, would produce incorrect results  
**Use:** Historical reference only

#### `mean_dice.py`
**Status:** ⚠️ OLDEST (July 30, 2024)  
**Issues:** Basic implementation, no modern fixes  
**Use:** Historical reference only

---

### **4. Utility Scripts**

#### `process_new_aira_masks.py`
**Purpose:** Complete preprocessing pipeline for AIRA predictions  
**Date:** October 29, 2025

**Features:**
- ✅ Spatial reorientation to match ground truth
- ✅ Label remapping (AIRA → Human convention)
- ✅ Int16 conversion for exact integers
- ✅ Batch processing

---

## 🧮 Dice Coefficient Implementations

### **Method Comparison:**

| Script | Method | Boolean Logic | Edge Cases | Value Clamp | FDA Compliant |
|--------|--------|---------------|------------|-------------|---------------|
| `batch_compare_annotators.py` | Enhanced | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| `compare_two_annotators.py` | Enhanced | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| `fda_multiple_case_dice.py` | Enhanced | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes ⭐ |
| `fda_multi_reader_analysis.py` | Enhanced | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| `fda_single_case_dice.py` | Simple | ❌ No | ⚠️ Basic | ❌ No | ⚠️ Partial |
| Older scripts | Simple | ❌ No | ❌ No | ❌ No | ❌ No |

**Recommendation:** Use enhanced method (boolean logic) for all new work.

---

### **"Both Kidneys" Calculation Methods:**

#### **Union Method (CURRENT - Used in batch scripts):**
```python
# Combine all kidney voxels first
both_kidneys_mask1 = ((data1 == 1) | (data1 == 2)).astype(np.float32)
both_kidneys_mask2 = ((data2 == 1) | (data2 == 2)).astype(np.float32)

# Then calculate Dice on combined regions
dice_both = dice_coefficient(both_kidneys_mask1, both_kidneys_mask2)
```

**Formula:** `Dice = 2 × |A_Both ∩ B_Both| / (|A_Both| + |B_Both|)`  
Where: `A_Both = A_Right ∪ A_Left`

**Advantage:** Treats both kidneys as one region, single unified metric

---

#### **Averaging Method (Alternative - not used):**
```python
# Calculate Dice for each kidney separately
dice_right = dice_coefficient(mask1_right, mask2_right)
dice_left = dice_coefficient(mask1_left, mask2_left)

# Then average the scores
dice_avg = (dice_right + dice_left) / 2
```

**Formula:** `Dice_avg = (Dice_Right + Dice_Left) / 2`

**Advantage:** Shows average performance across kidneys

**Note:** Union method typically gives slightly different (usually slightly higher) values than averaging.

---

## 🔧 Recent Changes & Fixes

### **November 7, 2025 - Annotator Comparison Scripts**
✅ Created `compare_two_annotators.py` - Single case comparison  
✅ Created `batch_compare_annotators.py` - Batch processing  
✅ Implemented radiologist's perspective label convention  
✅ Fixed label mapping: Label 1 = Right, Label 2 = Left  
✅ Updated Row 4 (Average) to use union method instead of averaging  
✅ Fixed LargerMask column to show "Equal" when volumes are identical  
✅ Added comprehensive documentation

### **October 29, 2025 - Int16 Fix**
✅ Fixed floating-point precision bug in all FDA scripts  
✅ Changed `remap_labels()` to return `np.int16` instead of `float`  
✅ Ensures exact integer labels [0, 1, 2]  
✅ Created verification and test scripts  
✅ All scripts validated and passing tests

**Files Fixed:**
- `fda_multiple_case_dice.py`
- `fda_single_case_dice.py`
- `fda_multi_reader_analysis.py`
- `test_corrected_mapping.py`
- `comprehensive_mask_analysis.py`
- `validate_labels.py`

### **October 21, 2025 - Spatial Orientation Fix**
✅ Fixed 0.0000 Dice issue (orientation mismatch)  
✅ Implemented `reorient_to_match()` function  
✅ Fixed label mapping confusion (spatial vs naming)  
✅ AIRA performance improved from 0.0 to ~0.908 Dice  
✅ Created comprehensive multi-reader analysis

---

## 📊 Quick Reference Table

### **Which Script Should I Use?**

| Task | Recommended Script | Alternative |
|------|-------------------|-------------|
| **Compare 2 annotators (batch)** | `batch_compare_annotators.py` ⭐ | - |
| **Compare 2 annotators (single)** | `compare_two_annotators.py` | - |
| **FDA AI validation (multi-reader)** | `fda_multi_reader_analysis.py` ⭐ | - |
| **FDA AI validation (batch)** | `fda_multiple_case_dice.py` | - |
| **FDA AI validation (single)** | `fda_multiple_case_dice.py` | `fda_single_case_dice.py` |
| **Preprocess AIRA masks** | `process_new_aira_masks.py` | - |

---

### **Label Convention Quick Reference:**

| Script Type | Label 0 | Label 1 | Label 2 | View Perspective |
|------------|---------|---------|---------|------------------|
| **Annotator Comparison** | Background | RIGHT Kidney | LEFT Kidney | Radiologist (from front) |
| **FDA Analysis (Human)** | Background | LEFT Kidney | RIGHT Kidney | Anatomical |
| **FDA Analysis (AIRA)** | Background | Noise→BG | RIGHT (spatial) | Needs remapping |

---

### **Dice Method Quick Reference:**

| Method | Formula | When to Use |
|--------|---------|-------------|
| **Enhanced (Boolean)** | `intersection = np.sum(y_true_bin & y_pred_bin)` | ✅ All new work |
| **Simple (Multiplication)** | `intersection = np.sum(y_true * y_pred)` | ⚠️ Legacy only |

---

## 🎯 Best Practices

1. **Always use the latest scripts** from November 2025
2. **Use boolean logic Dice** (enhanced method) for all new analysis
3. **Document label convention** clearly in any new scripts
4. **Verify spatial orientation** before comparing masks
5. **Use int16 data type** for segmentation labels
6. **Include preprocessing** (reorientation, label mapping) in pipeline
7. **Test on single case first** before batch processing

---

## 📝 File Naming Conventions

### **Ground Truth Files:**
- FDA/MC: `N-XXX_MC.nii` or `N-XXX_Updated_MC.nii`
- AS (Annotator 1): `N-XXX_AS.nii` or `N-XXX_Updated_AS.nii`
- GM (Annotator 2): `N-XXX_GM.nii` or `N-XXX_Updated_GM.nii`

### **AIRA Predictions:**
- Original: `mask.nii` or `N-XXX_AIRA.nii`
- Processed: `mask_processed.nii` or `N-XXX_AIRA_processed.nii`

---

## 🔗 Related Documentation

- `FINAL_SUMMARY_FDA_ANALYSIS.md` - FDA multi-reader analysis summary
- `INT16_FIX_VERIFICATION_REPORT.md` - Int16 fix verification
- `FDA_AIRA_Metrics_Documentation.md` - Metrics explanation
- `FDA_Compliance_Documentation.md` - FDA compliance features
- `CORRECTIONS_SUMMARY.md` - Historical fixes

---

## 📞 Support & Questions

For questions about:
- **Label conventions:** Check this document's Label Convention Summary section
- **Dice calculations:** Check the Dice Coefficient Implementations section
- **FDA compliance:** See `FDA_Compliance_Documentation.md`
- **Recent changes:** Check the Recent Changes & Fixes section

---

**Last Updated:** November 7, 2025  
**Maintained By:** Medical AI Validation Team  
**Status:** ✅ Current and Active

---

## 🚀 Quick Start Examples

### Example 1: Compare Two Annotators (Batch)
```bash
# 1. Edit batch_compare_annotators.py
BATCH_ROOT_DIR = r'path\to\your\data'
ANNOTATOR_1_PATTERN = '*_AS.nii'
ANNOTATOR_2_PATTERN = '*_GM.nii'

# 2. Run
python batch_compare_annotators.py

# 3. Results saved to:
# d:\2024\zTest\results\batch_annotator_comparison\Batch_Annotator_Comparison_TIMESTAMP.csv
```

### Example 2: FDA Multi-Reader Analysis
```bash
# 1. Ensure data is in correct folders
# 2. Edit fda_multi_reader_analysis.py configuration
# 3. Run
python fda_multi_reader_analysis.py

# 4. Results include:
# - Excel report with comprehensive metrics
# - Visualizations (plots, heatmaps)
# - Statistical validation
```

### Example 3: Single Case Comparison
```bash
# 1. Edit compare_two_annotators.py
ANNOTATOR_1_PATH = r'path\to\case\annotator1.nii'
ANNOTATOR_2_PATH = r'path\to\case\annotator2.nii'
CASE_ID = 'N-071'

# 2. Run
python compare_two_annotators.py

# 3. Results:
# - CSV with metrics
# - Detailed text report
# - Console output with analysis
```

---

**⭐ Remember:** This is the MASTER REFERENCE document. Update it when making changes to label conventions or adding new scripts!
