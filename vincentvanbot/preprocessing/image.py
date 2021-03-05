import os
import pandas as pd
from google.cloud import storage
from termcolor import colored
import joblib
from vincentvanbot.params import IMAGES_PATH, BUCKET_NAME, JOBLIB_PATH_ROOT
from vincentvanbot.preprocessing.utils import preprocess_image

from tqdm import tqdm


def create_joblib_db(size=100, path=IMAGES_PATH, dim=(36,42)):
    """For each image in path, resizes it to the given dim, transforms it into a flat vector
    and stores in a df. Then dumps it into a joblib file"""

    # stores flat images in a dataframe
    img_db = pd.DataFrame()
    print("\nCreating joblib database...")
    for filename in tqdm(os.listdir(IMAGES_PATH)[:size], bar_format='{l_bar}{bar:30}{r_bar}{bar:-10b}'):
        img = preprocess_image(os.path.join(IMAGES_PATH, filename),dim=dim)
        img_db = img_db.append(pd.DataFrame(img,index=[filename.strip('.jpg')]))

    # save df to joblib file
    img_db.sort_index(inplace=True)
    if size:
        joblib.dump(img_db,JOBLIB_PATH_ROOT+'_'+str(size)+'.joblib')
    else:
        joblib.dump(img_db,JOBLIB_PATH_ROOT+'.joblib')


def joblib_upload(size=100, rm=False):
    """Upload joblib file to google cloud"""
    client = storage.Client().bucket(BUCKET_NAME)

    if size:
        JOBLIB_PATH = JOBLIB_PATH_ROOT+'_'+str(size)+'.joblib'
        local_joblib_name = f'flat_resized_images_{str(size)}.joblib'
    else:
        JOBLIB_PATH = JOBLIB_PATH_ROOT+'.joblib'
        local_joblib_name = 'flat_resized_images.joblib'
    
    storage_location = f"data/{local_joblib_name}"
    blob = client.blob(storage_location)
    blob.upload_from_filename(JOBLIB_PATH)
    print(colored(f"\n=> {local_joblib_name} uploaded to bucket {BUCKET_NAME} inside {storage_location}",
                  "green"))
    if rm:
        os.remove(JOBLIB_PATH)


if __name__ == '__main__':
    create_joblib_db(size=10)
    # joblib_upload(size=10,rm=True)