"""
This is a boilerplate pipeline 'eda'
generated using Kedro 0.18.14
"""

from kedro.pipeline import Pipeline, pipeline, node
from .nodes import get_mult_bar_plot, get_box_plot


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline(
        [
            node(
                name='EDA_categorical_variables1',
                func=get_mult_bar_plot,
                inputs='shopping_raw',
                outputs='shopping_raw_hbar',
            ),
            node(
                name='EDA_categorical_variables2',
                func=get_box_plot,
                inputs=['shopping_raw', 'params:box_plot'],
                outputs=['shopping_raw_box_gender', 'shopping_raw_box_category', 'shopping_raw_box_season'],
            )
        ]
        )
