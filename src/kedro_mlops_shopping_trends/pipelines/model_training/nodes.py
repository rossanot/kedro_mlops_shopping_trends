"""
This is a boilerplate pipeline 'model_training'
generated using Kedro 0.18.14
"""
import logging

from typing import List, Tuple
from typing_extensions import Self

import numpy as np
import pandas as pd

import sklearn
from sklearn import svm
from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from xgboost import XGBClassifier
from sklearn.metrics import (classification_report,
                             accuracy_score,
                             recall_score,
                             f1_score)
from sklearn.model_selection import (GridSearchCV, KFold, StratifiedKFold)
from sklearn.feature_selection import mutual_info_classif

logger = logging.getLogger(__name__)


def model_train(
        model: sklearn.base.BaseEstimator,
        X_train: pd.DataFrame,
        y_train: pd.DataFrame,
        ):
    return model().fit(
        X_train,
        y_train.to_numpy().reshape(-1)
        )


def model_evaluate(
        model: sklearn.base.BaseEstimator,
        X_test: pd.DataFrame,
        y_test: pd.DataFrame,
        ) -> Tuple[float]:
    y_predict = model.predict(X_test)
    fscore = f1_score(y_test.to_numpy(), y_predict)
    acc = accuracy_score(y_test.to_numpy(), y_predict)
    recall = recall_score(y_test.to_numpy(), y_predict)
    report = classification_report(y_test.to_numpy(), y_predict)

    logger.info('F-score: {:.3f}'.format(fscore))
    logger.info('Accuracy: {:.3f}'.format(acc))
    logger.info('Recall: {:.3f}'.format(recall))
    
    return fscore, acc, report


def top_feats_mutual(
        X_train: pd.DataFrame,
        y_train: pd.DataFrame,
        max_number: int = 14,
        ) -> np.array:
    feature_imp = mutual_info_classif(
        X_train,
        y_train.to_numpy().reshape(-1)
        )

    columns_all = X_train.columns.to_numpy()

    return columns_all[np.argsort(feature_imp)[-max_number:]]


def train_baseline(X_train, X_test, y_train, y_test):
    trained_model = model_train(DecisionTreeClassifier, X_train, y_train)
    model_evaluate(trained_model, X_test, y_test)
    return trained_model


def train_feature_select(X_train, X_test, y_train, y_test):
    features = top_feats_mutual(X_train, y_train)
    
    trained_model = model_train(
        DecisionTreeClassifier, X_train[features], y_train)
    model_evaluate(trained_model, X_test[features], y_test)

    logger.info('Top features: {}'.format(features))
    return trained_model

