import streamlit as st
import pandas as pd

# URL base de los archivos en GitHub
GITHUB_RAW_BASE = "https://raw.githubusercontent.com/CarlosCO94/Scout_911/main/data/"

# Nombres de los archivos que deseas cargar
league_files = [
    "Argentina Copa de la Liga 2024.parquet",
    "Argentina Primera Nacional 2024.parquet",
    "Bolivian LFPB 2024.parquet",
    "Brasileirão 2024.parquet",
    "Brazil Serie B 2024.parquet",
    "Brazil Serie C 2024.parquet",
    "Chilean Primera B 2024.parquet",
    "Chilean Primera Division 2024.parquet",
    "Colombian Primera A 2024.parquet",
    "Colombian Torneo BetPlay 2024.parquet",
    "Ecuador Liga Pro 2024.parquet",
    "MLS 2024.parquet",
    "Panama LPF 2024.parquet",
    "Paraguay Division Profesional 2024.parquet",
    "Peruvian Liga 1 2024.parquet",
    "Uruguay Primera División 2024.parquet"
]

# Función para cargar todos los datos en session_state
def load_all_league_data():
    if 'data' not in st.session_state:
        st.session_state['data'] = {}
        for league_file in league_files:
            url = GITHUB_RAW_BASE + league_file
            st.session_state['data'][league_file] = pd.read_parquet(url)

# Función para obtener los datos
def get_data():
    if 'data' in st.session_state:
        return st.session_state['data']
    return None

# Llamada para cargar todos los datos una vez
load_all_league_data()

# Ponderaciones para cada posición
weights = {
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
    'Lateral': {
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
    'Mediocampista': {
        'Assists per 90': 0.15,
        'xA per 90': 0.1,
        'Offensive duels won, %': 0.1,
        'Aerial duels won, %': 0.05,
        'Defensive duels won, %': 0.05,
        'Interceptions per 90': 0.1,
        'Received passes per 90': 0.05,
        'Accurate short / medium passes, %': 0.1,
        'Accurate passes to final third, %': 0.1,
        'Accurate long passes, %': 0.05,
        'Accurate progressive passes, %': 0.05,
        'Successful dribbles, %': 0.1,
        'xG per 90': 0.05,
        'Goals per 90': 0.1
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
        'Touches in box per 90': 0.05}
}

# Función para calcular el puntaje basado en la posición
def calculate_score(row, position):
    score = 0
    if position in weights:
        for metric, weight in weights[position].items():
            score += row.get(metric, 0) * weight
    return score

# Configuración de la página de Streamlit
st.title("Sistema de Scoring de Jugadores por Liga")
st.write("Selecciona una liga y una posición para calcular el scoring de los jugadores.")

# Selección de liga
selected_league = st.selectbox("Selecciona la liga", league_files)
data = get_data()[selected_league] if get_data() else None

# Selección de posición
selected_position = st.selectbox("Selecciona la posición", [
    'Arquero', 'Defensa', 'Lateral Izquierdo', 'Lateral Derecho', 
    'Mediocampista Defensivo', 'Mediocampista Central', 'Mediocampista Ofensivo', 
    'Extremos', 'Delantero'
])

if data is not None:
    # Aplicar filtro de posición
    if selected_position == 'Arquero':
        df = data[data['Position'].str.contains('GK', na=False)]
    elif selected_position == 'Defensa':
        df = data[data['Position'].str.contains('CB', na=False)]
    elif selected_position == 'Lateral Izquierdo':
        df = data[data['Position'].str.contains('LB|LWB', na=False)]
    elif selected_position == 'Lateral Derecho':
        df = data[data['Position'].str.contains('RB|RWB', na=False)]
    elif selected_position == 'Mediocampista Defensivo':
        df = data[data['Position'].str.contains('DMF', na=False)]
    elif selected_position == 'Mediocampista Central':
        df = data[data['Position'].str.contains('CMF', na=False)]
    elif selected_position == 'Mediocampista Ofensivo':
        df = data[data['Position'].str.contains('AMF', na=False)]
    elif selected_position == 'Extremos':
        df = data[data['Position'].str.contains('RW|LW|LWF|RWF', na=False)]
    elif selected_position == 'Delantero':
        df = data[data['Position'].str.contains('CF', na=False)]
    
    # Calcular el scoring para la posición filtrada
    df['Score Total'] = df.apply(lambda row: calculate_score(row, selected_position), axis=1)

    # Normalizar los puntajes a una escala de 1 a 10
    min_score, max_score = df['Score Total'].min(), df['Score Total'].max()
    df['Score Total'] = df['Score Total'].apply(lambda x: 1 + (x - min_score) * 9 / (max_score - min_score) if max_score > min_score else 1)

    # Seleccionar las columnas deseadas y mostrar solo los 10 primeros resultados
    st.write(f"Scoring calculado para la posición: {selected_position}")
    st.dataframe(df[['Full name', 'Team within selected timeframe', 'Age', 'Passport country', 'Score Total']].head(10))
else:
    st.write("No se encontraron datos en session_state. Por favor, carga los datos antes de continuar.")
