import pandas as pd
from tqdm import tqdm
import os
from os.path import join, dirname
from vincentvanbot.params import IMAGES_PATH, FLAT_IMAGES_DB_PATH_ROOT, BUCKET_NAME
import joblib
from google.cloud import storage
from vincentvanbot.preprocessing import preprocess_image


def create_flat_images_db(start=0, end=100, dim=(100,100)):
    """For each image in path, resizes it to the given dim, transforms it into a flat vector
    and stores in a df. Then dumps it into a joblib file.
    Start and end define which images to consider."""

    if len(os.listdir(IMAGES_PATH)) < start:
        return None
    elif len(os.listdir(IMAGES_PATH)) < end:
        end = len(os.listdir(IMAGES_PATH))
    filelist = sorted(os.listdir(IMAGES_PATH), key=lambda x: int(x.strip('.jpg')))[start:end]

    # stores flat images in a dataframe
    img_db = pd.DataFrame()
    print("Creating joblib database...")
    for filename in tqdm(filelist, bar_format='{l_bar}{bar:30}{r_bar}{bar:-10b}'):
        img = preprocess_image(os.path.join(IMAGES_PATH, filename),dim=dim)
        img_db = img_db.append(pd.DataFrame(img,index=[int(filename.strip('.jpg'))]))

    # save df to joblib file
    path = join(dirname(__file__),'..','raw_data','test_images_db_2','flat_resized_images')
    img_db.sort_index(inplace=True)
    joblib.dump(img_db,'_'.join([path,str(start),str(end-1)])+'.joblib')
    print(f"=> Created file {'_'.join([path,str(start),str(end-1)])+'.joblib'}")


if __name__ == '__main__':
    size = 1000
    offset = 11000
    for i in range(size,1001,size):
        print(f"\nBucket number {i//size}")
        create_flat_images_db(start=offset+i-size,end=offset+i)
