import requests
import io
import time

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
    # Send POST request to Orthanc server with Basic Authentication
    response = requests.post(query_url, json=query_params, auth=("admin", "password"))

    # Check if request was successful
    if response.status_code == 200:
        # Parse the JSON response
        studies = response.json()
        elapsed_time = time.time() - start_time
        print(f"Time taken to retrieve Study ID: {elapsed_time:.2f} seconds")
        
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

    # Send GET request to download the archive
    response = requests.get(archive_url, auth=("admin", "password"))
    response.raise_for_status()

    # Calculate time taken
    elapsed_time = time.time() - start_time
    print(f"Time taken to download study as ZIP: {elapsed_time:.2f} seconds")

    # Return the content of the ZIP file
    return response.content


def download_study(orthanc_url, basic_auth, study_instance_uid):
    start_time = time.time()
    
    # Get the Study ID using the provided Study Instance UID
    study_id = get_study_ids(orthanc_url, basic_auth, study_instance_uid)

    if not study_id:
        raise ValueError("StudyInstanceUID not found")

    # Download the study as a ZIP file
    zip_file_content = download_study_as_zip(orthanc_url, basic_auth, study_id)

    # Create a BytesIO object from the zip file content
    zip_file = io.BytesIO(zip_file_content)

    # Calculate total time taken
    total_time = time.time() - start_time
    print(f"Total time taken for the whole process: {total_time:.2f} seconds")

    # Return the BytesIO object and the study ID (for naming the file)
    return zip_file, study_id


# Test the function
if __name__ == "__main__":
    # Set your parameters
    orthanc_url = "http://192.168.1.188:8042"
    basic_auth = "Basic YWRtaW46cGFzc3dvcmQ="
    study_instance_uid = "1.3.12.2.1107.5.1.7.107889.30000024081417115758500000006"

    try:
        # Call the function
        zip_file, study_id = download_study(orthanc_url, basic_auth, study_instance_uid)

        # Save the file to disk (for testing purposes)
        with open(f'{study_id}.zip', 'wb') as f:
            f.write(zip_file.getvalue())
        print(f"Study {study_id} downloaded successfully as {study_id}.zip")

    except Exception as e:
        print(f"Error: {e}")
