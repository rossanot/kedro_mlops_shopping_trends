"""
This is a boilerplate pipeline 'eda'
generated using Kedro 0.18.14
"""

import pandas as pd
import matplotlib.pyplot as plt
from typing import Any

def get_description(dataset: Any) -> pd.DataFrame:
    """Get basic statistical descriptors of the dataset

    :param dataset: _description_
    :type dataset: Any
    :return: pd.DataFrame
    """

    df = pd.read_csv(dataset)
    return df.describe()

def get_corr_plot(df: pd.DataFrame) -> None:
    """Plot a correlation plot for a given pd.DataFrame

    :param df: _description_
    :type df: pd.DataFrame
    """

    plt.matshow(df.corr())
    plt.savefig('')
