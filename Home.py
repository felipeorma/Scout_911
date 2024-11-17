import streamlit as st
import pandas as pd
import requests
from io import BytesIO

# Configurar la página en formato "wide"
st.set_page_config(page_title="911_Scout", page_icon="⚽", layout="wide")

# Agregar el logo en la parte superior de la barra lateral
st.sidebar.image("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ0NVTRcTGt9QcKvw2jdga0vvJjlW_RoLUUdw&s", use_column_width=True)
st.sidebar.markdown("### DEPARTAMENTO DE SCOUTING")

# URL base de los archivos en GitHub
GITHUB_RAW_BASE = "https://raw.githubusercontent.com/CarlosCO94/Scout_911/main/data/"

# Nombres de los archivos que deseas cargar
league_files = [
    "Argentina Copa de la Liga 2024.parquet",
    "Argentina Primera Nacional 2024.parquet",
    "Bolivian LFPB 2024.parquet",
    "Brasileirao 2024.parquet",
    "Brazil Serie B 2024.parquet",
    "Brazil Serie C 2024.parquet",
    "Canadian Premier League 2024.parquet",
    "Chilean Primera B 2024.parquet",
    "Chilean Primera Division 2023.parquet",
    "Chilean Primera Division 2024.parquet",
    "Colombian Primera A 2024.parquet",
    "Colombian Torneo BetPlay 2024.parquet",
    "Ecuador Liga Pro 2024.parquet",
    "MLS 2024.parquet",
    "MLS Next Pro 2024.parquet",
    "Panama LPF 2024.parquet",
    "Paraguay Division Profesional 2024.parquet",
    "Peruvian Liga 1 2024.parquet",
    "USL Championship 2024.parquet",
    "Uruguay Primera Division 2024.parquet",
]

# Estilo CSS para ajustar el ancho de la tabla y centrar los valores
st.markdown("""
    <style>
    .dataframe {
        width: 100% !important;
    }
    .stDataFrame tbody tr td {
        text-align: center !important;
    }
    </style>
""", unsafe_allow_html=True)

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
    columnas_a_mostrar = ['Team logo', 'Full name', 'Team within selected timeframe', 'Age', 'Position', 'Passport country']
    
    # Verificar que las columnas existan en el DataFrame
    if all(col in st.session_state['data'].columns for col in columnas_a_mostrar):
        # Filtrar datos para las columnas relevantes
        df_filtered = st.session_state['data'][columnas_a_mostrar].head(10)  # Muestra solo los primeros 10 registros
        
        # Configurar column_config para mostrar imágenes en Team Logo
        st.write("Vista previa de los datos:")
        st.data_editor(
            df_filtered,
            column_config={
                "Team logo": st.column_config.ImageColumn(
                    "Team logo", help="Logos of the teams", width="100px"
                ),
            },
            hide_index=True,
        )
    else:
        st.warning("No se encontraron todas las columnas necesarias en los datos.")
else:
    st.info("Haz clic en el botón 'Cargar Datos' para cargar los archivos.")

