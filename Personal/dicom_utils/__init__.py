"""
DICOM Utilities Package 

A comprehensive set of tools for extracting, modifying, 
and recombining DICOM images with full metadata preservation.
"""

from .extractor import extract_dicom_components, extract_and_preserve_sequences, extract_icon_data
from .recombiner import recombine_components, restore_sequence_data
from .analyzer import analyze_dicom_compression, compare_dicom_files, analyze_dicom_tag_sizes

__version__ = "1.0.0" 