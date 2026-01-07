import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(
    page_title="Sistema de Impacto de Robos en Obra",
    layout="centered"
)

st.title("SISTEMA DE IMPACTO DE ROBOS EN OBRA")
st.write("Modelo corporativo de impacto económico real (versión web)")

st.markdown("---")

# =============================
# 1. CONFIGURACION CORPORATIVA
# =============================

TASA_COSTO_CAPITAL = 0.10
PAGO_FINAL = 0.20
COSTO_DIARIO_OBRA = 2_500_000
VALOR_VIVIENDA = 71_000_000

LEAD_TIMES = {
    "Instalaciones críticas (cobre, cañerías)": 12,
    "Equipamiento eléctrico / sanitario": 15,
    "Herramientas y equipos menores": 5,
    "Maquinaria y equipos mayores": 20,
    "Materiales de obra gruesa": 7,
    "Materiales de terminaciones": 20,
    "Elementos de seguridad / cierres": 10,
    "Tecnología / equipos no obra": 3,
    "Otros": 10
}

BUFFERS = {
    "Obra gruesa": 4,
    "Instalaciones": 2,
    "Terminaciones": 1,
    "Etapa final": 0
}

# =============================
# 2. FORMULARIO (IGUAL A CMD)
# =============================

with st.form("impacto_robo_cmd"):
    st.subheader("Ingreso de datos del robo")

    material = st.selectbox(
        "Tipo de material robado",
        list(LEAD_TIMES.keys())
    )

    etapa = st.selectbox(
        "Etapa de la obra",
        list(BUFFERS.keys())
    )

    costo_robado = st.number_input(
        "Costo directo de lo robado ($)",
        min_value=0,
        step=100_000
    )

    unidades_afectadas = st.number_input(
        "Cantidad de viviendas afectadas (0 si no aplica)",
        min_value=0,
        step=1
    )

    calcular = st.form_submit_button("Calcular impacto real")

# =============================
# 3. CALCULOS (MISMO CMD)
# =============================

if calcular:
    st.success("✅ Cálculo ejecutado correctamente")

    lead_time = LEAD_TIMES[material]
    buffer = BUFFERS[etapa]

    atraso_neto = max(0, lead_time - buffer)
    costo_atraso = atraso_neto * COSTO_DIARIO_OBRA

    if unidades_afectadas > 0:
        ventas = unidades_afectadas * VALOR_VIVIENDA
        costo_comercial = ventas * (TASA_COSTO_CAPITAL / 365) * atraso_neto
    else:
        costo_comercial = 0

    flujo_retrasado = unidades_afectadas * VALOR_VIVIENDA * PAGO_FINAL
    costo_financiero = flujo_retrasado * (TASA_COSTO_CAPITAL / 365) * atraso_neto

    impacto_total = costo_robado + costo_atraso + costo_comercial + costo_financiero

    st.markdown("## 📊 Resultado del impacto real")

    col1, col2 = st.columns(2)

    with col1:
        st.metric("💸 Costo directo del robo", f"${costo_robado:,.0f}")
        st.metric("⏱️ Días reales de atraso", atraso_neto)
        st.metric("🏗️ Costo atraso obra", f"${costo_atraso:,.0f}")

    with col2:
        st.metric("📉 Costo comercial", f"${costo_comercial:,.0f}")
        st.metric("🏦 Costo financiero", f"${costo_financiero:,.0f}")

    st.markdown("---")
    st.metric("🔥 IMPACTO TOTAL REAL", f"${impacto_total:,.0f}")
