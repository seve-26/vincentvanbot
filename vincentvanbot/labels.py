from vincentvanbot.params import IMAGES_PATH
from vincentvanbot.utils import get_labels_from_url, get_labels_from_local_path
from os.path import join

from tqdm import tqdm
tqdm.pandas(bar_format='{l_bar}{bar:30}{r_bar}{bar:-10b}')


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