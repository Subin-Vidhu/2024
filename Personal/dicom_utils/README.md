# DICOM Utilities

A comprehensive set of tools for extracting, analyzing, and recombining DICOM medical images with full metadata preservation.

## Features

- **Extract DICOM Components**: Separate DICOM files into metadata and pixel data components, preserving all original information
- **Preserve Complex Data**: Special handling for binary data, sequences, and private tags
- **Exact Format Preservation**: Maintain original numeric format (70 vs 70.0) and scientific notation
- **Recombine Components**: Rebuild exact DICOM files from extracted components 
- **Analysis Tools**: Compare DICOM files and analyze tag size contributions
- **Flexible Extraction Modes**: Choose how much data to extract based on your needs
- **Multiple Pixel Formats**: Save pixel data in raw binary (.raw) or Python pickle (.p) formats

## Extraction Modes

The package supports three extraction modes to give you flexibility when working with DICOM files:

1. **Minimal Mode**: Extracts only the essential components
   - Metadata (in JSON format)
   - Pixel data (raw binary)
   - Skips private tags and most binary data
   - Results in the smallest output size and fastest processing

2. **Standard Mode**: A balanced approach that includes
   - Everything in minimal mode
   - Essential binary data (like image orientation, position, spacing)
   - Data needed for meaningful medical interpretation
   - Skips non-essential binary data and some private tags

3. **Full Mode**: Comprehensive extraction of all components
   - All metadata, pixel data, and binary data
   - All private tags
   - Raw file meta information
   - DICOM preamble
   - Icon image data
   - Results in the largest output size but preserves everything

## Pixel Data Formats

You can choose how to save the extracted pixel data:

1. **Raw Binary (.raw)**: Default format
   - Simple binary data exactly as stored in the DICOM file
   - No additional metadata or structure
   - Maximum compatibility with any language or tool
   - Requires size and format information from the metadata to interpret

2. **Python Pickle (.p)**: Python-specific format
   - Preserves exact data types and additional metadata
   - Stores image dimensions and DICOM properties with the data
   - Easier to load directly in Python scripts
   - Requires Python's pickle module to read

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/dicom-utils.git

# Navigate to the directory
cd dicom-utils

# Install dependencies
pip install -r requirements.txt
```

## Requirements

- Python 3.7+
- pydicom
- numpy

## Usage

### As a Module

```python
from dicom_utils import (
    extract_dicom_components, 
    recombine_components,
    EXTRACTION_MODE_MINIMAL,
    EXTRACTION_MODE_STANDARD,
    EXTRACTION_MODE_FULL,
    PIXEL_FORMAT_RAW,
    PIXEL_FORMAT_PICKLE
)

# Extract DICOM components with standard mode (default is EXTRACTION_MODE_FULL)
# and save pixel data in raw format (default)
extract_dicom_components(
    dicom_folder="path/to/dicom/files", 
    output_folder="path/to/output",
    extraction_mode=EXTRACTION_MODE_STANDARD,
    pixel_format=PIXEL_FORMAT_RAW
)

# For minimal extraction with pickle format for pixel data
extract_dicom_components(
    dicom_folder="path/to/dicom/files", 
    output_folder="path/to/output/minimal",
    extraction_mode=EXTRACTION_MODE_MINIMAL,
    pixel_format=PIXEL_FORMAT_PICKLE
)

# Recombine components into a new DICOM file
# The function automatically detects if the pixel file is raw or pickle format
recombine_components(
    metadata_file="path/to/metadata.json",
    pixel_file="path/to/pixels.raw",  # or "path/to/pixels.p" for pickle format
    output_dcm="path/to/output.dcm"
)
```

### Complete Example Script

Here's a complete example script that analyzes, extracts, recombines, and verifies DICOM files:

```python
import os
from pathlib import Path
from dicom_utils import (
    extract_dicom_components,
    recombine_components, 
    analyze_dicom_compression,
    compare_dicom_files,
    analyze_dicom_tag_sizes,
    EXTRACTION_MODE_STANDARD,
    PIXEL_FORMAT_PICKLE
)

# Define paths
dicom_folder = "/path/to/dicom/folder"
output_folder = "/path/to/output/folder"

# Analyze a sample DICOM file
sample_dicom = Path(dicom_folder) / "sample.dcm"
if sample_dicom.exists():
    print("Analyzing sample DICOM file...")
    compression_info = analyze_dicom_compression(sample_dicom)
    print(f"Transfer Syntax: {compression_info['compression_type']}")
    print(f"Compression Ratio: {compression_info['compression_ratio']:.2f}x")

# Extract all DICOM files in the folder using standard mode and pickle format
extract_dicom_components(
    dicom_folder, 
    output_folder, 
    extraction_mode=EXTRACTION_MODE_STANDARD, 
    pixel_format=PIXEL_FORMAT_PICKLE
)

# Recombine a specific file
metadata_file = os.path.join(output_folder, "sample_metadata.json")
pixel_file = os.path.join(output_folder, "sample_pixels.p")  # Note the .p extension
output_dcm = os.path.join(output_folder, "sample_recombined.dcm")

if os.path.exists(metadata_file) and os.path.exists(pixel_file):
    # Recombine the components
    recombine_components(metadata_file, pixel_file, output_dcm)
    
    # Compare original and recombined files
    comparison = compare_dicom_files(sample_dicom, output_dcm)
    if comparison['is_identical']:
        print("✅ Files are identical!")
    else:
        print(f"❌ Files have differences: {comparison['value_differences']} value mismatches")
```

### Command Line Interface

The package provides a command-line interface for common operations:

```bash
# Extract all DICOM files in a folder using standard extraction mode and raw format
python -m dicom_utils extract -i /path/to/dicom/files -o /path/to/output --mode standard --pixel-format raw

# Extract with minimal mode and pickle format
python -m dicom_utils extract -i /path/to/dicom/files -o /path/to/output --mode minimal --pixel-format pickle

# Extract with full mode
python -m dicom_utils extract -i /path/to/dicom/files -o /path/to/output --mode full

# Recombine a single file
python -m dicom_utils recombine -m /path/to/metadata.json -p /path/to/pixels.p -o /path/to/output.dcm

# Analyze a DICOM file
python -m dicom_utils analyze -i /path/to/dicom/file.dcm -o /path/to/comparison.dcm

# Process a folder (extract, recombine, and compare) with standard mode and pickle format
python -m dicom_utils process -i /path/to/dicom/files -o /path/to/output --mode standard --pixel-format pickle
```

### Real-world Example

For a real-world example, if you have DICOM files in `D:/dicom_data/patient1` and want to extract and recombine them:

```bash
# Create output directory
mkdir -p D:/dicom_data/processed

# Extract all DICOM files with standard mode and pickle format
python -m dicom_utils extract -i D:/dicom_data/patient1 -o D:/dicom_data/processed --mode standard --pixel-format pickle

# Process specific file for recombination
python -m dicom_utils recombine \
    -m D:/dicom_data/processed/CT000123_metadata.json \
    -p D:/dicom_data/processed/CT000123_pixels.p \
    -o D:/dicom_data/processed/CT000123_recombined.dcm

# Compare original and recombined files
python -m dicom_utils analyze \
    -i D:/dicom_data/patient1/CT000123.dcm \
    -o D:/dicom_data/processed/CT000123_recombined.dcm
```

## Project Structure

```
dicom_utils/
├── __init__.py         # Package initialization and exports
├── analyzer.py         # DICOM analysis functions
├── constants.py        # Constants and configuration
├── extractor.py        # Component extraction functions
├── logger.py           # Logging utilities
├── main.py             # Command-line interface
├── recombiner.py       # Component recombination
└── utils.py            # Helper utilities
```

## How It Works

This package handles the full lifecycle of DICOM processing:

1. **Extraction**: The original DICOM file is decomposed into:
   - Structured metadata (JSON)
   - Raw pixel data (binary or pickle format)
   - Binary data elements (stored separately)
   - Sequence elements (specially encoded)

2. **Recombination**: Components are reassembled into a valid DICOM file:
   - Metadata is parsed and recreated with exact VRs
   - Binary data is inserted
   - Sequences are rebuilt
   - Numeric values preserve exact formatting
   - Proper transfer syntax is maintained

3. **Analysis**: Tools to verify preservation:
   - Compare original and recombined files
   - Analyze tag size contributions 
   - Validate pixel data integrity

## License

MIT License 