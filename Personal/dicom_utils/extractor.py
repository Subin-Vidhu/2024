"""
Functions for extracting components from DICOM files
"""

import os
import json
import pickle
import pydicom
from pathlib import Path
from .constants import TRANSFER_SYNTAX_NAMES, UNCOMPRESSED_TRANSFER_SYNTAXES
from .logger import logger
from .utils import get_orig_value_format

# Define extraction modes
EXTRACTION_MODE_MINIMAL = "minimal"  # Just extract metadata and pixel data
EXTRACTION_MODE_STANDARD = "standard"  # Extract metadata, pixel data, and essential binary data
EXTRACTION_MODE_FULL = "full"  # Extract all components including all binary data

# Define pixel data formats
PIXEL_FORMAT_RAW = "raw"      # Save as raw binary (.raw)
PIXEL_FORMAT_PICKLE = "pickle"  # Save as Python pickle (.p)

def extract_and_preserve_sequences(dicom_dataset):
    """
    Extract and preserve sequence data from a DICOM dataset,
    as sequences often cause issues during JSON serialization.
    
    Args:
        dicom_dataset: The DICOM dataset to extract sequences from
    
    Returns:
        Dictionary with sequence data that can be JSON serialized
    """
    sequence_data = {}
    
    for elem in dicom_dataset:
        if elem.VR == 'SQ':
            keyword = elem.keyword if hasattr(elem, 'keyword') else str(elem.tag)
            sequence_data[keyword] = []
            
            # Process each sequence item
            for i, item in enumerate(elem.value):
                item_dict = {}
                for dataset_elem in item:
                    # Handle nested sequences recursively
                    if dataset_elem.VR == 'SQ':
                        nested_keyword = dataset_elem.keyword if hasattr(dataset_elem, 'keyword') else str(dataset_elem.tag)
                        item_dict[nested_keyword] = extract_and_preserve_sequences(dataset_elem.value)
                    else:
                        # Store non-sequence elements
                        elem_keyword = dataset_elem.keyword if hasattr(dataset_elem, 'keyword') else str(dataset_elem.tag)
                        if isinstance(dataset_elem.value, bytes):
                            # Convert binary data to a list of integers for JSON serialization
                            item_dict[elem_keyword] = {
                                'tag': [dataset_elem.tag.group, dataset_elem.tag.element],
                                'VR': dataset_elem.VR,
                                'value': "BINARY_DATA",
                                'binary_length': len(dataset_elem.value)
                            }
                        else:
                            try:
                                # Try to JSON serialize the value
                                json.dumps(dataset_elem.value)
                                item_dict[elem_keyword] = {
                                    'tag': [dataset_elem.tag.group, dataset_elem.tag.element],
                                    'VR': dataset_elem.VR,
                                    'value': dataset_elem.value
                                }
                            except (TypeError, OverflowError):
                                # If it can't be serialized, convert to string
                                item_dict[elem_keyword] = {
                                    'tag': [dataset_elem.tag.group, dataset_elem.tag.element],
                                    'VR': dataset_elem.VR,
                                    'value': str(dataset_elem.value)
                                }
                
                sequence_data[keyword].append(item_dict)
    
    return sequence_data

def extract_icon_data(dicom_dataset, output_dir, base_filename, extraction_mode=EXTRACTION_MODE_FULL):
    """
    Extract icon image data from a DICOM dataset
    
    Args:
        dicom_dataset: DICOM dataset to extract icon data from
        output_dir: Directory to save binary data
        base_filename: Base filename for saving extracted data
        extraction_mode: Level of detail to extract (minimal, standard, full)
    
    Returns:
        Dictionary with extracted icon data info
    """
    icon_data = {}
    
    # In minimal mode, don't extract icon data
    if extraction_mode == EXTRACTION_MODE_MINIMAL:
        return icon_data
        
    icon_tag = pydicom.tag.Tag('IconImageSequence')  # (0088, 0200)
    
    if icon_tag in dicom_dataset and len(dicom_dataset[icon_tag].value) > 0:
        icon_seq = dicom_dataset[icon_tag].value[0]
        
        # Save all binary data in the icon sequence
        for elem in icon_seq:
            if isinstance(elem.value, bytes):
                # Special case for pixel data and lookup tables
                suffix = ""
                if elem.tag == pydicom.tag.Tag('PixelData'):
                    suffix = "_icon"
                    
                binary_file = os.path.join(
                    output_dir, 
                    f"{elem.tag.group:04x}_{elem.tag.element:04x}{suffix}.bin"
                )
                
                with open(binary_file, 'wb') as f:
                    f.write(elem.value)
                
                # Store the binary file info
                icon_data[str(elem.tag)] = {
                    'binary_file': os.path.relpath(binary_file, os.path.dirname(output_dir)),
                    'length': len(elem.value),
                    'VR': elem.VR
                }
    
    return icon_data

def extract_dicom_components(dicom_folder, output_folder, extraction_mode=EXTRACTION_MODE_FULL, pixel_format=PIXEL_FORMAT_RAW):
    """
    Extract DICOM components with compression support:
    - Store metadata as JSON files
    - Store compressed pixel data separately
    - Track compression information
    
    Args:
        dicom_folder: Path to folder containing DICOM files
        output_folder: Path to store output files
        extraction_mode: Level of extraction detail (minimal, standard, full)
                         - minimal: Only metadata and pixel data
                         - standard: Metadata, pixel data, and essential binary data
                         - full: All data including private tags and binary data
        pixel_format: Format to save pixel data in
                     - raw: Save as raw binary (.raw)
                     - pickle: Save as Python pickle (.p)
    """
    # Create output directory if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)
    
    # Validate extraction mode
    if extraction_mode not in [EXTRACTION_MODE_MINIMAL, EXTRACTION_MODE_STANDARD, EXTRACTION_MODE_FULL]:
        logger.warning(f"Invalid extraction mode: {extraction_mode}. Using 'full' mode.")
        extraction_mode = EXTRACTION_MODE_FULL
    
    # Validate pixel format
    if pixel_format not in [PIXEL_FORMAT_RAW, PIXEL_FORMAT_PICKLE]:
        logger.warning(f"Invalid pixel format: {pixel_format}. Using 'raw' format.")
        pixel_format = PIXEL_FORMAT_RAW
    
    logger.info(f"Using extraction mode: {extraction_mode}")
    logger.info(f"Using pixel format: {pixel_format}")
    
    # Get list of DICOM files
    dicom_files = list(Path(dicom_folder).glob('*.dcm'))
    
    logger.info(f"Found {len(dicom_files)} DICOM files")
    
    for i, dicom_path in enumerate(dicom_files):
        try:
            # Read DICOM file - with stop_before_pixels=False to include all data
            dicom = pydicom.dcmread(str(dicom_path), force=True, stop_before_pixels=False)
            
            # Generate base filename from original DICOM filename
            base_filename = os.path.splitext(os.path.basename(dicom_path))[0]
            
            # Get original file size
            original_file_size = os.path.getsize(dicom_path)
            
            # Extract transfer syntax information
            transfer_syntax_uid = str(dicom.file_meta.TransferSyntaxUID) if hasattr(dicom.file_meta, 'TransferSyntaxUID') else '1.2.840.10008.1.2'
            is_compressed = transfer_syntax_uid not in UNCOMPRESSED_TRANSFER_SYNTAXES
            compression_type = TRANSFER_SYNTAX_NAMES.get(transfer_syntax_uid, f"Unknown ({transfer_syntax_uid})")
            
            # Get pixel dimensions
            rows = dicom.Rows if 'Rows' in dicom else 0
            columns = dicom.Columns if 'Columns' in dicom else 0
            samples_per_pixel = dicom.SamplesPerPixel if 'SamplesPerPixel' in dicom else 1
            bits_allocated = dicom.BitsAllocated if 'BitsAllocated' in dicom else 0
            number_of_frames = getattr(dicom, 'NumberOfFrames', 1) if 'NumberOfFrames' in dicom else 1
            
            # Save preamble if present (full mode only)
            preamble_path = None
            if extraction_mode == EXTRACTION_MODE_FULL and hasattr(dicom, 'preamble') and dicom.preamble:
                preamble_path = os.path.join(output_folder, f"{base_filename}_preamble.bin")
                with open(preamble_path, 'wb') as f:
                    f.write(dicom.preamble)
            
            # Create a directory for binary data (standard and full modes)
            binary_dir = None
            if extraction_mode in [EXTRACTION_MODE_STANDARD, EXTRACTION_MODE_FULL]:
                binary_dir = os.path.join(output_folder, f"{base_filename}_binary")
                os.makedirs(binary_dir, exist_ok=True)
            
            # Save the raw compressed pixel data directly
            if 'PixelData' in dicom:
                compressed_pixel_data = dicom.PixelData
                compressed_size = len(compressed_pixel_data)
                
                # Calculate theoretical uncompressed size
                uncompressed_bytes_per_pixel = bits_allocated // 8
                theoretical_uncompressed_size = rows * columns * samples_per_pixel * uncompressed_bytes_per_pixel * number_of_frames
                
                # Save pixel data in the selected format
                if pixel_format == PIXEL_FORMAT_RAW:
                    # Save as raw binary
                    pixel_path = os.path.join(output_folder, f"{base_filename}_pixels.raw")
                    with open(pixel_path, 'wb') as f:
                        f.write(compressed_pixel_data)
                else:  # pixel_format == PIXEL_FORMAT_PICKLE
                    # Save as Python pickle with metadata
                    pixel_info = {
                        'data': compressed_pixel_data,
                        'rows': rows,
                        'columns': columns,
                        'samples_per_pixel': samples_per_pixel,
                        'bits_allocated': bits_allocated,
                        'number_of_frames': number_of_frames,
                        'transfer_syntax_uid': transfer_syntax_uid,
                        'is_compressed': is_compressed
                    }
                    pixel_path = os.path.join(output_folder, f"{base_filename}_pixels.p")
                    with open(pixel_path, 'wb') as f:
                        pickle.dump(pixel_info, f)
                
                # Compression ratio (if compressed)
                compression_ratio = theoretical_uncompressed_size / compressed_size if is_compressed and compressed_size > 0 else 1.0
            else:
                compressed_size = 0
                theoretical_uncompressed_size = 0
                compression_ratio = 1.0
                logger.warning(f"No pixel data found in {dicom_path.name}")
            
            # Create metadata dictionary with enhanced information
            metadata = {
                'FileMetaInfo': {},
                'DataElements': {},
                'BinaryDataInfo': {},
                'SequenceData': {},  # For storing sequence data
                'RawMetaInfo': {},   # For storing exact binary data of file meta info
                'PrivateTags': {},    # For tracking private tags
                'IconData': {}        # For icon image sequence data
            }
            
            # Extract icon data (standard and full modes)
            if extraction_mode in [EXTRACTION_MODE_STANDARD, EXTRACTION_MODE_FULL]:
                metadata['IconData'] = extract_icon_data(dicom, binary_dir, base_filename, extraction_mode)
            
            # Save raw file meta information
            if hasattr(dicom, 'file_meta'):
                for elem in dicom.file_meta:
                    metadata['FileMetaInfo'][elem.keyword if hasattr(elem, 'keyword') else str(elem.tag)] = {
                        'tag': [elem.tag.group, elem.tag.element],
                        'VR': elem.VR if hasattr(elem, 'VR') else 'UN',
                        'value': str(elem.value) if not isinstance(elem.value, bytes) else "BINARY_DATA"
                    }
                
                # Store raw file meta bytes (full mode only)
                if extraction_mode == EXTRACTION_MODE_FULL and hasattr(dicom.file_meta, '_dict_elements') and binary_dir:
                    raw_meta = {}
                    for tag, elem in dicom.file_meta._dict_elements.items():
                        if hasattr(elem, 'value') and isinstance(elem.value, bytes):
                            binary_file = os.path.join(binary_dir, f"meta_{tag.group:04x}_{tag.element:04x}.bin")
                            with open(binary_file, 'wb') as f:
                                f.write(elem.value)
                            raw_meta[str(tag)] = {
                                'binary_file': os.path.relpath(binary_file, output_folder),
                                'length': len(elem.value)
                            }
                    metadata['RawMetaInfo'] = raw_meta
            
            # Extract and preserve sequence data
            metadata['SequenceData'] = extract_and_preserve_sequences(dicom)
            
            # Define essential tags for standard mode
            essential_tags = [
                # Patient and study information
                'PatientID', 'PatientName', 'PatientBirthDate', 'PatientSex',
                'StudyInstanceUID', 'StudyID', 'StudyDate', 'StudyTime',
                'SeriesInstanceUID', 'SeriesNumber', 'SeriesDate', 'SeriesTime',
                # Image information
                'ImagePositionPatient', 'ImageOrientationPatient', 'SliceLocation',
                'PixelSpacing', 'SliceThickness', 'SpacingBetweenSlices',
                # MR-specific
                'EchoTime', 'RepetitionTime', 'MagneticFieldStrength', 'FlipAngle',
                # CT-specific
                'KVP', 'ExposureTime', 'XRayTubeCurrent'
            ]
            
            # Create a set of essential tag objects for faster lookup
            essential_tag_objects = set()
            for keyword in essential_tags:
                tag = pydicom.datadict.tag_for_keyword(keyword)
                if tag is not None:
                    essential_tag_objects.add(tag)
            
            # Convert DICOM dataset to dictionary, preserving VR types
            for elem in dicom:
                tag_str = str(elem.tag)
                tag_is_private = elem.tag.is_private
                elem_dict = {
                    'tag': [elem.tag.group, elem.tag.element],
                    'VR': elem.VR if hasattr(elem, 'VR') else 'UN',
                    'keyword': elem.keyword if hasattr(elem, 'keyword') else '',
                    'name': elem.name if hasattr(elem, 'name') else '',
                    'is_private': tag_is_private
                }
                
                # Skip private tags in minimal mode
                if extraction_mode == EXTRACTION_MODE_MINIMAL and tag_is_private:
                    continue
                
                # In standard mode, only include essential binary data
                if extraction_mode == EXTRACTION_MODE_STANDARD and isinstance(elem.value, bytes):
                    if elem.tag != pydicom.tag.Tag('PixelData') and elem.tag not in essential_tag_objects:
                        # Skip non-essential binary data in standard mode
                        continue
                
                if isinstance(elem.value, bytes):
                    # For binary data (including private tags), save to separate files if not in minimal mode
                    if elem.tag != pydicom.tag.Tag('PixelData') and binary_dir:  # Skip PixelData as it's handled separately
                        binary_file = os.path.join(binary_dir, f"{elem.tag.group:04x}_{elem.tag.element:04x}.bin")
                        with open(binary_file, 'wb') as f:
                            f.write(elem.value)
                        
                        # Store information about binary data
                        metadata['BinaryDataInfo'][tag_str] = {
                            'length': len(elem.value),
                            'VR': elem.VR if hasattr(elem, 'VR') else 'UN',
                            'binary_file': os.path.relpath(binary_file, output_folder)
                        }
                    elem_dict['value'] = "BINARY_DATA"
                elif elem.VR == 'SQ':
                    # For sequences, reference the data stored in SequenceData
                    elem_dict['value'] = "SEQUENCE_DATA"
                    elem_dict['items_count'] = len(elem.value)
                else:
                    try:
                        # Try to convert to native Python type
                        json.dumps(elem.value)
                        # For numeric values, preserve original format
                        if elem.VR in ['DS', 'IS', 'FL', 'FD', 'SL', 'SS', 'UL', 'US']:
                            elem_dict['original_format'] = get_orig_value_format(elem.value)
                        elem_dict['value'] = elem.value
                    except (TypeError, OverflowError):
                        # If value can't be JSON serialized, convert to string
                        elem_dict['value'] = str(elem.value)
                
                # Store in appropriate dictionary
                metadata['DataElements'][tag_str] = elem_dict
                
                # For private tags, add to private tags dictionary (in full mode only)
                if tag_is_private and extraction_mode == EXTRACTION_MODE_FULL:
                    metadata['PrivateTags'][tag_str] = elem_dict.copy()
            
            # Add encoding information
            metadata['EncodingInfo'] = {
                'is_little_endian': getattr(dicom, 'is_little_endian', True),
                'is_implicit_VR': getattr(dicom, 'is_implicit_VR', True),
                'has_preamble': hasattr(dicom, 'preamble') and dicom.preamble is not None,
                'preamble_file': os.path.basename(preamble_path) if preamble_path else None
            }
            
            # Add file metadata to capture compression info
            metadata['CompressionInfo'] = {
                'TransferSyntaxUID': transfer_syntax_uid,
                'TransferSyntaxName': compression_type,
                'IsCompressed': is_compressed,
                'OriginalFileSize': original_file_size,
                'CompressedPixelDataSize': compressed_size,
                'TheoreticalUncompressedSize': theoretical_uncompressed_size,
                'CompressionRatio': compression_ratio,
                'ExtractionMode': extraction_mode,  # Store the extraction mode used
                'PixelFormat': pixel_format  # Store the pixel format used
            }
            
            # Add image shape information
            metadata['ImageInfo'] = {
                'Rows': rows,
                'Columns': columns,
                'SamplesPerPixel': samples_per_pixel,
                'BitsAllocated': bits_allocated,
                'NumberOfFrames': number_of_frames
            }
            
            # Save metadata as JSON
            json_path = os.path.join(output_folder, f"{base_filename}_metadata.json")
            with open(json_path, 'w') as f:
                json.dump(metadata, f, indent=2)
            
            logger.info(f"Processed: {dicom_path.name}")
            logger.info(f"  - Compression: {compression_type}")
            logger.info(f"  - Original size: {original_file_size:,} bytes")
            logger.info(f"  - Pixel data size: {compressed_size:,} bytes")
            if is_compressed:
                logger.info(f"  - Compression ratio: {compression_ratio:.2f}x")
            logger.info(f"  - Metadata: {os.path.basename(json_path)}")
            logger.info(f"  - Pixel data: {os.path.basename(pixel_path)} ({pixel_format} format)")
            if binary_dir:
                logger.info(f"  - Binary data: {os.path.basename(binary_dir)}/")
            
        except Exception as e:
            logger.error(f"Error processing {dicom_path}: {e}", exc_info=True)
    
    logger.info("\nProcessing complete!")
    logger.info(f"Files saved to: {output_folder}") 