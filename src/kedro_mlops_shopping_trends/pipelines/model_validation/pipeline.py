"""
This is a boilerplate pipeline 'model_validation'
generated using Kedro 0.18.14
"""
from pathlib import Path
from kedro.config import OmegaConfigLoader
from kedro.framework.project import settings

from kedro.pipeline import Pipeline, pipeline, node
from .nodes import (model_evaluate,
                    conf_matrix,
                    auc_roc)

PATH = './'
conf_path = str(Path(PATH) / settings.CONF_SOURCE)
conf_loader = OmegaConfigLoader(conf_source=conf_path)
stage = conf_loader['parameters']['model_training']['dataset_stage']


stage_datasets = {
    'baseline': {
        'inputs': {
            'y_true': 'y_val_' + stage,
            'y_predicted': 'dt_baseline_val_ypredicted_' + stage
            },
        'outputs': {
            'scores': 'dt_baseline_scores_' + stage,
            'cm': 'dt_baseline_cm_val_' + stage,
            'aucroc': 'dt_baseline_auc_val_' + stage
            }
        },
    'cv_validation': {
        'inputs': {
            'y_true': 'y_val_' + stage,
            'y_predicted': 'dt_cv_val_ypredicted_' + stage
            },
        'outputs': {
            'scores': 'dt_cv_val_scores_' + stage,
            'cm': 'dt_cv_cm_val_' + stage,
            'aucroc': 'dt_cv_auc_val_' + stage
            }
        },
    'cv_test': {
        'inputs': {
            'y_true': 'y_test_' + stage,
            'y_predicted': 'dt_cv_test_ypredicted_' + stage
            },
        'outputs': {
            'scores': 'dt_cv_test_scores_' + stage,
            'cm': 'dt_cv_cm_test_' + stage,
            'aucroc': 'dt_cv_auc_test_' + stage
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
            **stage_datasets['baseline']['inputs']
            },
        outputs={
            **stage_datasets['baseline']['outputs']
            },
        namespace='model_validation'
    )

    eval_cv_val = pipeline(
        pipe=evaluate,
        inputs={
            **stage_datasets['cv_validation']['inputs']
                },
        outputs={
            **stage_datasets['cv_validation']['outputs']
            },
        namespace='model_validation'
    )

    eval_cv_test = pipeline(
        pipe=evaluate,
        inputs={
            **stage_datasets['cv_test']['inputs'],
        },
        outputs={
            **stage_datasets['cv_test']['outputs'],
            },
        namespace='model_validation'
    )

    return eval_baseline + eval_cv_val + eval_cv_test
