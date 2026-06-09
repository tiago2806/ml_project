
# Customer Segmentation & Market Basket Analytics
> **Course:** Machine Learning II | NOVA Information Management School

# Customer Segmentation Project
GitHub Repository: https://github.com/tiago2806/ml_project

## Our Group

| Name | Student ID |
| :--- | :--- |
| **Henrique Santos** | 20241752
| **Laura Lisboa** | 20241783 |
| **Tiago Carvalho** | 20241728 |

---

## Project Overview

This project focuses on applying machine learning techniques to create clusters of different types of customers based on their demographics, spending behavior, and purchasing patterns. By applying clustering methods and association rules, our final results are insights for creating personalized marketing campaigns. 
For this project, we had access to two datasets: one containing customer data and another transaction baskets.

## The Structure

├── data/
│   ├── customer_info.csv                # Raw Customer Info
│   ├── customer_basket.csv              # Raw Bakset Transactions
│   ├── clean_customer_info.csv          # Customer Info Pre-Processed and ready for the modelling
│   ├── customer_basket_transactions.pkl # Pickle to presever the list datatypes on the basket
│   ├── customer_final_clusters.csv            # Dataframe matching each customer_id to its final assigned cluster
│   └── full_dataset_map.csv             # All the customers represented on the map (without defined sample size)
├── notebooks/
│   ├── 01_EDA.ipynb                     # Exploratory Data Analysis, outlier, duplicates and impossible values detection and feature discovery
│   ├── 02_Data_Preprocessing.ipynb      # Pipelines for cleaning and correct what we identified before and feature engineering
│   ├── 03_modelling.ipynb               # Elbow, Silhouette, K-Means, Hierarchical and some visualizations
│   └── 04_Association_rules.ipynb       # Association Rules with the Apriori method
├── src/
│   ├── datacleaning.py                  # Demographic cleaning modules and pipeline functions
│   ├── clustering.py              # Modular K-Means wrappers, scoring, and profiling scripts
│   ├── association.py 
│   └── eda.py     
│         # Reusable transactional encoding and rule mining engines
├── webapp/                              # Complete source code for the interactive Streamlit/React dashboard
├── requirements.txt                     # Centralized Python library dependencies for the Jupyter environment
└── README.md                            # Main project documentation

---

## Requirements and Necessary Libraries

To be able to see the whole project, your workspace must include the following dependencies. 

### For the Python Files and Notebooks

 `pandas`
 `numpy` 
 `scikit-learn`
 `seaborn`
 `ast`
 `sys`
 `os`
 `mlxtend` 
 `geopandas` 
 `mapclassify`
 `matplotlib` 

### Instruction to Run Web App
Run these on your terminal:

1. **`cd webapp`**
   * It "moves" you to inside of the web app folder which has everything related to the web app

2. **`npm install`**
   * Installs the package needed if you do not already have it

3. **`npm run dev`**
   * After running this command, it should open the webapp automatically. If it doesn´t, it will show you a link similar to this one: http://localhost:5173/ .Try "Ctrl + click on the link".