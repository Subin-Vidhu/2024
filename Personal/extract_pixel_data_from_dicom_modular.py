#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
DICOM Component Extraction and Recombination

A simpler version of the original script that uses the modular dicom_utils package.
"""

import os
from pathlib import Path
from dicom_utils import (
    extract_dicom_components,
    recombine_components, 
    analyze_dicom_compression,
    compare_dicom_files,
    analyze_dicom_tag_sizes
)

def main():
    """Main function to extract and recombine DICOM files"""
    # Example paths - replace with your actual paths
    dicom_folder = "D:/ARAMIS_radon/radonData/dcm/ARAMIS/MR/2025/5/15/AZbT-LaMX-4vjb/AZbT-LaMX-4vjb.000"
    output_folder = "D:/ARAMIS_radon/radonData/dcm/ARAMIS/MR/2025/5/15/AZbT-LaMX-4vjb/AZbT-LaMX-4vjb.000/output"
    
    # Analyze a single DICOM file to see compression details
    sample_dicom = Path(dicom_folder) / "00294.dcm"
    if sample_dicom.exists():
        print("Analyzing sample DICOM file...")
        compression_info = analyze_dicom_compression(sample_dicom)
        for key, value in compression_info.items():
            print(f"{key}: {value}")
        
        # Analyze tag sizes
        print("\nAnalyzing DICOM tag sizes...")
        tag_size_info = analyze_dicom_tag_sizes(sample_dicom)
    
    # Extract all DICOM files in the folder
    extract_dicom_components(dicom_folder, output_folder)
    
    # Example of loading pixel data back
    metadata_file = os.path.join(output_folder, "00294_metadata.json")
    pixel_file = os.path.join(output_folder, "00294_pixels.raw")
    output_dcm = os.path.join(output_folder, "00294_recombined.dcm")
    
    if os.path.exists(metadata_file) and os.path.exists(pixel_file):
        print("Recombining sample DICOM file...")
        result = recombine_components(metadata_file, pixel_file, output_dcm)
        
        # Verify recombined file
        if os.path.exists(output_dcm):
            print("Analyzing recombined DICOM file...")
            recombined_info = analyze_dicom_compression(output_dcm)
            print("Comparison between original and recombined:")
            for key in ['compression_type', 'compressed_pixel_size', 'compression_ratio']:
                if key in compression_info and key in recombined_info:
                    print(f"{key}: {compression_info[key]} (original) vs {recombined_info[key]} (recombined)")
            
            # Analyze recombined tag sizes
            if os.path.exists(output_dcm):
                print("\nAnalyzing recombined DICOM tag sizes...")
                recombined_tag_size_info = analyze_dicom_tag_sizes(output_dcm)
            
            # Compare original and recombined DICOM files in detail
            print("\nPerforming detailed tag comparison...")
            comparison_result = compare_dicom_files(sample_dicom, output_dcm)
            
            # Check if the files are identical
            if comparison_result.get('is_identical', False):
                print("✅ The original and recombined DICOM files are identical!")
            else:
                print("❌ The original and recombined DICOM files have differences.")
    else:
        print(f"Could not find metadata file {metadata_file} or pixel file {pixel_file}")

if __name__ == "__main__":
    main() 