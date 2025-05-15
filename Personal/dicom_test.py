import os
from pathlib import Path

# Import from the dicom_utils package
from dicom_utils import (
    extract_dicom_components,
    recombine_components, 
    analyze_dicom_compression,
    compare_dicom_files,
    analyze_dicom_tag_sizes
)

def main():
    """Test script for the dicom_utils package"""
    # Define paths
    dicom_folder = "D:/ARAMIS_radon/radonData/dcm/ARAMIS/MR/2025/5/15/AZbT-LaMX-4vjb/AZbT-LaMX-4vjb.000"
    output_folder = "D:/ARAMIS_radon/radonData/dcm/ARAMIS/MR/2025/5/15/AZbT-LaMX-4vjb/AZbT-LaMX-4vjb.000/output"
    
    # Analyze a sample DICOM file
    sample_dicom = Path(dicom_folder) / "00294.dcm"
    if sample_dicom.exists():
        print("Analyzing sample DICOM file...")
        compression_info = analyze_dicom_compression(sample_dicom)
        print(f"Transfer Syntax: {compression_info['compression_type']}")
        print(f"Compression Ratio: {compression_info['compression_ratio']:.2f}x")
    
    # Extract all DICOM files in the folder
    extract_dicom_components(dicom_folder, output_folder)
    
    # Recombine a specific file
    metadata_file = os.path.join(output_folder, "00294_metadata.json")
    pixel_file = os.path.join(output_folder, "00294_pixels.raw")
    output_dcm = os.path.join(output_folder, "00294_recombined.dcm")
    
    if os.path.exists(metadata_file) and os.path.exists(pixel_file):
        # Recombine the components
        recombine_components(metadata_file, pixel_file, output_dcm)
        
        # Compare original and recombined files
        comparison = compare_dicom_files(sample_dicom, output_dcm)
        if comparison['is_identical']:
            print("✅ Files are identical!")
        else:
            print(f"❌ Files have differences: {comparison['value_differences']} value mismatches")

if __name__ == "__main__":
    main() 