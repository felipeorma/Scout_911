import streamlit as st
import pandas as pd

# Diccionario ajustado con métricas por posición y su tipo (promedio o acumulativo)
metrics_by_position = {
    'Portero': {
        "Team within selected timeframe": "last",  # Mostrar el último equipo
        "Matches played": "sum", 
        "Minutes played": "sum", 
        "Conceded goals per 90": "avg", 
        "xG against per 90": "avg", 
        "Prevented goals per 90": "avg", 
        "Save rate, %": "avg", 
        "Exits per 90": "avg", 
        "Aerial duels per 90": "avg", 
        "Back passes received as GK per 90": "avg", 
        "Accurate passes, %": "avg", 
        "Accurate forward passes, %": "avg", 
        "Accurate long passes, %": "avg"
    },
    'Defensa': {
        "Team within selected timeframe": "last",  # Mostrar el último equipo
        "Matches played": "sum", 
        "Minutes played": "sum", 
        "Accelerations per 90": "avg", 
        "Progressive runs per 90": "avg", 
        "Aerial duels per 90": "avg", 
        "Aerial duels won, %": "avg", 
        "Defensive duels won, %": "avg", 
        "Duels won, %": "avg", 
        "Sliding tackles per 90": "avg", 
        "Interceptions per 90": "avg", 
        "Key passes per 90": "avg", 
        "Short / medium passes per 90": "avg", 
        "Forward passes per 90": "avg", 
        "Long passes per 90": "avg", 
        "Passes per 90": "avg", 
        "PAdj Interceptions": "avg", 
        "Accurate passes to final third, %": "avg", 
        "Accurate forward passes, %": "avg", 
        "Accurate back passes, %": "avg", 
        "Accurate long passes, %": "avg", 
        "Accurate passes, %": "avg"
    },
    'Defensa': {
        "Team within selected timeframe": "ignore", 
        "Matches played": "sum", 
        "Minutes played": "sum", 
        "Accelerations per 90": "avg", 
        "Progressive runs per 90": "avg", 
        "Aerial duels per 90": "avg", 
        "Aerial duels won, %": "avg", 
        "Defensive duels won, %": "avg", 
        "Duels won, %": "avg", 
        "Sliding tackles per 90": "avg", 
        "Interceptions per 90": "avg", 
        "Key passes per 90": "avg", 
        "Short / medium passes per 90": "avg", 
        "Forward passes per 90": "avg", 
        "Long passes per 90": "avg", 
        "Passes per 90": "avg", 
        "PAdj Interceptions": "avg", 
        "Accurate passes to final third, %": "avg", 
        "Accurate forward passes, %": "avg", 
        "Accurate back passes, %": "avg", 
        "Accurate long passes, %": "avg", 
        "Accurate passes, %": "avg"
    },
    'Lateral': {
        "Team within selected timeframe": "ignore", 
        "Matches played": "sum", 
        "Minutes played": "sum", 
        "Successful attacking actions per 90": "avg", 
        "Successful defensive actions per 90": "avg", 
        "Accelerations per 90": "avg", 
        "Progressive runs per 90": "avg", 
        "Crosses to goalie box per 90": "avg", 
        "Aerial duels won, %": "avg", 
        "Offensive duels won, %": "avg", 
        "Defensive duels won, %": "avg", 
        "Defensive duels per 90": "avg", 
        "Duels won, %": "avg", 
        "Interceptions per 90": "avg", 
        "Passes per 90": "avg", 
        "Forward passes per 90": "avg", 
        "Accurate passes to penalty area, %": "avg", 
        "Received passes per 90": "avg", 
        "Accurate passes to final third, %": "avg", 
        "Accurate through passes, %": "avg", 
        "Accurate forward passes, %": "avg", 
        "Accurate progressive passes, %": "avg", 
        "Third assists per 90": "avg", 
        "xA per 90": "avg"
    },
    'Mediocampista': {
        "Team within selected timeframe": "ignore", 
        "Matches played": "sum", 
        "Minutes played": "sum", 
        "Assists per 90": "avg", 
        "xA per 90": "avg", 
        "Offensive duels won, %": "avg", 
        "Aerial duels won, %": "avg", 
        "Defensive duels won, %": "avg", 
        "Interceptions per 90": "avg", 
        "Received passes per 90": "avg", 
        "Accurate short / medium passes, %": "avg", 
        "Accurate passes to final third, %": "avg", 
        "Accurate long passes, %": "avg", 
        "Accurate progressive passes, %": "avg", 
        "Successful dribbles, %": "avg", 
        "xG per 90": "avg", 
        "Goals per 90": "avg"
    },
    'Extremos': {
        "Team within selected timeframe": "ignore", 
        "Matches played": "sum", 
        "Minutes played": "sum", 
        "xG per 90": "avg", 
        "Goals per 90": "avg", 
        "Assists per 90": "avg", 
        "xA per 90": "avg", 
        "Received passes per 90": "avg", 
        "Accurate crosses, %": "avg", 
        "Accurate through passes, %": "avg", 
        "Accurate progressive passes, %": "avg", 
        "Crosses to goalie box per 90": "avg", 
        "Accurate passes to penalty area, %": "avg", 
        "Offensive duels won, %": "avg", 
        "Defensive duels won, %": "avg", 
        "Interceptions per 90": "avg", 
        "Successful dribbles, %": "avg"
    },
    'Delantero': {
        "Team within selected timeframe": "ignore", 
        "Matches played": "sum", 
        "Minutes played": "sum", 
        "Goals per 90": "avg", 
        "Head goals per 90": "avg", 
        "Non-penalty goals per 90": "avg", 
        "Goal conversion, %": "avg", 
        "xG per 90": "avg", 
        "xA per 90": "avg", 
        "Assists per 90": "avg", 
        "Key passes per 90": "avg", 
        "Passes per 90": "avg", 
        "Passes to penalty area per 90": "avg", 
        "Passes to final third per 90": "avg", 
        "Accurate passes, %": "avg", 
        "Accurate passes to final third, %": "avg", 
        "Aerial duels won, %": "avg", 
        "Duels won, %": "avg", 
        "Shots per 90": "avg", 
        "Shots on target, %": "avg", 
        "Touches in box per 90": "avg"
    }
}

# Función para obtener los datos cargados desde session_state
def get_data():
    return st.session_state.data if 'data' in st.session_state else None

# Función para promediar, sumar métricas o mostrar el último equipo
def calcular_metricas_ajustadas(df, metricas):
    # Agrupar por jugador
    jugadores = df['Full name'].unique()
    datos_ajustados = []

    for jugador in jugadores:
        jugador_df = df[df['Full name'] == jugador]
        resultado_jugador = {'Full name': jugador}
        
        # Para cada métrica, aplicar la operación correspondiente (suma, promedio o último equipo)
        for metrica, operacion in metricas.items():
            if metrica in jugador_df.columns:
                if operacion == 'avg':
                    resultado_jugador[metrica] = jugador_df[metrica].mean()
                elif operacion == 'sum':
                    resultado_jugador[metrica] = jugador_df[metrica].sum()
                elif operacion == 'last':
                    resultado_jugador[metrica] = jugador_df[metrica].iloc[-1]  # Obtener el último valor registrado
            else:
                st.warning(f"Métrica {metrica} no encontrada en los datos para {jugador}. Omitiendo...")
        
        datos_ajustados.append(resultado_jugador)

    return pd.DataFrame(datos_ajustados)

# Función principal de comparación
def comparacion():
    st.title("Comparación de Jugadores")
    
    # Obtener los datos cargados desde session_state
    df = get_data()
    
    if df is None or df.empty:
        st.warning("No hay datos cargados. Por favor, carga los datos en la página principal.")
        return
    
    # Seleccionar los jugadores para la comparación
    jugadores_disponibles = df['Full name'].unique()
    jugadores_seleccionados = st.multiselect("Selecciona los jugadores para comparar", jugadores_disponibles)

    # Selección de posición para mostrar métricas específicas
    posiciones = list(metrics_by_position.keys())
    posicion_seleccionada = st.selectbox("Selecciona la posición para mostrar las métricas específicas", posiciones)

    if jugadores_seleccionados and posicion_seleccionada:
        # Obtener métricas automáticas basadas en la posición seleccionada
        metricas_seleccionadas = metrics_by_position[posicion_seleccionada]

        # Verificar si las columnas existen en los datos
        columnas_existentes = ['Full name'] + [m for m in metricas_seleccionadas if m in df.columns]
        
        if len(columnas_existentes) <= 1:
            st.warning("No se encontraron métricas disponibles para la posición seleccionada.")
            return
        
        # Filtrar los jugadores seleccionados y las métricas seleccionadas
        df_comparacion = df[df['Full name'].isin(jugadores_seleccionados)][columnas_existentes]

        # Aplicar promedios, sumas o mostrar el último equipo según corresponda
        df_ajustado = calcular_metricas_ajustadas(df_comparacion, metricas_seleccionadas)

        # Crear tabla HTML para transponer
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
        </style>
        <table border='1'>
        <thead>
        <tr><th>Métrica</th>
        """

        # Crear cabecera de jugadores
        for jugador in df_ajustado['Full name']:
            table_html += f"<th>{jugador}</th>"
        table_html += "</tr></thead><tbody>"
        
        # Agregar las métricas como filas
        for metrica in metricas_seleccionadas:
            if metrica in df_ajustado.columns:  # Verificar si la métrica está en el DataFrame ajustado
                table_html += f"<tr><td>{metrica}</td>"
                if pd.api.types.is_numeric_dtype(df_ajustado[metrica]):
                    max_valor = df_ajustado[metrica].max()  # Encuentra el valor máximo en esta métrica
                    for valor in df_ajustado[metrica]:
                        if valor == max_valor:
                            table_html += f"<td style='background-color: yellow;'>{valor}</td>"
                        else:
                            table_html += f"<td>{valor}</td>"
                else:
                    # No aplicar formato condicional si no es numérico
                    for valor in df_ajustado[metrica]:
                        table_html += f"<td>{valor}</td>"
                table_html += "</tr>"
        
        # Cerrar tabla
        table_html += "</tbody></table>"
        
        # Mostrar la tabla HTML
        st.markdown(table_html, unsafe_allow_html=True)

if __name__ == "__main__":
    comparacion()
