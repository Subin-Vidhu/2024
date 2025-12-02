# 📊 Comparison: process_new_aira_masks.py vs process_batch_storage_masks.py

**Date:** December 2, 2025

---

## 🔍 Key Differences

### **1. Input Path**

| File | Path |
|------|------|
| `process_new_aira_masks.py` | `K:/AIRA_FDA_Models/DATA/batch_storage` |
| `process_batch_storage_masks.py` | `G:\AIRA_Models_RESULTS\batch_storage` |

---

### **2. Reference Ground Truth**

| File | Reference GT Path |
|------|-------------------|
| `process_new_aira_masks.py` | `r'c:\Users\Subin-PC\Downloads\Telegram Desktop\OneDrive_1_10-8-2025'` (has reference) |
| `process_batch_storage_masks.py` | `None` (no reference, always uses LPI) |

**Impact:**
- **process_new_aira_masks.py**: Will try to match reference GT orientation if found
- **process_batch_storage_masks.py**: Always uses LPI orientation (no reference lookup)

---

### **3. Mask Filename Pattern**

| File | Pattern Handling |
|------|------------------|
| `process_new_aira_masks.py` | Hardcoded in `find_aira_mask_in_folder()` function: `"mask_model_checkpoint_664_0.6738.nii.gz"` (commented out other patterns) |
| `process_batch_storage_masks.py` | **Configurable variable:** `MASK_FILENAME_PATTERN = "mask_model_checkpoint_664_0.6738.nii.gz"` |

**Impact:**
- **process_new_aira_masks.py**: Pattern is embedded in code (harder to change)
- **process_batch_storage_masks.py**: Pattern is a config variable (easier to modify)

---

### **4. Label Mapping**

| File | Label Mapping | Comment |
|------|---------------|---------|
| `process_new_aira_masks.py` | ```python<br>LABEL_MAPPING_AIRA = {<br>    0: 0,  # Background<br>    1: 0,  # Noise → Background<br>    2: 2,  # AIRA label 2 (spatially RIGHT) → GT right (2)<br>    3: 1   # AIRA label 3 (spatially LEFT) → GT left (1)<br>}``` | Comments say: label 2 is RIGHT, label 3 is LEFT |
| `process_batch_storage_masks.py` | ```python<br>LABEL_MAPPING_AIRA = {<br>    0: 0,  # Background<br>    1: 0,  # Noise → Background<br>    2: 2,  # Left Kidney → stays as 2<br>    3: 1   # Right Kidney → becomes 1<br>}``` | Comments say: label 2 is LEFT, label 3 is RIGHT |

**⚠️ IMPORTANT:** The actual mapping code is **IDENTICAL** (`2→2, 3→1`), but the comments are **OPPOSITE**!

**Actual behavior:** Both files do the same thing:
- Label 2 → stays as 2
- Label 3 → becomes 1

---

### **5. Mask Finding Function**

| File | `find_aira_mask_in_folder()` Behavior |
|------|--------------------------------------|
| `process_new_aira_masks.py` | 1. Checks hardcoded pattern<br>2. Falls back to `*.nii.gz` or `*.nii`<br>3. Searches recursively in subdirectories |
| `process_batch_storage_masks.py` | 1. Checks `MASK_FILENAME_PATTERN` variable<br>2. Case-insensitive match<br>3. Pattern matching with `*mask_model_checkpoint*.nii.gz`<br>4. **Does NOT search recursively** |

**Impact:**
- **process_new_aira_masks.py**: More flexible, searches subdirectories
- **process_batch_storage_masks.py**: More focused, only looks in case folder root

---

### **6. Error Messages**

| File | Error Message Style |
|------|-------------------|
| `process_new_aira_masks.py` | `"⚠️  {case_id}: No AIRA mask found in folder"` |
| `process_batch_storage_masks.py` | `"⚠️  {case_id}: No mask file found matching pattern '{MASK_FILENAME_PATTERN}'"` |

**Impact:**
- **process_batch_storage_masks.py**: More specific error message (shows which pattern it's looking for)

---

### **7. Console Output**

| File | Output Details |
|------|---------------|
| `process_new_aira_masks.py` | Shows: Input path, Reference GT path, Timestamp |
| `process_batch_storage_masks.py` | Shows: Input path, **Mask filename pattern**, Reference GT path (or "None"), **Target orientation: LPI**, Label mapping, Timestamp |

**Impact:**
- **process_batch_storage_masks.py**: More informative startup output

---

### **8. Summary Output**

| File | Summary Details |
|------|----------------|
| `process_new_aira_masks.py` | Generic: "Spatial reorientation (when reference GT available)" |
| `process_batch_storage_masks.py` | Specific: "Reorientation to LPI orientation (default)" or "Spatial reorientation (when reference GT available)" |

---

## 📋 Summary Table

| Feature | process_new_aira_masks.py | process_batch_storage_masks.py |
|---------|---------------------------|--------------------------------|
| **Input Path** | `K:/AIRA_FDA_Models/DATA/batch_storage` | `G:\AIRA_Models_RESULTS\batch_storage` |
| **Reference GT** | Has path (tries to match) | None (always LPI) |
| **Mask Pattern** | Hardcoded in function | Config variable |
| **Label Mapping** | Same code, confusing comments | Same code, clearer comments |
| **Search Behavior** | Recursive subdirectory search | Only case folder root |
| **Error Messages** | Generic | Specific (shows pattern) |
| **Output Info** | Basic | More detailed |
| **Use Case** | General purpose, flexible | Specific to batch_storage, standardized |

---

## 🎯 Which File Should You Use?

### **Use `process_new_aira_masks.py` if:**
- ✅ You have reference GT files and want to match their orientation
- ✅ Masks might be in subdirectories
- ✅ You need flexibility in mask finding
- ✅ Working with `K:/AIRA_FDA_Models/DATA/batch_storage`

### **Use `process_batch_storage_masks.py` if:**
- ✅ Working with `G:\AIRA_Models_RESULTS\batch_storage`
- ✅ No reference GT available (always want LPI)
- ✅ Masks are always in case folder root (not subdirectories)
- ✅ Want standardized LPI orientation for all files
- ✅ Prefer configurable mask pattern variable

---

## ⚠️ Important Notes

1. **Label Mapping:** Both files have **identical mapping logic** (`2→2, 3→1`), but comments differ. The actual behavior is the same.

2. **Orientation:** 
   - `process_new_aira_masks.py` will match reference GT if available, otherwise LPI
   - `process_batch_storage_masks.py` always uses LPI (no reference GT)

3. **Mask Finding:**
   - `process_new_aira_masks.py` searches recursively (more flexible)
   - `process_batch_storage_masks.py` only searches case folder root (faster, more focused)

---

**Last Updated:** December 2, 2025

