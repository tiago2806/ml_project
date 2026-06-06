import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans, AgglomerativeClustering
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
from umap import UMAP
from scipy.cluster.hierarchy import dendrogram, linkage
from sklearn.metrics import silhouette_score, silhouette_samples
from sklearn.base import clone
from utils import (
    plot_dendrogram,
    plot_2d_with_classes,
    visualize_dimensionality_reduction
)

def plot_elbow(X_scaled, k_range=15):
    """
    Calculates and plots the Elbow Method (Inertia)
    
    Parameters:
    X_scaled: The scaled feature matrix.
    k_range: The maximum number of clusters to test (default is 15).
    """
    inertias = []

    for k in range(2, k_range + 1):
        experimental_kmeans = KMeans(n_clusters=k, random_state=42).fit(X_scaled)
        inertias.append(experimental_kmeans.inertia_)

    plt.plot(range(2, k_range + 1), inertias, marker='o')
    plt.xlabel('Number of clusters')
    plt.ylabel('Dispersion (inertia)')
    plt.title('Elbow Method for Optimal K')
    plt.show()


def plot_silhouette(X_scaled, K_range=15):
    scores = []

    for k in range(2,K_range+1):
        experimental_kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
        labels = experimental_kmeans.fit_predict(X_scaled)
        scores.append(silhouette_score(X_scaled, labels))
    
    plt.figure(figsize=(8, 5))
    plt.plot(range(2,K_range+1), scores, marker='o')
    plt.xlabel('Number of clusters')
    plt.ylabel('Silhouette Score')
    plt.title('Silhouette Scores')
    plt.show()
