"""
This is a boilerplate pipeline 'eda'
generated using Kedro 0.18.14
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from typing import Any, List, Dict

def get_description(dataset: Any) -> pd.DataFrame:
    """Get basic statistical descriptors of the dataset

    :param dataset: _description_
    :type dataset: Any
    :return: pd.DataFrame
    """

    df = pd.read_csv(dataset)
    return df.describe()


def _get_categ_features(df: pd.DataFrame) -> List[str]:
    """Get categorical features

    :param df: A dataframe
    :type df: pd.DataFrame
    :return: A list of features of object type
    """    
    return df.select_dtypes(include='object').columns.to_list()


def get_mult_bar_plot(df: pd.DataFrame):
    """Get bar plot

    :param df: the entire dataframe
    :type df: pd.DataFrame
    :return: a matplotlib object
    """    

    features = _get_categ_features(df)
    a, b = int(len(features)/3)+1, 3
    c = 1

    fig = plt.figure(figsize=(25, 55))
    for feature in features:
        plt.subplot(a, b, c)
        plt.barh(list(df[feature].value_counts().index), \
                    df[feature].value_counts().values)
        plt.xticks(rotation=45)
        plt.xlabel('Count')
        plt.ylabel(feature)
        c+=1

    return fig


def get_box_plot(df: pd.DataFrame, features: Dict) -> List:
    """Generate box plot

    :param df: the entire dataframe
    :type df: pd.DataFrame
    :param features: a Dict containing the features to plot
    :type features: Dict
    :return: a list of matplotlib objects
    """
    figs = []
    for feature in features['features']:
        fig = plt.figure(figsize=(5, 5))
        sns.boxplot(data=df, x=feature, y='Review Rating', hue=feature)
        
        figs.append(fig)

    return figs