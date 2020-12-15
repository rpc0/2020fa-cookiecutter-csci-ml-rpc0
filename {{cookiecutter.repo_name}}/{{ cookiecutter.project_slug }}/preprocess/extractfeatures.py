import re

def extract_features_from_text_column(ddf, existing_text_feature_name, new_feature_name, extract_words):
    ''' Sample extraction function, useful for feature engineering
    Does regex search in the description column. Adds new binary column if any of the extract words are found
    It assumes that the data set is already cleaned and contains no NA values

    :param ddf: dask dataframe
             Dataframe object to be modified
    :param existing_text_feature_name: string
             Feature name of existing column from which to extract
    :param new_feature_name: string
             Feature name to be added to the df
    :param extract_words: list of strings
             Word list to be searched
    :return: Modified dataframe
    '''

    check_regex = (r'\b(?:{})\b'.format('|'.join(map(re.escape, extract_words))))

    ddf[new_feature_name] = (ddf[existing_text_feature_name].str.contains(check_regex, regex=True).astype('uint8'))

    return ddf


def extract_features_from_dask_dataframe(ddf):
    ''' Customize as appropriate for your dataset
    Extracts features from the dataset and adds new columns as needed, also cleans up after feature engineering
    :param ddf: dask dataset
                Dataset to be engineered with new features
    :return: Modified dataframe
    '''

    # TODO: Edit here to specify logic for new features
    # e.g. is_city = ["Boston", "Seattle"]
    # desc_extracting dict = {"is_city": is_city}


    # Add the new features to train and test datasets
    for key, value in desc_extracting_dict.items():
        ddf = extract_features_from_text_column(ddf, key, value)

    # TODO: Add any other feature engineering calls before returning the modfiied dataframe

    return ddf
