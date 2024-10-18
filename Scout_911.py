import streamlit as st
from pathlib import Path
import importlib.util

# Configuración de la página en modo wide
st.set_page_config(page_title="Scout_911", layout="wide")

# Título de la aplicación
st.title("Scout_911")
st.subheader("By CECO")

# Definir las páginas disponibles
pages = {
    "🔍 Búsqueda General": "Pages/Busqueda_General.py",
    "📊 Comparación de Métricas": "Pages/Comparacion_Metricas.py",
    "📈 % de Similitud": "Pages/Porcentaje_Similitud.py",
    "⭐ Scoring": "Pages/Scoring.py",
    "⚽ Smart 11": "Pages/Smart_11.py"
}

# Selección de la página desde la barra lateral
page = st.sidebar.selectbox("Selecciona una página", pages.keys())

# Función para cargar y ejecutar una página dada su ruta
def run_page(page_path):
    page_file = Path(page_path)
    spec = importlib.util.spec_from_file_location(page_file.stem, page_file)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

# Ejecutar la página seleccionada
run_page(pages[page])
