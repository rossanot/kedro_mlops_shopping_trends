from typing import Dict, List, Tuple
from pathlib import Path
import re

import pandas as pd
from kedro.config import OmegaConfigLoader
from kedro.framework.project import settings


def _get_config_item(item: str = 'catalog'):
    """Load ConfigLoader
    """
    conf_path = str(Path.cwd() / settings.CONF_SOURCE)
    conf_loader = OmegaConfigLoader(conf_source=conf_path, env="local")
    return conf_loader[item]


def get_filepath(catalog_file: str) -> Dict:
    """Get data file path using ConfigLoader
    """
    configure_item = _get_config_item('catalog')
    try:
        return configure_item[catalog_file]['filepath']
    except KeyError:
        return configure_item[catalog_file]['dataset']['filepath']


def get_features_from_catalog(layer: str) -> Dict:
    """Get pd.DataFrame features using ConfigLoader
    """
    configure_item = _get_config_item('parameters')
    return configure_item[layer]['features']


def get_features_dynamically(df: pd.DataFrame) -> Tuple[List, List]:
    """Get pd.DataFrame features dynamically
    """
    categorical = df.select_dtypes(include='object').columns.to_list()
    numerical = df.select_dtypes(
        include=['float64', 'int64', 'int32']
        ).columns.to_list()

    return (categorical, numerical)


def read_datafile(file_path: str) -> pd.DataFrame:
    """Load data file
    """
    if re.search('.csv$', file_path):
        return pd.read_csv(file_path)
    
    return pd.read_parquet(file_path)


# visualization
