import pandas as pd

#DATA TYPES
def handle_datatypes(dataset):
    dataset['customer_birthdate'] = pd.to_datetime(dataset['customer_birthdate'], errors='coerce')
    dataset['kids_home'] = dataset['kids_home'].astype('Int64')
    dataset['teens_home'] = dataset['teens_home'].astype('Int64')
    dataset['number_complaints'] = dataset['number_complaints'].astype('Int64')
    dataset['distinct_stores_visited'] = dataset['distinct_stores_visited'].astype('Int64')    
    dataset['typical_hour'] = pd.to_datetime('typical_hour').dt.hour


    return dataset

print("olá")

def eliminate_duplicates(dataset):
    dataset.drop_duplicates(inplace=True)
    return dataset


def check_impossible_values(dataset):
    return dataset


def handle_missing_values(dataset):
    spend_cols = [col for col in dataset.columns if 'lifetime_spend' in col] #onde é nulo, é porque provavelmenet o cliente nunca la foi
    dataset[spend_cols] = dataset[spend_cols].fillna(0) 


    return dataset

def handle_outliers(dataset):
    return dataset

def scale_data(dataset):
    return dataset



def clean_data():
    """
    This function contains all the other "mini" functions.
    """

    pass
