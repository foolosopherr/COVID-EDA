import pandas as pd
import streamlit as st
import numpy as np
import plotly.express as px
from streamlit_plots import *

st.write("""
# Exploratory Data Analysis
""")

df = pd.read_csv('cleaned df.csv', index_col=0)

options_plot = st.selectbox(label='Plot:', options=['Distribution', 'Scatter', 'Heatmap', 'Map', 'Sunburst'])


if options_plot == 'Distribution':
    plot_streamlit_distribution(df)
elif options_plot == 'Scatter':
    plot_streamlit_scatter(df)
elif options_plot == 'Heatmap':
    plot_streamlit_heatmap(df)
elif options_plot == 'Map':
    plot_streamlit_map(df)
elif options_plot == 'Sunburst':
    plot_streamlit_sunburst(df)
else:
    st.write("""
    # Coming soon
    """)
    st.write(df['Continent'].unique())



