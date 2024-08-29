# -*- coding: utf-8 -*-
"""
Created on Tue Aug 27 10:56:59 2024

@author: Subin-PC
"""

import requests
import httpx
import aiohttp
import asyncio
import time

def get_study_ids_requests(orthanc_url, study_instance_uid, username, password):
    query_url = f"{orthanc_url}/tools/find"
    query_params = {
        "Level": "Study",
        "Query": {
            "StudyInstanceUID": study_instance_uid
        }
    }
    response = requests.post(query_url, json=query_params, auth=(username, password))
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to retrieve study IDs. Status code: {response.status_code}")
        return None

async def get_study_ids_aiohttp(orthanc_url, study_instance_uid, username, password):
    async with aiohttp.ClientSession() as session:
        async with session.post(
            f"{orthanc_url}/tools/find",
            json={
                "Level": "Study",
                "Query": {
                    "StudyInstanceUID": study_instance_uid
                }
            },
            auth=aiohttp.BasicAuth(username, password)
        ) as response:
            if response.status == 200:
                return await response.json()
            else:
                print(f"Failed to retrieve study IDs. Status code: {response.status}")
                return None

async def get_study_ids_httpx(orthanc_url, study_instance_uid, username, password):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{orthanc_url}/tools/find",
            json={
                "Level": "Study",
                "Query": {
                    "StudyInstanceUID": study_instance_uid
                }
            },
            auth=httpx.BasicAuth(username, password)
        )
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Failed to retrieve study IDs. Status code: {response.status_code}")
            return None

async def main():

    # Requests
    start_time = time.time()
    study_ids = get_study_ids_requests(ORTHANC_URL, STUDY_INSTANCE_UID, USERNAME, PASSWORD)
    end_time = time.time()
    print(f"Requests: {end_time - start_time} seconds")

    # AIOHTTP
    start_time = time.time()
    study_ids = await get_study_ids_aiohttp(ORTHANC_URL, STUDY_INSTANCE_UID, USERNAME, PASSWORD)
    end_time = time.time()
    print(f"AIOHTTP: {end_time - start_time} seconds")

    # HTTPX
    start_time = time.time()
    study_ids = await get_study_ids_httpx(ORTHANC_URL, STUDY_INSTANCE_UID, USERNAME, PASSWORD)
    end_time = time.time()
    print(f"HTTPX: {end_time - start_time} seconds")

asyncio.run(main())