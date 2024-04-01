"""
This is a boilerplate pipeline 'model_training'
generated using Kedro 0.18.14
"""

from kedro.pipeline import Pipeline, pipeline, node
from .nodes import (train_baseline, train_feature_select)


def create_pipeline(**kwargs) -> Pipeline:
    baseline_model = pipeline(
        [
            node(
                func=train_baseline,
                inputs=[
                    'X_train',
                    'X_val',
                    'y_train',
                    'y_val'
                ],
                outputs='baseline_trained',
                name='train_baseline_model'
                ),
        ]),
    feature_selection = pipeline(
        [
            node(
                func=train_feature_select,
                inputs=[
                    'X_train',
                    'X_val',
                    'y_train',
                    'y_val'
                ],
                outputs='feature_selection_trained',
                name='train_feature_selection',
            )
            ]
            )

    baseline_inter = pipeline(
        pipe=baseline_model,
        inputs={
            'X_train': 'X_train_intermediate',
            'X_val': 'X_val_intermediate',
            'y_train': 'y_train_intermediate',
            'y_val': 'y_val_intermediate',
            },
        outputs={
            'baseline_trained': 'dt_baseline_inter'
            },
        namespace='baseline_intermediate'
        )

    feature_selection = pipeline(
        pipe=feature_selection,
        inputs={
            'X_train': 'X_train_intermediate',
            'X_val': 'X_val_intermediate',
            'y_train': 'y_train_intermediate',
            'y_val': 'y_val_intermediate',
            },
        outputs={
            'feature_selection_trained': 'dt_feature_selection_inter'
            },
        namespace='feature_selection_intermediate'
        )

    return baseline_inter + feature_selection