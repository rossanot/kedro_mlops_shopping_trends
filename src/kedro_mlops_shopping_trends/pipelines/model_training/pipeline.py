"""
This is a boilerplate pipeline 'model_training'
generated using Kedro 0.18.14
"""

from kedro.pipeline import Pipeline, pipeline, node
from .nodes import (train_baseline)


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
                outputs='trained_model',
                name='train_baseline_model'
                ),
        ])

    baseline_inter = pipeline(
        pipe=baseline_model,
        inputs={
            'X_train': 'X_train_intermediate',
            'X_val': 'X_val_intermediate',
            'y_train': 'y_train_intermediate',
            'y_val': 'y_val_intermediate',
            },
        outputs={
            'trained_model': 'dt_baseline_inter'
            },
        namespace='baseline_intermediate'
        )

    return baseline_inter