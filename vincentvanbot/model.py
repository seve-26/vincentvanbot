import os
import random
import numpy as np
import pickle
import matplotlib.pyplot
from matplotlib.pyplot import imshow

from sklearn.neighbors import NearestNeighbors
from keras.applications.imagenet_utils import decode_predictions, preprocess_input


#open saved feature vectors with pickle file (Seve)


# take random subsample of image set of size num_images
# num_images = 100

#load image

def load_image(html_link):
    jpg_link = get_jpg_link(html_link)
    img = jpg_to_array(jpg_link)
    #x = np.expand_dims(x, axis=0)
    X = resize_image(img,width=420,height=360)

    return img, X

#plot image

def show_image():
    img, X = load_image(html_link)
    print("shape of x: ", x.shape)
    print("data type: ", x.dtype)

    plt.imshow(img)


# Flatten so we have ndarrays of shape (453600,)
def flatten_images():
    # Read scaled images as numpy arrays
    images = df_transformed['IMAGE'].iloc[:,]
    flat_images = [image.flatten() for image in images]

    return flat_images


# fit the KNN model

model = NearestNeighbors(n_neighbors=k_neighbors)
model.fit(flat_images)
NearestNeighbors(n_neighbors=k_neighbors)

k_neighbors = 3

# Passing new image

# Return the distances and index of the k_neighbors closest points
model.kneighbors(flat_images,n_neighbors=3)

# convert flattened image back to shape and show image



#define a function that show nearest images

