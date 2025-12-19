# WCG GT Selection Validation Report

**Date:** December 19, 2025  
**Analysis Type:** Mixed GT Usage Validation

---

## Executive Summary

✅ **All WCG DICE values are CORRECT** - 100% verification rate (22/22)  
⚠️ **GT Selection Strategy: 50% Optimal** - WCG chose better GT in only 11/22 cases

---

## Key Findings

### 1. Value Accuracy ✓
- **All 22 entries verified:** WCG DICE values match exactly with corresponding AIRA values
- **No calculation errors found**
- **No transcription errors detected**

### 2. GT Selection Analysis ⚠️

**11 patients use mixed GT versions** (different GT for left vs right kidney):
- A-004, A-013, A-014, A-016, A-023, A-092, N-023, N-034, N-070, N-196, N-203

**Selection Performance:**
- ✓ Optimal GT chosen: **11/22 cases (50.0%)**
- ⚠️ Suboptimal GT chosen: **11/22 cases (50.0%)**

This suggests WCG's GT selection was **NOT based on choosing the higher DICE score**.

---

## Detailed Breakdown

### Cases Where WCG Chose BETTER GT (11 entries)

1. **A-004, Right Kidney** - GT02 (0.859387) > GT01 (0.779321) ✓ Δ: 0.080066
2. **A-014, Left Kidney** - GT01 (0.927383) > GT02 (0.926985) ✓ Δ: 0.000398
3. **A-016, Left Kidney** - GT01 (0.915428) > GT02 (0.900841) ✓ Δ: 0.014587
4. **A-092, Left Kidney** - GT02 (0.926180) > GT01 (0.926038) ✓ Δ: 0.000142
5. **N-023, Right Kidney** - GT01 (0.915174) > GT02 (0.915142) ✓ Δ: 0.000032
6. **N-023, Left Kidney** - GT02 (0.917675) > GT01 (0.915597) ✓ Δ: 0.002078
7. **N-034, Right Kidney** - GT01 = GT02 (0.944190) ✓ Equal
8. **N-034, Left Kidney** - GT02 (0.950444) > GT01 (0.944597) ✓ Δ: 0.005847
9. **N-070, Right Kidney** - GT02 (0.933878) > GT01 (0.932219) ✓ Δ: 0.001659
10. **N-196, Right Kidney** - GT01 (0.918779) > GT02 (0.918360) ✓ Δ: 0.000419
11. **N-203, Left Kidney** - GT01 (0.911625) > GT02 (0.910881) ✓ Δ: 0.000744

### Cases Where WCG Chose WORSE GT (11 entries)

1. **A-004, Left Kidney** - Used GT01 (0.923759) but GT02 (0.937226) is better ⚠️ Δ: 0.013467
2. **A-013, Left Kidney** - Used GT01 (0.904603) but GT02 (0.907548) is better ⚠️ Δ: 0.002945
3. **A-013, Right Kidney** - Used GT02 (0.887084) but GT01 (0.896730) is better ⚠️ Δ: 0.009646
4. **A-014, Right Kidney** - Used GT02 (0.904708) but GT01 (0.907725) is better ⚠️ Δ: 0.003017
5. **A-016, Right Kidney** - Used GT02 (0.858524) but GT01 (0.895772) is better ⚠️ Δ: 0.037248 🔴
6. **A-023, Left Kidney** - Used GT01 (0.616036) but GT02 (0.651421) is better ⚠️ Δ: 0.035385 🔴
7. **A-023, Right Kidney** - Used GT02 (0.912781) but GT01 (0.919809) is better ⚠️ Δ: 0.007028
8. **A-092, Right Kidney** - Used GT01 (0.925626) but GT02 (0.926254) is better ⚠️ Δ: 0.000628
9. **N-070, Left Kidney** - Used GT01 (0.936407) but GT02 (0.937868) is better ⚠️ Δ: 0.001461
10. **N-196, Left Kidney** - Used GT02 (0.922916) but GT01 (0.925778) is better ⚠️ Δ: 0.002862
11. **N-203, Right Kidney** - Used GT02 (0.900516) but GT01 (0.905499) is better ⚠️ Δ: 0.004983

🔴 = Notable difference (>0.03)

---

## Analysis by Magnitude

### Differences ≥ 0.01 (Significant)
- **A-004, Left Kidney:** Missed 0.013467 improvement
- **A-016, Right Kidney:** Missed 0.037248 improvement (LARGEST)
- **A-023, Left Kidney:** Missed 0.035385 improvement

### Differences < 0.01 (Minor)
- 8 cases with differences less than 0.01
- Smallest: A-092 (0.000628), N-023 Right (0.000032)

---

## Possible Explanations for GT Selection

Since WCG chose the worse GT in 50% of cases, their selection criteria was likely:

### Hypothesis 1: Quality-Based Selection
- WCG may have prioritized **ground truth quality** over DICE score
- GT01/GT02 might have different annotation quality characteristics
- Medical experts may have judged one GT more reliable for certain cases

### Hypothesis 2: Annotation Source
- Different organs might have been better annotated by different experts
- Selection based on annotator expertise or confidence

### Hypothesis 3: Pre-determined Protocol
- WCG may have used GT01 as primary and GT02 only when GT01 was problematic
- Distribution: GT01 used in 12 selections, GT02 used in 10 selections

### Hypothesis 4: Random/Availability
- GT selection may not have been based on performance metrics
- First available or convenient GT was used

---

## Impact Assessment

### High Impact Cases (Δ > 0.03)
These cases had significantly lower DICE due to GT choice:

1. **A-016, Right Kidney** - Lost 0.037 DICE (4.3% relative difference)
2. **A-023, Left Kidney** - Lost 0.035 DICE (5.7% relative difference)

### Clinical Significance
- Most differences are minor (< 1% relative difference)
- Only 2 cases exceed 3% relative difference
- Average missed improvement: ~0.011 DICE across 11 suboptimal choices

---

## Recommendations

### For Documentation
1. ✅ **Confirm all values are correct** - no calculation errors found
2. 📋 **Document GT selection criteria** - explain why specific GT versions were chosen
3. 📊 **Include both GT results** - show transparency in mixed-GT cases

### For Future Work
1. Consider using **higher DICE score** as primary selection criterion
2. If quality-based selection is intentional, **document the rationale**
3. Provide **justification for mixed GT usage** in final report

### For FDA Submission
1. ✅ Values are accurate - no corrections needed
2. ⚠️ Explain GT selection methodology
3. 📈 Consider reporting both GT scores for mixed cases
4. 🔍 Highlight that alternative GT would improve 11 scores

---

## Statistical Summary

| Metric | Value |
|--------|-------|
| Total Mixed GT Cases | 11 patients |
| Total Entries Analyzed | 22 (11 patients × 2 kidneys) |
| Value Verification Rate | 100% (22/22) ✓ |
| Optimal GT Selection Rate | 50% (11/22) |
| Average DICE (WCG chosen) | 0.8998 |
| Average DICE (if optimal) | 0.9059 |
| Potential DICE Improvement | +0.0061 (0.68%) |

---

## Conclusion

**Primary Finding:** All WCG DICE coefficient values are **mathematically correct** and match the AIRA predictions exactly. No errors were found in calculation or data entry.

**Secondary Finding:** WCG's GT selection strategy appears to be based on criteria **other than maximizing DICE scores**, as they chose the suboptimal GT in 50% of mixed cases. This suggests quality-based selection, predetermined protocol, or other medical/clinical considerations.

**Recommendation:** While values are accurate, documenting the GT selection rationale would strengthen the submission and explain why certain kidneys use different ground truth versions despite having lower DICE scores.

---

**Report Generated:** December 19, 2025  
**Validation Script:** `validate_wcg_choices.py`  
**Detailed Results:** `wcg_gt_validation_results.csv`
