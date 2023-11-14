"""
This is a boilerplate pipeline 'data_acquisition'
generated using Kedro 0.18.14
"""

from kedro.pipeline import Pipeline, node, pipeline
from .nodes import request_kaggle_dataset


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline(
        [
            node(
                name='Download_dataset',
                func=request_kaggle_dataset,
                inputs=['params:kaggle_parms'],
                outputs=None
        ),
        #     node(
        #         name='get_data',
        #         func=get_raw_dataset,
        #         inputs=['kaggle_dataset'],
        #         outputs=None
        # ),
    ]
)
