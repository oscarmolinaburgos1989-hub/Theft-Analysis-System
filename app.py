import streamlit as st
import re

# =============================
# CONFIGURACIÓN GENERAL
# =============================
st.set_page_config(
    page_title="Sistema corporativo de impacto por robos",
    layout="wide"
)

st.title("📊 Sistema corporativo de análisis de impacto por robo en obra")
st.write("Cálculo rápido, detallado y defendible del costo real del robo")
st.markdown("---")

# =============================
# BASE DE PRECIOS – MERCADO CHILENO
# =============================
BASE_PRECIOS = {
    "calefon": ("Calefón a gas estándar", "unidad", 120000, 280000),
    "monomando": ("Grifería monomando estándar", "unidad", 35000, 120000),
    "cobre": ("Cañería de cobre sanitaria", "metro", 9000, 12000),
    "cable": ("Cable eléctrico de cobre", "metro", 2500, 6000),
    "tablero": ("Tablero eléctrico domiciliario", "unidad", 180000, 350000),
    "herramienta": ("Herramientas manuales / eléctricas", "unidad", 30000, 150000)
}

def reconocer_producto(texto):
    texto = texto.lower()
    for k, v in BASE_PRECIOS.items():
        if re.search(k, texto):
            desc, unidad, pmin, pmax = v
            prom = int((pmin + pmax) / 2)
            return k, desc, unidad, pmin, pmax, prom
    return "genérico", "Elemento de obra genérico", "unidad", 50000, 150000, 100000

# =============================
# CONFIGURACIÓN ECONÓMICA
# =============================
st.header("1️⃣ Parámetros económicos del proyecto")

valor_vivienda = st.number_input("Valor promedio por vivienda ($)", 71000000, step=1000000)
costo_dia_obra = st.number_input("Costo diario total de obra ($)", 2500000, step=100000)
costo_mano_obra = st.number_input("Costo diario mano de obra ($)", 1200000, step=50000)
tasa_capital = st.number_input("Costo de capital anual (%)", 10.0) / 100
pago_final = st.number_input("Pago final retenido (%)", 20.0) / 100

st.markdown("---")

# =============================
# DETALLE DEL ROBO
# =============================
st.header("2️⃣ Evento de robo")

detalle = st.text_area("Detalle de lo robado", placeholder="Ej: 2 calefont ionizado + 5 monomando")
cantidad = st.number_input("Cantidad robada", 1)
dias_atraso = st.number_input("Días de atraso generados", 10)
viviendas_afectadas = st.number_input("Viviendas afectadas", 0)

# =============================
# RECONOCIMIENTO Y PRECIO
# =============================
clave, desc, unidad, pmin, pmax, pref = reconocer_producto(detalle)

st.markdown("### 🔎 Reconocimiento automático")
st.write(f"""
Producto identificado: **{desc}**  
Unidad: **{unidad}**  
Rango mercado Chile: **${pmin:,} – ${pmax:,}**
""")

precio_unitario = st.number_input("Precio unitario de referencia ($)", pref, step=1000)
costo_directo = cantidad * precio_unitario

# =============================
# CÁLCULO FINAL
# =============================
if st.button("🧮 Calcular impacto real"):

    impacto_obra = dias_atraso * costo_dia_obra
    impacto_mo = dias_atraso * costo_mano_obra

    if viviendas_afectadas > 0:
        capital_inmovilizado = viviendas_afectadas * valor_vivienda * pago_final
        impacto_comercial = capital_inmovilizado * (tasa_capital / 365) * dias_atraso
        impacto_financiero = impacto_comercial
    else:
        impacto_comercial = impacto_financiero = 0
        capital_inmovilizado = 0

    impacto_total = costo_directo + impacto_obra + impacto_mo + impacto_comercial

    # =============================
    # INFORME EXPLICADO
    # =============================
    st.markdown("## 📑 Informe técnico detallado")

    st.markdown("### 1️⃣ Costo directo del robo")
    st.write(f"""
Se reconoce **{desc}** a partir del texto ingresado.  
El precio unitario se define usando referencias del mercado chileno.  
Costo directo = {cantidad} × ${precio_unitario:,.0f}
""")
    st.metric("Costo directo", f"${costo_directo:,.0f}")

    st.markdown("### 2️⃣ Impacto operativo")
    st.write(f"""
El robo genera un atraso de **{dias_atraso} días**.
Cada día de obra cuesta **${costo_dia_obra:,.0f}**.
""")
    st.metric("Impacto por atraso de obra", f"${impacto_obra:,.0f}")

    st.markdown("### 3️⃣ Impacto mano de obra")
    st.write(f"""
Durante el atraso, la empresa mantiene personal y contratistas activos.
Costo diario mano de obra = **${costo_mano_obra:,.0f}**.
""")
    st.metric("Impacto mano de obra", f"${impacto_mo:,.0f}")

    st.markdown("### 4️⃣ Impacto financiero")
    st.write(f"""
El atraso inmoviliza pagos finales por **${capital_inmovilizado:,.0f}**.
Se aplica una tasa anual de **{tasa_capital*100:.1f}%**, prorrateada por días.
""")
    st.metric("Impacto financiero", f"${impacto_financiero:,.0f}")

    st.markdown("---")
    st.metric("💥 IMPACTO ECONÓMICO TOTAL REAL", f"${impacto_total:,.0f}")

    st.info("Informe basado en estimaciones técnicas y referencias públicas de mercado chileno.")

