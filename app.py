import streamlit as st
import pandas as pd
import os

# =============================
# CONFIGURACIÓN GENERAL
# =============================
st.set_page_config(page_title="Inteligencia de Robos en Obras", layout="wide")
st.title("🔐 Sistema de Inteligencia y Análisis de Robos en Obras")
st.write("Registro, análisis y exportación de robos en Edificios y Casas")
st.markdown("---")

# =============================
# CATÁLOGO DE OBRAS
# =============================
OBRAS_EDIFICIOS = [
    "San Damián",
    "Doña Matilde",
    "Parque Norte",
    "Vista a la Viña"
    "Tejas Verdes",
    "Don Clemente",
    "Cumbres del Retiro Sur B",
    "Lomas Verdes",
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
    "Junquillar Retiro Sur"
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
    "costo_mano_obra",
    "camara_activa", "camara_alerto",
    "guardia_presente", "guardia_detecto"
]

if not os.path.exists(DB_FILE):
    pd.DataFrame(columns=COLUMNAS).to_csv(DB_FILE, index=False)

df_db = pd.read_csv(DB_FILE)

# =============================
# PESTAÑAS
# =============================
tab_edif, tab_casas = st.tabs(["🏢 Edificios", "🏘️ Casas"])

# =====================================================
# EDIFICIOS
# =====================================================
with tab_edif:
    st.header("🏢 Registro de robo – Edificios")

    with st.form("form_edificios"):
        obra = st.selectbox("Edificio", OBRAS_EDIFICIOS)
        sector = st.text_input("Torre / Piso / Sector")
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
            detalle = st.text_area("Detalle del robo")

        cantidad = st.number_input("Cantidad robada", 1)
        col3, col4 = st.columns(2)
        costo_directo = col3.number_input("Costo directo ($)", step=10000)
        dias_atraso = col4.number_input("Días de atraso", 0)
        costo_mo = st.number_input("Costo mano de obra ($)", step=10000)

        st.subheader("🔒 Seguridad")
        camara_activa = st.selectbox("¿Cámaras activas?", ["Sí", "No"])
        camara_alerto = st.selectbox("¿Cámaras alertaron?", ["Sí", "No"])
        guardia_presente = st.selectbox("¿Había guardia?", ["Sí", "No"])
        guardia_detecto = st.selectbox("¿Guardia detectó?", ["Sí", "No"])

        if st.form_submit_button("💾 Guardar robo"):
            nuevo = pd.DataFrame([{
                "fecha": fecha,
                "hora": hora.strftime("%H:%M"),
                "tipo_obra": "Edificio",
                "obra": obra,
                "sector": sector,
                "partida": partida,
                "zona_vulnerada": zona,
                "tipo_robo": tipo_robo,
                "detalle": detalle,
                "cantidad": cantidad,
                "costo_directo": costo_directo,
                "dias_atraso": dias_atraso,
                "costo_mano_obra": costo_mo,
                "camara_activa": camara_activa,
                "camara_alerto": camara_alerto,
                "guardia_presente": guardia_presente,
                "guardia_detecto": guardia_detecto
            }])

            df_db = pd.concat([df_db, nuevo], ignore_index=True)
            df_db.to_csv(DB_FILE, index=False)
            st.success("Robo registrado correctamente")

# =====================================================
# CASAS
# =====================================================
with tab_casas:
    st.header("🏘️ Registro de robo – Casas")

    with st.form("form_casas"):
        obra = st.selectbox("Proyecto de Casas", OBRAS_CASAS)
        sector = st.text_input("Manzana / Lote")
        partida = st.selectbox("Partida afectada", [
            "Sanitarias", "Eléctricas", "Gas",
            "Terminaciones", "Estructura", "Seguridad", "Otra"
        ])

        col1, col2 = st.columns(2)
        with col1:
            fecha = st.date_input("Fecha del robo", key="fc")
            hora = st.time_input("Hora aproximada", key="hc")
            zona = st.selectbox("Zona vulnerada", ["Bodega", "Acceso", "Cerco", "Interior", "Otro"], key="zc")
        with col2:
            tipo_robo = st.selectbox("Tipo de material robado", [
                "Instalaciones sanitarias",
                "Instalaciones eléctricas",
                "Herramientas",
                "Maquinaria",
                "Terminaciones",
                "Otros"
            ], key="trc")
            detalle = st.text_area("Detalle del robo", key="dc")

        cantidad = st.number_input("Cantidad robada", 1, key="qc")
        col3, col4 = st.columns(2)
        costo_directo = col3.number_input("Costo directo ($)", step=10000, key="cdc")
        dias_atraso = col4.number_input("Días de atraso", 0, key="dac")
        costo_mo = st.number_input("Costo mano de obra ($)", step=10000, key="moc")

        st.subheader("🔒 Seguridad")
        camara_activa = st.selectbox("¿Cámaras activas?", ["Sí", "No"], key="cac")
        camara_alerto = st.selectbox("¿Cámaras alertaron?", ["Sí", "No"], key="clc")
        guardia_presente = st.selectbox("¿Había guardia?", ["Sí", "No"], key="gpc")
        guardia_detecto = st.selectbox("¿Guardia detectó?", ["Sí", "No"], key="gdc")

        if st.form_submit_button("💾 Guardar robo"):
            nuevo = pd.DataFrame([{
                "fecha": fecha,
                "hora": hora.strftime("%H:%M"),
                "tipo_obra": "Casas",
                "obra": obra,
                "sector": sector,
                "partida": partida,
                "zona_vulnerada": zona,
                "tipo_robo": tipo_robo,
                "detalle": detalle,
                "cantidad": cantidad,
                "costo_directo": costo_directo,
                "dias_atraso": dias_atraso,
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
# EXPORTAR A EXCEL / POWER BI
# =============================
st.markdown("---")
st.header("📤 Exportación de datos")

if len(df_db) > 0:

    archivo_excel = "robos_analisis.xlsx"

    with pd.ExcelWriter(archivo_excel, engine="openpyxl") as writer:

        # 1️⃣ Base completa
        df_db.to_excel(writer, sheet_name="Base_Robos", index=False)

        # 2️⃣ Ranking de obras
        if 'df_ranking' in locals():
            df_ranking.to_excel(writer, sheet_name="Ranking_Obras", index=False)

        # 3️⃣ Semáforo
        if 'df_ranking' in locals() and 'Nivel de riesgo' in df_ranking.columns:
            df_ranking[[
                "Obra",
                "Tipo de obra",
                "Índice de vulnerabilidad",
                "Nivel de riesgo"
            ]].to_excel(writer, sheet_name="Semaforo_Riesgo", index=False)

        # 4️⃣ Horarios críticos
        if 'df_horario' in locals():
            df_horario.to_excel(writer, sheet_name="Horarios_Criticos", index=False)

        # 5️⃣ Comparativo mensual
        if 'mensual' in locals():
            mensual.to_excel(writer, sheet_name="Comparativo_Mensual", index=False)

    st.caption("Exporta la base completa para Excel o Power BI")

    with open(archivo_excel, "rb") as f:
        st.download_button(
            label="📥 Descargar Excel (Análisis de Robos)",
            data=f,
            file_name="robos_analisis.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True
        )

else:
    st.info("Aún no hay datos registrados para exportar.")


