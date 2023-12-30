"""
This is a boilerplate pipeline 'data_processing'
generated using Kedro 0.18.14
"""

from kedro.pipeline import Pipeline, pipeline, node
from .nodes import (get_intermediate, get_primary)


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline([
        node(
            func=get_intermediate,
            inputs='shopping_raw',
            outputs='shopping_02_intermediate',
            name='get_intermediate_data',
            ),
        node(
            func=get_primary,
            inputs='shopping_02_intermediate',
            outputs='shopping_03_primary',
            name='get_primary_data',
        )
    ])
