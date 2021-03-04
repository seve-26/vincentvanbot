import cv2
import matplotlib.pyplot as plt
from tensorflow.keras.preprocessing.image import load_img, img_to_array

def resize_image(img,width=420,height=360):
    dim = (width, height)

    return cv2.resize(img, dim, interpolation=cv2.INTER_AREA)

def get_jpg_link(html_link):
    """Tranform the html_link of the image to its respective jpg_link"""
    jpg_link = html_link.replace('html','art', 1).replace('html','jpg')
    
    return jpg_link

def jpg_to_array(jpg_link):
    """Given an image jpg_link, it returns its vectorial representation"""
    img_vector = plt.imread(jpg_link, format='jpg')
    
    return img_vector

def preprocess_image(img, dim=(36,42)):
    """Takes img (either bytes or local path), returns np.array of flat,resized,normalized img"""
    img = load_img('example-input.jpg', target_size=dim)
    img = img_to_array(img)
    img = img.flatten().reshape(1,-1)
    img = img / 255

    return img
