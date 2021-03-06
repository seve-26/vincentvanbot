"""This file defines the preprocessing pipeline for the recommender system.
Includes different steps to be conducted on different columns of the starting database"""

from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer


def build_pipe():
    """Build preprocessing pipeline for the initial database"""
    cols_to_encode = ["TYPE", "SCHOOL"]
    encoder = OneHotEncoder(sparse = False)

    preproc_pipe = ColumnTransformer([
        ('onehot', encoder, cols_to_encode)
    ], remainder='drop')

    return preproc_pipe


if __name__ == '__main__':
    from vincentvanbot.data import get_data_locally
    df = get_data_locally(nrows=100_000)
    pipe = build_pipe()
    array_transformed = pipe.fit_transform(df)
    print(array_transformed.shape)
