import streamlit as st
import pandas as pd

# Función para traducir la posición a términos más comunes
def traducir_posicion(posicion):
    posiciones = {
        'GK': 'arquero',
        'CB': 'defensa central',
        'LB': 'lateral izquierdo',
        'RB': 'lateral derecho',
        'DMF': 'mediocampista defensivo',
        'CMF': 'mediocampista central',
        'AMF': 'mediocampista ofensivo',
        'RW': 'extremo derecho',
        'LW': 'extremo izquierdo',
        'CF': 'delantero centro',
    }
    for abreviatura, nombre in posiciones.items():
        if abreviatura in posicion:
            return nombre
    return posicion  # Si no se encuentra una traducción, retorna la posición original

# Función principal para la búsqueda
def busqueda():
    st.title("Búsqueda de Jugadores")
    
    # Obtener los datos cargados desde session_state
    df = st.session_state['data'] if 'data' in st.session_state and not st.session_state['data'].empty else None
    
    if df is None:
        st.warning("No hay datos cargados. Asegúrate de cargar los datos en la página principal.")
        return

    # Mostrar el número total de registros
    st.write(f"Total de registros: {len(df)}")

    # Filtro de posición principal
    posiciones_disponibles = ['Arquero', 'Defensa', 'Lateral Izquierdo', 'Lateral Derecho',
                              'Mediocampista Defensivo', 'Mediocampista Central', 'Mediocampista Ofensivo',
                              'Extremos', 'Delantero']
    selected_position = st.selectbox("Filtrar por posición principal", posiciones_disponibles)

    # Aplicar filtro de posición
    if selected_position == 'Arquero':
        df = df[df['Position'].str.contains('GK', na=False)]
    elif selected_position == 'Defensa':
        df = df[df['Position'].str.contains('CB', na=False)]
    elif selected_position == 'Lateral Izquierdo':
        df = df[df['Position'].str.contains('LB|LWB', na=False)]
    elif selected_position == 'Lateral Derecho':
        df = df[df['Position'].str.contains('RB|RWB', na=False)]
    elif selected_position == 'Mediocampista Defensivo':
        df = df[df['Position'].str.contains('DMF', na=False)]
    elif selected_position == 'Mediocampista Central':
        df = df[df['Position'].str.contains('CMF', na=False)]
    elif selected_position == 'Mediocampista Ofensivo':
        df = df[df['Position'].str.contains('AMF', na=False)]
    elif selected_position == 'Extremos':
        df = df[df['Position'].str.contains('RW|LW|LWF|RWF', na=False)]
    elif selected_position == 'Delantero':
        df = df[df['Position'].str.contains('CF', na=False)]

    # Filtro de rango de edad y altura en la misma fila
    if 'Age' in df.columns and 'Height' in df.columns:
        col1, col2 = st.columns(2)

        with col1:
            min_age, max_age = int(df['Age'].min()), int(df['Age'].max())
            selected_age_range = st.slider("Selecciona un rango de edad", min_value=min_age, max_value=max_age, value=(min_age, max_age))

        with col2:
            min_height, max_height = int(df['Height'].min()), int(df['Height'].max())
            selected_height_range = st.slider("Selecciona un rango de altura (cm)", min_value=min_height, max_value=max_height, value=(min_height, max_height))

        # Aplicar los filtros de edad y altura
        df = df[(df['Age'] >= selected_age_range[0]) & (df['Age'] <= selected_age_range[1])]
        df = df[(df['Height'] >= selected_height_range[0]) & (df['Height'] <= selected_height_range[1])]
    else:
        st.warning("No se encontraron datos de edad o altura en los archivos.")
    
    # Filtro de pasaporte usando la columna 'Passport country'
    if 'Passport country' in df.columns:
        input_passport = st.text_input("Filtrar por pasaporte (ej. 'España')", "")
        if input_passport:
            df = df[df['Passport country'].str.contains(input_passport, case=False, na=False)]
    else:
        st.warning("No se encontraron datos de pasaporte en los archivos.")

    # Selección de las columnas específicas
    columnas_mostradas = ['Full name', 'Team within selected timeframe', 'Age', 'Position', 'Passport country',
                          'Defensive duels per 90', 'Defensive duels won, %', 'Offensive duels per 90', 'Offensive duels won, %']

    if set(columnas_mostradas).issubset(df.columns):
        df_filtered_columns = df[columnas_mostradas]
        
        # Mostrar los datos en formato de data_editor
        st.data_editor(df_filtered_columns)
    else:
        st.warning("Algunas de las columnas necesarias no están presentes en los datos.")

if __name__ == "__main__":
    busqueda()
