import streamlit as st
import pandas as pd

import plotly.express as px

from dashboard.utils import (read_datafile, get_filepath, get_features)

st.title('Shopping Patterns USA Dataset')

st.sidebar.title('Data Visualization')

# Pick dataset
# Pick features
dfs = {
    'Raw Dataset': [
        'shopping_raw',
        'intermediate_data_layer_pipeline'
        ],
    'Intermediate Dataset': [
        'shopping_02_intermediate',
        'intermediate_data_layer_pipeline'
        ],
    'Primary Dataset': [
        'shopping_03_primary',
        'primary_data_layer_pipeline'
        ],
    'Feature Dataset': [
        'shopping_04_feature',
        'feature_data_layer_pipeline'
        ]
    }

selected_df = st.sidebar.selectbox(
    'Dataset',
    dfs.keys(),
    placeholder='Select a dataset to visualize'
)

# Load df
df = read_datafile(get_filepath(dfs[selected_df][0]))

# Load  parameters
params = get_features(dfs[selected_df][1])
categ_params = params['categorical']
numeric_params = params['numerical']
label = params['target'][0]

# Print df info
df_rows, df_columns = df.shape
st.write('Total Number of Examples: {}, Total Number of Features: {}'.format(
    df_rows, df_columns)
    )

st.write(df.head(2))

with st.sidebar:
    bar_feature1 = st.selectbox(
        'Bar Chart',
        categ_params,
        placeholder='Select a feature to plot'
    )

    bar_feature2 = st.selectbox(
        'Box Plot Feature 1',
        categ_params + [label],
        placeholder='Select a feature to plot'
    )

    bar_feature3 = st.selectbox(
        'Box Plot Feature 2',
        numeric_params,
        placeholder='Select a feature to plot'
    )


data_container1 = st.container(border=True)
with data_container1:
    plot1, plot2 = st.columns(2)
    with plot1:
        corr_title = 'Feature Correlation'
        corr_matrix = df[numeric_params].corr()
        corr_fig = px.imshow(corr_matrix, title=corr_title)
        corr_fig.update_coloraxes(colorbar_orientation='h')
        corr_fig.update_layout(coloraxis_colorbar_y=0.8)
        st.plotly_chart(corr_fig, use_container_width=True)
    with plot2:
        pie_title = '{} Distribtuion'.format(label)
        pie_fig = px.pie(df, names=label, title=pie_title)
        st.plotly_chart(pie_fig, use_container_width=True)


data_container2 = st.container(border=True)
with data_container2:
    plot1, plot2 = st.columns(2)
    with plot1:
        bar_title = '{}'.format(bar_feature1)
        bar_fig = px.bar(df, x=bar_feature1, title=bar_title)
        st.plotly_chart(bar_fig, use_container_width=True)
    with plot2:
        box_title = '{} vs {}'.format(bar_feature2, bar_feature3)
        box_fig = px.box(df, x=bar_feature2, y=bar_feature3, title=box_title)
        st.plotly_chart(box_fig, use_container_width=True)
