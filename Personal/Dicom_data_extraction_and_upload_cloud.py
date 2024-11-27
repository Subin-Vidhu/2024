import os
import pydicom
import csv
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from threading import Lock
import re

class DicomInfoExtractor:
    def __init__(self, base_dir):
        self.base_dir = base_dir
        self.print_lock = Lock()
        self.csv_lock = Lock()
        self.output_file = r"E:\___SK_TEST_CASES_SREENADH___\DICOM\dicom_info.csv"
        
    def safe_print(self, message):
        with self.print_lock:
            print(message)
            
    def extract_number(self, folder_name):
        # Extract number from folder name (e.g., 'PA10' -> 10)
        match = re.search(r'PA(\d+)', folder_name)
        return int(match.group(1)) if match else float('inf')
            
    def extract_dicom_info(self, file_path):
        try:
            ds = pydicom.dcmread(file_path)
            folder_name = os.path.basename(os.path.dirname(os.path.dirname(os.path.dirname(file_path))))
            info = {
                'Folder_Number': self.extract_number(folder_name),  # For sorting
                'Folder': folder_name,
                'StudyInstanceUID': getattr(ds, 'StudyInstanceUID', 'N/A'),
                'SeriesInstanceUID': getattr(ds, 'SeriesInstanceUID', 'N/A'),
                'StudyDescription': getattr(ds, 'StudyDescription', 'N/A'),
                'SeriesDescription': getattr(ds, 'SeriesDescription', 'N/A'),
                'PatientID': getattr(ds, 'PatientID', 'N/A'),
                'PatientName': str(getattr(ds, 'PatientName', 'N/A')),
                'StudyDate': getattr(ds, 'StudyDate', 'N/A'),
                'SeriesDate': getattr(ds, 'SeriesDate', 'N/A'),
                'Modality': getattr(ds, 'Modality', 'N/A'),
                'FilePath': file_path
            }
            return info
            
        except Exception as e:
            self.safe_print(f"✗ Error processing {file_path}: {str(e)}")
            return None

    def process_all(self):
        # Find all DICOM files
        dicom_info_list = []
        pa_dirs = [d for d in os.listdir(self.base_dir) 
                   if os.path.isdir(os.path.join(self.base_dir, d)) 
                   and d.startswith('PA') 
                   and d != 'not_uploaded_to_cloud']
        
        # Sort PA dirs numerically
        pa_dirs.sort(key=self.extract_number)
        
        for pa_dir in pa_dirs:
            se_path = os.path.join(self.base_dir, pa_dir, 'ST0', 'SE0')
            if not os.path.exists(se_path):
                continue
                
            im_files = [os.path.join(se_path, f) for f in os.listdir(se_path) 
                       if f.startswith('IM')]
            # Only take first file from each series for efficiency
            if im_files:
                dicom_info_list.append(im_files[0])
        
        print(f"\nProcessing {len(dicom_info_list)} DICOM folders...")
        
        # Process files in parallel and collect results
        with ThreadPoolExecutor(max_workers=10) as executor:
            results = list(executor.map(self.extract_dicom_info, dicom_info_list))
        
        # Filter out None results (from errors) and sort by folder number
        results = [r for r in results if r]
        results.sort(key=lambda x: x['Folder_Number'])
        
        # Write sorted results to CSV
        if results:
            headers = list(results[0].keys())
            headers.remove('Folder_Number')  # Remove sorting key from output
            
            with open(self.output_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=headers)
                writer.writeheader()
                for result in results:
                    row = {k: v for k, v in result.items() if k != 'Folder_Number'}
                    writer.writerow(row)
        
        success_count = len(results)
        print(f"\nExtraction complete: {success_count}/{len(dicom_info_list)} folders processed")
        print(f"Results saved to: {self.output_file}")

if __name__ == "__main__":
    base_directory = r"E:\___SK_TEST_CASES_SREENADH___\DICOM"
    
    extractor = DicomInfoExtractor(base_directory)
    extractor.process_all()

#############################   details as json data
# import os
# import pydicom
# import json
# from pathlib import Path
# from concurrent.futures import ThreadPoolExecutor
# from threading import Lock
# import re

# class DicomInfoExtractor:
#     def __init__(self, base_dir):
#         self.base_dir = base_dir
#         self.print_lock = Lock()
#         self.json_data = {}
        
#     def safe_print(self, message):
#         with self.print_lock:
#             print(message)
            
#     def extract_dicom_info(self, file_path, folder_number):
#         try:
#             ds = pydicom.dcmread(file_path)
#             folder_name = os.path.basename(os.path.dirname(os.path.dirname(os.path.dirname(file_path))))
            
#             info = {
#                 'folder_name': folder_name,
#                 'folder_number': folder_number,
#                 'study_info': {
#                     'StudyInstanceUID': getattr(ds, 'StudyInstanceUID', 'N/A'),
#                     'StudyDescription': getattr(ds, 'StudyDescription', 'N/A'),
#                     'StudyDate': getattr(ds, 'StudyDate', 'N/A'),
#                 },
#                 'series_info': {
#                     'SeriesInstanceUID': getattr(ds, 'SeriesInstanceUID', 'N/A'),
#                     'SeriesDescription': getattr(ds, 'SeriesDescription', 'N/A'),
#                     'SeriesDate': getattr(ds, 'SeriesDate', 'N/A'),
#                 },
#                 'patient_info': {
#                     'PatientID': getattr(ds, 'PatientID', 'N/A'),
#                     'PatientName': str(getattr(ds, 'PatientName', 'N/A')),
#                 },
#                 'modality': getattr(ds, 'Modality', 'N/A'),
#                 'file_path': file_path
#             }
            
#             return info
            
#         except Exception as e:
#             self.safe_print(f"✗ Error processing {file_path}: {str(e)}")
#             return None

#     def natural_sort_key(self, s):
#         return [int(c) if c.isdigit() else c.lower() for c in re.split('([0-9]+)', s)]

#     def process_all(self):
#         # Find all DICOM files
#         pa_dirs = [d for d in os.listdir(self.base_dir) 
#                    if os.path.isdir(os.path.join(self.base_dir, d)) 
#                    and d.startswith('PA') 
#                    and d != 'not_uploaded_to_cloud']
        
#         # Sort PA dirs naturally
#         pa_dirs.sort(key=self.natural_sort_key)
        
#         dicom_files = []
#         folder_numbers = []
        
#         # Create a mapping of folder names to numbers
#         for index, pa_dir in enumerate(pa_dirs, 1):
#             se_path = os.path.join(self.base_dir, pa_dir, 'ST0', 'SE0')
#             if not os.path.exists(se_path):
#                 continue
                
#             im_files = [os.path.join(se_path, f) for f in os.listdir(se_path) 
#                        if f.startswith('IM')]
#             # Only take first file from each series for efficiency
#             if im_files:
#                 dicom_files.append(im_files[0])
#                 folder_numbers.append(index)
        
#         print(f"\nProcessing {len(dicom_files)} DICOM folders...")
        
#         # Process files and store results
#         results = []
#         with ThreadPoolExecutor(max_workers=10) as executor:
#             futures = [executor.submit(self.extract_dicom_info, file, num) 
#                       for file, num in zip(dicom_files, folder_numbers)]
#             for future in futures:
#                 result = future.result()
#                 if result:
#                     results.append(result)
        
#         # Sort results by folder number
#         results.sort(key=lambda x: x['folder_number'])
        
#         # Create final JSON structure
#         json_data = {
#             'total_folders': len(results),
#             'folders': results
#         }
        
#         # Save to JSON file
#         output_file = r"E:\___SK_TEST_CASES_SREENADH___\DICOM\dicom_info.json"
#         with open(output_file, 'w', encoding='utf-8') as f:
#             json.dump(json_data, f, indent=2)
        
#         print(f"\nExtraction complete: {len(results)} folders processed")
#         print(f"Results saved to: {output_file}")
        
#         # Print sample of the first folder's data
#         if results:
#             print("\nSample data from first folder:")
#             first_folder = results[0]
#             print(f"Folder Number: {first_folder['folder_number']}")
#             print(f"Folder Name: {first_folder['folder_name']}")
#             print(f"Study UID: {first_folder['study_info']['StudyInstanceUID']}")
#             print(f"Series UID: {first_folder['series_info']['SeriesInstanceUID']}")

# if __name__ == "__main__":
#     base_directory = r"E:\___SK_TEST_CASES_SREENADH___\DICOM"
    
#     extractor = DicomInfoExtractor(base_directory)
#     extractor.process_all()

# import os
# import requests
# from concurrent.futures import ThreadPoolExecutor, as_completed
# import time
# from threading import Lock

# class OptimizedDicomUploader:
#     def __init__(self, base_dir, server_url, username, password, max_workers=20):
#         self.base_dir = base_dir
#         if not server_url.startswith(('http://', 'https://')):
#             server_url = 'http://' + server_url
#         self.server_url = server_url
#         self.auth = (username, password)
#         self.max_workers = max_workers
#         self.print_lock = Lock()
#         self.success_count = 0
#         self.total_count = 0

#     def safe_print(self, message):
#         with self.print_lock:
#             print(message)
    
#     def upload_file(self, file_path):
#         try:
#             with open(file_path, 'rb') as f:
#                 # Use Orthanc's REST API with authentication
#                 response = requests.post(
#                     f"{self.server_url}/instances",
#                     data=f.read(),
#                     auth=self.auth,
#                     headers={'Content-Type': 'application/dicom'}
#                 )
                
#             if response.status_code == 200:
#                 self.success_count += 1
#                 self.safe_print(f"✓ Uploaded: {os.path.basename(file_path)}")
#                 return True
#             else:
#                 self.safe_print(f"✗ Failed {os.path.basename(file_path)}: {response.status_code}")
#                 return False
                
#         except Exception as e:
#             self.safe_print(f"✗ Error with {os.path.basename(file_path)}: {str(e)}")
#             return False

#     def find_dicom_files(self):
#         dicom_files = []
#         pa_dirs = [d for d in os.listdir(self.base_dir) 
#                    if os.path.isdir(os.path.join(self.base_dir, d)) 
#                    and d.startswith('PA') 
#                    and d != 'not_uploaded_to_cloud']
        
#         for pa_dir in sorted(pa_dirs):
#             se_path = os.path.join(self.base_dir, pa_dir, 'ST0', 'SE0')
#             if not os.path.exists(se_path):
#                 continue
                
#             im_files = [os.path.join(se_path, f) for f in os.listdir(se_path) 
#                        if f.startswith('IM')]
#             dicom_files.extend(im_files)
        
#         return dicom_files

#     def upload_all(self):
#         start_time = time.time()
#         files = self.find_dicom_files()
#         self.total_count = len(files)
        
#         print(f"\nStarting upload of {self.total_count} files using {self.max_workers} parallel connections...")
        
#         with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
#             futures = [executor.submit(self.upload_file, file) for file in files]
#             for future in as_completed(futures):
#                 pass
                
#         elapsed_time = time.time() - start_time
#         print(f"\nUpload complete in {elapsed_time:.1f} seconds")
#         print(f"Successfully uploaded: {self.success_count}/{self.total_count} files")
#         print(f"Average speed: {self.total_count/elapsed_time:.1f} files/second")

# if __name__ == "__main__":
#     base_directory = r"E:\___SK_TEST_CASES_SREENADH___\DICOM"
#     server_url = "https://skpacs.protosonline.in/"
#     username = ""
#     password = ""
    
#     uploader = OptimizedDicomUploader(
#         base_directory,
#         server_url,
#         username=username,
#         password=password,
#         max_workers=20
#     )
    
#     uploader.upload_all()

# # -*- coding: utf-8 -*-
# """
# Created on Wed Nov 27 10:18:19 2024

# @author: Subin-PC
# """

# import os
# import requests
# import base64
# from pathlib import Path

# def upload_dicom_to_orthanc(base_dir, orthanc_url, username, password):
#     """
#     Upload DICOM files to Orthanc server recursively from given directory structure
    
#     Args:
#         base_dir (str): Base directory containing PA* folders
#         orthanc_url (str): Orthanc server URL
#         username (str): Orthanc username
#         password (str): Orthanc password
#     """
#     # Create session for repeated requests
#     session = requests.Session()
#     session.auth = (username, password)
    
#     # Ensure URL has correct format
#     if not orthanc_url.startswith(('http://', 'https://')):
#         orthanc_url = 'http://' + orthanc_url
    
#     upload_url = f"{orthanc_url}/instances"
    
#     # Get all PA* directories except 'not_uploaded_to_cloud'
#     pa_dirs = [d for d in os.listdir(base_dir) 
#                if os.path.isdir(os.path.join(base_dir, d)) 
#                and d.startswith('PA') 
#                and d != 'not_uploaded_to_cloud']
    
#     total_files = 0
#     uploaded_files = 0
    
#     # Process each PA directory
#     for pa_dir in sorted(pa_dirs):
#         pa_path = os.path.join(base_dir, pa_dir)
        
#         # Navigate through ST0/SE0 structure
#         st_path = os.path.join(pa_path, 'ST0')
#         se_path = os.path.join(st_path, 'SE0')
        
#         if not os.path.exists(se_path):
#             print(f"Warning: Expected path not found: {se_path}")
#             continue
            
#         # Find all IM* files
#         im_files = [f for f in os.listdir(se_path) if f.startswith('IM')]
#         total_files += len(im_files)
        
#         for im_file in sorted(im_files):
#             file_path = os.path.join(se_path, im_file)
#             try:
#                 with open(file_path, 'rb') as f:
#                     dicom_content = f.read()
                
#                 # Upload to Orthanc
#                 response = session.post(
#                     upload_url,
#                     data=dicom_content,
#                     headers={'Content-Type': 'application/dicom'}
#                 )
                
#                 if response.status_code == 200:
#                     uploaded_files += 1
#                     print(f"Successfully uploaded: {file_path}")
#                 else:
#                     print(f"Failed to upload {file_path}: {response.status_code} - {response.text}")
                    
#             except Exception as e:
#                 print(f"Error processing {file_path}: {str(e)}")
    
#     print(f"\nUpload complete: {uploaded_files}/{total_files} files uploaded successfully")

# # Usage
# base_directory = r"E:\___SK_TEST_CASES_SREENADH___\DICOM"
# orthanc_url = ""
# username = ""
# password = ""

# upload_dicom_to_orthanc(base_directory, orthanc_url, username, password)
