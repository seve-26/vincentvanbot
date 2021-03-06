import os
from sklearn.neighbors import NearestNeighbors
import joblib
import pandas as pd
from google.cloud import storage
from vincentvanbot.params import BUCKET_NAME, BUCKET_INITIAL_DATASET_FOLDER
from vincentvanbot.preprocessing.utils import get_jpg_link


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

def get_closest_images_indexes(user_input_transformed, nsimilar=3, rm=True):
    """Takes user_input_transformed as np.array. Downloads fitted knn model and related indexes.
    Returns indexes of nsimilar closest images"""
    client = storage.Client().bucket(BUCKET_NAME)
    
    # download model
    local_name = 'model_10000.joblib'
    storage_location = f"predict/{local_name}"
    blob = client.blob(storage_location)
    blob.download_to_filename(local_name)
    print(f"=> {local_name} downloaded from storage")
    model = joblib.load(local_name)
    
    # download indexes
    local_name = 'train_indexes_10000.joblib'
    storage_location = f"predict/{local_name}"
    blob = client.blob(storage_location)
    blob.download_to_filename(local_name)
    print(f"=> {local_name} downloaded from storage")
    indexes = joblib.load(local_name)
    
    if rm:
        os.remove('model_10000.joblib')
        os.remove('train_indexes_10000.joblib')
    
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
    from vincentvanbot.preprocessing.utils import preprocess_image
    # from vincentvanbot.data import get_joblib_data
    path = os.path.join(os.path.dirname(__file__),'..','notebooks','example-input.jpg')
    # print(path)
    user_img = preprocess_image(path,dim=(100,100))
    # train_df = get_joblib_data()

    # train_model(train_df)
    # save_model_to_cloud(rm=True)
    indexes = get_closest_images_indexes(user_img)
    urls = get_info_from_index(indexes)
    print(urls)
