"""This file is used to predict paintings that are closest to the given title of painting."""

import os
import joblib
from google.cloud import storage
import pandas as pd
from vincentvanbot.params import BUCKET_NAME, BUCKET_INITIAL_DATASET_FOLDER
from vincentvanbot.utils import get_jpg_link, download_single_image



def transform_user_input(regex: str, df, case=False):
    """User input is a title of an image as a string. Search title column of original df,
    return index of respective row."""
    matched_row = df[df['TITLE'].str.contains(regex, regex=True, case=case, na=False)][:1]
    user_idx = matched_row.index[0]

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
    from vincentvanbot.fromtitle.data_rec import create_joined_img_df, create_flat_images_db, get_data_locally
    from vincentvanbot.preprocessing import build_pipe_for_categorical

    user_idx = transform_user_input('art', get_data_locally, case=False)
    user_input_transformed = create_joined_img_df(build_pipe_for_categorical, img_db, size=3200).iloc[[user_idx]]
    indexes = get_closest_images_indexes(user_input_transformed)
    urls = get_info_from_index(indexes)
    print(urls)

