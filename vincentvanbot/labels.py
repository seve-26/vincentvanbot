from os.path import join
import io
from google.cloud import vision
from vincentvanbot.params import IMAGES_PATH, LABELS_SELECTION
from tqdm import tqdm

tqdm.pandas(bar_format='{l_bar}{bar:30}{r_bar}{bar:-10b}')


def get_labels_from_url(uri, max_results, proba_threshold=0.6):
    """Takes in uri (i.e. jpg link to an image). Returns dictionary having as keys the identified
    labels, and as values their related proba.
    In particular:
    - only labels with proba > proba_threshold
    - a maximum of max_results different labels
    - only labels manually defined in LABELS_SELECTION"""

    # connect to google vision
    client = vision.ImageAnnotatorClient()
    image = vision.Image()

    # get labels for input uri
    image.source.image_uri = uri
    response = client.label_detection(image=image, max_results=max_results)
    labels = response.label_annotations

    # create dict having as keys all labels, as values their related probas
    # filter dict to only include labels in LABELS_SELECTION and proba > proba_threshold
    labels_dict = {}
    for label in labels:
        if label.description in LABELS_SELECTION and label.score > proba_threshold:
            labels_dict[label.description] = label.score
    
    return labels_dict

def get_labels_from_local_path(path, max_results, proba_threshold=0.6):
    """Takes in path (i.e. path to an image). Returns dictionary having as keys the identified
    labels, and as values their related proba.
    In particular:
    - only labels with proba > proba_threshold
    - a maximum of max_results different labels
    - only labels manually defined in LABELS_SELECTION"""

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
    # filter dict to only include labels in LABELS_SELECTION and proba > proba_threshold
    labels_dict = {}
    for label in labels:
        if label.description in LABELS_SELECTION and label.score > proba_threshold:
            labels_dict[label.description] = label.score
    
    return labels_dict

def get_labels_row(row, max_results, proba_threshold,source):
    if source == 'url':
        labels_dict = get_labels_from_url(
            row['URL'],
            max_results=max_results,
            proba_threshold=proba_threshold
            )
    elif source == 'local':
        path = join(IMAGES_PATH, str(row.name) + '.jpg')
        labels_dict = get_labels_from_local_path(
            path,
            max_results=max_results,
            proba_threshold=proba_threshold
            )
    else:
        raise ValueError("Unknown source for images.")
    
    row.drop(row.index,inplace=True)
    for label, proba in labels_dict.items():
        row[label] = proba
    return row

def get_labels_df(df, max_results, source='url', proba_threshold=0.6):
    """Get labels for each url of the given df."""
    labels_df = df.copy()

    print("\nExtracting labels from Google Vision API...")
    labels_df = labels_df.progress_apply(
        get_labels_row,
        axis=1,
        max_results=max_results,
        proba_threshold=proba_threshold,
        source=source
        )

    labels_df.fillna(0, inplace= True)
    
    return labels_df


if __name__ == '__main__':
    from vincentvanbot.data import get_data_locally
    df = get_data_locally(5)
    labels_df = get_labels_df(df,25, source='local')
    print(labels_df)
    labels_df = get_labels_df(df,25, source='url')
    print(labels_df)
