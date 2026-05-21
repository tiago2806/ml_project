
import pandas as pd
import numpy as np
from datetime import datetime
from sklearn.preprocessing import StandardScaler
from sklearn.impute import KNNImputer
from sklearn.cluster import DBSCAN


# ==========================================
# HELPER FUNCTIONS
# ==========================================

def drop_column(dataset, columns):
    '''
    Removes a specific column or columns from the dataset.

    Input:
    - dataset: the df from which the column(s) will be removed.
    - columns: the column name or a list of column names to be removed.

    Output:
    - df: the dataset with the specified column(s) removed.
    '''
    df = dataset.copy()
    df.drop(columns, axis=1, inplace=True, errors='ignore')
    return df

# ==========================================
# 1. DATA TYPES
# ==========================================

def handle_datatypes(dataset):
    '''
    Make necessary conversions to some column data types,
    calculate the customer age based on the birthdate and 
    drop the birthdate and loyalty card number columns.

    Input:
    - dataset: the df with the original data types.

    Output:
    - df: the dataset with the correct data types and new age column.
    '''
    df = dataset.copy()

    # Dates and Typical Hour
    df['customer_birthdate'] = pd.to_datetime(df['customer_birthdate'], errors='coerce', format= 'mixed')
    df['typical_hour'] = pd.to_numeric(df['typical_hour'], errors='coerce')

    # Calculate Age & Drop Birthdate and Loyalty Card Number
    current_year = datetime.now().year
    df['customer_age'] = current_year - df['customer_birthdate'].dt.year
    df = drop_column(df, ['customer_birthdate','loyalty_card_number'])


    # Numerical columns
    df['kids_home'] = df['kids_home'].round().astype('Int64')
    df['teens_home'] = df['teens_home'].round().astype('Int64')
    df['number_complaints'] = df['number_complaints'].round().astype('Int64')
    df['distinct_stores_visited'] = df['distinct_stores_visited'].round().astype('Int64')    
    df['lifetime_total_distinct_products'] = df['lifetime_total_distinct_products'].round().astype('Int64')
    df['year_first_transaction'] = df['year_first_transaction'].round().astype('Int64')
   
    return df

# ==========================================
# 2. DUPLICATES
# ==========================================

def eliminate_duplicates(dataset):
    '''
    Removes duplicate rows from the dataset.

    Input:
    - dataset: the df that may contain duplicate rows.

    Output:
    - df: the dataset with duplicate rows removed.
    '''
    df = dataset.copy()
    df = df.drop_duplicates()
    return df

# ==========================================
# 3. IMPOSSIBLE VALUES
# ==========================================

def check_impossible_values(dataset):
    '''
    Handles impossible values based on predefined rules.
    
    Input:
    - dataset: the df that may contain impossible values.
    
    Output:
    - df: the dataset with impossible values set to NaN.
    '''

    df = dataset.copy()

    #Customer Age (0-120)
    if 'customer_age' in dataset.columns:
        df.loc[(df['customer_age'] <= 0) | (df['customer_age'] > 120), 'customer_age'] = np.nan

    #Negative values in count columns and 'lifetime_spend' columns
    count_cols = ['kids_home', 'teens_home', 'number_complaints', 'distinct_stores_visited']
    for col in count_cols:
        if col in dataset.columns:
            df.loc[df[col] < 0, col] = np.nan

    spend_cols = [col for col in dataset.columns if 'lifetime_spend' in col]
    for col in spend_cols:
        df.loc[df[col] < 0, col] = np.nan

    #Typical hour has to be between 6 and 23
    if 'typical_hour' in dataset.columns:
        df.loc[(df['typical_hour'] < 6) | (df['typical_hour'] > 23), 'typical_hour'] = np.nan

    #Percentage of products bought in promotion has to be between 0 and 1
    if 'percentage_of_products_bought_promotion' in dataset.columns:
        df.loc[(df['percentage_of_products_bought_promotion'] < 0) | (df['percentage_of_products_bought_promotion'] > 1.0), 'percentage_of_products_bought_promotion'] = np.nan

    #Year of first transaction cannot be in the future
    if 'year_first_transaction' in dataset.columns:
        current_year = datetime.now().year
        df.loc[df['year_first_transaction'] > current_year, 'year_first_transaction'] = np.nan

    #Latitude and longitude need to be in the correct range
    if 'latitude' in dataset.columns:
        df.loc[(df['latitude'] < -90) | (df['latitude'] > 90), 'latitude'] = np.nan
        
    if 'longitude' in dataset.columns:
        df.loc[(df['longitude'] < -180) | (df['longitude'] > 180), 'longitude'] = np.nan

    return df

# ==========================================
# 4. MISSING VALUES
# ==========================================

def handle_missing_values(dataset):
    '''
    What it does:
    - Missing Values in'lifetime_spend' columns are filled with 0 (assuming no purchase was made).
    - Applies KNN Imputation (k=7) in numeric columns.
    - The probability values are clipped to valid ranges ([0, 1]).
    - Rounds count columns to the nearest integer and converts them to Int64 type.
    
    Input:
        dataset: The dataframe with missing values.
    Output:
        df: A dataset with zero missing values.
    '''
    df = dataset.copy()

    #Lifetime spend columns, set to zero
    spend_cols = [col for col in dataset.columns if 'lifetime_spend' in col]
    df[spend_cols] = df[spend_cols].fillna(0) 


    #KNN imputation for numerical columns, but first we need to temporarily scale the data 
    numeric_cols = df.select_dtypes(include=['int64', 'float64', 'Int64']).columns
    if len(numeric_cols) > 0:
        scaler = StandardScaler()
        imputer = KNNImputer(n_neighbors=7)
        
        scaled_data = scaler.fit_transform(df[numeric_cols])
        imputed_data = imputer.fit_transform(scaled_data)
        df[numeric_cols] = scaler.inverse_transform(imputed_data) #to get the original scale back so we can find outliers and round the values
    
    df['percentage_of_products_bought_promotion'] = df['percentage_of_products_bought_promotion'].clip(0.0, 1.0)
        
    count_cols = ['kids_home', 'teens_home', 'number_complaints', 'distinct_stores_visited', 'typical_hour', 'customer_age']
    for col in count_cols:
        if col in df.columns:
            df[col] = df[col].round().astype('Int64')
        
    return df
    

# ==========================================
# 5. OUTLIERS
# ==========================================

def handle_outliers(dataset):
    '''
    Finds and removes multidimensional outliers using the DBSCAN algorithm.
    
    Input:
        dataset - The df with potential outliers.
        
    Returns:
        df- df with outliers removed.
    '''

    df = dataset.copy()

    numeric_cols = df.select_dtypes(include=['int64', 'float64', 'Int64']).columns

    if len(numeric_cols) > 0:
        scaler = StandardScaler()
        scaled_data = scaler.fit_transform(df[numeric_cols])
        
        dbscan = DBSCAN(eps=3.5, min_samples=5)
        dbscan.fit(scaled_data)
      
        outliers_mask = dbscan.labels_ == -1
        number_of_outliers = outliers_mask.sum()
        
        df = df[~outliers_mask]

    return df


# ==========================================
# 6. FEATURE ENGINEERING
# ==========================================

def feature_engineering(dataset):
    '''
    Extracts underlying information into new predictive features.
    
    Input:
        dataset - The current dataframe.
        
    Ouput:
        df - dataset with the new features (e.g., education_level, hour_sin).
    '''

    df = dataset.copy()

    # Extract academic titles
    df['education_level'] = df['customer_name'].str.extract(r'(Bsc|Msc|Phd)')
    df['education_level'] = df['education_level'].fillna('Unknown')
    df['customer_name'] = df['customer_name'].str.replace(r'(Bsc\.\s*|Msc\.\s*|Phd\.\s*)', '', regex=True)

    #Family size and has children
    df['total_children'] = df['kids_home'] + df['teens_home']
    df['has_children'] = (df['total_children'] > 0).astype(int)

    # Time of day and cyclic encoding of typical hour
    df['time_of_day'] = pd.cut(df['typical_hour'], bins=[-1, 5, 11, 17, 24], labels=['Night', 'Morning', 'Afternoon', 'Evening'])
    df['hour_sin'] = np.sin(2 * np.pi * df['typical_hour'] / 24.0)
    df['hour_cos'] = np.cos(2 * np.pi * df['typical_hour'] / 24.0)

    return df   


# ==========================================
# PIPELINE 
# ==========================================

def clean_data(dataset):

    """
    This function executes the entire data cleaning pipeline
    in the correct order.

    Input:
    - dataset: the original df that needs to be cleaned.

    Output:
    - clean_df: the cleaned dataset ready for modeling.
    """
    clean_df = handle_datatypes(dataset)
    clean_df = eliminate_duplicates(clean_df)
    clean_df = check_impossible_values(clean_df)
    clean_df = handle_missing_values(clean_df)
    clean_df = handle_outliers(clean_df)
    clean_df = feature_engineering(clean_df)

    return clean_df

    pass
