"""
This is a boilerplate pipeline 'data_processing'
generated using Kedro 0.18.14
"""
import pandas as pd
from pandas import CategoricalDtype
from sklearn.model_selection import train_test_split

from typing import Any, List, Dict


# Split data
# def split_data(df: pd.DataFrame) -> pd.DataFrame:


# Encode Binary columns
def _get_binary(df):
    return [col for col in df.columns.to_list() if len(df[col].unique()) == 2]


def _set_dtypes(df: pd.DataFrame) -> pd.DataFrame:
    """Fix dtype of Purchase column

    :param df: a pd.DataFrame
    :return: pd.DataFrame
    """
    df['Purchase Amount (USD)'] = df['Purchase Amount (USD)'].astype('float64')
    return df


def _encode_binary(df: pd.DataFrame) -> pd.DataFrame:
    """Encode binary columns

    :param df: a pd.DataFrame
    :return: encoded pd.DataFrame
    """
    features = ['Gender', 'Subscription Status',
                'Discount Applied', 'Promo Code Used']

    for feature in features:
        if feature == 'Gender':
            df[feature] = df[feature].replace({'Male': 0, 'Female': 1})
        else:
            df[feature] = df[feature].replace({'Yes': 1, 'No': 0})
    
    return df


def get_intermediate(df: pd.DataFrame) -> pd.DataFrame:
    """Perform non-transformtative encoding
    
    Encode raw dataset to generate the intermediate dataset
    :param df: a pd.DataFrame
    :return: encoded pd.DataFrame
    """
    _df = df.copy()
    _df = _set_dtypes(_df)
    _df = _encode_binary(_df)
    
    return _df


# Encode Item Purchase
# Auxiliary functions
def _categorize_column(df: pd.DataFrame,
                       feature_name: str,
                       end: int,
                       start: int = 0
                       ) -> pd.DataFrame:
    """Help identify values out of admitted classes

    Create Null values for unseen classes
    """
    categorizer = CategoricalDtype(categories=list(range(start, end)))
    df[feature_name] = df[feature_name].astype(categorizer)
    
    return df


def _fix_redudant_frequency(df: pd.DataFrame) -> pd.DataFrame:
    """Clean redundancy in frequency of purchases classes
    """
    clean_replace = {'Fortnightly': 'Bi-Weekly',
                     'Every 3 Months': 'Quarterly'}
    
    df['Frequency of Purchases'] = df['Frequency of Purchases'].replace(clean_replace)
    
    return df


# Encoding functions
def _encode_item_purchased(df: pd.DataFrame) -> pd.DataFrame:
    """Encode item purchase

    Encodes the iteam purchase using an alternative classification to
    the Category column
    :param df: a pd.DataFrame
    :return: encoded pd.DataFrame
    """

    item_a = ['Blouse', 'Shirt', 'T-shirt'] # tops: 0
    item_b = ['Sweater', 'Coat', 'Jacket' \
              'Hoodie', 'Scarf', 'Hat', 'Gloves'] # outwear: 1
    item_c = ['Jeans', 'Shorts', 'Pants'] # bottoms: 2
    item_d = ['Shoes', 'Sandals', 'Sneakers', 'Boots'] # footwear: 3
    item_e = ['Handbag', 'Backpack'] # bags: 4 
    item_f = ['Dress', 'Skirt'] # dresses: 5
    item_g = ['Sunglasses', 'Jewelry', 'Belt', 'Socks'] # others: 6
    
    items = [item_a, item_b, item_c, item_d, item_e, item_f, item_g]
    for code, item_i in enumerate(items):
        df.loc[df['Item Purchased'].isin(item_i), 'Item Purchased'] = code

    
    return _categorize_column(df, 'Item Purchased', 7)


def _encode_category(df: pd.DataFrame) -> pd.DataFrame:
    """Encode item category column

    :param df: a pd.DataFrame
    :return: encoded pd.DataFrame
    """
    category_replace = {'Clothing': 0, 'Footwear': 1, 'Outerwear': 2, 'Accessories': 3}
    df['Category'] = df['Category'].replace(category_replace)
    
    return _categorize_column(df, 'Category', 4)


def _encode_size(df: pd.DataFrame) -> pd.DataFrame:
    """Encode size column

    :param df: a pd.DataFrame
    :return: encoded pd.DataFrame
    """
    size_replace = {'S': 0, 'M': 1, 'L': 2, 'XL': 3}
    df['Size'] = df['Size'].replace(size_replace)
    
    return _categorize_column(df, 'Size', 4)


def _encode_color(df: pd.DataFrame) -> pd.DataFrame:
    """Encode color column by hue categories

    :param df: a pd.DataFrame
    :return: encoded pd.DataFrame
    """
    color_a = ['Gray', 'White', 'Beige',\
               'Charcoal', 'Silver', 'Black', 'Brown'] # whites, grays, and black
    color_b = ['Red', 'Maroon', 'Orange',\
               'Gold', 'Yellow', 'Peach'] # reds, yellows, and oranges
    color_c = ['Blue', 'Turquoise', 'Teal',\
               'Indigo', 'Cyan', 'Green', 'Olive'] # blues and greens
    color_d = ['Violet', 'Lavender', 'Pink',\
               'Purple', 'Magenta'] # pinks and purples
    
    colors = [color_a, color_b, color_c, color_d]
    for code, color_i in enumerate(colors):
        df.loc[df['Color'].isin(color_i), 'Color'] = code

    return _categorize_column(df, 'Color', 4)


def _encode_season(df: pd.DataFrame) -> pd.DataFrame:
    """Encode Season column

    :param df: a pd.DataFrame
    :return: encoded pd.DataFrame
    """
    season_replace = {'Winter': 0, 'Spring': 1, 'Summer': 2, 'Fall': 3}
    df['Season'] = df['Season'].replace(season_replace)

    return _categorize_column(df, 'Season', 4)


def _encode_shipping(df: pd.DataFrame) -> pd.DataFrame:
    """Encode Shipping Type column

    :param df: a pd.DataFrame
    :return: encoded pd.DataFrame
    """
    ship_replace = {'Express': 0, 'Free Shipping': 1,
                    'Next Day Air': 2, 'Standard': 3, 
                    '2-Day Shipping': 4, 'Store Pickup': 5}
    
    df['Shipping Type'] = df['Shipping Type'].replace(ship_replace)

    return _categorize_column(df, 'Shipping Type', 6)


def _encode_payment(df: pd.DataFrame) -> pd.DataFrame:
    """Encode Payment Method column

    :param df: a pd.DataFrame
    :return: encoded pd.DataFrame
    """
    pay_replace = {'Venmo': 0, 'Cash': 1, 'Credit Card': 2, 
                   'PayPal': 3, 'Bank Transfer': 4, 'Debit Card': 5}
    
    df['Payment Method'] = df['Payment Method'].replace(pay_replace)
    
    return _categorize_column(df, 'Payment Method', 6)


def _encode_frequency(df: pd.DataFrame) -> pd.DataFrame:
    """Encode Frequency of Purchases column

    :param df: a pd.DataFrame
    :return: encoded pd.DataFrame
    """ 
    df = _fix_redudant_frequency(df) 

    # Encode
    frequency_replace = {
        'Bi-Weekly': 0, 'Weekly': 1, 'Annually': 2, 
        'Quarterly': 3, 'Monthly': 4}

    df['Frequency of Purchases'] = df['Frequency of Purchases'].replace(frequency_replace)
    
    return _categorize_column(df, 'Frequency of Purchases', 5)


def _encode_location(df: pd.DataFrame) -> pd.DataFrame:
    """Encode Location column by USA's States regions

    Regions were taken from Wikipedia
    https://en.wikipedia.org/wiki/List_of_regions_of_the_United_States
    :param df: a pd.DataFrame
    :return: an ecoded pd.DataFrame
    """
    # Northeast
    region_1 = ['Connecticut', 'Maine', 'Massachusetts', 
                'New Hampshire', 'Rhode Island', 'Vermont', 
                'New Jersey', 'New York', 'Pennsylvania']
    # Midwest
    region_2 = ['Illinois', 'Indiana', 'Michigan', 
                'Ohio', 'Wisconsin', 'Iowa', 'Kansas', 
                'Minnesota', 'Missouri', 'Nebraska', 
                'North Dakota', 'South Dakota']
    # South
    region_3 = ['Delaware', 'Florida', 'Georgia',
                'Maryland', 'North Carolina', 'South Carolina',
                'Virginia', 'Washington', 'D.C.', 'West Virginia',
                'Alabama', 'Kentucky', 'Mississippi', 'Tennessee', 
                'Arkansas', 'Louisiana', 'Oklahoma', 'Texas']
    # West
    region_4 = ['Arizona', 'Colorado', 'Idaho', 'Montana', 'Nevada', 
                'New Mexico', 'Utah', 'Wyoming', 'Alaska', 
                'California', 'Hawaii', 'Oregon', 'Washington']

    regions = [region_1, region_2, region_3, region_4]
    for code, region in enumerate(regions):
        df.loc[df['Location'].isin(region), 'Location'] = code

    return _categorize_column(df, 'Location', 5)


def get_primary(df: pd.DataFrame) -> pd.DataFrame:
    """Encode all non-binary columns

    :param df: a pd.DataFrame to encode
    :return: encoded pd.DataFrame
    """
    _df = df.copy()
    _df = _encode_item_purchased(_df)
    _df = _encode_category(_df)
    _df = _encode_size(_df)
    _df = _encode_color(_df)
    _df = _encode_season(_df)
    _df = _encode_shipping(_df)
    _df = _encode_payment(_df)
    _df = _encode_frequency(_df)
    _df = _encode_location(_df)

    return _df