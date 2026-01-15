"""Compare WCG Hausdorff CSV against the latest internal Hausdorff Excel results.

Usage: python compare_wcg_hausdorff.py
Adjust paths below if needed.
"""
from __future__ import annotations

import math
from pathlib import Path
from typing import Iterable, List, Tuple

import numpy as np
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent
WCG_CSV = BASE_DIR / "data to compare" / "excel_shared_by_wcg" / "66017_WCG_Hausdorff_14Jan2026.csv"
RESULTS_DIR = BASE_DIR / "results" / "hausdorff_distances"
SHEET_NAME = "AIRA_vs_Larger_GT"
TOL = 1e-3
EXPECTED_COLS = [
    "Patient",
    "AIRA_File",
    "Organ",
    "GT_Selected",
    "GT_File",
    "AIRA_Volume_mm3",
    "GT01_Volume_mm3",
    "GT02_Volume_mm3",
    "Selected_GT_Volume_mm3",
    "HD_mm",
    "HD95_mm",
    "Message",
]


def find_latest_excel(results_dir: Path) -> Path:
    candidates = sorted(results_dir.glob("Hausdorff_Distances_*.xlsx"))
    if not candidates:
        raise FileNotFoundError("No Hausdorff_Distances_*.xlsx files found")
    return max(candidates, key=lambda p: p.stat().st_mtime)


def normalize(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["Patient"] = df["Patient"].astype(str).str.strip()
    df["Organ"] = df["Organ"].astype(str).str.strip()
    return df


def check_columns(df: pd.DataFrame, source: str) -> Tuple[List[str], List[str]]:
    missing = [c for c in EXPECTED_COLS if c not in df.columns]
    extra = [c for c in df.columns if c not in EXPECTED_COLS]
    if missing or extra:
        print(f"[WARN] Column mismatch in {source}: missing={missing}, extra={extra}")
    else:
        print(f"[OK] Columns match expected for {source}")
    return missing, extra


def find_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    dup_mask = df.duplicated(subset=["Patient", "Organ"], keep=False)
    return df.loc[dup_mask].sort_values(["Patient", "Organ"])


def compare_values(row_a: pd.Series, row_b: pd.Series, num_cols: Iterable[str], str_cols: Iterable[str]) -> List[str]:
    mismatches: List[str] = []
    for col in num_cols:
        va, vb = row_a.get(col), row_b.get(col)
        if pd.isna(va) and pd.isna(vb):
            continue
        if pd.isna(va) != pd.isna(vb):
            mismatches.append(f"{col}: ours={va}, wcg={vb}")
            continue
        if not math.isclose(float(va), float(vb), rel_tol=0, abs_tol=TOL):
            mismatches.append(f"{col}: ours={va}, wcg={vb}")
    for col in str_cols:
        va, vb = row_a.get(col), row_b.get(col)
        if pd.isna(va):
            va = ""
        if pd.isna(vb):
            vb = ""
        if str(va).strip() != str(vb).strip():
            mismatches.append(f"{col}: ours={va}, wcg={vb}")
    return mismatches


def main() -> None:
    latest_excel = find_latest_excel(RESULTS_DIR)
    print(f"Using internal file: {latest_excel.name} (sheet {SHEET_NAME})")
    print(f"Using WCG file: {WCG_CSV.name}\n")

    wcg_df = normalize(pd.read_csv(WCG_CSV))
    ours_df = normalize(pd.read_excel(latest_excel, sheet_name=SHEET_NAME))

    check_columns(wcg_df, "WCG CSV")
    check_columns(ours_df, "Internal Excel sheet")

    wcg_dups = find_duplicates(wcg_df)
    ours_dups = find_duplicates(ours_df)
    if not wcg_dups.empty:
        print("[WARN] Duplicate (Patient, Organ) rows in WCG:")
        print(wcg_dups[["Patient", "Organ"]])
    if not ours_dups.empty:
        print("[WARN] Duplicate (Patient, Organ) rows in internal sheet:")
        print(ours_dups[["Patient", "Organ"]])

    wcg_keys = set(zip(wcg_df["Patient"], wcg_df["Organ"]))
    ours_keys = set(zip(ours_df["Patient"], ours_df["Organ"]))

    missing_in_ours = sorted(wcg_keys - ours_keys)
    missing_in_wcg = sorted(ours_keys - wcg_keys)

    print(f"Total WCG rows: {len(wcg_df)}")
    print(f"Total internal rows: {len(ours_df)}")
    print(f"Missing in internal: {len(missing_in_ours)}")
    print(f"Missing in WCG: {len(missing_in_wcg)}\n")

    if missing_in_ours:
        print("Cases in WCG but not in internal:")
        for patient, organ in missing_in_ours:
            print(f"  {patient} | {organ}")
        print()

    if missing_in_wcg:
        print("Cases in internal but not in WCG:")
        for patient, organ in missing_in_wcg:
            print(f"  {patient} | {organ}")
        print()

    num_cols = [
        "AIRA_Volume_mm3",
        "GT01_Volume_mm3",
        "GT02_Volume_mm3",
        "Selected_GT_Volume_mm3",
        "HD_mm",
        "HD95_mm",
    ]
    str_cols = ["GT_Selected", "GT_File", "AIRA_File", "Message"]

    mismatches: List[Tuple[str, str, List[str]]] = []
    for patient, organ in sorted(wcg_keys & ours_keys):
        row_wcg = wcg_df[(wcg_df["Patient"] == patient) & (wcg_df["Organ"] == organ)]
        row_ours = ours_df[(ours_df["Patient"] == patient) & (ours_df["Organ"] == organ)]
        if len(row_wcg) != 1 or len(row_ours) != 1:
            mismatches.append((patient, organ, ["Duplicate rows found during comparison"]))
            continue
        diff = compare_values(row_ours.iloc[0], row_wcg.iloc[0], num_cols, str_cols)
        if diff:
            mismatches.append((patient, organ, diff))

    print(f"Value mismatches: {len(mismatches)}")
    if mismatches:
        print("\nDetailed mismatches:")
        for patient, organ, issues in mismatches:
            print(f"- {patient} | {organ}")
            for issue in issues:
                print(f"    {issue}")


if __name__ == "__main__":
    main()
