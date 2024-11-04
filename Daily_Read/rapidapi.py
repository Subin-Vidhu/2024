# -*- coding: utf-8 -*-
"""
Created on Sun Oct 22 13:40:38 2023

@author: Subin-PC
"""

#Browser: https://rapidapi.com/googlecloud/api/google-translate1/
# Testing language
import requests

url = "https://google-translate1.p.rapidapi.com/language/translate/v2/detect"

payload = { "q": "English is hard, but detectably so" }
headers = {
	"content-type": "application/x-www-form-urlencoded",
	"Accept-Encoding": "application/gzip",
	"X-RapidAPI-Key": "fe76a72813mshce74e93488d33c5p155a2ejsndad865e267b7",
	"X-RapidAPI-Host": "google-translate1.p.rapidapi.com"
}

response = requests.post(url, data=payload, headers=headers)

print(response.json())


# Translating 
import requests

url = "https://google-translate1.p.rapidapi.com/language/translate/v2"

payload = {
	"q": "I love you Subin",
	"target": "ml",
	"source": "en"
}
headers = {
	"content-type": "application/x-www-form-urlencoded",
	"Accept-Encoding": "application/gzip",
	"X-RapidAPI-Key": "fe76a72813mshce74e93488d33c5p155a2ejsndad865e267b7",
	"X-RapidAPI-Host": "google-translate1.p.rapidapi.com"
}

response = requests.post(url, data=payload, headers=headers)

print(response.json())