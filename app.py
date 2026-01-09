import streamlit as st
import pandas as pd
import os
from datetime import datetime

# =============================
# CONFIGURACIÓN
# =============================
st.set_page_config(page_title="Inteligencia de Robos en Obra", layout="wide")
st.title("🔐 Sistema de Inteligencia y Análisis de Robos en Obra")
st.write("Registro, análisis comparativo y detección de patrones")
st.markdown("---")

DB_FILE = "robos_db.csv"

# =============================
# BASE DE DATOS
# =============================
COLUMNAS = [
    "fecha", "hora", "obra", "ubicacion", "zona_vulnerada",
    "tipo_robo", "detalle", "cantidad",
    "costo_directo", "dias_atraso",
    "costo_atraso", "costo_mano_obra",
    "camara_activa", "camara_alerto",
    "guardia_presente", "guardia_detecto"
]

if not os.path.exists(DB_FILE):
    pd.DataFrame(columns=COLUMNAS).to_csv(DB_FILE, index=False)

df_db = pd.read_csv(DB_FILE)

# =============================
# FORMULARIO DE INGRESO
# =============================
st.header("📝 Registrar nuevo robo")

with st.form("form_robo"):
    col1, col2, col3 = st.columns(3)

    with col1:
        fecha = st.date_input("Fecha del robo")
        hora = st.time_input("Hora aproximada")
        obra = st.text_input("Nombre de la obra / ubicación")
        zona = st.selectbox("Zona vulnerada", ["Bodega", "Acceso", "Cerco", "Interior", "Otro"])

    with col2:
        tipo_robo = st.selectbox("Tipo de material", [
            "Instalaciones sanitarias",
            "Instalaciones eléctricas",
            "Herramientas",
            "Maquinaria",
            "Terminaciones",
            "Otros"
        ])
        detalle = st.text_area("Detalle específico de lo robado")
        cantidad = st.number_input("Cantidad", 1)

    with col3:
        costo_directo = st.number_input("Costo directo ($)", step=10000)
        dias_atraso = st.number_input("Días de atraso", 0)
        costo_atraso = st.number_input("Costo por atraso ($)", step=10000)
        costo_mo = st.number_input("Costo mano de obra recontratada ($)", step=10000)

    st.subheader("🔒 Seguridad")
    camara_activa = st.selectbox("¿Cámaras activas?", ["Sí", "No"])
    camara_alerto = st.selectbox("¿Cámaras alertaron?", ["Sí", "No"])
    guardia_presente = st.selectbox("¿Había guardia?", ["Sí", "No"])
    guardia_detecto = st.selectbox("¿Guardia detectó el robo?", ["Sí", "No"])

    submit = st.form_submit_button("💾 Guardar robo")

    if submit:
        nuevo = pd.DataFrame([{
            "fecha": fecha,
            "hora": hora.strftime("%H:%M"),
            "obra": obra,
            "ubicacion": obra,
            "zona_vulnerada": zona,
            "tipo_robo": tipo_robo,
            "detalle": detalle,
            "cantidad": cantidad,
            "costo_directo": costo_directo,
            "dias_atraso": dias_atraso,
            "costo_atraso": costo_atraso,
            "costo_mano_obra": costo_mo,
            "camara_activa": camara_activa,
            "camara_alerto": camara_alerto,
            "guardia_presente": guardia_presente,
            "guardia_detecto": guardia_detecto
        }])

        df_db = pd.concat([df_db, nuevo], ignore_index=True)
        df_db.to_csv(DB_FILE, index=False)
        st.success("Robo registrado correctamente")

# =============================
# ANÁLISIS
# =============================
st.markdown("---")
st.header("📊 Análisis comparativo de robos")

if len(df_db) > 0:

    df_db["hora"] = pd.to_datetime(df_db["hora"], format="%H:%M").dt.hour

    colA, colB = st.columns(2)

    with colA:
        st.subheader("⏰ Horas más frecuentes")
        st.bar_chart(df_db["hora"].value_counts().sort_index())

        st.subheader("🧱 Tipo de robo más repetido")
        st.bar_chart(df_db["tipo_robo"].value_counts())

    with colB:
        st.subheader("📍 Obras con más robos")
        st.bar_chart(df_db["obra"].value_counts())

        st.subheader("💰 Dinero robado por obra")
        st.bar_chart(df_db.groupby("obra")["costo_directo"].sum())

    st.subheader("🚨 Fallas de seguridad")
    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "% cámaras NO alertaron",
            f"{round((df_db[df_db['camara_alerto']=='No'].shape[0] / len(df_db))*100, 1)}%"
        )

    with col2:
        st.metric(
            "% guardias NO detectaron",
            f"{round((df_db[df_db['guardia_detecto']=='No'].shape[0] / len(df_db))*100, 1)}%"
        )

else:
    st.info("Aún no hay robos registrados")

