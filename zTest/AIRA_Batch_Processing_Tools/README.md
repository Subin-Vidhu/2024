# AIRA Batch Processing Tools

**Complete suite of automated tools for AIRA kidney segmentation mask processing and FDA validation analysis**

---

## 📋 Overview

This folder contains **7 production tools** and **1 test utility** designed for batch processing AIRA AI-generated kidney segmentation masks for FDA compliance validation. These tools handle the complete workflow from raw AIRA masks to FDA-ready validated results.

**Creation Date:** October 29, 2025  
**Last Updated:** December 2, 2025  
**Purpose:** FDA AI/ML Software as a Medical Device (SaMD) Validation  
**Dataset:** AIRA kidney segmentation predictions (SET_2_LIVE)  

---

## 🛠️ Tools Included

### 1. `process_batch_storage_masks.py` - Batch Storage Mask Processor ⭐ **NEW**
**Purpose:** Complete preprocessing pipeline for batch_storage masks with volume CSV export

**What it does:**
- Processes AIRA masks from `G:\AIRA_Models_RESULTS\batch_storage` folder
- Handles specific mask pattern: `mask_model_checkpoint_664_0.6738.nii.gz`
- **Automatically applies LPI orientation** (standardized output)
- Applies label remapping: {2→2, 3→1} (Left stays, Right becomes 1)
- Uses int16 data type for exact integer labels
- **Exports volume CSV** with Case Name, Right Kidney Volume, Left Kidney Volume
- Saves processed masks ready for analysis

**Key Features:**
- ✅ **Configurable mask pattern:** Easy to change target filename
- ✅ **LPI orientation:** Always standardizes to LPI (no reference GT needed)
- ✅ **Label remapping:** Converts labels 3→1, 2→2
- ✅ **Volume calculation:** Calculates kidney volumes in cm³
- ✅ **CSV export:** Automatically generates volume report in results folder
- ✅ **Timestamped output:** Creates timestamped subfolder for each run
- ✅ **int16 precision:** Ensures exact integer values (0, 1, 2)
- ✅ **Detailed logging:** Shows each processing step

**Label Mapping:**
```python
LABEL_MAPPING_AIRA = {
    0: 0,  # Background → Background
    1: 0,  # Noise (if present) → Background
    2: 2,  # Left Kidney → stays as 2
    3: 1   # Right Kidney → becomes 1
}
```

**Configuration:**
```python
# Input path
NEW_AIRA_PATH = r"G:\AIRA_Models_RESULTS\batch_storage"

# Mask filename pattern
MASK_FILENAME_PATTERN = "mask_model_checkpoint_664_0.6738.nii.gz"

# Reference GT (optional - set to None for LPI default)
GROUND_TRUTH_REFERENCE_PATH = None

# Label mapping
LABEL_MAPPING_AIRA = {0: 0, 1: 0, 2: 2, 3: 1}
```

**Usage:**
```bash
python process_batch_storage_masks.py
```

**Output:**
- Processed masks: `*_processed.nii` in each case folder
- Volume CSV: `results/Batch_Storage_Volumes_TIMESTAMP/Kidney_Volumes_TIMESTAMP.csv`

**CSV Format:**
```csv
Case Name,Right Kidney Volume (cm³),Left Kidney Volume (cm³)
N-001,125.45,118.32
N-002,132.18,129.67
...
```

**Example Output:**
```
Processing: N-001
  📂 Loading AIRA mask: mask_model_checkpoint_664_0.6738.nii.gz
    Orientation: RAS
  🔄 No reference GT found, applying default orientation: RAS → LPI
    ✓ Default reorientation to LPI successful
  🏷️  Applying label remapping
    After remapping: [0, 1, 2]
  📊 Volume Analysis:
    Right Kidney: 125,450 voxels = 125.45 cm³
    Left Kidney: 118,320 voxels = 118.32 cm³
  💾 Saving processed mask: mask_model_checkpoint_664_0.6738_processed.nii
    ✓ Saved successfully

📊 Volume CSV exported to: results/Batch_Storage_Volumes_20251202_143022/Kidney_Volumes_20251202_143022.csv
```

**Recent Updates (Dec 2, 2025):**
- Added automatic CSV volume export
- Creates timestamped subfolder in results directory
- Includes both successful and failed cases in CSV

---

### 2. `process_new_aira_masks.py` - AIRA Mask Preprocessor ⭐
**Purpose:** Complete preprocessing pipeline for new AIRA masks with label remapping and automatic orientation handling

**What it does:**
- Processes new AIRA masks with all required preprocessing steps
- Handles both `.nii` and `.nii.gz` files (including misnamed .gz files)
- **Automatically applies LPI orientation** (even without reference GT)
- Reorients to match reference ground truth when available
- Applies label remapping: AIRA {0,1,2,3} → Human reader {0,0,2,1}
- Uses int16 data type for exact integer labels (no floating-point precision issues)
- Creates backup of original files
- Saves processed masks ready for FDA analysis

**Key Features:**
- ✅ **Smart .nii.gz handling:** Detects and fixes files with .gz extension that aren't actually gzipped
- ✅ **Default LPI orientation:** Automatically converts RAS → LPI when no reference GT found
- ✅ **Reference-based reorientation:** Uses ground truth orientation when available
- ✅ **Label remapping:** Converts AIRA labels to human reader convention
- ✅ **int16 precision:** Ensures exact integer values (0, 1, 2) not floats (0.996...)
- ✅ **Volume analysis:** Calculates kidney volumes in cm³
- ✅ **Detailed logging:** Shows each processing step with success/error messages
- ✅ **Backup creation:** Preserves original files

**Label Mapping:**
```python
LABEL_MAPPING_AIRA = {
    0: 0,  # Background → Background
    1: 0,  # Noise (few voxels) → Background
    2: 2,  # AIRA right kidney → GT right kidney
    3: 1   # AIRA left kidney → GT left kidney
}
```

**Configuration:**
```python
# Input/Output paths
NEW_AIRA_PATH = r"D:\__SHARED__\AIRA_FDA_SET_2_LIVE"
GROUND_TRUTH_REFERENCE_PATH = r"c:\Users\...\OneDrive_1_10-8-2025"

# Label mapping
LABEL_MAPPING_AIRA = {0: 0, 1: 0, 2: 2, 3: 1}

# Default orientation when no reference GT
DEFAULT_ORIENTATION = 'LPI'
```

**Usage:**
```bash
python process_new_aira_masks.py
```

**Output Example:**
```
Processing: A-089(N195)
  Loading AIRA mask: aira_mask.nii
  Shape: (512, 512, 102)
  Orientation: RAS
  🔄 No reference GT found, applying default orientation: RAS → LPI
  ✓ Default reorientation successful
  Original labels: [0, 2, 3]
  Applying label remapping
  After remapping: [0, 1, 2]
  Final orientation: LPI
  Reorientation applied: True
  ✅ Processing complete
```

**Recent Updates (Oct 29, 2025):**
- Added default LPI orientation for cases without reference GT
- All 26/26 processed cases now have consistent LPI orientation
- Enhanced documentation in header

---

### 2. `batch_reorient_nifti.py` - NIfTI Orientation Converter
**Purpose:** Batch reorientation of NIfTI medical imaging files to match required orientations

**What it does:**
- Recursively scans folders for specific NIfTI files
- Reorients medical images to target orientation (e.g., RAS → LPS)
- Creates new files with clean naming convention: `AIRA_{folder_name}.nii`
- Preserves original files (no overwriting)
- Handles both `.nii` and `.nii.gz` formats

**Key Features:**
- ✅ **Smart naming:** Uses parent folder name (e.g., `A-089(N195)` → `AIRA_A-089_N195_.nii`)
- ✅ **Safe characters:** Replaces parentheses with underscores to avoid path issues
- ✅ **Skip already oriented:** Avoids redundant processing
- ✅ **Verification:** Reloads saved files to confirm correct orientation
- ✅ **Detailed summary:** Shows success/failed/skipped counts

**Configuration:**
```python
INPUT_FOLDER = r"d:\__SHARED__\AIRA_FDA_SET_2_LIVE\test"
FILE_PATTERN = "aira_mask_processed.nii"  # Files to process
TARGET_ORIENTATION = "LPS"                 # Target orientation
RECURSIVE_SEARCH = True                    # Search in subfolders
OUTPUT_SUFFIX = "_reoriented"              # Not used (uses folder name)
```

**Usage:**
```bash
python batch_reorient_nifti.py
```

**Output Example:**
```
Input:  D:\AIRA_FDA_SET_2_LIVE\A-089(N195)\aira_mask_processed.nii (RAS)
Output: D:\AIRA_FDA_SET_2_LIVE\A-089(N195)\AIRA_A-089_N195_.nii (LPS)
```

**Common Orientations:**
- **RAS** - Right, Anterior, Superior (neuroimaging standard)
- **LPS** - Left, Posterior, Superior (radiological convention)
- **LPI** - Left, Posterior, Inferior (alternative standard)

---

### 3. `cleanup_aira_folders.py` - Folder Cleanup Utility
**Purpose:** Remove intermediate/temporary files, keeping only essential AIRA masks

**What it does:**
- Scans AIRA case folders recursively
- Identifies files to keep vs delete based on patterns
- Removes backup files, intermediate processing files, and duplicates
- Provides detailed analysis before deletion (dry run mode)
- Frees up disk space

**Files KEPT (2 per case folder):**
- ✅ `aira_mask.nii` - Original AIRA prediction
- ✅ `AIRA_*.nii` - Processed/reoriented mask (e.g., `AIRA_A-089_N195_.nii`)

**Files DELETED:**
- ❌ `aira_mask.nii.gz.backup` - Backup of misnamed .gz files
- ❌ `aira_mask_processed.nii` - Intermediate processed file
- ❌ Any other files not matching keep patterns

**Key Features:**
- ✅ **Case-sensitive matching:** Ensures `AIRA_*.nii` doesn't match `aira_*.nii`
- ✅ **Dry run mode:** Preview what will be deleted before actual deletion
- ✅ **Confirmation prompt:** Asks for "yes" confirmation in live mode
- ✅ **Detailed reporting:** Shows file sizes and space savings per folder
- ✅ **Error handling:** Continues processing even if some files fail

**Configuration:**
```python
INPUT_FOLDER = r"D:\__SHARED__\AIRA_FDA_SET_2_LIVE"
RECURSIVE_SEARCH = True
KEEP_PATTERNS = [
    "aira_mask.nii",    # Original AIRA mask
    "AIRA_*.nii"        # Processed masks only (case-sensitive)
]
DRY_RUN = True  # Set to False to actually delete
```

**Usage:**
```bash
# Preview what will be deleted (safe)
python cleanup_aira_folders.py

# Actually delete files (after reviewing dry run)
# 1. Edit script: DRY_RUN = False
# 2. Run again and confirm with "yes"
python cleanup_aira_folders.py
```

**Output Statistics:**
- Folders processed: 26
- Files to keep: 52 (2 per folder)
- Files to delete: 52 (2 per folder)
- Space freed: ~1.8 GB

---

### 4. `check_orientation.py` - Orientation Verification Tool
**Purpose:** Verify and compare orientations of NIfTI files across all case folders

**What it does:**
- Scans all case folders for specified NIfTI files
- Reports orientation for each file (RAS, LPS, LPI, etc.)
- Provides side-by-side comparison for before/after preprocessing
- Shows orientation distribution statistics
- Detects orientation changes and inconsistencies

**Key Features:**
- ✅ **Flexible configuration:** Check any files by name pattern
- ✅ **Batch analysis:** Processes all folders at once
- ✅ **Comparison mode:** Shows before/after orientation changes
- ✅ **Statistics:** Counts and percentages for each orientation
- ✅ **Quality control:** Detects if files have inconsistent orientations

**Configuration:**
```python
ROOT_PATH = r"D:\__SHARED__\AIRA_FDA_SET_2_LIVE"

# Files to check (customize as needed)
FILES_TO_CHECK = [
    "aira_mask.nii",
    "aira_mask_processed.nii"
]
```

**Usage:**
```bash
python check_orientation.py
```

**Output Example:**
```
================================================================================
ORIENTATION CHECK - NIfTI FILES
================================================================================

FILE: aira_mask.nii
Statistics:
  Total folders: 27
  Files found: 26
  Successfully loaded: 26
  Orientation distribution:
    RAS: 26 files (100.0%)
  ✓ All files have consistent orientation

FILE: aira_mask_processed.nii
Statistics:
  Total folders: 27
  Files found: 26
  Successfully loaded: 26
  Orientation distribution:
    LPI: 26 files (100.0%)
  ✓ All files have consistent orientation

SIDE-BY-SIDE COMPARISON
Case ID              aira_mask.nii          aira_mask_processed.nii
--------------------------------------------------------------------------------
A-089(N195)          RAS                    LPI                    ⚠️  CHANGED
N-071                RAS                    LPI                    ⚠️  CHANGED
...

✓ Orientation changes detected in 26 cases: RAS → LPI
```

**Use Cases:**
- Verify preprocessing worked correctly
- Check orientation consistency across dataset
- Quality control before FDA analysis
- Troubleshoot orientation issues

---

### 5. `rename_files.py` - Batch File Renaming Tool
**Purpose:** Rename files across multiple folders using customizable patterns

**What it does:**
- Renames files using folder-name-based patterns
- Supports multiple rename rules simultaneously
- Cleans folder names (removes parentheses, spaces, etc.)
- Provides dry-run mode for safe preview
- Detects conflicts and prevents overwrites

**Key Features:**
- ✅ **Pattern-based:** Use `{folder_name}` placeholder in rename rules
- ✅ **Folder name cleaning:** Automatically handles special characters
- ✅ **Dry run mode:** Preview all changes before executing
- ✅ **Safety checks:** Prevents overwriting existing files
- ✅ **Backup option:** Can create .backup files before renaming
- ✅ **Batch processing:** Rename across all case folders at once

**Configuration:**
```python
ROOT_PATH = r"D:\__SHARED__\AIRA_FDA_SET_2_LIVE"

# Rename rules: source → target pattern
RENAME_CONFIG = {
    "aira_mask_processed.nii": "AIRA_{folder_name}.nii",
    # Add more rules as needed
}

# Folder name cleaning
CLEAN_FOLDER_NAME = True
REPLACE_PARENTHESES = True  # A-089(N195) → A-089_N195_
REMOVE_SPACES = True

# Safety
DRY_RUN = True  # Preview mode (set False to rename)
CREATE_BACKUP = False
```

**Usage:**
```bash
# Preview mode (safe)
python rename_files.py

# After reviewing, set DRY_RUN = False and run again
```

**Output Example:**
```
================================================================================
BATCH FILE RENAMING TOOL
================================================================================
Mode: DRY RUN
Rename rules:
  aira_mask_processed.nii → AIRA_{folder_name}.nii

Case: A-089(N195)
  → aira_mask_processed.nii → AIRA_A-089_N195_.nii

Case: N-071
  → aira_mask_processed.nii → AIRA_N-071.nii

SUMMARY
Total cases processed: 27
Status breakdown:
  → Would rename: 26
  ○ Not found: 1

⚠⚠⚠ DRY RUN MODE - No files were actually renamed
Set DRY_RUN = False to perform actual renaming
```

**Use Cases:**
- Standardize filenames across dataset
- Prepare files for FDA submission
- Clean up naming conventions
- Batch renaming with folder-based patterns

---

### 6. `check_nested_orientation.py` - Nested Folder Analyzer with DICOM Support
**Purpose:** Recursively scan nested folder structures to find and analyze orientation of NIfTI and DICOM files

**What it does:**
- Recursively scans deeply nested subfolder hierarchies
- Finds all NIfTI (.nii, .nii.gz) and DICOM (.dcm) files
- Reports orientation for each file type
- Extracts and interprets DICOM Image Orientation Patient (IOP) tags
- Provides per-folder and overall statistics
- Calculates total storage size

**Key Features:**
- ✅ **Deep recursion:** Scans nested folders at any depth level
- ✅ **DICOM support:** Reads DICOM files and extracts orientation from IOP tags
- ✅ **NIfTI support:** Standard RAS/LPS/LPI orientation detection
- ✅ **Modality detection:** Identifies file types (CT, MRI, etc.)
- ✅ **Smart display:** Limits file display to avoid spam from large DICOM series
- ✅ **Statistics:** Shows orientation distribution and storage size
- ✅ **Flexible patterns:** Search for multiple file extensions

**DICOM Orientation Interpretation:**
- Converts Image Orientation Patient (IOP) 6-element array to readable format
- Maps DICOM coordinate system to LPH/RAS convention
- Shows raw IOP values: `[1.00, 0.00, 0.00, 0.00, 1.00, 0.00]`
- Example: LPH = Left-Posterior-Head/Superior (standard axial CT)

**Configuration:**
```python
ROOT_PATH = r"D:\__SHARED__\AIRA_FDA_SET_2_LIVE\Original_Images"

# File patterns to search
FILE_PATTERNS = [
    "*.nii",
    "*.nii.gz",
    "*.dcm"  # DICOM files
]

# Display options
SHOW_DETAILED_FILES = True   # Show individual files
SHOW_FOLDER_SUMMARY = True   # Show per-folder summaries
SHOW_OVERALL_STATS = True    # Show overall statistics
MAX_FILES_PER_FOLDER = 3     # Limit files shown per folder
```

**Usage:**
```bash
python check_nested_orientation.py
```

**Output Example:**
```
================================================================================
NESTED FOLDER ORIENTATION CHECK
================================================================================
Root path: D:\__SHARED__\AIRA_FDA_SET_2_LIVE\Original_Images
================================================================================

✓ Found 2476 DICOM files in 26 subfolders

────────────────────────────────────────────────────────────────────────────────
📁 Folder: A089 N195\bff3cd0d1a619595\CT AXIAL WO
   Depth: 3 | Files: 102
────────────────────────────────────────────────────────────────────────────────
  ✓ CT000000.dcm
     Modality: CT       | Orientation: LPH    | Shape: (512, 512)
     Image Orientation Patient: [1.00, 0.00, 0.00, 0.00, 1.00, 0.00]
  ✓ CT000001.dcm
     Modality: CT       | Orientation: LPH    | Shape: (512, 512)
     Image Orientation Patient: [1.00, 0.00, 0.00, 0.00, 1.00, 0.00]
  ... and 99 more files

OVERALL STATISTICS
Total subfolders scanned: 26
Total files found: 2476
Successfully analyzed: 2476

Orientation distribution:
  LPH    : 2476 files (100.0%) ██████████████████████████████████████████████████

Total size: 0.35 GB (356.5 MB)
```

**Use Cases:**
- Analyze original DICOM CT imaging data
- Verify orientation consistency across nested datasets
- Find all medical imaging files in complex folder structures
- Calculate total storage requirements
- Quality control for imaging archives

**DICOM Orientation Details:**
- **LPH** = Left-Posterior-Head/Superior (standard axial CT)
- **IOP [1, 0, 0, 0, 1, 0]** = Standard supine patient position
  - Rows: X-axis (Right → Left)
  - Columns: Y-axis (Anterior → Posterior)
  - Slices: Z-axis (Inferior → Superior / Feet → Head)

---

### 7. `test_default_orientation.py` - Orientation Test Utility
**Purpose:** Test and verify default LPI orientation conversion logic

**What it does:**
- Creates test NIfTI image in RAS orientation
- Applies LPI orientation conversion
- Verifies conversion worked correctly
- Tests the same logic used in `process_new_aira_masks.py`

**Key Features:**
- ✅ **Unit test:** Validates orientation conversion algorithm
- ✅ **Quick verification:** Runs in seconds
- ✅ **Clear output:** Shows pass/fail with details

**Usage:**
```bash
python test_default_orientation.py
```

**Output Example:**
```
======================================================================
Testing Default LPI Orientation Conversion
======================================================================

✓ Created test image with orientation: RAS

🔄 Converting RAS → LPI...
✓ Conversion successful!
  Final orientation: LPI

✅ TEST PASSED: Orientation correctly converted to LPI
======================================================================
```

---

## 🔄 Complete Workflow

### Step 1: Preprocess New AIRA Masks
```bash
# Configure process_new_aira_masks.py
NEW_AIRA_PATH = r"D:\__SHARED__\AIRA_FDA_SET_2_LIVE"
GROUND_TRUTH_REFERENCE_PATH = r"c:\Users\...\OneDrive_1_10-8-2025"

# Run
python process_new_aira_masks.py
```

**Result:** Each folder gets `aira_mask_processed.nii` with:
- Label remapping applied (AIRA → Human convention)
- LPI orientation (default or from reference GT)
- int16 data type (exact integer labels)

### Step 2: Verify Orientations (Optional Quality Check)
```bash
# Check that all files have correct orientation
python check_orientation.py
```

**Result:** Confirms all masks have consistent LPI orientation

### Step 3: Rename to Final Format (Optional)
```bash
# Configure rename_files.py
RENAME_CONFIG = {
    "aira_mask_processed.nii": "AIRA_{folder_name}.nii"
}
DRY_RUN = True  # Preview first

# Preview
python rename_files.py

# Review output, then set DRY_RUN = False and run again
```

**Result:** Files renamed to `AIRA_A-089_N195_.nii` format

### Step 4: Clean Up Intermediate Files (Optional)
```bash
# Configure cleanup_aira_folders.py
INPUT_FOLDER = r"D:\__SHARED__\AIRA_FDA_SET_2_LIVE"
DRY_RUN = True  # Preview first

# Preview
python cleanup_aira_folders.py

# Review output, then set DRY_RUN = False and run again
```

**Result:** Only essential files remain (saves ~1.8 GB)

### Step 5: FDA Validation Analysis
Use validation scripts from main zTest folder:
- `fda_multiple_case_dice.py` - Batch Dice analysis
- `fda_single_case_dice.py` - Single case validation  
- `fda_multi_reader_analysis.py` - Multi-reader agreement

---

## 📊 Expected Results

### Typical Dice Scores (Kidney Segmentation)
- **Excellent:** Dice > 0.90 (90% overlap)
- **Good:** Dice > 0.85 (85% overlap) - **FDA threshold**
- **Acceptable:** Dice > 0.70 (70% overlap)
- **Poor:** Dice < 0.70

### Volume Differences
- **Excellent:** < 5% relative difference
- **Good:** < 10% relative difference
- **Acceptable:** < 15% relative difference

---

## 🐛 Troubleshooting

### Issue: Files not found during batch processing
**Solution:** 
- Check `INPUT_FOLDER` or `ROOT_PATH` is correct
- Ensure `RECURSIVE_SEARCH = True` if files are in subfolders
- Verify `FILE_PATTERN` matches actual filenames (case-sensitive)

### Issue: Orientation not applied correctly
**Solution:**
- Use `check_orientation.py` to verify current orientations
- Check console output for error messages
- Ensure reference GT files are in correct location (for `process_new_aira_masks.py`)
- Default LPI orientation applies automatically when no reference GT found

### Issue: Label values are not exact integers (e.g., 0.996...)
**Solution:**
- This bug was FIXED on Oct 29, 2025
- All scripts now use `int16` data type
- Ensure you're using the latest version from this folder
- Old float-based scripts will produce 0.996... instead of 1.0

### Issue: Cleanup script deleting wrong files
**Solution:**
- ALWAYS run in `DRY_RUN = True` mode first
- Review the detailed analysis before setting `DRY_RUN = False`
- Pattern matching is case-sensitive: `AIRA_*.nii` ≠ `aira_*.nii`
- Check `KEEP_PATTERNS` configuration

### Issue: Rename conflicts detected
**Solution:**
- Review dry-run output to see conflicts
- Manually resolve existing target files before renaming
- Adjust `RENAME_CONFIG` patterns to avoid conflicts
- Enable `CREATE_BACKUP = True` for safety

### Issue: Orientation verification shows "N/A"
**Solution:**
- File may be corrupted or invalid NIfTI format
- Check file can be opened with nibabel manually
- Verify file extension matches actual format (.nii vs .nii.gz)

---

## 📝 Important Notes

### Default LPI Orientation (Oct 29, 2025 Update)
`process_new_aira_masks.py` now automatically applies LPI orientation even when no reference GT is available:
```python
DEFAULT_ORIENTATION = 'LPI'

# Cases with reference GT: Use GT orientation (usually LPI)
# Cases without reference GT: Apply default LPI orientation
# Result: 100% orientation consistency across all 26/26 cases
```

### Data Type Fix (Oct 29, 2025)
All scripts updated to use `np.int16` for segmentation labels to avoid floating-point precision issues:
```python
# OLD (BUGGY):
return remapped_data.astype(float)  # Returns 0.996... instead of 1

# NEW (FIXED):
remapped_data = np.zeros_like(data_rounded, dtype=np.int16)
return remapped_data  # Returns exact integers: 0, 1, 2
```

### File Naming Convention
- **Original AIRA:** `aira_mask.nii`
- **Processed:** `aira_mask_processed.nii` (intermediate, can be renamed/deleted)
- **Final (optional):** `AIRA_A-089_N195_.nii` (standardized naming)

### Orientation Standards
- **AIRA default:** RAS (Right-Anterior-Superior)
- **FDA analysis:** LPI (Left-Posterior-Inferior) - most common in this dataset
- **Original DICOM CT:** LPH (Left-Posterior-Head/Superior) with IOP [1, 0, 0, 0, 1, 0]
- **Alternative:** LPS (Left-Posterior-Superior)
- **Reorientation:** Ensures spatial consistency with ground truth

**DICOM to NIfTI Orientation Conversion:**
- Original CT scans (DICOM): LPH orientation
- AIRA processing: Converts DICOM → NIfTI with RAS orientation
- Our preprocessing: Converts RAS → LPI to match ground truth
- Result: All processed masks have consistent LPI orientation

### Workflow Flexibility
The tools can be used independently or as a complete pipeline:
- **Minimal:** Just run `process_new_aira_masks.py` → Ready for FDA analysis
- **Standard:** Preprocess → Verify → FDA analysis
- **Complete:** Preprocess → Verify → Rename → Cleanup → FDA analysis

---

## 🔧 Dependencies

```python
import os
import glob
import nibabel as nib
import numpy as np
import pandas as pd
import pydicom  # For DICOM file support
from pathlib import Path
from datetime import datetime
from collections import Counter, defaultdict
```

**Install:**
```bash
pip install nibabel numpy pandas pydicom
```

---

## 📞 Support & References

### Tool Inventory
**Production Tools (7):**
1. `process_batch_storage_masks.py` - Batch storage mask processor with CSV export ⭐ **NEW**
2. `process_new_aira_masks.py` - Preprocessing with label remapping and orientation ⭐
3. `batch_reorient_nifti.py` - Batch orientation converter
4. `cleanup_aira_folders.py` - Folder cleanup utility
5. `check_orientation.py` - Orientation verification tool
6. `rename_files.py` - Batch file renaming tool
7. `check_nested_orientation.py` - Nested folder structure analyzer with DICOM support

**Test Utilities (1):**
8. `test_default_orientation.py` - Orientation conversion test

### FDA Guidance
- **FDA AI/ML SaMD Guidance (2021)**
- **FDA Statistical Guidance for Clinical Trials (2019)**
- **STARD 2015 Guidelines** (Bossuyt et al.)

### Technical References
- **Dice Coefficient:** Zou et al. (2004) Academic Radiology
- **Volume Analysis:** Kessler et al. (2015) Statistical Methods in Medical Research
- **NIfTI Format:** Neuroimaging Informatics Technology Initiative

### Related Scripts (in main zTest folder)
- `fda_multiple_case_dice.py` - FDA batch validation analysis
- `fda_single_case_dice.py` - Single case validation tool
- `fda_multi_reader_analysis.py` - Multi-reader agreement analysis

---

## 📜 Version History

**v1.4 - December 2, 2025**
- ✨ New tool: `process_batch_storage_masks.py` - Batch storage mask processor
- 📊 Added automatic CSV volume export with Case Name, Right/Left Kidney Volumes
- 📁 Creates timestamped subfolders in results directory
- 🎯 Specifically designed for `G:\AIRA_Models_RESULTS\batch_storage` workflow
- 📝 Updated README with new tool documentation

**v1.3 - October 29, 2025**
- ✨ New tool: `check_nested_orientation.py` - Nested folder analyzer with DICOM support
- 🔬 DICOM orientation extraction: Reads and interprets Image Orientation Patient (IOP) tags
- 📊 Discovered: All 2,476 original CT DICOM files have LPH orientation
- 📝 Updated dependencies to include `pydicom`
- 📖 Enhanced README with DICOM orientation documentation

**v1.2 - October 29, 2025**
- ⭐ Added default LPI orientation feature to `process_new_aira_masks.py`
- ✨ New tool: `check_orientation.py` - Orientation verification and comparison
- ✨ New tool: `rename_files.py` - Batch file renaming with patterns
- ✨ New utility: `test_default_orientation.py` - Unit test for orientation logic
- 📊 Updated README with complete tool documentation
- ✅ All 26/26 cases now have consistent LPI orientation

**v1.1 - October 29, 2025**
- Fixed int16 precision bug in all scripts
- Enhanced .nii.gz handling in `process_new_aira_masks.py`
- Improved case-sensitive pattern matching in `cleanup_aira_folders.py`

**v1.0 - October 29, 2025**
- Initial release with core preprocessing tools
- Batch orientation converter
- Cleanup utility
- FDA batch analysis integration

---

## ⚖️ License & Compliance

**Intended Use:** FDA AI/ML SaMD validation for kidney segmentation  
**Compliance:** FDA 21 CFR Part 11, FDA AI/ML SaMD Guidance  
**Data Privacy:** Ensure HIPAA compliance when processing patient data

---

## 📧 Contact

For questions about these tools or FDA validation workflow:
- Review zTest folder for related validation scripts
- Check individual script headers for detailed documentation
- See `INT16_FIX_VERIFICATION_REPORT.md` (main zTest folder) for precision fix details

---

**Last Updated:** December 2, 2025  
**Status:** Production Ready ✅  
**Tools Count:** 7 production + 1 test utility
