import streamlit as st
import pandas as pd
import altair as alt
import os

# =============================
# CONFIGURACIÓN GENERAL
# =============================
st.set_page_config(
    page_title="Inteligencia de Robos en Obras",
    layout="wide"
)

st.markdown(
    "<h1 style='color:#b00020;'>🔐 Inteligencia de Robos en Obras</h1>",
    unsafe_allow_html=True
)
st.write("Sistema corporativo de registro, análisis y control de robos")
st.markdown("---")

# =============================
# OBRAS
# =============================
OBRAS_EDIFICIOS = [
    "San Damián", "Doña Matilde", "Parque Norte", "Vista a la Viña"
]

OBRAS_CASAS = [
    "Tejas Verdes", "Don Clemente", "Cumbres del Retiro Sur B",
    "Lomas Verdes", "Kennedy", "Machalí", "VG Norte",
    "Alto Lo Castillo", "Recreo", "Rengo", "Zapallar",
    "Avellano", "San Miguel", "Doña Antonia", "VG Linares",
    "Huertos de Linares", "Portones de Linares",
    "Doña Javiera", "Huertos de Chillán", "PU Chillán",
    "Coronel", "Junquillar Retiro Sur"
]

# =============================
# BASE DE DATOS LOCAL
# =============================
DB_FILE = "robos_db.csv"

COLUMNAS = [
    "fecha", "hora", "tipo_obra", "obra",
    "sector", "partida", "zona_vulnerada",
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
tab_ed, tab_ca = st.tabs(["🏢 EDIFICIOS", "🏘️ CASAS"])

def formulario_registro(tipo, obras):
    with st.form(f"form_{tipo}"):
        obra = st.selectbox("Obra", obras)
        sector = st.text_input("Sector / Lote / Piso")
        partida = st.selectbox("Partida", [
            "Sanitarias", "Eléctricas", "Gas",
            "Terminaciones", "Estructura", "Seguridad", "Otra"
        ])

        col1, col2 = st.columns(2)
        with col1:
            fecha = st.date_input("Fecha")
            hora = st.time_input("Hora")
            zona = st.selectbox("Zona vulnerada", [
                "Bodega", "Acceso", "Cerco", "Interior", "Otra"
            ])
        with col2:
            tipo_robo = st.selectbox("Tipo de robo", [
                "Instalaciones sanitarias",
                "Instalaciones eléctricas",
                "Herramientas",
                "Maquinaria",
                "Terminaciones",
                "Otros"
            ])
            detalle = st.text_area("Detalle de lo robado")

        cantidad = st.number_input("Cantidad", min_value=1, value=1)

        col3, col4, col5 = st.columns(3)
        costo_directo = col3.number_input("Costo directo ($)", step=10000)
        dias_atraso = col4.number_input("Días de atraso", min_value=0)
        costo_mo = col5.number_input("Costo mano de obra ($)", step=10000)

        st.subheader("🔒 Seguridad")
        camara_activa = st.selectbox("Cámaras activas", ["Sí", "No"])
        camara_alerto = st.selectbox("Cámaras alertaron", ["Sí", "No"])
        guardia_presente = st.selectbox("Guardia presente", ["Sí", "No"])
        guardia_detecto = st.selectbox("Guardia detectó", ["Sí", "No"])

        guardar = st.form_submit_button("💾 Guardar robo")

        if guardar:
            nuevo = pd.DataFrame([{
                "fecha": fecha,
                "hora": hora.strftime("%H:%M"),
                "tipo_obra": tipo,
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

            df = pd.read_csv(DB_FILE)
            df = pd.concat([df, nuevo], ignore_index=True)
            df.to_csv(DB_FILE, index=False)

            st.success("✅ Robo guardado correctamente")

with tab_ed:
    st.header("🏢 Registro – Edificios")
    formulario_registro("Edificio", OBRAS_EDIFICIOS)

with tab_ca:
    st.header("🏘️ Registro – Casas")
    formulario_registro("Casas", OBRAS_CASAS)

# =============================
# ANÁLISIS GENERAL
# =============================
st.markdown("---")
st.header("📊 Análisis ejecutivo")

if len(df_db) == 0:
    st.info("Aún no hay robos registrados.")
else:
    df_db["hora"] = pd.to_datetime(df_db["hora"], format="%H:%M").dt.hour
    df_db["fecha"] = pd.to_datetime(df_db["fecha"])

    # Robos en el tiempo
    serie = df_db.groupby("fecha").size().reset_index(name="Robos")

    graf_robos = alt.Chart(serie).mark_line(
        color="#b00020", strokeWidth=3
    ).encode(
        x="fecha:T",
        y="Robos:Q",
        tooltip=["fecha:T", "Robos:Q"]
    )

    st.subheader("📈 Evolución temporal de robos")
    st.altair_chart(graf_robos, use_container_width=True)

    # Impacto económico
    impacto = df_db.groupby("fecha")["costo_directo"].sum().reset_index()

    graf_impacto = alt.Chart(impacto).mark_line(
        color="#b00020", strokeDash=[4,2], strokeWidth=3
    ).encode(
        x="fecha:T",
        y="costo_directo:Q",
        tooltip=["fecha:T", "costo_directo:Q"]
    )

    st.subheader("💰 Evolución del impacto económico")
    st.altair_chart(graf_impacto, use_container_width=True)

# =============================
# DESCARGA EXCEL (VISIBLE SIEMPRE)
# =============================
st.markdown("---")
st.header("📥 Descarga ejecutiva")

if len(df_db) == 0:
    st.warning("No hay datos para exportar.")
else:
    archivo = "robos_analisis.xlsx"
    with pd.ExcelWriter(archivo, engine="openpyxl") as writer:
        df_db.to_excel(writer, sheet_name="Base_Robos", index=False)

    with open(archivo, "rb") as f:
        st.download_button(
            "⬇️ Descargar Excel ejecutivo",
            f,
            file_name="robos_analisis.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )


