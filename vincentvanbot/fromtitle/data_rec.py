import os
import pandas as pd
import joblib
from vincentvanbot.params import IMAGES_PATH, FLAT_IMAGES_DB_PATH_ROOT, BUCKET_NAME, BUCKET_JOIN_IMAGES_DB_FOLDER, JOIN_IMAGES_DB_PATH_ROOT
from vincentvanbot.utils import download_single_image, get_jpg_link
from vincentvanbot.preprocessing import preprocess_image, build_pipe_for_categorical
from google.cloud import storage
from tqdm import tqdm


def get_data_locally(nrows=10):
    """Return df with initial database and jpg image"""
    path = os.path.join(os.path.dirname(__file__),'..', '..','raw_data','catalog.csv')
    # encode to take care of non-ASCII characters such as 'ö'
    df = pd.read_csv(path, encoding= 'unicode_escape')

    # transform html link to jpg
    df['URL'] = df['URL'].map(get_jpg_link)

    # keep only paintings
    df = df[df['FORM'] == 'painting'].head(nrows)

    return df


def download_images_locally(df):
    """Saves jpg files under raw_data/images based on paintings in df"""
    tqdm.pandas(bar_format='{l_bar}{bar:30}{r_bar}{bar:-10b}')

    if not os.path.exists(IMAGES_PATH):
        os.mkdir(IMAGES_PATH)
    print(f'\nDownloading images to {IMAGES_PATH}...')
    df = df.progress_apply(download_single_image,axis=1)



def create_flat_images_db(size=100, path=IMAGES_PATH, dim=(36,42)):
    """For each image in path, resizes it to the given dim, transforms it into a flat vector
    and stores in a df. Then dumps it into a joblib file"""

    # stores flat images in a dataframe
    img_db = pd.DataFrame()
    for filename in tqdm(os.listdir(IMAGES_PATH)[:size], bar_format='{l_bar}{bar:30}{r_bar}{bar:-10b}'):
        img = preprocess_image(os.path.join(IMAGES_PATH, filename),dim=dim)
        img_db = img_db.append(pd.DataFrame(img,index=[filename.strip('.jpg')]))

    return img_db


def create_joined_img_df(build_pipe_for_categorical, img_db, size=32008):
    img_db.index = [int(i) for i in img_db.index] # transform index from str to int
    pipe = build_pipe_for_categorical()
    array_transformed = pd.DataFrame(pipe.fit_transform(get_data_locally(nrows=32008)))
    join_images_db = pd.DataFrame(img_db.join(array_transformed, lsuffix='_left', rsuffix='_right'))

    # save df to joblib file
    join_images_db.sort_index(inplace=True)
    if size:
       joblib.dump(join_images_db,JOIN_IMAGES_DB_PATH_ROOT+'_'+str(size)+'.joblib')
    else:
       joblib.dump(join_images_db,JOIN_IMAGES_DB_PATH_ROOT+'.joblib')

    return join_images_db



def joined_images_db_upload(size=32008, rm=False):
    """Upload df of flat image vectors as joblib file to google cloud"""
    client = storage.Client().bucket(BUCKET_NAME)

    if size:
        JOIN_IMAGES_DB_PATH = JOIN_IMAGES_DB_PATH_ROOT+'_'+str(size)+'.joblib'
        local_images_db_name = f'joined_resized_images_{str(size)}.joblib'
    else:
        JOIN_IMAGES_DB_PATH = JOIN_IMAGES_DB_PATH_ROOT+'.joblib'
        local_images_db_name = 'joined_resized_images.joblib'

    storage_location = f"data/recommender/{local_images_db_name}"
    blob = client.blob(storage_location)
    blob.upload_from_filename(JOIN_IMAGES_DB_PATH)
    print(f"\n=> {local_images_db_name} uploaded to bucket {BUCKET_NAME} inside {storage_location}")
    if rm:
        os.remove(JOIN_IMAGES_DB_PATH)



def joined_images_db_download(size=32008, source='gcp', rm=True):
    """Downloads df of flat image vectors as joblib file from source and returns it"""
    if size:
        JOIN_IMAGES_DB_PATH = JOIN_IMAGES_DB_PATH_ROOT+'_'+str(size)+'.joblib'
        local_images_db_name = f'joined_resized_images_{str(size)}.joblib'
    else:
        JOIN_IMAGES_DB_PATH = JOIN_IMAGES_DB_PATH_ROOT+'.joblib'
        local_images_db_name = 'joined_resized_images.joblib'

    if source == 'local':
        path = JOIN_IMAGES_DB_PATH
        joined_img_df= joblib.load(path)
    elif source == 'gcp':
        client = storage.Client().bucket(BUCKET_NAME)
        storage_location = f"{BUCKET_JOIN_IMAGES_DB_FOLDER}/{local_images_db_name}"
        blob = client.blob(storage_location)
        blob.download_to_filename(local_images_db_name)
        joined_img_df = joblib.load(local_images_db_name)
        print(f"=> {local_images_db_name} downloaded from storage")
        if rm:
            os.remove(local_images_db_name)

    return joined_img_df


if __name__ == '__main__':
    nrows=32008
    df = get_data_locally(nrows=nrows)
    #download_images_locally(df)
    img_db = create_flat_images_db(size=nrows, path=IMAGES_PATH, dim=(36,42))
    create_joined_img_df(build_pipe_for_categorical, img_db, size=nrows)
    joined_images_db_upload(size=nrows, rm=True)
    joined_img_df = joined_images_db_download(size=nrows, source='gcp')
    print(img_df.shape)
