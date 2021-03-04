import os
import pandas as pd
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from google.cloud import storage
from termcolor import colored
from vincentvanbot.params import IMAGES_PATH, BUCKET_NAME, PICKLE_PATH_ROOT

from tqdm import tqdm


def create_pickle_db(size=100, path=IMAGES_PATH, dim=(36,42)):
    """For each image in path, resizes it to the given dim, transforms it into a flat vector
    and stores in a df. Then dumps it into a pickle file"""

    # stores flat images in a dataframe
    img_db = pd.DataFrame()
    print("\nCreating pickle database...")
    for filename in tqdm(os.listdir(IMAGES_PATH), bar_format='{l_bar}{bar:30}{r_bar}{bar:-10b}'):
        img = os.path.join(IMAGES_PATH, filename)
        img = load_img(img, target_size=dim)
        img = img_to_array(img)
        img = img.flatten().reshape(1,-1)
        img_db = img_db.append(pd.DataFrame(img,index=[filename.strip('.jpg')]))

    # normalize and save df to pickle file
    img_db.sort_index(inplace=True)
    img_db = img_db / 255
    if size:
        img_db.to_pickle(PICKLE_PATH_ROOT+'_'+str(size)+'.pkl')
    else:
        img_db.to_pickle(PICKLE_PATH_ROOT+'.pkl')


def pickle_upload(size=100, rm=False):
    """Upload pickle file to google cloud"""
    client = storage.Client().bucket(BUCKET_NAME)

    if size:
        PICKLE_PATH = PICKLE_PATH_ROOT+'_'+str(size)+'.pkl'
        local_pickle_name = f'flat_resized_images_{str(size)}.pkl'
    else:
        PICKLE_PATH = PICKLE_PATH_ROOT+'.pkl'
        local_pickle_name = 'flat_resized_images.pkl'
    
    storage_location = f"data/{local_pickle_name}"
    blob = client.blob(storage_location)
    blob.upload_from_filename(PICKLE_PATH)
    print(colored(f"\n=> {local_pickle_name} uploaded to bucket {BUCKET_NAME} inside {storage_location}",
                  "green"))
    if rm:
        os.remove(PICKLE_PATH)


if __name__ == '__main__':
    create_pickle_db()
    pickle_upload(rm=True)