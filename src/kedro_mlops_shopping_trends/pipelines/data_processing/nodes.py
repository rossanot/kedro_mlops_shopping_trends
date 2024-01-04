"""
This is a boilerplate pipeline 'data_processing'
generated using Kedro 0.18.14
"""
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OrdinalEncoder
from typing import Tuple, Dict
import logging

logger = logging.getLogger(__name__)


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
    
    return X_train, X_test, y_train, y_test


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
    """
    clean_replace = {'Fortnightly': 'Bi-Weekly',
                     'Every 3 Months': 'Quarterly'}
    
    df['Frequency of Purchases'] = df['Frequency of Purchases'].replace(clean_replace)
    
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

    regions = [region_0, region_1, region_2, region_3]
    for code, region in enumerate(regions):
        df.loc[df['Location'].isin(region), 'Location'] = 'region_' + str(code)

    return df


# Encode colors
def _encode_color(df: pd.DataFrame) -> pd.DataFrame:
    """Encode color column by hue categories

    :param df: a pd.DataFrame
    :return: encoded pd.DataFrame
    """
    color_0 = ['Gray', 'White', 'Beige',\
               'Charcoal', 'Silver', 'Black', 'Brown'] # whites, grays, and black
    color_1 = ['Red', 'Maroon', 'Orange',\
               'Gold', 'Yellow', 'Peach'] # reds, yellows, and oranges
    color_2 = ['Blue', 'Turquoise', 'Teal',\
               'Indigo', 'Cyan', 'Green', 'Olive'] # blues and greens
    color_3 = ['Violet', 'Lavender', 'Pink',\
               'Purple', 'Magenta'] # pinks and purples
    
    colors = [color_0, color_1, color_2, color_3]
    for code, color_i in enumerate(colors):
        df.loc[df['Color'].isin(color_i), 'Color'] = 'color_' + str(code)

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
    
    items = [item_0, item_1, item_2, item_3, item_4, item_5, item_6]
    for code, item_i in enumerate(items):
        df.loc[df['Item Purchased'].isin(item_i), 'Item Purchased'] = 'item_' + str(code)
  
    return df


# Get intermediate
# Clean columns
def get_intermediate(df: pd.DataFrame) -> pd.DataFrame:
    """Perform non-transformtative encoding
    
    Encode raw dataset to generate the intermediate dataset
    :param df: a pd.DataFrame
    :return: encoded pd.DataFrame
    """
    _df = df.copy()
    _df = _set_dtypes(_df)
    _df = _fix_redudant_frequency(_df)
    _df = _encode_location(_df)
    _df = _encode_color(_df)
    _df = _encode_item_purchased(_df)
    
    return _df

# Encode using Ordinal encoder
# Get Primary
# Encode as arrays
def get_primary(
        X_train: pd.DataFrame,
        X_test: pd.DataFrame,
        features: Dict
        ) -> Tuple:
    """Encode X datasets and return primary df

    :param X_train: encoded pd.DataFrame
    :param X_test: encoded pd.DataFrame
    :return: pd.DataFrame
    """
    _X_train, _X_test = X_train.copy(), X_test.copy()

    for feature in features['categorical']:
        oec = OrdinalEncoder(
            handle_unknown='use_encoded_value',
            unknown_value=np.nan
            )
        _X_train[feature] = oec.fit_transform(
            _X_train[feature].to_numpy().reshape(-1, 1)
            )
        _X_test[feature] = oec.transform(
            _X_test[feature].to_numpy().reshape(-1, 1)
            )
        _X_test = _X_test.dropna()
    
    logger.info('During encoding {} rows were dropped from X_test'.format(
        X_test.shape[0]-_X_test.shape[0]))
    
    return _X_train, _X_test
