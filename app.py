import streamlit as st
import pandas as pd
import os

# =============================
# CONFIGURACIÓN GENERAL
# =============================
st.set_page_config(page_title="Inteligencia de Robos en Obras", layout="wide")
st.title("🔐 Sistema de Inteligencia y Análisis de Robos en Obras")
st.write("Registro estructurado, base de datos histórica y análisis comparativo")
st.markdown("---")

# =============================
# CATÁLOGO DE OBRAS
# =============================

OBRAS_EDIFICIOS = [
    "San Damián",
    "Doña Matilde",
    "Parque Norte",
    "Vista a la Viña"
]

OBRAS_CASAS = [
    "Tejas Verdes",
    "Don Clemente",
    "Cumbres del Retiro Sur B",
    "Lomas Verdes",
    "Kennedy",
    "Machalí",
    "VG Norte",
    "Alto Lo Castillo",
    "Recreo",
    "Rengo",
    "Zapallar",
    "Avellano",
    "San Miguel",
    "Doña Antonia",
    "VG Linares",
    "Huertos de Linares",
    "Portones de Linares",
    "Doña Javiera",
    "Huertos de Chillán",
    "PU Chillán",
    "Coronel",
    "Junquillar Retiro Sur"
]

TODAS_LAS_OBRAS = OBRAS_EDIFICIOS + OBRAS_CASAS

def tipo_obra_por_nombre(nombre):
    if nombre in OBRAS_EDIFICIOS:
        return "Edificio"
    elif nombre in OBRAS_CASAS:
        return "Casas"
    else:
        return "No definido"

# =============================
# BASE DE DATOS
# =============================
DB_FILE = "robos_db.csv"

COLUMNAS = [
    "fecha", "hora",
    "obra", "tipo_obra",
    "sector", "contratista", "partida",
    "zona_vulnerada",
    "tipo_robo", "detalle", "cantidad",
    "costo_atraso", "costo_mano_obra",
    "camara_activa", "camara_alerto",
    "guardia_presente", "guardia_detecto"
]

if not os.path.exists(DB_FILE):
    pd.DataFrame(columns=COLUMNAS).to_csv(DB_FILE, index=False)

df_db = pd.read_csv(DB_FILE)

# =============================
# FORMULARIO DE REGISTRO
# =============================
st.header("📝 Registro de robo")

with st.form("form_robo"):
    col1, col2, col3 = st.columns(3)

    with col1:
        obra = st.selectbox("Obra", TODAS_LAS_OBRAS)
        tipo_obra = tipo_obra_por_nombre(obra)
        st.info(f"Tipo de obra detectado automáticamente: **{tipo_obra}**")
        sector = st.text_input("Bloque / Torre / Sector")

    with col2:
        contratista = st.text_input("Contratista responsable")
        partida = st.selectbox("Partida afectada", [
            "Sanitarias",
            "Eléctricas",
            "Gas",
            "Terminaciones",
            "Estructura",
            "Seguridad",
            "Otra"
        ])

    with col3:
        fecha = st.date_input("Fecha del robo")
        hora = st.time_input("Hora aproximada")
        zona = st.selectbox("Zona vulnerada", [
            "Bodega",
            "Acceso",
            "Cerco",
            "Interior",
            "Otro"
        ])

    st.markdown("---")

    col4, col5, col6 = st.columns(3)

    with col4:
        tipo_robo = st.selectbox("Tipo de material robado", [
            "Instalaciones sanitarias",
            "Instalaciones eléctricas",
            "Herramientas",
            "Maquinaria",
            "Terminaciones",
            "Otros"
        ])
        detalle = st.text_area("Detalle específico de lo robado")

    with col5:
        cantidad = st.number_input("Cantidad robada", min_value=1, value=1)
        dias_atraso = st.number_input("Días de atraso", min_value=0, value=0)

    with col6:
        costo_directo = st.number_input("Costo directo ($)", step=10000)
        costo_atraso = st.number_input("Costo atraso obra ($)", step=10000)
        costo_mano_obra = st.number_input("Costo mano de obra ($)", step=10000)

    st.subheader("🔒 Seguridad")

    col7, col8 = st.columns(2)

    with col7:
        camara_activa = st.selectbox("¿Cámaras activas?", ["Sí", "No"])
        camara_alerto = st.selectbox("¿Cámaras alertaron?", ["Sí", "No"])

    with col8:
        guardia_presente = st.selectbox("¿Había guardia?", ["Sí", "No"])
        guardia_detecto = st.selectbox("¿Guardia detectó el robo?", ["Sí", "No"])

    guardar = st.form_submit_button("💾 Guardar robo")

    if guardar:
        nuevo = pd.DataFrame([{
            "fecha": fecha,
            "hora": hora.strftime("%H:%M"),
            "obra": obra,
            "tipo_obra": tipo_obra,
            "sector": sector,
            "contratista": contratista,
            "partida": partida,
            "zona_vulnerada": zona,
            "tipo_robo": tipo_robo,
            "detalle": detalle,
            "cantidad": cantidad,
            "costo_directo": costo_directo,
            "dias_atraso": dias_atraso,
            "costo_atraso": costo_atraso,
            "costo_mano_obra": costo_mano_obra,
            "camara_activa": camara_activa,
            "camara_alerto": camara_alerto,
            "guardia_presente": guardia_presente,
            "guardia_detecto": guardia_detecto
        }])

        df_db = pd.concat([df_db, nuevo], ignore_index=True)
        df_db.to_csv(DB_FILE, index=False)
        st.success("✅ Robo registrado correctamente")

# =============================
# ANÁLISIS COMPARATIVO
# =============================
st.markdown("---")
st.header("📊 Análisis comparativo")

if len(df_db) > 0:
    df_db["hora"] = pd.to_datetime(df_db["hora"], format="%H:%M").dt.hour

    colA, colB = st.columns(2)

    with colA:
        st.subheader("🏢 Edificios vs 🏘️ Casas (Cantidad de robos)")
        st.bar_chart(df_db["tipo_obra"].value_counts())

        st.subheader("⏰ Horas más frecuentes de robos")
        st.bar_chart(df_db["hora"].value_counts().sort_index())

    with colB:
        st.subheader("💰 Impacto económico por obra")
        st.bar_chart(df_db.groupby("obra")["costo_directo"].sum())

        st.subheader("👷 Impacto por contratista")
        st.bar_chart(df_db.groupby("contratista")["costo_directo"].sum())

else:
    st.info("Aún no hay robos registrados")

