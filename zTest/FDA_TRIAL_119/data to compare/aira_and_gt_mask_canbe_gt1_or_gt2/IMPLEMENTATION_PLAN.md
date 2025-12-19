# DICE Score Comparison - Detailed Implementation Plan

## Project Overview
This project compares DICE coefficient values from three CSV files for FDA Trial 119:
1. **WCG Team's CSV** (`66017_WCG_DICE_16Dec2025.csv`) - Ground truth comparisons
2. **AIRA vs GT01** (`AIRA_vs_GT01.csv`) - AI predictions vs Ground Truth 1
3. **AIRA vs GT02** (`AIRA_vs_GT02.csv`) - AI predictions vs Ground Truth 2

## Key Challenges Identified

### 1. Data Structure Differences
- **WCG File Structure:**
  - Columns: `Patient`, `Mask1`, `Mask2`, `Organ`, `DiceCoefficient`, `Mask1_Volume_mL`, `Mask2_Volume_mL`
  - Each row represents one patient-organ comparison
  - Uses either GT01 or GT02 per row (indicated in `Mask2` column)
  
- **AIRA Files Structure:**
  - Columns: `Patient`, `AIRA_File`, `GT_File`, `Organ`, `DiceCoefficient`, plus volume and metadata
  - Contains "Average" rows (e.g., "A-003 Average") that should be excluded
  - Contains "ERROR" rows for shape mismatches
  - More detailed metadata than WCG file

### 2. Patient ID Inconsistencies
- **Spacing variations:** `"A-065"` vs `"A-065 "` (trailing space)
- **Case sensitivity:** Generally consistent but needs normalization
- **Solution:** Strip whitespace and normalize before comparison

### 3. GT Version Matching
- WCG file uses **either GT01 OR GT02** for each patient-organ pair
- Must extract GT version from `Mask2` column (e.g., "A-003_GT01.nii" → GT01)
- Pattern variations: `GT01`, `GT_01`, `GT 01`, etc.

### 4. Row Ordering
- Files may have different row orders
- Cannot rely on index-based matching
- Must use patient ID + organ combination as key

### 5. Organ Name Variations
- Generally consistent: "Right Kidney", "Left Kidney"
- Need case-insensitive matching for safety

## Implementation Strategy

### Phase 1: Data Loading and Normalization
```python
1. Load all three CSV files using pandas
2. Normalize patient IDs (strip whitespace)
3. Normalize organ names (lowercase, strip)
4. Extract GT version from WCG Mask2 column
5. Filter out "Average" and "ERROR" rows from AIRA files
```

### Phase 2: Matching Logic
```python
For each row in WCG file:
    1. Get: patient_id, organ, dice_value, gt_version
    2. Select appropriate AIRA file (GT01 or GT02)
    3. Find matching row: WHERE patient_id = X AND organ = Y
    4. Compare DICE values with tolerance
    5. Record result (match/mismatch/missing)
```

### Phase 3: Reverse Check
```python
For each row in AIRA files:
    Check if it exists in WCG file with same GT version
    Record if missing from WCG
```

### Phase 4: Reporting
```python
Generate comprehensive report with:
    - Summary statistics
    - Detailed mismatches
    - Missing entries
    - Errors encountered
```

## Algorithm Details

### GT Version Extraction
```python
def extract_gt_version(mask_file):
    # Input: "A-003_GT01.nii" or "A-065 GT01.nii"
    # Output: "GT01" or "GT02"
    
    mask_str = str(mask_file).upper()
    
    if 'GT01' in mask_str or 'GT_01' in mask_str:
        return 'GT01'
    elif 'GT02' in mask_str or 'GT_02' in mask_str:
        return 'GT02'
    else:
        return 'UNKNOWN'
```

### Matching Key
```python
# Unique identifier for each comparison
matching_key = (normalized_patient_id, normalized_organ, gt_version)
```

### DICE Value Comparison
```python
def compare_dice_values(wcg_value, aira_value, tolerance=0.000001):
    difference = abs(wcg_value - aira_value)
    is_match = difference <= tolerance
    return is_match, difference
```

## Edge Cases Handled

1. **Average Rows in AIRA files**
   - Filter: `Organ` contains "Average"
   - Action: Exclude from comparison

2. **Error Rows in AIRA files**
   - Filter: `Organ` == "ERROR"
   - Action: Exclude from comparison

3. **Unknown GT Version**
   - If GT version cannot be extracted from Mask2
   - Action: Report as error

4. **Multiple Matches**
   - If patient-organ combination appears multiple times
   - Action: Report as error (should not happen)

5. **Missing Data**
   - Present in WCG but not in AIRA
   - Present in AIRA but not in WCG
   - Action: Report separately

6. **Floating Point Precision**
   - Use tolerance (default: 0.000001)
   - Allows for minor rounding differences

## Output Files

### 1. `comparison_report.txt`
Text report with:
- Summary statistics
- Match rate percentage
- Detailed mismatches
- Missing entries
- Errors

### 2. `comparison_matches.csv`
All rows where DICE values match within tolerance

### 3. `comparison_mismatches.csv`
Rows where DICE values differ beyond tolerance
Columns: patient, organ, gt_version, wcg_dice, aira_dice, difference

### 4. `missing_in_aira.csv`
Rows present in WCG but not found in AIRA files

### 5. `missing_in_wcg.csv`
Rows present in AIRA files but not found in WCG

### 6. `comparison_errors.csv`
Any errors encountered during processing

## Usage Instructions

### Prerequisites
```bash
# Activate virtual environment
D:\2024\test_venv\Scripts\activate

# Install required packages
pip install pandas numpy
```

### Running the Script
```bash
# Navigate to the data directory
cd "d:\2024\zTest\FDA_TRIAL_119\data to compare\aira_and_gt_mask_canbe_gt1_or_gt2"

# Run the comparison
python compare_dice_scores.py
```

### Customizing Tolerance
Edit the script's `main()` function:
```python
comparator = DiceScoreComparator(
    wcg_file=str(wcg_file),
    aira_gt01_file=str(aira_gt01_file),
    aira_gt02_file=str(aira_gt02_file),
    tolerance=0.000001  # Adjust this value
)
```

## Expected Results

### Best Case Scenario
- All DICE values match within tolerance
- No missing entries
- No errors
- Output: "✓ ALL DICE SCORES MATCH PERFECTLY!"

### Likely Scenarios to Check
1. **Minor floating point differences** - Should match within tolerance
2. **Missing cases** - Some patients in one file but not others
3. **GT version mismatches** - WCG uses GT01 but patient should use GT02
4. **Data entry errors** - Typos in patient IDs or values

## Validation Checklist

- [ ] All WCG rows have matching AIRA rows
- [ ] All DICE values match within tolerance
- [ ] No duplicate patient-organ-GT combinations
- [ ] All GT versions correctly identified
- [ ] Patient ID normalization works for all cases
- [ ] Organ name matching is case-insensitive
- [ ] Average rows are excluded from AIRA files
- [ ] Error rows are excluded from AIRA files

## Troubleshooting

### Issue: "File not found"
**Solution:** Ensure CSV files are in the same directory as the script

### Issue: "Could not determine GT version"
**Solution:** Check Mask2 column format in WCG file, may need pattern update

### Issue: High mismatch rate
**Solution:** 
1. Check if tolerance is too tight
2. Verify data preprocessing
3. Check for systematic bias

### Issue: Many missing entries
**Solution:**
1. Verify patient ID normalization
2. Check for case sensitivity issues
3. Look for additional whitespace or special characters

## Technical Specifications

- **Language:** Python 3.8+
- **Dependencies:** pandas, numpy
- **Memory Requirements:** Minimal (<100MB for these datasets)
- **Processing Time:** <10 seconds for ~600 total rows
- **Precision:** Float comparison with 1e-6 tolerance
- **Encoding:** UTF-8 for CSV files

## Future Enhancements

1. **GUI Interface** - User-friendly interface for non-technical users
2. **Batch Processing** - Handle multiple comparison sets
3. **Statistical Analysis** - Mean, median, std dev of differences
4. **Visualization** - Plots showing distribution of matches/mismatches
5. **Excel Output** - Generate formatted Excel reports
6. **Email Notifications** - Auto-send reports to stakeholders
7. **Version Control Integration** - Track changes over time

## Contact & Support

For questions or issues:
1. Review this documentation
2. Check the comparison_report.txt for detailed findings
3. Examine output CSV files for specific cases
4. Verify input data integrity

---

**Document Version:** 1.0  
**Date:** December 19, 2025  
**Author:** AI Assistant for FDA Trial 119  
**Status:** Production Ready
