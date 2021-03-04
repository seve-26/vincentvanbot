from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from google.cloud import vision, storage
import requests
import os
from os.path import join, dirname
from dotenv import load_dotenv
import pandas as pd
import time

# Uploading env variable
env_path = join(dirname(__file__),'.env')
load_dotenv(dotenv_path=env_path)
model_type = os.getenv('MODEL_TYPE')
PROJECT_ID = 'vincent-van-bot'
BUCKET_NAME = 'vincent-van-bot-bucket'

# Initiating load function
def load_file_from_gcp(file_path):
    storage_client = storage.Client(PROJECT_ID)
    bucket = storage_client.get_bucket(BUCKET_NAME)
    blob = bucket.blob(file_path)
    
    filename = file_path.split("/")[1]
    blob.download_to_filename(filename)
    
    return filename

# Loading models
catalogue = load_file_from_gcp('data/catalog.csv')
#image_preprocessor = load_model_from_gcp('predict/image_preprocessing.joblib')
#knn_model = load_model_from_gcp('predict/model.joblib')

# Starting API server and uploading our catalogue to memory
app = FastAPI()

database = pd.read_csv(catalogue, encoding='unicode_escape')
database = database[database['FORM'] == 'painting']

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


# To check if server is up and running
@app.get("/")
def index():
    return {"greeting": "Hello world"}


# Receives the file from the frontend or Telegram bot
@app.post("/uploadfile/")
def create_upload_file(file: UploadFile = File(...)):
    response_to_user = dummy_model(file.file) if model_type == 'dummy' else process_user_file(file.file)
    return response_to_user


# Actual method that will be called with when we push our model to production
def process_user_file(file, n_similar=3):
    # PSEUDOCODE:
    # 1. Get file from a user
    contents = file.read()
    temp_file_name = str(time.time())
    with open(temp_file_name, 'wb') as user_file:
        user_file.write(contents)
         
    # 2. Preprossor function is downloaded from a joblib/pickle file {load_model_from_gcp...}. OUTPUT: Preprocessor function in a variable
    # image_processed = image_preprocessor(temp_file_name)
    
    # 3. Sequence of bytes/file is passed to preprocessor {preproc.transform(X)}. OUTPUT: Vector of size matching the KNN model.
    # 4. Fitted KNN model is downloaded from a joblib/pickle file {load_model_from_gcp...}. OUTPUT: KNN model in a variable
    # 5. n_similar closest neighbors are returned {knn_model} = their indices
    # 6. Take the rows by indices, get HTML URLs
    # 7. Convert HTML URLs to JPG urls.
    # 8. Send response back. Response structure: [ n_similar pieces of {img_url, html_url, author, title, created, museum}]
    pass


# Being used until we make our own model work
def dummy_model(file, n_similar=3):
    
    GOOGLE_SEARCH_API_LINK='https://customsearch.googleapis.com/customsearch/v1'
    api_key = os.getenv('API_KEY')
    cx_key = os.getenv('CX_KEY')
    client = vision.ImageAnnotatorClient()
    
    contents = file.read()
    
    image = vision.Image(content=contents)
    response = client.label_detection(image=image)
    labels = response.label_annotations
    descs = [label.description for label in labels]
    
    params = dict(key=api_key, cx=cx_key, q=' '.join(descs[0:2]), \
        siteSearch='https://www.wga.hu', siteSearchFilter='i', searchType='image', \
            exactTerms='searchable fine arts image database')
    
    resp = requests.get(GOOGLE_SEARCH_API_LINK, params).json()
    if resp['searchInformation']['totalResults'] == '0': return []
    
    response = []
    for item in resp['items']:
        link = item['link']
        if '/art/' not in link:
            continue

        context_link = item['image']['contextLink']
        if context_link not in set(database['URL']):
            continue
        
        response_item = dict (img_url = link, html_url = context_link, \
                              author = database.loc[database['URL'] == context_link, 'AUTHOR'].values[0], \
                              title = database.loc[database['URL'] == context_link, 'TITLE'].values[0], \
                              created = database.loc[database['URL'] == context_link, 'DATE'].values[0], \
                              museum = database.loc[database['URL'] == context_link, 'LOCATION'].values[0])

        response.append(response_item)
        
        if len(response) == n_similar:
            break
    
    return response



    