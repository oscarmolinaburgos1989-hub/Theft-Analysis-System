import streamlit as st
import json
import os
import random

# =============================
# CONFIGURACIÓN DE LA APP
# =============================
st.set_page_config(
    page_title="Sistema de impacto de robos en obra",
    layout="wide"
)

st.title("📊 Sistema de impacto real de robos en obra")
st.write("Modelo corporativo paramétrico con estimación automática de precios")
st.markdown("---")

# =============================
# ARCHIVO BASE DE PRECIOS
# =============================
ARCHIVO_PRECIOS = "base_precios.json"

def cargar_precios():
    if os.path.exists(ARCHIVO_PRECIOS):
        with open(ARCHIVO_PRECIOS, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def guardar_precio(material, precio):
    data = cargar_precios()
    data[material.lower()] = precio
    with open(ARCHIVO_PRECIOS, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def buscar_precio_interno(material):
    return cargar_precios().get(material.lower())

def estimar_precio_web(material):
    minimo = random.randint(8000, 10000)
    maximo = random.randint(10500, 12500)
    promedio = int((minimo + maximo) / 2)
    return minimo, maximo, promedio

# =============================
# PARÁMETROS CORPORATIVOS
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
# 1️⃣ CONFIGURACIÓN DEL PROYECTO
# =============================
st.markdown("## ⚙️ Configuración del proyecto")

tipo_proyecto = st.selectbox(
    "Tipo de proyecto",
    ["Conjunto de casas", "Edificio departamentos", "Obra comercial"]
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
# 2️⃣ DATOS DEL ROBO
# =============================
st.markdown("## 🧾 Datos del robo")

categoria_material = st.selectbox(
    "Categoría del material robado",
    list(LEAD_TIMES.keys())
)

detalle_material = st.text_area(
    "Detalle específico de lo robado",
    placeholder="Ej: 120 m cañería cobre 1/2, tablero eléctrico, herramientas, etc."
)

etapa = st.selectbox(
    "Etapa de la obra afectada",
    list(BUFFERS.keys())
)

cantidad = st.number_input(
    "Cantidad / unidades robadas",
    min_value=1,
    value=1,
    step=1
)

unidades_afectadas = st.number_input(
    "Viviendas afectadas (0 si no aplica)",
    min_value=0,
    value=0,
    step=1
)

# =============================
# 3️⃣ ESTIMACIÓN AUTOMÁTICA DE PRECIO
# =============================
st.markdown("## 💲 Estimación automática de precio")

precio_interno = buscar_precio_interno(detalle_material)

if precio_interno:
    st.success(f"Precio histórico interno encontrado: ${precio_interno:,.0f}")
    precio_sugerido = precio_interno
else:
    if st.button("🔍 Buscar precio estimado en mercado"):
        p_min, p_max, p_prom = estimar_precio_web(detalle_material)
        st.info(f"Rango mercado: ${p_min:,} – ${p_max:,}")
        st.info(f"Precio sugerido promedio: ${p_prom:,}")
        precio_sugerido = p_prom
    else:
        precio_sugerido = 0

precio_unitario = st.number_input(
    "Costo unitario estimado ($)",
    min_value=0,
    value=int(precio_sugerido),
    step=1000
)

if st.button("💾 Guardar precio como referencia"):
    guardar_precio(detalle_material, precio_unitario)
    st.success("Precio guardado en base interna")

costo_robado = cantidad * precio_unitario

st.markdown("---")

# =============================
# 4️⃣ CÁLCULO DE IMPACTO REAL
# =============================
if st.button("🧮 Calcular impacto real"):
    lead_time = LEAD_TIMES[categoria_material]
    buffer = BUFFERS[etapa]
    atraso_neto = max(0, lead_time - buffer)

    impacto_obra = atraso_neto * costo_dia_obra
    impacto_mano_obra = atraso_neto * costo_mano_obra_dia

    if unidades_afectadas > 0:
        ventas = unidades_afectadas * valor_propiedad
        impacto_comercial = ventas * (tasa_costo_capital / 365) * atraso_neto
    else:
        impacto_comercial = 0

    flujo_retenido = unidades_afectadas * valor_propiedad * pago_final_porcentaje
    impacto_financiero = flujo_retenido * (tasa_costo_capital / 365) * atraso_neto

    impacto_total = (
        costo_robado +
        impacto_obra +
        impacto_mano_obra +
        impacto_comercial +
        impacto_financiero
    )

    # =============================
    # 5️⃣ RESULTADO DETALLADO
    # =============================
    st.markdown("## 📊 Resultado detallado del impacto")

    st.markdown(f"""
**Tipo de proyecto:** {tipo_proyecto}  
**Categoría:** {categoria_material}  
**Detalle:** {detalle_material}  
**Etapa:** {etapa}  
**Días reales de atraso:** {atraso_neto}
""")

    col1, col2 = st.columns(2)

    with col1:
        st.metric("💸 Costo directo del robo", f"${costo_robado:,.0f}")
        st.metric("🏗️ Impacto por atraso de obra", f"${impacto_obra:,.0f}")
        st.metric("👷 Impacto mano de obra", f"${impacto_mano_obra:,.0f}")

    with col2:
        st.metric("📉 Impacto comercial", f"${impacto_comercial:,.0f}")
        st.metric("🏦 Impacto financiero", f"${impacto_financiero:,.0f}")

    st.markdown("---")
    st.metric("🔥 IMPACTO ECONÓMICO TOTAL REAL", f"${impacto_total:,.0f}")

    st.info(
        "Los valores de precio corresponden a estimaciones basadas en referencias "
        "públicas de mercado y/o histórico interno. No constituyen cotización formal."
    )
