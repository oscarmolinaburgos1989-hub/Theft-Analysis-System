import streamlit as st
import pandas as pd
import os

# =============================
# CONFIGURACIÓN GENERAL
# =============================
st.set_page_config(page_title="Inteligencia de Robos en Obras", layout="wide")
st.title("🔐 Sistema de Inteligencia y Análisis de Robos en Obras")
st.write("Registro y análisis histórico de robos en Edificios y Casas")
st.markdown("---")

# =============================
# CATÁLOGO DE OBRAS
# =============================
OBRAS_EDIFICIOS = [
    "San Damián",
    "Doña Matilde",
    "Parque Norte",
    "Vista a la Viña",
    "Don Clemente",
    "Tejas Verdes",
    "Cumbres del Retiro Sur B",
    "Lomas Verdes"
]

OBRAS_CASAS = [
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
    "Junquillar",
    "Retiro Sur"
]

# =============================
# BASE DE DATOS
# =============================
DB_FILE = "robos_db.csv"

COLUMNAS = [
    "fecha", "hora",
    "tipo_obra", "obra",
    "sector", "partida",
    "zona_vulnerada",
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
# PESTAÑAS PRINCIPALES
# =============================
tab_edificios, tab_casas = st.tabs(["🏢 Edificios", "🏘️ Casas"])

# =====================================================
# PESTAÑA EDIFICIOS
# =====================================================
with tab_edificios:
    st.header("🏢 Registro de robo – Edificios")

    with st.form("form_edificios"):
        obra = st.selectbox("Edificio", OBRAS_EDIFICIOS)
        sector = st.text_input("Torre / Piso / Sector")
        contratista = st.text_input("Contratista responsable")
        partida = st.selectbox("Partida afectada", [
            "Sanitarias", "Eléctricas", "Gas",
            "Terminaciones", "Estructura", "Seguridad", "Otra"
        ])

        col1, col2 = st.columns(2)
        with col1:
            fecha = st.date_input("Fecha del robo")
            hora = st.time_input("Hora aproximada")
            zona = st.selectbox("Zona vulnerada", ["Bodega", "Acceso", "Cerco", "Interior", "Otro"])
        with col2:
            tipo_robo = st.selectbox("Tipo de material robado", [
                "Instalaciones sanitarias",
                "Instalaciones eléctricas",
                "Herramientas",
                "Maquinaria",
                "Terminaciones",
                "Otros"
            ])
            detalle = st.text_area("Detalle de lo robado")

        cantidad = st.number_input("Cantidad robada", min_value=1, value=1)

        col3, col4, col5 = st.columns(3)
        costo_directo = col3.number_input("Costo directo ($)", step=10000)
        dias_atraso = col4.number_input("Días de atraso", min_value=0, value=0)
        costo_mo = col5.number_input("Costo mano de obra ($)", step=10000)

        st.subheader("🔒 Seguridad")
        camara_activa = st.selectbox("¿Cámaras activas?", ["Sí", "No"])
        camara_alerto = st.selectbox("¿Cámaras alertaron?", ["Sí", "No"])
        guardia_presente = st.selectbox("¿Había guardia?", ["Sí", "No"])
        guardia_detecto = st.selectbox("¿Guardia detectó el robo?", ["Sí", "No"])

        guardar = st.form_submit_button("💾 Guardar robo en Edificios")

        if guardar:
            nuevo = pd.DataFrame([{
                "fecha": fecha,
                "hora": hora.strftime("%H:%M"),
                "tipo_obra": "Edificio",
                "obra": obra,
                "sector": sector,
                "contratista": contratista,
                "partida": partida,
                "zona_vulnerada": zona,
                "tipo_robo": tipo_robo,
                "detalle": detalle,
                "cantidad": cantidad,
                "costo_directo": costo_directo,
                "dias_atraso": dias_atraso,
                "costo_atraso": 0,
                "costo_mano_obra": costo_mo,
                "camara_activa": camara_activa,
                "camara_alerto": camara_alerto,
                "guardia_presente": guardia_presente,
                "guardia_detecto": guardia_detecto
            }])

            df_db = pd.concat([df_db, nuevo], ignore_index=True)
            df_db.to_csv(DB_FILE, index=False)
            st.success("✅ Robo registrado en Edificios")

# =====================================================
# PESTAÑA CASAS
# =====================================================
with tab_casas:
    st.header("🏘️ Registro de robo – Casas")

    with st.form("form_casas"):
        obra = st.selectbox("Proyecto de Casas", OBRAS_CASAS)
        sector = st.text_input("Manzana / Lote")
        contratista = st.text_input("Contratista responsable")
        partida = st.selectbox("Partida afectada", [
            "Sanitarias", "Eléctricas", "Gas",
            "Terminaciones", "Estructura", "Seguridad", "Otra"
        ])

        col1, col2 = st.columns(2)
        with col1:
            fecha = st.date_input("Fecha del robo", key="fecha_c")
            hora = st.time_input("Hora aproximada", key="hora_c")
            zona = st.selectbox("Zona vulnerada", ["Bodega", "Acceso", "Cerco", "Interior", "Otro"], key="zona_c")
        with col2:
            tipo_robo = st.selectbox("Tipo de material robado", [
                "Instalaciones sanitarias",
                "Instalaciones eléctricas",
                "Herramientas",
                "Maquinaria",
                "Terminaciones",
                "Otros"
            ], key="tipo_robo_c")
            detalle = st.text_area("Detalle de lo robado", key="detalle_c")

        cantidad = st.number_input("Cantidad robada", min_value=1, value=1, key="cantidad_c")

        col3, col4, col5 = st.columns(3)
        costo_directo = col3.number_input("Costo directo ($)", step=10000, key="cd_c")
        dias_atraso = col4.number_input("Días de atraso", min_value=0, value=0, key="da_c")
        costo_mo = col5.number_input("Costo mano de obra ($)", step=10000, key="mo_c")

        st.subheader("🔒 Seguridad")
        camara_activa = st.selectbox("¿Cámaras activas?", ["Sí", "No"], key="ca_c")
        camara_alerto = st.selectbox("¿Cámaras alertaron?", ["Sí", "No"], key="cal_c")
        guardia_presente = st.selectbox("¿Había guardia?", ["Sí", "No"], key="gp_c")
        guardia_detecto = st.selectbox("¿Guardia detectó el robo?", ["Sí", "No"], key="gd_c")

        guardar = st.form_submit_button("💾 Guardar robo en Casas")

        if guardar:
            nuevo = pd.DataFrame([{
                "fecha": fecha,
                "hora": hora.strftime("%H:%M"),
                "tipo_obra": "Casas",
                "obra": obra,
                "sector": sector,
                "contratista": contratista,
                "partida": partida,
                "zona_vulnerada": zona,
                "tipo_robo": tipo_robo,
                "detalle": detalle,
                "cantidad": cantidad,
                "costo_directo": costo_directo,
                "dias_atraso": dias_atraso,
                "costo_atraso": 0,
                "costo_mano_obra": costo_mo,
                "camara_activa": camara_activa,
                "camara_alerto": camara_alerto,
                "guardia_presente": guardia_presente,
                "guardia_detecto": guardia_detecto
            }])

            df_db = pd.concat([df_db, nuevo], ignore_index=True)
            df_db.to_csv(DB_FILE, index=False)
            st.success("✅ Robo registrado en Casas")

# =============================
# ANÁLISIS GENERAL
# =============================
st.markdown("---")
st.header("📊 Análisis general")

if len(df_db) > 0:
    df_db["hora"] = pd.to_datetime(df_db["hora"], format="%H:%M").dt.hour

    colA, colB = st.columns(2)
    with colA:
        st.subheader("🏢 vs 🏘️ Cantidad de robos")
        st.bar_chart(df_db["tipo_obra"].value_counts())

        st.subheader("⏰ Horas más frecuentes")
        st.bar_chart(df_db["hora"].value_counts().sort_index())

    with colB:
        st.subheader("💰 Impacto económico por obra")
        st.bar_chart(df_db.groupby("obra")["costo_directo"].sum())

        st.subheader("👷 Impacto por contratista")
        st.bar_chart(df_db.groupby("contratista")["costo_directo"].sum())

