import json
import os
import argparse

def extract_instance_metadata(source_file, instance_number, output_dir=None):
    """
    Extract metadata for a specific DICOM instance from a larger JSON file
    
    Args:
        source_file: Path to the source JSON file containing multiple instances
        instance_number: Instance number to extract (e.g., "00294")
        output_dir: Optional output directory
    
    Returns:
        Path to the output metadata file
    """
    # Load the source JSON
    with open(source_file, 'r') as f:
        source_data = json.load(f)
    
    # Check if the requested instance exists
    if instance_number not in source_data.get('ds_jn_instances', {}):
        print(f"Instance {instance_number} not found in the source file.")
        return None
    
    # Create the output metadata structure
    metadata = {}
    
    # Add file metadata information
    instance_info = None
    for series in source_data.get("pixelDataOffsets", {}).get("series", {}).values():
        for instance in series.get("instances", []):
            if instance.get("instance_number") == instance_number:
                instance_info = instance
                break
        if instance_info:
            break
    
    if instance_info:
        # Add compression info
        metadata["CompressionInfo"] = {
            "TransferSyntaxUID": instance_info["offset_info"]["transfer_syntax_uid"],
            "is_compressed": instance_info["offset_info"]["transfer_syntax_uid"] not in [
                "1.2.840.10008.1.2", "1.2.840.10008.1.2.1", "1.2.840.10008.1.2.2"
            ],
            "compression_type": "JPEG 2000 Lossless" if instance_info["offset_info"]["transfer_syntax_uid"] == "1.2.840.10008.1.2.4.90" else "Unknown"
        }
        
        # Add encoding info (assuming little endian for JPEG2000)
        metadata["EncodingInfo"] = {
            "is_little_endian": True,
            "is_implicit_VR": False,
            "has_preamble": True
        }
        
        # Add file info
        metadata["FileInfo"] = {
            "file_size": instance_info["file_info"]["filesize"],
            "SOP_class_uid": "1.2.840.10008.5.1.4.1.1.4",  # MR Image Storage
            "SOP_instance_uid": instance_info["SOPInstanceUID"]
        }
    
    # Create file meta info section
    metadata["FileMetaInfo"] = {
        "MediaStorageSOPClassUID": {
            "tag": [2, 3],
            "VR": "UI",
            "value": "1.2.840.10008.5.1.4.1.1.4"
        },
        "MediaStorageSOPInstanceUID": {
            "tag": [2, 16],
            "VR": "UI",
            "value": instance_info["SOPInstanceUID"] if instance_info else ""
        },
        "TransferSyntaxUID": {
            "tag": [2, 16],
            "VR": "UI",
            "value": instance_info["offset_info"]["transfer_syntax_uid"] if instance_info else ""
        }
    }
    
    # Add all data elements first from ds_jn (common data)
    metadata["DataElements"] = {}
    
    # Add common tags from ds_jn
    for tag, value in source_data.get("ds_jn", {}).items():
        if tag.startswith("00") or tag.startswith("7F"):  # Only process valid DICOM tags
            metadata["DataElements"][tag] = {
                "tag": [int(tag[0:4], 16), int(tag[4:8], 16)],
                "VR": value.get("vr", "UN"),
                "value": value.get("Value", None)
            }
    
    # Override with instance-specific tags from ds_jn_instances
    for tag, value in source_data.get("ds_jn_instances", {}).get(instance_number, {}).items():
        metadata["DataElements"][tag] = {
            "tag": [int(tag[0:4], 16), int(tag[4:8], 16)],
            "VR": value.get("vr", "UN"),
            "value": value.get("Value", None)
        }
    
    # Handle pixel data specially
    metadata["DataElements"]["7FE00010"] = {
        "tag": [0x7FE0, 0x0010],
        "VR": "OW",
        "value": "BINARY_DATA",
        "binary_length": instance_info["file_info"]["filesize"] - instance_info["offset_info"]["pixel_data_offset"] if instance_info else 0
    }
    
    # Add PixelDataInfo
    metadata["PixelDataInfo"] = {
        "offset": instance_info["offset_info"]["pixel_data_offset"] if instance_info else 0,
        "first_16_bytes_hex": instance_info["offset_info"]["first_16_bytes_hex"] if instance_info else "",
        "is_compressed": instance_info["offset_info"]["transfer_syntax_uid"] not in [
            "1.2.840.10008.1.2", "1.2.840.10008.1.2.1", "1.2.840.10008.1.2.2"
        ] if instance_info else False
    }
    
    # Generate the output filename
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
        output_file = os.path.join(output_dir, f"{instance_number}_metadata.json")
    else:
        output_file = f"{instance_number}_metadata.json"
    
    # Write the output file
    with open(output_file, 'w') as f:
        json.dump(metadata, f, indent=2)
    
    return output_file

def main():
    parser = argparse.ArgumentParser(description='Extract DICOM instance metadata from a source JSON file.')
    parser.add_argument('source_file', help='Source JSON file containing multiple instances')
    parser.add_argument('instance_number', help='Instance number to extract (e.g., "00294")')
    parser.add_argument('--output-dir', '-o', help='Output directory for the extracted metadata')
    parser.add_argument('--batch', '-b', action='store_true', help='Extract all instances')
    
    args = parser.parse_args()
    
    # Load the source file to get all instances for batch mode
    if args.batch:
        with open(args.source_file, 'r') as f:
            source_data = json.load(f)
        
        instances = source_data.get('ds_jn_instances', {}).keys()
        print(f"Extracting {len(instances)} instances...")
        
        for instance_number in instances:
            output_file = extract_instance_metadata(args.source_file, instance_number, args.output_dir)
            if output_file:
                print(f"Extracted {instance_number} to {output_file}")
    else:
        output_file = extract_instance_metadata(args.source_file, args.instance_number, args.output_dir)
        if output_file:
            print(f"Metadata extracted to {output_file}")

if __name__ == "__main__":
    main()