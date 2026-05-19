
import pandas as pd
import numpy as np
from datetime import datetime
from sklearn.preprocessing import StandardScaler
from sklearn.impute import KNNImputer


# ==========================================
# HELPER FUNCTIONS
# ==========================================

def drop_column(dataset, columns):
    dataset.drop(columns, axis = 1, inplace = True)
    return dataset

# ==========================================
# 1. DATA TYPES
# ==========================================

def handle_datatypes(dataset):
    df = dataset.copy()

    # Dates and Typical Hour
    df['customer_birthdate'] = pd.to_datetime(df['customer_birthdate'], errors='coerce', format= 'mixed')
    df['year_first_transaction'] = pd.to_datetime(df['year_first_transaction'], errors='coerce').dt.year
    df['typical_hour'] = pd.to_numeric(df['typical_hour'], errors='coerce')

    # Calculate Age & Drop Birthdate
    current_year = datetime.now().year
    df['customer_age'] = current_year - df['customer_birthdate'].dt.year
    drop_column(df, ['customer_birthdate'])


    # Numerical columns
    df['kids_home'] = df['kids_home'].astype('Int64')
    df['teens_home'] = df['teens_home'].astype('Int64')
    df['number_complaints'] = df['number_complaints'].astype('Int64')
    df['distinct_stores_visited'] = df['distinct_stores_visited'].astype('Int64')    
    df['lifetime_total_distinct_products'] = df['lifetime_total_distinct_products'].astype('Int64')
   
    return df

# ==========================================
# 2. DUPLICATES
# ==========================================

def eliminate_duplicates(dataset):
    dataset = dataset.drop_duplicates()
    return dataset


# ==========================================
# 3. IMPOSSIBLE VALUES
# ==========================================


#customer age
def check_impossible_values(dataset):
    df = dataset.copy()
    if 'customer_age' in dataset.columns:
        df.loc[(df['customer_age'] <= 0) | (df['customer_age'] > 120), 'customer_age'] = np.nan

#negative values in count columns
    count_cols = ['kids_home', 'teens_home', 'number_complaints', 'distinct_stores_visited']
    for col in count_cols:
        if col in dataset.columns:
            df.loc[df[col] < 0, col] = np.nan

#Lifetime spend columns  
    spend_cols = [col for col in dataset.columns if 'lifetime_spend' in col]
    for col in spend_cols:
        df.loc[df[col] < 0, col] = np.nan

#typical hour (6-23)
    if 'typical_hour' in dataset.columns:
        df.loc[(df['typical_hour'] < 6) | (df['typical_hour'] > 23), 'typical_hour'] = np.nan

#percentage of products bought in promotion (0-1)
    if 'percentage_of_products_bought_promotion' in dataset.columns:
        df.loc[(df['percentage_of_products_bought_promotion'] < 0) | (df['percentage_of_products_bought_promotion'] > 1.0), 'percentage_of_products_bought_promotion'] = np.nan

#year of first transaction cannot be in the future)
    if 'year_first_transaction' in dataset.columns:
        current_year = datetime.now().year
        df.loc[df['year_first_transaction'] > current_year, 'year_first_transaction'] = np.nan

#latitude and longitude need to be in the correct range
    if 'latitude' in dataset.columns:
        df.loc[(df['latitude'] < -90) | (df['latitude'] > 90), 'latitude'] = np.nan
        
    if 'longitude' in dataset.columns:
        df.loc[(df['longitude'] < -180) | (df['longitude'] > 180), 'longitude'] = np.nan

    return dataset



# ==========================================
# 4. MISSING VALUES
# ==========================================

def handle_missing_values(dataset):

    df = dataset.copy()

    #lifetime spend... columns
    spend_cols = [col for col in dataset.columns if 'lifetime_spend' in col] #onde é nulo, é porque provavelmenet o cliente nunca la foi
    df[spend_cols] = df[spend_cols].fillna(0) 


    #KNN imputation for numerical columns, but first we need to scale the data 
    #numerical columns (kids_home, teens_home, number_complaints, distinct_stores_visited, typical_hour, percentage_of_products_bought_promotion)
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

    df = dataset.copy()

    return dataset


# ==========================================
# 6. FEATURE ENGINEERING
# ==========================================

def feature_engineering(dataset):

    df = dataset.copy()

    df['total_children'] = df['kids_home'] + df['teens_home']
    #df['has_children'] = 
    #create time of the day bins 'night' -> 00:00 - 05:59 etc.
    #create a cycliclal encoding for the hours (to let the model know that 23 and 00 are neighbours)
    return df   


# ==========================================
# 7. SCALING
# ==========================================

def scale_data(dataset):

    df = dataset.copy()

    return dataset


# ==========================================
# PIPELINE 
# ==========================================

def clean_data(dataset):

    """
    This function contains all the other functions.
    """
    clean_df = handle_datatypes(dataset)
    clean_df = eliminate_duplicates(clean_df)
    clean_df = check_impossible_values(clean_df)
    clean_df = handle_missing_values(clean_df)
    clean_df = handle_outliers(clean_df)
    clean_df = feature_engineering(clean_df)
    clean_df = scale_data(clean_df)

    return clean_df

    pass
