import streamlit as st
import pandas as pd

import plotly.express as px

from dashboard.utils import (read_datafile, get_filepath, get_features)

st.title('Shopping Patterns USA Dataset')

raw_df = read_datafile(get_filepath('shopping_raw'))
st.write(raw_df.head())

params_inter = get_features('intermediate_data_layer_pipeline')
categ_inter = params_inter['categorical']
numeric_inter = params_inter['numerical']

st.write(raw_df[categ_inter])
