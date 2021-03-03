import numpy as np
import pandas as pd
import pickle
import matplotlib.pyplot as plt
from sklearn.neighbors import NearestNeighbors


#open feature vectors with pickle file

# take random subsample of images of size num_images
# num_images = 100



def flatten_images():
    """Returns dataframe with a column of flattened image vectors of shape (453600,)"""
    images = df_transformed['IMAGE'].iloc[:,] # Read scaled images as numpy arrays
    flat_images = [image.flatten() for image in images]
    X_flattened = pd.DataFrame(np.vstack(flatten_images()))

    return X_flattened


def train_KNN_model(X_flattened, n_neighbors):
    model = NearestNeighbors(n_neighbors=n_neighbors)
    knn_model = model.fit(X_flattened)
    NearestNeighbors(n_neighbors=n_neighbors)

    return knn_model


def return_closest_images(df, knn_model, X_test):
    """Filters original dataframe with indices and returns reduced dataframe"""
    ind_list = list(knn_model.kneighbors(X_test,n_neighbors=5)[1][0])[1:] # get n closest points, unpack indices to a list
    df_closest_images = df.iloc[ind_list, :] # filter original df with indices. Sort by distance - default??
    #retrieve respective URLS

    return df_closest_images


def get_URL(ind_list, df_transformed):
    pass


# function which gets df with details of closest images (author, titel, date etc)
def img_details():
    # df_transformed.iloc[ind_df.iloc[1]].drop(columns=["URL", "IMAGE"])
    # convert to list or dict
    pass
