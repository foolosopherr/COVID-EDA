from copy import deepcopy
from unicodedata import numeric
from matplotlib import projections
import pandas as pd
import streamlit as st
import numpy as np
import plotly.express as px

def plot_streamlit_distribution(df):
    col1, col2, col3, col4, col5 = st.columns(5)

    _options_x = df.dtypes[df.dtypes != 'object'].index.to_list()
    continents = df['Continent'].unique()
    _options_bins = np.arange(5, 51, 5)
    _options_barmode = ['group', 'overlay', 'stack']
    _options_barnorm = [None, 'fraction', 'percent']

    with col1:
        options_x = st.selectbox(label="Feature:", options=_options_x)

    with col2:
        options_bins = st.selectbox(label="Number of bins:", options=_options_bins)

    with col3:
        options_barmode = st.selectbox(label="Barmode:", options=_options_barmode)

    with col4:
        options_barnorm = st.selectbox(label="Barnorm:", options=_options_barnorm)

    with col5:
        options_scale_ = st.selectbox(label='Scale:', options=['Normal', 'Logarithmic'])
        scale_ = True if options_scale_ == 'Logarithmic' else None

    barnorm = options_barnorm if options_barnorm != 'default' else None
    opacity = 0.5 if options_barmode == 'overlay' else 1

    fig1 = px.histogram(df, x=options_x, color='Continent', log_y=scale_,
                        nbins=int(options_bins), barmode=options_barmode,
                        title=options_x, barnorm=barnorm, opacity=opacity, height=500, width=800)

    st.plotly_chart(fig1)
    
    _col1, _col2 = st.columns(2)
    with _col1:
        options_continent = st.selectbox(label='Continent:', options=continents)

    with _col2:
        options_scale = st.selectbox(label='Scale:', options=['Normal', 'Logarithmic'])
        scale = True if options_scale == 'Logarithmic' else None

    slider = st.slider('Plot height:', 500, 800, 500)

    fig2 = px.histogram(df[df['Continent']==options_continent], log_y=scale,
                        x='Country', y=options_x, title=f'{options_x} for {options_continent}',
                        height=slider, width=800)
    st.plotly_chart(fig2)

def plot_streamlit_scatter(df):
    col1, col2, col3, col4 = st.columns(4)
    _options = df.dtypes[df.dtypes != 'object'].index.to_list()

    with col1:
        x_axis = st.selectbox(label='X axis feature:', options=_options)
    with col2:
        y_axis = st.selectbox(label='Y axis feature:', options=_options)
    with col3:
        scale_x = st.radio(label='X axis scale', options=['Normal', 'Logarithmic'])
    with col4:
        scale_y = st.radio(label='Y axis scale', options=['Normal', 'Logarithmic'])

    scale_x = scale_x == 'Logarithmic'
    scale_y = scale_y == 'Logarithmic'
    
    fig = px.scatter(df, x=x_axis, y=y_axis, color='Continent', title=f'Scatter plot between \
                     {x_axis} & {y_axis}', hover_name='Country', log_x=scale_x, log_y=scale_y)
    
    st.plotly_chart(fig)


def plot_streamlit_heatmap(df):
    continents = ['North America', 'South America', 'Asia', 'Europe', 'Oceania', 'Africa']
    named_colorscales = px.colors.named_colorscales()
    options = st.multiselect(label='Continents:', options=continents, default=continents)
    colorscale = st.sidebar.selectbox(label='Color scale:', options=named_colorscales)
    numeric_features = df.dtypes[df.dtypes != 'object'].index

    fig = px.imshow(df[df['Continent'].isin(options)][numeric_features].corr(), 
                    color_continuous_midpoint=0,
                    color_continuous_scale=colorscale, height=800, width=800,
                    title=f"Heatmap for {', '.join(options)}")

    st.plotly_chart(fig)
        
def plot_streamlit_map(df):
    col1, col2, col3 = st.columns(3)
    numeric_features = df.dtypes[df.dtypes != 'object'].index
    with col1:
        col_widget = st.selectbox(label='Population', options=numeric_features)
    
    scopes = ['World', 'North America', 'Asia', 'Europe', 'South America', 'Africa']
    with col2:
        scope = st.selectbox(label='Scope:', options=scopes)
    
    scales = ['Normal', 'Logarithmic']
    with col3:
        scale = st.selectbox(label='Scale', options=scales)

    all_projections = ['equirectangular', 'mercator', 'orthographic', 'natural earth', 
                       'kavrayskiy7', 'miller', 'robinson', 'eckert4', 'azimuthal equal area', 
                       'azimuthal equidistant', 'conic equal area', 'conic conformal', 
                       'conic equidistant', 'gnomonic', 'stereographic', 'mollweide', 'hammer', 
                       'transverse mercator', 'winkel tripel', 'aitoff', 'sinusoidal']
    projection = st.sidebar.selectbox(label='Projection:', options=all_projections)

    named_colorscales = px.colors.named_colorscales()
    colorscale = st.sidebar.selectbox(label='Color scale:', options=named_colorscales)
    if scope == 'World':
        title = f'{col_widget} around the world'
    else:
        title = f'{col_widget} in {scope}'

    values = df[col_widget] if scale == 'Normal' else np.log(df[col_widget])
    fig = px.choropleth(df,
                        locations='Alpha3 code', hover_name='Country',
                        color=values, hover_data={'Alpha3 code':False},
                        title=title, color_continuous_scale=colorscale,
                        projection=projection, scope=scope.lower(), height=700, width=1000)

    st.plotly_chart(fig)


def plot_streamlit_sunburst(df):
    numeric_features = df.dtypes[df.dtypes != 'object'].index
    continents = df['Continent'].unique()
    regions = df['Region'].unique()
    continent = st.sidebar.multiselect('Continents:', options=continents, default=continents)
    region = st.sidebar.multiselect('Regions:', options=regions, default=regions)
    feature = st.selectbox('Feature:', options=numeric_features)

    fig = px.sunburst(df[(df['Continent'].isin(continent)) & (df['Region'].isin(region))], 
                      path=['Continent', 'Region', 'Country'],
                      values=feature, 
                      title=f'Sunburst plot (feature: {feature})',
                      height=600, width=600
                    )
    st.plotly_chart(fig)
        
