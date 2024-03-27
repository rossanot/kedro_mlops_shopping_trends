"""
This is a boilerplate pipeline 'data_processing'
generated using Kedro 0.18.14
"""
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OrdinalEncoder
from sklearn.preprocessing import LabelEncoder
from typing import Tuple, Dict
import logging

logger = logging.getLogger(__name__)


# Encode Binary columns
def _set_dtypes(df: pd.DataFrame) -> pd.DataFrame:
    """Fix dtype of Purchase column

    :param df: a pd.DataFrame
    :return: pd.DataFrame
    """

    df['Purchase Amount (USD)'] = df['Purchase Amount (USD)'].astype('float64')
    return df


def _fix_redudant_frequency(df: pd.DataFrame) -> pd.DataFrame:
    """Clean redundancy in frequency of purchases classes
    
    Note: Own interpretation of Quarterly meaning might be wrong
    """
    clean_replace = {'Every 3 Months': 'Quarterly'}

    df['Frequency of Purchases'] = df['Frequency of Purchases'].replace(
        clean_replace)

    return df


# Encode countries
def _encode_location(df: pd.DataFrame) -> pd.DataFrame:
    """Encode Location column by USA's States regions

    Regions were taken from Wikipedia
    https://en.wikipedia.org/wiki/List_of_regions_of_the_United_States
    :param df: a pd.DataFrame
    :return: an ecoded pd.DataFrame
    """
    # Northeast
    region_0 = ['Connecticut', 'Maine', 'Massachusetts',
                'New Hampshire', 'Rhode Island', 'Vermont',
                'New Jersey', 'New York', 'Pennsylvania']
    # Midwest
    region_1 = ['Illinois', 'Indiana', 'Michigan',
                'Ohio', 'Wisconsin', 'Iowa', 'Kansas',
                'Minnesota', 'Missouri', 'Nebraska',
                'North Dakota', 'South Dakota']
    # South
    region_2 = ['Delaware', 'Florida', 'Georgia',
                'Maryland', 'North Carolina', 'South Carolina',
                'Virginia', 'Washington', 'D.C.', 'West Virginia',
                'Alabama', 'Kentucky', 'Mississippi', 'Tennessee',
                'Arkansas', 'Louisiana', 'Oklahoma', 'Texas']
    # West
    region_3 = ['Arizona', 'Colorado', 'Idaho', 'Montana', 'Nevada',
                'New Mexico', 'Utah', 'Wyoming', 'Alaska',
                'California', 'Hawaii', 'Oregon', 'Washington']

    df['Location_Regions'] = df['Location']
    regions = [region_0, region_1, region_2, region_3]
    for code, region in enumerate(regions):
        df.loc[df['Location_Regions'].isin(region),
               'Location_Regions'] = 'region_' + str(code)
    return df


# Encode colors
def _encode_color(df: pd.DataFrame) -> pd.DataFrame:
    """Encode color column by hue categories

    :param df: a pd.DataFrame
    :return: encoded pd.DataFrame
    """
    # whites, grays, and black
    color_0 = ['Gray', 'White', 'Beige',
               'Charcoal', 'Silver', 'Black', 'Brown']
    # reds, yellows, and oranges
    color_1 = ['Red', 'Maroon', 'Orange',
               'Gold', 'Yellow', 'Peach']
    # blues and greens
    color_2 = ['Blue', 'Turquoise', 'Teal',
               'Indigo', 'Cyan', 'Green', 'Olive']
    # pinks and purples
    color_3 = ['Violet', 'Lavender', 'Pink',
               'Purple', 'Magenta']

    df['Color_Groups'] = df['Color']
    colors = [color_0, color_1, color_2, color_3]
    for code, color_i in enumerate(colors):
        df.loc[df['Color_Groups'].isin(color_i),
               'Color_Groups'] = 'color_' + str(code)

    return df


# Encode item types
def _encode_item_purchased(df: pd.DataFrame) -> pd.DataFrame:
    """Encode item purchase

    Encodes the iteam purchase using an alternative classification to
    the Category column
    :param df: a pd.DataFrame
    :return: encoded pd.DataFrame
    """

    item_0 = ['Blouse', 'Shirt', 'T-shirt']  # tops: 0
    item_1 = ['Sweater', 'Coat', 'Jacket',
              'Hoodie', 'Scarf', 'Hat', 'Gloves']  # outwear: 1
    item_2 = ['Jeans', 'Shorts', 'Pants']  # bottoms: 2
    item_3 = ['Shoes', 'Sandals', 'Sneakers', 'Boots']  # footwear: 3
    item_4 = ['Handbag', 'Backpack']  # bags: 4 
    item_5 = ['Dress', 'Skirt']  # dresses: 5
    item_6 = ['Sunglasses', 'Jewelry', 'Belt', 'Socks']  # others: 6

    df['Item_Groups'] = df['Item Purchased']
    items = [item_0, item_1, item_2, item_3, item_4, item_5, item_6]
    for code, item_i in enumerate(items):
        df.loc[df['Item_Groups'].isin(item_i),
               'Item_Groups'] = 'item_' + str(code)

    return df


def _encode_age(df: pd.DataFrame) -> pd.DataFrame:
    """Encode Age

    Note: cut function implementation inspired by
    https://www.kaggle.com/code/mehedithedreamer/trendcast-forecasting-shopper-subscription
    :param df: a pd.DataFrame
    :return: encoded pd.DataFrame
    """

    df['Age_Groups'] = pd.cut(df['Age'],
                              bins=[0, 30, 40, 50, 100],
                              labels=['0-30', '31-40', '41-50', '51+'])

    return df


def _encode_purchase_amount(df: pd.DataFrame) -> pd.DataFrame:
    """Encode Purchase Amount

    :param df: a pd.DataFrame
    :return: encoded pd.DataFrame
    """
    group_a = df.loc[df['Purchase Amount (USD)'] <= 39.].index.to_list()
    group_b = df.loc[(df['Purchase Amount (USD)'] > 39.)
                     & (df['Purchase Amount (USD)'] <= 60.)].index.to_list()
    group_c = df.loc[(df['Purchase Amount (USD)'] > 60.)
                     & (df['Purchase Amount (USD)'] <= 81.)].index.to_list()
    group_d = df.loc[(df['Purchase Amount (USD)'] > 81.)].index.to_list()

    df['Purchase_Groups'] = df['Purchase Amount (USD)']
    groups = [group_a, group_b, group_c, group_d]
    for code, group in enumerate(groups):
        df.loc[group, 'Purchase_Groups'] = code

    return df


def _encode_previous_purchase(df: pd.DataFrame) -> pd.DataFrame:
    """Encode Previous Purchases

    :param df: a pd.DataFrame
    :return: encoded pd.DataFrame
    """
    group_a = df.loc[df['Previous Purchases'] <= 13].index.to_list()
    group_b = df.loc[(df['Previous Purchases'] > 13)
                     & (df['Previous Purchases'] <= 25)].index.to_list()
    group_c = df.loc[(df['Previous Purchases'] > 25)
                     & (df['Previous Purchases'] <= 38)].index.to_list()
    group_d = df.loc[df['Previous Purchases'] > 38].index.to_list()

    df['Previous_Groups'] = df['Previous Purchases']
    groups = [group_a, group_b, group_c, group_d]
    for code, group in enumerate(groups):
        df.loc[group, 'Previous_Groups'] = code

    return df


def _encode_review_rating(df: pd.DataFrame) -> pd.DataFrame:
    """Encode Review Rating

    :param df: a pd.DataFrame
    :return: encoded pd.DataFrame
    """
    rating_bad = df.loc[df['Review Rating'] <= 3.75].index.to_list()
    rating_good = df.loc[(df['Review Rating'] > 3.75)
                         & (df['Review Rating'] <= 5.)].index.to_list()
    
    df['Review_Groups'] = df['Review Rating']
    # Replace
    df.loc[rating_bad, 'Review_Groups'] = 0.
    df.loc[rating_good, 'Review_Groups'] = 1.

    return df


def _encode_subscription(df: pd.DataFrame) -> pd.DataFrame:
    """Encode Subscription Status

    :param df: a pd.DataFrame
    :return: encoded pd.DataFrame
    """
    subs = LabelEncoder().fit_transform(df['Subscription Status'])
    df['Subscription Status'] = subs

    return df


# Get intermediate
# Clean columns
def get_intermediate(df: pd.DataFrame) -> pd.DataFrame:
    """Encode label and clean features

    Encode raw df and generate the intermediate data layer
    :param df: a pd.DataFrame
    :return: encoded pd.DataFrame
    """
    _df = df.copy()
    _df = _set_dtypes(_df)
    _df = _fix_redudant_frequency(_df)
    _df = _encode_subscription(_df)
    return _df


def get_primary(df: pd.DataFrame) -> pd.DataFrame:
    """Encode features

    Encode raw df and generate the primary data layer
    Feature engineering: Location, Color, and Item Purchased
    :param df: a pd.DataFrame
    :return: encoded pd.DataFrame
    """
    _df = df.copy()
    _df = _encode_review_rating(_df)
    _df = _encode_location(_df)
    _df = _encode_color(_df)
    _df = _encode_item_purchased(_df)

    return _df


def get_feature(df: pd.DataFrame) -> pd.DataFrame:
    """Encode numerical features

    Encode raw df and generate the feature data layer
    Feature engineering: Age, Purchase Amount Previous Purchases
    :param df: a pd.DataFrame
    :return: encoded pd.DataFrame
    """
    _df = df.copy()
    _df = _encode_age(_df)
    _df = _encode_purchase_amount(_df)
    _df = _encode_previous_purchase(_df)

    return _df


# Split data
def split_data(df: pd.DataFrame, params: Dict, features: Dict) -> Tuple:
    """Split encoded dataset

    :param df: a pd.DataFrame
    :param params: split data parameters
    :return: test and train pd.DataFrames and pd.Series
    """

    X_train, X_test, y_train, y_test = train_test_split(
        df[features['categorical'] + features['numerical']],
        df[features['target']],
        test_size=params['test_size'],
        random_state=params['random_state']
        )

    X_val, X_test, y_val, y_test = train_test_split(
        X_test,
        y_test,
        test_size=params['validation_size'],
        random_state=params['random_state']
        )

    return X_train, X_val, X_test, y_train, y_val, y_test


# Encode using Ordinal encoder
def get_model_input(
        X_train: pd.DataFrame,
        X_val: pd.DataFrame,
        X_test: pd.DataFrame,
        features: Dict
        ) -> Tuple:
    """Encode X datasets and return primary df

    :param X_train: encoded pd.DataFrame
    :param X_test: encoded pd.DataFrame
    :return: pd.DataFrame
    """
    _X_train, _X_val, _X_test = X_train.copy(), X_val.copy(), X_test.copy()

    for feature in features['categorical']:
        oec = OrdinalEncoder(
            handle_unknown='use_encoded_value',
            unknown_value=np.nan
            )
        _X_train[feature] = oec.fit_transform(
            _X_train[feature].to_numpy().reshape(-1, 1)
            )
        _X_val[feature] = oec.transform(
            _X_val[feature].to_numpy().reshape(-1, 1)
            )
        _X_test[feature] = oec.transform(
            _X_test[feature].to_numpy().reshape(-1, 1)
            )
        _X_val = _X_val.dropna()
        _X_test = _X_test.dropna()

    logger.info('During encoding, were dropped:')
    logger.info('{} rows from X_val and {} rows from X_test'.format(
        X_val.shape[0]-_X_val.shape[0], X_test.shape[0]-_X_test.shape[0]))

    return _X_train, _X_val, _X_test
