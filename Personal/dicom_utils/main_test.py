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
from dicom_utils.recombiner import recombine_components
from dicom_utils.analyzer import analyze_dicom_compression, compare_dicom_files, analyze_dicom_tag_sizes

# Define paths
dicom_folder = r"D:\ARAMIS_radon\radonData\dcm\ARAMIS\MR\2025\6\11\AZdd-dP0y-bhpo\AZdd-dP0y-bhpo.000"
output_folder = r"D:\ARAMIS_radon\radonData\dcm\ARAMIS\MR\2025\6\11\AZdd-dP0y-bhpo\AZdd-dP0y-bhpo.000/output"
os.makedirs(output_folder, exist_ok=True)
# Analyze a sample DICOM file
sample_dicom = Path(dicom_folder) / "00294.dcm"
# print(sample_dicom)
# if sample_dicom.exists():
#     print("Analyzing sample DICOM file...")
#     compression_info = analyze_dicom_compression(sample_dicom)
#     print(f"Transfer Syntax: {compression_info['compression_type']}")
#     print(f"Compression Ratio: {compression_info['compression_ratio']:.2f}x")

# Extract all DICOM files in the folder with 'standard' extraction mode and raw pixel format
print("Extracting DICOM components with 'standard' extraction mode and raw format...")
extract_dicom_components(
    dicom_folder, 
    output_folder, 
    # extraction_mode=EXTRACTION_MODE_STANDARD,
    # extraction_mode=EXTRACTION_MODE_FULL,
    extraction_mode=EXTRACTION_MODE_MINIMAL,
    pixel_format=PIXEL_FORMAT_PICKLE
)

# Recombine a specific file with raw pixel data
# metadata_file = os.path.join(output_folder, "00294_metadata.json")
metadata_file = os.path.join(r"D:/2024/Personal/dicom_utils/00294_metadata.json")
pixel_file = os.path.join(output_folder, "00294_pixels.p")
output_dcm = os.path.join(output_folder, "00294_recombined.dcm")

if os.path.exists(metadata_file) and os.path.exists(pixel_file):
    print("Recombining DICOM components using raw pixel data...")
    # Recombine the components
    recombine_components(metadata_file, pixel_file, output_dcm)
    
    # Compare original and recombined files
    print("Comparing original and recombined files...")
    comparison = compare_dicom_files(sample_dicom, output_dcm)
    if comparison.get('is_identical', False):
        print("✅ Files are identical!")
    else:
        print(f"❌ Files have differences: {comparison.get('value_differences', 0)} value mismatches")
        
# # Example of using minimal mode with pickle format
# print("\nPerforming minimal extraction with pickle format...")
# minimal_output_folder = os.path.join(output_folder, "minimal_pickle")
# os.makedirs(minimal_output_folder, exist_ok=True)

# # Make sure to explicitly use PIXEL_FORMAT_PICKLE
# extract_dicom_components(
#     dicom_folder, 
#     minimal_output_folder, 
#     extraction_mode=EXTRACTION_MODE_MINIMAL,
#     pixel_format=PIXEL_FORMAT_RAW  # This needs to be explicitly PICKLE
# )

# # Recombine using pickle format
# pickle_metadata_file = os.path.join(minimal_output_folder, "00294_metadata.json")
# pickle_pixel_file = os.path.join(minimal_output_folder, "00294_pixels.p")  # .p extension
# pickle_output_dcm = os.path.join(minimal_output_folder, "00294_recombined.dcm")

# if os.path.exists(pickle_metadata_file) and os.path.exists(pickle_pixel_file):
#     print("Recombining DICOM components using pickle pixel data...")
#     recombine_components(pickle_metadata_file, pickle_pixel_file, pickle_output_dcm)
    
#     # Compare original and recombined files
#     print("Comparing original and pickle-recombined files...")
#     comparison = compare_dicom_files(sample_dicom, pickle_output_dcm)
#     if comparison.get('is_identical', False):
#         print("✅ Files are identical with pickle format!")
#     else:
#         print(f"❌ Files have differences with pickle format: {comparison.get('value_differences', 0)} value mismatches")