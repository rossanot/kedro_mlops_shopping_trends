"""
This is a boilerplate pipeline 'data_acquisition'
generated using Kedro 0.18.14
"""
import os
from pathlib import Path
from typing import Dict
from kedro.config import OmegaConfigLoader
from kedro.framework.project import settings
from typing import Dict


def request_kaggle_dataset(params: Dict) -> None:
    '''
    '''

    conf_path = str(Path('./') / settings.CONF_SOURCE)
    conf_loader = OmegaConfigLoader(conf_source=conf_path)

    credentials = conf_loader["credentials"]

    os.environ['KAGGLE_USERNAME']=credentials['kaggle']['KAGGLE_USERNAME']
    os.environ['KAGGLE_KEY']=credentials['kaggle']['KAGGLE_KEY']
    
    import kaggle

    kaggle.api.dataset_download_file('/'.join([params['user'], params['dataset_name']]),
                                     file_name=params['file_name'],
                                     path='./data/01_raw')