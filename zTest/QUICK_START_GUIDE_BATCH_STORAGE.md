# 🚀 Quick Start Guide - Processing batch_storage Masks

**Date:** December 2, 2025  
**Folder:** `G:\AIRA_Models_RESULTS\batch_storage`

---

## ✅ What's Been Configured

The script `process_new_aira_masks.py` has been updated for your specific needs:

### **Configuration:**
- **Input Folder:** `G:\AIRA_Models_RESULTS\batch_storage`
- **Mask Pattern:** `mask_model_checkpoint_664_0.6738.nii.gz`
- **Label Mapping:**
  - Label 2 (Left Kidney) → stays as 2 ✅
  - Label 3 (Right Kidney) → becomes 1 ✅
- **Reference GT:** None (orientation detection only, no reorientation)

---

## 🎯 What It Will Do

For each subfolder (e.g., `N-001`, `N-002`, etc.):

1. ✅ **Find** the file `mask_model_checkpoint_664_0.6738.nii.gz`
2. ✅ **Detect** the orientation of the mask
3. ✅ **Remap labels:**
   - Label 3 (Right Kidney) → Label 1
   - Label 2 (Left Kidney) → Label 2 (unchanged)
4. ✅ **Save** processed file as `mask_model_checkpoint_664_0.6738_processed.nii`
5. ✅ **Create backup** of original (if enabled)

---

## 📝 How to Run

### **Step 1: Verify Configuration**
Open `process_new_aira_masks.py` and check lines 32-47:

```python
NEW_AIRA_PATH = r"G:\AIRA_Models_RESULTS\batch_storage"
MASK_FILENAME_PATTERN = "mask_model_checkpoint_664_0.6738.nii.gz"
LABEL_MAPPING_AIRA = {
    0: 0,  # Background
    1: 0,  # Noise → Background
    2: 2,  # Left Kidney → stays 2
    3: 1   # Right Kidney → becomes 1
}
```

### **Step 2: Run the Script**
```bash
cd d:\2024\zTest
python process_new_aira_masks.py
```

### **Step 3: Check Output**
Processed files will be saved in each case folder:
- `G:\AIRA_Models_RESULTS\batch_storage\N-001\mask_model_checkpoint_664_0.6738_processed.nii`
- `G:\AIRA_Models_RESULTS\batch_storage\N-002\mask_model_checkpoint_664_0.6738_processed.nii`
- etc.

---

## 📊 Expected Output

### **Console Output:**
```
======================================================================
PROCESS NEW AIRA MASKS - COMPLETE PREPROCESSING PIPELINE
======================================================================
Input path: G:\AIRA_Models_RESULTS\batch_storage
Mask filename pattern: mask_model_checkpoint_664_0.6738.nii.gz
Reference GT path: None (orientation detection only)
Label mapping: {0: 0, 1: 0, 2: 2, 3: 1}
======================================================================

🔍 Scanning for AIRA cases...
✓ Found X case folders

============================================================
Processing: N-001
============================================================
  📂 Loading AIRA mask: mask_model_checkpoint_664_0.6738.nii.gz
    Shape: (512, 512, Z)
    Data type: float32
    Orientation: RAS (or LPI, etc.)
    Original unique values: [0. 2. 3.]
  🏷️  Applying label remapping
    Original labels: [0. 2. 3.]
    After remapping: [0 1 2]
  💾 Saving processed mask: mask_model_checkpoint_664_0.6738_processed.nii
    ✓ Saved successfully (X.XX MB)
  ✅ Processing complete for N-001
```

---

## 🔍 Verify Results

### **Check Label Values:**
After processing, verify the labels are correct:
- Label 0 = Background ✅
- Label 1 = Right Kidney ✅ (was label 3)
- Label 2 = Left Kidney ✅ (was label 2)

### **Check Orientation:**
The script will display the orientation for each file (e.g., "RAS", "LPI", "LPS")

---

## ⚙️ Optional: Add Reference for Reorientation

If you want to reorient masks to match a reference orientation:

1. Set `GROUND_TRUTH_REFERENCE_PATH` to your reference folder
2. The script will reorient each mask to match the reference

Example:
```python
GROUND_TRUTH_REFERENCE_PATH = r"G:\path\to\reference\masks"
```

---

## 🆘 Troubleshooting

### **Issue: "No case folders found"**
- Check that `NEW_AIRA_PATH` is correct
- Verify the folder exists and contains subfolders

### **Issue: "Mask file not found"**
- Check that `MASK_FILENAME_PATTERN` matches your files exactly
- The script looks for: `mask_model_checkpoint_664_0.6738.nii.gz`

### **Issue: "Error loading file"**
- Check file permissions
- Verify files are not corrupted
- Check disk space

---

## 📋 Summary

**Input:** `mask_model_checkpoint_664_0.6738.nii.gz` with labels (0, 2, 3)  
**Output:** `mask_model_checkpoint_664_0.6738_processed.nii` with labels (0, 1, 2)

**Label Changes:**
- Background (0) → Background (0) ✅
- Left Kidney (2) → Left Kidney (2) ✅
- Right Kidney (3) → Right Kidney (1) ✅

**Ready to use!** 🎉

