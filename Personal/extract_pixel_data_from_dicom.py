# -*- coding: utf-8 -*-
"""
Created on Thu May 15 15:09:06 2025

@author: Subin-PC
"""

import pydicom
import json
import os
import numpy as np
from pathlib import Path
from pydicom.dataset import FileDataset
import datetime
import pydicom.uid
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, 
                   format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Dictionary of common transfer syntax UIDs for reference
TRANSFER_SYNTAX_NAMES = {
    '1.2.840.10008.1.2': 'Implicit VR Little Endian (Uncompressed)',
    '1.2.840.10008.1.2.1': 'Explicit VR Little Endian (Uncompressed)',
    '1.2.840.10008.1.2.2': 'Explicit VR Big Endian (Uncompressed)',
    '1.2.840.10008.1.2.4.50': 'JPEG Baseline (Process 1)',
    '1.2.840.10008.1.2.4.51': 'JPEG Extended (Process 2 & 4)',
    '1.2.840.10008.1.2.4.57': 'JPEG Lossless, Non-Hierarchical (Process 14)',
    '1.2.840.10008.1.2.4.70': 'JPEG Lossless, Non-Hierarchical, First-Order Prediction',
    '1.2.840.10008.1.2.4.80': 'JPEG-LS Lossless',
    '1.2.840.10008.1.2.4.81': 'JPEG-LS Lossy (Near-Lossless)',
    '1.2.840.10008.1.2.4.90': 'JPEG 2000 Lossless',
    '1.2.840.10008.1.2.4.91': 'JPEG 2000 Lossy',
    '1.2.840.10008.1.2.5': 'RLE Lossless'
}

# List of uncompressed transfer syntaxes
UNCOMPRESSED_TRANSFER_SYNTAXES = [
    '1.2.840.10008.1.2',    # Implicit VR Little Endian
    '1.2.840.10008.1.2.1',  # Explicit VR Little Endian
    '1.2.840.10008.1.2.2'   # Explicit VR Big Endian
]

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

def extract_icon_data(dicom_dataset, output_dir, base_filename):
    """
    Extract icon image data from a DICOM dataset
    
    Args:
        dicom_dataset: DICOM dataset to extract icon data from
        output_dir: Directory to save binary data
        base_filename: Base filename for saving extracted data
    
    Returns:
        Dictionary with extracted icon data info
    """
    icon_data = {}
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

def extract_dicom_components(dicom_folder, output_folder):
    """
    Extract DICOM components with compression support:
    - Store metadata as JSON files
    - Store compressed pixel data separately
    - Track compression information
    
    Args:
        dicom_folder: Path to folder containing DICOM files
        output_folder: Path to store output files
    """
    # Create output directory if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)
    
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
            
            # Save preamble if present
            preamble_path = None
            if hasattr(dicom, 'preamble') and dicom.preamble:
                preamble_path = os.path.join(output_folder, f"{base_filename}_preamble.bin")
                with open(preamble_path, 'wb') as f:
                    f.write(dicom.preamble)
            
            # Create a directory for binary data
            binary_dir = os.path.join(output_folder, f"{base_filename}_binary")
            os.makedirs(binary_dir, exist_ok=True)
            
            # Save the raw compressed pixel data directly
            if 'PixelData' in dicom:
                compressed_pixel_data = dicom.PixelData
                compressed_size = len(compressed_pixel_data)
                
                # Calculate theoretical uncompressed size
                uncompressed_bytes_per_pixel = bits_allocated // 8
                theoretical_uncompressed_size = rows * columns * samples_per_pixel * uncompressed_bytes_per_pixel * number_of_frames
                
                # Save compressed pixel data
                pixel_path = os.path.join(output_folder, f"{base_filename}_pixels.raw")
                with open(pixel_path, 'wb') as f:
                    f.write(compressed_pixel_data)
                
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
            
            # Extract icon data
            metadata['IconData'] = extract_icon_data(dicom, binary_dir, base_filename)
            
            # Save raw file meta information
            if hasattr(dicom, 'file_meta'):
                for elem in dicom.file_meta:
                    metadata['FileMetaInfo'][elem.keyword if hasattr(elem, 'keyword') else str(elem.tag)] = {
                        'tag': [elem.tag.group, elem.tag.element],
                        'VR': elem.VR if hasattr(elem, 'VR') else 'UN',
                        'value': str(elem.value) if not isinstance(elem.value, bytes) else "BINARY_DATA"
                    }
                
                # Store raw file meta bytes
                if hasattr(dicom.file_meta, '_dict_elements'):
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
            
            # Helper function to preserve numeric format
            def get_orig_value_format(value):
                """Get original value format for proper serialization"""
                if isinstance(value, (int, float)):
                    return str(value)
                return value
            
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
                
                if isinstance(elem.value, bytes):
                    # For binary data (including private tags), save to separate files
                    if elem.tag != pydicom.tag.Tag('PixelData'):  # Skip PixelData as it's handled separately
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
                
                # For private tags, add to private tags dictionary 
                if tag_is_private:
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
                'CompressionRatio': compression_ratio
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
            logger.info(f"  - Pixel data: {os.path.basename(pixel_path)}")
            logger.info(f"  - Binary data: {os.path.basename(binary_dir)}/")
            
        except Exception as e:
            logger.error(f"Error processing {dicom_path}: {e}", exc_info=True)
    
    logger.info("\nProcessing complete!")
    logger.info(f"Files saved to: {output_folder}")

def restore_sequence_data(dataset, sequence_data):
    """
    Restore sequence data to a DICOM dataset
    
    Args:
        dataset: The DICOM dataset to add sequence data to
        sequence_data: Dictionary containing sequence data
    """
    import pydicom.sequence
    
    for keyword, items in sequence_data.items():
        # Try to get the tag from keyword or string representation
        try:
            if keyword.startswith('('):
                # This is a tag string like '(0008, 1140)'
                tag = pydicom.tag.Tag(keyword.strip('()').replace(' ', ''))
            else:
                # This is a keyword like 'ReferencedImageSequence'
                tag = pydicom.datadict.tag_for_keyword(keyword)
            
            # Create a new sequence
            seq = pydicom.sequence.Sequence()
            
            # Add each item to the sequence
            for item_dict in items:
                ds = pydicom.dataset.Dataset()
                
                # Add each element in the item
                for elem_keyword, elem_data in item_dict.items():
                    if isinstance(elem_data, dict) and 'tag' in elem_data and 'VR' in elem_data:
                        # This is a regular element
                        elem_tag = pydicom.tag.Tag(elem_data['tag'][0], elem_data['tag'][1])
                        elem_vr = elem_data['VR']
                        elem_value = elem_data['value']
                        
                        if elem_value == "BINARY_DATA":
                            # Skip binary data for now
                            continue
                        
                        # Add the element to the dataset
                        ds.add_new(elem_tag, elem_vr, elem_value)
                    elif isinstance(elem_data, dict) and all(isinstance(v, list) for v in elem_data.values()):
                        # This is a nested sequence
                        restore_sequence_data(ds, {elem_keyword: elem_data})
                
                # Add the item to the sequence
                seq.append(ds)
            
            # Add the sequence to the dataset
            if hasattr(dataset, 'add_new'):
                try:
                    dataset.add_new(tag, 'SQ', seq)
                except Exception as e:
                    logger.warning(f"Could not add sequence {keyword} to dataset: {e}")
            
        except Exception as e:
            logger.warning(f"Could not restore sequence {keyword}: {e}")

def recombine_components(metadata_file, pixel_file, output_dcm):
    """
    Recombine metadata and pixel data into a DICOM file,
    preserving original compression and metadata structure.
    
    Args:
        metadata_file: Path to JSON metadata file
        pixel_file: Path to raw pixel data file
        output_dcm: Path to save output DICOM file
    """
    # Load metadata
    with open(metadata_file, 'r') as f:
        metadata = json.load(f)
    
    # Get base directory for relative paths
    base_dir = os.path.dirname(metadata_file)

    # Create new DICOM dataset
    file_meta = pydicom.dataset.FileMetaDataset()
    
    # Restore file meta information from saved metadata
    file_meta_info = metadata.get('FileMetaInfo', {})
    for key, elem_info in file_meta_info.items():
        if key != 'TransferSyntaxUID':  # Handle this separately to ensure it's set correctly
            try:
                tag = pydicom.tag.Tag(elem_info['tag'][0], elem_info['tag'][1])
                vr = elem_info['VR']
                value = elem_info['value']
                
                if value != "BINARY_DATA":
                    if vr == 'UI':  # Handle UIDs
                        file_meta.add(pydicom.DataElement(tag, vr, value))
                    else:
                        file_meta.add(pydicom.DataElement(tag, vr, value))
            except Exception as e:
                logger.warning(f"Error restoring file meta element {key}: {e}")
    
    # Make sure these critical elements are set
    transfer_syntax_uid = metadata.get('CompressionInfo', {}).get('TransferSyntaxUID', '1.2.840.10008.1.2')
    file_meta.TransferSyntaxUID = transfer_syntax_uid
    
    if 'MediaStorageSOPClassUID' not in file_meta:
        file_meta.MediaStorageSOPClassUID = file_meta_info.get('MediaStorageSOPClassUID', pydicom.uid.generate_uid())
    
    if 'MediaStorageSOPInstanceUID' not in file_meta:
        file_meta.MediaStorageSOPInstanceUID = file_meta_info.get('MediaStorageSOPInstanceUID', pydicom.uid.generate_uid())
    
    if 'ImplementationClassUID' not in file_meta:
        file_meta.ImplementationClassUID = file_meta_info.get('ImplementationClassUID', pydicom.uid.PYDICOM_IMPLEMENTATION_UID)
    
    # Restore binary file meta data
    raw_meta_info = metadata.get('RawMetaInfo', {})
    for tag_str, binary_info in raw_meta_info.items():
        try:
            tag = pydicom.tag.Tag(tag_str.strip('()').replace(' ', ''))
            binary_file = os.path.join(base_dir, binary_info['binary_file'])
            if os.path.exists(binary_file):
                with open(binary_file, 'rb') as f:
                    binary_data = f.read()
                
                # Add back to file_meta
                if tag not in file_meta:
                    file_meta.add(pydicom.DataElement(tag, 'OB', binary_data))
        except Exception as e:
            logger.warning(f"Error restoring binary file meta for {tag_str}: {e}")
    
    # Load preamble if present
    preamble = None
    encoding_info = metadata.get('EncodingInfo', {})
    if encoding_info.get('has_preamble', False) and encoding_info.get('preamble_file'):
        preamble_path = os.path.join(base_dir, encoding_info['preamble_file'])
        if os.path.exists(preamble_path):
            with open(preamble_path, 'rb') as f:
                preamble = f.read()
        else:
            preamble = b"\0" * 128
    else:
        preamble = b"\0" * 128

    # Create dataset with proper file meta and preamble
    ds = FileDataset(output_dcm, {}, file_meta=file_meta, preamble=preamble)

    # Restore encoding information
    ds.is_little_endian = encoding_info.get('is_little_endian', True)
    ds.is_implicit_VR = encoding_info.get('is_implicit_VR', True)

    # Function to format numeric strings exactly as in the original
    def format_numeric_value(value, original_str):
        """Format numeric value to match original string format exactly"""
        if isinstance(value, (int, float)) and isinstance(original_str, str):
            # If original has no decimal point but is a float, remove the .0
            if '.' not in original_str and str(value).endswith('.0'):
                return int(value)
            # If original is in scientific notation, match that format
            if 'e' in original_str.lower():
                # Try to match the exact scientific notation
                original_e_pos = original_str.lower().find('e')
                original_exp = original_str[original_e_pos:]
                # Handle differences in exponent notation (e-012 vs e-12)
                if '-0' in original_exp:
                    new_exp = original_exp.replace('-0', '-')
                    return float(str(value).replace('e-', 'e-0'))
        return value
    
    # Process all data elements (including private tags)
    binary_data_info = metadata.get('BinaryDataInfo', {})
    
    # First, restore non-binary data elements
    for tag_str, elem_info in metadata.get('DataElements', {}).items():
        try:
            tag = pydicom.tag.Tag(elem_info['tag'][0], elem_info['tag'][1])
            vr = elem_info['VR']
            value = elem_info['value']
            
            # Skip binary data elements as they will be handled separately
            if value == "BINARY_DATA":
                continue
            
            # Skip sequence data as it will be restored separately
            if value == "SEQUENCE_DATA":
                continue
                
            # Create and set the data element
            if vr == 'SQ':
                # Handle sequences (empty for now, will be populated later)
                ds.add_new(tag, vr, [])
            elif vr == 'DS' or vr == 'FL' or vr == 'FD':
                # Handle decimal strings and float values
                # Check if it's a string representation of a list/array
                if isinstance(value, str) and value.startswith('[') and value.endswith(']'):
                    try:
                        # Convert string representation of array to actual array of floats
                        # First remove brackets and split by commas
                        value_str = value[1:-1]
                        values = []
                        for v in value_str.split(','):
                            v = v.strip()
                            # Try to match original format exactly
                            values.append(format_numeric_value(float(v), v))
                        ds.add_new(tag, vr, values)
                    except Exception as e:
                        logger.warning(f"Error converting array value for {tag_str}: {e}")
                        ds.add_new(tag, vr, value)
                else:
                    # For single values, preserve original format
                    original_format = elem_info.get('original_format')
                    try:
                        if vr == 'DS' and original_format and '.' not in original_format and original_format.isdigit():
                            # If it's a decimal string with no decimal point, use int
                            ds.add_new(tag, vr, int(float(value)))
                        else:
                            # Otherwise use formatted value
                            ds.add_new(tag, vr, format_numeric_value(float(value) if vr != 'DS' else value, 
                                                                  original_format if original_format else value))
                    except:
                        ds.add_new(tag, vr, value)
            elif vr == 'IS' or vr == 'SS' or vr == 'US' or vr == 'SL' or vr == 'UL':
                # Handle integer strings and integer values
                if isinstance(value, str) and value.startswith('[') and value.endswith(']'):
                    try:
                        value_str = value[1:-1]
                        values = [int(v.strip()) for v in value_str.split(',')]
                        ds.add_new(tag, vr, values)
                    except Exception as e:
                        logger.warning(f"Error converting array value for {tag_str}: {e}")
                        ds.add_new(tag, vr, value)
                else:
                    # Ensure integers are stored as integers, not floats
                    original_format = elem_info.get('original_format')
                    try:
                        if vr == 'IS':
                            ds.add_new(tag, vr, int(float(value)))
                        else:
                            ds.add_new(tag, vr, value)
                    except:
                        ds.add_new(tag, vr, value)
            elif vr == 'CS':
                # Handle Code Strings which may be arrays
                if isinstance(value, str) and value.startswith('[') and value.endswith(']') and "'" in value:
                    try:
                        # This handles lists of strings like "['DERIVED', 'SECONDARY']"
                        # We need to eval it safely to convert to a real list
                        import ast
                        values = ast.literal_eval(value)
                        ds.add_new(tag, vr, values)
                    except Exception as e:
                        logger.warning(f"Error converting CS array for {tag_str}: {e}")
                        ds.add_new(tag, vr, value)
                else:
                    ds.add_new(tag, vr, value)
            elif vr == 'UI':
                # Handle UIDs
                ds.add_new(tag, vr, value)
            else:
                # Handle all other VR types
                ds.add_new(tag, vr, value)
        except Exception as e:
            logger.warning(f"Error restoring element {tag_str}: {e}")
    
    # Now restore binary data elements (including private tags)
    for tag_str, binary_info in binary_data_info.items():
        try:
            # Parse tag from string representation
            tag_parts = tag_str.strip('()').replace(' ', '').split(',')
            if len(tag_parts) == 2:
                tag = pydicom.tag.Tag(int(tag_parts[0], 16), int(tag_parts[1], 16))
            else:
                # Try to convert directly if it's in format (xxxx,xxxx)
                tag = pydicom.tag.Tag(tag_str.strip('()').replace(' ', ''))
            
            # Get VR from info
            vr = binary_info.get('VR', 'OB')  # Default to OB for binary data
            
            # Load binary file
            binary_file = os.path.join(base_dir, binary_info['binary_file'])
            if os.path.exists(binary_file):
                with open(binary_file, 'rb') as f:
                    binary_data = f.read()
                
                # Add to dataset with appropriate VR
                ds.add(pydicom.DataElement(tag, vr, binary_data))
            else:
                logger.warning(f"Binary file not found for tag {tag_str}: {binary_file}")
        except Exception as e:
            logger.warning(f"Error restoring binary data for {tag_str}: {e}")
    
    # Restore sequence data with special handling for Icon Image Sequence
    if 'SequenceData' in metadata:
        restore_sequence_data(ds, metadata['SequenceData'])
    
    # Special handling for Icon Image Sequence
    icon_tag = pydicom.tag.Tag('IconImageSequence')  # (0088, 0200)
    icon_binary_data = metadata.get('IconData', {})
    
    if icon_tag in ds and len(ds[icon_tag].value) > 0 and icon_binary_data:
        icon_seq = ds[icon_tag].value[0]
        
        # Restore binary data for icon image
        for tag_str, binary_info in icon_binary_data.items():
            try:
                # Parse tag from string representation
                tag_parts = tag_str.strip('()').replace(' ', '').split(',')
                if len(tag_parts) == 2:
                    tag = pydicom.tag.Tag(int(tag_parts[0], 16), int(tag_parts[1], 16))
                else:
                    tag = pydicom.tag.Tag(tag_str.strip('()').replace(' ', ''))
                
                vr = binary_info.get('VR', 'OW')  # Default to OW for icon data
                binary_file = os.path.join(base_dir, binary_info['binary_file'])
                
                if os.path.exists(binary_file):
                    with open(binary_file, 'rb') as f:
                        binary_data = f.read()
                    
                    # Add to icon sequence
                    icon_seq.add(pydicom.DataElement(tag, vr, binary_data))
            except Exception as e:
                logger.warning(f"Error restoring icon binary data for {tag_str}: {e}")

    # Load raw pixel data
    with open(pixel_file, 'rb') as f:
        pixel_data = f.read()
    
    # Set pixel data
    pixel_tag = pydicom.tag.Tag('PixelData')
    if metadata.get('CompressionInfo', {}).get('IsCompressed', False):
        ds.add_new(pixel_tag, 'OB', pixel_data)  # OB for compressed pixel data
    else:
        ds.add_new(pixel_tag, 'OW', pixel_data)  # OW for uncompressed pixel data

    # Save to DICOM file (explicitly specify write_like_original=True to maintain format)
    ds.save_as(output_dcm, write_like_original=True)
    
    # Output size comparison
    new_size = os.path.getsize(output_dcm)
    original_size = metadata.get('CompressionInfo', {}).get('OriginalFileSize', 0)
    
    logger.info(f"Saved recombined DICOM to: {output_dcm}")
    logger.info(f"Original file size: {original_size:,} bytes")
    logger.info(f"Reconstructed file size: {new_size:,} bytes")
    logger.info(f"Size difference: {new_size - original_size:+,} bytes ({(new_size/original_size - 1)*100:.2f}%)")
    
    return {
        'file_path': output_dcm,
        'original_size': original_size,
        'new_size': new_size,
        'is_compressed': metadata.get('CompressionInfo', {}).get('IsCompressed', False),
        'compression_type': metadata.get('CompressionInfo', {}).get('TransferSyntaxName', 'Unknown')
    }

def analyze_dicom_compression(dicom_path):
    """
    Analyze DICOM file compression details
    
    Args:
        dicom_path: Path to DICOM file
    
    Returns:
        Dictionary with compression details
    """
    try:
        # Read DICOM file
        dicom = pydicom.dcmread(str(dicom_path), force=True)
        
        # Get file size
        file_size = os.path.getsize(dicom_path)
        
        # Get transfer syntax
        transfer_syntax_uid = str(dicom.file_meta.TransferSyntaxUID)
        compression_type = TRANSFER_SYNTAX_NAMES.get(transfer_syntax_uid, f"Unknown ({transfer_syntax_uid})")
        is_compressed = transfer_syntax_uid not in UNCOMPRESSED_TRANSFER_SYNTAXES
        
        # Get pixel dimensions
        rows = dicom.Rows if 'Rows' in dicom else 0
        columns = dicom.Columns if 'Columns' in dicom else 0
        samples_per_pixel = dicom.SamplesPerPixel if 'SamplesPerPixel' in dicom else 1
        bits_allocated = dicom.BitsAllocated if 'BitsAllocated' in dicom else 0
        number_of_frames = getattr(dicom, 'NumberOfFrames', 1) if 'NumberOfFrames' in dicom else 1
        
        # Calculate theoretical uncompressed size
        uncompressed_bytes_per_pixel = bits_allocated // 8
        theoretical_uncompressed_size = rows * columns * samples_per_pixel * uncompressed_bytes_per_pixel * number_of_frames
        
        # Get compressed pixel data size
        compressed_pixel_size = len(dicom.PixelData) if 'PixelData' in dicom else 0
        
        # Compression ratio
        compression_ratio = theoretical_uncompressed_size / compressed_pixel_size if is_compressed and compressed_pixel_size > 0 else 1.0
        
        return {
            'file_path': dicom_path,
            'file_size': file_size,
            'transfer_syntax_uid': transfer_syntax_uid,
            'compression_type': compression_type,
            'is_compressed': is_compressed,
            'rows': rows,
            'columns': columns,
            'samples_per_pixel': samples_per_pixel,
            'bits_allocated': bits_allocated,
            'number_of_frames': number_of_frames,
            'theoretical_uncompressed_size': theoretical_uncompressed_size,
            'compressed_pixel_size': compressed_pixel_size,
            'compression_ratio': compression_ratio
        }
    except Exception as e:
        logger.error(f"Error analyzing {dicom_path}: {e}", exc_info=True)
        return {
            'file_path': dicom_path,
            'error': str(e)
        }

def compare_dicom_files(original_dicom_path, recombined_dicom_path):
    """
    Compare two DICOM files to check if all tags and values are the same.
    
    Args:
        original_dicom_path: Path to the original DICOM file
        recombined_dicom_path: Path to the recombined DICOM file
    
    Returns:
        Dictionary with comparison results
    """
    try:
        # Read both DICOM files
        original_dicom = pydicom.dcmread(str(original_dicom_path), force=True)
        recombined_dicom = pydicom.dcmread(str(recombined_dicom_path), force=True)
        
        # Get file sizes
        original_size = os.path.getsize(original_dicom_path)
        recombined_size = os.path.getsize(recombined_dicom_path)
        
        # Compare file meta information
        meta_differences = []
        if hasattr(original_dicom, 'file_meta') and hasattr(recombined_dicom, 'file_meta'):
            original_meta_tags = set([elem.tag for elem in original_dicom.file_meta])
            recombined_meta_tags = set([elem.tag for elem in recombined_dicom.file_meta])
            
            # Tags in original but not in recombined
            missing_meta_tags = original_meta_tags - recombined_meta_tags
            if missing_meta_tags:
                for tag in missing_meta_tags:
                    elem = original_dicom.file_meta[tag]
                    meta_differences.append(f"Missing meta tag: {elem.tag} ({elem.name if hasattr(elem, 'name') else 'Unknown'})")
            
            # Tags in both - check for value differences
            common_meta_tags = original_meta_tags.intersection(recombined_meta_tags)
            for tag in common_meta_tags:
                orig_elem = original_dicom.file_meta[tag]
                recom_elem = recombined_dicom.file_meta[tag]
                
                # Skip binary data comparison for simplicity
                if isinstance(orig_elem.value, bytes) or isinstance(recom_elem.value, bytes):
                    continue
                
                if str(orig_elem.value) != str(recom_elem.value):
                    meta_differences.append(f"Meta value mismatch for {orig_elem.tag} ({orig_elem.name if hasattr(orig_elem, 'name') else 'Unknown'}): "
                                          f"Original: {orig_elem.value}, Recombined: {recom_elem.value}")
        
        # Compare dataset elements (excluding pixel data)
        data_differences = []
        original_tags = set([elem.tag for elem in original_dicom if elem.tag != pydicom.tag.Tag('PixelData')])
        recombined_tags = set([elem.tag for elem in recombined_dicom if elem.tag != pydicom.tag.Tag('PixelData')])
        
        # Tags in original but not in recombined
        missing_tags = original_tags - recombined_tags
        if missing_tags:
            for tag in missing_tags:
                elem = original_dicom[tag]
                data_differences.append(f"Missing tag: {elem.tag} ({elem.name if hasattr(elem, 'name') else 'Unknown'})")
        
        # Tags in recombined but not in original
        extra_tags = recombined_tags - original_tags
        if extra_tags:
            for tag in extra_tags:
                elem = recombined_dicom[tag]
                data_differences.append(f"Extra tag: {elem.tag} ({elem.name if hasattr(elem, 'name') else 'Unknown'})")
        
        # Tags in both - check for value differences
        common_tags = original_tags.intersection(recombined_tags)
        for tag in common_tags:
            orig_elem = original_dicom[tag]
            recom_elem = recombined_dicom[tag]
            
            # Skip binary data comparison for simplicity
            if isinstance(orig_elem.value, bytes) or isinstance(recom_elem.value, bytes):
                continue
            
            # For arrays, convert to string representation for comparison
            orig_value = str(orig_elem.value)
            recom_value = str(recom_elem.value)
            
            # Compare string representation of values
            if orig_value != recom_value:
                data_differences.append(f"Value mismatch for {orig_elem.tag} ({orig_elem.name if hasattr(orig_elem, 'name') else 'Unknown'}): "
                                       f"Original: {orig_value}, Recombined: {recom_value}")
        
        # Check pixel data
        pixel_data_identical = False
        if 'PixelData' in original_dicom and 'PixelData' in recombined_dicom:
            original_pixel = original_dicom.PixelData
            recombined_pixel = recombined_dicom.PixelData
            pixel_data_identical = original_pixel == recombined_pixel
        
        # Summary
        total_differences = len(meta_differences) + len(data_differences)
        
        logger.info(f"\nDICOM Comparison Results:")
        logger.info(f"Original file: {original_dicom_path}")
        logger.info(f"Recombined file: {recombined_dicom_path}")
        logger.info(f"Original size: {original_size:,} bytes")
        logger.info(f"Recombined size: {recombined_size:,} bytes")
        logger.info(f"Size difference: {recombined_size - original_size:+,} bytes ({(recombined_size/original_size - 1)*100:.2f}%)")
        logger.info(f"Total tags in original: {len(original_tags) + len(original_meta_tags)}")
        logger.info(f"Total tags in recombined: {len(recombined_tags) + len(recombined_meta_tags)}")
        logger.info(f"Missing tags in recombined: {len(missing_tags) + len(missing_meta_tags)}")
        logger.info(f"Extra tags in recombined: {len(extra_tags)}")
        logger.info(f"Value differences in common tags: {total_differences - len(missing_tags) - len(extra_tags) - len(missing_meta_tags)}")
        logger.info(f"Pixel data identical: {pixel_data_identical}")
        
        # Log specific differences if any
        if meta_differences:
            logger.info("\nFile meta differences:")
            for diff in meta_differences:
                logger.info(f"  - {diff}")
        
        if data_differences:
            logger.info("\nData element differences:")
            for diff in data_differences[:20]:  # Limit to 20 to avoid overwhelming output
                logger.info(f"  - {diff}")
            
            if len(data_differences) > 20:
                logger.info(f"  ... and {len(data_differences) - 20} more differences")
        
        # Create comparison result
        comparison_result = {
            'original_file': str(original_dicom_path),
            'recombined_file': str(recombined_dicom_path),
            'original_size': original_size,
            'recombined_size': recombined_size,
            'missing_tags': len(missing_tags) + len(missing_meta_tags),
            'extra_tags': len(extra_tags),
            'value_differences': total_differences - len(missing_tags) - len(extra_tags) - len(missing_meta_tags),
            'pixel_data_identical': pixel_data_identical,
            'meta_differences': meta_differences,
            'data_differences': data_differences,
            'is_identical': total_differences == 0 and pixel_data_identical
        }
        
        return comparison_result
    
    except Exception as e:
        logger.error(f"Error comparing DICOM files: {e}", exc_info=True)
        return {
            'error': str(e),
            'is_identical': False
        }

def analyze_dicom_tag_sizes(dicom_path):
    """
    Analyze the size contribution of each DICOM tag to help identify 
    which elements might be missing or differently encoded in recombined files.
    
    Args:
        dicom_path: Path to the DICOM file to analyze
    
    Returns:
        Dictionary with tag size information
    """
    try:
        # Use dcmdump to get detailed information about each element
        import tempfile
        import subprocess
        from collections import defaultdict
        
        # First read with pydicom to get basic info
        dicom_dataset = pydicom.dcmread(str(dicom_path), force=True)
        
        # Analyze the file manually by creating a binary dump and parsing it
        with open(dicom_path, 'rb') as f:
            file_content = f.read()
        
        file_size = len(file_content)
        
        # Group tags by category
        tag_categories = {
            'Standard': [],
            'Private': [],
            'Sequences': [],
            'Binary': [],
            'Pixel Data': []
        }
        
        # Track all elements and their sizes
        tag_sizes = {}
        
        # Analyze using pydicom
        for elem in dicom_dataset.file_meta:
            tag_key = f"{elem.tag} ({elem.name if hasattr(elem, 'name') else 'Unknown'})"
            element_size = len(elem.to_bytes() if hasattr(elem, 'to_bytes') else b'')
            tag_sizes[tag_key] = element_size
            
            if elem.tag.is_private:
                tag_categories['Private'].append((tag_key, element_size))
            else:
                tag_categories['Standard'].append((tag_key, element_size))
        
        for elem in dicom_dataset:
            tag_key = f"{elem.tag} ({elem.name if hasattr(elem, 'name') else 'Unknown'})"
            element_size = len(elem.to_bytes() if hasattr(elem, 'to_bytes') else b'')
            tag_sizes[tag_key] = element_size
            
            if elem.VR == 'SQ':
                tag_categories['Sequences'].append((tag_key, element_size))
            elif isinstance(elem.value, bytes) and elem.tag != pydicom.tag.Tag('PixelData'):
                tag_categories['Binary'].append((tag_key, element_size))
            elif elem.tag == pydicom.tag.Tag('PixelData'):
                tag_categories['Pixel Data'].append((tag_key, element_size))
            elif elem.tag.is_private:
                tag_categories['Private'].append((tag_key, element_size))
            else:
                tag_categories['Standard'].append((tag_key, element_size))
        
        # Sort tags by size in each category
        for category in tag_categories:
            tag_categories[category].sort(key=lambda x: x[1], reverse=True)
        
        # Calculate total size for each category
        category_sizes = {category: sum(size for _, size in tags) for category, tags in tag_categories.items()}
        
        # Calculate approximate overhead (headers, file structure, etc.)
        known_size = sum(category_sizes.values())
        overhead = file_size - known_size
        
        # Prepare report
        logger.info(f"\nDICOM Tag Size Analysis for {os.path.basename(dicom_path)}")
        logger.info(f"Total file size: {file_size:,} bytes")
        logger.info(f"Size breakdown by category:")
        for category, size in sorted(category_sizes.items(), key=lambda x: x[1], reverse=True):
            percentage = (size / file_size) * 100
            logger.info(f"  - {category}: {size:,} bytes ({percentage:.1f}%)")
        
        estimated_overhead_percentage = (overhead / file_size) * 100
        logger.info(f"  - Estimated overhead: {overhead:,} bytes ({estimated_overhead_percentage:.1f}%)")
        
        # List top 10 largest elements in each category
        for category, tags in tag_categories.items():
            if tags:
                logger.info(f"\nLargest {category} elements:")
                for i, (tag_key, size) in enumerate(tags[:10]):  # Show top 10
                    percentage = (size / file_size) * 100
                    logger.info(f"  {i+1}. {tag_key}: {size:,} bytes ({percentage:.1f}%)")
                
                if len(tags) > 10:
                    logger.info(f"  ... and {len(tags) - 10} more elements")
        
        return {
            'file_path': dicom_path,
            'file_size': file_size,
            'category_sizes': category_sizes,
            'overhead': overhead,
            'tag_sizes': tag_sizes,
            'tag_categories': tag_categories
        }
    
    except Exception as e:
        logger.error(f"Error analyzing tag sizes in {dicom_path}: {e}", exc_info=True)
        return {'error': str(e)}

# Example usage
if __name__ == "__main__":
    # Example paths - replace with your actual paths
    dicom_folder = "D:/ARAMIS_radon/radonData/dcm/ARAMIS/MR/2025/5/15/AZbT-LaMX-4vjb/AZbT-LaMX-4vjb.000"
    output_folder = "D:/ARAMIS_radon/radonData/dcm/ARAMIS/MR/2025/5/15/AZbT-LaMX-4vjb/AZbT-LaMX-4vjb.000/output"
    
    # Analyze a single DICOM file to see compression details
    sample_dicom = Path(dicom_folder) / "00294.dcm"
    if sample_dicom.exists():
        logger.info("Analyzing sample DICOM file...")
        compression_info = analyze_dicom_compression(sample_dicom)
        for key, value in compression_info.items():
            logger.info(f"{key}: {value}")
        
        # Analyze tag sizes
        logger.info("\nAnalyzing DICOM tag sizes...")
        tag_size_info = analyze_dicom_tag_sizes(sample_dicom)
    
    # Extract all DICOM files in the folder
    extract_dicom_components(dicom_folder, output_folder)
    
    # Example of loading pixel data back
    metadata_file = os.path.join(output_folder, "00294_metadata.json")
    pixel_file = os.path.join(output_folder, "00294_pixels.raw")
    output_dcm = os.path.join(output_folder, "00294_recombined.dcm")
    
    if os.path.exists(metadata_file) and os.path.exists(pixel_file):
        logger.info("Recombining sample DICOM file...")
        result = recombine_components(metadata_file, pixel_file, output_dcm)
        
        # Verify recombined file
        if os.path.exists(output_dcm):
            logger.info("Analyzing recombined DICOM file...")
            recombined_info = analyze_dicom_compression(output_dcm)
            logger.info("Comparison between original and recombined:")
            for key in ['compression_type', 'compressed_pixel_size', 'compression_ratio']:
                if key in compression_info and key in recombined_info:
                    logger.info(f"{key}: {compression_info[key]} (original) vs {recombined_info[key]} (recombined)")
            
            # Analyze recombined tag sizes
            if os.path.exists(output_dcm):
                logger.info("\nAnalyzing recombined DICOM tag sizes...")
                recombined_tag_size_info = analyze_dicom_tag_sizes(output_dcm)
            
            # Compare original and recombined DICOM files in detail
            logger.info("\nPerforming detailed tag comparison...")
            comparison_result = compare_dicom_files(sample_dicom, output_dcm)
            
            # Check if the files are identical
            if comparison_result.get('is_identical', False):
                logger.info("✅ The original and recombined DICOM files are identical!")
            else:
                logger.info("❌ The original and recombined DICOM files have differences.")
    else:
        logger.warning(f"Could not find metadata file {metadata_file} or pixel file {pixel_file}")