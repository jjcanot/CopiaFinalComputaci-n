import pandas as pd
import streamlit as st
from PIL import Image
import numpy as np
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Análisis de Sensores - Mi Ciudad",
    page_icon="",
    layout="wide"
)

# Define colores y fuentes (opcional)
primary_color = "#2196F3"  # Example blue
secondary_color = "#F44336"  # Example red
main_font = "Arial"

# Custom CSS with defined colors and fonts (optional)
st.markdown("""
<style>
body {
    font-family: %(main_font)s;
}
.st-subheader, .stButton, .stText {
    color: %(primary_color)s;
}
.stAlert {
    background-color: %(secondary_color)s;
    color: white;
}
.main {
    padding: 2rem;
}
</style>
""", unsafe_allow_html=True, main_font=main_font, primary_color=primary_color, secondary_color=secondary_color)

# Universidad EAFIT location (separate variable)
eafit_location = {
    "lat": 6.2006,
    "lon": -75.5783,
    "name": "Universidad EAFIT"
}

# Title and description
st.title(' Análisis de Datos de Sensores Urbanos')
st.markdown("""
Esta aplicación permite analizar datos de temperatura y humedad
recogidos por sensores en **%(eafit_location[name])s**.
""" % eafit_location)

# Map
st.subheader(f" Ubicación del Sensor - {eafit_location['name']}")
st.map(eafit_location, zoom=15)

# File uploader
uploaded_file = st.file_uploader('Seleccione archivo CSV', type=['csv'])

# Process uploaded data
if uploaded_file is not None:
    try:
        df1 = pd.read_csv(uploaded_file)
        column_mapping = {
            'temperatura {device="ESP32", name="Sensor 1"}': 'temperatura',
            'humedad {device="ESP32", name="Sensor 1"}': 'humedad'
        }
        df1 = df1.rename(columns=column_mapping)
        df1['Time'] = pd.to_datetime(df1['Time'])
        df1 = df1.set_index('Time')

        # Tabs
        tab1, tab2, tab3, tab4 = st.tabs([" Visualización", " Estadísticas", " Filtros", "️ Información del Sitio"])

        # Visualization tab
        with tab1:
            st.subheader('Visualización de Datos')
            variable = st.selectbox(
                "Seleccione variable a visualizar",
                ["temperatura", "humedad", "Ambas variables"]
            )
            chart_type = st
