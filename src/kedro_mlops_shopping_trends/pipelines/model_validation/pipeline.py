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
            'y_predicted': 'dt_baseline_val_ypredicted_' + layer
            },
        'outputs': {
            'scores': 'dt_baseline_scores_' + layer,
            'cm': 'dt_baseline_cm_val_' + layer,
            'aucroc': 'dt_baseline_auc_val_' + layer
            }
        },
    'cv_validation': {
        'inputs': {
            'y_true': 'y_val_' + layer,
            'y_predicted': 'dt_cv_val_ypredicted_' + layer
            },
        'outputs': {
            'scores': 'dt_cv_val_scores_' + layer,
            'cm': 'dt_cv_cm_val_' + layer,
            'aucroc': 'dt_cv_auc_val_' + layer
            }
        },
    'cv_test': {
        'inputs': {
            'y_true': 'y_test_' + layer,
            'y_predicted': 'dt_cv_test_ypredicted_' + layer
            },
        'outputs': {
            'scores': 'dt_cv_test_scores_' + layer,
            'cm': 'dt_cv_cm_test_' + layer,
            'aucroc': 'dt_cv_auc_test_' + layer
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

    eval_cv_val = pipeline(
        pipe=evaluate,
        inputs={
            **layer_datasets['cv_validation']['inputs']
                },
        outputs={
            **layer_datasets['cv_validation']['outputs']
            },
        namespace='model_validation'
    )

    eval_cv_test = pipeline(
        pipe=evaluate,
        inputs={
            **layer_datasets['cv_test']['inputs'],
        },
        outputs={
            **layer_datasets['cv_test']['outputs'],
            },
        namespace='model_validation'
    )

    return eval_baseline + eval_cv_val + eval_cv_test
