import streamlit as st
from datetime import date

st.set_page_config(
    page_title="Sistema de análisis de robos",
    layout="centered"
)

st.title("📊 Sistema de análisis de robos")
st.write("Ingresa los datos del robo y obtén el detalle automáticamente")

st.markdown("---")

with st.form("form_robo"):
    fecha = st.date_input("📅 Fecha del robo", value=date.today())
    lugar = st.text_input("🏪 Lugar / Sucursal")
    producto = st.text_input("📦 Producto robado")
    cantidad = st.number_input("🔢 Cantidad robada", min_value=1, step=1)
    costo_unitario = st.number_input("💲 Costo unitario", min_value=0.0, step=100.0)

    calcular = st.form_submit_button("📈 Calcular impacto")

if calcular:
    total = cantidad * costo_unitario

    st.success("Cálculo realizado correctamente")

    st.subheader("🧾 Detalle del robo")
    st.write(f"**Fecha:** {fecha}")
    st.write(f"**Lugar:** {lugar}")
    st.write(f"**Producto:** {producto}")
    st.write(f"**Cantidad robada:** {cantidad}")
    st.write(f"**Costo unitario:** ${costo_unitario:,.0f}")

    st.markdown("---")
    st.metric("💰 Costo total del robo", f"${total:,.0f}")

