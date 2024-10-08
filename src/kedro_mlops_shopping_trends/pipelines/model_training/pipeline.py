"""
This is a boilerplate pipeline 'model_training'
generated using Kedro 0.18.14
"""
from kedro.pipeline import Pipeline, pipeline, node
from kedro_mlops_shopping_trends.pipelines.utils import data_layer
from .nodes import (model_train,
                    model_predict,
                    top_feats_mutual,
                    get_reduced_x,
                    grid_search)

layer = data_layer()

layer_datasets = {
    'baseline': {
        'inputs': {
            'X_train': 'X_train_' + layer,
            'X_val': 'X_val_' + layer,
            'y_train': 'y_train_' + layer
            },
        'outputs': {
            'model_output': 'dt_baseline_' + layer,
            'y_predicted': 'dt_baseline_val_ypredicted_' + layer
            },
            },
    'cv': {
        'inputs': {
            'X_test': 'X_test_' + layer,
        },
        'outputs': {
            'features': 'dt_cv_features_' + layer,
            'model_output': 'dt_cv_' + layer,
            'y_val_predicted': 'dt_cv_val_ypredicted_' + layer,
            'y_test_predicted': 'dt_cv_test_ypredicted_' + layer
        },
            }}


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
                outputs=['y_predicted'],
                name='baseline_predictions'
            )
        ]),
    cross_validation = pipeline(
        [
            node(
                func=top_feats_mutual,
                inputs=[
                    'X_train',
                    'y_train'
                    ],
                outputs='features',
                name='feature_selection'
            ),
            node(
                func=get_reduced_x,
                inputs=[
                    'features',
                    'X_train',
                    'X_val',
                    'X_test'
                ],
                outputs=[
                    '_X_train',
                    '_X_val',
                    '_X_test'
                ],
                name='x_reduction'
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
                name='cross_validation_grid_search'
            ),
            node(
                func=model_predict,
                inputs=[
                    'model_output',
                    '_X_val',
                    '_X_test',
                ],
                outputs=[
                    'y_val_predicted',
                    'y_test_predicted'
                    ],
                name='cross_validation_predictions'
            )
            ]
            )

    baseline_inter = pipeline(
        pipe=baseline,
        inputs={
            **layer_datasets['baseline']['inputs']
            },
        outputs={
            **layer_datasets['baseline']['outputs']
            },
        namespace='model_training'
        )

    cv_train_inter = pipeline(
        pipe=cross_validation,
        inputs={
            **layer_datasets['baseline']['inputs'],
            **layer_datasets['cv']['inputs']
            },
        outputs={
            **layer_datasets['cv']['outputs']
            },
        namespace='model_training'
        )

    return baseline_inter + cv_train_inter
