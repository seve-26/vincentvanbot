import os

IMAGES_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__),'..','raw_data','images'))
PICKLE_PATH_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__),'..','raw_data','flat_resized_images'))

# gcloud
BUCKET_NAME='vincent-van-bot-bucket'
BUCKET_PICKLE_FOLDER='data'
BUCKET_INITIAL_DATASET_FOLDER = 'data'
