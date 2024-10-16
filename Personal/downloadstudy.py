import requests, os
import io
import time
from tqdm import tqdm
from dotenv import load_dotenv

def get_study_ids(orthanc_url, basic_auth, study_instance_uid):
    start_time = time.time()

    # Construct the URL for the query
    query_url = f"{orthanc_url}/tools/find"

    # Construct the query parameters
    query_params = {
        "Level": "Study",
        "Query": {
            "StudyInstanceUID": study_instance_uid
        }
    }

    # Measure time taken to establish connection and send request
    connection_start = time.time()
    response = requests.post(query_url, json=query_params, auth=("admin", "password"))
    connection_time = time.time() - connection_start
    print(f"Time taken to establish connection and send request: {connection_time:.2f} seconds")

    # Check if request was successful
    if response.status_code == 200:
        # Parse the JSON response
        parsing_start = time.time()
        studies = response.json()
        parsing_time = time.time() - parsing_start
        print(f"Time taken to parse response: {parsing_time:.2f} seconds")
        
        elapsed_time = time.time() - start_time
        print(f"Total time taken to retrieve Study ID: {elapsed_time:.2f} seconds")
        
        if studies:
            # Return the Study ID
            return studies[0]
        else:
            return None
    else:
        # Raise an exception if the request failed
        response.raise_for_status()

def download_study_as_zip(orthanc_url, basic_auth, study_id):
    start_time = time.time()
    
    # Construct the URL to download the study archive
    archive_url = f"{orthanc_url}/studies/{study_id}/media"

    # Measure time to start connection for downloading the archive
    connection_start = time.time()
    with requests.get(archive_url, auth=("admin", "password"), stream=True) as response:
        connection_time = time.time() - connection_start
        print(f"Time taken to establish connection and start download: {connection_time:.2f} seconds")
        
        response.raise_for_status()
        
        # Total size in bytes
        total_size = int(response.headers.get('content-length', 0))
        block_size = 1024  # 1 KiB blocks

        # Initialize the tqdm progress bar with percentage
        tqdm_bar = tqdm(total=total_size, unit='B', unit_scale=True, desc='Downloading', ncols=100, ascii=True, leave=True, bar_format='{l_bar}{bar} | {percentage:3.0f}%')

        # Measure time to download and write content in chunks
        download_start = time.time()
        zip_file_content = io.BytesIO()

        for data in response.iter_content(block_size):
            tqdm_bar.update(len(data))
            zip_file_content.write(data)
        
        download_time = time.time() - download_start
        tqdm_bar.close()
        print(f"Time taken to download and write content: {download_time:.2f} seconds")
    
    # Calculate time taken
    elapsed_time = time.time() - start_time
    print(f"Total time taken to download study as ZIP: {elapsed_time:.2f} seconds")

    # Return the content of the ZIP file
    return zip_file_content.getvalue()

def download_study(orthanc_url, basic_auth, study_instance_uid):
    start_time = time.time()
    
    # Get the Study ID using the provided Study Instance UID
    study_id = get_study_ids(orthanc_url, basic_auth, study_instance_uid)

    if not study_id:
        raise ValueError("StudyInstanceUID not found")

    # Download the study as a ZIP file
    zip_file_content = download_study_as_zip(orthanc_url, basic_auth, study_id)

    # Measure time to create a BytesIO object from the zip file content
    bytesio_start = time.time()
    zip_file = io.BytesIO(zip_file_content)
    bytesio_time = time.time() - bytesio_start
    print(f"Time taken to create BytesIO object: {bytesio_time:.2f} seconds")

    # Calculate total time taken
    total_time = time.time() - start_time
    print(f"Total time taken for the whole process: {total_time:.2f} seconds")

    # Return the BytesIO object and the study ID (for naming the file)
    return zip_file, study_id
load_dotenv()

orthanc_url = os.getenv('ORTHANC_LINK')
basic_auth = os.getenv('BASIC_AUTH')
study_instance_uid = os.getenv('STUDY_INSTANCE_UID')

# Test the function
if __name__ == "__main__":
    try:
        # Call the function
        zip_file, study_id = download_study(orthanc_url, basic_auth, study_instance_uid)

        # Save the file to disk (for testing purposes)
        with open(f'{study_id}.zip', 'wb') as f:
            f.write(zip_file.getvalue())
        print(f"Study {study_id} downloaded successfully as {study_id}.zip")

    except Exception as e:
        print(f"Error: {e}")
