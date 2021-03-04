from sklearn.base import TransformerMixin, BaseEstimator
from vincentvanbot.preprocessing.utils import jpg_to_array

from tqdm import tqdm
tqdm.pandas(bar_format='{l_bar}{bar:30}{r_bar}{bar:-10b}')

class ImageVectorizer(TransformerMixin, BaseEstimator):
    """Receives entire dataset, with jpg_col column having link to the jpg image.
    Returns entire df, with additional IMAGE column containing vector representation of jpg_col"""
    def __init__(self, jpg_col='URL'):
        self.jpg_col = jpg_col
        
    def fit(self, X, y=None):
        return self
    
    def transform(self, X, y=None):
        """X is a df with jpg_col"""
        X_transformed = X.copy()
        print("\nGetting matrix representation of images...")
        X_transformed['IMAGE'] = X[self.jpg_col].progress_map(jpg_to_array)
        return X_transformed
