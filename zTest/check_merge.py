import sys
sys.path.insert(0, r'd:\2024\zTest')
from compare_aira_vs_annotators_from_csv import merge_specific_cases, parse_aira_csv, parse_fda_csv

aira = parse_aira_csv(r'd:\2024\zTest\FDA_trial_cases\CSV_data\AIRA_Volume_Values.csv')
fda = parse_fda_csv(r'd:\2024\zTest\FDA_trial_cases\CSV_data\FDA-team-both-annotators.csv')

print(f"\nOriginal AIRA cases: {len(aira)}")
print(f"Original FDA cases: {len(fda)}")

aira_m = merge_specific_cases(aira)
fda_m = merge_specific_cases(fda)

print(f"\nAIRA after merge: {len(aira_m)}")
print(f"FDA after merge: {len(fda_m)}")

merged_aira = [k for k in aira_m.keys() if "/" in str(k)]
merged_fda = [k for k in fda_m.keys() if "/" in str(k)]

print(f"\nMerged cases in AIRA: {merged_aira}")
print(f"Merged cases in FDA: {merged_fda}")

matching = set(aira_m.keys()) & set(fda_m.keys())
print(f"\nMatching cases: {len(matching)}")

# Check if A-088, N-088, A-090, N-090 exist
for case in ['A-088', 'N-088', 'A-090', 'N-090', 'A-088 / N-088', 'A-090 / N-090']:
    in_aira = case in aira_m
    in_fda = case in fda_m
    print(f"  {case}: AIRA={in_aira}, FDA={in_fda}")
