import streamlit as st
import pandas as pd

import plotly.express as px

from dashboard.utils import (read_file, get_filepath)

st.title('Shopping Patterns USA Dataset')

raw_df = read_file(get_filepath('shopping_raw'))
st.write(raw_df.head())


