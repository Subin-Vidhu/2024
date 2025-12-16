"""
Compute Hausdorff distances (HD and HD95) for many mask pairs stored in subfolders.

Assumptions:
- Root folder contains many subfolders.
- Each subfolder contains exactly two .nii/.nii.gz masks:
    - one predicted (filename contains 'model' or 'mask_model' or 'pred')
    - one original / human annotated (the other one)
- Both masks are same shape and alignment (same voxel grid). If not, you must resample externally.

Outputs:
- hausdorff_results.csv with per-folder HD and HD95
- printed summary of mean/median values

Requires:
    pip install nibabel scipy numpy pandas
"""

import os
from pathlib import Path
import numpy as np
import nibabel as nib
import pandas as pd
from scipy import ndimage
from scipy.spatial import distance

# ---------- User settings ----------
ROOT_FOLDER = r"D:\Hausdorff Distance"   # <- change this to your main folder (string)
OUT_CSV = "hausdorff_results.csv"
COMPUTE_HD95 = True   # also compute 95th percentile Hausdorff
# -----------------------------------

def find_mask_files(folder):
    """Return (orig_path, pred_path) based on simple filename heuristics.
    If cannot detect, returns (first, second).
    """
    nii_files = [p for p in Path(folder).iterdir() if p.suffix in ('.nii', '.gz', '.nii.gz')]
    # also consider .nii.gz endings
    # Normalize list
    nii_files = sorted(nii_files)
    if len(nii_files) < 2:
        return None, None
    # Heuristic: predicted file likely contains 'model' or 'mask_model' or 'pred'
    pred_candidates = [p for p in nii_files if ('model' in p.name.lower()) or ('pred' in p.name.lower())]
    if len(pred_candidates) == 1:
        pred = pred_candidates[0]
        orig = [p for p in nii_files if p != pred][0]
        return orig, pred
    # If multiple or none found, try detecting manual/MC vs other
    orig_candidates = [p for p in nii_files if ('mc' in p.name.lower()) or ('manual' in p.name.lower()) or ('annot' in p.name.lower())]
    if len(orig_candidates) == 1:
        orig = orig_candidates[0]
        pred = [p for p in nii_files if p != orig][0]
        return orig, pred
    # fallback: assume the filename with 'mask_model' is pred
    for p in nii_files:
        if 'mask_model' in p.name.lower():
            pred = p
            orig = [q for q in nii_files if q != p][0]
            return orig, pred
    # finally fallback to first=orig, second=pred
    return nii_files[0], nii_files[1]

def load_mask_as_binary(path):
    """Load NIfTI and return a binary numpy array (bool), plus voxel spacing (zooms)."""
    img = nib.load(str(path))
    data = img.get_fdata()
    # Binarize: non-zero considered foreground
    binary = np.asarray(data != 0, dtype=bool)
    # voxel spacing (tuple)
    try:
        zooms = img.header.get_zooms()[:3]
    except Exception:
        zooms = (1.0, 1.0, 1.0)
    return binary, np.array(zooms, dtype=float)

def surface_points_from_mask(mask):
    """Return coordinates (N x 3) of surface voxels (indices) for a binary mask.
    Surface = mask & ~eroded(mask). Uses a 3x3x3 structure element.
    """
    structure = ndimage.generate_binary_structure(3, 1)
    eroded = ndimage.binary_erosion(mask, structure=structure, iterations=1)
    boundary = mask & (~eroded)
    coords = np.argwhere(boundary)  # shape (N,3) in (z,y,x) order typically
    return coords

def voxel_indices_to_world(coords, zooms):
    """Convert voxel indices to physical coords in mm using voxel spacing.
    coords: (N,3) in (i,j,k) order -> multiply by zooms (kinda assumes axes aligned)
    """
    # coords are array of [i, j, k] where i moves along axis0 (z) etc.
    # We multiply each axis by respective zoom
    return coords.astype(float) * zooms.reshape((1,3))

def hausdorff_distance_from_pointsets(A_pts, B_pts):
    """Compute symmetric Hausdorff distance (max of directed distances) in mm.
    A_pts, B_pts: (N,3) numpy arrays of coordinates in mm.
    Returns: hd (float), hd95 (float)
    """
    if A_pts.size == 0 or B_pts.size == 0:
        return np.nan, np.nan
    # compute distance matrix in a memory-safe way if sets are large:
    # compute min distances from A to B
    D = distance.cdist(A_pts, B_pts, metric='euclidean')
    minAtoB = D.min(axis=1)
    minBtoA = D.min(axis=0)
    hd = max(minAtoB.max(), minBtoA.max())
    # HD95: 95th percentile of directed distances, take max of two directions
    hd95 = max(np.percentile(minAtoB, 95), np.percentile(minBtoA, 95))
    return float(hd), float(hd95)

def process_folder(folder):
    orig_path, pred_path = find_mask_files(folder)
    if orig_path is None or pred_path is None:
        print(f"[WARN] Skipping {folder}: not enough .nii files found")
        return None
    # load
    orig_mask, orig_zoom = load_mask_as_binary(orig_path)
    pred_mask, pred_zoom = load_mask_as_binary(pred_path)

    # check shapes
    if orig_mask.shape != pred_mask.shape:
        print(f"[WARN] Shape mismatch in {folder}: {orig_mask.shape} vs {pred_mask.shape}. Attempting shape alignment by cropping/padding is not implemented.")
        # you could resample here if required, but we stop
        return {
            "folder": Path(folder).name,
            "orig": str(orig_path.name),
            "pred": str(pred_path.name),
            "hd": np.nan,
            "hd95": np.nan,
            "notes": "shape_mismatch"
        }

    # choose zoom: if zooms differ, take orig_zoom (assume same)
    if not np.allclose(orig_zoom, pred_zoom):
        print(f"[INFO] Voxel spacing differs in {folder}. using original spacing for conversion.")
    zooms = orig_zoom

    # get boundary point indices
    pts_orig_idx = surface_points_from_mask(orig_mask)
    pts_pred_idx = surface_points_from_mask(pred_mask)

    # convert to world coordinates (mm)
    pts_orig_mm = voxel_indices_to_world(pts_orig_idx, zooms)
    pts_pred_mm = voxel_indices_to_world(pts_pred_idx, zooms)

    # compute hausdorff
    hd, hd95 = hausdorff_distance_from_pointsets(pts_orig_mm, pts_pred_mm)

    return {
        "folder": Path(folder).name,
        "orig": str(orig_path.name),
        "pred": str(pred_path.name),
        "n_pts_orig": int(len(pts_orig_mm)),
        "n_pts_pred": int(len(pts_pred_mm)),
        "hd": hd,
        "hd95": hd95,
        "notes": ""
    }

def main(root_folder, out_csv):
    root = Path(root_folder)
    if not root.exists():
        raise FileNotFoundError(f"{root_folder} does not exist")
    rows = []
    # iterate subfolders
    for sub in sorted(root.iterdir()):
        if sub.is_dir():
            res = process_folder(sub)
            if res:
                rows.append(res)
    if not rows:
        print("No results computed.")
        return
    df = pd.DataFrame(rows)
    df.to_csv(out_csv, index=False)
    print(f"\nSaved results to {out_csv}\n")
    # print brief summary
    numeric = df[['hd','hd95']].apply(pd.to_numeric, errors='coerce')
    print("Summary (ignoring NaNs):")
    print(f"Count: {len(df)}")
    print(f"Mean HD:  {numeric['hd'].mean():.3f} mm")
    print(f"Median HD: {numeric['hd'].median():.3f} mm")
    print(f"Mean HD95: {numeric['hd95'].mean():.3f} mm")
    print(f"Median HD95: {numeric['hd95'].median():.3f} mm")
    print("\nPer-folder results (first 10 shown):")
    print(df[['folder','orig','pred','n_pts_orig','n_pts_pred','hd','hd95']].head(10).to_string(index=False))

if __name__ == "__main__":
    main(ROOT_FOLDER, OUT_CSV)
