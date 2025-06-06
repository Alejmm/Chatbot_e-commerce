import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import oracledb
from datetime import datetime, date
import matplotlib.dates as mdates

# Configuración de conexión Oracle
DB_USER = "CHAT"
DB_PASSWORD = "CHAT1"
DB_DSN = "localhost:1521/XE"

def conectar():
    return oracledb.connect(user=DB_USER, password=DB_PASSWORD, dsn=DB_DSN)

def cargar_historial():
    conn = conectar()
    query = """
        SELECT h.id_producto, p.nombre, h.precio, h.fecha_actualizacion, c.nombre AS categoria
        FROM historial_precio h
        JOIN producto p ON h.id_producto = p.id_producto
        JOIN categoria c ON p.id_categoria = c.id_categoria
        ORDER BY h.id_producto, h.fecha_actualizacion
    """
    df = pd.read_sql(query, conn)
    conn.close()
    df.columns = [col.lower() for col in df.columns]
    if 'fecha_actualizacion' in df.columns:
        df['fecha_actualizacion'] = pd.to_datetime(df['fecha_actualizacion'])
    return df

def cargar_predicciones():
    conn = conectar()
    query = """
        SELECT pr.id_producto, p.nombre, pr.precio_predicho, pr.fecha_prediccion
        FROM prediccion_precio pr
        JOIN producto p ON pr.id_producto = p.id_producto
    """
    df = pd.read_sql(query, conn)
    conn.close()
    df.columns = [col.lower() for col in df.columns]
    if 'fecha_prediccion' in df.columns:
        df['fecha_prediccion'] = pd.to_datetime(df['fecha_prediccion'])
    return df

def actualizar_precio_producto(id_producto, nuevo_precio):
    conn = conectar()
    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE producto SET precio = :1 WHERE id_producto = :2", (nuevo_precio, id_producto))
        conn.commit()
        st.success(f"Precio del producto actualizado a ${nuevo_precio:.2f}")
    except Exception as e:
        st.error(f"Error al actualizar el precio: {e}")
    finally:
        cursor.close()
        conn.close()

# Interfaz Streamlit
st.set_page_config(page_title="Panel de Administración", layout="wide")
st.title("🧠 Panel de Administración de Precios")

# Cargar datos
historial = cargar_historial()
predicciones = cargar_predicciones()

# Filtros
categorias = sorted(historial['categoria'].unique())
categoria_sel = st.selectbox("📁 Filtrar por categoría", ["Todas"] + categorias)

fecha_min = historial['fecha_actualizacion'].min().date()
fecha_max = historial['fecha_actualizacion'].max().date()
fecha_sel = st.slider("🗕️ Rango de fechas", min_value=fecha_min, max_value=fecha_max, value=(fecha_min, fecha_max))

# Aplicar filtros
filtro = (historial['fecha_actualizacion'].dt.date >= fecha_sel[0]) & (historial['fecha_actualizacion'].dt.date <= fecha_sel[1])
if categoria_sel != "Todas":
    filtro &= (historial['categoria'] == categoria_sel)

hist_filtrado = historial[filtro]

# Mostrar tabla filtrada
st.subheader("📊 Historial de Precios")
st.dataframe(hist_filtrado, use_container_width=True)

# Gráfica de evolución por producto
productos_disponibles = hist_filtrado['nombre'].unique()
producto_sel = st.selectbox("📈 Ver evolución de un producto", productos_disponibles)

if producto_sel:
    datos = hist_filtrado[hist_filtrado['nombre'] == producto_sel]
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(datos['fecha_actualizacion'], datos['precio'], marker='o', linestyle='-')

    # Mejora de visualización del eje X (fechas)
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    ax.xaxis.set_major_locator(mdates.AutoDateLocator())
    plt.xticks(rotation=45)
    plt.tight_layout()

    ax.set_title(f"Evolución de Precio - {producto_sel}")
    ax.set_xlabel("Fecha")
    ax.set_ylabel("Precio")
    ax.grid(True)
    st.pyplot(fig)

# Mostrar predicciones
st.subheader("🧮 Predicciones de Precios")
st.dataframe(predicciones[['nombre', 'precio_predicho', 'fecha_prediccion']], use_container_width=True)


# ================== Sección: Comparación de precios actuales vs predicciones ==================

st.subheader("📈 Comparación de Precios Actuales vs Predicciones")

# Unimos historial y predicciones por id_producto y nos quedamos con el precio más reciente
historial_reciente = historial.sort_values('fecha_actualizacion').groupby('id_producto').last().reset_index()
predicciones_reciente = predicciones.sort_values('fecha_prediccion').groupby('id_producto').last().reset_index()

# Merge para comparación
comparacion = pd.merge(historial_reciente, predicciones_reciente, on='id_producto', how='inner', suffixes=('_actual', '_predicho'))

# Calculamos diferencia y error relativo
comparacion['diferencia'] = comparacion['precio_predicho'] - comparacion['precio']
comparacion['error_%'] = ((comparacion['diferencia']) / comparacion['precio']) * 100

# Tabla
st.dataframe(comparacion[['nombre_actual', 'precio', 'precio_predicho', 'diferencia', 'error_%']].rename(columns={
    'nombre_actual': 'Producto',
    'precio': 'Precio Actual',
    'precio_predicho': 'Precio Predicho',
    'diferencia': 'Diferencia',
    'error_%': 'Error (%)'
}), use_container_width=True)

# Gráfica de barras
st.write("📊 Diferencia entre Precios Actuales y Predicciones por Producto")

fig, ax = plt.subplots(figsize=(12, 6))
colores = ['green' if diff >= 0 else 'red' for diff in comparacion['diferencia']]

barras = ax.bar(comparacion['nombre_actual'], comparacion['diferencia'], color=colores)
ax.axhline(0, color='gray', linestyle='--')
ax.set_ylabel('Diferencia de Precio', fontsize=12)
ax.set_xlabel('Producto', fontsize=12)
ax.set_title('Diferencias entre Precio Actual y Predicho', fontsize=14)
plt.xticks(rotation=30, ha='right', fontsize=10)
ax.tick_params(axis='y', labelsize=10)
ax.grid(True, axis='y', linestyle='--', alpha=0.7)

# Etiquetas sobre cada barra
for bar, diff in zip(barras, comparacion['diferencia']):
    height = bar.get_height()
    ax.annotate(f'{diff:.2f}',
                xy=(bar.get_x() + bar.get_width() / 2, height),
                xytext=(0, 5 if height >= 0 else -15),
                textcoords="offset points",
                ha='center',
                fontsize=9,
                color='black')

st.pyplot(fig)


# Formulario para actualizar precio
st.subheader("🔄 Actualizar Precio de un Producto")

productos_predichos = predicciones['nombre'].unique()
if len(productos_predichos) == 0:
    st.warning("⚠️ No hay productos con predicciones disponibles.")
else:
    prod_a_actualizar = st.selectbox("Seleccionar producto", productos_predichos)

    if prod_a_actualizar:
        producto_data = predicciones[predicciones['nombre'] == prod_a_actualizar]
        if not producto_data.empty:
            producto_info = producto_data.iloc[0]
            id_producto = int(producto_info['id_producto'])
            precio_sugerido = producto_info['precio_predicho']

            nuevo_precio = st.number_input(
                "Nuevo precio a establecer", 
                min_value=0.0, 
                value=float(precio_sugerido), 
                step=0.1, 
                format="%.2f"
            )

            if st.button("Actualizar precio"):
                actualizar_precio_producto(id_producto, nuevo_precio)
        else:
            st.error("❌ No se encontró información para el producto seleccionado.")

