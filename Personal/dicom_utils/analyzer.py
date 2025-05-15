"""
Functions for analyzing DICOM files
"""

import os
import pydicom
from collections import defaultdict
from .constants import TRANSFER_SYNTAX_NAMES, UNCOMPRESSED_TRANSFER_SYNTAXES
from .logger import logger

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
        # Use pydicom to read the file
        dicom_dataset = pydicom.dcmread(str(dicom_path), force=True)
        
        # Analyze the file manually for size information
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