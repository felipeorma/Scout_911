import streamlit as st
import pandas as pd
import requests
from io import BytesIO

# Configurar la página en formato "wide"
st.set_page_config(page_title="911_Scout", page_icon="⚽", layout="wide")

# Título principal y subtítulo
st.header("Carga de datos")
st.subheader("Desarrollado por: Carlos Eduardo Canal Ortiz")

# URL base de los archivos en GitHub
GITHUB_RAW_BASE = "https://raw.githubusercontent.com/CarlosCO94/Scout_911/main/data/"

# Nombres de los archivos que deseas cargar
league_files = [
    "Argentina Copa de la Liga 2024.parquet",
    "Argentina Primera Nacional 2024.parquet",
    "Bolivian LFPB 2024.parquet",
    "Brasileirão 2024.parquet",
    "Brazil Serie B 2024.parquet",
    "Brazil Serie C 2024.parquet",
    "Chilean Primera B 2024.parquet",
    "Chilean Primera División 2024.parquet",
    "Colombian Primera A 2024.parquet",
    "Colombian Torneo BetPlay 2024.parquet",
    "Ecuador Liga Pro 2024.parquet",
    "MLS 2024.parquet",
    "Panama LPF 2024.parquet",
    "Paraguay Division Profesional 2024.parquet",
    "Peruvian Liga 1 2024.parquet",
    "Uruguay Primera División 2024.parquet"
]

# Función para cargar los datos desde GitHub
@st.cache_data
def load_data():
    combined_df = pd.DataFrame()
    
    for file_name in league_files:
        file_url = f"{GITHUB_RAW_BASE}{file_name.replace(' ', '%20')}"
        try:
            response = requests.get(file_url, verify=False)
            response.raise_for_status()
            df = pd.read_parquet(BytesIO(response.content))
            combined_df = pd.concat([combined_df, df], ignore_index=True)
        except Exception as e:
            st.error(f"Error al leer el archivo {file_name}: {str(e)}")
    
    return combined_df

# Botón para cargar datos manualmente
if st.button("Cargar Datos") or 'data' in st.session_state:
    if 'data' not in st.session_state:
        st.session_state['data'] = load_data()
        st.success("Archivos cargados correctamente.")

    # Mostrar el contenido de la data si existe
    st.write("Archivos cargados:")
    # Seleccionar solo las columnas que quieres mostrar
    columnas_a_mostrar = ['Full name', 'Team within selected timeframe', 'Age', 'Position', 'Passport country']
    
    # Verificar que las columnas existan en el DataFrame
    if all(col in st.session_state['data'].columns for col in columnas_a_mostrar):
        st.dataframe(st.session_state['data'][columnas_a_mostrar].head(10))  # Muestra solo los primeros 10 registros
    else:
        st.warning("No se encontraron todas las columnas necesarias en los datos.")
else:
    st.info("Haz clic en el botón 'Cargar Datos' para cargar los archivos.")

