"""This file is used to predict paintings that are closest to the given title of painting."""

import os
import joblib
from google.cloud import storage
import pandas as pd
from vincentvanbot.params import BUCKET_NAME, BUCKET_INITIAL_DATASET_FOLDER, IMAGES_PATH
from vincentvanbot.utils import get_jpg_link, download_single_image
from vincentvanbot.fromtitle.data_rec import create_joined_img_df, get_data_locally
from vincentvanbot.preprocessing import build_pipe_for_categorical
from vincentvanbot.fromtitle.data_rec import create_flat_images_db



def get_index_of_user_input(user_input, get_data_locally, case=False):
    """User input is a title, author and date of an image as a string. Search
    column of original df, return index of respective row."""
    df = get_data_locally(nrows=100_000)
    lst = user_input.split('; ')
    user_idx = df[(df['AUTHOR'] == lst[1]) & (df['TITLE'] == lst[0]) & (df['DATE'] == lst[2])].index[0]

    return user_idx


def get_closest_images_indexes(user_input_transformed, nsimilar=3, rm=True):
    """Takes user_input_transformed as np.array. Downloads fitted knn model and
    related indexes. Returns indexes of nsimilar closest images"""
    client = storage.Client().bucket(BUCKET_NAME)

    # download model
    local_name = 'recommender_model.joblib'
    storage_location = f"predict/recommender_model/{local_name}"
    blob = client.blob(storage_location)
    blob.download_to_filename(local_name)
    print(f"=> {local_name} downloaded from storage")
    model = joblib.load(local_name)

    # download indexes
    local_name = 'rec_train_indexes.joblib'
    storage_location = f"predict/recommender_model/{local_name}"
    blob = client.blob(storage_location)
    blob.download_to_filename(local_name)
    print(f"=> {local_name} downloaded from storage")
    indexes = joblib.load(local_name)

    if rm:
        os.remove('recommender_model.joblib')
        os.remove('rec_train_indexes.joblib')

    index_neighbors = model.kneighbors(user_input_transformed, n_neighbors=nsimilar)[1][0]

    return [int(indexes[i]) for i in list(index_neighbors)]


def get_info_from_index(indexes, all_info=False):
    """From given image indexes, gets initial dataset from gcloud
    and returns respective information (urls, etc.)"""
    client = storage.Client()

    dataset_filename = 'catalog.csv'
    path = f"gs://{BUCKET_NAME}/{BUCKET_INITIAL_DATASET_FOLDER}/{dataset_filename}"

    df = pd.read_csv(path, encoding= 'unicode_escape')
    df['URL'] = df['URL'].map(get_jpg_link)

    urls = [df.iloc[i]['URL'] for i in indexes]

    if not all_info:
        return urls

    # get additional info
    titles = [df.iloc[i]['TITLE'] for i in indexes]
    authors = [df.iloc[i]['AUTHOR'] for i in indexes]

    return urls, titles, authors


if __name__=='__main__':
    user_input = "Allegory; AACHEN, Hans von; 1598"
    user_idx = get_index_of_user_input(user_input, get_data_locally, case=False)
    img_db = create_flat_images_db(size=100, path=IMAGES_PATH, dim=(100,100))
    user_input_transformed = create_joined_img_df(build_pipe_for_categorical, img_db, size=100).iloc[[user_idx]]
    indexes = get_closest_images_indexes(user_input_transformed)
    urls = get_info_from_index(indexes)
    print(urls)

