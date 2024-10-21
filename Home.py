import streamlit as st
import pandas as pd
import io

# Configurar la página en formato "wide"
st.set_page_config(page_title="911_Scout", page_icon="⚽", layout="wide")

# Cargar los archivos de datos
def load_data():
    if 'data' not in st.session_state:
        st.session_state.data = None

    # Cargar archivos Parquet
    uploaded_files = st.file_uploader("Carga tus archivos de datos de jugadores (Parquet)", type="parquet", accept_multiple_files=True)

    if uploaded_files:
        dfs = []
        for file in uploaded_files:
            try:
                # Leer el archivo Parquet
                df = pd.read_parquet(io.BytesIO(file.read()))
                df['source_file'] = file.name  # Agregar nombre del archivo como columna
                dfs.append(df)
            except Exception as e:
                st.error(f"Error al leer el archivo {file.name}: {str(e)}")
        
        # Concatenar los archivos cargados y almacenarlos en session_state
        if dfs:
            st.session_state.data = pd.concat(dfs, ignore_index=True)
            st.success("¡Datos cargados exitosamente!")
    else:
        st.warning("Por favor, carga tus archivos Parquet para continuar.")

# Llamar a la función para cargar datos
load_data()

# Mostrar los datos cargados si existen
if st.session_state.data is not None:
    st.write(f"Total de registros: {len(st.session_state.data)}")
    st.dataframe(st.session_state.data.head())  # Mostrar solo las primeras filas
else:
    st.info("No se han cargado datos aún.")

