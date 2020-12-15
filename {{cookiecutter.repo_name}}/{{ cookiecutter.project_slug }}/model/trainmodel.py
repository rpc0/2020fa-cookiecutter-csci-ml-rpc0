def train_model(train_ddf):
    ''' FRAMEWORK EXAMPLE - You can leave it mostly as is, customize label and model as needed
    Define label, extract train X and y from dask ddf, define model, fit model, return the history and model

    :param train_ddf: dask dataframe
            Dataframe object containing training set
    :return: Fitted model and history from model.fit
    '''

    # Specify your label, the column on which to run the model training
    label = "<Add yours here>"

    # FRAMEWORK CODE - Modify at your own peril
    y = train_ddf[label]
    X = train_ddf.drop(label, axis=1)
    # END FRAMEWORK CODE

    # TODO - Add model definition here. All sklearn models supported. TF/Keras support pending
    model =

    # FRAMEWORK CODE - Modify at your own peril
    history = model.fit(X, y)

    return model, history