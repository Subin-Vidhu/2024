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
    EXTRACTION_MODE_FULL
)
from dicom_utils.recombiner import recombine_components
from dicom_utils.analyzer import analyze_dicom_compression, compare_dicom_files, analyze_dicom_tag_sizes

# Define paths
dicom_folder = "D:/ARAMIS_radon/radonData/dcm/ARAMIS/MR/2025/5/15/AZbT-LaMX-4vjb/AZbT-LaMX-4vjb.000"
output_folder = "D:/ARAMIS_radon/radonData/dcm/ARAMIS/MR/2025/5/15/AZbT-LaMX-4vjb/AZbT-LaMX-4vjb.000/output"
# output_folder = "D:/ARAMIS_radon/radonData/dcm/ARAMIS/MR/2025/5/15/AZbT-LaMX-4vjb/AZbT-LaMX-4vjb.000/output/minimal"

# Analyze a sample DICOM file
sample_dicom = Path(dicom_folder) / "00294.dcm"
if sample_dicom.exists():
    print("Analyzing sample DICOM file...")
    compression_info = analyze_dicom_compression(sample_dicom)
    print(f"Transfer Syntax: {compression_info['compression_type']}")
    print(f"Compression Ratio: {compression_info['compression_ratio']:.2f}x")

# Extract all DICOM files in the folder with 'standard' extraction mode
# This will extract metadata, pixel data, and essential binary data
print("Extracting DICOM components with 'standard' extraction mode...")
# extract_dicom_components(dicom_folder, output_folder, EXTRACTION_MODE_STANDARD)
extract_dicom_components(dicom_folder, output_folder, EXTRACTION_MODE_FULL)

# Recombine a specific file
metadata_file = os.path.join(output_folder, "00294_metadata.json")
pixel_file = os.path.join(output_folder, "00294_pixels.raw")
output_dcm = os.path.join(output_folder, "00294_recombined.dcm")

if os.path.exists(metadata_file) and os.path.exists(pixel_file):
    print("Recombining DICOM components...")
    # Recombine the components
    recombine_components(metadata_file, pixel_file, output_dcm)
    
    # Compare original and recombined files
    print("Comparing original and recombined files...")
    comparison = compare_dicom_files(sample_dicom, output_dcm)
    if comparison.get('is_identical', False):
        print("✅ Files are identical!")
    else:
        print(f"❌ Files have differences: {comparison.get('value_differences', 0)} value mismatches")
        
# Example of using minimal mode for a quick extraction with minimal output
# print("\nPerforming minimal extraction for comparison...")
# minimal_output_folder = os.path.join(output_folder, "minimal")
# os.makedirs(minimal_output_folder, exist_ok=True)
# extract_dicom_components(dicom_folder, minimal_output_folder, EXTRACTION_MODE_MINIMAL)