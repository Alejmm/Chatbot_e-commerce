import oracledb
import pandas as pd
from sklearn.linear_model import LinearRegression
from datetime import datetime
import logging

# Configuración de conexión
DB_USER = "CHAT"
DB_PASSWORD = "CHAT1"
DB_DSN = "localhost:1521/XE"

def get_connection():
    return oracledb.connect(user=DB_USER, password=DB_PASSWORD, dsn=DB_DSN)

def entrenar_y_guardar_predicciones():
    conn = get_connection()
    cur = conn.cursor()

    # Obtener todos los id_producto únicos
    cur.execute("SELECT DISTINCT id_producto FROM historial_precio")
    productos = cur.fetchall()

    for (id_producto,) in productos:
        # Obtener historial para ese producto
        cur.execute("""
            SELECT precio, fecha_actualizacion
            FROM historial_precio
            WHERE id_producto = :id
            ORDER BY fecha_actualizacion
        """, {"id": id_producto})
        datos = cur.fetchall()

        if len(datos) >= 2:
            precios, fechas = zip(*datos)
            df = pd.DataFrame({
                "fecha": pd.to_datetime(fechas),
                "precio": precios
            })

            # Codificar fecha como días desde la primera fecha
            df["dias"] = (df["fecha"] - df["fecha"].min()).dt.days

            X = df[["dias"]]
            y = df["precio"]

            modelo = LinearRegression()
            modelo.fit(X, y)

            siguiente_dia = df["dias"].max() + 1
            precio_predicho = modelo.predict([[siguiente_dia]])[0]

            # Guardar predicción
            cur.execute("""
                INSERT INTO prediccion_precio (id_producto, precio_predicho)
                VALUES (:id_producto, :precio)
            """, {
                "id_producto": id_producto,
                "precio": round(precio_predicho, 2)
            })
            conn.commit()
            print(f"✅ Producto {id_producto} → ${precio_predicho:.2f}")

        else:
            print(f"⚠️ Producto {id_producto} tiene datos insuficientes.")

    cur.close()
    conn.close()

if __name__ == "__main__":
    entrenar_y_guardar_predicciones()


from app.utils.oracledb_utils import get_connection

def guardar_predicciones(predicciones):
    try:
        with get_connection() as conn:
            cur = conn.cursor()
            for id_producto, precio_predicho in predicciones:
                # Eliminar predicción anterior si existe
                cur.execute("""
                    DELETE FROM prediccion_precio
                    WHERE id_producto = :id_producto
                """, {"id_producto": id_producto})

                # Insertar nueva predicción
                cur.execute("""
                    INSERT INTO prediccion_precio (id_producto, precio_predicho)
                    VALUES (:id_producto, :precio_predicho)
                """, {
                    "id_producto": id_producto,
                    "precio_predicho": round(precio_predicho, 2)
                })

            conn.commit()
            print("✅ Predicciones actualizadas correctamente.")
    except Exception as e:
        print(f"❌ Error al guardar predicciones: {e}")
