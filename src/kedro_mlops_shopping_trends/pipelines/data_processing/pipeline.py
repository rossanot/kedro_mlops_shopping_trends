"""
This is a boilerplate pipeline 'data_processing'
generated using Kedro 0.18.14
"""

from kedro.pipeline import Pipeline, pipeline, node
from .nodes import (get_intermediate, split_data, get_primary)


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline([
        node(
            func=get_intermediate,
            inputs='shopping_raw',
            outputs='shopping_02_intermediate',
            name='get_intermediate_data',
            ),
        node(
            func=split_data,
            inputs=[
                'shopping_02_intermediate',
                'params:split_data',
                'params:features'],
            outputs=[
                '_X_train',
                '_X_test',
                'y_train',
                'y_test'
                ],
            name='split_data',
        ),
        node(
            func=get_primary,
            inputs=['_X_train', '_X_test', 'params:features'],
            outputs=['X_train', 'X_test'],
            name='get_primary_data',
        )
    ])
