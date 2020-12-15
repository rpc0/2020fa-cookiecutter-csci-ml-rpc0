import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

def plot_feature_importance(model, feature_names):
    ''' Sample - modify if you need to plot the feature importance in any other way
    Plots feature importances given the model and feature names as a list
    :param model: model
                Fitted model
    :param feature_names: list of strings
                List of column names in the data set used to fit the model
    :return: matplotlib fig object containing visualization which can be displayed or saved to file
    '''

    feature_importance = (
        pd.DataFrame({
            'feature': feature_names,
            'importance': model.feature_importances_})
        )

    feature_importance = (feature_importance.sort_values(by="importance", ascending=False))

    fig = plt.figure(figsize=(20, 15))
    plt.rcParams['font.size'] = 24
    sns.set(font_scale=1.5, style="whitegrid")
    values = np.array(feature_importance.importance)
    # https://stackoverflow.com/questions/3832809/how-to-change-the-color-of-a-single-bar-if-condition-is-true-matplotlib
    colors = ['grey' if (x < max(values)) else 'red' for x in values ]
    ax = sns.barplot(x="importance", y="feature", data=feature_importance, palette=colors)
    plt.title("Most Significant Features", size =24)

    return fig

def visualizefeaturesignificance(model, ddf):
    ''' FRAMEWORK CODE - Modify only the label
    Called by orchestrator after model is trained to visualize significance of features for the specified label
    :param model: model
                Fitted model
    :param ddf: dataframe
                Dask dataframe used to fit the model.
                Note that this could have been just the list of column names, but passing dataframe to permit changes
    :return: matplotlib fig to be displayed or saved
    '''

    # Specify label or target column name
    label = "<add yours here>"

    # FRAMEWORK CODE begins
    X_test = ddf.drop(label, axis=1)
    features = X_test.columns
    
    return plot_feature_importance(model, features)