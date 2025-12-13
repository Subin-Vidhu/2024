# AIRA vs FDA Annotators Comparison (CSV-based)

## Overview

This script compares AIRA volume predictions with FDA annotator volumes using pre-calculated CSV data. It generates separate comparisons for:
- **AIRA vs Annotator 1 (GT01)**
- **AIRA vs Annotator 2 (GT02)**

## Input Files

1. **FDA CSV** (`FDA-team-both-annotators.csv`):
   - Contains volumes for both annotators (GT01 and GT02)
   - Includes inter-annotator Dice scores
   - Volumes in both mm³ and mL (cm³)

2. **AIRA CSV** (`AIRA_Volume_Values.csv`):
   - Contains AIRA predicted volumes
   - Volumes in cm³

## Output File

The script generates a **single Excel file** (`AIRA_vs_Annotators_*.xlsx`) with **4 sheets**:

1. **Sheet 1: AIRA_vs_GT01** - Detailed case-by-case comparison
   - Columns include:
     - Case_ID
     - AIRA volumes (Right, Left, Total)
     - FDA GT01 annotator volumes (Right, Left, Total)
     - Volume differences (absolute and percentage)
     - Inter-annotator agreement metrics (Dice scores between GT01 and GT02)

2. **Sheet 2: AIRA_vs_GT01_Stats** - Summary statistics
   - Summary statistics
   - Regression metrics (MAE, RMSE, MAPE, R², Correlation, MBE)
   - Clinical agreement rates
   - 95% confidence intervals
   - Inter-annotator agreement summary

3. **Sheet 3: AIRA_vs_GT02** - Detailed case-by-case comparison
   - Same structure as Sheet 1, but comparing AIRA vs GT02

4. **Sheet 4: AIRA_vs_GT02_Stats** - Summary statistics
   - Same structure as Sheet 2, but for GT02 comparison

## Requirements

```bash
pip install pandas numpy scipy openpyxl
```

## Usage

```bash
python compare_aira_vs_annotators_from_csv.py
```

## Configuration

Edit the following paths in the script:

```python
FDA_CSV_PATH = r'd:\2024\zTest\FDA_trial_cases\CSV_data\FDA-team-both-annotators.csv'
AIRA_CSV_PATH = r'd:\2024\zTest\FDA_trial_cases\CSV_data\AIRA_Volume_Values.csv'
OUTPUT_DIR = r'd:\2024\zTest\results\aira_vs_annotators_csv'
```

## Features

- **Automatic case matching**: Handles various case ID formats (N-001, A-003, etc.)
- **Volume comparisons**: Absolute and percentage differences
- **Comprehensive metrics**: Regression analysis, agreement rates, confidence intervals
- **Inter-annotator metrics**: Includes Dice scores between GT01 and GT02 from FDA CSV
- **Robust error handling**: Handles missing data and edge cases

## Output Location

Results are saved to: `d:\2024\zTest\results\aira_vs_annotators_csv\`

The output is a single Excel file (`.xlsx`) with 4 sheets, making it easy to navigate and compare results.

## Notes

- The script matches cases by case ID (e.g., "N-001", "A-003")
- Cases that don't match between CSVs are included but with empty values
- Inter-annotator Dice scores are from the FDA CSV (comparison between GT01 and GT02)
- Volume differences are calculated as: `(AIRA - FDA) / FDA * 100`

