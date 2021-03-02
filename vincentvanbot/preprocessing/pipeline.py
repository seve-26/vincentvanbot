from sklearn.pipeline import Pipeline
from vincentvanbot.preprocessing.imagevectorizer import ImageVectorizer
from vincentvanbot.preprocessing.imageresizer import ImageResizer
import cv2

def build_pipe(jpg_col='URL', dim=(420,360), interpolation=cv2.INTER_AREA):
    pipe = Pipeline([
        ('image_vector', ImageVectorizer(jpg_col=jpg_col)),
        ('image_resize', ImageResizer(dim=dim, interpolation=interpolation))
    ])
    
    return pipe