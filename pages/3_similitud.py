import streamlit as st
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.metrics.pairwise import euclidean_distances, cosine_similarity

# Lista de métricas permitidas para la comparación
metricas_permitidas = [
    'Duels per 90', 'Duels won, %', 'Successful defensive actions per 90', 'Defensive duels per 90',
    'Defensive duels won, %', 'Aerial duels per 90', 'Aerial duels won, %', 'Sliding tackles per 90', 
    'PAdj Sliding tackles', 'Shots blocked per 90', 'Interceptions per 90', 'PAdj Interceptions', 
    'Fouls per 90', 'Yellow cards', 'Yellow cards per 90', 'Red cards', 'Red cards per 90', 
    'Successful attacking actions per 90', 'Goals per 90', 'Non-penalty goals', 'Non-penalty goals per 90', 
    'xG per 90', 'Head goals', 'Head goals per 90', 'Shots', 'Shots per 90', 'Shots on target, %', 
    'Goal conversion, %', 'Assists per 90', 'Crosses per 90', 'Accurate crosses, %', 'Crosses from left flank per 90', 
    'Accurate crosses from left flank, %', 'Crosses from right flank per 90', 'Accurate crosses from right flank, %', 
    'Crosses to goalie box per 90', 'Dribbles per 90', 'Successful dribbles, %', 'Offensive duels per 90', 
    'Offensive duels won, %', 'Touches in box per 90', 'Progressive runs per 90', 'Accelerations per 90', 
    'Received passes per 90', 'Received long passes per 90', 'Fouls suffered per 90', 'Passes per 90', 
    'Accurate passes, %', 'Forward passes per 90', 'Accurate forward passes, %', 'Back passes per 90', 
    'Accurate back passes, %', 'Short / medium passes per 90', 'Accurate short / medium passes, %', 
    'Long passes per 90', 'Accurate long passes, %', 'Average pass length, m', 'Average long pass length, m', 
    'xA per 90', 'Shot assists per 90', 'Second assists per 90', 'Third assists per 90', 'Smart passes per 90', 
    'Accurate smart passes, %', 'Key passes per 90', 'Passes to final third per 90', 
    'Accurate passes to final third, %', 'Passes to penalty area per 90', 'Accurate passes to penalty area, %', 
    'Through passes per 90', 'Accurate through passes, %', 'Deep completions per 90', 'Deep completed crosses per 90', 
    'Progressive passes per 90', 'Accurate progressive passes, %', 'Accurate vertical passes, %', 
    'Vertical passes per 90', 'Conceded goals', 'Conceded goals per 90', 'Shots against', 'Shots against per 90', 
    'Clean sheets', 'Save rate, %', 'xG against', 'xG against per 90', 'Prevented goals', 'Prevented goals per 90', 
    'Back passes received as GK per 90', 'Exits per 90', 'Aerial duels per 90.1', 'Free kicks per 90', 
    'Direct free kicks per 90', 'Direct free kicks on target, %', 'Corners per 90', 'Penalties taken', 
    'Penalty conversion, %'
]

# Función principal para la búsqueda de jugadores similares
def busqueda_similaridad():
    st.title("Búsqueda de Jugadores Similares")
    
    # Obtener los datos cargados desde session_state
    df = st.session_state.data if 'data' in st.session_state else None
    
    if df is None or df.empty:
        st.warning("No hay datos cargados. Por favor, asegúrate de que los datos se han cargado correctamente en la página principal.")
        return
    
    # Paso 1: Filtro de competición (basado en los archivos Parquet cargados)
    if 'source_file' in df.columns:
        competencia_seleccionada = st.multiselect("Competición (archivo)", df['source_file'].unique().tolist())
        if competencia_seleccionada:
            df = df[df['source_file'].isin(competencia_seleccionada)]
        else:
            st.warning("Selecciona al menos una competencia para continuar.")
            return
    else:
        st.warning("No se encontraron archivos de competencias.")
        return

    # Paso 2: Selección de jugador
    nombre_col = 'Full name' if 'Full name' in df.columns else 'nombre'
    jugadores_disponibles = df[nombre_col].tolist()  # Lista de jugadores disponibles después de filtrar
    jugador = st.selectbox("Seleccione un jugador", jugadores_disponibles)
    
    # Verificar si el jugador está en los datos
    if jugador not in jugadores_disponibles:
        st.warning("El jugador seleccionado no se encuentra en los datos filtrados.")
        return

    # Paso 3: Filtrar las métricas para la comparación, considerando solo las permitidas
    numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns
    metricas_validas = [col for col in numeric_cols if col in metricas_permitidas]  # Filtrar las métricas válidas

    if not metricas_validas:
        st.warning("No se encontraron métricas válidas para comparar.")
        return

    metricas_seleccionadas = st.multiselect("Seleccione las métricas para calcular la similitud", metricas_validas, default=metricas_validas)
    if not metricas_seleccionadas:
        st.warning("Por favor, seleccione al menos una métrica para calcular la similitud.")
        return

    # Paso 4: Filtrar jugadores por rango de edad, excluyendo al jugador seleccionado
    if 'Age' in df.columns:
        min_age, max_age = int(df['Age'].min()), int(df['Age'].max())
        selected_age_range = st.slider("Seleccione el rango de edad", min_value=min_age, max_value=max_age, value=(min_age, max_age))

        # Filtrar por edad, pero sin eliminar al jugador seleccionado
        df_filtrado = df[(df['Age'] >= selected_age_range[0]) & (df['Age'] <= selected_age_range[1]) | (df[nombre_col] == jugador)]
    else:
        st.warning("No se encontraron datos de edad en los archivos.")
        return

    # Paso 5: Manejar NaN en los datos seleccionados
    if df_filtrado[metricas_seleccionadas].isnull().values.any():
        st.warning("Se encontraron valores NaN en los datos de métricas seleccionadas. Se reemplazarán con ceros.")
        df_filtrado[metricas_seleccionadas] = df_filtrado[metricas_seleccionadas].fillna(0)

    # Normalizar los datos en función de las métricas seleccionadas
    scaler = StandardScaler()
    df_scaled = pd.DataFrame(scaler.fit_transform(df_filtrado[metricas_seleccionadas]), columns=metricas_seleccionadas, index=df_filtrado.index)

    # Paso 6: Cálculo de la similitud
    jugador_fila = df_filtrado[df_filtrado[nombre_col] == jugador]
    
    # Obtener el índice del jugador
    jugador_index = jugador_fila.index[0]

    # Calcular la distancia euclidiana
    distancias_euclid = euclidean_distances(df_scaled.loc[[jugador_index]], df_scaled).flatten()
    
    # Calcular la similitud basada en el coseno
    similitudes_coseno = cosine_similarity(df_scaled.loc[[jugador_index]], df_scaled).flatten()

    # Calcular la similitud como un porcentaje (inverso de la distancia euclidiana)
    max_dist = distancias_euclid.max()
    df_filtrado['Similitud Euclídea (%)'] = (1 - (distancias_euclid / max_dist)) * 100

    # La similitud coseno ya está entre 0 y 1, por lo que simplemente la multiplicamos por 100 para tener un porcentaje
    df_filtrado['Similitud Coseno (%)'] = similitudes_coseno * 100

    # Excluir al jugador seleccionado de las tablas de resultados
    df_filtrado = df_filtrado[df_filtrado[nombre_col] != jugador]

    # Ordenar los jugadores por las dos distancias (euclidiana y coseno)
    similares_euclid = df_filtrado[[nombre_col, 'Age', 'Team within selected timeframe', 'Similitud Euclídea (%)']].sort_values('Similitud Euclídea (%)', ascending=False).head(10)
    similares_coseno = df_filtrado[[nombre_col, 'Age', 'Team within selected timeframe', 'Similitud Coseno (%)']].sort_values('Similitud Coseno (%)', ascending=False).head(10)

    # Mostrar las tablas de resultados lado a lado
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader(f"Jugadores más similares a {jugador} (Distancia Euclídea)")
        st.dataframe(similares_euclid)
        st.markdown("""
        **Distancia Euclídea**  
        La distancia euclídea mide la distancia "común" entre los valores de las métricas de dos jugadores. Si dos jugadores tienen valores de métricas cercanos, serán considerados similares.
        """)
        
    with col2:
        st.subheader(f"Jugadores más similares a {jugador} (Distancia Coseno)")
        st.dataframe(similares_coseno)
        st.markdown("""
        **Distancia Coseno**  
        La distancia coseno mide el ángulo entre los vectores de las métricas de dos jugadores. Esto significa que un jugador con menos minutos jugados puede parecer similar a otro con más minutos jugados si sus valores de métricas están en la misma dirección.
        """)

# Llamar a la función principal
if __name__ == "__main__":
    busqueda_similaridad()
