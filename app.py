import streamlit as st
import pandas as pd

# =============================
# CONFIGURACIÓN DE LA PÁGINA
# =============================
st.set_page_config(
    page_title="Sistema de análisis de robos en obra",
    layout="wide"
)

st.title("📊 Sistema de análisis de robos en obra")
st.write("Modelo corporativo de impacto económico real (versión web)")
st.markdown("---")

# =============================
# PARÁMETROS BASE
# =============================
LEAD_TIMES = {
    "Instalaciones críticas": 12,
    "Equipamiento eléctrico / sanitario": 15,
    "Herramientas": 5,
    "Maquinaria": 20,
    "Obra gruesa": 7,
    "Terminaciones": 20,
    "Seguridad": 10,
    "Tecnología": 3,
    "Otros": 10
}

BUFFERS = {
    "Obra gruesa": 4,
    "Instalaciones": 2,
    "Terminaciones": 1,
    "Etapa final": 0
}

# =============================
# 1. CONFIGURACIÓN DEL PROYECTO
# =============================
st.markdown("## ⚙️ Configuración del proyecto")

tipo_proyecto = st.selectbox(
    "Tipo de proyecto",
    ["Conjunto de casas", "Edificio departamentos", "Obra comercial"]
)

valor_propiedad = st.number_input(
    "Valor promedio por unidad ($)",
    min_value=10000000,
    value=71000000,
    step=1000000
)

costo_dia_obra = st.number_input(
    "Costo diario de obra ($)",
    min_value=500000,
    value=2500000,
    step=100000
)

costo_mano_obra_dia = st.number_input(
    "Costo diario mano de obra / contratistas ($)",
    min_value=300000,
    value=1200000,
    step=50000
)

tasa_costo_capital = st.number_input(
    "Costo de capital anual (%)",
    min_value=1.0,
    value=10.0,
    step=0.5
) / 100

pago_final_porcentaje = st.number_input(
    "Pago final retenido (%)",
    min_value=0.0,
    value=20.0,
    step=1.0
) / 100

st.markdown("---")

# =============================
# 2. INGRESO DE DATOS DEL ROBO
# =============================
st.markdown("## 🧾 Ingreso de datos del robo")

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
    value=2000000,
    step=100000
)

unidades_afectadas = st.number_input(
    "Cantidad de viviendas afectadas (0 si no aplica)",
    min_value=0,
    value=0,
    step=1
)

calcular = st.button("🧮 Calcular impacto real")

# =============================
# 3. CÁLCULO DEL IMPACTO
# =============================
if calcular:
    lead_time = LEAD_TIMES[material]
    buffer = BUFFERS[etapa]

    atraso_neto = max(0, lead_time - buffer)

    # Impacto obra
    costo_atraso_obra = atraso_neto * costo_dia_obra

    # Impacto mano de obra
    costo_mano_obra = atraso_neto * costo_mano_obra_dia

    # Impacto comercial
    if unidades_afectadas > 0:
        ventas = unidades_afectadas * valor_propiedad
        costo_comercial = ventas * (tasa_costo_capital / 365) * atraso_neto
    else:
        costo_comercial = 0

    # Impacto financiero
    flujo_retenido = unidades_afectadas * valor_propiedad * pago_final_porcentaje
    costo_financiero = flujo_retenido * (tasa_costo_capital / 365) * atraso_neto

    impacto_total = (
        costo_robado
        + costo_atraso_obra
        + costo_mano_obra
        + costo_comercial
        + costo_financiero
    )

    # =============================
    # 4. RESULTADOS
    # =============================
    st.markdown("---")
    st.markdown("## 📊 Resultado del impacto económico real")

    st.markdown(f"""
    **Tipo de proyecto:** {tipo_proyecto}  
    **Material robado:** {material}  
    **Etapa de la obra:** {etapa}  
    **Días reales de atraso:** {atraso_neto}
    """)

    col1, col2 = st.columns(2)

    with col1:
        st.metric("💸 Costo directo del robo", f"${costo_robado:,.0f}")
        st.metric("🏗️ Impacto por atraso de obra", f"${costo_atraso_obra:,.0f}")
        st.metric("👷 Mano de obra / contratistas", f"${costo_mano_obra:,.0f}")

    with col2:
        st.metric("📉 Impacto comercial", f"${costo_comercial:,.0f}")
        st.metric("🏦 Impacto financiero", f"${costo_financiero:,.0f}")

    st.markdown("---")
    st.metric("🔥 IMPACTO TOTAL REAL DEL ROBO", f"${impacto_total:,.0f}")
