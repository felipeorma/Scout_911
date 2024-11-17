# Importar las librerías necesarias
import streamlit as st
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.metrics.pairwise import cosine_similarity, euclidean_distances

# Diccionario de métricas por posición
metrics_by_position = {
    'Portero': ["Matches played", "Minutes played", "Conceded goals per 90", "xG against per 90", 
                "Prevented goals per 90", "Save rate, %", "Exits per 90", "Aerial duels per 90", 
                "Back passes received as GK per 90", "Accurate passes, %", "Accurate forward passes, %", 
                "Accurate long passes, %"],
    'Defensa': ["Matches played", "Minutes played", "Accelerations per 90", "Progressive runs per 90", 
                "Aerial duels per 90", "Aerial duels won, %", "Defensive duels won, %", "Duels won, %", 
                "Sliding tackles per 90", "Interceptions per 90", "Key passes per 90", "Short / medium passes per 90", 
                "Forward passes per 90", "Long passes per 90", "Passes per 90", "Accurate passes to final third, %", 
                "Accurate forward passes, %", "Accurate back passes, %", "Accurate long passes, %", "Accurate passes, %"],
    'Lateral Izquierdo': ["Matches played", "Minutes played", "Successful attacking actions per 90", 
                          "Successful defensive actions per 90", "Accelerations per 90", "Progressive runs per 90", 
                          "Crosses to goalie box per 90", "Aerial duels won, %", "Offensive duels won, %", 
                          "Defensive duels won, %", "Defensive duels per 90", "Duels won, %", 
                          "Interceptions per 90", "Passes per 90", "Forward passes per 90", 
                          "Accurate passes to penalty area, %", "Received passes per 90", 
                          "Accurate passes to final third, %", "Accurate through passes, %", 
                          "Accurate forward passes, %", "Accurate progressive passes, %", "Third assists per 90", "xA per 90"],
    'Lateral Derecho': ["Matches played", "Minutes played", "Successful attacking actions per 90", 
                        "Successful defensive actions per 90", "Accelerations per 90", "Progressive runs per 90", 
                        "Crosses to goalie box per 90", "Aerial duels won, %", "Offensive duels won, %", 
                        "Defensive duels won, %", "Defensive duels per 90", "Duels won, %", 
                        "Interceptions per 90", "Passes per 90", "Forward passes per 90", 
                        "Accurate passes to penalty area, %", "Received passes per 90", 
                        "Accurate passes to final third, %", "Accurate through passes, %", 
                        "Accurate forward passes, %", "Accurate progressive passes, %", "Third assists per 90", "xA per 90"],
    'Mediocampista Defensivo': ["Matches played", "Minutes played", "Assists per 90", "xA per 90", "Offensive duels won, %", 
                                "Aerial duels won, %", "Defensive duels won, %", "Interceptions per 90", 
                                "Received passes per 90", "Accurate short / medium passes, %", 
                                "Accurate passes to final third, %", "Accurate long passes, %", 
                                "Accurate progressive passes, %", "Successful dribbles, %", "xG per 90", "Goals per 90"],
    'Mediocampista Central': ["Matches played", "Minutes played", "Assists per 90", "xA per 90", "Offensive duels won, %", 
                              "Aerial duels won, %", "Defensive duels won, %", "Interceptions per 90", 
                              "Received passes per 90", "Accurate short / medium passes, %", 
                              "Accurate passes to final third, %", "Accurate long passes, %", 
                              "Accurate progressive passes, %", "Successful dribbles, %", "xG per 90", "Goals per 90"],
    'Mediocampista Ofensivo': ["Matches played", "Minutes played", "Assists per 90", "xA per 90", "Offensive duels won, %", 
                               "Aerial duels won, %", "Defensive duels won, %", "Interceptions per 90", 
                               "Received passes per 90", "Accurate short / medium passes, %", 
                               "Accurate passes to final third, %", "Accurate long passes, %", 
                               "Accurate progressive passes, %", "Successful dribbles, %", "xG per 90", "Goals per 90"],
    'Extremos': ["Matches played", "Minutes played", "xG per 90", "Goals per 90", "Assists per 90", 
                 "xA per 90", "Received passes per 90", "Accurate crosses, %", "Accurate through passes, %", 
                 "Accurate progressive passes, %", "Crosses to goalie box per 90", "Accurate passes to penalty area, %", 
                 "Offensive duels won, %", "Defensive duels won, %", "Interceptions per 90", "Successful dribbles, %"],
    'Delantero': ["Matches played", "Minutes played", "Goals per 90", "Head goals per 90", 
                  "Non-penalty goals per 90", "Goal conversion, %", "xG per 90", "xA per 90", 
                  "Assists per 90", "Key passes per 90", "Passes per 90", "Passes to penalty area per 90", 
                  "Passes to final third per 90", "Accurate passes, %", "Accurate passes to final third, %", 
                  "Aerial duels won, %", "Duels won, %", "Shots per 90", "Shots on target, %", "Touches in box per 90"]
}

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
    
    st.title("Comparador de Similitud de Jugadores")

    # Paso 1: Seleccionar jugador/equipo (combinación única)
    jugador_equipo = st.selectbox("Selecciona un jugador/equipo", df['Jugador_Equipo'].unique())
    df_jugador = df[df['Jugador_Equipo'] == jugador_equipo].copy()

    if df_jugador.empty:
        st.warning(f"No se encontró el jugador '{jugador_equipo}' en los datos originales.")
    else:
        # Paso 2: Filtro de posición y obtención de métricas específicas
        posiciones = list(metrics_by_position.keys())
        selected_position = st.selectbox("Selecciona la posición del jugador", posiciones)
        metricas_seleccionadas = metrics_by_position[selected_position]

        # Paso 3: Filtrar jugadores restantes por posición
        if selected_position == 'Portero':
            df_restantes = df[df['Position'].str.contains('GK', na=False)]
        elif selected_position == 'Defensa':
            df_restantes = df[df['Position'].str.contains('CB', na=False)]
        elif selected_position == 'Lateral Izquierdo':
            df_restantes = df[df['Position'].str.contains('LB|LWB', na=False)]
        elif selected_position == 'Lateral Derecho':
            df_restantes = df[df['Position'].str.contains('RB|RWB', na=False)]
        elif selected_position == 'Mediocampista Defensivo':
            df_restantes = df[df['Position'].str.contains('DMF', na=False)]
        elif selected_position == 'Mediocampista Central':
            df_restantes = df[df['Position'].str.contains('CMF', na=False)]
        elif selected_position == 'Mediocampista Ofensivo':
            df_restantes = df[df['Position'].str.contains('AMF', na=False)]
        elif selected_position == 'Extremos':
            df_restantes = df[df['Position'].str.contains('RW|LW|LWF|RWF', na=False)]
        elif selected_position == 'Delantero':
            df_restantes = df[df['Position'].str.contains('CF', na=False)]
        else:
            df_restantes = df.copy()  # Si no hay un filtro válido, no se aplica ningún filtro

        # Paso 4: Filtrar por pasaporte
        if 'Passport country' in df.columns:
            input_passport = st.text_input("Filtrar por país de pasaporte (ej. 'Argentina')", "")
            if input_passport:
                df_restantes = df_restantes[df_restantes['Passport country'].str.contains(input_passport, case=False, na=False)]

        # Paso 5: Normalización y comparación
        scaler = StandardScaler()
        df_restantes[metricas_seleccionadas] = df_restantes[metricas_seleccionadas].fillna(0)
        df_jugador[metricas_seleccionadas] = df_jugador[metricas_seleccionadas].fillna(0)

        df_scaled = pd.DataFrame(
            scaler.fit_transform(df_restantes[metricas_seleccionadas]),
            columns=metricas_seleccionadas,
            index=df_restantes.index
        )
        jugador_scaled = scaler.transform(df_jugador[metricas_seleccionadas])

        # Calcular similitudes
        distancias_euclid = euclidean_distances(jugador_scaled, df_scaled).flatten()
        similitudes_coseno = cosine_similarity(jugador_scaled, df_scaled).flatten()

        # Calcular porcentajes
        max_dist = distancias_euclid.max()
        df_restantes['Similitud Euclídea (%)'] = (1 - (distancias_euclid / max_dist)) * 100
        df_restantes['Similitud Coseno (%)'] = similitudes_coseno * 100

        # Ordenar y mostrar resultados
        similares_euclid = df_restantes[['Full name', 'Age', 'Team within selected timeframe', 'Similitud Euclídea (%)']].sort_values('Similitud Euclídea (%)', ascending=False).head(10)
        similares_coseno = df_restantes[['Full name', 'Age', 'Team within selected timeframe', 'Similitud Coseno (%)']].sort_values('Similitud Coseno (%)', ascending=False).head(10)

        col1, col2 = st.columns(2)
        with col1:
            st.subheader(f"Jugadores más similares a {jugador_equipo} (Distancia Euclídea)")
            st.dataframe(similares_euclid)

        with col2:
            st.subheader(f"Jugadores más similares a {jugador_equipo} (Distancia Coseno)")
            st.dataframe(similares_coseno)
