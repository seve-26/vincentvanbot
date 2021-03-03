import numpy as np
import pandas as pd
import pickle
import matplotlib.pyplot as plt
from sklearn.neighbors import NearestNeighbors

from vincentvanbot.data import get_data_locally
from vincentvanbot.preprocessing.pipeline import build_pipe



def flatten_images(df_transformed):
    """Returns dataframe with a column of flattened image vectors of shape (453600,)"""
    images = df_transformed['IMAGE'].iloc[:,] # Read scaled images as numpy arrays
    flat_images = [image.flatten() for image in images]
    X_flattened = pd.DataFrame(np.vstack(flatten_images(df_transformed)))

    return X_flattened


def train_KNN_model(X_flattened, n_neighbors):
    model = NearestNeighbors(n_neighbors=n_neighbors)
    knn_model = model.fit(X_flattened)
    NearestNeighbors(n_neighbors=n_neighbors)

    return knn_model


def return_closest_images(df_transformed, knn_model, X_test):
    """Filters original dataframe with indices and returns reduced dataframe"""
    ind_list = list(knn_model.kneighbors(X_test,n_neighbors=5)[1][0])[1:] # get n closest points, unpack indices to a list
    df_closest_images = df.iloc[ind_list, :] # filter original df with indices

    return df_closest_images


def get_URL(ind_list, df_transformed):
    """Returns list of URLs of closest images"""
    lst_URL = []
    for i in range(len(ind_list)):
        closest_img = df_transformed.iloc[i] # original dataframe
        img_URL = closest_img[6]
        lst_URL.append(img_URL)

    return lst_URL


def img_details():
    """function which gets df with details of closest images (author, titel, date etc)"""
    # df_transformed.iloc[ind_df.iloc[1]].drop(columns=["URL", "IMAGE"])
    # convert to list or dict
    pass

