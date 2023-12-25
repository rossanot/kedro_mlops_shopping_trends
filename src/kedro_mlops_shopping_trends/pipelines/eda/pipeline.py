"""
This is a boilerplate pipeline 'eda'
generated using Kedro 0.18.14
"""

from kedro.pipeline import Pipeline, pipeline, node
from .nodes import (get_description, get_mult_bar_plot, get_box_plot, \
                    get_bar_plot, get_hist_plot, get_corr_plot)


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline(
        [
            node(
                name='EDA_Raw_Stats',
                func=get_description,
                inputs='shopping_raw',
                outputs='shopping_raw_stats',
            ),
            node(
                name='EDA_Raw_Multiple_Barplot',
                func=get_mult_bar_plot,
                inputs='shopping_raw',
                outputs='shopping_raw_hbar',
            ),
            node(
                name='EDA_Raw_Boxplot',
                func=get_box_plot,
                inputs=['shopping_raw', 'params:box_plot'],
                outputs=['shopping_raw_box_gender', 'shopping_raw_box_category', \
                         'shopping_raw_box_season'],
            ),
            node(
                name='EDA_Raw_Barplot',
                func=get_bar_plot,
                inputs=['shopping_raw', 'params:bar_plot'],
                outputs=['shopping_raw_bar_gender', 'shopping_raw_bar_category', \
                         'shopping_raw_bar_season'],
            ),
            node(
                name='EDA_Raw_Histplot',
                func=get_hist_plot,
                inputs=['shopping_raw', 'params:hist_plot'],
                outputs=['shopping_raw_hist_age', \
                         'shopping_raw_hist_purchase_amount', \
                         'shopping_raw_hist_prev_purchase',
                         'shopping_raw_hist_rating'],
            ),
            node(
                name='EDA_Raw_Correlation_Plot',
                func=get_corr_plot,
                inputs=['shopping_raw', 'params:corr_plot'],
                outputs='shopping_raw_correlation',
            ),
        ]
        )
