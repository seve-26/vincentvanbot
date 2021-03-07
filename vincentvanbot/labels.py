import os
from os.path import join
import io
from google.cloud import vision, storage
from vincentvanbot.params import IMAGES_PATH, LABELS_SELECTION, BUCKET_NAME
from tqdm import tqdm

tqdm.pandas(bar_format='{l_bar}{bar:30}{r_bar}{bar:-10b}')


def get_labels_from_url(uri, max_results, proba_threshold=0.6, manual=True):
    """Takes in uri (i.e. jpg link to an image). Returns dictionary having as keys the identified
    labels, and as values their related proba.
    In particular:
    - only labels with proba > proba_threshold
    - a maximum of max_results different labels
    - only labels manually defined in LABELS_SELECTION (if manual)"""

    # connect to google vision
    client = vision.ImageAnnotatorClient()
    image = vision.Image()

    # get labels for input uri
    image.source.image_uri = uri
    response = client.label_detection(image=image, max_results=max_results)
    labels = response.label_annotations

    # create dict having as keys all labels, as values their related probas
    # filter dict to only include labels where proba > proba_threshold
    # filter dict to only include labels in LABELS_SELECTION if manual
    labels_dict = {}
    for label in labels:
        if label.score > proba_threshold:
            if manual:
                if label.description in LABELS_SELECTION:
                    labels_dict[label.description] = label.score
            else:
                labels_dict[label.description] = label.score
    
    return labels_dict

def get_labels_from_local_path(path, max_results, proba_threshold=0.6, manual=True):
    """Takes in path (i.e. path to an image). Returns dictionary having as keys the identified
    labels, and as values their related proba.
    In particular:
    - only labels with proba > proba_threshold
    - a maximum of max_results different labels
    - only labels manually defined in LABELS_SELECTION (if manual)"""

    # open image file
    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    # connect to google vision
    client = vision.ImageAnnotatorClient()
    image = vision.Image(content=content)

    # get labels for input path
    response = client.label_detection(image=image, max_results=max_results)
    labels = response.label_annotations

    # create dict having as keys all labels, as values their related probas
    # filter dict to only include labels where proba > proba_threshold
    # filter dict to only include labels in LABELS_SELECTION if manual
    labels_dict = {}
    for label in labels:
        if label.score > proba_threshold:
            if manual:
                if label.description in LABELS_SELECTION:
                    labels_dict[label.description] = label.score
            else:
                labels_dict[label.description] = label.score
    
    return labels_dict

def get_labels_row(row, max_results, proba_threshold, manual, source):
    if source == 'url':
        labels_dict = get_labels_from_url(
            row['URL'],
            max_results=max_results,
            proba_threshold=proba_threshold,
            manual=manual
            )
    elif source == 'local':
        path = join(IMAGES_PATH, str(row.name) + '.jpg')
        labels_dict = get_labels_from_local_path(
            path,
            max_results=max_results,
            proba_threshold=proba_threshold,
            manual=manual
            )
    else:
        raise ValueError("Unknown source for images.")
    
    row.drop(row.index,inplace=True)
    for label, proba in labels_dict.items():
        row[label] = proba
    return row

def get_labels_df(df, max_results, source='url', proba_threshold=0.6, manual=True):
    """Get labels for each url of the given df."""
    labels_df = df.copy()

    print("\nExtracting labels from Google Vision API...")
    labels_df = labels_df.progress_apply(
        get_labels_row,
        axis=1,
        max_results=max_results,
        proba_threshold=proba_threshold,
        source=source,
        manual=manual
        )

    labels_df.fillna(0, inplace= True)
    
    return labels_df

def labels_df_upload(labels_df, rm=True):
    """Uploads df of labeled dataset to google cloud"""
    client = storage.Client().bucket(BUCKET_NAME)

    labels_df_name = f'labels_df_seve.csv'
    labels_df.to_csv(labels_df_name)

    storage_location = f"data/{labels_df_name}"
    blob = client.blob(storage_location)
    blob.upload_from_filename(labels_df_name)
    print(f"\n=> {labels_df_name} uploaded to bucket {BUCKET_NAME} inside {storage_location}")

    if rm:
        os.remove(labels_df_name)


if __name__ == '__main__':
    from vincentvanbot.data import get_data_locally
    df = get_data_locally(100_000)
    labels_df = get_labels_df(df,100_000, source='local', manual=False)
    # print(labels_df)
    labels_df_upload(labels_df)
