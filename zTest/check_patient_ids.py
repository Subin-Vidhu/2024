import pandas as pd
import re

our = pd.read_csv('results/fda_ground_truth_comparison/FDA_GT01_vs_GT02_Comparison_20251216_085819.csv')

print("Checking Patient ID vs Filename patterns:")
print("=" * 70)

# Sample first 30 unique patients
unique_patients = our['Patient'].unique()[:30]

for patient in unique_patients:
    row = our[our['Patient'] == patient].iloc[0]
    gt01_file = row['GT01_File']
    
    # Extract prefix from filename
    match = re.search(r'^([AN])-', str(gt01_file), re.IGNORECASE)
    file_prefix = match.group(1).upper() if match else "None"
    
    print(f"Patient: {patient:>6}  ->  File: {gt01_file:30}  Prefix: {file_prefix}")

print("\n" + "=" * 70)
print("OBSERVATION:")
print("=" * 70)
print("Patient column has:")
print("  - Just numbers for N-cases: '001', '002', etc.")
print("  - A-prefix for A-cases: 'A-005', 'A-006', etc.")
print("\nTo match FDA data, we need to:")
print("  - Add 'N-' prefix to numeric-only Patient IDs")
print("  - Keep A-prefix as-is")
