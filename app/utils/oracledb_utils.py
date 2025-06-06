import oracledb
import pandas as pd
import logging
import re
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
from datetime import datetime

# Configuración de conexión
DB_USER = "CHAT"
DB_PASSWORD = "CHAT1"
DB_DSN = "localhost:1521/XE"

def get_connection():
    return oracledb.connect(user=DB_USER, password=DB_PASSWORD, dsn=DB_DSN)

# -----------------------------
# Limpieza de descripción
# -----------------------------
def limpiar_descripcion(texto: str) -> str:
    texto = texto.lower()

    stopwords = [
        "the", "new", "pro", "plus", "max", "series", "available", "in", "with",
        "and", "color", "black", "gold", "green", "space gray", "white", "blue",
        "pink", "android", "gb", "tb", "inch", "pulgadas", "nuevo", "modelo"
    ]

    for palabra in stopwords:
        texto = re.sub(rf"\b{palabra}\b", "", texto)

    texto = re.sub(r"[^a-z0-9 ]", "", texto)
    texto = re.sub(r"\s+", " ", texto)

    return texto.strip()

# -----------------------------
# Buscar por nombre de producto
# -----------------------------
def buscar_producto_por_nombre(nombre_completo, limite=5):
    try:
        descripcion_limpia = limpiar_descripcion(nombre_completo)
        palabras = descripcion_limpia.lower().split()

        if not palabras:
            return []

        condiciones = " AND ".join([
            f"LOWER(p.nombre) LIKE '%' || :palabra{i} || '%'" 
            for i in range(len(palabras))
        ])

        query = f"""
            SELECT p.nombre, p.descripcion, p.precio, p.imagen_url, p.id_categoria
            FROM producto p
            WHERE {condiciones}
            AND ROWNUM <= :limite
        """

        params = {f"palabra{i}": palabra for i, palabra in enumerate(palabras)}
        params["limite"] = limite

        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute(query, params)
            resultados = cur.fetchall()
            return resultados
    except Exception as e:
        logging.error(f"❌ Error al buscar producto por nombre: {e}")
        return []

# -----------------------------
# Buscar por categoría
# -----------------------------
def obtener_productos_por_categoria(categoria, limite=5):
    try:
        if isinstance(categoria, int):  # Si es ID
            query = """
                SELECT p.nombre, p.descripcion, p.precio, p.imagen_url
                FROM producto p
                WHERE p.id_categoria = :categoria
                AND ROWNUM <= :limite
            """
        else:  # Si es nombre
            query = """
                SELECT p.nombre, p.descripcion, p.precio, p.imagen_url
                FROM producto p
                JOIN categoria c ON p.id_categoria = c.id_categoria
                WHERE LOWER(c.nombre) = LOWER(:categoria)
                AND ROWNUM <= :limite
            """

        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute(query, {"categoria": categoria, "limite": limite})
            return cur.fetchall()

    except Exception as e:
        logging.error(f"❌ Error al consultar productos por categoría: {e}")
        return []

# -----------------------------
# Productos destacados
# -----------------------------
def obtener_productos_destacados(limite=5):
    query = """
        SELECT p.nombre, p.descripcion, p.precio, p.imagen_url
        FROM producto p
        WHERE ROWNUM <= :limite
    """
    try:
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute(query, {"limite": limite})
            return cur.fetchall()
    except Exception as e:
        logging.error(f"❌ Error al obtener productos destacados: {e}")
        return []

def obtener_todos_los_productos():
    query = """
        SELECT nombre, descripcion, precio, imagen_url FROM producto
    """
    try:
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute(query)
            return cur.fetchall()
    except Exception as e:
        logging.error(f"❌ Error al obtener todos los productos: {e}")
        return []

def obtener_categorias_disponibles():
    query = "SELECT nombre FROM categoria ORDER BY id_categoria"
    try:
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute(query)
            categorias = cur.fetchall()
            return [c[0] for c in categorias]
    except Exception as e:
        logging.error(f"❌ Error al obtener categorías: {e}")
        return []

def obtener_datos_historial():
    conn = oracledb.connect(user=DB_USER, password=DB_PASSWORD, dsn=DB_DSN)
    query = """
        SELECT h.id_producto, p.nombre, h.precio, h.FECHA_ACTUALIZACION AS fecha_actualizacion
        FROM historial_precio h
        JOIN producto p ON h.id_producto = p.id_producto
        ORDER BY h.id_producto, h.FECHA_ACTUALIZACION
    """
    df = pd.read_sql(query, conn)
    conn.close()
    df.columns = [col.lower() for col in df.columns]  # normaliza columnas a minúsculas
    df['fecha_actualizacion'] = pd.to_datetime(df['fecha_actualizacion'])

    return df

# Cargar y procesar los datos
df = obtener_datos_historial()
df['fecha_actualizacion'] = pd.to_datetime(df['fecha_actualizacion'])

# Convertir fecha a días desde la primera fecha
df['dias'] = (df['fecha_actualizacion'] - df['fecha_actualizacion'].min()).dt.days

# Entrenamiento por producto
modelos = {}
resultados = []

for id_producto in df['id_producto'].unique():
    df_prod = df[df['id_producto'] == id_producto]
    if len(df_prod) >= 2:
        X = df_prod[['dias']]
        y = df_prod['precio']
        X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42)

        modelo = LinearRegression()
        modelo.fit(X_train, y_train)

        futuro = [[df['dias'].max() + 1]]
        pred = modelo.predict(futuro)[0]

        resultados.append({
            "ID": id_producto,
            "Producto": df_prod['nombre'].iloc[0],
            "Predicción próxima": round(pred, 2),
            "R²": round(r2_score(y_test, modelo.predict(X_test)), 3),
            "MSE": round(mean_squared_error(y_test, modelo.predict(X_test)), 2)
        })

def guardar_predicciones_en_bd(predicciones):
    """
    Guarda en la tabla `prediccion_precio` los datos [(id_producto, precio_predicho)].
    """
    conn = conectar()
    cursor = conn.cursor()

    for id_producto, precio_predicho in predicciones:
        try:
            cursor.execute("""
                INSERT INTO prediccion_precio (id_producto, precio_predicho)
                VALUES (:1, :2)
            """, (id_producto, precio_predicho))
        except Exception as e:
            print(f"❌ Error al guardar predicción para producto {id_producto}: {e}")
            continue

    conn.commit()
    cursor.close()
    conn.close()


# -----------------------------
# Obtener precio predicho
# -----------------------------
def obtener_precio_predicho(id_producto):
    """
    Retorna el precio predicho para un producto específico desde la tabla prediccion_precio.
    """
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT precio_predicho 
            FROM prediccion_precio 
            WHERE id_producto = :1
        """, (id_producto,))
        row = cur.fetchone()
        cur.close()
        conn.close()

        if row:
            return float(row[0])
        return None
    except Exception as e:
        logging.error(f"❌ Error al obtener precio predicho para producto {id_producto}: {e}")
        return None


# -----------------------------
# Entrenamiento del modelo
# -----------------------------
if __name__ == "__main__":
    # Cargar y procesar los datos
    df = obtener_datos_historial()
    df['fecha_actualizacion'] = pd.to_datetime(df['fecha_actualizacion'])
    df['dias'] = (df['fecha_actualizacion'] - df['fecha_actualizacion'].min()).dt.days

    modelos = {}
    resultados = []

    for id_producto in df['id_producto'].unique():
        df_prod = df[df['id_producto'] == id_producto]
        if len(df_prod) >= 2:
            X = df_prod[['dias']]
            y = df_prod['precio']
            X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42)

            modelo = LinearRegression()
            modelo.fit(X_train, y_train)

            futuro = [[df['dias'].max() + 1]]
            pred = modelo.predict(futuro)[0]

            resultados.append({
                "ID": id_producto,
                "Producto": df_prod['nombre'].iloc[0],
                "Predicción próxima": round(pred, 2),
                "R²": round(r2_score(y_test, modelo.predict(X_test)), 3),
                "MSE": round(mean_squared_error(y_test, modelo.predict(X_test)), 2)
            })    

def obtener_id_categoria_por_nombre(nombre_categoria):
    query = "SELECT id_categoria FROM categoria WHERE LOWER(nombre) = LOWER(:nombre)"
    try:
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute(query, {"nombre": nombre_categoria})
            resultado = cur.fetchone()
            return resultado[0] if resultado else None
    except Exception as e:
        logging.error(f"❌ Error al obtener ID de categoría: {e}")
        return None

    resultado_df = pd.DataFrame(resultados)
    print(resultado_df)

    guardar_predicciones_en_bd(
        [(r["ID"], r["Predicción próxima"]) for r in resultados]
    )
    
    