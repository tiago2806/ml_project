
import pandas as pd


def clean_data(dataset):
    dataset.drop_duplicates(inplace=True)
    return dataset

def handle_datatypes(dataset):
    dataset['customer_birthdate'] = pd.to_datetime(dataset['customer_birthdate'], errors='coerce')
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

