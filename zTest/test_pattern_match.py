import re

patterns = ["aira_mask.nii", "AIRA_*.nii"]
test_files = [
    "aira_mask.nii",
    "aira_mask_processed.nii",
    "AIRA_A-089_N195_.nii",
    "aira_mask.nii.gz.backup"
]

def should_keep(filename):
    for pattern in patterns:
        regex_pattern = pattern.replace('.', '\\.').replace('*', '.*')
        regex_pattern = f'^{regex_pattern}$'
        if re.match(regex_pattern, filename):
            return True
    return False

for filename in test_files:
    matches = should_keep(filename)
    print(f"{filename:30s} - {'KEEP' if matches else 'DELETE'}")
