# Quick Start Guide - DICE Score Comparison Tool

## 🚀 Quick Usage

```bash
# 1. Activate virtual environment
D:\2024\test_venv\Scripts\activate

# 2. Navigate to data folder
cd "d:\2024\zTest\FDA_TRIAL_119\data to compare\aira_and_gt_mask_canbe_gt1_or_gt2"

# 3. Run comparison
python compare_dice_scores.py
```

## 📁 Input Files Required

Place these files in the same directory as the script:
- `66017_WCG_DICE_16Dec2025.csv` (WCG ground truth)
- `AIRA_vs_GT01.csv` (AIRA predictions vs GT01)
- `AIRA_vs_GT02.csv` (AIRA predictions vs GT02)

## 📊 Output Files Generated

After running, you'll find:
1. `comparison_report.txt` - Human-readable full report
2. `comparison_matches.csv` - All matching DICE scores
3. `comparison_mismatches.csv` - DICE scores that differ
4. `missing_in_wcg.csv` - Cases in AIRA but not WCG
5. *(Optional)* `missing_in_aira.csv` - Cases in WCG but not AIRA

## ⚙️ Customization

### Change Tolerance
Edit `compare_dice_scores.py` line ~520:
```python
comparator = DiceScoreComparator(
    wcg_file=str(wcg_file),
    aira_gt01_file=str(aira_gt01_file),
    aira_gt02_file=str(aira_gt02_file),
    tolerance=0.000001  # Change this value
)
```

**Suggested tolerances:**
- `0.000001` (1e-6) - Very strict (current)
- `0.00001` (1e-5) - Strict
- `0.0001` (1e-4) - Moderate
- `0.001` (1e-3) - Lenient

## 📋 Understanding Results

### Summary Statistics
```
Total Comparisons Attempted: 230
  ✓ Matches (within tolerance): 227
  ✗ Mismatches (exceeds tolerance): 3
  ? Missing in AIRA files: 0
  ? Missing in WCG file: 238
```

**What this means:**
- **Matches:** DICE values are identical or differ by less than tolerance
- **Mismatches:** DICE values differ by more than tolerance
- **Missing in AIRA:** WCG has cases that AIRA doesn't
- **Missing in WCG:** AIRA has cases that WCG doesn't

### Match Rate
```
Match Rate: 98.70%
```
- Calculated as: (Matches / Total Comparisons) × 100
- Higher is better (>95% is excellent)

## 🔍 Interpreting Mismatches

Example mismatch:
```
1. Patient: A-071, Organ: left kidney
   GT Version: GT01
   WCG DICE:  0.883840
   AIRA DICE: 0.883796
   Difference: 0.000044
   Source: AIRA_vs_GT01
```

**Key information:**
- **Patient & Organ:** Identifies the specific case
- **GT Version:** Which ground truth was used (GT01 or GT02)
- **Difference:** Absolute difference between values
- **Source:** Which AIRA file the comparison came from

## 🐛 Troubleshooting

### Error: "File not found"
**Solution:** Ensure all 3 CSV files are in the same folder as the script

### Error: "UnicodeEncodeError"
**Already fixed** - Script now uses UTF-8 encoding

### High number of mismatches
**Check:**
1. Is tolerance too strict?
2. Are the input files correct versions?
3. Review the differences - are they systematic or random?

### Missing pandas/numpy
**Solution:**
```bash
D:/2024/test_venv/Scripts/pip.exe install pandas numpy
```

## 📖 Key Features

### ✅ Automatic Handling
- Patient ID normalization (removes spaces, case-insensitive)
- GT version detection (GT01/GT02 from filenames)
- Row order independence
- Average row filtering
- Error row filtering

### ✅ Smart Matching
- Matches: Patient ID + Organ + GT Version
- Tolerant of filename variations
- Handles different file structures

### ✅ Comprehensive Reporting
- Match/mismatch details
- Missing entries in both directions
- Statistical summary
- CSV exports for further analysis

## 📝 Common Questions

**Q: Why are there entries in AIRA but not WCG?**  
A: WCG may have selected a subset of cases for their analysis.

**Q: Should I worry about small differences (< 0.0001)?**  
A: Usually no - these are typically rounding differences.

**Q: What if DICE = 0.000000 in AIRA?**  
A: Check for notes in AIRA file - may indicate labeling issues.

**Q: Can I compare just GT01 or just GT02?**  
A: Not directly, but you can modify the script or filter output CSVs.

## 🔄 Workflow Example

1. **Receive new data** → Place CSVs in folder
2. **Run script** → `python compare_dice_scores.py`
3. **Check summary** → Look at console output
4. **Review mismatches** → Open `comparison_mismatches.csv`
5. **Investigate issues** → Cross-reference with source data
6. **Generate report** → Use `comparison_report.txt`
7. **Share results** → Email `RESULTS_SUMMARY.md` to team

## 📞 Support Files

- `IMPLEMENTATION_PLAN.md` - Detailed technical documentation
- `RESULTS_SUMMARY.md` - Analysis summary and recommendations
- `compare_dice_scores.py` - Main Python script

## 🎯 Success Criteria

**Excellent:** Match rate > 95%  
**Good:** Match rate > 90%  
**Acceptable:** Match rate > 85%  
**Review Required:** Match rate < 85%

**Current Result: 98.70% ✅ Excellent**

---

**Last Updated:** December 19, 2025  
**Version:** 1.0  
**Contact:** See project documentation
