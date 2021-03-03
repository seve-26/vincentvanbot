import os

IMAGES_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__),'..','raw_data','images'))
PICKLE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__),'..','raw_data','flat_resized_images.pkl'))

# gcloud
BUCKET_NAME='vincent-van-bot-bucket'
BUCKET_PICKLE_PATH='data/flat_resized_images.pkl'
