import streamlit as st

# =============================
# CONFIGURACIÓN DE LA PÁGINA
# =============================
st.set_page_config(
    page_title="Sistema de impacto de robos en obra",
    layout="wide"
)

st.title("📊 Sistema de impacto real de robos en obra")
st.write("Modelo corporativo paramétrico de impacto económico")
st.markdown("---")

# =============================
# PARÁMETROS BASE (MODELO)
# =============================

LEAD_TIMES = {
    "Instalaciones críticas": 12,
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
# 1. CONFIGURACIÓN ECONÓMICA
# =============================
st.markdown("## ⚙️ Configuración económica del proyecto")

tipo_proyecto = st.selectbox(
    "Tipo de proyecto",
    ["Conjunto de casas", "Edificio de departamentos", "Obra comercial"]
)

valor_propiedad = st.number_input(
    "Valor promedio por unidad ($)",
    min_value=10_000_000,
    value=71_000_000,
    step=1_000_000
)

costo_dia_obra = st.number_input(
    "Costo diario de la obra ($)",
    min_value=500_000,
    value=2_500_000,
    step=100_000
)

costo_mano_obra_dia = st.number_input(
    "Costo diario mano de obra / contratistas ($)",
    min_value=300_000,
    value=1_200_000,
    step=50_000
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
# 2. DATOS DEL ROBO
# =============================
st.markdown("## 🧾 Datos del robo")

material_categoria = st.selectbox(
    "Categoría del material robado",
    list(LEAD_TIMES.keys())
)

detalle_material = st.text_area(
    "Detalle específico de lo robado (descripción libre)",
    placeholder="Ej: 120 metros de cañería de cobre tipo L, 6 calefont, cableado eléctrico tablero principal..."
)

etapa = st.selectbox(
    "Etapa de la obra afectada",
    list(BUFFERS.keys())
)

costo_robado = st.number_input(
    "Costo directo estimado de lo robado ($)",
    min_value=0,
    value=2_000_000,
    step=100_000
)

unidades_afectadas = st.number_input(
    "Cantidad de viviendas afectadas (0 si no aplica)",
    min_value=0,
    value=0,
    step=1
)

calcular = st.button("🧮 Calcular impacto real")

# =============================
# 3. CÁLCULO DE IMPACTO
# =============================
if calcular:
    lead_time = LEAD_TIMES[material_categoria]
    buffer = BUFFERS[etapa]

    atraso_neto = max(0, lead_time - buffer)

    # Impactos
    impacto_atraso_obra = atraso_neto * costo_dia_obra
    impacto_mano_obra = atraso_neto * costo_mano_obra_dia

    if unidades_afectadas > 0:
        ventas = unidades_afectadas * valor_propiedad
        impacto_comercial = ventas * (tasa_costo_capital / 365) * atraso_neto
    else:
        impacto_comercial = 0

    flujo_retenido = unidades_afectadas * valor_propiedad * pago_final_porcentaje
    impacto_financiero = flujo_retenido * (tasa_costo_capital / 365) * atraso_neto

    impacto_total = (
        costo_robado
        + impacto_atraso_obra
        + impacto_mano_obra
        + impacto_comercial
        + impacto_financiero
    )

    # =============================
    # 4. RESULTADOS
    # =============================
    st.markdown("---")
    st.markdown("## 📊 Resultado del impacto económico real")

    st.markdown(f"""
**Tipo de proyecto:** {tipo_proyecto}  
**Categoría del material:** {material_categoria}  
**Detalle de lo robado:** {detalle_material if detalle_material else "No especificado"}  
**Etapa de la obra:** {etapa}  
**Días reales de atraso:** {atraso_neto}
""")

    col1, col2 = st.columns(2)

    with col1:
        st.metric("💸 Costo directo del robo", f"${costo_robado:,.0f}")
        st.metric("🏗️ Impacto por atraso de obra", f"${impacto_atraso_obra:,.0f}")
        st.metric("👷 Impacto mano de obra / contratistas", f"${impacto_mano_obra:,.0f}")

    with col2:
        st.metric("📉 Impacto comercial", f"${impacto_comercial:,.0f}")
        st.metric("🏦 Impacto financiero", f"${impacto_financiero:,.0f}")

    st.markdown("---")
    st.metric("🔥 IMPACTO ECONÓMICO TOTAL REAL", f"${impacto_total:,.0f}")

    st.info(
        "El impacto total considera efectos directos, operacionales, "
        "comerciales y financieros derivados del robo, según parámetros "
        "económicos definidos para el proyecto."
    )
