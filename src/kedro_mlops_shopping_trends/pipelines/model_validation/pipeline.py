"""
This is a boilerplate pipeline 'model_validation'
generated using Kedro 0.18.14
"""
from kedro.pipeline import Pipeline, pipeline, node
from kedro_mlops_shopping_trends.pipelines.utils import data_layer
from .nodes import (model_evaluate,
                    conf_matrix,
                    auc_roc)

layer = data_layer()

layer_datasets = {
    'baseline': {
        'inputs': {
            'y_true': 'y_val_' + layer,
            'y_predicted': 'baseline_val_ypredicted_' + layer
            },
        'outputs': {
            'scores': 'baseline_scores_' + layer,
            'cm': 'baseline_cm_val_' + layer,
            'aucroc': 'baseline_auc_val_' + layer
            }
        },
    'grid_search_validation': {
        'inputs': {
            'y_true': 'y_val_' + layer,
            'y_predicted': 'grid_search_val_ypredicted_' + layer
            },
        'outputs': {
            'scores': 'grid_search_val_scores_' + layer,
            'cm': 'grid_search_cm_val_' + layer,
            'aucroc': 'grid_search_auc_val_' + layer
            }
        },
    'grid_search_test': {
        'inputs': {
            'y_true': 'y_test_' + layer,
            'y_predicted': 'grid_search_test_ypredicted_' + layer
            },
        'outputs': {
            'scores': 'grid_search_test_scores_' + layer,
            'cm': 'grid_search_cm_test_' + layer,
            'aucroc': 'grid_search_auc_test_' + layer
            }
            }
            }


def create_pipeline(**kwargs) -> Pipeline:
    evaluate = pipeline(
        [
            node(
                func=model_evaluate,
                inputs=['y_true', 'y_predicted'],
                outputs='scores'
            ),
            node(
                func=conf_matrix,
                inputs=['y_true', 'y_predicted'],
                outputs='cm'
            ),
            node(
                func=auc_roc,
                inputs=['y_true', 'y_predicted'],
                outputs='aucroc'
            )
            ])

    eval_baseline = pipeline(
        pipe=evaluate,
        inputs={
            **layer_datasets['baseline']['inputs']
            },
        outputs={
            **layer_datasets['baseline']['outputs']
            },
        namespace='model_validation'
    )

    eval_grid_search_val = pipeline(
        pipe=evaluate,
        inputs={
            **layer_datasets['grid_search_validation']['inputs']
                },
        outputs={
            **layer_datasets['grid_search_validation']['outputs']
            },
        namespace='model_validation'
    )

    eval_grid_search_test = pipeline(
        pipe=evaluate,
        inputs={
            **layer_datasets['grid_search_test']['inputs'],
        },
        outputs={
            **layer_datasets['grid_search_test']['outputs'],
            },
        namespace='model_validation'
    )

    return eval_baseline + eval_grid_search_val + eval_grid_search_test
