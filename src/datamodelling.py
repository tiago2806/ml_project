import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans, AgglomerativeClustering
from scipy.cluster.hierarchy import dendrogram, linkage
from sklearn.metrics import silhouette_score
from sklearn.base import clone
from utils import (
    plot_dendrogram
)

class Clusteringworkflow:
    """
    Class containing the workflow of the algorithms used for the creation of clusters.
    """
    def __init__(self, algorithm):
        #instatiation of an object, which is just a clustering algorithm
        self.algorithm = algorithm

        
    def find_optimal_k(self, data_scaled, K_range= 25):
        """
        This function, for the algorithm selected, fits it experimentally on the data, and plots either an elbow method for KMeans or a dendrogam
        for AgglomerativeClustering so that we can extract a possible optimal number of clusters (K).

        Parameters:
        data_scaled -> dataframe: The data on which we want to experimental fit the algorithm.
        K_range -> int: The values of K we are going to test the algorithm with. Initially set to 25 because only KMeans uses that parameter, and by setting
        it initially to 25, we don't need to manually pass a number to it, which means when the algorithm is not KMeans, it will just ignore that parameter.

        -----------
        Output:
        A graph, either the inertia plot for KMeans, or a dendogram for AgglomerativeClustering, suggesting an optimal number of clusters.
        """
        if isinstance(self.algorithm, KMeans):
            dispersion = []
            for k in range(2, K_range):
                model_kmeans = clone(self.algorithm)
                model_kmeans.set_params(n_clusters=k)
                model_kmeans.fit(data_scaled)
                dispersion.append(model_kmeans.inertia_)

            plt.plot(range(2, K_range), dispersion, marker='o')
            plt.xlabel('Number of clusters')
            plt.ylabel('Dispersion (inertia)')
            plt.show()

        elif isinstance(self.algorithm, AgglomerativeClustering):
            model_hierarchical = clone(self.algorithm)
            model_hierarchical.set_params(compute_distances=True)
            model_hierarchical.fit(data_scaled)
            fig, ax = plt.subplots()
            plt.title("Hierarchical Clustering Dendrogram")
            # plot the top three levels of the dendrogram
            plot_dendrogram(model_hierarchical, truncate_mode="level", p=50)
            plt.axhline(y = 50, color = 'r', linestyle = '-')
            plt.show() 

        else:
            raise ValueError("This is only for KMeans or AgglomerativeClustering")
        
    def silhouette(self, data_scaled, K_range = 25):
        """
        Function with similar objective as the previous one. It also helps to find an optimal number of clusters
        
        Parameters:
        data_scaled -> dataframe: The data on which we want to experimental fit the algorithm.
        K_range -> int: The values of K we are going to test the algorithm with. Initially set to 25 because only KMeans uses that parameter, and by setting
        it initially to 25, we don't need to manually pass a number to it, which means when the algorithm is not KMeans, it will just ignore that parameter.

        --------------
        Output:
        A graph, showing the silhouette score for each value of k
        """
        if not isinstance(self.algorithm, (KMeans, AgglomerativeClustering)):
                raise ValueError("Silhouette only works for KMeans or AgglomerativeClustering")
        
        silhouette_scores = []

        for k in range(2,K_range):
            model = clone(self.algorithm)
            model.set_params(n_clusters=k)
            
            labels = model.fit_predict(data_scaled)
            silhouette_scores.append(silhouette_score(data_scaled, labels))


        plt.figure(figsize=(8, 5))
        plt.plot(range(2,K_range), silhouette_scores, marker='o')
        plt.xlabel('Number of clusters')
        plt.ylabel('Silhouette Score')
        plt.title('Silhouette Scores')
        plt.show()
    

    def fit_and_prediction(self, original_data, data_scaled):
        """
        This function fits the chosen algorithm to the data previously scaled and creates a column in the original dataset containing the cluster that
        each observation is allocated to.

        Parameters:
        original_data -> dataframe: The dataframe where we'll add the column with the labels for each observation.
        data_scaled -> dataframe: The data on which we'll train the algorithm and create the clusters.
        """
        col_name = f"cluster_{self.algorithm.__class__.__name__.lower()}"
        original_data[col_name] = self.algorithm.fit_predict(data_scaled) 
    
        return self



class DimensionalityReduction:
    """
    This is the class for the algorithms that are going to be used with the intent of facilitating visualization
    """