

def clean_data(dataset):
    dataset.drop_duplicates(inplace=True)
    return dataset