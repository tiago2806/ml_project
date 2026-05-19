import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans, AgglomerativeClustering
from scipy.cluster.hierarchy import dendrogram, linkage
from sklearn.metrics import silhouette_score
from utils import (
    plot_dendrogram
)

class Clusteringworkflow:

    def __init__(self, algorithm):
        self.algorithm = algorithm

        
    def find_optimal_k(self, data_scaled, K_range):
        if isinstance(self.algorithm, KMeans):
            dispersion = []
            for k in range(2, K_range):
                model_kmeans = KMeans(n_clusters=k, random_state=0).fit(data_scaled) #experimental fit
                dispersion.append(model_kmeans.inertia_)

            plt.plot(range(2, K_range), dispersion, marker='o')
            plt.xlabel('Number of clusters')
            plt.ylabel('Dispersion (inertia)')
            plt.show()

        elif isinstance(self.algorithm, AgglomerativeClustering):
            model_hierarchical = self.algorithm
            fig, ax = plt.subplots()
            plt.title("Hierarchical Clustering Dendrogram")
            # plot the top three levels of the dendrogram
            plot_dendrogram(model_hierarchical, truncate_mode="level", p=50)
            plt.axhline(y = 50, color = 'r', linestyle = '-')
            plt.show() 

        else:
            raise ValueError("This is only for KMeans or AgglomerativeClustering")
        
    def silhouette(self, data_scaled, K_range):
        silhouette_scores = []

        for k in K_range:
            if isinstance(self.algorithm, KMeans):
                model_kmeans = KMeans(n_clusters=k, random_state=0).fit(data_scaled)
                labels = model_kmeans.labels_
            elif isinstance(self.algorithm, AgglomerativeClustering):
                model_hierarchical = AgglomerativeClustering(n_clusters=k).fit(data_scaled)
                labels = model_hierarchical.labels_
            else:
                raise ValueError("Silhouette only works for KMeans or AgglomerativeClustering")
            
            silhouette_scores.append(silhouette_score(data_scaled, labels))


        plt.figure(figsize=(8, 5))
        plt.plot(K_range, silhouette_scores, marker='o')
        plt.xlabel('Number of clusters')
        plt.ylabel('Silhouette Score')
        plt.title('Silhouette Scores')
        plt.show()
    
    def fit(self, data_scaled):
        self.algorithm.fit(data_scaled) #fit the model to the data with the correct number of k

        return self

    def predict(self, X_train, data_scaled):
        if not isinstance(self.algorithm, KMeans):
            raise ValueError("Predict only works for KMeans")

        X_train['cluster_kmeans'] = self.algorithm.predict(data_scaled) 
    


    