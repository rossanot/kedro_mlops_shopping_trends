from pathlib import Path
import re

import pandas as pd
from kedro.config import OmegaConfigLoader
from kedro.framework.project import settings


def get_filepath(catalog_file):
    conf_path = str(Path.cwd() / settings.CONF_SOURCE)
    conf_loader = OmegaConfigLoader(conf_source=conf_path, env="local")
    conf_catalog = conf_loader['catalog']
    return conf_catalog[catalog_file]['filepath']


def read_file(file_path):
    if re.search('.csv$', file_path):
        return pd.read_csv(file_path)
    return pd.read_parquet(file_path)
