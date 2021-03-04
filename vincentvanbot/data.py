import os
import pandas as pd
import joblib
from vincentvanbot.preprocessing.utils import get_jpg_link
from vincentvanbot.preprocessing.image import create_joblib_db, joblib_upload
from vincentvanbot.params import IMAGES_PATH, JOBLIB_PATH_ROOT, BUCKET_NAME, BUCKET_JOBLIB_FOLDER
from vincentvanbot.utils import download_single_image
from google.cloud import storage

from tqdm import tqdm
tqdm.pandas(bar_format='{l_bar}{bar:30}{r_bar}{bar:-10b}')

def get_data_locally(nrows=10):
    """Return df with initial database and jpg image"""
    path = os.path.join(os.path.dirname(__file__),'..','raw_data','catalog.csv')
    # encode to take care of non-ASCII characters such as 'ö'
    df = pd.read_csv(path, encoding= 'unicode_escape')

    # transform html link to jpg
    df['URL'] = df['URL'].map(get_jpg_link)

    # keep only paintings
    df = df[df['FORM'] == 'painting'].head(nrows)

    return df

def download_images_locally(df):
    """Saves jpg files under raw_data/images based on paintings in df"""
    if not os.path.exists(IMAGES_PATH):
        os.mkdir(IMAGES_PATH)
    print(f'\nDownloading images to {IMAGES_PATH}...')
    df = df.progress_apply(download_single_image,axis=1)

def get_joblib_data(size=100, source='gcp', rm=True):
    """Gets joblib file from source and returns images df"""
    # client = storage.Client()
    if size:
        JOBLIB_PATH = JOBLIB_PATH_ROOT+'_'+str(size)+'.joblib'
        local_joblib_name = f'flat_resized_images_{str(size)}.joblib'
    else:
        JOBLIB_PATH = JOBLIB_PATH_ROOT+'.joblib'
        local_joblib_name = 'flat_resized_images.joblib'
    
    if source == 'local':
        path = JOBLIB_PATH
        img_df = joblib.load(path)
    elif source == 'gcp':
        client = storage.Client().bucket(BUCKET_NAME)
        # path = f"gs://{BUCKET_NAME}/{BUCKET_JOBLIB_FOLDER}/{local_joblib_name}"
        storage_location = f"{BUCKET_JOBLIB_FOLDER}/{local_joblib_name}"
        blob = client.blob(storage_location)
        blob.download_to_filename(local_joblib_name)
        img_df = joblib.load(local_joblib_name)
        print(f"=> {local_joblib_name} downloaded from storage")
        if rm:
            os.remove(local_joblib_name)

    return img_df


if __name__ == '__main__':
    nrows=100000
    # df = get_data_locally(nrows=nrows)
    # download_images_locally(df)
    create_joblib_db(size=nrows, path=IMAGES_PATH, dim=(100,100))
    joblib_upload(size=nrows, rm=True)
    # img_df = get_joblib_data(size=nrows, source='gcp')
    # print(img_df.shape)
