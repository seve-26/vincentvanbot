from sklearn.pipeline import Pipeline
#from model-seve import train_model
from vincentvanbot.preprocessing.featureencoder import transformer


def build_pipe():
    pipe = Pipeline(steps =[
        ('t', transformer),
        ('model', knn_model)
        ])

    return pipe
