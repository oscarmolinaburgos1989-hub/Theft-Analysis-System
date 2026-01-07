import streamlit as st
from datetime import date

st.set_page_config(
    page_title="Sistema de impacto real por robos",
    layout="centered"
)

st.title("📊 Sistema de impacto real por robos")
st.write("Evaluación económica, operativa y comercial del impacto de robos")

st.markdown("---")

with st.form("impacto_robo"):
    st.subheader("🧾 Datos generales del evento")

    fecha = st.date_input("📅 Fecha del robo", value=date.today())
    lugar = st.text_input("🏗 Obra / Proyecto / Sucursal")
    tipo_robo = st.selectbox(
        "🚨 Tipo de evento",
        ["Robo en obra", "Robo en instalaciones", "Hurto", "Asalto"]
    )

    st.markdown("---")
    st.subheader("💰 Impacto directo")

    valor_robado = st.number_input(
        "Valor del bien robado ($)",
        min_value=0.0,
        step=100000.0
    )

    st.markdown("---")
    st.subheader("⏱ Impacto por retraso en construcción")

    dias_retraso = st.number_input("Días de retraso generados", min_value=0, step=1)
    costo_diario_obra = st.number_input(
        "Costo diario de la obra ($)",
        min_value=0.0,
        step=100000.0
    )

    st.markdown("---")
    st.subheader("👷 Impacto en mano de obra")

    trabajadores_afectados = st.number_input(
        "Trabajadores detenidos",
        min_value=0,
        step=1
    )
    costo_diario_trabajador = st.number_input(
        "Costo diario por trabajador ($)",
        min_value=0.0,
        step=10000.0
    )

    st.markdown("---")
    st.subheader("📉 Impacto comercial")

    perdida_comercial = st.number_input(
        "Pérdida comercial estimada ($)",
        min_value=0.0,
        step=100000.0
    )
    multas = st.number_input(
        "Multas / penalizaciones ($)",
        min_value=0.0,
        step=100000.0
    )

    st.markdown("---")
    st.subheader("🧾 Impacto administrativo")

    horas_admin = st.number_input(
        "Horas administrativas perdidas",
        min_value=0,
        step=1
    )
    costo_hora_admin = st.number_input(
        "Costo hora administrativa ($)",
        min_value=0.0,
        step=5000.0
    )

    generar = st.form_submit_button("📊 Calcular impacto real")

if generar:
    impacto_obra = dias_retraso * costo_diario_obra
    impacto_mano_obra = trabajadores_afectados * costo_diario_trabajador * dias_retraso
    impacto_a_

