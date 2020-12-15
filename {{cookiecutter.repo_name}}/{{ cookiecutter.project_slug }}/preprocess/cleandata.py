import numpy as np

def clean_data(ddf, drop_columns, target_name):
    ''' FRAMEWORK EXAMPLE - You can leave it mostly as is unless you have custom cleaning to do
    Dropping unnecessary columns, duplicate rows and empty rows of label or target.

    :param ddf: dask dataframe
            Dataframe object to be cleaned
    :param drop_columns: list of strings
            Column names to be dropped
    :param target_name: string
            Name of the target variable
    :return: Cleaned dataframe
    '''

    # Drop the columns asked to be dropped
    ddf = ddf.drop(columns=drop_columns)

    # Drop rows that are duplicate based on all columns, except index
    ddf = ddf.drop_duplicates(ignore_index=True)

    # Drop all rows where the numeric columns contain nan
    numeric_columns = list(ddf.select_dtypes(include=[np.number]).columns.values)
    ddf = ddf.dropna(subset=numeric_columns, how="any").reset_index(drop=True)

    # # Drop all columns with object datatypes having null values
    # object_columns = [x for x in list(ddf.columns) if x not in numeric_columns]
    # ddf = ddf.filter(ddf[object_columns].isNotNull())    

    # Drop rows with label column having null values
    ddf = ddf.dropna(subset=[target_name], how="any").reset_index(drop=True)

    return ddf


def clean_datasets(ddf):
    ''' FRAMEWORK CODE - Input drop_columns and target_name. Leave the rest alone, or add other cleaning functions
     Call functions to clean the dask dataframe.

    :param ddf: dask dataframe
             Dataframe object to be cleaned
    :return: Cleaned dataframe
    '''

    # Specify list of columns to drop.
    drop_columns = [<Add yours here>]

    # Specify label here.
    target_name = "<Add yours here>"

    # FRAMEWORK CODE - Add other functions to clean in other ways
    return clean_data(ddf=ddf, drop_columns=drop_columns, target_name=target_name)

