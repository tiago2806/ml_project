import pandas as pd 
import seaborn as sns 
import matplotlib.pyplot as plt 
import math

def plot_missing_values(df, title='Count of Missing Values per Feature'):
    """
    Calculates and plots a horizontal bar chart of missing values in the dataset.
    """
    missing_data = df.isnull().sum()
    missing_data = missing_data[missing_data > 0].sort_values(ascending=False)
        
    plt.figure(figsize=(16, 5))
    sns.barplot(x=missing_data.values, y=missing_data.index, color='skyblue')
    plt.title(title, fontsize=14, fontweight='bold')
    plt.xlabel('Number of Missing Rows')
    plt.ylabel('')
    plt.show()



def plot_distribution(df):
    """
    Plots the distribution for all numeric columns in a clean grid layout.
    Automatically disables KDE for discrete variables (like counts).
    """
    
    numeric_cols = df.select_dtypes(include=['int64', 'float64', 'Int64']).columns
    
    n_cols = 7
    n_rows = math.ceil(len(numeric_cols) / n_cols)
    
    fig, axes = plt.subplots(n_rows, n_cols, figsize=(20, 2.5 * n_rows))
    axes = axes.flatten()
    
    for i, col in enumerate(numeric_cols):
        
        is_discrete = df[col].nunique() < 15
        
        sns.histplot(data=df, x=col, bins=30, color='skyblue', kde=not is_discrete, ax=axes[i])
        axes[i].set_title(f'{col}', fontsize=10, fontweight='bold')
        axes[i].set_xlabel('')
        axes[i].set_ylabel('')
        
    for j in range(len(numeric_cols), len(axes)):
        fig.delaxes(axes[j])
        
    plt.tight_layout()
    plt.show()

def plot_pie_chart(df, variable, colors, legend, title_):

    """
    Creates a pie chart to visualize the distribution of a categorical variable.

    Parameters:
    - df (pd.DataFrame): DataFrame containing the data.
    - variable (str): The name of the column to plot.
    - colors (list): List of colors to use for the slices.
    - legend (list): List of labels for the legend.
    - title_ (str): Title of the plot.
    """

    # Count the occurrences of each category
    counts = df[variable].value_counts()
    
    plt.figure(figsize=(10, 6))
    plt.pie(counts, labels=legend, colors=colors, autopct='%1.1f%%', startangle=140, textprops={'fontsize': 12})
    plt.title(title_, fontsize=14, fontweight='bold')
    plt.axis('equal') 
    plt.show()

