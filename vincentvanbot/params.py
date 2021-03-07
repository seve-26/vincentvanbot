import os

IMAGES_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__),'..','raw_data','images'))
JOBLIB_PATH_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__),'..','raw_data','flat_resized_images'))

# gcloud
BUCKET_NAME='vincent-van-bot-bucket'
BUCKET_JOBLIB_FOLDER='data'
BUCKET_INITIAL_DATASET_FOLDER = 'data'

# labels
LABELS_SELECTION = [
    'Illustration', 'History', 'Drawing', 'Mythology', 'Flower','Stock photography', 'Holy places',
    'Event', 'Artifact', 'Ancient history', 'Wood', 'Vintage clothing', 'Tourist attraction',
    'Sculpture','Font', 'Tree', 'Sky', 'Carving', 'Landscape', 'Metal', 'Middle ages', 'Prophet',
    'Arch', 'Cloud', 'Building'
    ]
