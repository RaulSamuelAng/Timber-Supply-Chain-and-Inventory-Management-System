import streamlit as st
import sqlite3
import pandas as pd

# Configuración de la página web
st.set_page_config(page_title="Maderas del Norte - Web", page_icon="🪵", layout="wide")

st.title("🪵 Maderas del Norte - Panel de Control Web")
st.markdown("Bienvenido al sistema de gestión inteligente. Desde aquí puedes monitorear el almacén en tiempo real.")

# Conectores rápidos a la base de datos
def obtener_inventario():
    conexion = sqlite3.connect("inventario_maderas.db")
    df = pd.read_sql_query("SELECT id AS ID, tipo_madera AS 'Tipo de Madera', metros_cubicos AS 'Stock (m³)', precio_por_m3 AS 'Precio (€/m³)' FROM inventario", conexion)
    conexion.close()
    return df

def obtener_mermas():
    conexion = sqlite3.connect("inventario_maderas.db")
    query = """
        SELECT mermas.id AS 'ID Pérdida', inventario.tipo_madera AS 'Madera', 
               mermas.cantidad_perdida AS 'Cantidad (m³)', mermas.motivo AS 'Motivo', mermas.fecha AS 'Fecha/Hora'
        FROM mermas
        INNER JOIN inventario ON mermas.producto_id = inventario.id
    """
    df = pd.read_sql_query(query, conexion)
    conexion.close()
    return df

# --- DISEÑO DE LA INTERFAZ WEB ---
pestana1, pestana2, pestana3 = st.tabs(["📊 Inventario Real", "📋 Historial de Pérdidas", "📈 Gráficos de Analítica"])

with pestana1:
    st.header("Stock Actual en el Almacén")
    df_inventario = obtener_inventario()
    
    st.dataframe(df_inventario, use_container_width=True, hide_index=True)

with pestana2:
    st.header("Registro Histórico de Mermas")
    df_mermas = obtener_mermas()
    st.dataframe(df_mermas, use_container_width=True, hide_index=True)

with pestana3:
    st.header("Analítica de Pérdidas")
    df_mermas = obtener_mermas()
    
    if df_mermas.empty:
        st.info("No hay datos de pérdidas suficientes para generar gráficos.")
    else:
        df_grafico = df_mermas.groupby("Motivo")["Cantidad (m³)"].sum().reset_index()
        st.subheader("¿Por qué estamos perdiendo madera? (Metros cúbicos totales)")
        st.bar_chart(data=df_grafico, x="Motivo", y="Cantidad (m³)", color="#f44336")