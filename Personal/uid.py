# import httpx
# import json
# import time

# def get_study_ids(orthanc_url, study_instance_uid, username, password):
#     try:
#         client = httpx.Client()
#         start_time = time.time()
#         response = client.post(
#             f"{orthanc_url}/tools/find",
#             json={
#                 "Level": "Study",
#                 "Query": {
#                     "StudyInstanceUID": study_instance_uid
#                 }
#             },
#             auth=httpx.BasicAuth(username, password),
#             timeout=10  # 10-second timeout
#         )
#         response.raise_for_status()  # Raise an exception for 4xx or 5xx status codes
#         end_time = time.time()
#         time_taken = end_time - start_time
#         print(f"Time taken: {time_taken:.6f} seconds")
#         return response.json()
#     except httpx.RequestError as e:
#         print(f"Error occurred: {e}")
#         return None

# def main():
#     ORTHANC_URL = 'http://localhost:8042'
#     STUDY_INSTANCE_UID = '1.3.12.2.1107.5.1.4.45508.30000019041701442478100000055'
#     USERNAME = 'admin'
#     PASSWORD = 'password'

#     study_ids = get_study_ids(ORTHANC_URL, STUDY_INSTANCE_UID, USERNAME, PASSWORD)
#     print(study_ids)

# if __name__ == "__main__":
#     main()

# import requests
# import json
# from cachetools import TTLCache
# import time

# cache = TTLCache(maxsize=100, ttl=60)  # 1-minute cache

# def get_study_ids(orthanc_url, study_instance_uid, username, password):
#     try:
#         start_time = time.time()
#         if study_instance_uid in cache:
#             end_time = time.time()
#             time_taken = end_time - start_time
#             print(f"Time taken to get study IDs from cache: {time_taken:.6f} seconds")
#             return cache[study_instance_uid]
#         response = requests.post(
#             f"{orthanc_url}/tools/find",
#             json={
#                 "Level": "Study",
#                 "Query": {
#                     "StudyInstanceUID": study_instance_uid
#                 }
#             },
#             auth=(username, password),
#             timeout=10  # 10-second timeout
#         )
#         response.raise_for_status()  # Raise an exception for 4xx or 5xx status codes
#         try:
#             study_ids = response.json()
#             cache[study_instance_uid] = study_ids
#             end_time = time.time()
#             time_taken = end_time - start_time
#             print(f"Time taken to get study IDs: {time_taken:.6f} seconds")
#             return study_ids
#         except json.JSONDecodeError as e:
#             print(f"Error parsing response: {e}")
#             return None
#     except requests.RequestException as e:
#         print(f"Error occurred: {e}")
#         return None

# def main():

#     study_ids = get_study_ids(ORTHANC_URL, STUDY_INSTANCE_UID, USERNAME, PASSWORD)
#     print(study_ids)

# if __name__ == "__main__":
#     main()

import requests
import json
import time
from dotenv import load_dotenv
import os

load_dotenv()

ORTHANC_URL = os.getenv("ORTHANC_URL")
STUDY_INSTANCE_UID = os.getenv("STUDY_INSTANCE_UID")
USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")

def get_study_ids(orthanc_url, study_instance_uid, username, password):
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
            study_ids = response.json()
            end_time = time.time()
            time_taken = end_time - start_time
            print(f"Time taken to get study IDs: {time_taken:.2f} seconds")
            return study_ids
        except json.JSONDecodeError as e:
            print(f"Error parsing response: {e}")
            return None
    except requests.RequestException as e:
        print(f"Error occurred: {e}")
        return None

def main():
    study_ids = get_study_ids(ORTHANC_URL, STUDY_INSTANCE_UID, USERNAME, PASSWORD)
    print(study_ids)

if __name__ == "__main__":
    main()


# import requests
# import json
# import time
# from functools import lru_cache

# # Create a session object for connection pooling
# session = requests.Session()

# @lru_cache(maxsize=128)
# def get_study_ids(orthanc_url, study_instance_uid, username, password):
#     try:
#         start_time = time.time()
#         response = session.post(
#             f"{orthanc_url}/tools/find",
#             json={
#                 "Level": "Study",
#                 "Query": {
#                     "StudyInstanceUID": study_instance_uid
#                 }
#             },
#             auth=(username, password),
#             timeout=5  # Reduced timeout to 5 seconds
#         )
#         response.raise_for_status()
#         study_ids = response.json()
#         end_time = time.time()
#         time_taken = end_time - start_time
#         print(f"Time taken to get study IDs: {time_taken:.2f} seconds")
#         return study_ids
#     except (requests.RequestException, json.JSONDecodeError) as e:
#         print(f"Error occurred: {e}")
#         return None

# def main():
#     ORTHANC_URL = 'http://localhost:8042'
#     STUDY_INSTANCE_UID = '1.3.12.2.1107.5.1.4.45508.30000019041701442478100000055'
#     USERNAME = 'admin'
#     PASSWORD = 'password'

#     study_ids = get_study_ids(ORTHANC_URL, STUDY_INSTANCE_UID, USERNAME, PASSWORD)
#     print(study_ids)

# if __name__ == "__main__":
#     main()


# import requests
# import time

# def get_study_id(orthanc_url, study_instance_uid, username, password):
#     try:
#         start_time = time.time()
#         response = requests.get(
#             f"{orthanc_url}/studies/{study_instance_uid}",
#             auth=(username, password),
#             timeout=5
#         )
#         response.raise_for_status()
#         end_time = time.time()
#         time_taken = end_time - start_time
#         print(f"Time taken to get study ID: {time_taken:.2f} seconds")
#         return response.json().get('ID')
#     except requests.RequestException as e:
#         print(f"Error occurred: {e}")
#         return None

# def main():
#     ORTHANC_URL = 'http://localhost:8042'
#     STUDY_INSTANCE_UID = '1.3.12.2.1107.5.1.4.45508.30000019041701442478100000055'
#     USERNAME = 'admin'
#     PASSWORD = 'password'

#     study_id = get_study_id(ORTHANC_URL, STUDY_INSTANCE_UID, USERNAME, PASSWORD)
#     print(f"Study ID: {study_id}")

# if __name__ == "__main__":
#     main()