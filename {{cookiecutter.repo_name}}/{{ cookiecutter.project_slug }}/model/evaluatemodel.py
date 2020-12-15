
def evaluate_model(model, test_ddf):
    ''' FRAMEWORK EXAMPLE - You can leave it mostly as is, customize label and model as needed
     Generate predictions using the model and test dataset

    :param model: model object
             Model object containing already fitted model
    :param test_ddf: dask dataframe
             Dataframe object containing test set
    :return: Dask series containing predictions of label for each row of features in test set
    '''

    # Specify the column name you want as the label on which to train the model
    label = "<add here>"

    # FRAMEWORK CODE - Modify at your own peril
    y_test = test_ddf[label]
    X_test = test_ddf.drop(label, axis=1)

    y_predicted = model.predict(X_test)
    print(type(y_predicted))
    # END FRAMEWORK CODE

    # TODO - Add scoring function here such as MSE

    # FRAMEWORK CODE - Modify at your own peril
    return y_predicted

