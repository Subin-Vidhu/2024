#!/usr/bin/env python3

import os

def check_file_format(file_path):
    """Check if a file is actually gzip compressed or just a regular NIfTI file."""
    
    if not os.path.exists(file_path):
        print(f"File does not exist: {file_path}")
        return
    
    with open(file_path, 'rb') as f:
        header = f.read(10)
        print(f'File: {file_path}')
        print(f'Size: {os.path.getsize(file_path)} bytes')
        print('First 10 bytes (hex):', ' '.join(f'{b:02x}' for b in header))
        print('First 10 bytes (as chars):', ''.join(chr(b) if 32 <= b <= 126 else '.' for b in header))
        
        # Check if it's gzip (starts with 1f 8b)
        if header[:2] == b'\x1f\x8b':
            print('✓ File appears to be gzip compressed')
            return 'gzip'
        else:
            print('✗ File is NOT gzip compressed')
            # Check if it's a regular NIfTI file
            f.seek(344)  # NIfTI magic number location
            magic = f.read(4)
            print(f'Magic bytes at position 344: {magic}')
            if magic in [b'ni1\0', b'n+1\0']:
                print('✓ File appears to be an uncompressed NIfTI file')
                return 'nifti'
            else:
                print('? File format unknown')
                return 'unknown'

if __name__ == "__main__":
    file_path = r'c:\Users\Subin-PC\Downloads\Telegram Desktop\OneDrive_1_10-8-2025\N-072\mask.nii.gz'
    result = check_file_format(file_path)
    
    print(f"\nResult: {result}")
    
    if result == 'nifti':
        print("\nSOLUTION:")
        print("The file has a .nii.gz extension but is actually an uncompressed NIfTI file.")
        print("You can either:")
        print("1. Rename the file to remove the .gz extension:")
        print(f"   rename '{file_path}' to '{file_path[:-3]}'")
        print("2. Or modify your code to handle this case")
