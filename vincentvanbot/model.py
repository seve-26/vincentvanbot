import numpy as np
import pandas as pd
import pickle
import matplotlib.pyplot as plt
#import model


#open feature vectors with pickle file

# take random subsample of images of size num_images
# num_images = 100


def flatten_images():
    """Returns dataframe with a column of flattened image vectors of shape (453600,)"""
    images = df_transformed['IMAGE'].iloc[:,] # Read scaled images as numpy arrays
    flat_images = [image.flatten() for image in images]
    X_flattened = pd.DataFrame(np.vstack(flatten_images()))

    return X_flattened


def get_distance(model, X_flattened):
    """Return the distances of the k_neighbors closest points"""
    distance_lst = list(model.kneighbors(X_flattened,n_neighbors=5)[0][0])
    distance_df = pd.DataFrame(distance_lst, columns=['distance'])

    return distance_df


def get_indexes(model, X_flattened):
    """Return the index of the k_neighbors closest point"""
    index_list = list(model.kneighbors(X_flattened,n_neighbors=5)[1][0])
    index_df = pd.DataFrame(index_list, columns=['index'])

    return index_df


# function which gets df with details of closest images (author, titel, date etc)
def img_details():
    # df_transformed.iloc[ind_df.iloc[1]].drop(columns=["URL", "IMAGE"])
    # convert to list or dict
    pass
