import streamlit as st
import pandas as pd

# Diccionario ajustado con métricas por posición
metrics_by_position = {
    'Portero': ["Team within selected timeframe", "Matches played", "Minutes played", "Conceded goals per 90", "xG against per 90", 
                "Prevented goals per 90", "Save rate, %", "Exits per 90", "Aerial duels per 90", "Back passes received as GK per 90", 
                "Accurate passes, %", "Accurate forward passes, %", "Accurate long passes, %"],
    'Defensa': ["Team within selected timeframe", "Matches played", "Minutes played", "Accelerations per 90", "Progressive runs per 90", 
                "Aerial duels per 90", "Aerial duels won, %", "Defensive duels won, %", "Duels won, %", "Sliding tackles per 90", 
                "Interceptions per 90", "Key passes per 90", "Short / medium passes per 90", "Forward passes per 90", "Long passes per 90", 
                "Passes per 90", "PAdj Interceptions", "Accurate passes to final third, %", "Accurate forward passes, %", 
                "Accurate back passes, %", "Accurate long passes, %", "Accurate passes, %"],
    'Lateral': ["Team within selected timeframe", "Matches played", "Minutes played", "Successful attacking actions per 90", 
                "Successful defensive actions per 90", "Accelerations per 90", "Progressive runs per 90", "Crosses to goalie box per 90", 
                "Aerial duels won, %", "Offensive duels won, %", "Defensive duels won, %", "Defensive duels per 90", 
                "Duels won, %", "Interceptions per 90", "Passes per 90", "Forward passes per 90", 
                "Accurate passes to penalty area, %", "Received passes per 90", "Accurate passes to final third, %", 
                "Accurate through passes, %", "Accurate forward passes, %", "Accurate progressive passes, %", "Third assists per 90", "xA per 90"],
    'Mediocampista': ["Team within selected timeframe", "Matches played", "Minutes played", "Assists per 90", "xA per 90", "Offensive duels won, %", 
                      "Aerial duels won, %", "Defensive duels won, %", "Interceptions per 90", "Received passes per 90", 
                      "Accurate short / medium passes, %", "Accurate passes to final third, %", 
                      "Accurate long passes, %", "Accurate progressive passes, %", "Successful dribbles, %", "xG per 90", "Goals per 90"],
    'Extremos': ["Team within selected timeframe", "Matches played", "Minutes played", "xG per 90", "Goals per 90", "Assists per 90", 
                 "xA per 90", "Received passes per 90", "Accurate crosses, %", "Accurate through passes, %", 
                 "Accurate progressive passes, %", "Crosses to goalie box per 90", "Accurate passes to penalty area, %", 
                 "Offensive duels won, %", "Defensive duels won, %", "Interceptions per 90", "Successful dribbles, %"],
    'Delantero': ["Team within selected timeframe", "Matches played", "Minutes played", "Goals per 90", "Head goals per 90", 
                  "Non-penalty goals per 90", "Goal conversion, %", "xG per 90", "xA per 90", "Assists per 90", 
                  "Key passes per 90", "Passes per 90", "Passes to penalty area per 90", "Passes to final third per 90", 
                  "Accurate passes, %", "Accurate passes to final third, %", "Aerial duels won, %", "Duels won, %", 
                  "Shots per 90", "Shots on target, %", "Touches in box per 90"]
}

# Filtrar las métricas "per 90" para ser promediadas automáticamente
def get_metrics_to_avg(metricas):
    return [m for m in metricas if "per 90" in m]

# Función para obtener los datos cargados desde session_state
def get_data():
    return st.session_state.data if 'data' in st.session_state else None

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

        # Filtrar los jugadores seleccionados
        df_comparacion = df[df['Full name'].isin(jugadores_seleccionados)].fillna(0)

        # Definir las métricas a promediar y a sumar
        metrics_to_avg = get_metrics_to_avg(metricas_seleccionadas)
        metrics_to_sum = [m for m in metricas_seleccionadas if m not in metrics_to_avg]

        # Agrupar por jugador y realizar las operaciones adecuadas
        df_agrupado = df_comparacion.groupby('Full name').agg({
            **{m: 'mean' for m in metrics_to_avg if m in df_comparacion.columns},  # Promediar las métricas "per 90"
            **{m: 'sum' for m in metrics_to_sum if m in df_comparacion.columns},   # Sumar las métricas acumulativas
            "Team within selected timeframe": 'last'  # Mostrar el último equipo
        }).reset_index()

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
        for jugador in df_agrupado['Full name']:
            table_html += f"<th>{jugador}</th>"
        table_html += "</tr></thead><tbody>"
        
        # Agregar las métricas como filas
        for metrica in metricas_seleccionadas:
            if metrica in df_agrupado.columns:
                table_html += f"<tr><td>{metrica}</td>"
                if pd.api.types.is_numeric_dtype(df_agrupado[metrica]):
                    max_valor = df_agrupado[metrica].max()  # Encuentra el valor máximo en esta métrica
                    for valor in df_agrupado[metrica]:
                        if valor == max_valor:
                            table_html += f"<td style='background-color: yellow;'>{valor}</td>"
                        else:
                            table_html += f"<td>{valor}</td>"
                else:
                    # No aplicar formato condicional si no es numérico
                    for valor in df_agrupado[metrica]:
                        table_html += f"<td>{valor}</td>"
                table_html += "</tr>"
        
        # Cerrar tabla
        table_html += "</tbody></table>"
        
        # Mostrar la tabla HTML
        st.markdown(table_html, unsafe_allow_html=True)

if __name__ == "__main__":
    comparacion()
