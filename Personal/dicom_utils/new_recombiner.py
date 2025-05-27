"""
Updated functions for recombining extracted DICOM components
based on the new JSON metadata structure
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
                    if isinstance(elem_data, dict) and 'vr' in elem_data and 'Value' in elem_data:
                        # This is the new format for sequence items
                        elem_vr = elem_data['vr']
                        elem_value = elem_data['Value']
                        
                        # Create tag from the element keyword
                        elem_tag = pydicom.tag.Tag(int(elem_keyword[0:4], 16), int(elem_keyword[4:8], 16))
                        
                        # Add the element to the dataset
                        ds.add_new(elem_tag, elem_vr, elem_value)
                    elif isinstance(elem_data, dict) and isinstance(next(iter(elem_data.values()), None), dict):
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
                    file_meta.add(pydicom.DataElement(tag, vr, value))
            except Exception as e:
                logger.warning(f"Error restoring file meta element {key}: {e}")
    
    # Make sure these critical elements are set
    transfer_syntax_uid = metadata.get('CompressionInfo', {}).get('TransferSyntaxUID', '1.2.840.10008.1.2')
    file_meta.TransferSyntaxUID = transfer_syntax_uid
    
    if 'MediaStorageSOPClassUID' not in file_meta:
        file_meta.MediaStorageSOPClassUID = file_meta_info.get('MediaStorageSOPClassUID', {}).get('value', pydicom.uid.MRImageStorage)
    
    if 'MediaStorageSOPInstanceUID' not in file_meta:
        file_meta.MediaStorageSOPInstanceUID = file_meta_info.get('MediaStorageSOPInstanceUID', {}).get('value', pydicom.uid.generate_uid())
    
    if 'ImplementationClassUID' not in file_meta:
        file_meta.ImplementationClassUID = pydicom.uid.PYDICOM_IMPLEMENTATION_UID
    
    # Load preamble if present
    preamble = None
    encoding_info = metadata.get('EncodingInfo', {})
    if encoding_info.get('has_preamble', False):
        preamble = b"\0" * 128
    else:
        preamble = b"\0" * 128

    # Create dataset with proper file meta and preamble
    ds = FileDataset(output_dcm, {}, file_meta=file_meta, preamble=preamble)

    # Restore encoding information
    ds.is_little_endian = encoding_info.get('is_little_endian', True)
    ds.is_implicit_VR = encoding_info.get('is_implicit_VR', True)
    
    # Process all data elements
    data_elements = metadata.get('DataElements', {})
    
    # First, restore non-binary data elements
    for tag_str, elem_info in data_elements.items():
        try:
            tag = pydicom.tag.Tag(elem_info['tag'][0], elem_info['tag'][1])
            vr = elem_info['VR']
            value = elem_info['value']
            
            # Skip pixel data as it will be handled separately
            if tag_str == '7FE00010':
                continue
            
            # Skip binary data elements with placeholder
            if value == "BINARY_DATA":
                continue
            
            # Create and set the data element
            if vr == 'SQ':
                # Restore sequences - sequences are stored with their content
                if isinstance(value, list) and all(isinstance(item, dict) for item in value):
                    # Create sequence
                    seq = pydicom.sequence.Sequence()
                    
                    # Add each sequence item
                    for item_dict in value:
                        ds_item = pydicom.dataset.Dataset()
                        
                        # Add elements to the item
                        for elem_tag, elem_data in item_dict.items():
                            if isinstance(elem_data, dict) and 'vr' in elem_data and 'Value' in elem_data:
                                # Create tag from element tag string
                                item_tag = pydicom.tag.Tag(int(elem_tag[0:4], 16), int(elem_tag[4:8], 16))
                                item_vr = elem_data['vr']
                                item_value = elem_data['Value']
                                
                                # Add element to item dataset
                                ds_item.add_new(item_tag, item_vr, item_value)
                        
                        # Add item to sequence
                        seq.append(ds_item)
                    
                    # Add sequence to main dataset
                    ds.add_new(tag, vr, seq)
                else:
                    # Empty sequence
                    ds.add_new(tag, vr, [])
            elif vr == 'DS' or vr == 'FL' or vr == 'FD':
                # Handle decimal strings and float values
                if isinstance(value, list):
                    # Array of values - convert each element if needed
                    if all(isinstance(v, (int, float)) for v in value):
                        ds.add_new(tag, vr, value)
                    else:
                        # Convert strings to appropriate numeric types
                        processed_values = []
                        for v in value:
                            if isinstance(v, str):
                                try:
                                    processed_values.append(float(v))
                                except:
                                    processed_values.append(v)
                            else:
                                processed_values.append(v)
                        ds.add_new(tag, vr, processed_values)
                elif value is None:
                    # Empty value
                    ds.add_new(tag, vr, '')
                else:
                    # Single value
                    ds.add_new(tag, vr, value)
            elif vr in ['IS', 'SS', 'US', 'SL', 'UL']:
                # Handle integer types
                if isinstance(value, list):
                    # Array of values
                    if all(isinstance(v, int) for v in value):
                        ds.add_new(tag, vr, value)
                    else:
                        # Convert strings to integers
                        processed_values = []
                        for v in value:
                            if isinstance(v, str):
                                try:
                                    processed_values.append(int(v))
                                except:
                                    processed_values.append(v)
                            else:
                                processed_values.append(v)
                        ds.add_new(tag, vr, processed_values)
                elif value is None:
                    # Empty value
                    ds.add_new(tag, vr, '')
                else:
                    # Single value
                    ds.add_new(tag, vr, value)
            else:
                # Handle all other VR types
                ds.add_new(tag, vr, value)
        except Exception as e:
            logger.warning(f"Error restoring element {tag_str}: {e}")
    
    # Load pixel data
    pixel_info = metadata.get('PixelDataInfo', {})
    is_compressed = pixel_info.get('is_compressed', False)
    pixel_format = '.p' if pixel_file.endswith('.p') else '.raw'
    
    # Determine if the file is a pickle file
    is_pickle = pixel_file.endswith('.p')
    
    if is_pickle:
        # Load pixel data from pickle file
        with open(pixel_file, 'rb') as f:
            pixel_data = pickle.load(f)
            if isinstance(pixel_data, dict) and 'data' in pixel_data:
                pixel_data = pixel_data['data']
    else:
        # Load raw binary data directly
        with open(pixel_file, 'rb') as f:
            pixel_data = f.read()
    
    # Set pixel data
    pixel_tag = pydicom.tag.Tag('PixelData')
    if is_compressed:
        ds.add_new(pixel_tag, 'OB', pixel_data)  # OB for compressed pixel data
    else:
        ds.add_new(pixel_tag, 'OW', pixel_data)  # OW for uncompressed pixel data

    # Save to DICOM file (explicitly specify write_like_original=True to maintain format)
    ds.save_as(output_dcm, write_like_original=True)
    
    # Output size comparison
    new_size = os.path.getsize(output_dcm)
    original_size = metadata.get('FileInfo', {}).get('file_size', 0)
    
    logger.info(f"Saved recombined DICOM to: {output_dcm}")
    logger.info(f"Original file size: {original_size:,} bytes")
    logger.info(f"Reconstructed file size: {new_size:,} bytes")
    logger.info(f"Size difference: {new_size - original_size:+,} bytes ({(new_size/original_size - 1)*100:.2f}%)")
    
    return {
        'file_path': output_dcm,
        'original_size': original_size,
        'new_size': new_size,
        'is_compressed': is_compressed,
        'compression_type': metadata.get('CompressionInfo', {}).get('compression_type', 'Unknown')
    }