import os
import pydicom
import pickle
import json
from pathlib import Path
import logging

# Constants
PIXEL_FORMAT_RAW = 'raw'
PIXEL_FORMAT_PICKLE = 'pickle'
UNCOMPRESSED_TRANSFER_SYNTAXES = {
    '1.2.840.10008.1.2',  # Implicit VR Little Endian
    '1.2.840.10008.1.2.1',  # Explicit VR Little Endian
    '1.2.840.10008.1.2.2',  # Explicit VR Big Endian
}
TRANSFER_SYNTAX_NAMES = {
    '1.2.840.10008.1.2': 'Implicit VR Little Endian',
    '1.2.840.10008.1.2.1': 'Explicit VR Little Endian',
    '1.2.840.10008.1.2.2': 'Explicit VR Big Endian',
    '1.2.840.10008.1.2.4.50': 'JPEG Baseline (Process 1)',
    '1.2.840.10008.1.2.4.70': 'JPEG Lossless, Nonhierarchical (Process 14)',
    # Add more as needed
}

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

def extract_pixel_data_info(dicom_file, output_folder, pixel_format=PIXEL_FORMAT_PICKLE):
    """
    Extract only pixel data information from a DICOM file.

    Args:
        dicom_file: Path to a DICOM file.
        output_folder: Directory to save the extracted pixel data.
        pixel_format: Format to save the pixel data ('raw' or 'pickle').
    """
    os.makedirs(output_folder, exist_ok=True)

    if pixel_format not in [PIXEL_FORMAT_RAW, PIXEL_FORMAT_PICKLE]:
        logger.warning(f"Invalid pixel format: {pixel_format}. Defaulting to 'raw'.")
        pixel_format = PIXEL_FORMAT_RAW

    dicom_path = Path(dicom_file)
    base_filename = dicom_path.stem

    try:
        dicom = pydicom.dcmread(str(dicom_path), force=True, stop_before_pixels=False)

        # Extract essential pixel info
        rows = dicom.Rows if 'Rows' in dicom else 0
        columns = dicom.Columns if 'Columns' in dicom else 0
        samples_per_pixel = dicom.SamplesPerPixel if 'SamplesPerPixel' in dicom else 1
        bits_allocated = dicom.BitsAllocated if 'BitsAllocated' in dicom else 0
        number_of_frames = getattr(dicom, 'NumberOfFrames', 1) if 'NumberOfFrames' in dicom else 1

        # Transfer Syntax
        transfer_syntax_uid = str(dicom.file_meta.TransferSyntaxUID) if hasattr(dicom.file_meta, 'TransferSyntaxUID') else '1.2.840.10008.1.2'
        is_compressed = transfer_syntax_uid not in UNCOMPRESSED_TRANSFER_SYNTAXES
        compression_type = TRANSFER_SYNTAX_NAMES.get(transfer_syntax_uid, f"Unknown ({transfer_syntax_uid})")

        # Handle PixelData
        if 'PixelData' in dicom:
            pixel_data = dicom.PixelData
            compressed_size = len(pixel_data)
            uncompressed_bytes_per_pixel = bits_allocated // 8
            theoretical_uncompressed_size = rows * columns * samples_per_pixel * uncompressed_bytes_per_pixel * number_of_frames
            compression_ratio = theoretical_uncompressed_size / compressed_size if is_compressed and compressed_size > 0 else 1.0

            # Save pixel data
            if pixel_format == PIXEL_FORMAT_RAW:
                pixel_path = os.path.join(output_folder, f"{base_filename}_pixels.raw")
                with open(pixel_path, 'wb') as f:
                    f.write(pixel_data)
            else:
                pixel_info = {
                    'data': pixel_data,
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

            logger.info(f"Pixel data extracted for {dicom_path.name}")
            logger.info(f"  - Format: {pixel_format}")
            logger.info(f"  - Compression: {compression_type}")
            logger.info(f"  - Compressed size: {compressed_size:,} bytes")
            logger.info(f"  - Estimated uncompressed size: {theoretical_uncompressed_size:,} bytes")
            if is_compressed:
                logger.info(f"  - Compression ratio: {compression_ratio:.2f}x")
            logger.info(f"  - Saved to: {pixel_path}")
        else:
            logger.warning(f"No pixel data found in {dicom_path.name}")

    except Exception as e:
        logger.error(f"Error reading pixel data from {dicom_file}: {e}", exc_info=True)

if __name__ == "__main__":
    # Example usage
    dicom_file = "D:/ARAMIS_radon/radonData/dcm/ARAMIS/MR/2025/5/17/AZbc-Bas0-dXr-/AZbc-Bas0-dXr-.000/00294.dcm"
    output_folder = "D:/ARAMIS_radon/radonData/dcm/ARAMIS/MR/2025/5/17/AZbc-Bas0-dXr-/AZbc-Bas0-dXr-.000/output_pixel_data_only"
    os.makedirs(output_folder, exist_ok=True)
    extract_pixel_data_info(dicom_file, output_folder, pixel_format=PIXEL_FORMAT_PICKLE)
