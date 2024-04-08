"""
This is a boilerplate pipeline 'model_training'
generated using Kedro 0.18.14
"""
import logging

from typing import Dict, Tuple

import numpy as np
import pandas as pd

import sklearn
from sklearn import svm
from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from xgboost import XGBClassifier
from sklearn.metrics import (f1_score,
                             accuracy_score,
                             recall_score
                             )
from sklearn.model_selection import (GridSearchCV,
                                     KFold,
                                     StratifiedKFold)
from sklearn.feature_selection import mutual_info_classif

logger = logging.getLogger(__name__)


models = {
    'Decision Tree': DecisionTreeClassifier,
    'XGBoost': XGBClassifier,
    'Logistic Regression': LogisticRegression,
    'KNN': KNeighborsClassifier,
    'Naïve Bayes': GaussianNB,
    'SVM': svm
    }


def model_train(
        model_name: str,
        X_train: pd.DataFrame,
        y_train: pd.DataFrame,
        ):
    """Train classifier

    :param model_name: classifier name code
    :param X_train: train pd.DataFrame
    :param y_train: train labels pd.DataFrame
    :return: trained classifier
    """
    model = models[model_name]

    return model().fit(
        X_train,
        y_train.to_numpy().reshape(-1)
        )


def model_predict(
        model: sklearn.base.BaseEstimator,
        X_test: pd.DataFrame
        ) -> pd.DataFrame:
    """ Make predictions

    :param model: trained classifier
    :param X_test: test pd.DataFrame
    """
    return pd.DataFrame(model.predict(X_test))


def model_evaluate(
        y_predicted: pd.DataFrame,
        y_test: pd.DataFrame,
        ) -> Dict:
    """Evaluate classifier

    :param y_predicted: predicted labels pd.DataFrame
    :param y_test: true labels pd.DataFrame
    :return: scores Dict
    """
    
    fscore = f1_score(y_test.to_numpy(), y_predicted)
    acc = accuracy_score(y_test.to_numpy(), y_predicted)
    recall = recall_score(y_test.to_numpy(), y_predicted)

    logger.info('F-score: {:.3f}'.format(fscore))
    logger.info('Accuracy: {:.3f}'.format(acc))
    logger.info('Recall: {:.3f}'.format(recall))
    
    return pd.DataFrame(
        {'F1-score': fscore,
         'Accuracy': acc,
         'Recall': recall}, index=[0]
        )


def _top_feats_mutual(
        X_train: pd.DataFrame,
        y_train: pd.DataFrame,
        max_number: int = 14,
        ) -> np.array:
    """Select top features using mutual information method
    """
    feature_imp = mutual_info_classif(
        X_train,
        y_train.to_numpy().reshape(-1)
        )

    columns_all = X_train.columns.to_numpy()

    return columns_all[np.argsort(feature_imp)[-max_number:]]


def get_reduced_x(
        X_train: pd.DataFrame,
        X_test: pd.DataFrame,
        y_train: pd.DataFrame
        ) -> Tuple:
    """Reduce datasets using top features

    :param X_train: train pd.DataFrame
    :param X_test: test pd.DataFrame
    :return: reduced datasets
    """
    columns = _top_feats_mutual(X_train, y_train)

    return X_train[columns], X_test[columns], {'features': columns.tolist()}


def grid_search(
        model_name: str,
        X_train: pd.DataFrame,
        y_train: pd.DataFrame,
        params: Dict,
        kfold: bool = True,
        ):
    """Grid search

    Uses f1 scoring
    :param model_name: classifier name code
    :param X_train: train pd.DataFrame
    :param y_train: train labels pd.DataFrame
    :param params: classifier parameters Dict
    :param kfold: KFold or StratifiedKFold, defaults to True
    :return: trained classifier
    """
    
    model = models[model_name]

    if kfold:
        cv_method = KFold(n_splits=5, shuffle=True)
    else:
        cv_method = StratifiedKFold(n_splits=5, shuffle=True)

    best_classifier = GridSearchCV(
        estimator=model(),
        param_grid=params,
        cv=cv_method,
        verbose=True,
        n_jobs=1,
        scoring='f1'
        )

    if isinstance(y_train, np.ndarray):
        y_train = y_train.reshape(-1)

    else:
        y_train = y_train.to_numpy().reshape(-1)
   
    return best_classifier.fit(X_train, y_train)
