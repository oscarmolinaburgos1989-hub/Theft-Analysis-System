import streamlit as st
import pandas as pd
import os
import smtplib
from email.message import EmailMessage
from datetime import datetime

# =============================
# CONFIGURACIÓN GENERAL
# =============================
st.set_page_config(page_title="Registro de Robos en Obras", layout="wide")
st.title("🔐 Registro y Control de Robos en Obras (LOCAL)")
st.caption("Los robos se guardan automáticamente y pueden enviarse por correo")
st.markdown("---")

# =============================
# CONFIGURACIÓN DE CORREO
# =============================
CORREO_REMITENTE = "TU_CORREO_GMAIL@gmail.com"          # 🔴 CAMBIAR
CLAVE_APP_GMAIL = "CLAVE_DE_APLICACION_GMAIL"          # 🔴 CAMBIAR

CORREOS_DESTINO = [
    "cctv@galilea.cl",
    "oscar.molina@galilea.com"
]

# =============================
# RUTA LOCAL
# =============================
BASE_DIR = os.path.join(os.path.expanduser("~"), "Documents", "Robos_Obra")
os.makedirs(BASE_DIR, exist_ok=True)

CSV_PATH = os.path.join(BASE_DIR, "robos_db.csv")
XLSX_PATH = os.path.join(BASE_DIR, "robos_db.xlsx")

# =============================
# CATÁLOGO DE OBRAS
# =============================
OBRAS_EDIFICIOS = [
    "San Damián", "Doña Matilde", "Parque Norte", "Vista a la Viña"
]

OBRAS_CASAS = [
    "Tejas Verdes", "Don Clemente", "Cumbres del Retiro Sur B",
    "Lomas Verdes", "Kennedy", "Machalí", "VG Norte",
    "Alto Lo Castillo", "Recreo", "Rengo", "Zapallar",
    "Avellano", "San Miguel", "Doña Antonia",
    "VG Linares", "Huertos de Linares", "Portones de Linares",
    "Doña Javiera", "Huertos de Chillán", "PU Chillán",
    "Coronel", "Junquillar Retiro Sur"
]

# =============================
# BASE DE DATOS
# =============================
COLUMNAS = [
    "fecha", "hora", "tipo_obra", "obra",
    "sector", "partida", "zona",
    "tipo_robo", "detalle", "cantidad",
    "costo_directo", "dias_atraso",
    "costo_mano_obra"
]

if os.path.exists(CSV_PATH):
    df_db = pd.read_csv(CSV_PATH)
else:
    df_db = pd.DataFrame(columns=COLUMNAS)
    df_db.to_csv(CSV_PATH, index=False)

# =============================
# FUNCIONES
# =============================
def guardar_registro(data):
    global df_db
    df_db = pd.concat([df_db, pd.DataFrame([data])], ignore_index=True)
    df_db.to_csv(CSV_PATH, index=False)
    df_db.to_excel(XLSX_PATH, index=False)

def enviar_excel_por_correo(ruta_excel):
    try:
        msg = EmailMessage()
        msg["Subject"] = "Registro actualizado de robos en obras"
        msg["From"] = CORREO_REMITENTE
        msg["To"] = ", ".join(CORREOS_DESTINO)

        msg.set_content(
            "Se adjunta el registro actualizado de robos en obras.\n\n"
            "Este correo fue enviado manualmente desde el sistema local."
        )

        with open(ruta_excel, "rb") as f:
            msg.add_attachment(
                f.read(),
                maintype="application",
                subtype="vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                filename="robos_db.xlsx"
            )

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(CORREO_REMITENTE, CLAVE_APP_GMAIL)
            smtp.send_message(msg)

        return True

    except Exception as e:
        return str(e)

# =============================
# PESTAÑAS
# =============================
tab1, tab2 = st.tabs(["🏢 Edificios", "🏘️ Casas"])

# =============================
# EDIFICIOS
# =============================
with tab1:
    st.header("🏢 Registro de robo – Edificios")

    with st.form("form_edificios"):
        obra = st.selectbox("Edificio", OBRAS_EDIFICIOS)
        sector = st.text_input("Torre / Piso / Sector")
        partida = st.text_input("Partida afectada")
        zona = st.text_input("Zona vulnerada")
        tipo_robo = st.text_input("Tipo de material robado")
        detalle = st.text_area("Detalle del robo")

        col1, col2, col3 = st.columns(3)
        cantidad = col1.number_input("Cantidad", 1)
        costo = col2.number_input("Costo directo ($)", step=10000)
        atraso = col3.number_input("Días de atraso", 0)

        costo_mo = st.number_input("Costo mano de obra ($)", step=10000)

        if st.form_submit_button("💾 Guardar robo"):
            guardar_registro({
                "fecha": datetime.now().date(),
                "hora": datetime.now().strftime("%H:%M"),
                "tipo_obra": "Edificio",
                "obra": obra,
                "sector": sector,
                "partida": partida,
                "zona": zona,
                "tipo_robo": tipo_robo,
                "detalle": detalle,
                "cantidad": cantidad,
                "costo_directo": costo,
                "dias_atraso": atraso,
                "costo_mano_obra": costo_mo
            })
            st.success("Robo guardado y archivo actualizado")

# =============================
# CASAS
# =============================
with tab2:
    st.header("🏘️ Registro de robo – Casas")

    with st.form("form_casas"):
        obra = st.selectbox("Proyecto de casas", OBRAS_CASAS)
        sector = st.text_input("Manzana / Lote")
        partida = st.text_input("Partida afectada")
        zona = st.text_input("Zona vulnerada")
        tipo_robo = st.text_input("Tipo de material robado")
        detalle = st.text_area("Detalle del robo")

        col1, col2, col3 = st.columns(3)
        cantidad = col1.number_input("Cantidad", 1, key="c1")
        costo = col2.number_input("Costo directo ($)", step=10000, key="c2")
        atraso = col3.number_input("Días de atraso", 0, key="c3")

        costo_mo = st.number_input("Costo mano de obra ($)", step=10000, key="c4")

        if st.form_submit_button("💾 Guardar robo"):
            guardar_registro({
                "fecha": datetime.now().date(),
                "hora": datetime.now().strftime("%H:%M"),
                "tipo_obra": "Casas",
                "obra": obra,
                "sector": sector,
                "partida": partida,
                "zona": zona,
                "tipo_robo": tipo_robo,
                "detalle": detalle,
                "cantidad": cantidad,
                "costo_directo": costo,
                "dias_atraso": atraso,
                "costo_mano_obra": costo_mo
            })
            st.success("Robo guardado y archivo actualizado")

# =============================
# VISTA EN TIEMPO REAL
# =============================
st.markdown("---")
st.header("📊 Registro en tiempo real")
st.write(f"📁 Carpeta local: {BASE_DIR}")
st.dataframe(df_db, use_container_width=True)

# =============================
# ENVÍO DE CORREO
# =============================
st.markdown("---")
st.header("📧 Enviar registro por correo")

if os.path.exists(XLSX_PATH):
    if st.button("📧 Enviar Excel por correo"):
        resultado = enviar_excel_por_correo(XLSX_PATH)

        if resultado is True:
            st.success("Excel enviado correctamente a CCTV y Oscar Molina.")
        else:
            st.error(f"Error al enviar correo: {resultado}")
else:
    st.info("Aún no existe un archivo Excel para enviar.")


