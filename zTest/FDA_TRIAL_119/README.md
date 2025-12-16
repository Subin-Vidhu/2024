# FDA Ground Truth Trial 119 - Analysis Suite

**Project:** Inter-observer agreement analysis for kidney segmentation  
**Dataset:** 119 FDA trial cases (N-prefix: normal, A-prefix: abnormal)  
**Annotators:** GT01 vs GT02 ground truth comparisons  
**Last Updated:** December 16, 2025

---

## 📁 Repository Structure

```
FDA_TRIAL_119/
├── README.md                              # This file
├── batch_compare_fda_ground_truth.py      # Main processing script
├── fda_utils.py                           # Shared utility functions
├── final_filename_validation.py           # Validation script
├── FDA_Ground_Truth_Formulas.md          # Complete formula documentation
└── results/                               # Output directory
    └── fda_ground_truth_comparison/
        ├── FDA_GT01_vs_GT02_Comparison_YYYYMMDD_HHMMSS.csv
        └── Aramis Dice Sample - DICE Run.csv  # FDA reference data
```

---

## 📄 File Descriptions

### 1. **batch_compare_fda_ground_truth.py** ⭐ MAIN SCRIPT
**Purpose:** Process all 119 FDA trial cases to calculate inter-observer agreement metrics.

**What it does:**
- Loads GT01 and GT02 segmentation masks for each case
- Calculates Dice coefficient (inter-observer agreement)
- Computes kidney volumes (mm³ and cm³)
- Calculates volume differences using FDA convention
- Outputs 3 rows per case (Right Kidney, Left Kidney, Average)

**Input Data Location:**
```
J:\FDA_GROUND_TRUTH_TRIAL_119\Aramis Truther Masks\Aramis Truther Masks\
```

**When to run:**
- When you need to reprocess all 119 cases
- After modifying formulas or calculations
- To generate fresh results with new parameters

**How to run:**
```bash
python batch_compare_fda_ground_truth.py
```

**Output:** Creates timestamped CSV in `results/fda_ground_truth_comparison/`

---

### 2. **fda_utils.py** 🛠️ UTILITIES
**Purpose:** Shared utility functions used by multiple scripts.

**Contains:**
- `extract_case_from_filename()` - Extract case IDs from filenames (A-###, N-###)
- `parse_diffpercent()` - Parse percentage values from various formats
- `validate_dice_match()` - Compare Dice coefficients with tolerance
- `validate_diffpercent_match()` - Compare DiffPercent values with tolerance
- `load_and_prepare_kidney_data()` - Load CSV and prepare kidney measurements
- `load_and_prepare_average_data()` - Load CSV and prepare average data
- `print_validation_summary()` - Formatted validation output

**When to modify:**
- When adding new shared functionality
- When standardizing calculations across scripts
- When updating case ID extraction logic

**Do NOT run directly** - This is a library module imported by other scripts.

---

### 3. **final_filename_validation.py** ✅ VALIDATION
**Purpose:** Validate our calculations against FDA's reference dataset.

**What it does:**
- Compares our calculated values vs FDA reference data
- Validates Dice coefficient (100% match required)
- Validates DiffPercent formula (100% match required)
- Validates Average calculation (100% match required)
- Reports coverage across all cases

**When to run:**
- After running `batch_compare_fda_ground_truth.py`
- To verify formula correctness
- Before submitting results to FDA
- After making any formula changes

**How to run:**
```bash
python final_filename_validation.py
```

**Expected output:**
```
✅ SUCCESS! ALL FORMULAS MATCH FDA 100%!
   • Dice Coefficient:  238/238 measurements
   • DiffPercent:       238/238 measurements
   • Average:           119/119 cases
   Validated across 119 cases
```

**⚠️ Important:** Update the CSV paths in the script if filenames change:
```python
our_csv = 'results/fda_ground_truth_comparison/FDA_GT01_vs_GT02_Comparison_YYYYMMDD_HHMMSS.csv'
fda_csv = 'results/fda_ground_truth_comparison/Aramis Dice Sample - DICE Run.csv'
```

---

### 4. **FDA_Ground_Truth_Formulas.md** 📖 DOCUMENTATION
**Purpose:** Comprehensive documentation of all formulas and conventions.

**Contains:**
- **Dice Coefficient:** Boolean logic implementation with edge cases
- **Volume Calculations:** Voxel-based measurements (mm³ and cm³)
- **DiffPercent Formula:** FDA convention using max volume denominator
- **Average Calculation:** Arithmetic mean of Right + Left Dice
- **Label Convention:** Radiologist's perspective (Label 1=Right, Label 2=Left)
- **Validation Results:** 100% match across 238 measurements
- **Examples:** Real case calculations with step-by-step math

**When to reference:**
- Understanding formula rationale
- Troubleshooting calculation differences
- Writing reports or papers
- Onboarding new team members

---

## 🚀 Quick Start Guide

### First Time Setup

1. **Verify data location:**
   ```
   J:\FDA_GROUND_TRUTH_TRIAL_119\Aramis Truther Masks\Aramis Truther Masks\
   ```

2. **Activate virtual environment:**
   ```bash
   D:\2024\test_venv\Scripts\activate
   ```

### Typical Workflow

**Step 1: Process all cases**
```bash
cd d:\2024\zTest\FDA_TRIAL_119
python batch_compare_fda_ground_truth.py
```
- Takes ~5-10 minutes for 119 cases
- Creates timestamped CSV in `results/fda_ground_truth_comparison/`

**Step 2: Validate results**
```bash
python final_filename_validation.py
```
- Should show 100% match on all metrics
- If validation fails, check formula implementations

**Step 3: Review results**
- Open the generated CSV in Excel/Python
- Each case has 3 rows: Right Kidney, Left Kidney, Average
- Check for any cases with errors in the Error column

---

## 📊 Output Format

### CSV Structure (3 rows per case)

| Patient | GT01_File | GT02_File | Organ | DiceCoefficient | GT01_Volume_cm3 | GT02_Volume_cm3 | DiffPercent | LargerMask |
|---------|-----------|-----------|-------|-----------------|-----------------|-----------------|-------------|------------|
| N-001 | N-001-GT01.nii | N-001-GT02.nii | Right Kidney | 0.965432 | 130.07 | 135.21 | 3.80% | Mask2 |
| N-001 | N-001-GT01.nii | N-001-GT02.nii | Left Kidney | 0.978123 | 145.33 | 142.89 | 1.68% | Mask1 |
| N-001 | N-001-GT01.nii | N-001-GT02.nii | N-001 Average | 0.971778 | | | | |

---

## 🔬 Key Formulas (Summary)

### Dice Coefficient
```
Dice = 2 × |A ∩ B| / (|A| + |B|)
```
- Measures overlap between two annotators
- Range: 0 (no overlap) to 1 (perfect agreement)
- Uses boolean logic for accurate intersection

### DiffPercent (FDA Convention)
```
DiffPercent = |Vol1 - Vol2| / max(Vol1, Vol2) × 100
```
- Uses **maximum volume** as denominator (not average)
- More conservative than average-based calculation
- Validated 100% against FDA reference

### Average
```
Average = (Dice_Right + Dice_Left) / 2
```
- Simple arithmetic mean
- Reported in row 3 for each case

---

## ⚙️ Configuration Options

### Debug Mode (batch_compare_fda_ground_truth.py)

**Process only first N cases:**
```python
MAX_CASES_TO_PROCESS = 5  # Test with 5 cases
MAX_CASES_TO_PROCESS = None  # Process all 119 cases (production)
```

**Enable detailed file search logging:**
```python
DEBUG_FILE_SEARCH = True  # Show all file matching details
DEBUG_FILE_SEARCH = False  # Standard output
```

---

## 🔧 Troubleshooting

### Problem: Validation shows mismatches
**Solution:** 
1. Check if you're using the latest batch processing script
2. Verify formulas match FDA_Ground_Truth_Formulas.md
3. Ensure using `fda_utils.py` functions for consistency

### Problem: Files not found for specific cases
**Solution:**
1. Check case folder names on J: drive
2. Review filename patterns (handles N-001, A-005, missing dashes, etc.)
3. Enable `DEBUG_FILE_SEARCH = True` to see matching logic

### Problem: DiffPercent values don't match FDA
**Solution:**
- Ensure using `max(vol1, vol2)` as denominator, NOT `(vol1 + vol2)/2`
- Formula: `|Vol1 - Vol2| / max(Vol1, Vol2) × 100`

---

## 📝 Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | Dec 16, 2025 | Initial validated release with 100% FDA match |

---

## 📧 Support

For questions or issues:
1. Review `FDA_Ground_Truth_Formulas.md` for formula details
2. Check validation output for specific errors
3. Verify data paths and file naming conventions

---

## ✅ Validation Status

**Last Validation:** December 16, 2025  
**Status:** ✅ PRODUCTION READY  
**FDA Match Rate:** 100% (238/238 kidney measurements)

- ✅ Dice Coefficient: 238/238 (100%)
- ✅ DiffPercent: 238/238 (100%)  
- ✅ Average: 119/119 (100%)
