"""
This is a boilerplate pipeline 'eda'
generated using Kedro 0.18.14
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from typing import List, Dict


def get_description(df: pd.DataFrame) -> str:
    """Get basic statistical descriptors of the dataset

    :param df: a pd.Dataframe
    :return: str
    """

    return df.describe().to_string()


def _get_categ_features(df: pd.DataFrame) -> List[str]:
    """Get categorical features

    :param df: a pd.Dataframe
    :return: A list of features of object type
    """
    return df.select_dtypes(include='object').columns.to_list()


def get_mult_bar_plot(df: pd.DataFrame) -> plt.figure:
    """Get multiple bar plot

    :param df: a pd.Dataframe
    :return: a matplotlib object
    """

    features = _get_categ_features(df)
    a, b = int(len(features)/3)+1, 3
    c = 1

    fig = plt.figure(figsize=(25, 55))
    for feature in features:
        plt.subplot(a, b, c)
        plt.barh(list(df[feature].value_counts().index), 
                 df[feature].value_counts().values)
        plt.xticks(rotation=45)
        plt.xlabel('Count')
        plt.ylabel(feature)
        c += 1

    return fig


def get_bar_plot(df: pd.DataFrame, params: Dict) -> List:
    """Get bar plot

    :param df: a pd.Dataframe
    :param params: a Dict containing the features to plot
    :return: a list of matplotlib objects
    """
    figs = []
    for feature in params['bar_plot']['features']:
        fig = plt.figure(figsize=(10, 10))
        plt.barh(list(df[feature].value_counts().index),
                 df[feature].value_counts().values)
        plt.xticks(rotation=45)
        plt.xlabel('Count')
        plt.ylabel(feature.replace('_', ' '))
        figs.append(fig)

    return figs


def get_box_plot(df: pd.DataFrame, params: Dict) -> List:
    """Generate box plot

    :param df: a pd.Dataframe
    :param params: a Dict containing the features to plot
    :return: a List of matplotlib objects
    """
    figs = []
    for feature in params['box_plot']['features']:
        fig = plt.figure(figsize=(5, 5))
        sns.boxplot(data=df, x=feature, y='Review Rating', hue=feature)
        
        figs.append(fig)

    return figs


def get_hist_plot(df: pd.DataFrame, params: Dict) -> List:
    """Generate box plot

    :param df: a pd.Dataframe
    :param params: a Dict containing the features to plot
    :return: a List of matplotlib objects
    """
    figs = []
    for feature in params['hist_plot']['features']:
        fig = plt.figure(figsize=(5, 5))
        sns.histplot(data=df, x=feature, kde=True, color='black')

        figs.append(fig)

    return figs


def get_corr_plot(df: pd.DataFrame, params: Dict) -> plt.figure:
    """Generate correlation matrix plot

    :param df: a pd.Dataframe
    :param params: a Dict containing the features to plot
    :return: a matplotlib object
    """

    fig = plt.figure(figsize=(10, 10))
    sns.heatmap(
        df[params['corr_plot']['features']].corr(),
        annot=True,
        cmap="magma", fmt='.2f'
        )
    
    return fig
