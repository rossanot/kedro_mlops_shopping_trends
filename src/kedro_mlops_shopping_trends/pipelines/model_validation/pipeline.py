"""
This is a boilerplate pipeline 'model_validation'
generated using Kedro 0.18.14
"""

from kedro.pipeline import Pipeline, pipeline, node
from .nodes import (model_evaluate,
                    conf_matrix,
                    auc_roc)


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

    eval_baseline_inter = pipeline(
        pipe=evaluate,
        inputs={'y_true': 'y_val_intermediate',
                'y_predicted': 'dt_baseline_val_ypredicted_inter'},
        outputs={
            'scores': 'dt_baseline_scores_inter',
            'cm': 'dt_baseline_cm_val_inter',
            'aucroc': 'dt_baseline_auc_val_inter',
            },
        namespace='model_validation'
    )

    eval_cv_val_inter = pipeline(
        pipe=evaluate,
        inputs={'y_true': 'y_val_intermediate',
                'y_predicted': 'dt_cv_val_ypredicted_inter'
                },
        outputs={
            'scores': 'dt_cv_val_scores_inter',
            'cm': 'dt_cv_cm_val_inter',
            'aucroc': 'dt_cv_auc_val_inter',
            },
        namespace='model_validation'
    )

    eval_cv_test_inter = pipeline(
        pipe=evaluate,
        inputs={'y_true': 'y_test_intermediate',
                'y_predicted': 'dt_cv_test_ypredicted_inter'},
        outputs={
            'scores': 'dt_cv_test_scores_inter',
            'cm': 'dt_cv_cm_test_inter',
            'aucroc': 'dt_cv_auc_test_inter',
            },
        namespace='model_validation'
    )

    return eval_baseline_inter + eval_cv_val_inter + eval_cv_test_inter
