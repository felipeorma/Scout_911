import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics.pairwise import euclidean_distances
import seaborn as sns
import mplsoccer as mps

# Configuración de la página
st.set_page_config(
    page_title="ScoutiFY by Felipe Ormazabal",
    initial_sidebar_state="expanded"
)

# Diccionario de usuarios y contraseñas
usuarios = {
    "Carlos": {"Contrasena": "scout", "nombre_visualizar": "Carlos Canal"}
}

# Mapeo de posiciones y métricas para radar
posicion_mapeo = {
    'GK': 'Portero',
    'LB': 'Lateral izquierdo', 'LWB': 'Lateral izquierdo',
    'RB': 'Lateral Derecho', 'RWB': 'Lateral Derecho',
    'LCB': 'Defensa', 'CB': 'Defensa', 'RCB': 'Defensa',
    'LDMF': 'Mediocampo', 'LCMF': 'Mediocampo', 'DMF': 'Mediocampo', 'RDMF': 'Mediocampo',
    'RCMF': 'Mediocampo', 'AMF': 'Mediocampo',
    'LAMF': 'Extremo Izquierdo', 'LW': 'Extremo Izquierdo', 'LWF': 'Extremo Izquierdo',
    'RAMF': 'Extremo Derecho', 'RW': 'Extremo Derecho', 'RWF': 'Extremo Derecho',
    'CF': 'Delantero',
}

metricas_por_posicion_para_radar = {
    'Portero': ["Goles recibidos/90", "xG en contra/90", "Goles evitados/90", "Paradas, %", "Salidas/90", "Duelos aéreos en los 90",
                "Pases recibidos /90", "Precisión pases laterales, %", "Precisión pases hacia adelante, %", "Precisión pases largos, %"],
    'Defensa': ["Duelos defensivos ganados, %", "Duelos aéreos ganados, %", "Entradas/90", "Interceptaciones/90","Posesión conquistada después de una interceptación",
                "Precisión pases, %","Precisión pases largos, %","Aceleraciones/90","Carreras en progresión/90","Jugadas claves/90"],
    'Lateral': ["xA/90","Precisión pases en profundidad, %", "Pases recibidos /90", "Pases/90","Centros al área pequeña/90", "Centros desde el último tercio/90",
                "Aceleraciones/90", "Carreras en progresión/90", "Acciones de ataque exitosas/90", "Duelos atacantes ganados, %",
                "Interceptaciones/90","Duelos defensivos ganados, %"],
    'Mediocampista': ["xG/90", "Goles/90", "Asistencias/90", "xA/90","Regates realizados, %", "Pases recibidos /90", "Precisión pases cortos / medios, %",
                   "Precisión pases en el último tercio, %", "Duelos defensivos ganados, %","Interceptaciones/90"],
    'Extremos': ["xG/90", "Goles/90","xA/90", "Asistencias/90", "Centros al área pequeña/90", 
                "Pases hacía el área pequeña, %","Precisión pases en el último tercio, %",  "Duelos atacantes ganados, %","Regates realizados, %"],
    'Delantero': ["xG/90","Goles/90","Goles, excepto los penaltis/90","Goles de cabeza/90","Duelos aéreos ganados, %",
                  "xA/90","Asistencias/90","Jugadas claves/90","Pases al área de penalti/90","Precisión pases en el último tercio, %"]
}

roles_por_posicion = {
    'Portero': ['Portero Bueno con los Pies', 'Portero con Muchas paradas'],
    'Defensa': ['Central ganador de Duelos', 'Central Rapido','Central Tecnico'],
    'Lateral izquierdo': ['Lateral Defensivo', 'Lateral Ofensivo'],
    'Lateral Derecho': ['Lateral Defensivo', 'Lateral Ofensivo'],
    'Mediocampo' : ['Mediocentro Defensivo (Fisico)','Mediocentro BoxToBox','Mediocentro Creador'],
    'Extremo Izquierdo' : ['Extremo Regateador','Extremo centrador','Extremo Goleador'],
    'Extremo Derecho' : ['Extremo Regateador','Extremo centrador','Extremo Goleador'],
    'Delantero' : ['Delantero Asociativo','Delantero Cabeceador','Delantero Killer']
}

metricas_posicion_rating = {
    'Portero Bueno con los Pies': {
        'metricas': [
            'Pases recibidos /90', 'Pases/90', 'Precisión pases, %', 'Pases hacia adelante/90', 'Precisión pases hacia adelante, %',
            'Pases laterales/90', 'Precisión pases laterales, %', 'Pases cortos / medios /90', 'Precisión pases cortos / medios, %',
            'Pases largos/90', 'Precisión pases largos, %', 'Goles recibidos/90', 'Remates en contra/90', 'xG en contra/90',
            'Goles evitados/90', 'Salidas/90', 'Duelos aéreos en los 90', 'Paradas, %', 'Porterías imbatidas en los 90'
        ],
        'ponderaciones': [
            0.075, 0.1, 0.1251, 0.05, 0.075, 0.05, 0.075, 0.05, 0.075, 0.05, 0.075, -0.1, -0.075, -0.05, 0.1, 0.05, 0.075, 0.1, 0.1
        ]
    },
    'Portero con Muchas paradas': {
        'metricas': [
            'Goles recibidos/90', 'Remates en contra/90', 'xG en contra/90', 'Goles evitados/90', 'Salidas/90', 'Duelos aéreos en los 90',
            'Paradas, %', 'Porterías imbatidas en los 90'
        ],
        'ponderaciones': [
            -0.5, -0.373, -0.25, 0.5, 0.25, 0.373, 0.5, 0.5
        ]
    },
    'Lateral Defensivo': {
        'metricas': [
            'Duelos ganados, %', 'Acciones defensivas realizadas/90', 'Duelos defensivos/90', 'Duelos defensivos ganados, %', 
            'Duelos aéreos ganados, %', 'Interceptaciones/90', 'Pases/90', 'Precisión pases, %', 'Pases hacia adelante/90', 
            'Precisión pases hacia adelante, %'
        ],
        'ponderaciones': [
            0.1209, 0.0909, 0.0909, 0.1209, 0.0909, 0.1518, 0.0609, 0.1209, 0.0609, 0.0909
        ]
    },
    'Lateral Ofensivo': {
        'metricas': [
            'Duelos ganados, %', 'Acciones defensivas realizadas/90', 'Duelos defensivos/90', 'Duelos defensivos ganados, %',
            'Duelos aéreos ganados, %', 'Interceptaciones/90', 'Pases/90', 'Precisión pases, %', 'Pases hacia adelante/90',
            'Precisión pases hacia adelante, %', 'Acciones de ataque exitosas/90', 'Centros al área pequeña/90', 
            'Duelos atacantes ganados, %', 'Carreras en progresión/90', 'Aceleraciones/90', 'Pases recibidos /90', 
            'Third assists/90', 'Precisión pases en el último tercio, %', 'Pases hacía el área pequeña, %', 
            'Precisión pases en profundidad, %', 'Centros desde el último tercio/90', 'Precisión pases progresivos, %'
        ],
        'ponderaciones': [
            0.0758, 0.0568, 0.0568, 0.0758, 0.0568, 0.0947, 0.0379, 0.0758, 0.0379, 0.0568, 0.0313, 0.0313, 0.0313, 
            0.0313, 0.0313, 0.0313, 0.0313, 0.0313, 0.0313, 0.0313, 0.0313, 0.0313
        ]
    },
    'Lateral Ofensivo': {
        'metricas': [
            'Duelos ganados, %',
            'Acciones defensivas realizadas/90',
            'Duelos defensivos/90',
            'Duelos defensivos ganados, %',
            'Duelos aéreos ganados, %',
            'Interceptaciones/90',
            'Pases/90',
            'Precisión pases, %',
            'Pases hacia adelante/90',
            'Precisión pases hacia adelante, %',
            'Acciones de ataque exitosas/90',
            'Centros al área pequeña/90',
            'Duelos atacantes ganados, %',
            'Carreras en progresión/90',
            'Aceleraciones/90',
            'Pases recibidos /90',
            'Third assists/90',
            'Precisión pases en el último tercio, %',
            'Pases hacía el área pequeña, %',
            'Precisión pases en profundidad, %',
            'Centros desde el último tercio/90',
            'Precisión pases progresivos, %'
        ],
        'ponderaciones': [
        0.0758,  # Duelos ganados, %
        0.0568,  # Acciones defensivas realizadas/90
        0.0568,  # Duelos defensivos/90
        0.0758,  # Duelos defensivos ganados, %
        0.0568,  # Duelos aéreos ganados, %
        0.0947,  # Interceptaciones/90
        0.0379,  # Pases/90
        0.0758,  # Precisión pases, %
        0.0379,  # Pases hacia adelante/90
        0.0568,  # Precisión pases hacia adelante, %
        0.0313,  # Acciones de ataque exitosas/90 (valor inicial para métricas faltantes)
        0.0313,  # Centros al área pequeña/90
        0.0313,  # Duelos atacantes ganados, %
        0.0313,  # Carreras en progresión/90
        0.0313,  # Aceleraciones/90
        0.0313,  # Pases recibidos /90
        0.0313,  # Third assists/90
        0.0313,  # Precisión pases en el último tercio, %
        0.0313,  # Pases hacía el área pequeña, %
        0.0313,  # Precisión pases en profundidad, %
        0.0313,  # Centros desde el último tercio/90
        0.0313   # Precisión pases progresivos, % 
    ]
    },
    'Central ganador de Duelos': {
    'metricas': [
        'Duelos/90',
        'Duelos ganados, %',
        'Duelos defensivos/90',
        'Duelos defensivos ganados, %',
        'Duelos aéreos en los 90',
        'Duelos aéreos ganados, %'
    ],
    'ponderaciones': [
        0.1579,  # Duelos/90
        0.2105,  # Duelos ganados, %
        0.1053,  # Duelos defensivos/90
        0.2632,  # Duelos defensivos ganados, %
        0.1053,  # Duelos aéreos en los 90
        0.1579   # Duelos aéreos ganados, %
    ]
    },
    'Central Rapido': {
    'metricas': [
        'Aceleraciones/90',
        'Carreras en progresión/90',
        'Interceptaciones/90',
        'Duelos defensivos/90',
        'Posesión conquistada después de una interceptación',
        'Entradas/90'
    ],
    'ponderaciones': [
        0.16,  # Aceleraciones/90
        0.12,  # Carreras en progresión/90
        0.2,   # Interceptaciones/90
        0.08,  # Duelos defensivos/90
        0.16,  # Posesión conquistada después de una interceptación
        0.28   # Entradas/90
    ]
    },
    'Central Tecnico': {
    'metricas': [
        'Pases/90',
        'Precisión pases, %',
        'Pases cortos / medios /90',
        'Precisión pases cortos / medios, %',
        'Pases largos/90',
        'Precisión pases largos, %',
        'Pases hacia adelante/90',
        'Precisión pases hacia adelante, %',
        'Pases hacia atrás/90',
        'Precision pases hacia atrás, %',
        'Pases laterales/90',
        'Precisión pases laterales, %',
        'Jugadas claves/90',
        'Pases en el último tercio/90',
        'Precisión pases en el último tercio, %'
    ],
    'ponderaciones': [
        0.0755,  # Pases/90
        0.0943,  # Precisión pases, %
        0.0566,  # Pases cortos / medios /90
        0.0755,  # Precisión pases cortos / medios, %
        0.0566,  # Pases largos/90
        0.0755,  # Precisión pases largos, %
        0.0566,  # Pases hacia adelante/90
        0.0755,  # Precisión pases hacia adelante, %
        0.0377,  # Pases hacia atrás/90
        0.0566,  # Precision pases hacia atrás, %
        0.0377,  # Pases laterales/90
        0.0566,  # Precisión pases laterales, %
        0.0755,  # Jugadas claves/90
        0.0943,  # Pases en el último tercio/90
        0.0755   # Precisión pases en el último tercio, %
    ]
},
    'Mediocentro Defensivo (Fisico)': {
    'metricas': [
        'Duelos/90',
        'Duelos ganados, %',
        'Duelos defensivos/90',
        'Duelos defensivos ganados, %',
        'Interceptaciones/90',
        'Entradas/90',
        'Faltas/90',
        'Posesión conquistada después de una entrada',
        'Posesión conquistada después de una interceptación'
    ],
    'ponderaciones': [
        0.129,  # Duelos/90
        0.1613, # Duelos ganados, %
        0.129,  # Duelos defensivos/90
        0.1613, # Duelos defensivos ganados, %
        0.129,  # Interceptaciones/90
        0.129,  # Entradas/90
        -0.0968,# Faltas/90 (Se resta debido a que es una métrica negativa para un mediocentro defensivo)
        0.129,  # Posesión conquistada después de una entrada
        0.129   # Posesión conquistada después de una interceptación
    ]
},
    'Mediocentro BoxToBox': {
    'metricas': [
        'Duelos/90',
        'Duelos ganados, %',
        'Pases/90',
        'Precisión pases, %',
        'Interceptaciones/90',
        'Carreras en progresión/90',
        'Aceleraciones/90',
        'Remates/90',
        'Goles/90',
        'Asistencias/90',
        'Toques en el área de penalti/90',
        'Remates/90',
        'xG/90',
        'Pases al área de penalti/90'
    ],
    'ponderaciones': [
        0.07,  # Duelos/90
        0.09,  # Duelos ganados, %
        0.07,  # Pases/90
        0.08,  # Precisión pases, %
        0.07,  # Interceptaciones/90
        0.09,  # Carreras en progresión/90
        0.07,# Aceleraciones/90
        0.07,  # Remates/90
        0.06, # Goles/90
        0.07,  # Asistencias/90
        0.07,  # Toques en el área de penalti/90
        0.07,  # Remates/90
        0.06,  # xG/90
        0.06   # Pases al área de penalti/90
    ],
    },
    'Mediocentro Creador': {
    'metricas': [
        'Asistencias/90',
        'xA/90',
        'Acciones de ataque exitosas/90',
        'Goles/90',
        'Duelos/90',
        'Duelos ganados, %',
        'Entradas/90',
        'Interceptaciones/90',
        'Regates/90',
        'Precisión pases, %',
        'Precisión pases hacia adelante, %',
        'Jugadas claves/90',
        'Pases en el último tercio/90',
        'Precisión pases en el último tercio, %',
        'Centros/90',
        'Precisión centros, %',
        'Desmarques/90'
    ],
    'ponderaciones': [
        0.12,  # Asistencias/90
        0.12,  # xA/90
        0.10,  # Acciones de ataque exitosas/90
        0.07,  # Goles/90
        0.07,  # Duelos/90
        0.07,  # Duelos ganados, %
        0.01,  # Entradas/90
        0.06,  # Interceptaciones/90
        0.07,  # Regates/90
        0.05,  # Precisión en los pases/90
        0.05,  # Precisión en los pases hacia adelante/90
        0.04,  # Jugadas claves/90
        0.04,  # Pases en el último tercio/90
        0.04,  # Precisión en los pases en el último tercio/90
        0.03,  # Centros/90
        0.03,  # Precisión en los centros/90
        0.03   # Desmarques/90
    ]
},
    'Extremo Regateador': {
    'metricas': [
        'Regates/90',
        'Regates realizados, %',
        'Duelos atacantes/90',
        'Duelos atacantes ganados, %',
        'Aceleraciones/90',
        'Remates/90',
        'Asistencias/90',
        'Jugadas claves/90',
        'Toques en el área de penalti/90',
        'Centros/90',
        'Precisión centros, %'
    ],
    'ponderaciones': [
        0.15,  # Regates/90
        0.08,  # Regates realizados, %
        0.08,  # Duelos atacantes/90
        0.10,  # Duelos atacantes ganados, %
        0.08,  # Aceleraciones/90
        0.08,  # Remates/90
        0.08,  # Asistencias/90
        0.08,  # Jugadas claves/90
        0.09,  # Toques en el área de penalti/90
        0.08,  # Centros/90
        0.10   # Precisión centros, %
    ]
},
    'Extremo centrador': {
    'metricas': [
        'Centros/90',
        'Precisión centros, %',
        'Jugadas claves/90',
        'Asistencias/90',
        'Pases en el último tercio/90',
        'Precisión pases en el último tercio, %',
        'Toques en el área de penalti/90',
        'Pases al área de penalti/90',
        'Regates/90',
        'Aceleraciones/90',
        'xA/90'
    ],
    'ponderaciones': [
       0.15,  # Centros/90
        0.09,  # Precisión centros, %
        0.1,  # Jugadas claves/90
        0.1,  # Asistencias/90
        0.07,  # Pases en el último tercio/90
        0.09,  # Precisión pases en el último tercio, %
        0.05,  # Toques en el área de penalti/90
        0.09,  # Pases al área de penalti/90
        0.08,  # Regates/90
        0.09,  # Aceleraciones/90
        0.09   # xA/90
    ]
},
    'Extremo Goleador': {
    'metricas': [
        'Goles/90',
        'Remates/90',
        'xG/90',
        'Goles de cabeza/90',
        'Tiros a la portería, %',
        'Asistencias/90',
        'Jugadas claves/90',
        'Toques en el área de penalti/90',
        'Remates/90',
        'Goles hechos, %'
    ],
    'ponderaciones': [
        0.1,  # Goles/90
        0.13,  # Remates/90
        0.11,  # xG/90
        0.13,  # Goles de cabeza/90
        0.13,  # Tiros a la portería, %
        0.06,  # Asistencias/90
        0.1,  # Jugadas claves/90
        0.1,  # Toques en el área de penalti/90
        0.06,  # Remates/90 (repetido)
        0.08   # Goles hechos, %
    ]
},
    'Delantero Cabeceador': {
    'metricas': [
        'Goles de cabeza',
        'Goles de cabeza/90',
        'Duelos aéreos en los 90',
        'Duelos aéreos ganados, %',
        'Remates/90',
        'Goles/90',
        'xG/90',
        'Toques en el área de penalti/90'
    ],
    'ponderaciones': [
         0.2,  # Goles de cabeza
        0.1,  # Goles de cabeza/90
        0.14,  # Duelos aéreos en los 90
        0.15,  # Duelos aéreos ganados, %
        0.08,  # Remates/90
        0.08,  # Goles/90
        0.08,  # xG/90
        0.07,  # Centros recibidos/90
        0.10,  # Toques en el área de penalti/90
    ]
},
    'Delantero Killer': {
    'metricas': [
        'Goles/90',
        'xG/90',
        'Remates/90',
        'Tiros a la portería, %',
        'Goles hechos, %',
        'Asistencias/90',
        'Jugadas claves/90',
        'Toques en el área de penalti/90',
        'Remates/90',
        'Duelos ganados, %',
        'Pases al área de penalti/90',
        'Goles (excepto los penaltis)',
        'Goles, excepto los penaltis/90'
    ],
    'ponderaciones': [
        0.13,  # Goles/90
        0.1,  # xG/90
        0.1,   # Remates/90
        0.1,   # Tiros a la portería, %
        0.1,   # Goles hechos, %
        0.02,  # Asistencias/90
        0.05,  # Jugadas claves/90
        0.05,  # Toques en el área de penalti/90
        0.09,  # Remates/90
        0.06,  # Duelos ganados, %
        0.06,  # Pases al área de penalti/90
        0.07,  # Goles (excepto los penaltis)
        0.07    # Goles, excepto los penaltis/90
    ]
},
    'Delantero Asociativo': {
    'metricas': [
        'Asistencias/90',
        'Jugadas claves/90',
        'Pases/90',
        'Precisión pases, %',
        'Duelos ganados, %',
        'Toques en el área de penalti/90',
        'Remates/90',
        'xG/90',
        'Goles/90',
        'Pases en el último tercio/90',
        'Precisión pases en el último tercio, %',
        'Pases al área de penalti/90'
    ],
    'ponderaciones': [
         0.09,  # Asistencias/90
         0.1,  # Jugadas claves/90
         0.09,   # Pases/90
         0.09,   # Precisión pases, %
         0.09,  # Duelos ganados, %
         0.1,   # Toques en el área de penalti/90
         0.08,  # Remates/90
         0.08,   # xG/90
         0.08,   # Goles/90
         0.08,   # Pases en el último tercio/90
         0.04,   # Precisión pases en el último tercio, %
         0.08   # Pases al área de penalti/90
    ]
}
}


positions = {
    "Portero": (5, 35),
    "Lateral izquierdo": (25, 57),
    "Defensa central izquierdo": (20, 40),
    "Defensa central derecho": (20, 27),
    "Lateral derecho": (25, 10),
    "Medio defensivo": (45, 34.5),
    "Medio izquierdo": (55, 45),
    "Medio derecho": (55, 20),
    "Extremo izquierdo": (80, 57),
    "Delantero centro": (85, 34.5),
    "Extremo derecho": (80, 10)
}

situation_colors = {
    "Baja": "grey",
    "Cesion": "blue",
    "Lesion larga": "purple",
    "Juvenil": "yellow",
    "Extranjero": "red",
    "Incorporar": "orange"
}



# Función para cargar los datos desde session_state
def get_data():
    if 'data' in st.session_state:
        return st.session_state['data']
    return None

# Función de inicio de sesión
def iniciar_sesion(usuario, contrasena):
    return usuario in usuarios and usuarios[usuario]["Contrasena"] == contrasena

# Función para mostrar el formulario de inicio de sesión
def mostrar_formulario_login():
    st.title("Inicio de Sesión")
    usuario = st.text_input("Usuario", key="usuario")
    contrasena = st.text_input("Contraseña", type="password", key="contrasena")
    
    if st.button("Iniciar Sesión"):
        if iniciar_sesion(usuario, contrasena):
            st.session_state["usuario_autenticado"] = True
            st.session_state["nombre_asignado"] = usuarios[usuario]["nombre_visualizar"]
            st.experimental_rerun()
        else:
            st.error("Usuario o contraseña incorrectos.")

# Función para hacer logout
def hacer_logout():
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.experimental_rerun()

# Cargar los datos desde session_state
df = get_data()

# Función para mostrar el mensaje de bienvenida
def mostrar_bienvenida():
    if "usuario_autenticado" in st.session_state:
        nombre_usuario = st.session_state["nombre_asignado"]
        st.title("Bienvenido a ScoutiFY")
        st.write(f"Bienvenido, {nombre_usuario}!")
        
        if st.button("Cerrar sesión"):
            hacer_logout()
    else:
        mostrar_formulario_login()

# Función para calcular similitudes de jugadores
def calcular_similitudes(df, jugador_objetivo, metricas):
    # Filtrar los datos del jugador objetivo y el resto
    df_unico = df.drop_duplicates(subset='Full name')
    df_unico = df_unico[df_unico['Minutos jugados'] > 0]
    df_filtrado = df_unico[df_unico['Full name'] != jugador_objetivo].copy()
    df_metricas = df_filtrado[metricas].fillna(0)
    df_metricas['Jugador'] = df_filtrado['Full name']
    
    # Normalizar métricas
    scaler = MinMaxScaler()
    df_metricas_normalizadas = pd.DataFrame(scaler.fit_transform(df_metricas.drop('Jugador', axis=1)), columns=metricas)
    
    # Obtener las métricas del jugador objetivo
    valores_jugador_objetivo = df_unico[df_unico['Full name'] == jugador_objetivo][metricas].fillna(0)
    if valores_jugador_objetivo.shape[0] == 1:
        valores_objetivo = scaler.transform(valores_jugador_objetivo)
    else:
        raise ValueError("Múltiples o ningún jugador objetivo encontrado. Asegúrate de que el jugador objetivo sea único.")
    
    # Calcular similitudes usando distancias euclidianas
    distancias = euclidean_distances(df_metricas_normalizadas, valores_objetivo)
    similitudes = 1 / (1 + distancias) * 100
    df_filtrado['Porcentaje de Similitud'] = similitudes.flatten()
    df_filtrado['Porcentaje de Similitud'] = df_filtrado['Porcentaje de Similitud'].apply(lambda x: f"{x:.1f}%")
    return df_filtrado

# Función para calcular el rating de jugadores
def calcular_rating_jugadores(df, metricas, ponderaciones):
    # Verificar que las ponderaciones sumen aproximadamente 1
    suma_ponderaciones = sum(ponderaciones)
    if not 0.999 < suma_ponderaciones < 1.001:
        raise ValueError("La suma de las ponderaciones debe ser aproximadamente igual a 1.")
    
    # Calcular el rating basado en las métricas y ponderaciones
    df_rating = df.copy()
    for i, metrica in enumerate(metricas):
        df_rating[metrica] = df_rating[metrica].astype(float) * ponderaciones[i]
    df_rating['Rating'] = df_rating[metricas].sum(axis=1)
    
    # Normalizar el rating en una escala de 0 a 1
    min_rating = df_rating['Rating'].min()
    max_rating = df_rating['Rating'].max()
    df_rating['Rating'] = (df_rating['Rating'] - min_rating) / (max_rating - min_rating)
    df_rating['Rating'] = df_rating['Rating'].round(2)
    return df_rating['Rating']

# Función para mostrar la interfaz de similitudes de jugadores
def mostrar_similitudes(df):
    st.subheader("Similitudes de Jugadores")
    
    if df is not None:
        jugador_objetivo = st.selectbox('Selecciona el jugador objetivo', df['Full name'].unique())
        posicion_general = st.selectbox('Selecciona la posición general', list(metricas_por_posicion_para_radar.keys()))
        metricas = metricas_por_posicion_para_radar[posicion_general]
        
        if st.button('Calcular similitud'):
            df_similitudes = calcular_similitudes(df, jugador_objetivo, metricas)
            st.write(f"Jugadores similares a {jugador_objetivo}:")
            columnas_mostrar = ['Jugador', 'Age', 'Team within selected timeframe', 'Passport country', '$ Transfermarkt', 'Porcentaje de Similitud']
            st.dataframe(df_similitudes[columnas_mostrar].sort_values(by='Porcentaje de Similitud', ascending=False))
    else:
        st.warning("No se han cargado los datos. Por favor, carga los datos en la página principal.")

# Función para mostrar la interfaz de ratings de jugadores
def mostrar_ratings(df):
    st.subheader("Ratings de Jugadores")
    
    if df is not None:
        rol = st.selectbox('Rol:', list(roles_por_posicion.keys()))
        
        # Determina las métricas y ponderaciones según el rol
        roles_disponibles = roles_por_posicion[rol]
        rol_seleccionado = st.selectbox('Selecciona el tipo de rol', roles_disponibles)
        
        metricas = metricas_posicion_rating[rol_seleccionado]['metricas']
        ponderaciones = metricas_posicion_rating[rol_seleccionado]['ponderaciones']

        if st.button("Calcular Rating"):
            df['Rating'] = calcular_rating_jugadores(df, metricas, ponderaciones)
            st.write("Jugadores con rating calculado:")
            st.dataframe(df[['Full name', 'Age', 'Team within selected timeframe', 'Rating']].sort_values(by='Rating', ascending=False))
    else:
        st.warning("No se han cargado los datos. Por favor, carga los datos en la página principal.")
import matplotlib.patches as patches

# Función para agregar jugadores al campograma
def add_players(ax, players):
    for player, details in players.items():
        for idx, (name, color) in enumerate(details['names']):
            position = (details['position'][0], details['position'][1] - 3 * idx)
            text_color = 'black' if color in ['yellow', 'white', 'orange'] else 'white'
            ax.text(position[0], position[1], name, ha="center", va="center", color=text_color, fontsize=10, 
                    bbox=dict(facecolor=color, edgecolor="none", boxstyle="round,pad=0.3"))

# Función para crear el campograma
def create_campograma(players, save_as_file=False):
    fig, ax = plt.subplots(figsize=(15, 8))
    ax.add_patch(patches.Rectangle((0, 0), width=100, height=65, edgecolor="black", facecolor="green"))
    ax.add_patch(patches.Rectangle((0, 24.85), width=5.5, height=15.3, edgecolor="white", fill=False))
    ax.add_patch(patches.Rectangle((94.5, 24.85), width=5.5, height=15.3, edgecolor="white", fill=False))
    ax.add_patch(patches.Rectangle((0, 13.85), width=16.5, height=37.3, edgecolor="white", fill=False))
    ax.add_patch(patches.Rectangle((83.5, 13.85), width=16.5, height=37.3, edgecolor="white", fill=False))
    ax.plot([50, 50], [0, 65], color="white")
    ax.add_patch(patches.Circle((50, 32.5), 9.15, edgecolor="white", fill=False))
    ax.add_patch(patches.Circle((50, 32.5), 0.8, edgecolor="white", facecolor="white"))
    ax.add_patch(patches.Circle((11, 32.5), 0.8, edgecolor="white", facecolor="white"))
    ax.add_patch(patches.Circle((89, 32.5), 0.8, edgecolor="white", facecolor="white"))
    ax.annotate('', xy=(90, 5), xytext=(10, 5), arrowprops=dict(facecolor='white', edgecolor='white', arrowstyle='->', lw=2, alpha=0.5))
    add_players(ax, players)

    # Leyenda
    counts = {"grey": 0, "blue": 0, "purple": 0, "yellow": 0, "red": 0, "orange": 0, "white": 0, "total": 0}
    for details in players.values():
        for name, color in details['names']:
            counts[color] += 1
            counts["total"] += 1

    legend_labels = [
        ("Plantilla", "white", counts["total"]),
        ("Bajas", "grey", counts["grey"]),
        ("Cesiones", "blue", counts["blue"]),
        ("Lesión larga", "purple", counts["purple"]),
        ("Juveniles", "yellow", counts["yellow"]),
        ("Extranjeros", "red", counts["red"]),
        ("Incorporar", "orange", counts["orange"])
    ]

    for i, (label, color, count) in enumerate(legend_labels):
        text_color = 'black' if color in ['yellow', 'white', 'orange'] else 'white'
        ax.text(105, 60 - i*5, f"{label} ({count})", ha="left", va="center", color=text_color, fontsize=12, 
                bbox=dict(facecolor=color, edgecolor="none", boxstyle="round,pad=0.3"))

    ax.set_xlim(0, 120)
    ax.set_ylim(0, 65)
    ax.axis('off')

    if save_as_file:
        buf = io.BytesIO()
        fig.savefig(buf, format='png', dpi=300)
        buf.seek(0)
        return buf
    else:
        st.pyplot(fig)
# Estructura principal de la aplicación
def main():
    if "usuario_autenticado" not in st.session_state:
        mostrar_formulario_login()
    else:
        mostrar_bienvenida()

        # Crear las pestañas principales
        tabs = st.tabs(["Inicio", "Similitudes de Jugadores", "Ratings de Jugadores", "Campograma Plantel"])

        # Pestaña de inicio
        with tabs[0]:
            st.write("Bienvenido a la pestaña de inicio.")

        # Pestaña para similitudes de jugadores
        with tabs[1]:
            mostrar_similitudes(df)

        # Pestaña para los ratings de jugadores
        with tabs[2]:
            mostrar_ratings(df)

        # Pestaña para el campograma del plantel
        with tabs[3]:
            st.write("Campograma de Jugadores")
            
            if "players" not in st.session_state:
                st.session_state.players = {}

            # Formulario para agregar jugadores al campograma
            with st.form(key='player_form'):
                position = st.selectbox("Posición del jugador", options=list(posicion_mapeo.keys()))
                name = st.text_input("Nombre del jugador")
                situation = st.selectbox("Situación del jugador", options=["Jugador de plantilla"] + list(posicion_mapeo.keys()))
                add_player = st.form_submit_button("Agregar jugador")

                if add_player and name:
                    color = situation_colors.get(situation, "white")  # Default to white if situation is not specified
                    if position not in st.session_state.players:
                        st.session_state.players[position] = {"position": positions[position], "names": []}
                    st.session_state.players[position]["names"].append((name.title(), color))
                    st.success(f"Jugador {name.title()} agregado correctamente")
                    st.experimental_rerun()

            # Mostrar campograma
            if st.session_state.players:
                create_campograma(st.session_state.players)

            # Opciones para eliminar jugadores del campograma
            eliminar_jugador = st.selectbox("Selecciona el jugador a eliminar", options=[(pos, name) for pos in st.session_state.players for name, _ in st.session_state.players[pos]["names"]])
            if st.button("Eliminar jugador"):
                if eliminar_jugador:
                    pos, name = eliminar_jugador
                    st.session_state.players[pos]["names"] = [n for n in st.session_state.players[pos]["names"] if n[0] != name]
                    if not st.session_state.players[pos]["names"]:
                        del st.session_state.players[pos]
                    st.success(f"Jugador {name} eliminado correctamente")
                    st.experimental_rerun()

            # Botón para descargar el campograma como imagen
            if st.button("Descargar Campograma"):
                buf = create_campograma(st.session_state.players, save_as_file=True)
                st.download_button(
                    label="Descargar imagen del Campograma",
                    data=buf,
                    file_name="campograma.png",
                    mime="image/png"
                )

# Ejecutar la aplicación
if __name__ == "__main__":
    main()
