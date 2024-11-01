import os
import shutil
from pathlib import Path

def organize_files():
    # Source directory
    source_dir = r"C:\Users\Subin-PC\Downloads\Telegram Desktop"
    
    # Get all files in the directory
    files = [f for f in os.listdir(source_dir) if os.path.isfile(os.path.join(source_dir, f))]
    
    # Create a "Organized_Files" directory to avoid mixing with existing folders
    organized_dir = os.path.join(source_dir, "Organized_Files")
    os.makedirs(organized_dir, exist_ok=True)
    
    for file in files:
        # Get the file extension
        extension = Path(file).suffix.lower().replace(".", "")
        if not extension:
            extension = "no_extension"
            
        # Create extension-specific folder inside Organized_Files
        ext_folder = os.path.join(organized_dir, extension)
        os.makedirs(ext_folder, exist_ok=True)
        
        # Source and destination paths
        source_path = os.path.join(source_dir, file)
        dest_path = os.path.join(ext_folder, file)
        
        try:
            # Move the file to its corresponding folder
            shutil.move(source_path, dest_path)
            print(f"Moved {file} to {extension} folder")
        except Exception as e:
            print(f"Error moving {file}: {str(e)}")

if __name__ == "__main__":
    organize_files()
