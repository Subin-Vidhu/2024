# File downloaded successfully.
# Total download time: 25.92 seconds
# Downloaded file size: 171.40 MB
# Download speed: 6.61 MB/s

import requests
from requests.auth import HTTPBasicAuth
import time
import os
import shutil

# Orthanc server URL
ORTHANC_URL = "https://pacs.protosonline.in/studies/{}/media"

# Username and password for the Orthanc server
USERNAME = "admin"
PASSWORD = "password"

# The ID of the study you want to download as a DICOMDIR (media)
STUDY_ID = "6627b6ac-b846cbe0-a0af01cc-f94a6bd0-990a57c6"  # Replace with your actual study ID

def download_media(study_id, username, password):
    start_time = time.time()
    print("Step 1: Constructing the URL...")
    url = ORTHANC_URL.format(study_id)
    print(f"URL constructed: {url}")
    print(f"Time taken for Step 1: {time.time() - start_time:.2f} seconds")

    start_time1 = time.time()
    print("Step 2: Starting the timer...")
    start_time = time.time()
    print(f"Timer started at: {start_time}")
    print(f"Time taken for Step 2: {time.time() - start_time:.2f} seconds")

    start_time = time.time()
    print("Step 3: Sending the GET request...")
    response = requests.get(url, auth=HTTPBasicAuth(username, password), stream=True)
    print("GET request sent.")
    print(f"Time taken for Step 3: {time.time() - start_time:.2f} seconds")

    if response.status_code == 200:
        start_time = time.time()
        print("Step 4: Downloading the file...")
        dir_path = os.path.dirname(__file__)
        target_dir = os.path.join(dir_path, "DICOMDIR")

        if os.path.exists(target_dir):
            print("Step 5: Removing the existing directory...")
            shutil.rmtree(target_dir, ignore_errors=True)
            print("Existing directory removed.")
        print(f"Time taken for Step 4 and 5: {time.time() - start_time:.2f} seconds")

        start_time = time.time()
        print("Step 6: Creating the new directory...")
        os.makedirs(target_dir)
        print("New directory created.")
        print(f"Time taken for Step 6: {time.time() - start_time:.2f} seconds")

        start_time = time.time()
        try:
            print("Step 7: Writing the file to the directory...")
            with open(os.path.join(target_dir, "downloaded_media.zip"), "wb") as file:
                for chunk in response.iter_content(chunk_size=4096):
                    file.write(chunk)
            print("File written to the directory.")
        except IOError as e:
            print(f"Error writing file: {e}")
        print(f"Time taken for Step 7: {time.time() - start_time:.2f} seconds")

        start_time = time.time()
        print("Step 8: Stopping the timer...")
        end_time = time.time()
        print(f"Timer stopped at: {end_time}")
        print(f"Time taken for Step 8: {time.time() - start_time:.2f} seconds")

        download_time_time_module = end_time - start_time1
        download_time_elapsed = response.elapsed.total_seconds()
        file_size_MB = int(response.headers['Content-Length']) / (1024 * 1024)
        download_speed_MBps_time_module = file_size_MB / download_time_time_module
        download_speed_MBps_elapsed = file_size_MB / download_time_elapsed

        print(f"Total download time (time module): {download_time_time_module:.2f} seconds")
        print(f"Total download time (elapsed): {download_time_elapsed:.2f} seconds")
        print(f"Downloaded file size: {file_size_MB:.2f} MB")
        print(f"Download speed (time module): {download_speed_MBps_time_module:.2f} MB/s")
        print(f"Download speed (elapsed): {download_speed_MBps_elapsed:.2f} MB/s")
    else:
        print(f"Failed to download file. Status code: {response.status_code}")
        if response.status_code == 401:
            print("Authentication failed. Check your username and password.")
        elif response.status_code == 404:
            print("Resource not found. Check the study ID.")

if __name__ == "__main__":
    download_media(STUDY_ID, USERNAME, PASSWORD)

#httpx

# Total download time: 54.83 seconds
# Downloaded file size: 171.38 MB
# Download speed: 3.13 MB/s

# import httpx
# import time
# import os
# import shutil

# # Orthanc server URL
# orthanc_url = "https://pacs.protosonline.in/studies/{}/media"

# # Username and password for the Orthanc server
# username = "admin"
# password = "password"

# # The ID of the study you want to download as a DICOMDIR (media)
# study_id = "6627b6ac-b846cbe0-a0af01cc-f94a6bd0-990a57c6"  # Replace with your actual study ID

# # Construct the full URL for the media file
# url = orthanc_url.format(study_id)  # Format the URL with the study ID

# start_time = time.time()
# auth = httpx.BasicAuth(username, password)
# with httpx.stream("GET", url, auth=auth, timeout=300) as response:
#     dir_path = os.path.dirname(__file__)
#     target_dir = os.path.join(dir_path, "DICOMDIR")
#     if os.path.exists(target_dir):
#         shutil.rmtree(target_dir, ignore_errors=True)
#     os.makedirs(target_dir)
#     with open(os.path.join(target_dir, "downloaded_media.zip"), "wb") as file:
#         for chunk in response.iter_bytes():
#             file.write(chunk)
# end_time = time.time()
# download_time = end_time - start_time
# file_size_MB = os.path.getsize(os.path.join(target_dir, "downloaded_media.zip")) / (1024 * 1024)
# download_speed_MBps = file_size_MB / download_time
# print(f"Total download time: {download_time:.2f} seconds")
# print(f"Downloaded file size: {file_size_MB:.2f} MB")
# print(f"Download speed: {download_speed_MBps:.2f} MB/s")

#urlib3

# no output even after 2 minutes

# import urllib3
# import time
# import os
# import shutil
# import base64

# # Orthanc server URL
# orthanc_url = "https://pacs.protosonline.in/studies/{}/media"

# # Username and password for the Orthanc server
# username = "admin"
# password = "password"

# # The ID of the study you want to download as a DICOMDIR (media)
# study_id = "6627b6ac-b846cbe0-a0af01cc-f94a6bd0-990a57c6"  # Replace with your actual study ID

# # Construct the full URL for the media file
# url = orthanc_url.format(study_id)  # Format the URL with the study ID

# start_time = time.time()
# http = urllib3.PoolManager()
# auth_header = "Basic " + base64.b64encode(f"{username}:{password}".encode()).decode()
# response = http.request('GET', url, headers={"Authorization": auth_header})
# dir_path = os.path.dirname(__file__)
# target_dir = os.path.join(dir_path, "DICOMDIR")
# if os.path.exists(target_dir):
#     shutil.rmtree(target_dir, ignore_errors=True)
# os.makedirs(target_dir)
# with open(os.path.join(target_dir, "downloaded_media.zip"), "wb") as file:
#     file.write(response.data)
# end_time = time.time()
# download_time = end_time - start_time
# file_size_MB = len(response.data) / (1024 * 1024)
# download_speed_MBps = file_size_MB / download_time
# print(f"Total download time: {download_time:.2f} seconds")
# print(f"Downloaded file size: {file_size_MB:.2f} MB")
# print(f"Download speed: {download_speed_MBps:.2f} MB/s")

#pycurl


# Total download time: 54.52 seconds
# Downloaded file size: 171.38 MB
# Download speed: 3.14 MB/s

# import pycurl
# import time
# import os
# import shutil

# # Orthanc server URL
# orthanc_url = "https://pacs.protosonline.in/studies/{}/media"

# # Username and password for the Orthanc server
# username = "admin"
# password = "password"

# # The ID of the study you want to download as a DICOMDIR (media)
# study_id = "6627b6ac-b846cbe0-a0af01cc-f94a6bd0-990a57c6"  # Replace with your actual study ID

# # Construct the full URL for the media file
# url = orthanc_url.format(study_id)  # Format the URL with the study ID

# start_time = time.time()
# curl = pycurl.Curl()
# curl.setopt(pycurl.URL, url)
# curl.setopt(pycurl.HTTPAUTH, pycurl.HTTPAUTH_BASIC)
# curl.setopt(pycurl.USERPWD, "{}:{}".format(username, password))
# dir_path = os.path.dirname(__file__)
# target_dir = os.path.join(dir_path, "DICOMDIR")
# if os.path.exists(target_dir):
#     shutil.rmtree(target_dir, ignore_errors=True)
# os.makedirs(target_dir)
# with open(os.path.join(target_dir, "downloaded_media.zip"), "wb") as file:
#     curl.setopt(pycurl.WRITEDATA, file)
#     curl.perform()
# end_time = time.time()
# download_time = end_time - start_time
# file_size_MB = os.path.getsize(os.path.join(target_dir, "downloaded_media.zip")) / (1024 * 1024)
# download_speed_MBps = file_size_MB / download_time
# print(f"Total download time: {download_time:.2f} seconds")
# print(f"Downloaded file size: {file_size_MB:.2f} MB")
# print(f"Download speed: {download_speed_MBps:.2f} MB/s")
#aiohttp

# Total download time: 53.23 seconds
# Downloaded file size: 171.38 MB
# Download speed: 3.22 MB/s

# import aiohttp
# import asyncio
# import time
# import os
# import shutil

# # Orthanc server URL
# orthanc_url = "https://pacs.protosonline.in/studies/{}/media"

# # Username and password for the Orthanc server
# username = "admin"
# password = "password"

# # The ID of the study you want to download as a DICOMDIR (media)
# study_id = "6627b6ac-b846cbe0-a0af01cc-f94a6bd0-990a57c6"  # Replace with your actual study ID

# # Construct the full URL for the media file
# url = orthanc_url.format(study_id)  # Format the URL with the study ID

# async def fetch_page(session, url):
#     async with session.get(url) as response:
#         return await response.read()

# async def main():
#     start_time = time.time()
#     auth = aiohttp.BasicAuth(username, password)
#     session = aiohttp.ClientSession(auth=auth)
#     page = await fetch_page(session, url)
#     dir_path = os.path.dirname(__file__)
#     target_dir = os.path.join(dir_path, "DICOMDIR")
#     if os.path.exists(target_dir):
#         shutil.rmtree(target_dir, ignore_errors=True)
#     os.makedirs(target_dir)
#     with open(os.path.join(target_dir, "downloaded_media.zip"), "wb") as file:
#         file.write(page)
#     await session.close()
#     end_time = time.time()
#     download_time = end_time - start_time
#     file_size_MB = len(page) / (1024 * 1024)
#     download_speed_MBps = file_size_MB / download_time
#     print(f"Total download time: {download_time:.2f} seconds")
#     print(f"Downloaded file size: {file_size_MB:.2f} MB")
#     print(f"Download speed: {download_speed_MBps:.2f} MB/s")

# asyncio.run(main())



#########################################################################################
# import concurrent.futures
# import os
# import shutil
# import logging
# import MySQLdb
# import pydicom
# import dicom2nifti
# import zipfile
# import aiohttp
# import sys
# import re
# import tqdm
# from flask import Flask, session
# from flask import flash
# from dotenv import load_dotenv
# import time
# import asyncio

# app = Flask(__name__)

# # Load environment variables from .env file
# load_dotenv()

# base_dir = os.getcwd()
# if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
#     base_dir = os.path.join(sys._MEIPASS)

# static_folder = os.path.join(base_dir, 'static')
# template_folder = os.path.join(base_dir, 'templates')
# # Save images to the 'static' folder as Flask serves images from this directory
# UPLOADED_IMAGE = os.path.join(base_dir, 'static', 'images')
# UPLOADED_IMAGE_COPY = os.path.join(base_dir, 'static', 'Image_Copy')
# RESULT_FILE = os.path.join(base_dir, 'static', 'Results')
# RESULT_COPY = os.path.join(base_dir, 'static', 'Result_Copy')
# UPLOAD_GZ = os.path.join(base_dir, 'static', 'Gz_or_Rar')
# RAR_EXTRACT = os.path.join(base_dir, 'static', 'rar')
# GZ_EXTRACT = os.path.join(base_dir, 'static', 'Zip_gz')
# UPLOAD_FOLDER_DICOM = os.path.join(base_dir, 'static', 'DICOM')
# UPLOAD_FOLDER_Zip_Extract = os.path.join(base_dir, 'static', 'Zip_Extract')
# UPLOAD_FOLDER_Zip_Zip = os.path.join(base_dir, 'static', 'Zip_zip')
# SAVE_EDIT = os.path.join(base_dir, 'static', 'saveEdit')
# SAVE_EDIT_RESIZED = os.path.join(base_dir, 'static', 'saveEditResized')

# # Define the upload folder to save images uploaded by the user.
# app.config['UPLOADED_IMAGE'] = UPLOADED_IMAGE
# app.config['UPLOADED_IMAGE_COPY'] = UPLOADED_IMAGE_COPY
# app.config['RESULT_COPY'] = RESULT_COPY
# app.config['RESULT_FILE'] = RESULT_FILE
# app.config['UPLOAD_GZ'] = UPLOAD_GZ
# app.config['GZ_EXTRACT'] = GZ_EXTRACT
# app.config['RAR_EXTRACT'] = RAR_EXTRACT
# app.config['Zip_Extract'] = UPLOAD_FOLDER_Zip_Extract
# app.config['Zip_zip'] = UPLOAD_FOLDER_Zip_Zip
# app.config['Dicom'] = UPLOAD_FOLDER_DICOM
# app.config['saveEdit'] = SAVE_EDIT
# app.config['saveEditResized'] = SAVE_EDIT_RESIZED

# # Create a logger
# logger = logging.getLogger(__name__)
# logger.setLevel(logging.INFO)

# # Create a file handler
# file_handler = logging.FileHandler(os.path.join(base_dir, 'progress.log'))
# file_handler.setLevel(logging.INFO)

# # Create a console handler
# console_handler = logging.StreamHandler()
# console_handler.setLevel(logging.INFO)

# # Create a formatter and add it to the handlers
# formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# file_handler.setFormatter(formatter)
# console_handler.setFormatter(formatter)

# # Add the handlers to the logger
# logger.addHandler(file_handler)
# logger.addHandler(console_handler)

# def load_envfile():
#     # Get the path to the user's application data directory
#     db_host = os.getenv("DB_HOST")
#     db_port = os.getenv("DB_PORT")
#     db_user = os.getenv("DB_USER")
#     db_password = os.getenv("DB_PASSWORD")
#     db_name = os.getenv("MYSQL_DB")

#     print(f"DB_HOST: {db_host}, DB_PORT: {db_port}, DB_USER: {db_user}, DB_PASSWORD: {db_password}, DB_NAME: {db_name}")

#     # print("db_host", db_host, "db_port", db_port, "db_user", db_user, "db_password", db_password, "db_name", db_name)

#     return db_host, db_port, db_user, db_password, db_name

# from aiohttp import BasicAuth

# async def download_zip_file(oid, userid, olink, ouser, opassword):
#     start_time = time.time()
#     async with aiohttp.ClientSession() as session:
#         auth = BasicAuth(ouser, opassword)
#         async with session.get(olink + '/studies/' + oid + '/media', auth=auth) as response:
#             zip_file_path = os.path.join(app.config['Zip_zip'], userid, f"{oid}.zip")
#             with open(zip_file_path, 'wb') as f:
#                 chunk_size = 4096
#                 total_size_in_bytes = int(response.headers['Content-Length'])
#                 progress_bar = tqdm.tqdm(total=total_size_in_bytes, unit='iB', unit_scale=True)
#                 while True:
#                     chunk = await response.content.read(chunk_size)
#                     if not chunk:
#                         break
#                     f.write(chunk)
#                     progress_bar.update(len(chunk))
#                 progress_bar.close()
#     end_time = time.time()
#     logger.info(f"Download zip file took {end_time - start_time} seconds")
#     return zip_file_path

# def extract_zip_file(zip_file_path):
#     start_time = time.time()
#     folder = os.path.join(app.config['Zip_Extract'], userid)
#     if not os.path.exists(folder):
#         os.mkdir(folder)
#     with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
#         zip_ref.extractall(folder)
#     end_time = time.time()
#     logger.info(f"Extract zip file took {end_time - start_time} seconds")
#     return folder

# def convert_dicom_to_nifti(extracted_folder_path):
#     start_time = time.time()
#     path_to_save_nifti_file = os.path.join(app.config['UPLOADED_IMAGE'], userid, "img.nii")
#     dicom2nifti.dicom_series_to_nifti(extracted_folder_path, path_to_save_nifti_file)
#     end_time = time.time()
#     logger.info(f"Convert dicom to nifti took {end_time - start_time} seconds")
#     return path_to_save_nifti_file

# def copy_files(origin, target):
#     start_time = time.time()
#     files = os.listdir(origin)
#     for file_name in files:
#         shutil.copy(os.path.join(origin, file_name), os.path.join(target, file_name))
#     end_time = time.time()
#     logger.info(f"Copy files took {end_time - start_time} seconds")

# def database_operations(patient_details):
#     start_time = time.time()
#     db_host, db_port, db_user, db_password, db_name = load_envfile()
#     db = MySQLdb.connect(host=db_host, port=int(db_port), user=db_user, passwd=db_password, db=db_name)
#     cursor = db.cursor()
#     cursor.execute("SELECT distinct patient_autoid FROM patient_details WHERE patient_studyuid='" + patient_details[6] + "' AND patient_crtby='" + userid + "'")
#     rows = cursor.fetchall()
#     cursor.close()
#     patient_autoid = 0
#     for row in rows:
#         patient_autoid = row[0]
#     if patient_autoid == 0 or patient_autoid is None:
#         cursor1 = db.cursor()
#         cursor1.execute("REPLACE into patient_details(patient_studyid, patient_id, patient_studyuid, patient_age, patient_gender, patient_studydate, patient_description, patient_crtby) value(%s, %s, %s, %s, %s, %s, %s, %s)", (patient_details[0], patient_details[1], patient_details[6], patient_details[3], patient_details[4], patient_details[5], patient_details[2], userid))
#         db.commit()
#         patient_autoid = cursor1.lastrowid
#     db.close()
#     end_time = time.time()
#     logger.info(f"Database operations took {end_time - start_time} seconds")
#     return patient_autoid

# async def main(oid, userid, olink, ouser, opassword):
#     start_time = time.time()
#     zip_file_path = await download_zip_file(oid, userid, olink, ouser, opassword)
#     extracted_folder_path = extract_zip_file(zip_file_path)
#     nifti_file_path = convert_dicom_to_nifti(extracted_folder_path)
#     copy_files(os.path.join(app.config['UPLOADED_IMAGE'], userid), os.path.join(app.config['UPLOADED_IMAGE_COPY'], userid))
#     patient_details = []
#     folder1 = os.path.join(extracted_folder_path, "IMAGES")
#     entries = os.listdir(folder1)
#     dicom_path = os.path.join(folder1, entries[0])
#     ds = pydicom.read_file(dicom_path)
#     patient_details.append(ds["StudyID"].value)
#     patient_details.append(ds["PatientID"].value)
#     patient_details.append(ds["StudyDescription"].value)
#     patient_details.append(ds["PatientAge"].value)
#     patient_details.append(ds["PatientSex"].value)
#     patient_details.append(ds["StudyDate"].value)
#     patient_details.append(ds["StudyInstanceUID"].value)
#     patient_autoid = database_operations(patient_details)
#     logger.info("Converting...")
#     logger.info("Extracted...")
#     end_time = time.time()
#     logger.info(f"Total time took {end_time - start_time} seconds")
#     return patient_autoid

# if __name__ == '__main__':
#     oid = '6627b6ac-b846cbe0-a0af01cc-f94a6bd0-990a57c6'
#     userid = '2'
#     olink = 'https://pacs.protosonline.in/'
#     ouser = 'admin'
#     opassword = 'password'
#     patient_autoid = asyncio.run(main(oid, userid, olink, ouser, opassword))
#     print(patient_autoid)