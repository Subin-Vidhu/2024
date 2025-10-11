# Clean up old files from results directory (optional)
# Run this if you want to keep only the organized timestamped folders

import os
import glob

results_dir = 'results'

# Files to clean up (older files not in timestamped folders)
old_files = glob.glob(os.path.join(results_dir, '*.csv')) + \
           glob.glob(os.path.join(results_dir, '*.png'))

if old_files:
    print("Found old files in results directory:")
    for file in old_files:
        print(f"  • {os.path.basename(file)}")
    
    response = input("\nDo you want to delete these old files? (y/n): ").lower()
    if response == 'y':
        for file in old_files:
            try:
                os.remove(file)
                print(f"Deleted: {os.path.basename(file)}")
            except:
                print(f"Could not delete: {os.path.basename(file)}")
        print("\nCleanup complete! Only timestamped folders remain.")
    else:
        print("Cleanup cancelled.")
else:
    print("No old files found. Directory is already clean!")
