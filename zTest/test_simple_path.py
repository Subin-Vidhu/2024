#!/usr/bin/env python3
import os

gt_path = r"c:\Users\Subin-PC\Downloads\Telegram Desktop\GT01 - 5 Test Cases\N-071_AS.nii"
aira_path = r"D:\__SHARED__\AIRA_FDA_SET_2_LIVE\test\N-071\aira_mask_processed.nii"

print(f"GT exists: {os.path.exists(gt_path)}")
print(f"AIRA exists: {os.path.exists(aira_path)}")

if not os.path.exists(gt_path):
    print(f"Missing GT: {gt_path}")
if not os.path.exists(aira_path):
    print(f"Missing AIRA: {aira_path}")
