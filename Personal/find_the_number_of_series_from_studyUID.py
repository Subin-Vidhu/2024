# -*- coding: utf-8 -*-
"""
Created on Tue Oct  8 16:37:42 2024

@author: Subin-PC
"""

import requests
import time
import json

def get_study_series(orthanc_url, study_instance_uid, username, password):
    """
    Retrieves series information for a given study instance UID.

    Args:
        orthanc_url (str): The URL of the Orthanc server.
        study_instance_uid (str): The study instance UID.
        username (str): The username for authentication.
        password (str): The password for authentication.

    Returns:
        A dictionary containing series information, including names and IDs.
    """
    try:
        start_time = time.time()
        response = requests.post(
            f"{orthanc_url}/tools/find",
            json={
                "Level": "Study",
                "Query": {
                    "StudyInstanceUID": study_instance_uid
                }
            },
            auth=(username, password),
            timeout=10  # 10-second timeout
        )
        response.raise_for_status()  # Raise an exception for 4xx or 5xx status codes
        try:
            study_id = response.json()[0]
            study_url = f"{orthanc_url}/studies/{study_id}"
            response = requests.get(study_url, auth=(username, password), timeout=10)
            response.raise_for_status()
            study_info = response.json()
            series_ids = study_info["Series"]
            series_count = len(series_ids)
            series_info = []
            for series_id in series_ids:
                series_url = f"{orthanc_url}/series/{series_id}"
                response = requests.get(series_url, auth=(username, password), timeout=10)
                response.raise_for_status()
                series_data = response.json()
                series_name = series_data["MainDicomTags"]["SeriesDescription"]
                series_info.append({
                    "id": series_id,
                    "name": series_name
                })
            end_time = time.time()
            time_taken = end_time - start_time
            print(f"Time taken to get series information: {time_taken:.2f} seconds")
            print(f"Number of series: {series_count}")
            print("Series information:")
            for i, series in enumerate(series_info):
                print(f"{i+1}. ID: {series['id']}, Name: {series['name']}")
            return series_info
        except json.JSONDecodeError as e:
            print(f"Error parsing response: {e}")
            return None
        except requests.RequestException as e:
            print(f"Error occurred: {e}")
            return None
    except requests.RequestException as e:
        print(f"Error occurred: {e}")
        return None

# Example usage:
orthanc_url = "https://protosurokulpacs.radiumonline.in"
study_instance_uid = "1.3.12.2.1107.5.1.7.137912.30000024092008413606700000003"
username = "" # use your own credentials
password = ""

series_info = get_study_series(orthanc_url, study_instance_uid, username, password)

# To download: https://protosurokulpacs.radiumonline.in/series/4f8e3ef8-a943d37a-cc18888c-07667287-d1217b5b/media

