import pandas as pd
import streamlit as st
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns

# Configuración de la página
st.set_page_config(page_title="Análisis de Sensores - Mi Ciudad", page_icon="📊", layout="wide")

# CSS personalizado
st.markdown("""
    <style>
    .main { padding: 2rem; }
    .stAlert { margin-top: 1rem; }
    </style>
""", unsafe_allow_html=True)

# Título y descripción
st.title('📊 Análisis de Datos de Sensores en Mi Ciudad')
st.markdown("""
    Esta aplicación permite analizar datos de temperatura y humedad
    recolectados por sensores en diferentes puntos de la ciudad.
""")

# Cargar archivo CSV
uploaded_file = st.file_uploader('Seleccione archivo CSV', type=['csv'])

def cargar_datos(uploaded_file):
    """Función para cargar y procesar los datos del archivo CSV."""
    df = pd.read_csv(uploaded_file)
    
    # Renombrar columnas para simplificar
    column_mapping = {
        'temperatura {device="ESP32", name="Sensor 1"}': 'temperatura',
        'humedad {device="ESP32", name="Sensor 1"}': 'humedad'
    }
    df = df.rename(columns=column_mapping)
    
    # Convertir la columna 'Time' a formato datetime y establecerla como índice
    df['Time'] = pd.to_datetime(df['Time'])
    df = df.set_index('Time')
    
    return df

if uploaded_file is not None:
    try:
        df1 = cargar_datos(uploaded_file)
        
        # Crear pestañas para diferentes análisis
        tab1, tab2, tab3, tab4, tab5 = st.tabs(["📈 Visualización", "📊 Estadísticas", "🔍 Filtros", "🗺️ Información del Sitio", "📉 Análisis de Correlación"])

        with tab1:
            st.subheader('Visualización de Datos')
            
            # Selector de variable
            variable = st.selectbox("Seleccione variable a visualizar", ["temperatura", "humedad", "Ambas variables"])
            # Selector de tipo de gráfico
            chart_type = st.selectbox("Seleccione tipo de gráfico", ["Línea", "Área", "Barra"])
            
            # Gráficos
            if variable == "Ambas variables":
                st.write("### Temperatura")
                if chart_type == "Línea":
                    st.line_chart(df1["temperatura"])
                elif chart_type == "Área":
                    st.area_chart(df1["temperatura"])
                else:
                    st.bar_chart(df1["temperatura"])
                    
                st.write("### Humedad")
                if chart_type == "Línea":
                    st.line_chart(df1["humedad"])
                elif chart_type == "Área":
                    st.area_chart(df1["humedad"])
                else:
                    st.bar_chart(df1["humedad"])
            else:
                if chart_type == "Línea":
                    st.line_chart(df1[variable])
                elif chart_type == "Área":
                    st.area_chart(df1[variable])
                else:
                    st.bar_chart(df1[variable])
            
            # Mostrar datos crudos
            if st.checkbox('Mostrar datos crudos'):
                st.write(df1)

        with tab2:
            st.subheader('Análisis Estadístico')
            
            # Selector de variable para estadísticas
            stat_variable = st.radio("Seleccione variable para estadísticas", ["temperatura", "humedad"])
            
            # Resumen estadístico
            stats_df = df1[stat_variable].describe()
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.dataframe(stats_df)
            
            with col2:
                # Estadísticas adicionales
                if stat_variable == "temperatura":
                    st.metric("Temperatura Promedio", f"{stats_df['mean']:.2f}°C")
                    st.metric("Temperatura Máxima", f"{stats_df['max']:.2f}°C")
                    st.metric("Temperatura Mínima", f"{stats_df['min']:.2f}°C")
                else:
                    st.metric("Humedad Promedio", f"{stats_df['mean']:.2f}%")
                    st.metric("Humedad Máxima", f"{stats_df['max']:.2f}%")
                    st.metric("Humedad Mínima", f"{stats_df['min']:.2f}%")

        with tab3:
            st.subheader('Filtros de Datos')
            
            filter_variable = st.selectbox("Seleccione variable para filtrar", ["temperatura", "humedad"])
            col1, col2 = st.columns(2)
            
            with col1:
                # Filtro de valor mínimo
                min_val = st.slider(f'Valor mínimo de {filter_variable}', 
                                    float(df1[filter_variable].min()), float(df1[filter_variable].max()), 
                                    float(df1[filter_variable].mean()), key="min_val")
                filtrado_df_min = df1[df1[filter_variable] > min_val]
                st.write(f"Registros con {filter_variable} superior a", f"{min_val}{'°C' if filter_variable == 'temperatura' else '%'}:")
                st.dataframe(filtrado_df_min)
                
            with col2:
                # Filtro de valor máximo
                max_val = st.slider(f'Valor máximo de {filter_variable}', 
                                    float(df1[filter_variable].min()), float(df1[filter_variable].max()), 
                                    float(df1[filter_variable].mean()), key="max_val")
                filtrado_df_max = df1[df1[filter_variable] < max_val]
                st.write(f"Registros con {filter_variable} inferior a", f"{max_val}{'°C' if filter_variable == 'temperatura' else '%'}:")
                st.dataframe(filtrado_df_max)

            # Descarga de datos filtrados
            if st.button('Descargar datos filtrados'):
                csv = filtrado_df_min.to_csv().encode('utf-8')
                st.download_button(label="Descargar CSV", data=csv, file_name='datos_filtrados.csv', mime='text/csv')

        with tab4:
            st.subheader("Información del Sitio de Medición")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("### Ubicación del Sensor")
                st.write("**Universidad EAFIT**")
                st.write("- Latitud: 6.2006")
                st.write("- Longitud: -75.5783")
                st.write("- Altitud: ~1,495 metros sobre el nivel del mar")
            
            with col2:
                st.write("### Detalles del Sensor")
                st.write("- Tipo: ESP32")
                st.write("- Variables medidas:")
                st.write("  * Temperatura (°C)")
                st.write("  * Humedad (%)")
                st.write("- Frecuencia de medición: Según configuración")
                st.write("- Ubicación: Campus universitario")
        
        with tab5:
            st.subheader("📉 Análisis de Correlación")
            
            # Análisis de correlación entre temperatura y humedad
            st.write("### Correlación entre Temperatura y Humedad")
            corr = df1[['temperatura', 'humedad']].corr()
            st.write(f"Coeficiente de Correlación: {corr.iloc[0, 1]:.2f}")
            
            # Gráfico de dispersión
            fig, ax = plt.subplots()
            ax.scatter(df1['temperatura'], df1['humedad'], c='blue', alpha=0.5)
            ax.set_xlabel('Temperatura (°C)')
            ax.set_ylabel('Humedad (%)')
            ax.set_title('Gráfico de dispersión: Temperatura vs Humedad')
            st.pyplot(fig)
            
            # Histogramas
            st.write("### Histogramas de Temperatura y Humedad")
            col1, col2 = st.columns(2)
            
            with col1:
                fig, ax = plt.subplots()
                ax.hist(df1['temperatura'], bins=30, color='orange', edgecolor='black')
                ax.set_title('Distribución de Temperatura')
                ax.set_xlabel('Temperatura (°C)')
                ax.set_ylabel('Frecuencia')
                st.pyplot(fig)
            
            with col2:
                fig, ax = plt.subplots()
                ax.hist(df1['humedad'], bins=30, color='green', edgecolor='black')
                ax.set_title('Distribución de Humedad')
                ax.set_xlabel('Humedad (%)')
                ax.set_ylabel('Frecuencia')
                st.pyplot(fig)

