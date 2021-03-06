import requests
from PIL import Image
import io
from pathlib import Path
import numpy as np

_PIL_INTERPOLATION_METHODS = {
        'nearest': Image.NEAREST,
        'bilinear': Image.BILINEAR,
        'bicubic': Image.BICUBIC,
    }


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
        resample = _PIL_INTERPOLATION_METHODS[interpolation]
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

def preprocess_image(img, dim=(36,42)):
    """Takes img (either bytes or local path), returns np.array of flat,resized,normalized img"""
    img = load_img(img, target_size=dim)
    img = img_to_array(img)
    img = img.flatten().reshape(1,-1)
    img = img / 255

    return img
