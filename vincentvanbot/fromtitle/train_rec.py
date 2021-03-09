import os
from sklearn.neighbors import NearestNeighbors
import joblib
from google.cloud import storage
from vincentvanbot.params import BUCKET_NAME



def train_model(create_joined_img_df): # from data/create_joined_img_df
    """Takes preprocessed train data (pixel and enconded deatures) as df.
    Returns fitted KNN model and train data image indexes (used then to refer back to initial database).
    Saves locally model and indexes."""
    join_images_db = create_joined_img_df
    knn_model = NearestNeighbors().fit(join_images_db)

    joblib.dump(knn_model,'recommender_model.joblib')
    joblib.dump(df_concat.index,'train_indexes.joblib')


def save_model_to_cloud(rm=False):
    """Uploads fitted model and related indexes to GCloud."""
    client = storage.Client().bucket(BUCKET_NAME)

    for filename in ['recommender_model.joblib','train_indexes.joblib']:
        storage_location = f"predict/recommender_model/{filename}"
        blob = client.blob(storage_location)
        blob.upload_from_filename(filename)
        print(f"=> {filename} uploaded to bucket {BUCKET_NAME} inside {storage_location}")
    if rm:
        os.remove('recommender_model.joblib')
        os.remove('train_indexes.joblib')


if __name__=='__main__':
    from vincentvanbot.data import flat_images_db_download
    train_df = flat_images_db_download()
    train_model(train_df)
    save_model_to_cloud(rm=True)
