"""This file includes different functions related to the preprocessing steps."""

from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from vincentvanbot.utils import load_img, img_to_array


def build_pipe_for_categorical():
    """Builds preprocessing pipeline for categorical variables of the initial database"""
    cols_to_encode = ["TYPE", "SCHOOL"]
    encoder = OneHotEncoder(sparse = False)

    preproc_pipe = ColumnTransformer([
        ('onehot', encoder, cols_to_encode)
    ], remainder='drop')

    return preproc_pipe

def preprocess_image(img, dim=(100,100)):
    """Takes img (either bytes or local path), returns np.array of flat,resized,normalized img"""
    img = load_img(img, target_size=dim)
    img = img_to_array(img)
    img = img.flatten().reshape(1,-1)
    img = img / 255

    return img


if __name__ == '__main__':
    from vincentvanbot.data import get_data_locally
    df = get_data_locally(nrows=100_000)
    pipe = build_pipe_for_categorical()
    array_transformed = pipe.fit_transform(df)
    print(array_transformed.shape)
