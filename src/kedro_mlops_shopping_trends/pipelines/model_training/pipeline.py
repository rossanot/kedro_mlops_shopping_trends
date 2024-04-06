"""
This is a boilerplate pipeline 'model_training'
generated using Kedro 0.18.14
"""

from kedro.pipeline import Pipeline, pipeline, node
from .nodes import (model_train,
                    model_predict,
                    model_evaluate,
                    get_reduced_x,
                    grid_search)


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
                func=model_predict,
                inputs=[
                    'model_output',
                    'X_val'
                ],
                outputs='y_predicted',
                name='baseline_predictions'
            )
        ]),
    cross_validation = pipeline(
        [
            node(
                func=get_reduced_x,
                inputs=[
                    'X_train',
                    'X_val',
                    'y_train',
                ],
                outputs=[
                    '_X_train',
                    '_X_val',
                    'features',
                ],
                name='feature_selection',
            ),
            node(
                func=grid_search,
                inputs=[
                    'params:classifier',
                    '_X_train',
                    'y_train',
                    'params:hyperparams',
                    'params:kfold'
                ],
                outputs='model_output',
                name='evaluate_select_features'
            ),
            node(
                func=model_predict,
                inputs=[
                    'model_output',
                    '_X_val',
                ],
                outputs='y_predicted',
                name='cross_validation_predictions'
            )
            ]
            )

    baseline_inter = pipeline(
        pipe=baseline,
        inputs={
            'X_train': 'X_train_intermediate',
            'X_val': 'X_val_intermediate',
            'y_train': 'y_train_intermediate',
            },
        outputs={
            'model_output': 'dt_baseline_inter',
            'y_predicted': 'dt_baseline_y_predicted'
            },
        namespace='model_intermediate'
        )

    cross_validation_train = pipeline(
        pipe=cross_validation,
        inputs={
            'X_train': 'X_train_intermediate',
            'X_val': 'X_val_intermediate',
            'y_train': 'y_train_intermediate'
            },
        outputs={
            'features': 'dt_cv_features',
            'model_output': 'dt_cv_inter',
            'y_predicted': 'dt_cv_y_predicted'
            },
        namespace='model_intermediate'
        )

    return baseline_inter + cross_validation_train