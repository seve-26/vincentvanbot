from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from google.cloud import vision
import requests
import os
from os.path import join, dirname
from dotenv import load_dotenv

env_path = join(dirname(__file__),'.env')
load_dotenv(dotenv_path=env_path)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

@app.get("/")
def index():
    return {"greeting": "Hello world"}

@app.post("/uploadfile/")
def create_upload_file(file: UploadFile = File(...)):
    
    urls = dummy_model(file.file)
    return urls


def dummy_model(file):
    
    GOOGLE_SEARCH_API_LINK='https://customsearch.googleapis.com/customsearch/v1'
    api_key = os.getenv('API_KEY')
    cx_key = os.getenv('CX_KEY')
    client = vision.ImageAnnotatorClient()
    
    contents = file.read()
    
    image = vision.Image(content=contents)
    response = client.label_detection(image=image)
    labels = response.label_annotations
    descs = [label.description for label in labels]
    
    params = dict(key=api_key, cx=cx_key, q=' '.join(descs[0:5]), searchType='image')
    resp = requests.get(GOOGLE_SEARCH_API_LINK, params).json()
    
    urls = []
    for i in range(3):
        urls.append(resp['items'][i]['link'])
        
    return urls