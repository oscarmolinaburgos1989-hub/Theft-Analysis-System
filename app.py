import streamlit as st
import re

# =============================
# CONFIGURACIÓN GENERAL
# =============================
st.set_page_config(
    page_title="Sistema de impacto de robos en obra",
    layout="wide"
)

st.title("📊 Sistema de impacto real de robos en obra")
st.write("Informe técnico detallado de impacto económico, operativo y financiero")
st.markdown("---")

# =============================
# BASE TÉCNICA DE PRECIOS
# =============================
BASE_PRECIOS = {
    "cobre": {"metro": (9000, 12000)},
    "cañeria": {"metro": (9000, 12000)},
    "cable": {"metro": (2500, 6000)},
    "alambre": {"metro": (1500, 3000)},
    "tablero": {"unidad": (180000, 350000)},
    "calefont": {"unidad": (120000, 280000)},
    "herramienta": {"unidad": (30000, 150000)},
    "maquinaria": {"unidad": (800000, 5000000)},
    "reja": {"metro": (40000, 120000)},
    "porton": {"unidad": (600000, 2000000)}
}

def estimar_precio(detalle):
    detalle = detalle.lower()
    unidad = "unidad"
    if "metro" in detalle or "metros" in detalle:
        unidad = "metro"

    for palabra, valores in BASE_PRECIOS.items():
        if re.search(palabra, detalle):
            minimo, maximo = valores[unidad]
            promedio = int((minimo + maximo) / 2)
            return palabra, unidad, minimo, maximo, promedio

    return "referencia genérica", "unidad", 50000, 150000, 100000

# =============================
# CONFIGURACIÓN DEL PROYECTO
# =============================
st.header("1️⃣ Configuración del proyecto")

tipo_proyecto = st.selectbox(
    "Tipo de proyecto",
    ["Conjunto de casas", "Edificio de departamentos", "Obra comercial"]
)

valor_propiedad = st.number_input(
    "Valor promedio por unidad ($)",
    value=71_000_000,
    step=1_000_000
)

costo_dia_obra = st.number_input(
    "Costo diario total de la obra ($)",
    value=2_500_000,
    step=100_000
)

costo_mano_obra_dia = st.number_input(
    "Costo diario mano de obra / contratistas ($)",
    value=1_200_000,
    step=50_000
)

tasa_costo_capital = st.number_input(
    "Costo de capital anual (%)",
    value=10.0
) / 100

pago_final_porcentaje = st.number_input(
    "Pago final retenido (%)",
    value=20.0
) / 100

st.markdown("---")

# =============================
# DATOS DEL ROBO
# =============================
st.header("2️⃣ Detalle del robo")

detalle_material = st.text_area(
    "Detalle específico de lo robado",
    placeholder="Ej: 120 metros cañería cobre 1/2 tipo L"
)

cantidad = st.number_input(
    "Cantidad / unidades robadas",
    min_value=1,
    value=1
)

unidades_afectadas = st.number_input(
    "Viviendas afectadas (0 si no aplica)",
    min_value=0,
    value=0
)

dias_atraso = st.number_input(
    "Días estimados de atraso generados por el robo",
    min_value=0,
    value=10
)

st.markdown("---")

# =============================
# ESTIMACIÓN DE PRECIO
# =============================
st.header("3️⃣ Estimación técnica de precio")

palabra, unidad, p_min, p_max, p_prom = estimar_precio(detalle_material)

st.info(f"""
Referencia técnica detectada: **{palabra}**  
Unidad considerada: **{unidad}**  
Rango estimado mercado: **${p_min:,} – ${p_max:,}**
""")

precio_unitario = st.number_input(
    "Costo unitario estimado ($)",
    value=p_prom,
    step=1000
)

costo_robado = cantidad * precio_unitario

st.markdown("---")

# =============================
# CÁLCULOS DE IMPACTO
# =============================
if st.button("🧮 Calcular impacto detallado"):

    impacto_atraso_obra = dias_atraso * costo_dia_obra
    impacto_mano_obra = dias_atraso * costo_mano_obra_dia

    if unidades_afectadas > 0:
        ventas_afectadas = unidades_afectadas * valor_propiedad
        impacto_comercial = ventas_afectadas * (tasa_costo_capital / 365) * dias_atraso
        flujo_retenido = ventas_afectadas * pago_final_porcentaje
        impacto_financiero = flujo_retenido * (tasa_costo_capital / 365) * dias_atraso
    else:
        ventas_afectadas = 0
        impacto_comercial = 0
        impacto_financiero = 0

    impacto_total = (
        costo_robado +
        impacto_atraso_obra +
        impacto_mano_obra +
        impacto_comercial +
        impacto_financiero
    )

    # =============================
    # INFORME DETALLADO
    # =============================
    st.markdown("## 📑 INFORME TÉCNICO DE IMPACTO")

    st.markdown("### 🔹 1. Descripción del evento")
    st.write(f"""
- Tipo de proyecto: **{tipo_proyecto}**
- Material robado: **{detalle_material}**
- Cantidad: **{cantidad} {unidad}**
- Días de atraso generados: **{dias_atraso}**
""")

    st.markdown("### 🔹 2. Impacto directo")
    st.write(f"""
- Precio unitario estimado: **${precio_unitario:,.0f}**
- Costo directo del robo: **${costo_robado:,.0f}**
""")

    st.markdown("### 🔹 3. Impacto operativo (obra)")
    st.write(f"""
- Costo diario de obra: **${costo_dia_obra:,.0f}**
- Días de atraso: **{dias_atraso}**
- Impacto por atraso de obra: **${impacto_atraso_obra:,.0f}**
""")

    st.markdown("### 🔹 4. Impacto en mano de obra")
    st.write(f"""
- Costo diario mano de obra / contratistas: **${costo_mano_obra_dia:,.0f}**
- Impacto total mano de obra: **${impacto_mano_obra:,.0f}**
""")

    st.markdown("### 🔹 5. Impacto comercial")
    st.write(f"""
- Unidades afectadas: **{unidades_afectadas}**
- Ventas afectadas estimadas: **${ventas_afectadas:,.0f}**
- Impacto financiero por retraso comercial: **${impacto_comercial:,.0f}**
""")

    st.markdown("### 🔹 6. Impacto financiero")
    st.write(f"""
- Pago final retenido: **{pago_final_porcentaje*100:.1f}%**
- Capital inmovilizado: **${ventas_afectadas * pago_final_porcentaje:,.0f}**
- Costo financiero del atraso: **${impacto_financiero:,.0f}**
""")

    st.markdown("---")
    st.metric("💥 IMPACTO ECONÓMICO TOTAL REAL", f"${impacto_total:,.0f}")

    st.markdown("---")
    st.info(
        "Este informe corresponde a una estimación técnica basada en parámetros "
        "económicos definidos por el usuario y referencias públicas de mercado. "
        "No constituye cotización formal."
    )

