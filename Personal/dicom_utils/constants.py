"""
Constants for DICOM processing
"""

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