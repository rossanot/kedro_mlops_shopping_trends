from pathlib import Path
from kedro.config import OmegaConfigLoader
from kedro.framework.project import settings


def data_layer() -> str:
    """Get the data layer from the model_training .yaml file

    :return: The dataset_stage parameter
    """
    PATH = './'
    conf_path = str(Path(PATH) / settings.CONF_SOURCE)
    conf_loader = OmegaConfigLoader(conf_source=conf_path)
    return conf_loader['parameters']['model_training']['data_layer']