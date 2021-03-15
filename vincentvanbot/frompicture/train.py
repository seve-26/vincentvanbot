"""This file is used to train KNN model based on paintings from database, and to upload
the fitted model to Google Cloud."""

import os
from sklearn.neighbors import NearestNeighbors
import joblib
from google.cloud import storage
from vincentvanbot.params import BUCKET_NAME


def train_model(df_transformed):
    """Takes preprocessed train data as df. Returns fitted KNN model 
    and train data image indexes (used then to refer back to initial database).
    Saves locally model and indexes."""
    knn_model = NearestNeighbors().fit(df_transformed)
    
    joblib.dump(knn_model,'model.joblib')
    joblib.dump(df_transformed.index,'train_indexes.joblib')

def save_model_to_cloud(rm=False):
    """Uploads fitted model and related indexes to GCloud."""
    client = storage.Client().bucket(BUCKET_NAME)
    
    for filename in ['model.joblib','train_indexes.joblib']:
        storage_location = f"predict/{filename}"
        blob = client.blob(storage_location)
        blob.upload_from_filename(filename)
        print(f"=> {filename} uploaded to bucket {BUCKET_NAME} inside {storage_location}")
    if rm:
        os.remove('model.joblib')
        os.remove('train_indexes.joblib')


if __name__=='__main__':
    from vincentvanbot.data import flat_images_db_download
    train_df = flat_images_db_download()
    train_model(train_df)
    save_model_to_cloud(rm=True)
