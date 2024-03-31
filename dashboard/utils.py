from typing import Dict
from pathlib import Path
import re
import yaml

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
    """Get data file path using ConfiLloader
    """
    configure_item = _get_config_item('catalog')
    return configure_item[catalog_file]['filepath']


def get_features(layer: str) -> Dict:
    """Get pd.DataFrame features using ConfiLloader
    """
    configure_item = _get_config_item('parameters')
    return configure_item[layer]['features']


def read_datafile(file_path: str) -> pd.DataFrame:
    """Load data file
    """
    if re.search('.csv$', file_path):
        return pd.read_csv(file_path)
    return pd.read_parquet(file_path)


# visualization
