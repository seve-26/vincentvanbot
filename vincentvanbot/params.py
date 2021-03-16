"""List of hardcoded parameters used in different modules."""

from os.path import abspath, join, dirname

# paths
IMAGES_PATH = abspath(join(dirname(__file__),'..','raw_data','images'))
FLAT_IMAGES_DB_PATH_ROOT = abspath(join(dirname(__file__),'..','raw_data','flat_resized_images'))
JOIN_IMAGES_DB_PATH_ROOT = abspath(join(dirname(__file__),'..', 'raw_data','joined_resized_images'))

# gcloud
BUCKET_NAME='vincent-van-bot-bucket'
BUCKET_FLAT_IMAGES_DB_FOLDER='data'
BUCKET_INITIAL_DATASET_FOLDER = 'data'
BUCKET_JOIN_IMAGES_DB_FOLDER='data/recommender'

# labels
LABELS_SELECTION = [
    'Illustration', 'History', 'Drawing', 'Mythology', 'Flower','Stock photography', 'Holy places',
    'Event', 'Artifact', 'Ancient history', 'Wood', 'Vintage clothing', 'Tourist attraction',
    'Sculpture','Font', 'Tree', 'Sky', 'Carving', 'Landscape', 'Metal', 'Middle ages', 'Prophet',
    'Arch', 'Cloud', 'Building'
    ]
