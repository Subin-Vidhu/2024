"""
Validate WCG's GT Selection Choices
====================================
For the 11 patients with mixed GT usage, verify that WCG chose the correct
GT version by comparing DICE scores from both GT01 and GT02 options.
"""
import pandas as pd
import re

# Load all three files
wcg_df = pd.read_csv('66017_WCG_DICE_16Dec2025.csv')
aira_gt01_df = pd.read_csv('AIRA_vs_GT01.csv')
aira_gt02_df = pd.read_csv('AIRA_vs_GT02.csv')

# Normalize data
for df in [wcg_df, aira_gt01_df, aira_gt02_df]:
    df['Patient'] = df['Patient'].str.strip()
    df['Organ'] = df['Organ'].str.strip().str.lower()

# Extract GT version from WCG
wcg_df['GT_Version'] = wcg_df['Mask2'].str.extract(r'(GT0[12])', flags=re.IGNORECASE)[0].str.upper()

# Filter AIRA files (remove averages and errors)
aira_gt01_filtered = aira_gt01_df[~aira_gt01_df['Organ'].str.contains('average|error', case=False, na=False)]
aira_gt02_filtered = aira_gt02_df[~aira_gt02_df['Organ'].str.contains('average|error', case=False, na=False)]

# Find patients with mixed GT usage
patient_gt = wcg_df.groupby('Patient')['GT_Version'].unique()
mixed_patients = sorted([p for p, v in patient_gt.items() if len(v) > 1])

print('=' * 100)
print('WCG GT SELECTION VALIDATION - DETAILED ANALYSIS')
print('=' * 100)
print(f'\nAnalyzing {len(mixed_patients)} patients with mixed GT usage...\n')

validation_results = []
total_correct = 0
total_questionable = 0
total_verified = 0

for patient in mixed_patients:
    print('=' * 100)
    print(f'PATIENT: {patient}')
    print('=' * 100)
    
    # Get WCG data for this patient
    wcg_patient = wcg_df[wcg_df['Patient'] == patient].copy()
    
    for _, wcg_row in wcg_patient.iterrows():
        organ = wcg_row['Organ'].lower()
        wcg_gt = wcg_row['GT_Version']
        wcg_dice = wcg_row['DiceCoefficient']
        
        # Get AIRA GT01 value
        aira_gt01_match = aira_gt01_filtered[
            (aira_gt01_filtered['Patient'] == patient) & 
            (aira_gt01_filtered['Organ'] == organ)
        ]
        
        # Get AIRA GT02 value
        aira_gt02_match = aira_gt02_filtered[
            (aira_gt02_filtered['Patient'] == patient) & 
            (aira_gt02_filtered['Organ'] == organ)
        ]
        
        gt01_dice = aira_gt01_match.iloc[0]['DiceCoefficient'] if len(aira_gt01_match) > 0 else None
        gt02_dice = aira_gt02_match.iloc[0]['DiceCoefficient'] if len(aira_gt02_match) > 0 else None
        
        print(f'\n{organ.upper()}:')
        print(f'  WCG Choice: {wcg_gt} = {wcg_dice:.6f}')
        print(f'  AIRA GT01:  {"N/A" if gt01_dice is None else f"{gt01_dice:.6f}"}')
        print(f'  AIRA GT02:  {"N/A" if gt02_dice is None else f"{gt02_dice:.6f}"}')
        
        # Validation logic
        status = "UNKNOWN"
        notes = []
        
        if gt01_dice is not None and gt02_dice is not None:
            # Check if WCG value matches the selected GT
            if wcg_gt == 'GT01':
                expected_dice = gt01_dice
                other_dice = gt02_dice
                other_gt = 'GT02'
            else:
                expected_dice = gt02_dice
                other_dice = gt01_dice
                other_gt = 'GT01'
            
            diff = abs(wcg_dice - expected_dice)
            
            if diff < 0.000001:
                status = "✓ VERIFIED"
                total_verified += 1
                notes.append(f"WCG value matches AIRA {wcg_gt}")
            elif diff < 0.0001:
                status = "✓ CLOSE MATCH"
                total_verified += 1
                notes.append(f"WCG value close to AIRA {wcg_gt} (diff: {diff:.6f})")
            else:
                status = "✗ MISMATCH"
                notes.append(f"WCG value differs from AIRA {wcg_gt} by {diff:.6f}")
            
            # Check if they chose the better GT
            if expected_dice > other_dice:
                better_choice = "YES"
                notes.append(f"{wcg_gt} is better than {other_gt} (Δ: {expected_dice - other_dice:.6f})")
                total_correct += 1
            elif expected_dice < other_dice:
                better_choice = "NO"
                notes.append(f"{other_gt} would be better (Δ: {other_dice - expected_dice:.6f})")
                total_questionable += 1
            else:
                better_choice = "EQUAL"
                notes.append("Both GT versions have same DICE score")
                total_correct += 1
            
            print(f'  Validation: {status}')
            print(f'  Better GT?: {better_choice}')
            for note in notes:
                print(f'    - {note}')
            
            validation_results.append({
                'Patient': patient,
                'Organ': organ,
                'WCG_GT': wcg_gt,
                'WCG_DICE': wcg_dice,
                'GT01_DICE': gt01_dice,
                'GT02_DICE': gt02_dice,
                'Match_Status': status,
                'Better_Choice': better_choice,
                'Notes': '; '.join(notes)
            })
        else:
            print(f'  Validation: ⚠ INCOMPLETE DATA')
            if gt01_dice is None:
                print(f'    - Missing GT01 data in AIRA file')
            if gt02_dice is None:
                print(f'    - Missing GT02 data in AIRA file')
    
    print()

# Summary
print('=' * 100)
print('SUMMARY REPORT')
print('=' * 100)
print(f'\nTotal entries analyzed: {len(validation_results)}')
print(f'  ✓ Verified matches: {total_verified}')
print(f'  ✓ WCG chose better GT: {total_correct}')
print(f'  ⚠ WCG chose worse GT: {total_questionable}')
print()

if total_questionable > 0:
    print('⚠ QUESTIONABLE CHOICES (where alternative GT had higher DICE):')
    print('-' * 100)
    for result in validation_results:
        if result['Better_Choice'] == 'NO':
            print(f"  {result['Patient']}, {result['Organ']}: "
                  f"Used {result['WCG_GT']} ({result['WCG_DICE']:.6f}) "
                  f"but {'GT01' if result['WCG_GT'] == 'GT02' else 'GT02'} "
                  f"has {result['GT01_DICE'] if result['WCG_GT'] == 'GT02' else result['GT02_DICE']:.6f}")
    print()

# Calculate accuracy
accuracy = (total_correct / len(validation_results)) * 100 if validation_results else 0
print(f'GT Selection Accuracy: {accuracy:.1f}% ({total_correct}/{len(validation_results)})')

# Verification rate
verification_rate = (total_verified / len(validation_results)) * 100 if validation_results else 0
print(f'Value Verification Rate: {verification_rate:.1f}% ({total_verified}/{len(validation_results)})')

# Save detailed results
results_df = pd.DataFrame(validation_results)
results_df.to_csv('wcg_gt_validation_results.csv', index=False)
print(f'\n✓ Detailed results saved to: wcg_gt_validation_results.csv')

print('\n' + '=' * 100)
print('VALIDATION COMPLETE')
print('=' * 100)
