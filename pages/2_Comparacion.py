import streamlit as st
import pandas as pd

# Diccionario ajustado con métricas por posición
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
    'Lateral': ["Matches played", "Minutes played", "Successful attacking actions per 90", "Successful defensive actions per 90", 
                "Accelerations per 90", "Progressive runs per 90", "Crosses to goalie box per 90", "Aerial duels won, %", 
                "Offensive duels won, %", "Defensive duels won, %", "Defensive duels per 90", "Duels won, %", 
                "Interceptions per 90", "Passes per 90", "Forward passes per 90", "Accurate passes to penalty area, %", 
                "Received passes per 90", "Accurate passes to final third, %", "Accurate through passes, %", 
                "Accurate forward passes, %", "Accurate progressive passes, %", "Third assists per 90", "xA per 90"],
    'Mediocampista': ["Matches played", "Minutes played", "Assists per 90", "xA per 90", "Offensive duels won, %", 
                      "Aerial duels won, %", "Defensive duels won, %", "Interceptions per 90", "Received passes per 90", 
                      "Accurate short / medium passes, %", "Accurate passes to final third, %", 
                      "Accurate long passes, %", "Accurate progressive passes, %", "Successful dribbles, %", 
                      "xG per 90", "Goals per 90"],
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

# Función para obtener los datos
def get_data():
    if 'data' in st.session_state:
        return st.session_state['data']
    return None

# Función principal de comparación
def comparacion():
    st.title("Comparación de Jugadores")
    
    # Obtener los datos cargados desde session_state
    df = get_data()
    
    if df is None or df.empty:
        st.warning("No hay datos cargados. Por favor, carga los datos en la página principal.")
        return

    # Crear un identificador único combinando "Full name" y "Team" y asignarlo a la nueva columna "Player_ID"
    df['Player_ID'] = df['Full name'] + " (" + df['Team'] + ")"
    
    # Seleccionar los jugadores para la comparación usando el ID único
    jugadores_disponibles = df['Player_ID'].unique()
    jugadores_seleccionados = st.multiselect("Selecciona los jugadores para comparar", jugadores_disponibles)

    # Selección de posición para mostrar métricas específicas
    posiciones = list(metrics_by_position.keys())
    posicion_seleccionada = st.selectbox("Selecciona la posición para mostrar las métricas específicas", posiciones)

    if jugadores_seleccionados and posicion_seleccionada:
        # Obtener métricas automáticas basadas en la posición seleccionada
        metricas_seleccionadas = metrics_by_position[posicion_seleccionada]

        # Filtrar los jugadores seleccionados
        df_comparacion = df[df['Player_ID'].isin(jugadores_seleccionados)].fillna(0)

        # Crear tabla HTML para mostrar métricas
        table_html = """
        <style>
            table {
                width: 100%;
                border-collapse: collapse;
                text-align: center;
            }
            th, td {
                padding: 8px;
                text-align: center;
            }
            th {
                background-color: #f2f2f2;
            }
            .highlight {
                background-color: #ffeb9c; /* Amarillo claro */
            }
        </style>
        <table border='1'>
        <thead>
        <tr><th>Métrica</th>
        """

        # Crear cabecera de jugadores (usando "Player_ID")
        for jugador in df_comparacion['Player_ID'].unique():
            table_html += f"<th>{jugador}</th>"
        table_html += "</tr></thead><tbody>"
        
        # Agregar las métricas como filas
        for metrica in metricas_seleccionadas:
            # Crear una fila para cada métrica
            table_html += f"<tr><td>{metrica}</td>"
            max_valores = {}
            
            # Obtener los valores de cada jugador
            for jugador in df_comparacion['Player_ID'].unique():
                valor = ""
                df_jugador = df_comparacion[df_comparacion['Player_ID'] == jugador]
                
                for index, row in df_jugador.iterrows():
                    valor += f"{row[metrica]}<br>"
                
                # Si no hay valor, mostrar "No data"
                if not valor:
                    valor = "No data"
                
                # Guardamos el valor para encontrar el máximo
                try:
                    max_valores[jugador] = float(valor.split("<br>")[0])  # Tomar el primer valor como numérico
                except ValueError:
                    max_valores[jugador] = -1  # Si no es un número, usar un valor bajo para no destacar

                # Agregar la celda correspondiente
                table_html += f"<td>{valor}</td>"
            
            # Determinar el máximo y resaltar la celda correspondiente
            max_valor = max(max_valores.values())
            for jugador in max_valores.keys():
                if max_valores[jugador] == max_valor and max_valor >= 0:
                    table_html = table_html.replace(f"<td>{df_comparacion[df_comparacion['Player_ID'] == jugador][metrica].iloc[0]}<br></td>", 
                                                      f"<td class='highlight'>{df_comparacion[df_comparacion['Player_ID'] == jugador][metrica].iloc[0]}<br></td>")
        
            table_html += "</tr>"
        
        # Cerrar tabla
        table_html += "</tbody></table>"
        
        # Mostrar la tabla HTML
        st.markdown(table_html, unsafe_allow_html=True)

if __name__ == "__main__":
    comparacion()
