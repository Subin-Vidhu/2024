import os
import shutil

root_dir = r"K:\AIRA_FDA_Models\DATA\batch_storage"
# output_dir = os.path.join(root_dir, "ARAMIS_RAS_LPI")
output_dir = os.path.join(root_dir, "ARAMIS_RAI_LPS")

# Create output directory if not exists
os.makedirs(output_dir, exist_ok=True)

for folder in os.listdir(root_dir):
    folder_path = os.path.join(root_dir, folder)

    # Skip non-directories
    if not os.path.isdir(folder_path):
        continue

    # Skip output folder itself
    if folder == "ARAMIS_RAS_LPI":
        continue
    if folder == "ARAMIS_RAI_LPS":
        continue
    
    # Construct expected filename: AIRA_<folder>.nii
    expected_file = f"AIRA_{folder}.nii"
    file_path = os.path.join(folder_path, expected_file)

    if os.path.exists(file_path):
        print(f"Found: {file_path}")
        shutil.copy(file_path, os.path.join(output_dir, expected_file))
        print(f"Copied to: {output_dir}")
    else:
        print(f"Missing file: {expected_file} in {folder_path}")
