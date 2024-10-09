"""
This is a boilerplate pipeline 'model_validation'
generated using Kedro 0.18.14
"""
from typing import Dict
import pandas as pd
from kedro_mlops_shopping_trends.pipelines.utils import get_params
import matplotlib.pyplot as plt
from sklearn.metrics import (f1_score,
                             accuracy_score,
                             recall_score
                             )
from sklearn.metrics import (
    ConfusionMatrixDisplay,
    RocCurveDisplay)

import logging
logger = logging.getLogger(__name__)

steps = {'intermediate': 0, 'primary': 1, 'feature': 2}
layer = get_params('model_validation', 'data_layer')
classifier = get_params('model_validation', 'classifier')


def model_evaluate(
        y_true: pd.DataFrame,
        y_predicted: pd.DataFrame
        ) -> Dict:
    """Evaluate classifier

    :param y_predicted: predicted labels pd.DataFrame
    :param y_true: true labels pd.DataFrame
    :return: scores Dict
    """
    stage = get_params('model_validation', 'data_layer')

    fscore = f1_score(y_true.to_numpy(), y_predicted)
    acc = accuracy_score(y_true.to_numpy(), y_predicted)
    recall = recall_score(y_true.to_numpy(), y_predicted)

    # log on screen
    logger.info('F-score: {:.3f}'.format(fscore))
    logger.info('Accuracy: {:.3f}'.format(acc))
    logger.info('Recall: {:.3f}'.format(recall))

    metrics = {
        'F1-score': {'value': fscore, 'step': steps[stage]},
        'Accuracy': {'value': acc, 'step': steps[stage]},
        'Recall': {'value': recall, 'step': steps[stage]}
        }

    return metrics


def conf_matrix(
        y_true: pd.DataFrame,
        y_predicted: pd.DataFrame
        ) -> plt.Figure:
    """Plot confusion matrix
    """
    title = classifier + ' ' + layer + ' ' + 'Confusion Matrix'

    fig, ax = plt.subplots(figsize=(10, 5))
    ConfusionMatrixDisplay.from_predictions(y_true, y_predicted, ax=ax)
    ax.set_title(title)
    return fig


def auc_roc(
        y_true: pd.DataFrame,
        y_predicted: pd.DataFrame,
        title: str = 'AUC-ROC Curve'
        ) -> plt.Figure:
    """Plot AUC-ROC curve
    """
    title = classifier + ' ' + layer + ' ' + 'AUC-ROC Curve'

    fig, ax = plt.subplots(figsize=(10, 5))
    RocCurveDisplay.from_predictions(
        y_true,
        y_predicted,
        ax=ax)
    ax.set_title(title)

    return fig
