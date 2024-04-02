"""
This is a boilerplate pipeline 'model_training'
generated using Kedro 0.18.14
"""
import logging

from typing import Dict

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
from sklearn.model_selection import (GridSearchCV, KFold, StratifiedKFold)
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


def model_evaluate(
        model: sklearn.base.BaseEstimator,
        X_test: pd.DataFrame,
        y_test: pd.DataFrame,
        ) -> Dict:
    """Evaluate classifier

    :param model: trained classifier
    :param X_test: test pd.DataFrame
    :param y_test: test labels pd.DataFrame
    :return: scores Dict
    """
    y_predict = model.predict(X_test)
    fscore = f1_score(y_test.to_numpy(), y_predict)
    acc = accuracy_score(y_test.to_numpy(), y_predict)
    recall = recall_score(y_test.to_numpy(), y_predict)

    logger.info('F-score: {:.3f}'.format(fscore))
    logger.info('Accuracy: {:.3f}'.format(acc))
    logger.info('Recall: {:.3f}'.format(recall))
    
    return pd.DataFrame(
        {'F1-score': fscore, 'Accuracy': acc, 'Recall': recall}, index=[0]
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


def train_feature_select(
        model_name: str,
        X_train: pd.DataFrame,
        X_val: pd.DataFrame,
        y_train: pd.DataFrame,
        ):
    """Train model using selected features

    :param model_name: classifier name code
    :param X_train: train pd.DataFrame
    :param y_train: train labels pd.DataFrame
    :return: trained classifier
    """
    features = _top_feats_mutual(X_train, y_train)
    
    trained_model = model_train(
        model_name,
        X_train[features],
        y_train)
    
    logger.info('{} top features: {}'.format(model_name, features))
    return trained_model, X_val[features]
