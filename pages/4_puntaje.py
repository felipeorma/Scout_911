import streamlit as st
import pandas as pd
import requests
from io import BytesIO

# Configurar la página en formato "wide"
st.set_page_config(page_title="911_Scout - Scoring", page_icon="⚽", layout="wide")
st.subheader("By: CECO")

# Título principal
st.header("Scoring de Jugadores")

# URL base de los archivos en GitHub
GITHUB_RAW_BASE = "https://raw.githubusercontent.com/CarlosCO94/Scout_911/main/data/"

# Nombres de los archivos de liga
league_files = {
    "Argentina Copa de la Liga 2024": "Argentina Copa de la Liga 2024.parquet",
    "Argentina Primera Nacional 2024": "Argentina Primera Nacional 2024.parquet",
    "Bolivian LFPB 2024": "Bolivian LFPB 2024.parquet",
    "Brasileirão 2024": "Brasileirão 2024.parquet",
    "Brazil Serie B 2024": "Brazil Serie B 2024.parquet",
    "Brazil Serie C 2024": "Brazil Serie C 2024.parquet",
    "Chilean Primera B 2024": "Chilean Primera B 2024.parquet",
    "Chilean Primera Division 2024": "Chilean Primera Division 2024.parquet",
    "Colombian Primera A 2024": "Colombian Primera A 2024.parquet",
    "Colombian Torneo BetPlay 2024": "Colombian Torneo BetPlay 2024.parquet",
    "Ecuador Liga Pro 2024": "Ecuador Liga Pro 2024.parquet",
    "MLS 2024": "MLS 2024.parquet",
    "Panama LPF 2024": "Panama LPF 2024.parquet",
    "Paraguay Division Profesional 2024": "Paraguay Division Profesional 2024.parquet",
    "Peruvian Liga 1 2024": "Peruvian Liga 1 2024.parquet",
    "Uruguay Primera División 2024": "Uruguay Primera División 2024.parquet",
    # Agrega el resto de archivos aquí
}

# Función para cargar datos de una liga específica desde GitHub
def load_league_data(league_file):
    url = GITHUB_RAW_BASE + league_file.replace(" ", "%20")
    response = requests.get(url)
    response.raise_for_status()
    return pd.read_parquet(BytesIO(response.content))

# Ponderaciones para cada posición
weights = {
    'Mediocampista Ofensivo': {
        'Assists per 90': 0.2,
        'xA per 90': 0.15,
        'Key passes per 90': 0.15,
        'Accurate passes to penalty area, %': 0.1,
        'Successful dribbles, %': 0.1,
        'Goals per 90': 0.1,
        'Offensive duels won, %': 0.1,
        'Accurate forward passes, %': 0.05,
        'Accurate progressive passes, %': 0.05,
        'Interceptions per 90': 0.05
    },
    'Arquero': {
        'Save rate, %': 0.15,
        'Conceded goals per 90': -0.1,
        'Prevented goals per 90': 0.15,
        'Exits per 90': 0.1,
        'Aerial duels per 90': 0.1,
        'Back passes received as GK per 90': 0.05,
        'Accurate passes, %': 0.1,
        'Accurate forward passes, %': 0.1,
        'Accurate long passes, %': 0.05,
        'xG against per 90': -0.1
    },
    'Defensa': {
        'Defensive duels won, %': 0.15,
        'Interceptions per 90': 0.15,
        'Aerial duels per 90': 0.1,
        'Aerial duels won, %': 0.1,
        'Duels won, %': 0.05,
        'Sliding tackles per 90': 0.1,
        'Accurate passes, %': 0.05,
        'Accurate forward passes, %': 0.05,
        'Accurate passes to final third, %': 0.05,
        'Long passes per 90': 0.05,
        'Accelerations per 90': 0.05,
        'Progressive runs per 90': 0.1,
        'Key passes per 90': 0.1
    },
    'Lateral Izquierdo': {
        'Successful attacking actions per 90': 0.15,
        'Successful defensive actions per 90': 0.1,
        'Crosses to goalie box per 90': 0.1,
        'Aerial duels won, %': 0.1,
        'Offensive duels won, %': 0.1,
        'Defensive duels won, %': 0.1,
        'Duels won, %': 0.05,
        'Interceptions per 90': 0.05,
        'Accurate passes to penalty area, %': 0.05,
        'Third assists per 90': 0.05,
        'xA per 90': 0.05,
        'Accelerations per 90': 0.05,
        'Progressive runs per 90': 0.1
    },
    'Lateral Derecho': {
        'Successful attacking actions per 90': 0.15,
        'Successful defensive actions per 90': 0.1,
        'Crosses to goalie box per 90': 0.1,
        'Aerial duels won, %': 0.1,
        'Offensive duels won, %': 0.1,
        'Defensive duels won, %': 0.1,
        'Duels won, %': 0.05,
        'Interceptions per 90': 0.05,
        'Accurate passes to penalty area, %': 0.05,
        'Third assists per 90': 0.05,
        'xA per 90': 0.05,
        'Accelerations per 90': 0.05,
        'Progressive runs per 90': 0.1
    },
    'Mediocampista Defensivo': {
        'Defensive duels won, %': 0.2,
        'Interceptions per 90': 0.15,
        'Aerial duels won, %': 0.1,
        'Accurate short / medium passes, %': 0.1,
        'Accurate long passes, %': 0.1,
        'Offensive duels won, %': 0.05,
        'xA per 90': 0.05,
        'Progressive runs per 90': 0.05,
        'Successful dribbles, %': 0.05,
        'Goals per 90': 0.05,
        'Received passes per 90': 0.05,
        'Accurate progressive passes, %': 0.05
    },
    'Mediocampista Central': {
        'Assists per 90': 0.15,
        'xA per 90': 0.1,
        'Accurate passes to final third, %': 0.15,
        'Defensive duels won, %': 0.1,
        'Interceptions per 90': 0.1,
        'Received passes per 90': 0.1,
        'Accurate short / medium passes, %': 0.1,
        'Accurate long passes, %': 0.05,
        'Progressive runs per 90': 0.1,
        'Goals per 90': 0.05
    },
    'Extremos': {
        'xG per 90': 0.15,
        'Goals per 90': 0.15,
        'Assists per 90': 0.1,
        'xA per 90': 0.1,
        'Received passes per 90': 0.05,
        'Accurate crosses, %': 0.05,
        'Accurate through passes, %': 0.05,
        'Accurate progressive passes, %': 0.1,
        'Crosses to goalie box per 90': 0.1,
        'Accurate passes to penalty area, %': 0.05,
        'Offensive duels won, %': 0.05,
        'Defensive duels won, %': 0.05,
        'Interceptions per 90': 0.05,
        'Successful dribbles, %': 0.1
    },
    'Delantero': {
        'Goals per 90': 0.2,
        'Head goals per 90': 0.05,
        'Non-penalty goals per 90': 0.05,
        'Goal conversion, %': 0.1,
        'xG per 90': 0.1,
        'xA per 90': 0.1,
        'Assists per 90': 0.05,
        'Key passes per 90': 0.05,
        'Passes to penalty area per 90': 0.05,
        'Passes to final third per 90': 0.05,
        'Accurate passes, %': 0.05,
        'Accurate passes to final third, %': 0.05,
        'Aerial duels won, %': 0.05,
        'Duels won, %': 0.05,
        'Shots per 90': 0.05,
        'Shots on target, %': 0.05,
        'Touches in box per 90': 0.05
    }
}
# Función para calcular el puntaje basado en la posición, validando métricas
def calculate_score(row, position):
    score = 0
    if position in weights:
        for metric, weight in weights[position].items():
            if metric in row and pd.notna(row[metric]):
                score += row[metric] * weight
    return score

# Convertir el score a estrellas
def score_to_stars(score, max_stars=5):
    # Escala de Score Total (1 a 10) a estrellas (0 a max_stars)
    scaled_rating = (score - 1) * max_stars / 9  # Ajuste en escala a 0-max_stars
    full_stars = int(scaled_rating)
    half_star = (scaled_rating - full_stars) >= 0.5
    
    stars = '★' * full_stars  # Estrellas completas
    if half_star:
        stars += '★'  # Media estrella
    empty_stars = max_stars - full_stars - half_star
    stars += '☆' * empty_stars  # Estrellas vacías
    return stars

# Selección de liga
selected_league = st.selectbox("Selecciona la liga para cargar datos", list(league_files.keys()))

if selected_league:
    try:
        data = load_league_data(league_files[selected_league])
        st.write(f"Datos cargados para: {selected_league}")

        # Selección de posición
        selected_position = st.selectbox("Selecciona la posición para calcular scoring", [
            'Arquero', 'Defensa', 'Lateral Izquierdo', 'Lateral Derecho', 
            'Mediocampista Defensivo', 'Mediocampista Central', 'Mediocampista Ofensivo', 
            'Extremos', 'Delantero'
        ])

        # Filtrar los datos según la posición seleccionada
        position_map = {
            'Arquero': 'GK',
            'Defensa': 'CB',
            'Lateral Izquierdo': 'LB|LWB',
            'Lateral Derecho': 'RB|RWB',
            'Mediocampista Defensivo': 'DMF',
            'Mediocampista Central': 'CMF',
            'Mediocampista Ofensivo': 'AMF',
            'Extremos': 'RW|LW|LWF|RWF',
            'Delantero': 'CF'
        }
        
        if selected_position in position_map:
            df = data[data['Primary position'].str.contains(position_map[selected_position], na=False)]

        # Calcular el scoring para la posición filtrada
        df['Score Total'] = df.apply(lambda row: calculate_score(row, selected_position), axis=1)

        # Normalizar los puntajes a una escala de 1 a 10
        min_score, max_score = df['Score Total'].min(), df['Score Total'].max()
        if min_score != max_score:
            df['Score Total'] = df['Score Total'].apply(lambda x: 1 + (x - min_score) * 9 / (max_score - min_score))
        else:
            df['Score Total'] = 5

        # Agregar la columna de estrellas al DataFrame
        df['Estrellas'] = df['Score Total'].apply(lambda x: score_to_stars(x, max_stars=5))

        # Mostrar los resultados
        st.write(f"Scoring calculado para la posición: {selected_position} en {selected_league}")
        st.dataframe(df[['Full name', 'Team within selected timeframe', 'Age', 'Passport country', 'Score Total', 'Estrellas']].head(10))

    except requests.exceptions.RequestException as e:
        st.error(f"Error al cargar los datos: {e}")
else:
    st.write("Selecciona una liga para comenzar.")
