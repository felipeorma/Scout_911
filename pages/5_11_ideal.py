import streamlit as st
from utils import get_data

def ideal():
    st.title("Equipo Ideal")
    
    df = get_data()
    if df is None:
        st.warning("No hay datos cargados. Por favor, carga los datos en la página principal.")
        return

    st.write("Aquí puedes implementar un sistema para seleccionar el equipo ideal.")
    st.write("Por ejemplo, podrías crear un algoritmo que seleccione los mejores jugadores para cada posición:")

    # Ejemplo simple de selección de equipo ideal
    if 'posición' in df.columns:
        positions = df['posición'].unique()
        ideal_team = []
        for position in positions:
            top_player = df[df['posición'] == position].sort_values('score', ascending=False).head(1)
            ideal_team.append(top_player)
        st.write("Equipo ideal:")
        st.write(pd.concat(ideal_team))

if __name__ == "__main__":
    ideal()