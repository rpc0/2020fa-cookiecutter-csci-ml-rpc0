from dask_ml.preprocessing import OrdinalEncoder, Categorizer

def encode_categorical_data(ddf):
    ''' FRAMEWORK CODE - Modify only if you don't want all categorical fields to be encoded or to change encoder
    Encodes all categorical data column-wise in the dask dataframe with OrdinalEncoder
    :param ddf: dataframe
                Dask dataframe that will be encoded
    :return: Dask dataframe with encoded categorical data
    '''
    """encode data with OrdinalEncoder

            Parameters
            ----------
            train_df: dataframe
                training dataframe object to fit and transform
            test_df: dataframe
                test dataframe object to transform

            Returns
            -------
            transformed training and test dataframe
            """

    # Call this function only if this list which should be defined outside the framework and contains 1 or more item.
    # column list to ordinal encode
    categorizer = Categorizer()
    categorizer_series = categorizer.fit_transform(ddf).dtypes
    categorical_columns = list(categorizer_series[categorizer_series == "category"].index)

    # Per https://github.com/dask/dask-ml/issues/362 - workaround to mark columns as categorical
    cat = Categorizer(columns=categorical_columns)
    ddf_cat = cat.fit_transform(ddf)

    # transform train and test datasets
    # create ordinal encode object
    # object assigns -1 to the first-time-seen values of the test set
    ordinal_encoder = OrdinalEncoder(columns=categorical_columns)

    # fit object on the train dataset
    encoded_ddf = ordinal_encoder.fit_transform(ddf_cat)

    return encoded_ddf


def transform_dataframe(ddf):
    ''' FRAMEWORK CODE - Modify only to add additional transformation such as normalization, scaling, encoding, etc.
    Called by orchestrator to transform dask dataframe
    :param ddf: dask dataframe
                Dataframe to be transformed
    :return: Transformed dataframe
    '''
    # transform data
    encoded_data = encode_categorical_data(ddf)

    return encoded_data