import os
import pandas as pd
import joblib
from vincentvanbot.params import IMAGES_PATH, FLAT_IMAGES_DB_PATH_ROOT, BUCKET_NAME, BUCKET_JOIN_IMAGES_DB_FOLDER, JOIN_IMAGES_DB_PATH_ROOT
from vincentvanbot.utils import download_single_image, get_jpg_link
from vincentvanbot.preprocessing import preprocess_image, build_pipe_for_categorical
from google.cloud import storage
from tqdm import tqdm


def create_joined_img_df(size=100_000):
    img_db = create_flat_images_db(size=size, path=IMAGES_PATH, dim=(36,42))
    img_db.index = [int(i) for i in img_db.index] # transform index from str to int

    df = get_data_locally(nrows=100_000)
    pipe = build_pipe_for_categorical()
    array_transformed = pipe.fit_transform(df)
    column_name = pipe.get_feature_names()
    df_transformed = pd.DataFrame(array_transformed, columns=column_name, index=df.index)
    join_images_db = pd.DataFrame(img_db.join(df_transformed, lsuffix='_left', rsuffix='_right'))

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
    nrows=1000
    df = get_data_locally(nrows=nrows)
    #download_images_locally(df)
    #img_db = create_flat_images_db(size=nrows, path=IMAGES_PATH, dim=(36,42))
    create_joined_img_df(size=nrows)
    joined_images_db_upload(size=nrows, rm=True)
    joined_img_df = joined_images_db_download(size=nrows, source='gcp')
    print(joined_img_df.shape)
