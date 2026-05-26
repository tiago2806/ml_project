
import pandas as pd
import numpy as np
import ast
from datetime import datetime
from sklearn.preprocessing import StandardScaler
from sklearn.impute import KNNImputer
from sklearn.cluster import DBSCAN


# ==========================================
# SHARED HELPER FUNCTIONS
# ==========================================

def drop_column(dataset, columns):
    '''
    Removes a specific column or columns from the dataset.

    Parameters:
    - dataset: the df from which the column(s) will be removed.
    - columns: the column name or a list of column names to be removed.

    Output:
    - df: the dataset with the specified column(s) removed.
    '''
    df = dataset.copy()
    df.drop(columns, axis=1, inplace=True, errors='ignore')
    return df

def eliminate_duplicates(dataset):
    '''
    Removes duplicate rows from the dataset.

    Parameters:
    - dataset: the df that may contain duplicate rows.

    Output:
    - df: the dataset with duplicate rows removed.
    '''
    df = dataset.copy()
    df = df.drop_duplicates()
    return df

def handle_outliers(dataset, eps_value, min_samples_value):
    """
    Detects and removes multidimensional outliers using DBSCAN.
    Allows custom eps and min_samples for different datasets.

    Parameters:
        dataset - The df with potential outliers.
        eps_value - The epsilon value for DBSCAN.
        min_samples_value - The minimum samples value for DBSCAN.

    Returns:
        df- df with outliers removed.
    """
    df = dataset.copy()

    numeric_cols = df.select_dtypes(include=['int64', 'float64', 'Int64']).columns
    numeric_cols = [col for col in numeric_cols if col != 'customer_id']

    if len(numeric_cols) > 0:
        scaler = StandardScaler()
        scaled_data = scaler.fit_transform(df[numeric_cols])
        
        dbscan = DBSCAN(eps=eps_value, min_samples=min_samples_value)
        dbscan.fit(scaled_data)
      
        outliers_mask = dbscan.labels_ == -1
        df = df[~outliers_mask]

    return df


# ============================================
# ======== CUSTOMER INFO PIPELINE ============
# ============================================


# DATA TYPES ================================
#============================================

def customer_handle_datatypes(dataset):
    '''
    Make necessary conversions to some column data types,
    calculate the customer age based on the birthdate and 
    drop the birthdate and loyalty card number columns.

    Parameters:
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

# IMPOSSIBLE VALUES =========================
#============================================

def customer_check_impossible_values(dataset):
    '''
    Handles impossible values based on predefined rules.
    
    Parameters:
    - dataset: the df that may contain impossible values.
    
    Output:
    - df: the dataset with impossible values set to NaN.
    '''
    df = dataset.copy()

    #Customer Age (0-120)
    if 'customer_age' in dataset.columns:
        df.loc[(df['customer_age'] <= 0) | (df['customer_age'] > 120), 'customer_age'] = np.nan

    #Negative values in count columns and 'lifetime_spend' columns
    count_cols = ['kids_home', 'teens_home', 'number_complaints', 'distinct_stores_visited', 'year_first_transaction']
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


# MISSING VALUES ============================
#============================================

def customer_handle_missing_values(dataset):
    '''
    What it does:
    - Missing Values in'lifetime_spend' columns are filled with 0 (assuming no purchase was made).
    - Applies KNN Imputation (k=7) in numeric columns.
    - The probability values are clipped to valid ranges ([0, 1]).
    - Rounds count columns to the nearest integer and converts them to Int64 type.
    
    Parameters:
        dataset: The dataframe with missing values.

    Output:
        df: A dataset with zero missing values.
    '''
    df = dataset.copy()

    #Lifetime spend columns, set to zero
    spend_cols = [col for col in dataset.columns if 'lifetime_spend' in col]
    df[spend_cols] = df[spend_cols].fillna(0) 

    #Percentage of products bought on promotion, set to zero
    if 'percentage_of_products_bought_promotion' in df.columns:
        df['percentage_of_products_bought_promotion'] = df['percentage_of_products_bought_promotion'].fillna(0)

    #KNN imputation for numerical columns, but first we need to temporarily scale the data 
    cols_with_nans = df.columns[df.isna().any()].tolist()
    numeric_cols_with_nans = [col for col in cols_with_nans if df[col].dtype in ['int64', 'float64', 'Int64']]

    support_cols = ['customer_age', 'typical_hour'] 
    knn_cols = list(set(numeric_cols_with_nans + support_cols))
    knn_cols = [col for col in knn_cols if col in df.columns]

    if len(knn_cols) > 0:
        scaler = StandardScaler()
        imputer = KNNImputer(n_neighbors=7)
        
        scaled_data = scaler.fit_transform(df[knn_cols])
        imputed_data = imputer.fit_transform(scaled_data)
        df[knn_cols] = scaler.inverse_transform(imputed_data) #to get the original scale back so we can find outliers and round the values
    
    df['percentage_of_products_bought_promotion'] = df['percentage_of_products_bought_promotion'].clip(0.0, 1.0)
        
    count_cols = ['kids_home', 'teens_home', 'number_complaints', 'distinct_stores_visited', 'typical_hour', 'customer_age','year_first_transaction']
    for col in count_cols:
        if col in df.columns:
            df[col] = df[col].round().astype('Int64')
        
    return df

#FEATURE ENGINEERING ==============================
#==================================================

def customer_feature_engineering(dataset):
    '''
    Extracts underlying information into new predictive features.
    
    Parameters:
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

    ordered_columns = [
        'customer_name', 'customer_gender', 'customer_age', 'education_level',
        'kids_home', 'teens_home', 'total_children', 'has_children', 
        'year_first_transaction', 'distinct_stores_visited', 'number_complaints',
        'typical_hour', 'time_of_day', 'hour_sin', 'hour_cos',
        'lifetime_total_distinct_products', 'percentage_of_products_bought_promotion',
        'lifetime_spend_groceries', 'lifetime_spend_vegetables', 'lifetime_spend_meat', 
        'lifetime_spend_fish', 'lifetime_spend_electronics', 'lifetime_spend_videogames', 
        'lifetime_spend_nonalcohol_drinks', 'lifetime_spend_alcohol_drinks', 
        'lifetime_spend_hygiene', 'lifetime_spend_petfood',
        'latitude', 'longitude'
    ]
    
    final_columns = [col for col in ordered_columns if col in df.columns]
    df = df[final_columns]

    return df   

# FINAL PIPELINE =============================
#=============================================

def customer_clean_data(dataset):
    """
    This function executes the entire data cleaning pipeline
    in the correct order.

    Input:
    - dataset: the original df that needs to be cleaned.

    Output:
    - clean_df: the cleaned dataset ready for modeling.
    """
    clean_df = customer_handle_datatypes(dataset)
    clean_df = eliminate_duplicates(clean_df)
    clean_df = customer_check_impossible_values(clean_df)
    clean_df = customer_handle_missing_values(clean_df)
    clean_df = handle_outliers(clean_df, eps_value=3.5, min_samples_value=5)
    clean_df = customer_feature_engineering(clean_df)

    return clean_df


# ============================================
# ======= CUSTOMER BASKET PIPELINE ===========
# ============================================

# DATA TYPES ================================
#============================================

def basket_handle_datatypes(dataset):
    """
    Safely parses the string representation of lists into actual Python lists.
    
    Parameters:
        dataset (pd.DataFrame): The raw basket dataframe.
    Output:
        pd.DataFrame: Dataframe with list_of_goods as iterable lists.
    """
    df = dataset.copy()
    
    # ast.literal_eval turns the string "['a', 'b']" into a real list ['a', 'b']
    if 'list_of_goods' in df.columns:
        df['list_of_goods'] = df['list_of_goods'].apply(
            lambda x: ast.literal_eval(x) if isinstance(x, str) else x
        )
        
    return df

# FEATURE ENGINEERING ==============================
#===================================================

def basket_feature_engineering(dataset):
    """
    Extracts numerical metrics from the shopping baskets.
    
    Parameters:
        dataset (pd.DataFrame): Dataframe with parsed lists.
    Output:
        pd.DataFrame: Dataframe containing the size of each basket.
    """
    df = dataset.copy()
    
    # Calculates how many items were bought in this specific invoice
    if 'list_of_goods' in df.columns:
        df['basket_size'] = df['list_of_goods'].apply(lambda x: len(x) if isinstance(x, list) else 0)
        
    return df

# GROUP BY ONE ROW ======================================
# =======================================================

def basket_aggregate(dataset):
    """
    Aggregates multiple transaction rows into a single summary row per customer.
    
    Parameters:
        dataset (pd.DataFrame): Dataframe with individual invoices.
    Output:
        pd.DataFrame: A customer-level dataframe ready for merging.
    """
    df = dataset.copy()
    
    # Group by customer_id so we have one row per customer
    if 'customer_id' in df.columns:
        customer_baskets = df.groupby('customer_id').agg(
            total_trips=('invoice_id', 'nunique'),
            total_items_bought=('basket_size', 'sum'),
            average_basket_size=('basket_size', 'mean'),
            max_basket_size=('basket_size', 'max'),
            min_basket_size=('basket_size', 'min'),
            # Substitui a linha do unique_products_bought por esta:
            unique_products_bought=('list_of_goods', lambda x: len(set(item for sublist in x if isinstance(sublist, list) for item in sublist)))
        ).reset_index()
        
        # Keep the numbers clean
        customer_baskets['average_basket_size'] = customer_baskets['average_basket_size'].round(2)
        return customer_baskets
        
    return df

# FINAL PIPELINE ==============================
# =============================================

def basket_clean_data(dataset):
    """
    Executes the full cleaning and feature engineering pipeline for the basket data.
    
    Parameters:
        dataset (pd.DataFrame): The raw basket dataframe.
    Output:
        pd.DataFrame: A cleaned and feature-engineered customer-level dataframe.
    """
    clean_df = eliminate_duplicates(dataset)
    clean_df = basket_handle_datatypes(clean_df)
    clean_df = basket_feature_engineering(clean_df) # we still have one row per invoice
    clean_df = basket_aggregate(clean_df) # now we have one row per customer with all the basket features aggregated
    clean_df = handle_outliers(clean_df, eps_value=1.5, min_samples_value=15)
    
    return clean_df

def merge_datasets(clean_customer_df, clean_basket_df):
    """
    Merges the cleaned customer and basket datasets using an inner join.
    Ensures only customers with transaction history are retained.
    """
    import pandas as pd
    
    final_df = pd.merge(
        clean_customer_df, 
        clean_basket_df.set_index('customer_id'), 
        left_index=True, 
        right_index=True, 
        how='inner'
    )
    
    return final_df


# VALIDATION CHECKS ===========================
# =============================================

def check_missing(final_df, raw_data_customer, raw_data_basket):
    """
    Creates a dataframe comparing the missing values of the final dataset
    with the original raw datasets.
    """
    import pandas as pd
    
    final_missing = final_df.isnull().sum()
    
    raw_missing = pd.concat([
        raw_data_customer.isnull().sum(), 
        raw_data_basket.isnull().sum()
    ])
    
    # Remove duplicates
    raw_missing = raw_missing[~raw_missing.index.duplicated(keep='first')]
    
    missing_df = pd.DataFrame({
        'Missing Count (Final)': final_missing,
        'Missing Count (Original)': raw_missing
    })
    
    # Filtro: Mostrar apenas colunas que efetivamente tinham missing values no início
    missing_df = missing_df[missing_df['Missing Count (Original)'] > 0]
    
    return missing_df

def check_datatypes(final_df, raw_data_customer, raw_data_basket):
    """
    Creates a dataframe comparing the data types of the final dataset
    with the original raw datasets.
    """
    import pandas as pd
    
    final_dtypes = final_df.dtypes
    
    raw_dtypes = pd.concat([
        raw_data_customer.dtypes, 
        raw_data_basket.dtypes
    ])
    
    # Remove duplicates
    raw_dtypes = raw_dtypes[~raw_dtypes.index.duplicated(keep='first')]
    
    dtypes_df = pd.DataFrame({
        'Datatype (Final)': final_dtypes.astype(str),
        'Datatype (Original)': raw_dtypes.astype(str)
    })
    
    # Filtro: Mostrar apenas colunas que já existiam E cujo tipo de dados mudou
    dtypes_df = dtypes_df[
        (dtypes_df['Datatype (Final)'] != dtypes_df['Datatype (Original)']) & 
        (dtypes_df['Datatype (Original)'] != 'nan')
    ]
    
    return dtypes_df

def check_numeric_ranges(final_df):
    """
    Returns the minimum and maximum values for key numeric columns 
    to prove that no logical boundaries were violated.
    """
    columns_to_inspect = [
        'customer_age', 'typical_hour', 'percentage_of_products_bought_promotion', 
        'total_children', 'year_first_transaction', 'number_complaints',
        'distinct_stores_visited', 'lifetime_spend_groceries',
        'total_trips', 'average_basket_size'
    ]
    
    # Check only columns that actually exist in the dataframe to avoid errors
    cols_present = [col for col in columns_to_inspect if col in final_df.columns]
    
    return final_df[cols_present].describe().loc[['min', 'max']]
