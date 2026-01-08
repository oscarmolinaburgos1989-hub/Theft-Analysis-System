import streamlit as st
import re

# =============================
# CONFIGURACIÓN GENERAL
# =============================
st.set_page_config(
    page_title="Análisis real de impacto por robo en obra",
    layout="wide"
)

st.title("📊 Sistema inteligente de análisis de impacto por robo")
st.write("Cálculo automático, rápido y defendible del costo real del robo")
st.markdown("---")

# =============================
# BASE DE PRECIOS CHILE (REFERENCIA)
# =============================
# Rangos reales de mercado chileno (CLP)
BASE_PRECIOS_CHILE = {
    "calefon": {
        "descripcion": "Calefón a gas estándar (ionizado / tiro natural)",
        "unidad": "unidad",
        "min": 120000,
        "max": 280000
    },
    "monomando": {
        "descripcion": "Grifería monomando baño / cocina estándar",
        "unidad": "unidad",
        "min": 35000,
        "max": 120000
    },
    "cobre": {
        "descripcion": "Cañería de cobre sanitaria",
        "unidad": "metro",
        "min": 9000,
        "max": 12000
    },
    "cable": {
        "descripcion": "Cable eléctrico cobre",
        "unidad": "metro",
        "min": 2500,
        "max": 6000
    },
    "tablero": {
        "descripcion": "Tablero eléctrico domiciliario",
        "unidad": "unidad",
        "min": 180000,
        "max": 350000
    },
    "herramienta": {
        "descripcion": "Herramientas manuales / eléctricas",
        "unidad": "unidad",
        "min": 30000,
        "max": 150000
    }
}

def detectar_producto(texto):
    texto = texto.lower()
    for clave in BASE_PRECIOS_CHILE:
        if re.search(clave, texto):
            p = BASE_PRECIOS_CHILE[clave]
            promedio = int((p["min"] + p["max"]) / 2)
            return clave, p["descripcion"], p["unidad"], p["min"], p["max"], promedio
    return None, "Producto genérico", "unidad", 50000, 150000, 100000

# =============================
# CONFIGURACIÓN DEL PROYECTO
# =============================
st.header("1️⃣ Configuración económica del proyecto")

valor_vivienda = st.number_input(
    "Valor promedio por vivienda ($)",
    value=71_000_000,
    step=1_000_000
)

costo_diario_obra = st.number_input(
    "Costo diario total de la obra ($)",
    value=2_500_000,
    step=100_000
)

costo_mano_obra_dia = st.number_input(
    "Costo diario mano de obra / contratistas ($)",
    value=1_200_000,
    step=50_000
)

tasa_capital = st.number_input(
    "Costo de capital anual (%)",
    value=10.0
) / 100

pago_final = st.number_input(
    "Pago final retenido (%)",
    value=20.0
) / 100

st.markdown("---")

# =============================
# DATOS DEL ROBO
# =============================
st.header("2️⃣ Detalle del robo")

detalle = st.text_area(
    "¿Qué fue robado?",
    placeholder="Ej: 2 calefont ionizado + 5 monomando baño"
)

cantidad = st.number_input(
    "Cantidad robada",
    min_value=1,
    value=1
)

dias_atraso = st.number_input(
    "Días de atraso generados por el robo",
    value=10
)

viviendas_afectadas = st.number_input(
    "Viviendas afectadas (0 si no aplica)",
    value=0
)

st.markdown("---")

# =============================
# ESTIMACIÓN DE PRECIO
# =============================
st.header("3️⃣ Precio de referencia automático")

clave, descripcion, unidad, p_min, p_max, p_prom = detectar_producto(detalle)

st.info(f"""
Producto reconocido: **{descripcion}**  
Unidad considerada: **{unidad}**  
Rango mercado Chile: **${p_min:,} – ${p_max:,}**
""")

precio_unitario = st.number_input(
    "Precio unitario de referencia ($)",
    value=p_prom,
    step=1000
)

costo_directo = cantidad * precio_unitario

# =============================
# CÁLCULO DE IMPACTO
# =============================
if st.button("🧮 Analizar impacto real"):

    impacto_obra = dias_atraso * costo_diario_obra
    impacto_mano_obra = dias_atraso * costo_mano_obra_dia

    if viviendas_afectadas > 0:
        ventas_afectadas = viviendas_afectadas * valor_vivienda
        impacto_comercial = ventas_afectadas * (tasa_capital / 365) * dias_atraso
        flujo_retenido = ventas_afectadas * pago_final
        impacto_financiero = flujo_retenido * (tasa_capital / 365) * dias_atraso
    else:
        impacto_comercial = 0
        impacto_financiero = 0
        ventas_afectadas = 0

    impacto_total = (
        costo_directo +
        impacto_obra +
        impacto_mano_obra +
        impacto_comercial +
        impacto_financiero
    )

    # =============================
    # INFORME DETALLADO
    # =============================
    st.markdown("## 📑 INFORME DETALLADO DE IMPACTO")

    st.markdown("### 🔹 1. Costo directo del robo")
    st.write(f"""
Se reconoce el producto **{descripcion}** a partir del texto ingresado.
El sistema utiliza referencias del mercado chileno, con un rango entre
${p_min:,} y ${p_max:,}.  
Se adopta un valor de referencia **${precio_unitario:,.0f}** por {unidad}.
""")

    st.metric("Costo directo del robo", f"${costo_directo:,.0f}")

    st.markdown("### 🔹 2. Impacto por atraso de obra")
    st.write(f"""
El robo genera un atraso estimado de **{dias_atraso} días**.
Cada día de obra tiene un costo de **${costo_diario_obra:,.0f}**.
""")
    st.metric("Impacto por atraso de obra", f"${impacto_obra:,.0f}")

    st.markdown("### 🔹 3. Impacto en mano de obra")
    st.write(f"""
Durante el atraso, se mantiene costo diario de mano de obra y contratistas
por **${costo_mano_obra_dia:,.0f}**.
""")
    st.metric("Impacto mano de obra", f"${impacto_mano_obra:,.0f}")

    st.markdown("### 🔹 4. Impacto comercial")
    st.write(f"""
Se consideran **{viviendas_afectadas} viviendas afectadas**, con un valor
promedio de **${valor_vivienda:,.0f}** por unidad.
El costo corresponde al capital inmovilizado durante el atraso.
""")
    st.metric("Impacto comercial", f"${impacto_comercial:,.0f}")

    st.markdown("### 🔹 5. Impacto financiero")
    st.write(f"""
Se considera un pago final retenido del **{pago_final*100:.1f}%**,
con un costo de capital anual del **{tasa_capital*100:.1f}%**.
""")
    st.metric("Impacto financiero", f"${impacto_financiero:,.0f}")

    st.markdown("---")
    st.metric("💥 IMPACTO ECONÓMICO TOTAL REAL", f"${impacto_total:,.0f}")

    st.info(
        "Este análisis corresponde a una estimación técnica basada en referencias "
        "del mercado chileno y parámetros económicos del proyecto. "
        "No constituye cotización comercial."
    )

