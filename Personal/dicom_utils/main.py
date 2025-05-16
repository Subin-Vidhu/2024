"""
Main entry point for DICOM processing utilities
"""

import os
import argparse
from pathlib import Path
from .logger import logger
from .extractor import (
    extract_dicom_components,
    EXTRACTION_MODE_MINIMAL,
    EXTRACTION_MODE_STANDARD,
    EXTRACTION_MODE_FULL,
    PIXEL_FORMAT_RAW,
    PIXEL_FORMAT_PICKLE
)
from .recombiner import recombine_components
from .analyzer import analyze_dicom_compression, compare_dicom_files, analyze_dicom_tag_sizes

def process_folder(dicom_folder, output_folder, extraction_mode=EXTRACTION_MODE_FULL, pixel_format=PIXEL_FORMAT_RAW):
    """
    Extract and recombine all DICOM files in a folder
    
    Args:
        dicom_folder: Input folder with DICOM files
        output_folder: Output folder for extracted data
        extraction_mode: Level of extraction detail (minimal, standard, full)
        pixel_format: Format to save pixel data in (raw, pickle)
    """
    # Extract all components
    logger.info(f"Extracting components from DICOM files in {dicom_folder} using {extraction_mode} mode")
    logger.info(f"Saving pixel data in {pixel_format} format")
    extract_dicom_components(dicom_folder, output_folder, extraction_mode, pixel_format)
    
    # Get all metadata files
    metadata_files = list(Path(output_folder).glob('*_metadata.json'))
    logger.info(f"Found {len(metadata_files)} metadata files for recombination")
    
    # Process each file
    for metadata_file in metadata_files:
        base_name = metadata_file.stem.replace('_metadata', '')
        
        # Check for pixel file with appropriate extension based on format
        pixel_ext = '.p' if pixel_format == PIXEL_FORMAT_PICKLE else '.raw'
        pixel_file = os.path.join(output_folder, f"{base_name}_pixels{pixel_ext}")
        
        output_dcm = os.path.join(output_folder, f"{base_name}_recombined.dcm")
        
        if os.path.exists(pixel_file):
            logger.info(f"Recombining {base_name}...")
            recombine_components(metadata_file, pixel_file, output_dcm)
            
            # Find the original file for comparison
            original_file = os.path.join(dicom_folder, f"{base_name}.dcm")
            if os.path.exists(original_file):
                # Compare the files
                logger.info(f"Comparing original and recombined files...")
                comparison = compare_dicom_files(original_file, output_dcm)
                
                if comparison.get('is_identical', False):
                    logger.info("✅ The files are identical!")
                else:
                    logger.info("❌ The files have differences.")
                    
                    # If there are differences, analyze sizes in more detail
                    if comparison.get('value_differences', 0) > 0:
                        logger.info("Analyzing tag sizes for more details...")
                        analyze_dicom_tag_sizes(original_file)
                        analyze_dicom_tag_sizes(output_dcm)
            else:
                logger.warning(f"Original file {original_file} not found for comparison")
        else:
            logger.warning(f"Pixel file {pixel_file} not found for {base_name}")
    
    logger.info("Processing complete!")

def main():
    """
    Command-line entry point
    """
    parser = argparse.ArgumentParser(description='DICOM Processing Utilities')
    parser.add_argument('command', choices=['extract', 'recombine', 'analyze', 'process'],
                        help='Command to execute')
    parser.add_argument('--input', '-i', required=True, 
                        help='Input DICOM file or folder')
    parser.add_argument('--output', '-o', required=True,
                        help='Output folder or file')
    parser.add_argument('--metadata', '-m',
                        help='Metadata file for recombine command')
    parser.add_argument('--pixel-data', '-p',
                        help='Pixel data file for recombine command')
    parser.add_argument('--mode', choices=['minimal', 'standard', 'full'], default='full',
                        help='Extraction mode: minimal (metadata+pixels only), standard (essential data), full (all data)')
    parser.add_argument('--pixel-format', choices=['raw', 'pickle'], default='raw',
                        help='Pixel data format: raw (binary .raw) or pickle (Python pickle .p)')
    
    args = parser.parse_args()
    
    # Map mode string to constant
    extraction_mode = {
        'minimal': EXTRACTION_MODE_MINIMAL,
        'standard': EXTRACTION_MODE_STANDARD,
        'full': EXTRACTION_MODE_FULL
    }.get(args.mode, EXTRACTION_MODE_FULL)
    
    # Map pixel format string to constant
    pixel_format = {
        'raw': PIXEL_FORMAT_RAW,
        'pickle': PIXEL_FORMAT_PICKLE
    }.get(args.pixel_format, PIXEL_FORMAT_RAW)
    
    if args.command == 'extract':
        if os.path.isdir(args.input):
            extract_dicom_components(args.input, args.output, extraction_mode, pixel_format)
        else:
            logger.error("Input must be a directory for extract command")
    
    elif args.command == 'recombine':
        if args.metadata and args.pixel_data:
            recombine_components(args.metadata, args.pixel_data, args.output)
        else:
            logger.error("Both --metadata and --pixel-data are required for recombine command")
    
    elif args.command == 'analyze':
        if os.path.isfile(args.input):
            analyze_dicom_compression(args.input)
            analyze_dicom_tag_sizes(args.input)
            
            if os.path.isfile(args.output):
                compare_dicom_files(args.input, args.output)
        else:
            logger.error("Input must be a file for analyze command")
    
    elif args.command == 'process':
        if os.path.isdir(args.input) and os.path.isdir(args.output):
            process_folder(args.input, args.output, extraction_mode, pixel_format)
        else:
            logger.error("Both input and output must be directories for process command")

if __name__ == "__main__":
    main() 