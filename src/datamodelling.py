import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans, AgglomerativeClustering
from scipy.cluster.hierarchy import dendrogram, linkage

class Clusteringworkflow:

    def __init__(self, algorithm):
        self.algorithm = algorithm

        
    def elbow_method(self, X, max_k = 25):
        if  not isinstance(self.algorithm, KMeans):
            raise ValueError("Elbow method is only for KMeans algorithm.")        

        dispersion = []
        for k in range(2, max_k):
            model = self.algorithm.fit(X)
            dispersion.append(model.inertia_)

        plt.plot(range(1, max_k), dispersion, marker='o')
        plt.xlabel('Number of clusters')
        plt.ylabel('Dispersion (inertia)')
        plt.show()
    
    def fit(self, X):
        dispersion = []
        
        self.algorithm.fit(X)

        return self