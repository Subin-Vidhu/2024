import pandas as pd

our = pd.read_csv('results/fda_ground_truth_comparison/FDA_GT01_vs_GT02_Comparison_20251216_085819.csv')
fda = pd.read_csv('results/fda_ground_truth_comparison/Aramis Dice Sample - DICE Run.csv')

print('CASE 004 VERIFICATION:\n')
our_004 = our[our['Patient'] == '004']
fda_004 = fda[fda['Mask1'].str.contains('004', na=False)]

print('Right Kidney:')
print(f"  Our DiffPercent: {our_004.iloc[0]['DiffPercent']}, LargerMask: {our_004.iloc[0]['LargerMask']}")
print(f"  FDA DiffPercent: {fda_004.iloc[0]['DiffPercent']}, LargerMask: {fda_004.iloc[0]['LargerMask']}")
our_diff = our_004.iloc[0]['DiffPercent']
fda_diff = fda_004.iloc[0]['DiffPercent']
print(f"  Match: {'✅ YES' if our_diff == fda_diff else '❌ NO'}")

print('\nLeft Kidney:')
print(f"  Our DiffPercent: {our_004.iloc[1]['DiffPercent']}, LargerMask: {our_004.iloc[1]['LargerMask']}")
print(f"  FDA DiffPercent: {fda_004.iloc[1]['DiffPercent']}, LargerMask: {fda_004.iloc[1]['LargerMask']}")
our_diff = our_004.iloc[1]['DiffPercent']
fda_diff = fda_004.iloc[1]['DiffPercent']
print(f"  Match: {'✅ YES' if our_diff == fda_diff else '❌ NO'}")

print('\n' + '='*60)
print('SPOT CHECK: Cases 001, 003, 004, 075')
print('='*60)

for case_id in ['001', '003', '004', '075']:
    our_case = our[our['Patient'] == case_id]
    fda_case = fda[fda['Mask1'].str.contains(case_id, na=False)]
    
    if len(our_case) < 2 or len(fda_case) < 2:
        continue
    
    print(f'\nCase {case_id}:')
    for i, organ in enumerate(['Right', 'Left']):
        our_diff = our_case.iloc[i]['DiffPercent']
        fda_diff = fda_case.iloc[i]['DiffPercent']
        match = '✅' if our_diff == fda_diff else '❌'
        print(f"  {organ}: Our={our_diff}, FDA={fda_diff} {match}")
