from sklearn.neighbors import NearestNeighbors
import joblib
from os.path import abspath, join, dirname 


def train_model(df_transformed):
    """Takes preprocessed train data as df. Returns fitted KNN model 
    and train data image indexes (used then to refer back to initial database).
    Saves locally model and indexes."""
    knn_model = NearestNeighbors().fit(df_transformed)
    
    joblib.dump(knn_model,join(dirname(__file__),'..','..','raw_data','model.joblib'))
    joblib.dump(df_transformed.index,'train_indexes.joblib')
    print("=> model fitted and files created")

