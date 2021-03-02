import os
import pandas as pd
from vincentvanbot.preprocessing.utils import get_jpg_link
from vincentvanbot.preprocessing.pipeline import build_pipe
from vincentvanbot.params import IMAGES_PATH
from vincentvanbot.utils import download_single_image

from tqdm import tqdm
tqdm.pandas(bar_format='{l_bar}{bar:30}{r_bar}{bar:-10b}')

def get_data_locally(nrows=10):
    """Return df with initial database and jpg image"""
    path = os.path.join(os.path.dirname(__file__),'..','raw_data','catalog.csv')
    # encode to take care of non-ASCII characters such as 'ö'
    df = pd.read_csv(path, nrows=nrows, encoding= 'unicode_escape')

    # transform html link to jpg
    df['URL'] = df['URL'].map(get_jpg_link)

    # keep only paintings
    df = df[df['FORM'] == 'painting']

    return df

def download_images_locally(df):
    """Saves jpg files under raw_data/images based on aintings in df"""
    if not os.path.exists(IMAGES_PATH):
        os.mkdir(IMAGES_PATH)
    df = df.progress_apply(download_single_image,axis=1)


if __name__ == '__main__':
    df = get_data_locally(nrows=10)
    download_images_locally(df)
    # pipe = build_pipe(dim=(420,360))
    # df_transformed = pipe.fit_transform(df)
    # print(df_transformed.iloc[0]['IMAGE'].shape)    
