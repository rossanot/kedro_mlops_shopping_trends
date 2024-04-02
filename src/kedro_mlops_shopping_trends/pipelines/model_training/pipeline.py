"""
This is a boilerplate pipeline 'model_training'
generated using Kedro 0.18.14
"""

from kedro.pipeline import Pipeline, pipeline, node
from .nodes import (model_train, model_evaluate, train_feature_select)


def create_pipeline(**kwargs) -> Pipeline:
    baseline = pipeline(
        [
            node(
                func=model_train,
                inputs=[
                    'params:classifier',
                    'X_train',
                    'y_train'
                ],
                outputs='model_output',
                name='train_baseline'
                ),
            node(
                func=model_evaluate,
                inputs=[
                    'model_output',
                    'X_val',
                    'y_val',
                ],
                outputs='scores_output',
                name='evaluate_baseline'
            )
        ]),
    feature_selection = pipeline(
        [
            node(
                func=train_feature_select,
                inputs=[
                    'params:classifier',
                    'X_train',
                    'X_val',
                    'y_train',
                ],
                outputs=['model_output', '_X_val'],
                name='train_feature_selection',
            ),
            node(
                func=model_evaluate,
                inputs=[
                    'model_output',
                    '_X_val',
                    'y_val',
                ],
                outputs='scores_output',
                name='evaluate_select_features'
            )
            ]
            )

    baseline_inter = pipeline(
        pipe=baseline,
        inputs={
            'X_train': 'X_train_intermediate',
            'X_val': 'X_val_intermediate',
            'y_train': 'y_train_intermediate',
            'y_val': 'y_val_intermediate'
            },
        outputs={
            'model_output': 'dt_baseline_inter',
            'scores_output': 'dt_baseline_scores'
            },
        namespace='baseline'
        )

    feature_select_inter = pipeline(
        pipe=feature_selection,
        inputs={
            'X_train': 'X_train_intermediate',
            'X_val': 'X_val_intermediate',
            'y_train': 'y_train_intermediate',
            'y_val': 'y_val_intermediate',
            },
        outputs={
            'model_output': 'dt_feature_selection_inter',
            'scores_output': 'dt_feature_selection_scores'
            },
        namespace='feature_selection'
        )

    return baseline_inter + feature_select_inter