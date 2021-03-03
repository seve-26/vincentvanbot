import os
import pandas as pd
from vincentvanbot.preprocessing.utils import get_jpg_link
from vincentvanbot.preprocessing.image import create_pickle_db, pickle_upload
from vincentvanbot.params import IMAGES_PATH, PICKLE_PATH_ROOT, BUCKET_NAME, BUCKET_PICKLE_FOLDER
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

def get_pickle(size=100, source='gcp'):
    """Gets pickle file from source and returns images df"""
    client = storage.Client()
    if size:
        PICKLE_PATH = PICKLE_PATH_ROOT+'_'+str(size)+'.pkl'
        local_pickle_name = f'flat_resized_images_{str(size)}.pkl'
    else:
        PICKLE_PATH = PICKLE_PATH_ROOT+'.pkl'
        local_pickle_name = 'flat_resized_images.pkl'
    
    if source == 'local':
        path = PICKLE_PATH
    elif source == 'gcp':
        path = f"gs://{BUCKET_NAME}/{BUCKET_PICKLE_FOLDER}/{local_pickle_name}"
    img_df = pd.read_pickle(path)

    return img_df


if __name__ == '__main__':
    nrows=100
    df = get_data_locally(nrows=nrows)
    download_images_locally(df)
    create_pickle_db(size=nrows, path=IMAGES_PATH, dim=(36,42))
    pickle_upload(size=nrows, rm=True)
    img_df = get_pickle(size=nrows, source='gcp')
    print(img_df.shape)
