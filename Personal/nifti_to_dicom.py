# -*- coding: utf-8 -*-
"""
Created on Fri Dec 27 09:59:10 2024

@author: Subin-PC
"""
# now works in both itksnap and radiant - there is some flip issues though
import nibabel as nib
import numpy as np
import pydicom
from pydicom.dataset import FileDataset, FileMetaDataset
from pydicom.uid import generate_uid, ImplicitVRLittleEndian
from datetime import datetime
import os

def nifti_to_dicom_labels(nifti_path, output_dir):
    """
    Convert a NIfTI label map to DICOM series with correct orientation
    and ITK-SNAP compatibility.
    
    Parameters:
    nifti_path (str): Path to input NIfTI file
    output_dir (str): Directory to save output DICOM files
    """
    try:
        # Create output directory if it doesn't exist
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        # Load the NIfTI file
        print("Loading NIfTI file...")
        nifti_img = nib.load(nifti_path)
        nifti_data = nifti_img.get_fdata()
        
        # Fix orientation: flip the data array if needed
        nifti_data = np.flip(nifti_data, axis=1)  # Flip left-right
        
        # Convert to integers and scale to visible range
        unique_values = np.unique(nifti_data)
        print(f"Original unique values: {unique_values}")
        
        # Scale the values to be more visible (multiply by 1000)
        nifti_data = nifti_data * 1000
        nifti_data = np.clip(nifti_data, 0, 4095).astype(np.uint16)
        
        # Get orientation from affine
        affine = nifti_img.affine
        header = nifti_img.header
        
        # Extract spacing information
        pixel_spacing = header.get_zooms()[:2]
        slice_thickness = header.get_zooms()[2]
        
        # Generate minimal set of UIDs
        study_instance_uid = generate_uid()
        series_instance_uid = generate_uid()
        
        # Get current date and time
        dt = datetime.now()
        date_string = dt.strftime('%Y%m%d')
        time_string = dt.strftime('%H%M%S')
        
        print(f"Converting {nifti_data.shape[2]} slices...")
        
        for slice_idx in range(nifti_data.shape[2]):
            # Create minimal file meta information
            file_meta = FileMetaDataset()
            file_meta.MediaStorageSOPClassUID = '1.2.840.10008.5.1.4.1.1.2'
            file_meta.MediaStorageSOPInstanceUID = generate_uid()
            file_meta.TransferSyntaxUID = ImplicitVRLittleEndian
            
            # Create the FileDataset with minimal required tags
            ds = FileDataset(None, {}, file_meta=file_meta, preamble=b"\0" * 128)
            
            # Only include essential DICOM tags
            ds.SOPClassUID = file_meta.MediaStorageSOPClassUID
            ds.SOPInstanceUID = file_meta.MediaStorageSOPInstanceUID
            ds.StudyInstanceUID = study_instance_uid
            ds.SeriesInstanceUID = series_instance_uid
            ds.StudyDate = date_string
            ds.StudyTime = time_string
            ds.PatientName = "Anonymous"
            ds.PatientID = "123"
            ds.Modality = "CT"
            ds.SeriesNumber = 1
            ds.InstanceNumber = slice_idx + 1
            
            # Set standard orientation vectors for axial view
            ds.ImageOrientationPatient = [1, 0, 0, 0, 1, 0]
            ds.PixelSpacing = list(map(float, pixel_spacing))
            ds.SliceThickness = float(slice_thickness)
            ds.ImagePositionPatient = [0, 0, slice_idx * slice_thickness]
            
            # Image-specific attributes
            ds.SamplesPerPixel = 1
            ds.PhotometricInterpretation = "MONOCHROME2"
            ds.Rows = nifti_data.shape[0]
            ds.Columns = nifti_data.shape[1]
            ds.BitsAllocated = 16
            ds.BitsStored = 12
            ds.HighBit = 11
            ds.PixelRepresentation = 0
            
            # Window settings
            ds.WindowCenter = 2048
            ds.WindowWidth = 4096
            ds.RescaleIntercept = 0
            ds.RescaleSlope = 1
            
            # Set the pixel data for this slice
            slice_data = nifti_data[:, :, slice_idx].astype(np.uint16)
            ds.PixelData = slice_data.tobytes()
            
            # Save the DICOM file
            output_path = os.path.join(output_dir, f'slice_{slice_idx:04d}.dcm')
            ds.save_as(output_path)
            
            if (slice_idx + 1) % 10 == 0:
                print(f"Processed {slice_idx + 1}/{nifti_data.shape[2]} slices")
        
        print("Conversion completed successfully!")
        print(f"DICOM files saved in: {output_dir}")
        print("\nValue mapping:")
        for original_value in unique_values:
            print(f"Original value {original_value} -> Converted to {int(original_value * 1000)}")
        
    except Exception as e:
        print(f"Error during conversion: {str(e)}")
        raise

# Example usage
if __name__ == "__main__":
    nifti_file = "D:/__SHARED__/Radium_2/mask.nii"  # Replace with your NIfTI file path
    output_directory = "D:/__SHARED__/Radium_2/output_dicoms"  # Replace with desired output directory
    nifti_to_dicom_labels(nifti_file, output_directory)
