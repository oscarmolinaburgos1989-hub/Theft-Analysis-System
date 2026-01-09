import streamlit as st
import re
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
import tempfile
import os

# =============================
# CONFIGURACIÓN GENERAL
# =============================
st.set_page_config(
    page_title="Sistema corporativo de impacto por robos",
    layout="wide"
)

st.title("📊 Sistema corporativo de análisis de impacto por robo en obra")
st.write("Cálculo rápido, detallado y defendible + Informe PDF ejecutivo")
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

valor_vivienda = st.number_input("Valor promedio por vivienda ($)", 71_000_000, step=1_000_000)
costo_dia_obra = st.number_input("Costo diario total de obra ($)", 2_500_000, step=100_000)
costo_mano_obra = st.number_input("Costo diario mano de obra ($)", 1_200_000, step=50_000)
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
Unidad considerada: **{unidad}**  
Rango mercado Chile: **${pmin:,} – ${pmax:,}**
""")

precio_unitario = st.number_input("Precio unitario de referencia ($)", pref, step=1000)
costo_directo = cantidad * precio_unitario

# =============================
# CÁLCULO
# =============================
if st.button("🧮 Calcular impacto real"):

    impacto_obra = dias_atraso * costo_dia_obra
    impacto_mo = dias_atraso * costo_mano_obra

    if viviendas_afectadas > 0:
        capital_inmovilizado = viviendas_afectadas * valor_vivienda * pago_final
        impacto_financiero = capital_inmovilizado * (tasa_capital / 365) * dias_atraso
    else:
        capital_inmovilizado = 0
        impacto_financiero = 0

    impacto_total = costo_directo + impacto_obra + impacto_mo + impacto_financiero

    st.markdown("## 📑 Informe técnico resumido")
    st.metric("Costo directo del robo", f"${costo_directo:,.0f}")
    st.metric("Impacto por atraso de obra", f"${impacto_obra:,.0f}")
    st.metric("Impacto mano de obra", f"${impacto_mo:,.0f}")
    st.metric("Impacto financiero", f"${impacto_financiero:,.0f}")
    st.metric("💥 Impacto económico total", f"${impacto_total:,.0f}")

    # =============================
    # GENERACIÓN PDF
    # =============================
    if st.button("📄 Descargar informe PDF ejecutivo"):
        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
        doc = SimpleDocTemplate(tmp.name, pagesize=A4,
                                rightMargin=2*cm, leftMargin=2*cm,
                                topMargin=2*cm, bottomMargin=2*cm)

        styles = getSampleStyleSheet()
        content = []

        content.append(Paragraph("<b>INFORME EJECUTIVO – IMPACTO POR ROBO EN OBRA</b>", styles["Title"]))
        content.append(Spacer(1, 12))

        content.append(Paragraph("<b>1. Descripción del evento</b>", styles["Heading2"]))
        content.append(Paragraph(
            f"Detalle del robo: {detalle}<br/>"
            f"Cantidad: {cantidad} {unidad}<br/>"
            f"Días de atraso: {dias_atraso}", styles["Normal"]
        ))

        content.append(Spacer(1, 12))
        content.append(Paragraph("<b>2. Costo directo del robo</b>", styles["Heading2"]))
        content.append(Paragraph(
            f"El producto identificado corresponde a {desc}. "
            f"El valor unitario de referencia es ${precio_unitario:,.0f}, "
            f"obtenido desde referencias del mercado chileno. "
            f"El costo directo total del robo asciende a ${costo_directo:,.0f}.",
            styles["Normal"]
        ))

        content.append(Spacer(1, 12))
        content.append(Paragraph("<b>3. Impacto operativo</b>", styles["Heading2"]))
        content.append(Paragraph(
            f"El robo genera un atraso de {dias_atraso} días. "
            f"El costo diario total de la obra es ${costo_dia_obra:,.0f}, "
            f"lo que genera un impacto operativo de ${impacto_obra:,.0f}.",
            styles["Normal"]
        ))

        content.append(Spacer(1, 12))
        content.append(Paragraph("<b>4. Impacto mano de obra</b>", styles["Heading2"]))
        content.append(Paragraph(
            f"Durante el atraso, se mantienen costos de personal y contratistas "
            f"por ${costo_mano_obra:,.0f} diarios, generando un impacto de "
            f"${impacto_mo:,.0f}.",
            styles["Normal"]
        ))

        content.append(Spacer(1, 12))
        content.append(Paragraph("<b>5. Impacto financiero</b>", styles["Heading2"]))
        content.append(Paragraph(
            f"El atraso inmoviliza capital asociado a pagos finales por "
            f"${capital_inmovilizado:,.0f}. Aplicando una tasa de costo de capital "
            f"anual de {tasa_capital*100:.1f}%, el impacto financiero asciende a "
            f"${impacto_financiero:,.0f}.",
            styles["Normal"]
        ))

        content.append(Spacer(1, 12))
        content.append(Paragraph("<b>IMPACTO ECONÓMICO TOTAL</b>", styles["Heading2"]))
        content.append(Paragraph(
            f"El impacto económico total real del evento se estima en "
            f"<b>${impacto_total:,.0f}</b>.",
            styles["Normal"]
        ))

        content.append(Spacer(1, 18))
        content.append(Paragraph(
            "Este informe corresponde a una estimación técnica basada en "
            "referencias públicas del mercado chileno y parámetros económicos "
            "definidos para el proyecto. No constituye cotización formal.",
            styles["Italic"]
        ))

        doc.build(content)
        st.download_button(
            label="⬇️ Descargar PDF",
            data=open(tmp.name, "rb").read(),
            file_name="Informe_Impacto_Robo_Obra.pdf",
            mime="application/pdf"
        )

        os.unlink(tmp.name)

