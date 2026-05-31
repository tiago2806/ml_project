import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans, AgglomerativeClustering
from scipy.cluster.hierarchy import dendrogram, linkage
from sklearn.metrics import silhouette_score, silhouette_samples
from sklearn.preprocessing import StandardScaler
from matplotlib.lines import Line2D 



def plot_dendrogram(model, **kwargs):
    '''
    Create linkage matrix and then plot the dendrogram
    Arguments: 
    - model(HierarchicalClustering Model): hierarchical clustering model.
    - **kwargs
    Returns:
    None, but dendrogram plot is produced.
    '''
    # create the counts of samples under each node
    counts = np.zeros(model.children_.shape[0])
    n_samples = len(model.labels_)
    for i, merge in enumerate(model.children_):
        current_count = 0
        for child_idx in merge:
            if child_idx < n_samples:
                current_count += 1  # leaf node
            else:
                current_count += counts[child_idx - n_samples]
        counts[i] = current_count

    linkage_matrix = np.column_stack(
        [model.children_, model.distances_, counts]
    ).astype(float)

    # Plot the corresponding dendrogram
    dendrogram(linkage_matrix, **kwargs)


def scaling(data):
    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(data)

    return scaled_data

def plot_silhouette(X, labels, title="Silhouette Plot", ax_sil=None, ax_scatter=None):
    """Side-by-side silhouette diagram and scatter plot."""
    sample_scores = silhouette_samples(X, labels)
    overall = sample_scores.mean()
    n_clusters = len(np.unique(labels))
    colors = plt.cm.tab10(np.linspace(0, 1, n_clusters))

    fig = None
    if ax_sil is None:
        fig, (ax_sil, ax_scatter) = plt.subplots(1, 2, figsize=(14, 5))

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

    # --- Scatter plot ---
    for k, color in zip(range(n_clusters), colors):
        mask = labels == k
        ax_scatter.scatter(X[mask, 0], X[mask, 1], color=color,
                           s=40, alpha=0.7, label=f'C{k}')
    ax_scatter.set_title("Cluster Assignments")
    ax_scatter.legend()

    if fig:
        plt.tight_layout()
        plt.show()

    return overall



def plot_2d_with_classes(labels, components):
    unique_labels = np.unique(labels)
    colors = plt.cm.tab10(np.linspace(0, 1, len(unique_labels)))
    
    custom = [Line2D([], [], marker='.', color=colors[i], linestyle='None') 
              for i in range(len(unique_labels))]
    
    color_code = [colors[np.where(unique_labels == label)[0][0]] for label in labels]
    
    plt.scatter(
        components[:, 0],
        components[:, 1],
        alpha=0.5,
        c=color_code,
        edgecolors='black'
    )
    
    plt.legend(handles=custom,
               labels=[f'Cluster {l}' for l in unique_labels],
               bbox_to_anchor=(1.05, 0.5), loc='lower left')
    
    plt.show()


def visualize_dimensionality_reduction(transformation, targets):
    # create a scatter plot of the t-SNE output
    plt.scatter(transformation[:, 0], transformation[:, 1],
                c=np.array(targets).astype(int), cmap=plt.cm.tab20)

    labels = np.unique(targets)

    cmap = plt.cm.tab20
    norm = plt.Normalize(vmin=min(np.array(labels).astype(int)), vmax=max(np.array(labels).astype(int)))
    rgba_values = cmap(norm(labels))

    # create a legend with the class labels and colors
    handles = [plt.scatter([], [], c=rgba, label=label) for rgba, label in zip(rgba_values, labels)]
    plt.legend(handles=handles, title='Classes')
