import pandas as pd
import numpy as np
from sklearn.cluster import KMeans, AgglomerativeClustering
from scipy.cluster.hierarchy import dendrogram

def fit_model(model, data):
    model.fit(data)

def model_predictions(model, data):
    model.predict(data)

  