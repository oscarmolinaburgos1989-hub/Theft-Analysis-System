import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Sistema de análisis de robos",
    layout="wide"
)

st.title("📊 Sistema de análisis de robos")
st.write("Sistema de análisis e impacto de costo real por robos")

st.markdown("---")

st.subheader("📁 Cargar archivo Excel")
archivo = st.file_uploader(
    "Sube un archivo Excel (.xlsx)",
    type=["xlsx"]
)

if archivo is not None:
    df = pd.read_excel(archivo)

    st.success("Archivo cargado correctamente")

    st.subheader("📋 Datos")
    st.dataframe(df)

    if "Costo" in df.columns:
        st.subheader("💰 Impacto económico")
        total = df["Costo"].sum()
        st.metric("Costo total de robos", f"${total:,.0f}")
