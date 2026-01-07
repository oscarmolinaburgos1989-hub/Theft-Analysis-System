import streamlit as st
import json
import os
import re

# =============================
# CONFIGURACIÓN APP
# =============================
st.set_page_config(
    page_title="Sistema de impacto de robos en obra",
    layout="wide"
)

st.title("📊 Sistema de impacto real de robos en obra")
st.write("Estimación técnica de precios alineada al detalle robado")
st.markdown("---")

# =============================
# BASE DE PRECIOS TÉCNICOS
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

def estimar_precio_por_detalle(detalle):
    detalle = detalle.lower()

    unidad = "unidad"
    if "metro" in detalle or "metros" in detalle:
        unidad = "metro"

    for palabra, precios in BASE_PRECIOS.items():
        if re.search(palabra, detalle):
            if unidad in precios:
                minimo, maximo = precios[unidad]
                promedio = int((minimo + maximo) / 2)
                return minimo, maximo, promedio, palabra, unidad

    return 50000, 150000, 100000, "referencia genérica", "unidad"

# =============================
# CONFIGURACIÓN ECONÓMICA
# =============================
st.markdown("## ⚙️ Configuración del proyecto")

valor_propiedad = st.number_input(
    "Valor promedio por unidad ($)",
    value=71_000_000,
    step=1_000_000
)

costo_dia_obra = st.number_input(
    "Costo diario de obra ($)",
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
st.markdown("## 🧾 Detalle del robo")

detalle_material = st.text_area(
    "Detalle específico de lo robado",
    placeholder="Ej: 120 metros cañería cobre 1/2 tipo L"
)

cantidad = st.number_input(
    "Cantidad / unidades",
    min_value=1,
    value=1
)

unidades_afectadas = st.number_input(
    "Viviendas afectadas (0 si no aplica)",
    min_value=0,
    value=0
)

st.markdown("## 💲 Estimación de precio alineada al detalle")

precio_interno = buscar_precio_interno(detalle_material)

if precio_interno:
    st.success(f"Precio histórico interno encontrado: ${precio_interno:,.0f}")
    precio_unitario = precio_interno
else:
    if st.button("🔍 Estimar precio según detalle"):
        min_p, max_p, prom_p, palabra, unidad = estimar_precio_por_detalle(detalle_material)
        st.info(f"Referencia detectada: **{palabra}** ({unidad})")
        st.info(f"Rango estimado mercado: ${min_p:,} – ${max_p:,}")
        precio_unitario = prom_p
    else:
        precio_unitario = 0

precio_unitario = st.number_input(
    "Costo unitario estimado ($)",
    min_value=0,
    value=int(precio_unitario),
    step=1000
)

if st.button("💾 Guardar precio como referencia"):
    guardar_precio(detalle_material, precio_unitario)
    st.success("Precio guardado en base interna")

costo_robado = cantidad * precio_unitario

# =============================
# CÁLCULO IMPACTO
# =============================
if st.button("🧮 Calcular impacto"):
    dias_atraso = 10  # estimación estándar
    impacto_obra = dias_atraso * costo_dia_obra
    impacto_mano_obra = dias_atraso * costo_mano_obra_dia

    if unidades_afectadas > 0:
        ventas = unidades_afectadas * valor_propiedad
        impacto_comercial = ventas * (tasa_costo_capital / 365) * dias_atraso
    else:
        impacto_comercial = 0

    impacto_financiero = ventas * pago_final_porcentaje * (tasa_costo_capital / 365) * dias_atraso if unidades_afectadas else 0

    impacto_total = (
        costo_robado +
        impacto_obra +
        impacto_mano_obra +
        impacto_comercial +
        impacto_financiero
    )

    st.markdown("## 📊 Resultado final")
    st.metric("Costo directo del robo", f"${costo_robado:,.0f}")
    st.metric("Impacto total real estimado", f"${impacto_total:,.0f}")

    st.info(
        "Los precios son estimaciones técnicas basadas en el detalle ingresado "
        "y referencias públicas de mercado. No constituyen cotización formal."
    )

