import os
import sys
from pathlib import Path

# Add the parent directory to the system path so Python can find the package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Now we can import from dicom_utils as a package
from dicom_utils.extractor import (
    extract_dicom_components,
    EXTRACTION_MODE_MINIMAL,
    EXTRACTION_MODE_STANDARD,
    EXTRACTION_MODE_FULL,
    PIXEL_FORMAT_RAW,
    PIXEL_FORMAT_PICKLE
)
# Import the new recombiner instead of the old one
from dicom_utils.new_recombiner import recombine_components
from dicom_utils.analyzer import analyze_dicom_compression, compare_dicom_files, analyze_dicom_tag_sizes

# Define paths
dicom_folder = r"D:/ARAMIS_radon/radonData/dcm/ARAMIS/MR/2025/5/21/AZbx-T64W-wSYq/AZbx-T64W-wSYq.000"
output_folder = r"D:/ARAMIS_radon/radonData/dcm/ARAMIS/MR/2025/5/21/AZbx-T64W-wSYq/AZbx-T64W-wSYq.000/output"
os.makedirs(output_folder, exist_ok=True)
# Analyze a sample DICOM file
sample_dicom = Path(dicom_folder) / "00294.dcm"

# Extract all DICOM files in the folder with 'minimal' extraction mode and pickle pixel format
print("Extracting DICOM components with 'minimal' extraction mode and pickle format...")
extract_dicom_components(
    dicom_folder, 
    output_folder, 
    extraction_mode=EXTRACTION_MODE_MINIMAL,
    pixel_format=PIXEL_FORMAT_PICKLE
)

# Use the new format JSON metadata file
metadata_file = os.path.join(r"D:/2024/Personal/dicom_utils/00294_metadata.json")
pixel_file = os.path.join(output_folder, "00294_pixels.p")
output_dcm = os.path.join(output_folder, "00294_recombined_new.dcm")  # Different output name to avoid confusion

if os.path.exists(metadata_file) and os.path.exists(pixel_file):
    print("Recombining DICOM components using new recombiner...")
    # Recombine the components with new recombiner
    recombine_components(metadata_file, pixel_file, output_dcm)
    
    # Compare original and recombined files
    print("Comparing original and recombined files...")
    comparison = compare_dicom_files(sample_dicom, output_dcm)
    if comparison.get('is_identical', False):
        print("✅ Files are identical!")
    else:
        print(f"❌ Files have differences: {comparison.get('value_differences', 0)} value mismatches")
        
        # Analyze the differences in more detail
        print("Analyzing original file...")
        analyze_dicom_tag_sizes(sample_dicom)
        print("Analyzing recombined file...")
        analyze_dicom_tag_sizes(output_dcm)
else:
    print(f"Error: Could not find metadata file ({metadata_file}) or pixel file ({pixel_file})")