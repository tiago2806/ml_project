
# Customer Segmentation & Market Basket Analytics
> **Course:** Machine Learning II | NOVA Information Management School

## Our Group

| Name | Student ID |
| :--- | :--- |
| **Henrique Santos** | 20241752
| **Laura Lisboa** | 20241783 |
| **Tiago Carvalho** | 20241728 |

---

## The Structure

├── data/
│   ├── customer_info.csv                # Raw Customer Info
│   ├── customer_basket.csv              # Raw Bakset Transactions
│   ├── clean_customer_info.csv          # Customer Info Pre-Processed and ready for the modelling
│   ├── customer_basket_transactions.pkl # Pickle to presever the list datatypes on the basket
│   ├── customer_clusters.csv            # Dataframe matching each customer_id to its final assigned cluster
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

## Some Decisions

1. **Iterative Feature Engineering (Share of Wallet vs. Lifetime Spend):** * *The Hypothesis:* Initially, we engineered relative spending features ("Share of Wallet" percentages) to isolate pure lifestyle tastes and prevent the K-Means algorithm from being biased by absolute wealth. 
   * *The Reality:* Empirical testing revealed that percentage-based clustering failed to produce mathematically distinct or commercially viable segments on this specific dataset. 
   * *The Pivot:* We maintained the percentage analysis as a documented proof-of-concept but pivoted our definitive modeling matrix to utilize **absolute lifetime spend**. This architectural decision successfully generated highly cohesive, interpretable clusters ($K=8$) that perfectly align with actionable promotional strategies.

2. **Geospatial Fraud & Data Quality Audit:** Leveraged out-of-sample coordinate distributions to expose mathematically perfect geometric bounding boxes, unmasking the synthetic nature of the dataset's location metrics. To prove this anomaly globally, we generated mapping visualizations using both sampled data and the `full_dataset_map.csv`.

3. **Niche-Focused Association Rules:** Enforced granular minimum support thresholds (`0.02`) to filter out obvious, hyper-frequent commercial associations ("Bread -> Milk"). By focusing on high-lift, high-confidence rules across our specific $K=8$ clusters, we uncovered "Hidden Gems" tailored for niche cross-selling.

---


## Requirements and Necessary Libraries

To replicate the experimental environment, your workspace must include the following dependencies. These are split into the data engineering environment (Python) and the frontend dashboard application engine (Node.js).

### 1. Data Science & Machine Learning Stack (Python Ecosystem)

| Package | Purpose
| :--- | :--- |
| `pandas` | Dataframe manipulation, merging pipelines, and matrix aggregation. |
| `numpy` | Vectorized numerical operations and difference matrix evaluations. |
| `scikit-learn` | `StandardScaler` transformations and `KMeans` algorithm execution. |
| `mlxtend` | Market Basket Analysis via `apriori` and `association_rules` miners. |
| `geopandas` | Geospatial vector data handling to map latitudes and longitudes. |
| `mapclassify` | Choropleth classification and coordinate binning algorithms. |
| `matplotlib` |  Standard plotting engine for Elbow curves, Silhouette views, and scatter maps. |

### Detailed Web Application Execution Rationale

To interact with the final customer segmentation dashboards, the deployment lifecycle transitions from data science script environments to a full-stack Node.js framework runtime. Below is the technical breakdown of each initialization step:

1. **`cd webapp` (Directory Context Switch)**
   * **Purpose:** Moves the terminal's active working directory directly into the isolated `webapp/` folder architecture.
   * **Technical Rationale:** The front-facing interface is completely decoupled from the native root directories where the model training matrices and raw datasets are stored. This command targets the exact directory space where the application blueprint and configuration file (`package.json`) exist.

2. **`npm install` (Dependency Resolution & Environment Build)**
   * **Purpose:** Parses the centralized application manifest (`package.json`) to automatically fetch, resolve, and locally cache the entire collection of external open-source packages and frameworks required by the system.
   * **Technical Rationale:** This step instantiates the standard, repeatable execution sandbox inside a local `node_modules/` container. It safely configures UI component architectures, interactive graphing engines, and responsive styling sheets before any visual assets are rendered.

3. **`npm run dev` (Local Tool Engine Execution)**
   * **Purpose:** Executes the project's internal development runtime script to compile source modules into optimized browser assets and deploy an active, hot-reloading development engine.
   * **Technical Rationale:** This initiates the background engine that keeps the analytics app running locally. It outputs a designated host address (typically `http://localhost:5173`), creating a bridge that lets evaluators directly explore, filter, and test the commercial feasibility of the $K=8$ customer personas inside a modern web browser.