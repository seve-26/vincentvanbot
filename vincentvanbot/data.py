import os
import pandas as pd
from vincentvanbot.preprocessing.utils import get_jpg_link
from vincentvanbot.preprocessing.pipeline import build_pipe


def get_data_locally(nrows=10):
    """Return df with initial database and jpg image"""
    path = os.path.join(os.path.dirname(__file__),'..','raw_data','catalog.csv')
    # encode to take care of non-ASCII characters such as 'ö'
    df = pd.read_csv(path, nrows=nrows, encoding= 'unicode_escape')

    # transform html link to jpg
    df['URL'] = df['URL'].map(get_jpg_link)

    return df

if __name__ == '__main__':
    df = get_data_locally()
    pipe = build_pipe(dim=(420,360))
    df_transformed = pipe.fit_transform(df)
    print(df_transformed.iloc[0]['IMAGE'].shape)
    
