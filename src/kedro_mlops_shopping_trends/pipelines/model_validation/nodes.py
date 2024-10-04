"""
This is a boilerplate pipeline 'model_validation'
generated using Kedro 0.18.14
"""
from pathlib import Path
from kedro.config import OmegaConfigLoader
from kedro.framework.project import settings

from typing import Dict
import pandas as pd
from sklearn.metrics import (f1_score,
                             accuracy_score,
                             recall_score
                             )
from sklearn.metrics import (confusion_matrix,
                             ConfusionMatrixDisplay,
                             roc_curve,
                             auc,
                             RocCurveDisplay)

import logging
logger = logging.getLogger(__name__)

PATH = './'
conf_path = str(Path(PATH) / settings.CONF_SOURCE)
conf_loader = OmegaConfigLoader(conf_source=conf_path)
stage = conf_loader['parameters']['model_training']['dataset_stage']
steps = {'intermediate': 0, 'primary': 1, 'feature': 2}


def model_evaluate(
        y_true: pd.DataFrame,
        y_predicted: pd.DataFrame
        ) -> Dict:
    """Evaluate classifier

    :param y_predicted: predicted labels pd.DataFrame
    :param y_true: true labels pd.DataFrame
    :return: scores Dict
    """

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
        ):
    
    cm = confusion_matrix(y_true,
                          y_predicted
                          )
    
    disp = ConfusionMatrixDisplay(cm)
    return disp.plot().figure_
    

def auc_roc(
        y_true: pd.DataFrame,
        y_predicted: pd.DataFrame
        ):

    fpr, tpr, _ = roc_curve(
        y_true,
        y_predicted)

    roc_auc = auc(fpr, tpr)
    disp = RocCurveDisplay(
        fpr=fpr,
        tpr=tpr,
        roc_auc=roc_auc)

    return disp.plot().figure_
