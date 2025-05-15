"""
DICOM Extraction Demo

A demonstration of the DICOM utilities package to extract, modify and recombine DICOM files.
"""

import os
import argparse
from pathlib import Path
from dicom_utils import (
    extract_dicom_components,
    recombine_components,
    analyze_dicom_compression,
    compare_dicom_files,
    analyze_dicom_tag_sizes
)

def main():
    """Demo entry point"""
    parser = argparse.ArgumentParser(description='DICOM Extraction Demo')
    parser.add_argument('--input', '-i', required=True, help='Path to DICOM file or directory')
    parser.add_argument('--output', '-o', required=True, help='Output directory')
    args = parser.parse_args()
    
    input_path = Path(args.input)
    output_dir = Path(args.output)
    
    # Create output directory if it doesn't exist
    output_dir.mkdir(exist_ok=True, parents=True)
    
    if input_path.is_file():
        # Process a single file
        print(f"Processing single file: {input_path}")
        
        # Analyze original file
        print("\n=== Original DICOM Analysis ===")
        compression_info = analyze_dicom_compression(input_path)
        print(f"Transfer Syntax: {compression_info['compression_type']}")
        print(f"Compression Ratio: {compression_info['compression_ratio']:.2f}x")
        print(f"File Size: {compression_info['file_size']:,} bytes")
        
        # Extract components 
        extract_dir = output_dir / input_path.stem
        extract_dir.mkdir(exist_ok=True)
        print(f"\n=== Extracting DICOM Components to {extract_dir} ===")
        extract_dicom_components(input_path.parent, extract_dir)
        
        # Find extracted files
        metadata_file = next(extract_dir.glob(f"{input_path.stem}_metadata.json"))
        pixel_file = next(extract_dir.glob(f"{input_path.stem}_pixels.raw"))
        
        # Recombine
        output_file = output_dir / f"{input_path.stem}_recombined.dcm"
        print(f"\n=== Recombining Components to {output_file} ===")
        result = recombine_components(metadata_file, pixel_file, output_file)
        
        # Compare files
        print("\n=== Comparing Original and Recombined Files ===")
        comparison = compare_dicom_files(input_path, output_file)
        
        if comparison.get('is_identical', False):
            print("✅ Files are identical!")
        else:
            print(f"❌ Files have differences:")
            print(f"  - Missing tags: {comparison.get('missing_tags', 0)}")
            print(f"  - Extra tags: {comparison.get('extra_tags', 0)}")
            print(f"  - Value differences: {comparison.get('value_differences', 0)}")
            print(f"  - Pixel data identical: {comparison.get('pixel_data_identical', False)}")
        
    elif input_path.is_dir():
        # Process a directory of files
        print(f"Processing directory: {input_path}")
        
        # Extract all files
        print(f"\n=== Extracting All DICOM Files to {output_dir} ===")
        extract_dicom_components(input_path, output_dir)
        
        # Find all metadata files
        metadata_files = list(output_dir.glob("*_metadata.json"))
        print(f"\nFound {len(metadata_files)} extracted files")
        
        # Process each file
        for metadata_file in metadata_files:
            base_name = metadata_file.stem.replace("_metadata", "")
            pixel_file = output_dir / f"{base_name}_pixels.raw"
            
            if pixel_file.exists():
                print(f"\n=== Processing {base_name} ===")
                
                # Recombine
                output_file = output_dir / f"{base_name}_recombined.dcm"
                result = recombine_components(metadata_file, pixel_file, output_file)
                
                # Original file for comparison
                original_file = input_path / f"{base_name}.dcm"
                if original_file.exists():
                    comparison = compare_dicom_files(original_file, output_file)
                    if comparison.get('is_identical', False):
                        print(f"✅ {base_name}: Files are identical!")
                    else:
                        print(f"❌ {base_name}: Files have differences - " 
                              f"{comparison.get('value_differences', 0)} value mismatches")
    else:
        print(f"Error: {input_path} is not a valid file or directory")

if __name__ == "__main__":
    main() 