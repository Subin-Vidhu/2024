import cv2
import os
import requests
from fpdf import FPDF
from flask import Flask,request,render_template

API_KEY = "YOUR-API-KEY-HERE"
API_HOST = "youtube-media-downloader.p.rapidapi.com"
video_details_url = "https://youtube-media-downloader.p.rapidapi.com/v2/video/details"
subtitle_details_url = "https://youtube-media-downloader.p.rapidapi.com/v2/video/subtitles"

app = Flask(__name__)

def get_video_id(videoURL):
    # split YouTube URL by '/' so we can get its ID
    videoID = str(videoURL).split('/')
    # get the last part of the list which is the ID
    videoID = videoID[-1]
    if '=' in videoID:
        videoID = videoID.split('=')[-1]
    if not videoID[0].isalpha():
        videoID = videoID[1:]
    print(videoID)
    return videoID

def get_video_detail(videoID):
    # access the API
    url = video_details_url
    headers = {
        'x-rapidapi-host': API_HOST,
        'x-rapidapi-key': API_KEY
    }
    # send a get request to the API 
    querystring = {"videoId": videoID}
    response = requests.request("GET", url, headers=headers, params=querystring)
    # conver the response to json format
    json_response = response.json()
    # obtain the subtitle url (in XML format)
    try:
        subtitleURL = json_response['subtitles']['items'][0]['url']
        print(subtitleURL)
        return subtitleURL
    except:
        print('No subtitles in this video...')
        return None
        
def get_subtitle_text(subtitleURL):
    # access the API
    url = subtitle_details_url
    headers = {
        'x-rapidapi-host': API_HOST,
        'x-rapidapi-key': API_KEY
    }
    # send a get subtitle text request to the API 
    querystring = {"subtitleUrl": subtitleURL}
    response = requests.request("GET", url, headers=headers, params=querystring)
    # return the text response
    return response.text

def Convert_And_Download_Subtitle(text):
    # create a pdf object
    pdf = FPDF()
    # add a page to the pdf
    pdf.add_page()
    # set font and size of the font
    pdf.set_font("Arial", size=12)
    # for evey line in the text
    for line in text.split('\n'):
        # add the line to the pdf
        pdf.cell(200, 5, txt=line, ln=1)
    
    # save and download the pdf with a custom file name
    pdf.output("subtitle.pdf")
    print('Subtitles PDF Saved!!!')

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/downloadsubs',methods=['POST'])
def downloadsubs():
    if request.method == 'POST':
        videoURL = request.form['yturl']
        videoID = get_video_id(videoURL)
        subtitleURL = get_video_detail(videoID)
        if subtitleURL:
            subtitles = get_subtitle_text(subtitleURL)
            Convert_And_Download_Subtitle(subtitles)

    return render_template('home.html',url=subtitleURL,subtitletext=subtitles)


if __name__ == '__main__':
    app.run(debug=True)