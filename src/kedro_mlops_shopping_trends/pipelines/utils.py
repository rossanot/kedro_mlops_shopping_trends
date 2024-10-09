from pathlib import Path
from kedro.config import OmegaConfigLoader
from kedro.framework.project import settings


def get_params(pipeline: str,
               param: str) -> str:
    """Get the data layer from the model_training .yaml file

    :return: The dataset_stage parameter
    """
    PATH = './'
    conf_path = str(Path(PATH) / settings.CONF_SOURCE)
    conf_loader = OmegaConfigLoader(conf_source=conf_path)
    return conf_loader['parameters'][pipeline][param]
