"""
Functions for recombining extracted DICOM components
"""

import os
import json
import pickle
import pydicom
import datetime
from pydicom.dataset import FileDataset
import pydicom.sequence
import pydicom.uid
from .logger import logger
from .utils import format_numeric_value

def restore_sequence_data(dataset, sequence_data):
    """
    Restore sequence data to a DICOM dataset
    
    Args:
        dataset: The DICOM dataset to add sequence data to
        sequence_data: Dictionary containing sequence data
    """
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
        pixel_file: Path to raw pixel data file or pickle file (.raw or .p)
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

    # Load raw pixel data - check for file extension to determine format
    pixel_format = metadata.get('CompressionInfo', {}).get('PixelFormat', 'raw')
    
    # Determine if the file is a pickle file
    is_pickle = pixel_file.endswith('.p') or pixel_format == 'pickle'
    
    if is_pickle:
        # Load pixel data from pickle file
        with open(pixel_file, 'rb') as f:
            pixel_info = pickle.load(f)
            pixel_data = pixel_info['data']  # Get the actual binary data
    else:
        # Load raw binary data directly
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