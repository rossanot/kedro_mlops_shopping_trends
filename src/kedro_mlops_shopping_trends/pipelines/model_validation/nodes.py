"""
This is a boilerplate pipeline 'model_validation'
generated using Kedro 0.18.14
"""
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

    logger.info('F-score: {:.3f}'.format(fscore))
    logger.info('Accuracy: {:.3f}'.format(acc))
    logger.info('Recall: {:.3f}'.format(recall))

    return pd.DataFrame(
        {'F1-score': fscore,
         'Accuracy': acc,
         'Recall': recall}, index=[0]
        )


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
