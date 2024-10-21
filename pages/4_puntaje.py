import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import io

# Función para agregar jugadores en el campograma
def add_players(ax, players):
    for player, details in players.items():
        for idx, (name, color) in enumerate(details['names']):
            position = (details['position'][0], details['position'][1] - 3 * idx)
            text_color = 'black' if color in ['yellow', 'white', 'orange'] else 'white'
            ax.text(position[0], position[1], name, ha="center", va="center", color=text_color, fontsize=10, bbox=dict(facecolor=color, edgecolor="none", boxstyle="round,pad=0.3"))

# Función para crear el campograma
def create_campograma(players, save_as_file=False):
    fig, ax = plt.subplots(figsize=(15, 8))
    # Dibujar el campo de fútbol
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
    
    # Agregar los jugadores en el campo
    add_players(ax, players)

    # Leyenda de colores
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
        ax.text(105, 60 - i*5, f"{label} ({count})", ha="left", va="center", color=text_color, fontsize=12, bbox=dict(facecolor=color, edgecolor="none", boxstyle="round,pad=0.3"))

    # Configuración del campo
    ax.set_xlim(0, 120)
    ax.set_ylim(0, 65)
    ax.axis('off')

    # Mostrar en Streamlit o guardar como archivo
    if save_as_file:
        buf = io.BytesIO()
        fig.savefig(buf, format='png', dpi=300)
        buf.seek(0)
        return buf
    else:
        st.pyplot(fig)

# Función para tomar los datos desde session_state y crear el campograma
def mostrar_campograma():
    if 'data' in st.session_state and st.session_state.data is not None:
        # Aquí extraemos los jugadores de los datos subidos
        df = st.session_state.data
        
        # Vamos a suponer que tienes columnas como 'nombre', 'posición', 'estado'
        players = {}
        for index, row in df.iterrows():
            posicion = row['posicion']  # Suponiendo que 'posicion' contiene las coordenadas de los jugadores
            nombre = row['nombre']
            estado = row['estado']  # Aquí decides qué color asignar según el estado del jugador (baja, cesión, etc.)
            color = determinar_color(estado)  # Una función que convierta el estado a un color (ejemplo abajo)
            
            if posicion not in players:
                players[posicion] = {'position': (row['x'], row['y']), 'names': []}  # 'x' e 'y' serían las coordenadas
            players[posicion]['names'].append((nombre, color))
        
        # Crear el campograma
        create_campograma(players)
    else:
        st.warning("No se encontraron datos cargados. Por favor, asegúrate de cargar los datos en home.py.")

# Función que asigna un color según el estado del jugador
def determinar_color(estado):
    colores = {
        'baja': 'grey',
        'cesion': 'blue',
        'lesion': 'purple',
        'juvenil': 'yellow',
        'extranjero': 'red',
        'incorporar': 'orange',
        'plantilla': 'white'
    }
    return colores.get(estado.lower(), 'white')

# Llamar a la función mostrar_campograma para mostrar el gráfico en Streamlit
mostrar_campograma()
