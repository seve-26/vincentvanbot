import os
import time
import requests
from dotenv import load_dotenv
from os.path import join, dirname

import joblib
import pandas as pd
from google.cloud import storage
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware

from api.dummy import dummy_model
from vincentvanbot.utils import get_jpg_link
from vincentvanbot.preprocessing import preprocess_image


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

# Loading models to memory
catalogue = load_file_from_gcp('data/catalog.csv')

if model_type != 'dummy':
    print("Downloading KNN model from GCP...")
    knn_model_file = load_file_from_gcp('predict/model.joblib')
    print("Loading the KNN model to memory...")
    knn_model = joblib.load(knn_model_file)
    print("KNN model is downloaded and ready")

    train_indices_file = load_file_from_gcp('predict/train_indexes.joblib')
    train_indices = joblib.load(train_indices_file)


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
    try:
        response_to_user = dummy_model(database, file.file) if model_type == 'dummy' else process_user_file(file.file)
    except BaseException as e:
        print(e)
        response_to_user = []
        
    return response_to_user


# Actual method that will be called with when we push our model to production
def process_user_file(file, n_similar=3):

    # Getting a file from a user
    contents = file.read()
    temp_file_name = str(time.time())
    with open(temp_file_name, 'wb') as user_file:
        user_file.write(contents)

    # Sequence of bytes/file is passed to preprocessor {preproc.transform(X)}. OUTPUT: Vector of size matching the KNN model.
    image_processed = preprocess_image(temp_file_name)

    # n_similar closest neighbors are returned {knn_model} = their indice
    index_neighbors = knn_model.kneighbors(image_processed, n_neighbors=n_similar)[1][0]
    base_indices = [int(train_indices[i]) for i in list(index_neighbors)]

    # Send response back. Response structure: [ n_similar pieces of {img_url, html_url, author, title, created, museum}]
    response = []

    for ind in base_indices:
        response_item = dict (img_url = get_jpg_link(database.at[ind, 'URL']), html_url = database.at[ind, 'URL'], \
            author = database.at[ind, 'AUTHOR'], title = database.at[ind, 'TITLE'], \
            created = database.at[ind, 'DATE'],  museum =  database.at[ind, 'LOCATION'])

        response.append(response_item)

    # Deleting user pic  
    os.remove(temp_file_name)

    return response
