import requests
import os
import time
import sys
import tqdm
from flask import Flask, request
from dotenv import load_dotenv

load_dotenv()

oid = os.getenv('ORTHANC_OID')
olink = os.getenv('ORTHANC_LINK')
ouser = os.getenv('ORTHANC_USER')
opassword = os.getenv('ORTHANC_PASSWORD')
userid = os.getenv('ORTHANC_USERID')
base_dir= os.getcwd()
    
static_folder = os.path.join(base_dir, 'static')
template_folder = os.path.join(base_dir, 'templates')
#Save images to the 'static' folder as Flask serves images from this directory
UPLOADED_IMAGE = os.path.join(base_dir, 'static', 'images')
UPLOADED_IMAGE_COPY = os.path.join(base_dir, 'static', 'Image_Copy')
RESULT_FILE = os.path.join(base_dir, 'static', 'Results')
RESULT_COPY = os.path.join(base_dir, 'static', 'Result_Copy')
UPLOAD_GZ = os.path.join(base_dir, 'static', 'Gz_or_Rar')
RAR_EXTRACT = os.path.join(base_dir, 'static', 'rar')
GZ_EXTRACT = os.path.join(base_dir, 'static', 'Zip_gz')
UPLOAD_FOLDER_DICOM = os.path.join(base_dir, 'static', 'DICOM')
UPLOAD_FOLDER_Zip_Extract = os.path.join(base_dir, 'static', 'Zip_Extract')
UPLOAD_FOLDER_Zip_Zip = os.path.join(base_dir, 'static', 'Zip_zip')
SAVE_EDIT = os.path.join(base_dir, 'static', 'saveEdit')
SAVE_EDIT_RESIZED = os.path.join(base_dir, 'static', 'saveEditResized')


# Create a Flask app instance
app = Flask(__name__)

# Configure the app
app.config['Zip_zip'] = UPLOAD_FOLDER_Zip_Zip  # Replace with the actual path

def download_file_from_orthanc(oid, olink, ouser, opassword, userid):
    """
    Download a file from an Orthanc PACS server.

    Args:
        oid (str): The OID of the file to download.
        olink (str): The URL of the Orthanc server.
        ouser (str): The username for authentication.
        opassword (str): The password for authentication.
        userid (str): The ID of the user downloading the file.

    Returns:
        str: The path to the downloaded file.
    """

    # Create the output directory if it doesn't exist
    start_time = time.perf_counter()
    output_dir = os.path.join(app.config['Zip_zip'], userid)
    os.makedirs(output_dir, exist_ok=True)
    end_time = time.perf_counter()
    print(f"Created output directory in {end_time - start_time} seconds")

    # Create the output file path
    start_time = time.perf_counter()
    output_file_path = os.path.join(output_dir, f"{oid}.zip")
    end_time = time.perf_counter()
    print(f"Created output file path in {end_time - start_time} seconds")

    # Create the log file path
    start_time = time.perf_counter()
    log_file_path = os.path.join(output_dir, "download_progress.txt")
    end_time = time.perf_counter()
    print(f"Created log file path in {end_time - start_time} seconds")

    try:
        # Get the file size
        start_time = time.perf_counter()
        content = requests.get(olink+'/studies/' + oid + '/statistics', auth=(ouser, opassword)).json()
        total_size_in_bytes = int(content["DicomDiskSize"])
        end_time = time.perf_counter()
        print(f"Got file size in {end_time - start_time} seconds")

        # Start the timer
        start_time = time.perf_counter()
        initial_finding = time.perf_counter()
        end_time = time.perf_counter()
        print(f"Started timer in {end_time - start_time} seconds")

        # Download the file
        start_time = time.perf_counter()
        orthpatients = requests.get(olink+'/studies/' + oid + '/media', auth=(ouser, opassword), stream=True)
        end_time = time.perf_counter()
        print(f"Established connection in {end_time - start_time} seconds")

        start_time = time.perf_counter()
        block_size = 1024  # 1 Kibibyte
        progress_bar = tqdm.tqdm(total=total_size_in_bytes, unit='iB', unit_scale=True, file=sys.stdout)
        end_time = time.perf_counter()
        print(f"Initialized progress bar in {end_time - start_time} seconds")

        start_time = time.perf_counter()
        with open(log_file_path, 'w') as log_file, open(output_file_path, 'wb') as f:
            for data in orthpatients.iter_content(block_size):
                progress_bar.update(len(data))
                percent_downloaded = round(progress_bar.n / (total_size_in_bytes/2.16) * 100)

                if percent_downloaded <= 100:
                    log_file.write(f"{percent_downloaded}%\n")
                else:
                    log_file.write("Extracting...\n")

                f.write(data)
            progress_bar.close()
        end_time = time.perf_counter()
        print(f"Downloaded and wrote file in {end_time - start_time} seconds")

        # Print the download time
        print(f"Downloaded {oid} in {time.perf_counter() - initial_finding} seconds")

        return output_file_path

    except requests.exceptions.RequestException as e:
        print(f"Error downloading {oid}: {e}")
        return None


def download_file():
    oid = "6627b6ac-b846cbe0-a0af01cc-f94a6bd0-990a57c6"
    # olink = "https://pacs.protosonline.in"
    olink = "https://protospacs.radiumonline.in"
    ouser = "admin"
    opassword = "password"
    userid = "Tester"
    output_file_path = download_file_from_orthanc(oid, olink, ouser, opassword, userid)
    return f"Downloaded file to {output_file_path}"

download_file()