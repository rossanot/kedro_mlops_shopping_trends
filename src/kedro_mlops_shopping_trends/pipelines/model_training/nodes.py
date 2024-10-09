"""
This is a boilerplate pipeline 'model_training'
generated using Kedro 0.18.14
"""
import logging

from typing import Dict, List

import numpy as np
import pandas as pd

import sklearn
from sklearn import svm
from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from xgboost import XGBClassifier
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
    'Naive Bayes': GaussianNB,
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
        *args
        ) -> pd.DataFrame:
    """ Make predictions

    :param model: trained classifier
    :param X_test: test pd.DataFrame
    """
    dfs = []
    for df in args:
        dfs.append(pd.DataFrame(model.predict(df)))
    
    return dfs


def top_feats_mutual(
        X_train: pd.DataFrame,
        y_train: pd.DataFrame,
        max_number: int = 14,
        ) -> Dict:
    """Select top features using mutual information method
    """
    feature_imp = mutual_info_classif(
        X_train,
        y_train.to_numpy().reshape(-1)
        )

    columns_all = X_train.columns.to_numpy()

    importance_df = pd.DataFrame(
        {'Feature': columns_all, 'Importance': feature_imp}
        ).sort_values(by='Importance', ascending=False)

    logger.info('Feature importance: {}'.format(importance_df))

    columns_red = columns_all[np.argsort(feature_imp)[-max_number:]]
    return {'features': columns_red.tolist()}


def get_reduced_x(
        features: Dict,
        *args
        ) -> List:
    """Reduce datasets using top features

    :param X_train: train pd.DataFrame
    :param X_test: test pd.DataFrame
    :return: reduced datasets
    """
    
    dfs_red = []
    for df in args:
        dfs_red.append(df[features['features']])

    return dfs_red


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

    estimator = best_classifier.fit(X_train, y_train)
    estimator_params = estimator.best_params_
    logger.info('Best parameters: {}'.format(estimator_params))

    logger.info('Model training features{}'.format(X_train.columns.to_list()))

    return model(**estimator_params).fit(X_train, y_train)
