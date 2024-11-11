import streamlit as st
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.metrics.pairwise import cosine_similarity, euclidean_distances

# Función para cargar los datos desde el session_state
def get_data():
    if 'data' in st.session_state:
        return st.session_state['data']
    return None

# Cargar los datos desde session_state
df = get_data()

# Verificar si el DataFrame está en session_state
if df is None:
    st.warning("Los datos no están disponibles. Por favor, carga los datos en la página principal.")
else:
    # Crear una columna única para identificar cada combinación jugador/equipo
    df['Jugador_Equipo'] = df['Full name'] + " - " + df['Team within selected timeframe']
    
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

    st.title("Comparador de Similitud de Jugadores")

    # Paso 1: Seleccionar jugador/equipo (combinación única)
    jugador_equipo = st.selectbox("Selecciona un jugador/equipo", df['Jugador_Equipo'].unique())
    df_jugador = df[df['Jugador_Equipo'] == jugador_equipo].copy()  # DataFrame solo con el jugador/equipo seleccionado

    # Verificar si el jugador fue encontrado en los datos
    if df_jugador.empty:
        st.warning(f"No se encontró el jugador '{jugador_equipo}' en los datos originales.")
    else:
        # Paso 2: Crear un DataFrame df_restantes excluyendo al jugador/equipo seleccionado
        df_restantes = df[df['Jugador_Equipo'] != jugador_equipo].copy()

        # Paso 3: Filtrar jugadores por rango de edad solo en df_restantes
        if 'Age' in df.columns:
            min_age, max_age = int(df['Age'].min()), int(df['Age'].max())
            selected_age_range = st.slider("Seleccione el rango de edad", min_value=min_age, max_value=max_age, value=(min_age, max_age))
            df_restantes = df_restantes[(df_restantes['Age'] >= selected_age_range[0]) & (df_restantes['Age'] <= selected_age_range[1])]
        else:
            st.warning("No se encontraron datos de edad en los archivos.")

        # Paso 4: Filtrar por pasaporte en df_restantes
        if 'Passport country' in df.columns:
            input_passport = st.text_input("Filtrar por pasaporte (ej. 'Argentina')", "")
            if input_passport:
                df_restantes = df_restantes[df_restantes['Passport country'].str.contains(input_passport, case=False, na=False)]
        
        # Seleccionar las métricas para la comparación
        metricas_seleccionadas = st.multiselect("Selecciona las métricas para la comparación", metricas_permitidas, default=metricas_permitidas[:5])
        df_restantes[metricas_seleccionadas] = df_restantes[metricas_seleccionadas].fillna(0)
        df_jugador[metricas_seleccionadas] = df_jugador[metricas_seleccionadas].fillna(0)

        # Normalizar los datos de df_restantes y del jugador/equipo seleccionado
        scaler = StandardScaler()
        df_scaled = pd.DataFrame(scaler.fit_transform(df_restantes[metricas_seleccionadas]), columns=metricas_seleccionadas, index=df_restantes.index)
        jugador_scaled = scaler.transform(df_jugador[metricas_seleccionadas])

        # Calcular distancias y similitudes
        distancias_euclid = euclidean_distances(jugador_scaled, df_scaled).flatten()
        similitudes_coseno = cosine_similarity(jugador_scaled, df_scaled).flatten()

        # Calcular porcentaje de similitud
        max_dist = distancias_euclid.max()
        df_restantes['Similitud Euclídea (%)'] = (1 - (distancias_euclid / max_dist)) * 100
        df_restantes['Similitud Coseno (%)'] = similitudes_coseno * 100

        # Ordenar y mostrar resultados
        similares_euclid = df_restantes[['Full name', 'Age', 'Team within selected timeframe', 'Similitud Euclídea (%)']].sort_values('Similitud Euclídea (%)', ascending=False).head(10)
        similares_coseno = df_restantes[['Full name', 'Age', 'Team within selected timeframe', 'Similitud Coseno (%)']].sort_values('Similitud Coseno (%)', ascending=False).head(10)

        # Mostrar tablas de resultados
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader(f"Jugadores más similares a {jugador_equipo} (Distancia Euclídea)")
            st.dataframe(similares_euclid)
            st.markdown("""La distancia euclídea mide la distancia "común" entre los valores de las métricas de dos jugadores. Si dos jugadores tienen valores de métricas cercanos, serán considerados similares.""")

        
        with col2:
            st.subheader(f"Jugadores más similares a {jugador_equipo} (Distancia Coseno)")
            st.dataframe(similares_coseno)
            st.markdown("""La distancia coseno mide el ángulo entre los vectores de las métricas de dos jugadores. Esto significa que un jugador con menos minutos jugados puede parecer similar a otro con más minutos jugados si sus valores de métricas están en la misma dirección.""")
