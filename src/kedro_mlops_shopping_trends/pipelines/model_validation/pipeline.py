"""
This is a boilerplate pipeline 'model_validation'
generated using Kedro 0.18.14
"""

from kedro.pipeline import Pipeline, pipeline, node
from .nodes import model_evaluate


def create_pipeline(**kwargs) -> Pipeline:
    evaluate = pipeline(
        [
            node(
                func=model_evaluate,
                inputs=['y_true', 'y_predicted'],
                outputs=['scores'],
            )
            ]
            )

    eval_baseline_inter = pipeline(
        pipe=evaluate,
        inputs={'y_true': 'y_val_intermediate',
                'y_predicted': 'dt_baseline_val_ypredicted'},
        outputs={'scores': 'dt_baseline_scores'},
        namespace='model_validation'
    )

    eval_cv_val_inter = pipeline(
        pipe=evaluate,
        inputs={'y_true': 'y_val_intermediate',
                'y_predicted': 'dt_cv_val_ypredicted'},
        outputs={'scores': 'dt_cv_val_scores'},
        namespace='model_validation'
    )

    eval_cv_test_inter = pipeline(
        pipe=evaluate,
        inputs={'y_true': 'y_test_intermediate',
                'y_predicted': 'dt_cv_test_ypredicted'},
        outputs={'scores': 'dt_cv_test_scores'},
        namespace='model_validation'
    )
    
    return eval_baseline_inter + eval_cv_val_inter + eval_cv_test_inter
