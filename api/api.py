import os
import time
import requests
from dotenv import load_dotenv
from os.path import join, dirname

import joblib
import pandas as pd
from google.cloud import storage
from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware

from api.dummy import dummy_model
from vincentvanbot.utils import get_jpg_link
from vincentvanbot.preprocessing import preprocess_image
from vincentvanbot.labels import get_labels_from_local_path


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
    
    print("Downloading labels pickle from GCP...")
    labels_pickle = load_file_from_gcp('data/labels/labels.pkl')
    labeled_dataframe = pd.read_pickle(labels_pickle)
    
    print("Downloading train indices file from GCP...")
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
def create_upload_file(file: UploadFile = File(...), nsimilar: int = Form(...), rmfirst: bool = Form(...)):
    try:
        if model_type == 'dummy':
            response_to_user = dummy_model(database, file.file, n_similar=nsimilar)
        else:
            # If we're in the recommender part, remove the first result (because it's the same pic as chosen)
            n_request = nsimilar if not rmfirst else nsimilar + 1
            response_to_user = process_user_file(file.file, n_similar=n_request)
            if rmfirst and response_to_user:
                response_to_user.pop(0)
    except BaseException as e:
        print(e)
        response_to_user = []
        
    return response_to_user


# Actual method that will be called with when we push our model to production
def process_user_file(file, n_similar=3):
    
    response = []
    
    # Getting a file from a user
    contents = file.read()
    temp_file_name = str(time.time())
    with open(temp_file_name, 'wb') as user_file:
        user_file.write(contents)
    
    try:
        # Labeling a user pic
        labels_dict = get_labels_from_local_path(temp_file_name, 50, 0.5, manual=False)
        labels_list = [label for label in labels_dict.keys() if label in labeled_dataframe.columns]            

        # Sequence of bytes/file is passed to preprocessor {preproc.transform(X)}. OUTPUT: Vector of size matching the KNN model.
        image_processed = preprocess_image(temp_file_name)

        # n_similar closest neighbors are returned {knn_model} = their indice
        index_neighbors = knn_model.kneighbors(image_processed, n_neighbors = n_similar * 2)[1][0]
        base_indices = [int(train_indices[i]) for i in list(index_neighbors)]
        
        # Getting the knn rank
        labeled_knn_filtered = labeled_dataframe.loc[base_indices, :]
        labeled_knn_filtered['KNN_RANK'] = labeled_knn_filtered.reset_index().index.values + 1
        indices_with_knn_rank = labeled_knn_filtered[['KNN_RANK']]
        
        # Getting the labels rank
        labeled_knn_filtered = labeled_knn_filtered[labels_list]
        labeled_knn_filtered['SUM'] = labeled_knn_filtered.sum(axis=1)
        labeled_knn_filtered = labeled_knn_filtered.sort_values(by=['SUM'], ascending = False)
        labeled_knn_filtered['LABELS_RANK'] = labeled_knn_filtered.reset_index().index.values + 1
        indices_with_labels_rank = labeled_knn_filtered[['LABELS_RANK']]
        
        # Calculating the combined rank
        knn_with_labels = indices_with_knn_rank.join(indices_with_labels_rank, how='inner')
        knn_with_labels['RANK_SUM'] = knn_with_labels['KNN_RANK'] + knn_with_labels['LABELS_RANK']
        knn_with_labels = knn_with_labels.sort_values(by=['RANK_SUM'], ascending = True)
        
        results = list(knn_with_labels.index.values)[:n_similar]

        # Send response back. Response structure: [ n_similar pieces of {img_url, html_url, author, title, created, museum}]
        for ind in results:
            response_item = dict (img_url = get_jpg_link(database.at[ind, 'URL']), html_url = database.at[ind, 'URL'], \
                author = database.at[ind, 'AUTHOR'], title = database.at[ind, 'TITLE'], \
                created = database.at[ind, 'DATE'],  museum =  database.at[ind, 'LOCATION'])

            response.append(response_item)
            
    except BaseException as e:
        print(e)
    finally:
        # Deleting user pic
        os.remove(temp_file_name)

    return response
