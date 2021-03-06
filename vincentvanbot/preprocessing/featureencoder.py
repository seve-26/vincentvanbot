import pandas as pd
from vincentvanbot.data import get_data_locally
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer


def transformer(df):
    """df is original dataframe"""
    features_X = df[["TYPE", "SCHOOL"]]
    enc = [('onehot', OneHotEncoder(sparse = False), [0, 1])]
    transformer = ColumnTransformer(transformers=enc)

    return transformer


def get_col_transformed(transformer, df):
    """Return dataframe with encoded features TYPE and SCHOOL"""
    col_encoded = transformer(df).fit_transform(df[["TYPE", "SCHOOL"]])

    return pd.DataFrame(col_encoded)



