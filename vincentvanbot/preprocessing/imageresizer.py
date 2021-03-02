from sklearn.base import TransformerMixin, BaseEstimator
from vincentvanbot.preprocessing.utils import resize_image
import cv2

from tqdm import tqdm
tqdm.pandas(bar_format='{l_bar}{bar:30}{r_bar}{bar:-10b}')

class ImageResizer(TransformerMixin, BaseEstimator):
    """Receives entire dataset, with also IMAGE column, containing vector representation
    of the image from the URL. Returns the entire df, with IMAGE vector resized accoring to dim"""
    def __init__(self, dim=(420,360), interpolation=cv2.INTER_AREA):
        self.dim = dim
        self.interpolation = interpolation
        
    def fit(self, X, y=None):
        return self
    
    def transform(self, X, y=None):
        """X is a pd.DataFrame with IMAGE column having vector representation of the image"""
        X_transformed = X.copy()
        print("\nResizing images...")
        X_transformed['IMAGE'] = X['IMAGE'].progress_map(resize_image)
        return X_transformed
