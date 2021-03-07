import os
import io
import requests
from PIL import Image
from pathlib import Path
import numpy as np
from vincentvanbot.params import IMAGES_PATH, PIL_INTERPOLATION_METHODS


def get_jpg_link(html_link):
    """Tranform the html_link of the image to its respective jpg_link"""
    jpg_link = html_link.replace('html','art', 1).replace('html','jpg')
    
    return jpg_link

def load_img(path,target_size=(100,100), interpolation='nearest'):
    """read the path/image in bytes, and store it in img"""
    if isinstance(path, io.BytesIO):
        img = Image.open(path)
    elif isinstance(path, (Path, bytes, str)):
        if isinstance(path, Path):
            path = str(path.resolve())
        with open(path, 'rb') as f:
            img = Image.open(io.BytesIO(f.read()))
    else:
        raise TypeError('path should be path-like or io.BytesIO'
                        ', not {}'.format(type(path)))
    
    # resize the image
    if target_size is not None:
        width_height_tuple = (target_size[1], target_size[0])
        resample = PIL_INTERPOLATION_METHODS[interpolation]
        img = img.resize(width_height_tuple, resample)
    
    return img

def img_to_array(img, dtype='float32'):
    """Given a PIL image object, returns it's vectorial representation"""
    x = np.asarray(img, dtype=dtype)
    if len(x.shape) == 2:
            x = x.reshape((x.shape[0], x.shape[1], 1))
    return x

def jpg_to_array(jpg_link):
    """Given an image jpg_link, it returns its vectorial representation"""
    img = Image.open(requests.get(test_link, stream=True).raw)
    
    return img_to_array(img)

def download_single_image(df_row):
    response = requests.get(df_row['URL'])
    f = open(os.path.join(IMAGES_PATH,f'{df_row.name}.jpg'), 'wb')
    f.write(response.content)
    f.close()
    return df_row


if __name__ == '__main__':
    from vincentvanbot.data import get_data_locally
    df = get_data_locally(nrows=100_000)
    url_list = list(df.sample(3)['URL'])
    print([get_labels_from_url(url,25) for url in url_list])

    # from os.path import join, dirname
    # path = join(dirname(__file__),'..','raw_data','images','0.jpg')
    # print(get_labels_from_local_path(path,25))
