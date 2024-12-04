import streamlit as st
import pandas as pd
import requests
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import matplotlib.pyplot as plt
import numpy as np
import io
import pandas as pd
import math
import matplotlib.patches as patches
from io import BytesIO
from concurrent.futures import ThreadPoolExecutor
from sklearn.preprocessing import StandardScaler
from sklearn.metrics.pairwise import cosine_similarity, euclidean_distances
from mplsoccer import PyPizza
from scipy.stats import percentileofscore
from io import BytesIO
from scipy import stats
from math import pi
from matplotlib.patches import FancyArrowPatch

# Diccionario de métricas por posición
metrics_by_position = {
    'Portero': [
        ("Matches played", "Partidos jugados", "General"),
        ("Minutes played", "Minutos jugados", "General"),
        ("Conceded goals per 90", "Goles concedidos por 90 minutos", "Defensa"),
        ("xG against per 90", "xG en contra por 90 minutos", "Defensa"),
        ("Prevented goals per 90", "Goles evitados por 90 minutos", "Defensa"),
        ("Save rate, %", "Tasa de paradas, %", "Defensa"),
        ("Exits per 90", "Salidas por 90 minutos", "Defensa"),
        ("Aerial duels per 90", "Duelos aéreos por 90 minutos", "Defensa"),
        ("Back passes received as GK per 90", "Pases atrás recibidos como portero por 90 minutos", "Pases"),
        ("Accurate passes, %", "Pases precisos, %", "Pases"),
        ("Accurate forward passes, %", "Pases precisos hacia adelante, %", "Pases"),
        ("Accurate long passes, %", "Pases largos precisos, %", "Pases")
    ],
    'Defensa': [
        ("Matches played", "Partidos jugados", "General"),
        ("Minutes played", "Minutos jugados", "General"),
        ("Aerial duels per 90", "Duelos aéreos por 90 minutos", "Defensa"),
        ("Aerial duels won, %", "Duelos aéreos ganados, %", "Defensa"),
        ("Defensive duels won, %", "Duelos defensivos ganados, %", "Defensa"),
        ("Duels won, %", "Duelos ganados, %", "Defensa"),
        ("Sliding tackles per 90", "Entradas deslizantes por 90 minutos", "Defensa"),
        ("Interceptions per 90", "Intercepciones por 90 minutos", "Defensa"),
        ("Key passes per 90", "Pases clave por 90 minutos", "Pases"),
        ("Short / medium passes per 90", "Pases cortos/medios por 90 minutos", "Pases"),
        ("Forward passes per 90", "Pases hacia adelante por 90 minutos", "Pases"),
        ("Long passes per 90", "Pases largos por 90 minutos", "Pases"),
        ("Passes per 90", "Pases por 90 minutos", "Pases"),
        ("Accurate passes to final third, %", "Pases precisos al tercio final, %", "Pases"),
        ("Accurate forward passes, %", "Pases precisos hacia adelante, %", "Pases"),
        ("Accurate back passes, %", "Pases precisos hacia atrás, %", "Pases"),
        ("Accurate long passes, %", "Pases largos precisos, %", "Pases"),
        ("Accurate passes, %", "Pases precisos, %", "Pases"),
        ("Accelerations per 90", "Aceleraciones por 90 minutos", "Ataque"),
        ("Progressive runs per 90", "Carreras progresivas por 90 minutos", "Ataque")
    ],
    'Lateral Izquierdo': [
        ("Matches played", "Partidos jugados", "General"),
        ("Minutes played", "Minutos jugados", "General"),
        ("Successful defensive actions per 90", "Acciones defensivas exitosas por 90 minutos", "Defensa"),
        ("Aerial duels won, %", "Duelos aéreos ganados, %", "Defensa"),
        ("Defensive duels won, %", "Duelos defensivos ganados, %", "Defensa"),
        ("Defensive duels per 90", "Duelos defensivos por 90 minutos", "Defensa"),
        ("Duels won, %", "Duelos ganados, %", "Defensa"),
        ("Interceptions per 90", "Intercepciones por 90 minutos", "Defensa"),
        ("Passes per 90", "Pases por 90 minutos", "Pases"),
        ("Forward passes per 90", "Pases hacia adelante por 90 minutos", "Pases"),
        ("Accurate passes to penalty area, %", "Pases precisos al área penal, %", "Pases"),
        ("Received passes per 90", "Pases recibidos por 90 minutos", "Pases"),
        ("Accurate passes to final third, %", "Pases precisos al tercio final, %", "Pases"),
        ("Accurate through passes, %", "Pases filtrados precisos, %", "Pases"),
        ("Accurate forward passes, %", "Pases precisos hacia adelante, %", "Pases"),
        ("Accurate progressive passes, %", "Pases progresivos precisos, %", "Pases"),
        ("xA per 90", "xA por 90 minutos", "Pases"),
        ("Successful attacking actions per 90", "Acciones ofensivas exitosas por 90 minutos", "Ataque"),
        ("Accelerations per 90", "Aceleraciones por 90 minutos", "Ataque"),
        ("Progressive runs per 90", "Carreras progresivas por 90 minutos", "Ataque"),
        ("Crosses to goalie box per 90", "Centros al área por 90 minutos", "Ataque"),
        ("Third assists per 90", "Terceras asistencias por 90 minutos", "Ataque")
    ],
    'Lateral Derecho': [
        ("Matches played", "Partidos jugados", "General"),
        ("Minutes played", "Minutos jugados", "General"),
        ("Successful defensive actions per 90", "Acciones defensivas exitosas por 90 minutos", "Defensa"),
        ("Aerial duels won, %", "Duelos aéreos ganados, %", "Defensa"),
        ("Defensive duels won, %", "Duelos defensivos ganados, %", "Defensa"),
        ("Defensive duels per 90", "Duelos defensivos por 90 minutos", "Defensa"),
        ("Duels won, %", "Duelos ganados, %", "Defensa"),
        ("Interceptions per 90", "Intercepciones por 90 minutos", "Defensa"),
        ("Passes per 90", "Pases por 90 minutos", "Pases"),
        ("Forward passes per 90", "Pases hacia adelante por 90 minutos", "Pases"),
        ("Accurate passes to penalty area, %", "Pases precisos al área penal, %", "Pases"),
        ("Received passes per 90", "Pases recibidos por 90 minutos", "Pases"),
        ("Accurate passes to final third, %", "Pases precisos al tercio final, %", "Pases"),
        ("Accurate through passes, %", "Pases filtrados precisos, %", "Pases"),
        ("Accurate forward passes, %", "Pases precisos hacia adelante, %", "Pases"),
        ("Accurate progressive passes, %", "Pases progresivos precisos, %", "Pases"),
        ("xA per 90", "xA por 90 minutos", "Pases"),
        ("Successful attacking actions per 90", "Acciones ofensivas exitosas por 90 minutos", "Ataque"),
        ("Accelerations per 90", "Aceleraciones por 90 minutos", "Ataque"),
        ("Progressive runs per 90", "Carreras progresivas por 90 minutos", "Ataque"),
        ("Crosses to goalie box per 90", "Centros al área por 90 minutos", "Ataque"),
        ("Third assists per 90", "Terceras asistencias por 90 minutos", "Ataque")
    ],
    'Mediocampista Defensivo': [
        ("Matches played", "Partidos jugados", "General"),
        ("Minutes played", "Minutos jugados", "General"),
        ("Aerial duels won, %", "Duelos aéreos ganados, %", "Defensa"),
        ("Defensive duels won, %", "Duelos defensivos ganados, %", "Defensa"),
        ("Interceptions per 90", "Intercepciones por 90 minutos", "Defensa"),
        ("Received passes per 90", "Pases recibidos por 90 minutos", "Pases"),
        ("Accurate short / medium passes, %", "Pases cortos/medios precisos, %", "Pases"),
        ("Accurate passes to final third, %", "Pases precisos al tercio final, %", "Pases"),
        ("Accurate long passes, %", "Pases largos precisos, %", "Pases"),
        ("Accurate progressive passes, %", "Pases progresivos precisos, %", "Pases"),
        ("Assists per 90", "Asistencias por 90 minutos", "Pases"),
        ("xA per 90", "xA por 90 minutos", "Pases"),
        ("Successful dribbles, %", "Regates exitosos, %", "Ataque"),
        ("xG per 90", "xG por 90 minutos", "Ataque"),
        ("Goals per 90", "Goles por 90 minutos", "Ataque"),
        ("Offensive duels won, %", "Duelos ofensivos ganados, %", "Ataque")
    ],
    'Mediocampista Central': [
        ("Matches played", "Partidos jugados", "General"),
        ("Minutes played", "Minutos jugados", "General"),
        ("Aerial duels won, %", "Duelos aéreos ganados, %", "Defensa"),
        ("Defensive duels won, %", "Duelos defensivos ganados, %", "Defensa"),
        ("Interceptions per 90", "Intercepciones por 90 minutos", "Defensa"),
        ("Received passes per 90", "Pases recibidos por 90 minutos", "Pases"),
        ("Accurate short / medium passes, %", "Pases cortos/medios precisos, %", "Pases"),
        ("Accurate passes to final third, %", "Pases precisos al tercio final, %", "Pases"),
        ("Accurate long passes, %", "Pases largos precisos, %", "Pases"),
        ("Accurate progressive passes, %", "Pases progresivos precisos, %", "Pases"),
        ("Assists per 90", "Asistencias por 90 minutos", "Pases"),
        ("xA per 90", "xA por 90 minutos", "Pases"),
        ("Successful dribbles, %", "Regates exitosos, %", "Ataque"),
        ("xG per 90", "xG por 90 minutos", "Ataque"),
        ("Goals per 90", "Goles por 90 minutos", "Ataque"),
        ("Offensive duels won, %", "Duelos ofensivos ganados, %", "Ataque")
    ],
    'Mediocampista Ofensivo': [
        ("Matches played", "Partidos jugados", "General"),
        ("Minutes played", "Minutos jugados", "General"),
        ("Aerial duels won, %", "Duelos aéreos ganados, %", "Defensa"),
        ("Defensive duels won, %", "Duelos defensivos ganados, %", "Defensa"),
        ("Interceptions per 90", "Intercepciones por 90 minutos", "Defensa"),
        ("Received passes per 90", "Pases recibidos por 90 minutos", "Pases"),
        ("Accurate short / medium passes, %", "Pases cortos/medios precisos, %", "Pases"),
        ("Accurate passes to final third, %", "Pases precisos al tercio final, %", "Pases"),
        ("Accurate long passes, %", "Pases largos precisos, %", "Pases"),
        ("Accurate progressive passes, %", "Pases progresivos precisos, %", "Pases"),
        ("Assists per 90", "Asistencias por 90 minutos", "Pases"),
        ("xA per 90", "xA por 90 minutos", "Pases"),
        ("Successful dribbles, %", "Regates exitosos, %", "Ataque"),
        ("xG per 90", "xG por 90 minutos", "Ataque"),
        ("Goals per 90", "Goles por 90 minutos", "Ataque"),
        ("Offensive duels won, %", "Duelos ofensivos ganados, %", "Ataque")
    ],
    'Extremos': [
        ("Matches played", "Partidos jugados", "General"),
        ("Minutes played", "Minutos jugados", "General"),
        ("Defensive duels won, %", "Duelos defensivos ganados, %", "Defensa"),
        ("Interceptions per 90", "Intercepciones por 90 minutos", "Defensa"),
        ("xA per 90", "xA por 90 minutos", "Pases"),
        ("Assists per 90", "Asistencias por 90 minutos", "Pases"),
        ("Received passes per 90", "Pases recibidos por 90 minutos", "Pases"),
        ("Accurate crosses, %", "Centros precisos, %", "Pases"),
        ("Accurate through passes, %", "Pases filtrados precisos, %", "Pases"),
        ("Accurate progressive passes, %", "Pases progresivos precisos, %", "Pases"),
        ("Accurate passes to penalty area, %", "Pases precisos al área penal, %", "Pases"),
        ("Goals per 90", "Goles por 90 minutos", "Ataque"),
        ("xG per 90", "xG por 90 minutos", "Ataque"),
        ("Successful dribbles, %", "Regates exitosos, %", "Ataque"),
        ("Offensive duels won, %", "Duelos ofensivos ganados, %", "Ataque"),
        ("Crosses to goalie box per 90", "Centros al área por 90 minutos", "Ataque")
    ],
    'Delantero': [
        ("Matches played", "Partidos jugados", "General"),
        ("Minutes played", "Minutos jugados", "General"),
        ("Aerial duels won, %", "Duelos aéreos ganados, %", "Defensa"),
        ("Duels won, %", "Duelos ganados, %", "Defensa"),
        ("Passes per 90", "Pases por 90 minutos", "Pases"),
        ("Accurate passes, %", "Pases precisos, %", "Pases"),
        ("Key passes per 90", "Pases clave por 90 minutos", "Pases"),
        ("xA per 90", "xA por 90 minutos", "Pases"),
        ("Assists per 90", "Asistencias por 90 minutos", "Pases"),
        ("Goals per 90", "Goles por 90 minutos", "Ataque"),
        ("Non-penalty goals per 90", "Goles sin penales por 90 minutos", "Ataque"),
        ("Head goals per 90", "Goles de cabeza por 90 minutos", "Ataque"),
        ("Goal conversion, %", "Conversión de goles, %", "Ataque"),
        ("Shots per 90", "Disparos por 90 minutos", "Ataque"),
        ("Shots on target, %", "Disparos a puerta, %", "Ataque"),
        ("Touches in box per 90", "Toques en el área por 90 minutos", "Ataque"),
        ("xG per 90", "xG por 90 minutos", "Ataque")
    ]
}

# Configuración básica de la página
st.set_page_config(
    page_title="Deportivo Garcilaso ⚽️",
    layout="wide",
    page_icon="⚽🐈‍⬛🇵🇪📊",
    initial_sidebar_state="expanded"
)

# URLs base y archivos por temporada
BASE_URLS = {
    "2020": "https://raw.githubusercontent.com/CarlosCO94/Scout_911/main/data/2020",
    "20-21": "https://raw.githubusercontent.com/CarlosCO94/Scout_911/main/data/20-21",
    "2021": "https://raw.githubusercontent.com/CarlosCO94/Scout_911/main/data/2021",
    "21-22": "https://raw.githubusercontent.com/CarlosCO94/Scout_911/main/data/21-22",
    "2022": "https://raw.githubusercontent.com/CarlosCO94/Scout_911/main/data/2022",
    "22-23": "https://raw.githubusercontent.com/CarlosCO94/Scout_911/main/data/22-23",
    "2023": "https://raw.githubusercontent.com/CarlosCO94/Scout_911/main/data/2023",
    "23-24": "https://raw.githubusercontent.com/CarlosCO94/Scout_911/main/data/23-24",
    "2024": "https://raw.githubusercontent.com/CarlosCO94/Scout_911/main/data/2024",
    "24-25": "https://raw.githubusercontent.com/CarlosCO94/Scout_911/main/data/24-25"
}

FILE_NAMES = {
    "2024": [
        "Argentina Copa de la Liga 2024.parquet",
        "Argentina Primera Nacional 2024.parquet",
        "Bolivian LFPB 2024.parquet",
        "Brasileirao 2024.parquet",
        "Brazil Serie B 2024.parquet",
        "Brazil Serie C 2024.parquet",
        "Canadian Premier League 2024.parquet",
        "Chilean Primera B 2024.parquet",
        "Chilean Primera Division 2024.parquet",
        "Colombian Primera A 2024.parquet",
        "Colombian Torneo BetPlay 2024.parquet",
        "Ecuador Liga Pro 2024.parquet",
        "J1 2024.parquet",
        "K League 1 2024.parquet",
        "MLS 2024.parquet",
        "MLS Next Pro 2024.parquet",
        "Panama LPF 2024.parquet",
        "Paraguay Division Profesional 2024.parquet",
        "Peruvian Liga 1 2024.parquet",
        "USL Championship 2024.parquet",
        "USL League 1 2024.parquet",
        "Uruguay Primera Division 2024.parquet",
    ],
    "2023": [
        "Argentina LPF 2023.parquet",
        "Argentina Primera Nacional 2023.parquet",
        "Argentina Reserve League 2023.parquet",
        "Bolivian LFPB 2023.parquet",
        "Brasileirao 2023.parquet",
        "Brazil Serie B 2023.parquet",
        "Brazil Serie C 2023.parquet",
        "Canadian Premier League 2023.parquet",
        "Chilean Primera B 2023.parquet",
        "Chilean Primera Division 2023.parquet",
        "Colombian Primera A 2023.parquet",
        "Colombian Torneo BetPlay 2023.parquet",
        "Ecuador Liga Pro 2023.parquet",
        "J1 2023.parquet",
        "K League 1 2023.parquet",
        "MLS 2023.parquet",
        "MLS Next Pro 2023.parquet",
        "Panama LPF 2023.parquet",
        "Paraguay Division Profesional 2023.parquet",
        "Peruvian Liga 1 2023.parquet",
        "USL Championship 2023.parquet",
        "USL League 1 2023.parquet",
        "Uruguay Primera Division 2023.parquet",
    ],
    "2022": [
        "Bolivian LFPB 2022.parquet",
        "Brasileirao 2022.parquet",
        "Brazil Serie B 2022.parquet",
        "Brazil Serie C 2022.parquet",
        "Canadian Premier League 2022.parquet",
        "Chilean Primera B 2022.parquet",
        "Chilean Primera Division 2022.parquet",
        "Colombian Primera A 2022.parquet",
        "Colombian Torneo BetPlay 2022.parquet",
        "Ecuador Liga Pro 2022.parquet",
        "J1 2022.parquet",
        "K League 1 2022.parquet",
        "MLS 2022.parquet",
        "Panama LPF 2022.parquet",
        "Paraguay Division Profesional 2022.parquet",
        "Peruvian Liga 1 2022.parquet",
        "USL Championship 2022.parquet",
        "USL League 1 2022.parquet",
        "Uruguay Primera Division 2022.parquet",
    ],
    "2021": [
        "Bolivian LFPB 2021.parquet",
        "Brasileirao 2021.parquet",
        "Brazil Serie B 2021.parquet",
        "Brazil Serie C 2021.parquet",
        "Chilean Primera B 2021.parquet",
        "Chilean Primera Division 2021.parquet",
        "Colombian Primera A 2021.parquet",
        "Colombian Torneo BetPlay 2021.parquet",
        "Ecuador Liga Pro 2021.parquet",
        "J1 2021.parquet",
        "K League 1 2021.parquet",
        "MLS 2021.parquet",
        "Panama LPF 2021.parquet",
        "Paraguay Division Profesional 2021.parquet",
        "Peruvian Liga 1 2021.parquet",
        "USL Championship 2021.parquet",
        "Uruguay Primera Division 2021.parquet",
    ],
    "2020": [
        "Bolivian LFPB 2020.parquet",
        "Brasileirao 2020.parquet",
        "Brazil Serie B 2020.parquet",
        "Brazil Serie C 2020.parquet",
        "Canadian Premier League 2020.parquet",
        "Chilean Primera B 2020.parquet",
        "Chilean Primera Division 2020.parquet",
        "Colombian Primera A 2020.parquet",
        "Colombian Torneo BetPlay 2020.parquet",
        "Ecuador Liga Pro 2020.parquet",
        "J1 2020.parquet",
        "K League 1 2020.parquet",
        "MLS 2020.parquet",
        "Panama LPF 2020.parquet",
        "Paraguay Division Profesional 2020.parquet",
        "Peruvian Liga 1 2020.parquet",
        "USL Championship 2020.parquet",
        "Uruguay Primera Division 2020.parquet",
    ],
    "20-21": [
        "Belgian Pro League 20-21.parquet",
        "Bundesliga 20-21.parquet",
        "Campeonato de Portugal 20-21.parquet",
        "Championship 20-21.parquet",
        "Costa Rican Primera Division 20-21.parquet",
        "El Salvador Primera Division 20-21.parquet",
        "English National League 20-21.parquet",
        "Eredivisie 20-21.parquet",
        "French National 1 20-21.parquet",
        "Greek Super League 20-21.parquet",
        "Guatemalan Liga Nacional 20-21.parquet",
        "Honduran Liga Nacional 20-21.parquet",
        "La Liga 2 20-21.parquet",
        "La Liga 20-21.parquet",
        "League One 20-21.parquet",
        "League Two 20-21.parquet",
        "Liga MX 20-21.parquet",
        "Liga de Expansion MX 20-21.parquet",
        "Ligue 1 20-21.parquet",
        "Ligue 2 20-21.parquet",
        "Nicaragua Primera Division 20-21.parquet",
        "Portuguese Segunda Liga 20-21.parquet",
        "Premier League 20-21.parquet",
        "Primavera 1 20-21.parquet",
        "Primeira Liga 20-21.parquet",
        "Russian First League 20-21.parquet",
        "Russian Premier League 20-21.parquet",
        "Saudi Pro League 20-21.parquet",
        "Scottish Championship 20-21.parquet",
        "Serie A 20-21.parquet",
        "Serie B 20-21.parquet",
        "Serie C 20-21.parquet",
        "Super Lig 20-21.parquet",
        "Superliga 20-21.parquet",
        "Swiss Challenge League 20-21.parquet",
        "Swiss Super League 20-21.parquet",
        "UAE Pro League 20-21.parquet",
    ],
    "21-22": [
        "Belgian Pro League 21-22.parquet",
        "Bundesliga 21-22.parquet",
        "Campeonato de Portugal 21-22.parquet",
        "Championship 21-22.parquet",
        "Costa Rican Primera Division 21-22.parquet",
        "El Salvador Primera Division 21-22.parquet",
        "English National League 21-22.parquet",
        "Eredivisie 21-22.parquet",
        "French National 1 21-22.parquet",
        "Greek Super League 21-22.parquet",
        "Guatemalan Liga Nacional 21-22.parquet",
        "Honduran Liga Nacional 21-22.parquet",
        "La Liga 2 21-22.parquet",
        "La Liga 21-22.parquet",
        "League One 21-22.parquet",
        "League Two 21-22.parquet",
        "Liga MX 21-22.parquet",
        "Liga de Expansion MX 21-22.parquet",
        "Ligue 1 21-22.parquet",
        "Ligue 2 21-22.parquet",
        "Nicaragua Primera Division 21-22.parquet",
        "Portuguese Segunda Liga 21-22.parquet",
        "Premier League 21-22.parquet",
        "Primavera 1 21-22.parquet",
        "Primeira Liga 21-22.parquet",
        "Russian First League 21-22.parquet",
        "Russian Premier League 21-22.parquet",
        "Saudi Pro League 21-22.parquet",
        "Scottish Championship 21-22.parquet",
        "Serie A 21-22.parquet",
        "Serie B 21-22.parquet",
        "Serie C 21-22.parquet",
        "Super Lig 21-22.parquet",
        "Superliga 21-22.parquet",
        "Swiss Challenge League 21-22.parquet",
        "Swiss Super League 21-22.parquet",
        "UAE Pro League 21-22.parquet",
    ],
    "22-23": [
        "Belgian Pro League 22-23.parquet",
        "Bundesliga 22-23.parquet",
        "Campeonato de Portugal 22-23.parquet",
        "Championship 22-23.parquet",
        "Costa Rican Primera Division 22-23.parquet",
        "El Salvador Primera Division 22-23.parquet",
        "English National League 22-23.parquet",
        "Eredivisie 22-23.parquet",
        "French National 1 22-23.parquet",
        "Greek Super League 22-23.parquet",
        "Guatemalan Liga Nacional 22-23.parquet",
        "Honduran Liga Nacional 22-23.parquet",
        "La Liga 2 22-23.parquet",
        "La Liga 22-23.parquet",
        "League One 22-23.parquet",
        "League Two 22-23.parquet",
        "Liga MX 22-23.parquet",
        "Liga de Expansion MX 22-23.parquet",
        "Ligue 1 22-23.parquet",
        "Ligue 2 22-23.parquet",
        "Nicaragua Primera Division 22-23.parquet",
        "Portuguese Segunda Liga 22-23.parquet",
        "Premier League 22-23.parquet",
        "Primavera 1 22-23.parquet",
        "Primeira Liga 22-23.parquet",
        "Russian First League 22-23.parquet",
        "Russian Premier League 22-23.parquet",
        "Saudi Pro League 22-23.parquet",
        "Scottish Championship 22-23.parquet",
        "Serie A 22-23.parquet",
        "Serie B 22-23.parquet",
        "Serie C 22-23.parquet",
        "Super Lig 22-23.parquet",
        "Superliga 22-23.parquet",
        "Swiss Challenge League 22-23.parquet",
        "Swiss Super League 22-23.parquet",
        "UAE Pro League 22-23.parquet",
    ],
    "23-24": [
        "Belgian Pro League 23-24.parquet",
        "Bundesliga 23-24.parquet",
        "Campeonato de Portugal 23-24.parquet",
        "Championship 23-24.parquet",
        "Costa Rican Primera Division 23-24.parquet",
        "El Salvador Primera Division 23-24.parquet",
        "English National League 23-24.parquet",
        "Eredivisie 23-24.parquet",
        "French National 1 23-24.parquet",
        "Greek Super League 23-24.parquet",
        "Guatemalan Liga Nacional 23-24.parquet",
        "Honduran Liga Nacional 23-24.parquet",
        "La Liga 2 23-24.parquet",
        "La Liga 23-24.parquet",
        "League One 23-24.parquet",
        "League Two 23-24.parquet",
        "Liga MX 23-24.parquet",
        "Liga de Expansion MX 23-24.parquet",
        "Ligue 1 23-24.parquet",
        "Ligue 2 23-24.parquet",
        "Nicaragua Primera Division 23-24.parquet",
        "Portuguese Segunda Liga 23-24.parquet",
        "Premier League 23-24.parquet",
        "Primavera 1 23-24.parquet",
        "Primeira Liga 23-24.parquet",
        "Russian First League 23-24.parquet",
        "Russian Premier League 23-24.parquet",
        "Saudi Pro League 23-24.parquet",
        "Scottish Championship 23-24.parquet",
        "Serie A 23-24.parquet",
        "Serie B 23-24.parquet",
        "Serie C 23-24.parquet",
        "Super Lig 23-24.parquet",
        "Superliga 23-24.parquet",
        "Swiss Challenge League 23-24.parquet",
        "Swiss Super League 23-24.parquet",
        "UAE Pro League 23-24.parquet",
    ],
    "24-25": [
        "Belgian Pro League 24-25.parquet",
        "Bundesliga 24-25.parquet",
        "Championship 24-25.parquet",
        "Costa Rican Primera Division 24-25.parquet",
        "El Salvador Primera Division 24-25.parquet",
        "English National League 24-25.parquet",
        "Eredivisie 24-25.parquet",
        "French National 1 24-25.parquet",
        "Greek Super League 24-25.parquet",
        "Guatemalan Liga Nacional 24-25.parquet",
        "Honduran Liga Nacional 24-25.parquet",
        "La Liga 2 24-25.parquet",
        "La Liga 24-25.parquet",
        "League One 24-25.parquet",
        "League Two 24-25.parquet",
        "Liga MX 24-25.parquet",
        "Liga de Expansion MX 24-25.parquet",
        "Ligue 1 24-25.parquet",
        "Ligue 2 24-25.parquet",
        "Nicaragua Primera Division 24-25.parquet",
        "Portuguese Segunda Liga 24-25.parquet",
        "Premier League 24-25.parquet",
        "Primavera 1 24-25.parquet",
        "Primeira Liga 24-25.parquet",
        "Russian Premier League 24-25.parquet",
        "Saudi Pro League 24-25.parquet",
        "Scottish Championship 24-25.parquet",
        "Serie A 24-25.parquet",
        "Serie B 24-25.parquet",
        "Serie C 24-25.parquet",
        "Super Lig 24-25.parquet",
        "Superliga 24-25.parquet",
        "Swiss Challenge League 24-25.parquet",
        "Swiss Super League 24-25.parquet",
        "UAE Pro League 24-25.parquet",
    ],    
}

# Columnas necesarias para la aplicación
COLUMNS_TO_LOAD = [
    "Full name",
    "Team within selected timeframe",
    "Passport country",
    "Foot",
    "Age",
    "Minutes played",
    "Primary position",
    "Contract expires",
]

@st.cache_data
def load_parquet_data(file_url, season, competition):
    """
    Carga un archivo Parquet desde una URL y añade columnas de temporada y competición.
    """
    try:
        response = requests.get(file_url)
        if response.status_code == 200:
            file_bytes = BytesIO(response.content)
            data = pd.read_parquet(file_bytes)  # Cargar todas las columnas
            # Agregar columnas adicionales
            data["Season"] = season
            data["Competition"] = competition
            return data
        else:
            st.error(f"Error al descargar {file_url}: {response.status_code}")
            return None
    except Exception as e:
        st.error(f"Error al procesar {file_url}: {e}")
        return None

# Función para cargar múltiples archivos en paralelo
@st.cache_data
def load_files_in_parallel(file_urls, columns=None):
    """
    Carga múltiples archivos Parquet en paralelo.
    """
    with ThreadPoolExecutor() as executor:
        results = list(executor.map(lambda url: load_parquet_data(url, columns), file_urls))
    return [df for df in results if df is not None]

################################################### PAGINA CENTRAL ###############################################

def main_page():
    st.title("Deportivo Garcilaso ⚽️")
    st.write("Análisis de datos Propio | Rival | Scouting.")

    # Selección de temporadas
    available_seasons = list(BASE_URLS.keys())
    selected_seasons = st.multiselect(
        "Selecciona temporadas:", available_seasons, default=available_seasons, key="season_selector"
    )

    # Filtrar archivos por temporada seleccionada
    all_files = [
        (season, f"{BASE_URLS[season]}/{file}".replace(" ", "%20"), file.split(".")[0])
        for season in selected_seasons
        for file in FILE_NAMES[season]
    ]
    selected_files = st.multiselect(
        "Selecciona ligas:",
        ["Todas"] + [f"{season} - {file}" for season, _, file in all_files],
        default="Todas",
        key="league_selector",
    )

    if "Todas" in selected_files:
        files_to_load = all_files
    else:
        files_to_load = [
            (season, file_url, competition)
            for season, file_url, competition in all_files
            if f"{season} - {competition}" in selected_files
        ]

    # Botón para cargar datos
    if st.button("Cargar Datos", key="load_data_button"):
        # Barra de progreso
        progress_bar = st.progress(0)
        progress_step = 1 / len(files_to_load) if len(files_to_load) > 0 else 1

        # Cargar archivos
        dataframes = []
        for i, (season, file_url, competition) in enumerate(files_to_load):
            df = load_parquet_data(file_url, season=season, competition=competition)  # Sin `columns`
            if df is not None:
                dataframes.append(df)
            progress_bar.progress((i + 1) * progress_step)

        # Concatenar datos
        if dataframes:
            full_data = pd.concat(dataframes, ignore_index=True)
            st.session_state["filtered_data"] = full_data
            st.success(f"Se cargaron {len(dataframes)} archivos correctamente.")
            st.dataframe(full_data.head(), use_container_width=True)
        else:
            st.warning("No se pudo cargar ningún archivo. Verifica la conexión o los filtros seleccionados.")


################################################## BUSCAR ##################################################
############################################################################################################

import streamlit as st

def search_page():
    st.title("BUSCAR JUGADORES EN TODO EL MUNDO ⚽️")

    if "filtered_data" in st.session_state:
        data = st.session_state["filtered_data"]

        # Barra lateral para filtros
        st.sidebar.header("Filtros de Búsqueda")

        # Filtro de temporada
        selected_seasons = st.sidebar.multiselect(
            "Selecciona las temporadas:",
            options=sorted(data["Season"].dropna().unique().tolist()),
            default=sorted(data["Season"].dropna().unique().tolist()),
            key="season_filter"
        )

        # Filtrar datos según las temporadas seleccionadas
        filtered_data = data[data["Season"].isin(selected_seasons)]

        # Filtro de competición
        available_competitions = sorted(filtered_data["Competition"].dropna().unique().tolist())
        selected_competitions = st.sidebar.multiselect(
            "Selecciona las competiciones:",
            options=["Todos"] + available_competitions,
            default="Todos",
            key="competition_filter"
        )

        # Filtrar datos según las competiciones seleccionadas
        if "Todos" not in selected_competitions:
            filtered_data = filtered_data[filtered_data["Competition"].isin(selected_competitions)]

        # Filtro de equipo
        available_teams = sorted(filtered_data["Team within selected timeframe"].dropna().unique().tolist())
        selected_teams = st.sidebar.multiselect(
            "Selecciona los equipos:",
            options=["Todos"] + available_teams,
            default="Todos",
            key="team_filter"
        )

        # Filtrar datos según los equipos seleccionados
        if "Todos" not in selected_teams:
            filtered_data = filtered_data[filtered_data["Team within selected timeframe"].isin(selected_teams)]

        # Filtro de rango de edad
        min_age, max_age = filtered_data["Age"].min(), filtered_data["Age"].max()
        age_range = st.sidebar.slider(
            "Rango de edades:",
            int(min_age), int(max_age), (int(min_age), int(max_age)),
            key="age_filter"
        )

        # Filtrar datos según el rango de edad seleccionado
        filtered_data = filtered_data[
            (filtered_data["Age"] >= age_range[0]) &
            (filtered_data["Age"] <= age_range[1])
        ]

        # Filtros adicionales en la barra lateral
        st.sidebar.header("Filtros Adicionales")

        # Filtro de minutos jugados
        min_minutes, max_minutes = filtered_data["Minutes played"].min(), filtered_data["Minutes played"].max()
        minutes_range = st.sidebar.slider(
            "Rango de minutos jugados:",
            int(min_minutes), int(max_minutes), (int(min_minutes), int(max_minutes)),
            key="minutes_filter"
        )

        # Filtro de pierna dominante
        available_feet = sorted(filtered_data["Foot"].dropna().unique().tolist())
        selected_feet = st.sidebar.multiselect(
            "Pierna dominante:",
            options=["Todos"] + available_feet,
            default="Todos",
            key="foot_filter"
        )

        # Aplicar filtros finales
        filtered_data = filtered_data[
            (filtered_data["Minutes played"] >= minutes_range[0]) &
            (filtered_data["Minutes played"] <= minutes_range[1])
        ]
        if "Todos" not in selected_feet:
            filtered_data = filtered_data[filtered_data["Foot"].isin(selected_feet)]

        # Mostrar resultados
        if not filtered_data.empty:
            columns_to_display = [
                "Full name", "Team within selected timeframe", "Age", "Foot",
                "Passport country", "Minutes played", "Season", "Competition"
            ]
            # Asegúrate de ajustar el número de filas que quieres mostrar. Puedes también controlar el tamaño de la tabla.
            st.dataframe(filtered_data[columns_to_display], use_container_width=True, height=700)  # Ajusta el valor de 'height' según lo necesites
        else:
            st.warning("No se encontraron jugadores que coincidan con los filtros seleccionados.")
    else:
        st.warning("Primero debes cargar los datos en la pestaña principal.")


###################################### COMPARACIÓN ##########################################

def comparison_page():
    st.write("COMPARACIÓN DE JUGADORES ENTRE VARIAS TEMPORADAS ⚽️")

    if "filtered_data" not in st.session_state or st.session_state["filtered_data"].empty:
        st.warning("Primero debes cargar los datos en la pestaña principal.")
        return

    # Obtener los datos preprocesados
    data = st.session_state["filtered_data"].copy()

    # Crear una columna única `Player Instance` para diferenciar por temporada y equipo
    data["Player Instance"] = (
        data["Full name"] + " | " +
        data["Team within selected timeframe"].fillna("Sin equipo") + " | " +
        data["Season"].astype(str)
    )

    # Selección múltiple de jugadores por instancia
    selected_instances = st.multiselect(
        "Selecciona jugadores para comparar:",
        options=sorted(data["Player Instance"].unique()),
        format_func=lambda instance: instance
    )

    if not selected_instances:
        st.warning("Por favor, selecciona al menos un jugador para comparar.")
        return

    # Filtrar los datos de las instancias seleccionadas
    players_to_compare = data[data["Player Instance"].isin(selected_instances)]

    # Filtro por posición para elegir métricas específicas
    selected_position = st.selectbox(
        "Selecciona la posición de los jugadores:",
        options=list(metrics_by_position.keys())
    )

    # Filtrar las métricas específicas para la posición seleccionada
    metrics = metrics_by_position[selected_position]
    available_metrics = [metric[0] for metric in metrics if metric[0] in players_to_compare.columns]
    metric_labels = {metric[0]: metric[1] for metric in metrics if metric[0] in players_to_compare.columns}

    # Mostrar métricas faltantes para depuración
    missing_metrics = [metric[0] for metric in metrics if metric[0] not in players_to_compare.columns]
    if missing_metrics:
        st.warning(f"Métricas faltantes para esta posición: {', '.join(missing_metrics)}")

    if not available_metrics:
        st.warning("No hay métricas disponibles para la posición seleccionada.")
        return

    # Filtrar y organizar los datos para comparación
    comparison_data = players_to_compare[["Player Instance"] + available_metrics].set_index("Player Instance")
    if comparison_data.empty:
        st.warning("No se encontraron datos para las métricas seleccionadas.")
        return

    # Renombrar columnas con etiquetas en español
    comparison_data.rename(columns=metric_labels, inplace=True)

    # Transponer la tabla para colocar métricas como filas
    comparison_data = comparison_data.T

    # Redondear valores a dos decimales
    comparison_data = comparison_data.round(2)

    # Resaltar el valor más alto en cada fila
    def highlight_max(s):
        """
        Resalta el valor más alto en una serie.
        """
        is_max = s == s.max()
        return ['background-color: lightgreen' if v else '' for v in is_max]

    # Aplicar estilo al DataFrame
    styled_comparison_data = comparison_data.style.apply(highlight_max, axis=1).format("{:.2f}")

    # Mostrar tabla en Streamlit
    st.write("### Comparación de métricas:")
    st.dataframe(styled_comparison_data, use_container_width=True)


###################################### SIMILITUD ##########################################
###########################################################################################


def similarity_page():
    st.write("SIMILITUD DE JUGADORES (COSENO | EUCLIDIANA) ⚽️")

    if "filtered_data" in st.session_state and not st.session_state["filtered_data"].empty:
        data = st.session_state["filtered_data"]

        # Barra lateral para filtros
        st.sidebar.header("Filtros de Búsqueda")

        # Filtro de jugador de referencia
        player_to_compare = st.sidebar.selectbox(
            "Jugador de referencia:",
            options=sorted(data["Full name"].dropna().unique().tolist())
        )

        # Filtro de posición
        selected_position = st.sidebar.selectbox(
            "Posición:",
            options=["Todos"] + list(metrics_by_position.keys())
        )

        # Filtro de temporadas
        selected_seasons = st.sidebar.multiselect(
            "Temporadas:",
            options=sorted(data["Season"].dropna().unique().tolist()),
            default=sorted(data["Season"].dropna().unique().tolist())
        )

        # Filtro de competencias
        selected_competitions = st.sidebar.multiselect(
            "Competencias:",
            options=["Todos"] + sorted(data["Competition"].dropna().unique().tolist()),
            default="Todos"
        )

        # Filtro de país de pasaporte
        passport_country = st.sidebar.text_input("País de pasaporte (parcial o completo):", value="")

        # Filtros adicionales en la barra lateral
        min_age, max_age = int(data["Age"].min()), int(data["Age"].max())
        age_range = st.sidebar.slider("Rango de edades:", min_age, max_age, (min_age, max_age))

        min_minutes, max_minutes = int(data["Minutes played"].min()), int(data["Minutes played"].max())
        minutes_range = st.sidebar.slider("Rango de minutos jugados:", min_minutes, max_minutes, (min_minutes, max_minutes))

        dominant_foot = st.sidebar.multiselect(
            "Pierna dominante:",
            options=["Todos"] + sorted(data["Foot"].dropna().unique().tolist()),
            default="Todos"
        )

        # Filtrar datos
        filtered_data = data.copy()

        # Filtro por temporadas
        filtered_data = filtered_data[filtered_data["Season"].isin(selected_seasons)]

        # Filtro por competencias
        if "Todos" not in selected_competitions:
            filtered_data = filtered_data[filtered_data["Competition"].isin(selected_competitions)]

        # Filtro por posición
        if selected_position != "Todos":
            position_patterns = {
                "Portero": "GK", "Defensa": "CB",
                "Lateral Izquierdo": "LB|LWB", "Lateral Derecho": "RB|RWB",
                "Mediocampista Defensivo": "DMF", "Mediocampista Central": "CMF",
                "Mediocampista Ofensivo": "AMF", "Extremos": "RW|LW|LWF|RWF",
                "Delantero": "CF"
            }
            pattern = position_patterns[selected_position]
            filtered_data = filtered_data[filtered_data["Primary position"].str.contains(pattern, na=False)]

        # Filtro por país de pasaporte
        if passport_country.strip():
            filtered_data = filtered_data[
                filtered_data["Passport country"].str.contains(passport_country, na=False, case=False)
            ]

        # Filtro por edad
        filtered_data = filtered_data[
            (filtered_data["Age"] >= age_range[0]) & (filtered_data["Age"] <= age_range[1])
        ]

        # Filtro por minutos jugados
        filtered_data = filtered_data[
            (filtered_data["Minutes played"] >= minutes_range[0]) & (filtered_data["Minutes played"] <= minutes_range[1])
        ]

        # Filtro por pierna dominante
        if "Todos" not in dominant_foot:
            filtered_data = filtered_data[filtered_data["Foot"].isin(dominant_foot)]

        # Obtener los datos del jugador seleccionado
        player_data = data[data["Full name"] == player_to_compare]

        if player_data.empty:
            st.warning("No se encontraron datos para el jugador seleccionado.")
            return

        # Selección de temporada y equipo si hay múltiples registros
        if len(player_data) > 1:
            selected_row = st.selectbox(
                "Selecciona el equipo y la temporada:",
                options=player_data.index,
                format_func=lambda idx: f"{player_data.loc[idx, 'Team within selected timeframe']} - {player_data.loc[idx, 'Season']}"
            )
        else:
            selected_row = player_data.index[0]

        # Métricas por posición
        if selected_position != "Todos":
            metrics = metrics_by_position[selected_position]
        else:
            metrics = [metric for position_metrics in metrics_by_position.values() for metric in position_metrics]

        # Filtrar las métricas existentes
        available_metrics = [metric[0] for metric in metrics if metric[0] in filtered_data.columns]
        metric_labels = {metric[0]: metric[1] for metric in metrics if metric[0] in filtered_data.columns}

        # Normalización y cálculo de similitudes
        player_metrics = filtered_data[available_metrics].fillna(0)
        selected_player_metrics = player_data.loc[[selected_row], available_metrics].fillna(0)

        scaler = StandardScaler()
        player_metrics_normalized = scaler.fit_transform(player_metrics)
        selected_player_metrics_normalized = scaler.transform(selected_player_metrics)

        # Calcular similitudes
        cosine_similarities = cosine_similarity(selected_player_metrics_normalized, player_metrics_normalized).flatten()
        euclidean_dists = euclidean_distances(selected_player_metrics_normalized, player_metrics_normalized).flatten()
        max_distance = euclidean_dists.max()
        euclidean_similarities = (1 - (euclidean_dists / max_distance)) * 100

        # Añadir columnas de similitud
        filtered_data["Cosine Similarity"] = cosine_similarities * 100
        filtered_data["Euclidean Similarity"] = euclidean_similarities

        # Excluir al jugador seleccionado de los resultados
        similar_players = filtered_data[filtered_data.index != selected_row]

        # **Similitud Coseno**
        st.write("### Jugadores similares a {}".format(player_to_compare))
        st.write("""
        **Similitud Coseno:** Esta medida evalúa qué tan similares son dos jugadores en base a sus características, 
        como minutos jugados, edad, etc. Calcula el ángulo entre los vectores de características de los jugadores. 
        Mientras más alto es el valor, más similares son los jugadores.
        """)

        # Tabla de similitudes Coseno
        cosine_sorted = similar_players.sort_values(by="Cosine Similarity", ascending=False).head(30)
        cosine_table = cosine_sorted[
            ["Player", "Team within selected timeframe", "Season", "Competition", "Minutes played", "Age", "Passport country", "Cosine Similarity"]
        ]
        cosine_table = cosine_table.style.background_gradient(subset=["Cosine Similarity"], cmap="Greens", low=0, high=1)
        st.dataframe(cosine_table)

        # **Similitud Euclidiana**
        st.write("""
        **Similitud Euclidiana:** Esta medida evalúa la distancia entre dos jugadores en el espacio de características. 
        Mientras menor es la distancia, más similares son los jugadores. A medida que la distancia disminuye, 
        el valor de similitud se acerca a 100%.
        """)

        # Tabla de similitudes Euclidiana
        euclidean_sorted = similar_players.sort_values(by="Euclidean Similarity", ascending=False).head(30)
        euclidean_table = euclidean_sorted[
            ["Player", "Team within selected timeframe", "Season", "Competition", "Minutes played", "Age", "Passport country", "Euclidean Similarity"]
        ]
        euclidean_table = euclidean_table.style.background_gradient(subset=["Euclidean Similarity"], cmap="Blues", low=0, high=1)
        st.dataframe(euclidean_table)

    else:
        st.warning("Primero debes cargar los datos en la pestaña principal.")


###################################### DENSIDAD ###########################################
###########################################################################################

def density_page():
    st.write("DENSIDAD DE JUGADORES EN BASE A MÉTRICAS ⚽️")

    if "filtered_data" in st.session_state:
        data = st.session_state["filtered_data"]

        # Mover los filtros a la barra lateral
        st.sidebar.write("### Filtros de Selección")

        # Filtro de temporada
        available_seasons = ["Todos"] + sorted(data["Season"].dropna().unique().tolist())
        selected_season = st.sidebar.selectbox("Selecciona la temporada:", options=available_seasons, index=0)

        # Filtro de competiciones basadas en la temporada
        filtered_data = data.copy()
        if selected_season != "Todos":
            filtered_data = filtered_data[filtered_data["Season"] == selected_season]

        available_competitions = ["Todos"] + sorted(filtered_data["Competition"].dropna().unique().tolist())
        selected_competition = st.sidebar.selectbox("Selecciona la competición:", options=available_competitions, index=0)

        if selected_competition != "Todos":
            filtered_data = filtered_data[filtered_data["Competition"] == selected_competition]

        # Filtro de equipos basados en la competición
        available_teams = ["Todos"] + sorted(filtered_data["Team within selected timeframe"].dropna().unique().tolist())
        selected_team = st.sidebar.selectbox("Selecciona el equipo:", options=available_teams, index=0)

        if selected_team != "Todos":
            filtered_data = filtered_data[filtered_data["Team within selected timeframe"] == selected_team]

        # Filtro de jugadores basado en el equipo seleccionado
        available_players = sorted(filtered_data["Full name"].dropna().unique().tolist())
        if not available_players:
            st.warning("No hay jugadores disponibles para la selección actual.")
            return

        jugador_objetivo = st.sidebar.selectbox("Selecciona el primer jugador:", available_players, index=0)
        jugador_comparacion = st.sidebar.selectbox("Selecciona el jugador para comparar:", available_players, index=0)

        # Filtro de posición general
        posicion_general = st.sidebar.selectbox("Selecciona la posición general de los jugadores:", list(metrics_by_position.keys()))

        # Obtener métricas basadas en la posición seleccionada
        metricas = metrics_by_position[posicion_general]
        metric_names_english = [metric[0] for metric in metricas]
        metric_names_spanish = [metric[1] for metric in metricas]

        # Verificar si hay datos válidos
        if filtered_data.empty or len(metric_names_english) == 0:
            st.warning("No se encontraron datos válidos para generar gráficos.")
            return

        # Mostrar gráficos de densidad para cada métrica
        st.write("#### Gráficos de Densidad por Métrica")
        for metric_english, metric_spanish in zip(metric_names_english, metric_names_spanish):
            if metric_english not in filtered_data.columns:
                st.warning(f"La métrica '{metric_spanish}' no está disponible en los datos.")
                continue

            st.write(f"**Métrica:** {metric_spanish}")
            fig = generar_grafico_densidad(
                df=filtered_data,
                metric_english=metric_english,
                metric_spanish=metric_spanish,
                jugador_objetivo=jugador_objetivo,
                jugador_comparacion=jugador_comparacion,
                color_jugador_objetivo="#FF5733",
                color_jugador_comparacion="#33C4FF",
                promedio_liga=True
            )
            if fig:
                st.pyplot(fig)
    else:
        st.warning("Primero debes cargar los datos en la pestaña principal.")

def generar_grafico_densidad(df, metric_english, metric_spanish, jugador_objetivo, jugador_comparacion, color_jugador_objetivo, color_jugador_comparacion, promedio_liga=False):
    """
    Genera un gráfico de densidad para una métrica específica.
    """

    # Crear el gráfico
    fig, ax = plt.subplots(figsize=(15, 4))
    sns.kdeplot(data=df, x=metric_english, ax=ax, color="gray", fill=True, alpha=0.3, label="Todos los Jugadores")

    # Líneas para jugadores
    valor_objetivo = df.loc[df["Full name"] == jugador_objetivo, metric_english].values
    valor_comparacion = df.loc[df["Full name"] == jugador_comparacion, metric_english].values

    if len(valor_objetivo) > 0:
        ax.axvline(valor_objetivo[0], color=color_jugador_objetivo, linestyle="--", linewidth=2, label=jugador_objetivo)

    if len(valor_comparacion) > 0:
        ax.axvline(valor_comparacion[0], color=color_jugador_comparacion, linestyle="--", linewidth=2, label=jugador_comparacion)

    # Línea para el promedio de la liga (opcional)
    if promedio_liga:
        valor_promedio_liga = df[metric_english].mean()
        ax.axvline(valor_promedio_liga, color="blue", linestyle="--", linewidth=2, label="Promedio Liga")

    # Configuración del gráfico
    ax.set_title(f"Densidad: {metric_spanish}", fontsize=14)
    ax.set_xlabel(metric_spanish, fontsize=12)
    ax.set_ylabel("Densidad", fontsize=12)
    ax.legend(loc="upper right")

    plt.tight_layout()
    return fig

###################################### DISPERSIÓN ###########################################
#############################################################################################

def create_scatter_plot():
    if 'filtered_data' not in st.session_state:
        return

    df = st.session_state['filtered_data']
    
    # Mover los filtros a la barra lateral
    with st.sidebar:
        seasons = ['Todas'] + list(df['Season'].unique())
        selected_season = st.selectbox('Temporada:', seasons)

    filtered_df = df if selected_season == 'Todas' else df[df['Season'] == selected_season].copy()
    
    with st.sidebar:
        competitions = ['Todas'] + list(filtered_df['Competition'].unique())
        selected_competition = st.selectbox('Competición:', competitions)
    
    if selected_competition != 'Todas':
        filtered_df = filtered_df[filtered_df['Competition'] == selected_competition]
    
    with st.sidebar:
        teams = list(filtered_df['Team within selected timeframe'].unique())
        selected_teams = st.multiselect('Equipos:', teams)
    
    if selected_teams:
        filtered_df = filtered_df[filtered_df['Team within selected timeframe'].isin(selected_teams)]

    with st.sidebar:
        positions = ['Portero', 'Defensa', 'Lateral Izquierdo', 'Lateral Derecho', 
                    'Mediocampista Defensivo', 'Mediocampista Central', 'Mediocampista Ofensivo',
                    'Extremos', 'Delantero']
        selected_positions = st.multiselect('Posiciones:', positions)
    
    with st.sidebar:
        nationalities = ['Todas'] + list(filtered_df['Passport country'].unique())
        selected_nationality = st.selectbox('Nacionalidad:', nationalities)
    
    with st.sidebar:
        feet = ['Todos'] + list(filtered_df['Foot'].unique())
        selected_foot = st.selectbox('Pie:', feet)

    min_minutes = int(filtered_df['Minutes played'].min())
    max_minutes = int(filtered_df['Minutes played'].max())
    
    with st.sidebar:
        selected_minutes = st.slider('Minutos jugados', min_minutes, max_minutes, min_minutes)
    
    filtered_df = filtered_df[filtered_df['Minutes played'] >= selected_minutes]

    if selected_nationality != 'Todas':
        filtered_df = filtered_df[filtered_df['Passport country'] == selected_nationality]
    
    if selected_foot != 'Todos':
        filtered_df = filtered_df[filtered_df['Foot'] == selected_foot]

    position_filters = {
        'Portero': 'GK', 'Defensa': 'CB', 'Lateral Izquierdo': 'LB|LWB',
        'Lateral Derecho': 'RB|RWB', 'Mediocampista Defensivo': 'DMF',
        'Mediocampista Central': 'CMF', 'Mediocampista Ofensivo': 'AMF',
        'Extremos': 'RW|LW|LWF|RWF', 'Delantero': 'CF'
    }
    
    if selected_positions:
        position_pattern = '|'.join([position_filters[pos] for pos in selected_positions])
        filtered_df = filtered_df[filtered_df['Position'].str.contains(position_pattern, na=False)]

    numeric_cols = filtered_df.select_dtypes(include=[np.number]).columns.tolist()

    # Configuración del gráfico
    col7, col8, col9, col10 = st.columns(4)
    with col7:
        x_metric = st.selectbox('Eje X:', numeric_cols)
    with col8:
        y_metric = st.selectbox('Eje Y:', numeric_cols)
    with col9:
        size_metric = st.selectbox('Tamaño:', ['Minutes played'] + numeric_cols)
    with col10:
        color_options = ['Team within selected timeframe'] + numeric_cols
        color_metric = st.selectbox('Color:', color_options)

    if len(filtered_df) == 0:
        st.warning('No hay datos para mostrar con los filtros seleccionados.')
        return

    # Normalizar el tamaño y manejar NaN
    size_values = filtered_df[size_metric]
    size_values = size_values.fillna(size_values.mean())  # Reemplazar NaN con la media
    normalized_size = ((size_values - size_values.min()) / (size_values.max() - size_values.min()) * 30) + 10

    # Crear gráfico con estilo mejorado
    fig = px.scatter(
        filtered_df,
        x=x_metric,
        y=y_metric,
        size=normalized_size,
        color=color_metric,
        text='Full name',
        hover_data=['Full name', 'Team within selected timeframe'],
        title=f'{x_metric} vs {y_metric}',
        height=800,
        color_continuous_scale='Viridis'  # Puedes cambiar la paleta de colores
    )
    
    fig.update_traces(
        marker=dict(
            line=dict(width=2, color='DarkSlateGray'),  # Bordes de los puntos
            opacity=0.8  # Opacidad para un mejor estilo visual
        ),
        textposition='top center',
        textfont=dict(size=12, family='Arial')  # Fuente mejorada
    )
    
    fig.update_layout(
        title_font=dict(size=18, family='Arial, sans-serif', color='rgb(0,0,0)'),
        showlegend=True,
        plot_bgcolor='white',
        legend=dict(yanchor="top", y=0.99, xanchor="left", x=1.02),
        margin=dict(l=50, r=150, t=50, b=50),
        xaxis=dict(showgrid=True, gridcolor='LightGray', zeroline=False),
        yaxis=dict(showgrid=True, gridcolor='LightGray', zeroline=False),
        font=dict(family='Arial, sans-serif', size=14)
    )
    
    st.plotly_chart(fig, use_container_width=True)


###################################### RADAR #############################################################################################################################################


def radar_page():
    st.write("PERCENTILES ⚽️")

    if "filtered_data" in st.session_state and not st.session_state["filtered_data"].empty:
        data = st.session_state["filtered_data"]

        # Filtros de temporada y competición en la barra lateral
        seasons = data["Season"].unique()
        selected_season = st.sidebar.selectbox("Selecciona la temporada", seasons)

        competitions = data[data["Season"] == selected_season]["Competition"].unique()
        selected_competition = st.sidebar.selectbox("Selecciona la competición", ["Todos"] + list(competitions))

        if selected_competition == "Todos":
            filtered_data = data[data["Season"] == selected_season]
        else:
            filtered_data = data[(data["Season"] == selected_season) & (data["Competition"] == selected_competition)]

        # Seleccionar la posición en la barra lateral
        selected_position = st.sidebar.selectbox("Selecciona la posición", list(metrics_by_position.keys()))

        # Filtrar los jugadores según la posición seleccionada
        if selected_position == 'Portero':
            filtered_data = filtered_data[filtered_data['Primary position'].str.contains('GK', na=False)]
        elif selected_position == 'Defensa':
            filtered_data = filtered_data[filtered_data['Primary position'].str.contains('CB', na=False)]
        elif selected_position == 'Lateral Izquierdo':
            filtered_data = filtered_data[filtered_data['Primary position'].str.contains('LB|LWB', na=False)]
        elif selected_position == 'Lateral Derecho':
            filtered_data = filtered_data[filtered_data['Primary position'].str.contains('RB|RWB', na=False)]
        elif selected_position == 'Mediocampista Defensivo':
            filtered_data = filtered_data[filtered_data['Primary position'].str.contains('DMF', na=False)]
        elif selected_position == 'Mediocampista Central':
            filtered_data = filtered_data[filtered_data['Primary position'].str.contains('CMF', na=False)]
        elif selected_position == 'Mediocampista Ofensivo':
            filtered_data = filtered_data[filtered_data['Primary position'].str.contains('AMF', na=False)]
        elif selected_position == 'Extremos':
            filtered_data = filtered_data[filtered_data['Primary position'].str.contains('RW|LW|LWF|RWF', na=False)]
        elif selected_position == 'Delantero':
            filtered_data = filtered_data[filtered_data['Primary position'].str.contains('CF', na=False)]
        else:
            filtered_data = filtered_data

        # Agregar slider para minutos jugados en la barra lateral
        min_minutes = int(filtered_data['Minutes played'].min())
        max_minutes = int(filtered_data['Minutes played'].max())
        min_minutes_filter = st.sidebar.slider(
            "Filtrar por minutos jugados mínimos",
            min_value=min_minutes,
            max_value=max_minutes,
            value=350,
            step=50
        )

        # Filtrar jugadores según los minutos seleccionados
        filtered_data = filtered_data[filtered_data['Minutes played'] >= min_minutes_filter]
        total_players = len(filtered_data)

        if not filtered_data.empty:
            selected_player = st.selectbox("Selecciona un jugador", options=filtered_data["Full name"].unique())
            jugador_data = filtered_data[filtered_data['Full name'] == selected_player]

            if not jugador_data.empty:
                # Obtener todas las métricas disponibles para la posición
                all_metrics = metrics_by_position[selected_position]
                
                # Crear un diccionario con las métricas agrupadas por categoría
                metrics_by_category = {}
                for metric in all_metrics:
                    if metric[2] not in metrics_by_category:
                        metrics_by_category[metric[2]] = []
                    metrics_by_category[metric[2]].append((metric[0], metric[1]))  # metric[1] es la descripción en español

                # Crear selectores de métricas en una fila
                st.write("### Selecciona las métricas a mostrar")
                
                # Crear columnas para cada categoría
                cols = st.columns(len(metrics_by_category))
                
                selected_metrics = []
                selected_categories = []
                metric_labels = {}  # Diccionario para mantener las etiquetas en español
                
                # Iterar sobre las categorías y crear los selectores en cada columna
                for col, (category, metrics) in zip(cols, metrics_by_category.items()):
                    with col:
                        st.write(f"**{category}**")
                        # Checkbox para seleccionar todas las métricas de la categoría
                        select_all = st.checkbox(f"Todas", key=f"select_all_{category}")
                        
                        # Métricas individuales
                        for metric_name, metric_desc in metrics:
                            if metric_name in filtered_data.columns:  # Solo mostrar métricas disponibles
                                selected = st.checkbox(
                                    f"{metric_desc}",  # Usar la descripción en español
                                    value=select_all,
                                    key=f"metric_{metric_name}"
                                )
                                if selected:
                                    selected_metrics.append(metric_name)
                                    selected_categories.append(category)
                                    metric_labels[metric_name] = metric_desc  # Guardar la etiqueta en español

                if selected_metrics:  # Solo crear el gráfico si hay métricas seleccionadas
                    # Convertir las métricas a tipo numérico
                    for param in selected_metrics:
                        filtered_data[param] = pd.to_numeric(filtered_data[param], errors='coerce').fillna(0)
                        jugador_data[param] = pd.to_numeric(jugador_data[param], errors='coerce').fillna(0)

                    # Calcular los percentiles
                    values = []
                    categories = []
                    for param in selected_metrics:
                        value = jugador_data[param].iloc[0]
                        percentile = stats.percentileofscore(filtered_data[param], value)
                        values.append(math.floor(percentile))
                        
                        # Buscar la categoría correspondiente
                        for metric in all_metrics:
                            if metric[0] == param:
                                categories.append(metric[2])
                                break

                    # Definir los colores para cada categoría
                    category_colors = {
                        "General": "#1A78CF",      # Azul
                        "Defensa": "#FF9300",      # Naranja
                        "Pases": "#FF6347",        # Rojo
                        "Ataque": "#32CD32"        # Verde
                    }

                    # Asignar colores a las rebanadas según las categorías
                    slice_colors = [category_colors[cat] for cat in categories]

                    # Crear el gráfico de radar
                    baker = PyPizza(
                        params=[metric_labels[metric] for metric in selected_metrics],  # Usar etiquetas en español
                        background_color="#EBEBE9",
                        straight_line_color="#EBEBE9",
                        straight_line_lw=1,
                        last_circle_lw=0,
                        other_circle_lw=0,
                        inner_circle_size=18
                    )

                    fig, ax = baker.make_pizza(
                        values,
                        figsize=(8, 6.5),
                        color_blank_space="same",
                        slice_colors=slice_colors,
                        value_colors=["#F2F2F2"] * len(values),
                        value_bck_colors=slice_colors,
                        blank_alpha=0.4,
                        kwargs_slices=dict(edgecolor="#F2F2F2", zorder=2, linewidth=1),
                        kwargs_params=dict(color="#000000", fontsize=5, va="center"),
                        kwargs_values=dict(color="#000000", fontsize=7, zorder=3,
                                         bbox=dict(edgecolor="#000000", facecolor="cornflowerblue", 
                                                 boxstyle="round,pad=0.2", lw=1))
                    )

                    # Crear elementos de la leyenda
                    legend_elements = [
                        plt.Rectangle((0, 0), 1, 1, facecolor=color, label=category)
                        for category, color in category_colors.items()
                        if category in set(categories)  # Solo incluir categorías usadas
                    ]

                    # Agregar la leyenda
                    ax.legend(
                        handles=legend_elements,
                        loc='upper center',
                        bbox_to_anchor=(0.5, 1.1),
                        ncol=4,
                        frameon=False,
                        fontsize=10
                    )

                    # Ajustar el espaciado para acomodar la leyenda
                    plt.subplots_adjust(bottom=0.15)

                    # Agregar título y subtítulos
                    fig.text(0.5, 1.01, f"{selected_player} | {int(jugador_data['Age'].iloc[0])} años | {jugador_data['Team within selected timeframe'].iloc[0]}", 
                            size=16, ha="center", color="#000000")
                    fig.text(0.5, 0.98, f"{jugador_data['Foot'].iloc[0]} | {int(jugador_data['Minutes played'].iloc[0])} minutos | Comparado con {total_players} {selected_position}s", 
                            size=10, ha="center", color="#888888")
                    st.pyplot(fig)
                    
                else:
                    st.warning("Selecciona al menos una métrica para mostrar el gráfico.")
            else:
                st.warning("Jugador no encontrado.")
        else:
            st.warning("No hay jugadores que coincidan con los filtros seleccionados.")
    else:
        st.warning("Cargando los datos...")


################################# BEESWARMS ##################################################################################################################################################


def create_beeswarm_plot():
    # Utiliza los datos que ya tienes cargados en la sesión de Streamlit
    if "filtered_data" in st.session_state and not st.session_state["filtered_data"].empty:
        data = st.session_state["filtered_data"]
    else:
        st.warning("No se han cargado datos aún.")
        return

    # Convierte las columnas numéricas a tipo float
    numeric_columns = [col for col in data.columns if col in [metric[0] for metrics in metrics_by_position.values() for metric in metrics]]
    data[numeric_columns] = data[numeric_columns].astype(float)

    # Pide al usuario que seleccione la temporada
    available_seasons = sorted(data["Season"].dropna().unique().tolist())
    selected_season = st.selectbox("Selecciona la temporada:", available_seasons, key="season_selectbox")

    # Filtra los datos por temporada seleccionada
    filtered_data = data[data["Season"] == selected_season]

    # Pide al usuario que seleccione la competición
    available_competitions = sorted(filtered_data["Competition"].dropna().unique().tolist())
    selected_competition = st.selectbox("Selecciona la competición:", available_competitions, key="competition_selectbox")

    # Filtra los datos por competición seleccionada
    filtered_data = filtered_data[filtered_data["Competition"] == selected_competition]

    # Pide al usuario que seleccione el equipo
    available_teams = sorted(filtered_data["Team within selected timeframe"].dropna().unique().tolist())
    available_teams.insert(0, "Todos")
    selected_team = st.selectbox("Selecciona el equipo:", available_teams, index=0, key="team_selectbox")

    # Filtra los datos por equipo seleccionado
    if selected_team != "Todos":
        filtered_data = filtered_data[filtered_data["Team within selected timeframe"] == selected_team]

    # Pide al usuario que seleccione la posición
    position_options = list(metrics_by_position.keys())
    selected_position = st.selectbox("Selecciona la posición", position_options, key="position_selectbox")

    # Filtra los datos por posición seleccionada
    if selected_position == 'Portero':
        filtered_data = filtered_data[filtered_data['Position'].str.contains('GK', na=False)]
    elif selected_position == 'Defensa':
        filtered_data = filtered_data[filtered_data['Position'].str.contains('CB', na=False)]
    elif selected_position == 'Lateral Izquierdo':
        filtered_data = filtered_data[filtered_data['Position'].str.contains('LB|LWB', na=False)]
    elif selected_position == 'Lateral Derecho':
        filtered_data = filtered_data[filtered_data['Position'].str.contains('RB|RWB', na=False)]
    elif selected_position == 'Mediocampista Defensivo':
        filtered_data = filtered_data[filtered_data['Position'].str.contains('DMF', na=False)]
    elif selected_position == 'Mediocampista Central':
        filtered_data = filtered_data[filtered_data['Position'].str.contains('CMF', na=False)]
    elif selected_position == 'Mediocampista Ofensivo':
        filtered_data = filtered_data[filtered_data['Position'].str.contains('AMF', na=False)]
    elif selected_position == 'Extremos':
        filtered_data = filtered_data[filtered_data['Position'].str.contains('RW|LW|LWF|RWF', na=False)]
    elif selected_position == 'Delantero':
        filtered_data = filtered_data[filtered_data['Position'].str.contains('CF', na=False)]
    else:
        filtered_data = data

    # Pide al usuario que seleccione el jugador a destacar
    player_options = filtered_data['Full name'].unique()
    selected_player = st.selectbox("Selecciona el jugador a destacar", player_options, key="player_selectbox")

    # Selecciona la métrica a visualizar
    if selected_position in metrics_by_position:
        position_metrics = [metric[0] for metric in metrics_by_position[selected_position]]
        selected_metric = st.selectbox("Selecciona la métrica a visualizar:", position_metrics, key="metric_selectbox")
    else:
        st.warning(f"No se encontraron métricas definidas para la posición '{selected_position}'.")
        return

    # Ajusta el código de visualización según la métrica seleccionada
    fig, ax = plt.subplots(figsize=(6, 4))
    fig.set_facecolor('white')
    spines = ['top','bottom','left','right']
    for x in spines:
        if x in spines:
            ax.spines[x].set_visible(False)

    sns.swarmplot(x=selected_metric, data=filtered_data, zorder=1, ax=ax)

    if not filtered_data.empty and selected_player in filtered_data['Full name'].values:
        valor = filtered_data[filtered_data['Full name'] == selected_player][selected_metric].values[0]
    else:
        valor = 0

    ax.scatter(valor, 0, s=200, color='red', edgecolor='black', zorder=2)
    ax.set_xlabel(f'Valor de {selected_metric}', fontsize=12)
    ax.set_xticks([])
    ax.axvline(filtered_data[selected_metric].median(), lw=1.2, color='black')

    style = "Simple, tail_width=0.5, head_width=4, head_length=8"
    kw = dict(arrowstyle=style, color="k")
    a = patches.FancyArrowPatch((valor, 0), (valor+1, 0.2),
                                 connectionstyle="arc3,rad=.5", **kw)

    ax.add_patch(a)

    ax.text(valor+1.1, 0.2, selected_player.replace(' ', '\n'), fontsize=14, va='center')

    fig.text(.13, 1.05, f'Valor de {selected_metric} por jugador ({selected_position})', fontsize=15)
    fig.text(.13, 0.95, f'Jugadores de {selected_competition} en la temporada {selected_season} con más de\n270 min jugados', fontsize=15, color='grey')

    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=150, bbox_inches='tight')
    st.image(buf, use_column_width=True)


##################################### RADAR ###########################################################################################

def create_radar_plot():
    if 'filtered_data' not in st.session_state:
        return

    df = st.session_state['filtered_data']
    
    # Normalizar los datos
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    df[numeric_cols] = (df[numeric_cols] - df[numeric_cols].min()) / (df[numeric_cols].max() - df[numeric_cols].min())

    # Mover los filtros a la barra lateral
    with st.sidebar:
        seasons = ['Todas'] + list(df['Season'].unique())
        selected_season = st.selectbox('Temporada:', seasons, key='radar_plot_season')

    filtered_df = df if selected_season == 'Todas' else df[df['Season'] == selected_season].copy()

    with st.sidebar:
        competitions = ['Todas'] + list(filtered_df['Competition'].unique())
        selected_competition = st.selectbox('Competición:', competitions, key='radar_plot_comp')

    if selected_competition != 'Todas':
        filtered_df = filtered_df[filtered_df['Competition'] == selected_competition]

    with st.sidebar:
        teams = list(filtered_df['Team within selected timeframe'].unique())
        selected_teams = st.multiselect('Equipos:', teams, key='radar_plot_teams')

    if selected_teams:
        filtered_df = filtered_df[filtered_df['Team within selected timeframe'].isin(selected_teams)]

    with st.sidebar:
        positions = ['Todas', 'Portero', 'Defensa', 'Lateral Izquierdo', 'Lateral Derecho', 
                    'Mediocampista Defensivo', 'Mediocampista Central', 'Mediocampista Ofensivo',
                    'Extremos', 'Delantero']
        selected_position = st.selectbox('Posición:', positions, key='radar_plot_pos')

    if selected_position != 'Todas':
        position_filters = {
            'Portero': 'GK', 'Defensa': 'CB', 'Lateral Izquierdo': 'LB|LWB',
            'Lateral Derecho': 'RB|RWB', 'Mediocampista Defensivo': 'DMF',
            'Mediocampista Central': 'CMF', 'Mediocampista Ofensivo': 'AMF',
            'Extremos': 'RW|LW|LWF|RWF', 'Delantero': 'CF'
        }
        filtered_df = filtered_df[filtered_df['Position'].str.contains(position_filters[selected_position], na=False)]

    with st.sidebar:
        min_minutes = int(filtered_df['Minutes played'].min())
        max_minutes = int(filtered_df['Minutes played'].max())
        if min_minutes == max_minutes:
            selected_minutes = min_minutes
        else:
            selected_minutes = st.slider('Minutos jugados:', int(min_minutes), int(max_minutes), int(min_minutes), key='radar_plot_minutes')
        filtered_df = filtered_df[filtered_df['Minutes played'] >= selected_minutes]

    with st.sidebar:
        players = list(filtered_df['Full name'].unique())
        selected_players = st.multiselect('Jugadores (máx. 5):', players, max_selections=5, key='radar_plot_players')

    if selected_players:
        numeric_cols = filtered_df.select_dtypes(include=[np.number]).columns.tolist()
        selected_metrics = st.multiselect('Métricas a comparar:', numeric_cols, default=numeric_cols[:5] if len(numeric_cols) >= 5 else numeric_cols, key='radar_plot_metrics')

        if selected_metrics:
            df_radar = filtered_df[filtered_df['Full name'].isin(selected_players)].copy()
            
            fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(projection='polar'))
            angles = [n / float(len(selected_metrics)) * 2 * pi for n in range(len(selected_metrics))]
            angles += angles[:1]

            ax.set_theta_offset(pi / 2)
            ax.set_theta_direction(-1)
            ax.set_xticks(angles[:-1])
            ax.set_xticklabels(selected_metrics, size=7)
            ax.tick_params(axis='x', which='major', pad=7)

            colors = ['#e6194b', '#3cb44b', '#ffe119', '#4363d8', '#f58231']
            legend_handles = []
            for idx, player in enumerate(selected_players):
                values = df_radar[df_radar['Full name'] == player][selected_metrics].values.flatten().tolist()
                values += values[:1]
                line, = ax.plot(angles, values, linewidth=2, linestyle='solid', color=colors[idx])
                ax.fill(angles, values, colors[idx], alpha=0.2)
                legend_handles.append(line)

            plt.legend(legend_handles, selected_players, loc='upper center', bbox_to_anchor=(0.5, -0.1), ncol=5, fontsize=8)
            plt.subplots_adjust(top=0.85, bottom=0.15)
            plt.title('Comparación de métricas normalizadas de jugadores', fontsize=14, pad=20)
            st.pyplot(fig)

################################################################################################################################

tab_functions = {
    "Cargar Datos 🏆": main_page,
    "Buscar 🔎": search_page,
    "Comparar ⚖️": comparison_page,
    "Similitud 🥇🥈🥉": similarity_page,
    "Densidad 📊": density_page,
    "Dispersión - Análisis 📈": create_scatter_plot,
    "Percentiles 🎯": radar_page,
    "Besswarms ↔️": create_beeswarm_plot,
    "Radar Comparativo ⚔️": create_radar_plot
}

tab_selection = st.sidebar.radio("", list(tab_functions.keys()))
tab_functions[tab_selection]()
