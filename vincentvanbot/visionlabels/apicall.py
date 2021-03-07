from google.cloud import vision
import io

LABELS_SELECTION = [
    'Illustration', 'History', 'Drawing', 'Mythology', 'Flower','Stock photography', 'Holy places',
    'Event', 'Artifact', 'Ancient history', 'Wood', 'Vintage clothing', 'Tourist attraction',
    'Sculpture','Font', 'Tree', 'Sky', 'Carving', 'Landscape', 'Metal', 'Middle ages', 'Prophet',
    'Arch', 'Cloud', 'Building'
    ]


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


if __name__ == '__main__':
    # from vincentvanbot.data import get_data_locally
    # df = get_data_locally(nrows=100_000)
    # url_list = list(df.sample(3)['URL'])
    # print([get_labels_from_url(url,25) for url in url_list])

    from os.path import join, dirname
    path = join(dirname(__file__),'..','..','raw_data','images','0.jpg')
    print(get_labels_from_local_path(path,25))
