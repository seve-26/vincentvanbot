"""This file is used to predict paintings that are closest to the given picture."""

import os
import joblib
from google.cloud import storage
import pandas as pd
from vincentvanbot.params import BUCKET_NAME, BUCKET_INITIAL_DATASET_FOLDER
from vincentvanbot.utils import get_jpg_link


def get_closest_images_indexes(user_input_transformed, nsimilar=3, rm=True):
    """Takes user_input_transformed as np.array. Downloads fitted knn model and related indexes.
    Returns indexes of nsimilar closest images"""
    client = storage.Client().bucket(BUCKET_NAME)
    
    # download model
    #local_name = 'model_10000.joblib'
    #storage_location = f"predict/{local_name}"
    #blob = client.blob(storage_location)
    #blob.download_to_filename(local_name)
    #print(f"=> {local_name} downloaded from storage")
    model = joblib.load(os.path.join(os.path.dirname(__file__),'..','model.joblib'))
    
    # download indexes
    #local_name = 'train_indexes_10000.joblib'
    #storage_location = f"predict/{local_name}"
   # blob = client.blob(storage_location)
    #blob.download_to_filename(local_name)
    #print(f"=> {local_name} downloaded from storage")
    indexes = joblib.load(os.path.join(os.path.dirname(__file__),'..','train_indexes.joblib'))
    
    #if rm:
       # os.remove('model.joblib')
       # os.remove('train_indexes.joblib')
    
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
    from vincentvanbot.preprocessing import preprocess_image
    path = os.path.join(os.path.dirname(__file__),'..','..','notebooks','example-input.jpg')
    # print(path)
    user_img = preprocess_image(path,dim=(36,42))
    indexes = get_closest_images_indexes(user_img)
    urls = get_info_from_index(indexes)
    print(urls)
'''Chnage path to local here'''
