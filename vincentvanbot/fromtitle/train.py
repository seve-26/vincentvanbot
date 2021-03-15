### WORK IN PROGRESS! Currently not used by the api
""""""

import os
from sklearn.neighbors import NearestNeighbors
import joblib
from google.cloud import storage
from vincentvanbot.params import BUCKET_NAME


def train_model(joined_images_df):
    """Takes preprocessed train data (pixel and enconded features) as df.
    Returns fitted KNN model and train data image indexes (used then to refer
    back to initial database). Saves locally model and indexes."""
    knn_model = NearestNeighbors().fit(joined_images_df)

    joblib.dump(knn_model,'recommender_model.joblib')
    joblib.dump(joined_images_df.index,'rec_train_indexes.joblib')


def save_model_to_cloud(rm=False):
    """Uploads fitted model and related indexes to GCloud."""
    client = storage.Client().bucket(BUCKET_NAME)

    for filename in ['recommender_model.joblib','rec_train_indexes.joblib']:
        storage_location = f"predict/recommender_model/{filename}"
        blob = client.blob(storage_location)
        blob.upload_from_filename(filename)
        print(f"=> {filename} uploaded to bucket {BUCKET_NAME} inside {storage_location}")
    if rm:
        os.remove('recommender_model.joblib')
        os.remove('rec_train_indexes.joblib')


if __name__=='__main__':
    nrows=100_000
    from vincentvanbot.fromtitle.data_rec import joined_images_db_download
    train_df = joined_images_db_download(size=nrows, source='local', rm=False)
    train_model(train_df)
    save_model_to_cloud(rm=True)
