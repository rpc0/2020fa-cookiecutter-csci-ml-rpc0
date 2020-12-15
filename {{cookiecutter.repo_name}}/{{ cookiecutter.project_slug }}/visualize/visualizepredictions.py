import matplotlib.pyplot as plt
import pandas as pd

def plot_predicted_vs_actual(x, predictions, actuals):
    '''
    Plots predicted vs actuals
    :param x: series
            x values useful for scatterplots
    :param predictions: series
            Series containing predictions from model evaluation
    :param actuals: series
            Series containing actual values, e.g. from test set
    :return: matplotlib fig to display or save
    '''

    fig = plt.figure(figsize=(30, 15))

    fig, ax = plt.subplots()
    plt.rcParams['font.size'] = 24

    # ax.scatter(x = range(0, actuals.size), y=actuals, c = 'blue', label = 'Actual', alpha = 0.3)
    # ax.scatter(x = range(0, predictions.size), y=predictions, c = 'red', label = 'Predicted', alpha = 0.3)
    # plt.title('Actual and predicted values')
    # plt.xlabel('Observations')
    # plt.ylabel('mpg')
    # plt.legend()

    diff = actuals - predictions
    diff.hist(bins = 20)
    plt.title('Histogram of prediction errors')
    plt.xlabel('Prediction error')
    plt.ylabel('Frequency')

    return fig


def visualizepredictions(y_predicted, test_ddf):
    ''' FRAMEWORK CODE - Only modify label and x_axis_column name
    Called by orchstrator to visualize predictions
    :param y_predicted: numpy array
                    Contains predicted values of the label
    :param test_ddf: dataframe
                    Test set
    :return: matplotlib fig to display or save
    '''

    label = "<Add yours here>"
    x_axis_column = "<Add yours here>"

    y_test = test_ddf[label]
    x = test_ddf[x_axis_column]

    # Convert predictions which is a numpy array to a pandas series
    # Convert actuals which is a Dask series to a pandas series
    predictions = pd.Series(y_predicted)
    actuals = y_test.compute()
    
    return plot_predicted_vs_actual(x, predictions, actuals)