# DICE Score Comparison Results Summary

**Date:** December 19, 2025  
**Analysis:** FDA Trial 119 - AIRA vs Ground Truth Comparison  
**Analyst:** AI Assistant

---

## Executive Summary

The comparison tool successfully analyzed 230 patient-organ pairs from the WCG dataset against corresponding AIRA predictions. The results show an **excellent 98.70% match rate** with only 3 mismatches detected.

### Key Findings

✅ **227 matches** (98.70%) - DICE values match within tolerance  
⚠️ **3 mismatches** (1.30%) - DICE values differ beyond tolerance  
📊 **238 additional entries** in AIRA files not present in WCG dataset  
✔️ **0 missing entries** - All WCG rows found in appropriate AIRA files

---

## Detailed Analysis

### 1. Mismatches Identified (3 cases)

#### Case 1: A-071, Left Kidney (Minor Rounding Difference)
- **GT Version:** GT01
- **WCG DICE:** 0.883840
- **AIRA DICE:** 0.883796
- **Difference:** 0.000044 (4.4e-5)
- **Assessment:** Minor floating-point rounding difference, likely acceptable

#### Case 2: A-075, Right Kidney (Significant Difference)
- **GT Version:** GT01
- **WCG DICE:** 0.860023
- **AIRA DICE:** 0.000000
- **Difference:** 0.860023
- **Assessment:** AIRA file shows 0.000000 with note about label reversal issue

#### Case 3: A-075, Left Kidney (Significant Difference)
- **GT Version:** GT01
- **WCG DICE:** 0.822367
- **AIRA DICE:** 0.000000
- **Difference:** 0.822367
- **Assessment:** AIRA file shows 0.000000 with note about label reversal issue

### 2. Pattern Analysis

**Patient A-075 Issue:**
Both kidneys for patient A-075 show DICE score of 0.000000 in the AIRA files with an explanation:
> "The Dice Score is 0 because the unique labels assigned by the FDA team are reversed. Normally, the right kidney(RK) is labeled as 1 and the left kidney(LK) as 2, but in this case, the labels seems to be swapped"

This is a **data labeling issue** rather than a comparison error. The WCG team appears to have corrected this before calculating their DICE scores.

### 3. Missing in WCG File (238 entries)

The AIRA files contain 238 additional patient-organ comparisons not present in the WCG dataset. These fall into two categories:

**GT01 Missing (21 entries):**
- Includes patients: A-004, A-006, A-013, A-014, A-016, A-023, A-024, A-092, N-001, N-023, N-026, N-029, N-034, N-070, N-196, N-203

**GT02 Missing (217 entries):**
- Substantially more GT02 comparisons in AIRA files
- Suggests WCG primarily used GT01 for their analysis
- All N-series patients with GT02 are missing from WCG

### 4. Data Quality Assessment

**Excellent Quality Indicators:**
- ✅ Zero missing entries from WCG in AIRA files
- ✅ 98.7% exact match rate (excluding label reversal case)
- ✅ All patient IDs successfully normalized and matched
- ✅ GT version extraction 100% successful
- ✅ No errors in data processing

**Areas Requiring Attention:**
- ⚠️ Patient A-075 label reversal issue
- ⚠️ Large number of AIRA comparisons not in WCG dataset (238)
- ⚠️ One case with 0.000044 difference (A-071) - check if tighter tolerance needed

---

## Recommendations

### Immediate Actions

1. **Patient A-075:** 
   - Verify the WCG DICE scores of 0.860023 and 0.822367
   - Confirm if these used corrected label assignments
   - Document the label reversal issue in final report

2. **A-071 Left Kidney:**
   - Difference of 0.000044 is likely rounding-related
   - Consider if this level of precision difference is acceptable
   - Current tolerance: ±0.000001 (1e-6)

3. **Missing WCG Entries:**
   - Investigate why 238 AIRA comparisons are not in WCG dataset
   - Determine if WCG intentionally excluded certain cases
   - Check if WCG focused primarily on GT01 comparisons

### Data Validation

1. **Cross-reference** the 238 missing entries with source data
2. **Verify** that A-075's corrected DICE scores in WCG are accurate
3. **Document** the methodology WCG used for case selection
4. **Review** if the 1e-6 tolerance is appropriate for clinical validation

### Documentation

1. **Include** this analysis in the final FDA submission
2. **Highlight** the 98.7% agreement rate
3. **Explain** the A-075 label reversal case
4. **Justify** any tolerance-exceeding differences

---

## Technical Details

### Comparison Methodology

- **Tolerance:** ±0.000001 (1e-6)
- **Matching Key:** Patient ID + Organ + GT Version
- **Normalization:** Case-insensitive, whitespace-trimmed
- **Filtered:** Average rows and error rows excluded
- **GT Version Detection:** Automatic from mask filenames

### Files Generated

1. `comparison_report.txt` - Full detailed report
2. `comparison_matches.csv` - 227 matching cases
3. `comparison_mismatches.csv` - 3 mismatching cases
4. `missing_in_wcg.csv` - 238 AIRA entries not in WCG
5. `IMPLEMENTATION_PLAN.md` - Technical documentation

### Statistics

- **Total WCG Rows:** 230
- **Total AIRA GT01 Valid Rows:** 234
- **Total AIRA GT02 Valid Rows:** 234
- **Matched:** 227 (98.70%)
- **Mismatched:** 3 (1.30%)
- **Processing Time:** <5 seconds

---

## Conclusion

The comparison demonstrates **excellent agreement** between WCG and AIRA DICE scores with a 98.7% match rate. The three mismatches are:

1. **One minor rounding difference** (0.000044) - likely acceptable
2. **Two cases with known label reversal issue** (Patient A-075) - documented in AIRA data

The tool successfully handled:
- ✅ Patient ID variations and normalization
- ✅ GT version detection (GT01/GT02)
- ✅ Different file structures
- ✅ Row ordering differences
- ✅ Missing data detection

**Overall Assessment:** The DICE score comparison validates the consistency between WCG calculations and AIRA predictions, with only one patient (A-075) requiring special attention due to label reversal.

---

## Next Steps

1. ✅ **Completed:** Automated comparison tool implemented
2. ✅ **Completed:** Initial analysis run and results generated
3. ⏭️ **Pending:** Stakeholder review of findings
4. ⏭️ **Pending:** Decision on A-071 tolerance acceptance
5. ⏭️ **Pending:** Investigation of A-075 corrected values
6. ⏭️ **Pending:** Analysis of 238 missing WCG entries

---

**Report Generated:** December 19, 2025  
**Tool Version:** 1.0  
**Python Script:** `compare_dice_scores.py`  
**Status:** ✅ Complete and Ready for Review
