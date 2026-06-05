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



def plot_silhouette(X, labels, title="Silhouette Plot", ax_sil=None):
    """Side-by-side silhouette diagram and scatter plot."""
    sample_scores = silhouette_samples(X, labels)
    overall = sample_scores.mean()
    n_clusters = len(np.unique(labels))
    colors = plt.cm.tab10(np.linspace(0, 1, n_clusters))

    fig = None
    if ax_sil is None:
        fig, ax_sil = plt.subplots(figsize=(14, 5))

    # --- Silhouette bars ---
    y_lower = 10
    for k, color in zip(range(n_clusters), colors):
        cluster_scores = np.sort(sample_scores[labels == k])
        size_k = len(cluster_scores)
        y_upper = y_lower + size_k
        ax_sil.fill_betweenx(np.arange(y_lower, y_upper), 0, cluster_scores,
                             facecolor=color, edgecolor=color, alpha=0.8)
        ax_sil.text(-0.05, y_lower + size_k / 2, f"C{k}", fontsize=9, ha='right')
        y_lower = y_upper + 10

    ax_sil.axvline(overall, color='red', linestyle='--', linewidth=1.5,
                   label=f'Mean = {overall:.3f}')
    ax_sil.set_xlabel("Silhouette coefficient")
    ax_sil.set_ylabel("Cluster")
    ax_sil.set_title(title)
    ax_sil.set_xlim([-0.2, 1.0])
    ax_sil.legend(loc='upper right')

    return overall