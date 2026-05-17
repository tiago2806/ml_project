
import pandas as pd
import numpy as np
from datetime import datetime
from sklearn.preprocessing import StandardScaler
from sklearn.impute import KNNImputer



#DATA TYPES
def handle_datatypes(dataset):
    dataset['customer_birthdate'] = pd.to_datetime(dataset['customer_birthdate'], errors='coerce')
    dataset['kids_home'] = dataset['kids_home'].astype('Int64')
    dataset['teens_home'] = dataset['teens_home'].astype('Int64')
    dataset['number_complaints'] = dataset['number_complaints'].astype('Int64')
    dataset['distinct_stores_visited'] = dataset['distinct_stores_visited'].astype('Int64')    
    dataset['typical_hour'] = pd.to_datetime(dataset['typical_hour'], errors='coerce').dt.hour
    dataset['lifetime_total_distinct_products'] = dataset['lifetime_total_distinct_products'].astype('Int64')
    dataset['year_first_transaction'] = pd.to_datetime(dataset['year_first_transaction'], errors='coerce').dt.year
    return dataset

#HANDLE DUPLICATES
def eliminate_duplicates(dataset):
    dataset = dataset.drop_duplicates()
    return dataset

#HANDLE IMPOSSIBLE VALUES
def check_impossible_values(dataset):
    return dataset

#DROP COLUMNS
def drop_column(dataset, columns):
    dataset.drop(columns, axis = 1, inplace = True)
    return dataset

#HANDLE MISSING VALUES
def handle_missing_values(dataset):
    #lifetime spend... columns
    spend_cols = [col for col in dataset.columns if 'lifetime_spend' in col] #onde é nulo, é porque provavelmenet o cliente nunca la foi
    dataset[spend_cols] = dataset[spend_cols].fillna(0) 

    #customer birthdate
    current_year = datetime.now().year
    dataset['customer_age'] = current_year - dataset['customer_birthdate'].dt.year
    drop_column(dataset, ['customer_birthdate'])
    

    #KNN imputation for numerical columns, but first we need to scale the data 
    #numerical columns (kids_home, teens_home, number_complaints, distinct_stores_visited, typical_hour, percentage_of_products_bought_promotion)
    numeric_cols = dataset.select_dtypes(include=['int64', 'float64', 'Int64']).columns
    if len(numeric_cols) > 0:
        scaler = StandardScaler()
        imputer = KNNImputer(n_neighbors=5)
        
        scaled_data = scaler.fit_transform(dataset[numeric_cols])
        imputed_data = imputer.fit_transform(scaled_data)
        dataset[numeric_cols] = scaler.inverse_transform(imputed_data) #to get the original scale back so we can find outliers and round the values
    
    dataset['percentage_of_products_bought_promotion'] = dataset['percentage_of_products_bought_promotion'].clip(0.0, 1.0)
        
    count_cols = ['kids_home', 'teens_home', 'number_complaints', 'distinct_stores_visited', 'typical_hour']
    for col in count_cols:
        if col in dataset.columns:
            dataset[col] = dataset[col].round().astype('Int64')
        
    return dataset
    

#HANDLE OUTLIERS
def handle_outliers(dataset):
    return dataset

#FEATURE ENGINEERING
def feature_engineering(dataset):
    dataset['total_children'] = dataset['kids_home'] + dataset['teens_home']
    #dataset['has_children'] = 
    #create time of the day bins 'night' -> 00:00 - 05:59 etc.
    #create a cycliclal encoding for the hours (to let the model know that 23 and 00 are neighbours)
    return dataset

#SCALING DATA
def scale_data(dataset):
    return dataset



def clean_data():
    """
    This function contains all the other "mini" functions.
    """

    pass
