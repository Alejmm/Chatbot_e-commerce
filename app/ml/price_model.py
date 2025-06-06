import os
import pandas as pd
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LinearRegression

# -------------------------------
# CONFIGURACIÓN DE RUTAS
# -------------------------------

# Ruta al archivo CSV con datos de productos
DATA_PATH = os.path.join(os.path.dirname(__file__), '../../data/product_data.csv')

# Rutas para guardar modelo y vectorizador entrenado
MODEL_PATH = os.path.join(os.path.dirname(__file__), 'modelo_precio.pkl')
VECTORIZER_PATH = os.path.join(os.path.dirname(__file__), 'vectorizer.pkl')

# -------------------------------
# ENTRENAMIENTO DEL MODELO
# -------------------------------

def entrenar_modelo():
    """
    Entrena un modelo de regresión lineal a partir de un conjunto de datos
    con nombres de productos y sus precios. Utiliza TfidfVectorizer para
    convertir texto a vectores numéricos. Guarda el modelo y el vectorizador
    en archivos `.pkl`.
    """
    # Cargar dataset
    df = pd.read_csv(DATA_PATH)

    # Combinar nombre de producto y características en una sola entrada textual
    textos = df['product_name'] + " " + df['features']

    # Convertir texto en vectores numéricos
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(textos)

    # Variable objetivo (precio)
    y = df['price']

    # Entrenar el modelo de regresión
    modelo = LinearRegression()
    modelo.fit(X, y)

    # Guardar modelo y vectorizador para reutilización
    joblib.dump(modelo, MODEL_PATH)
    joblib.dump(vectorizer, VECTORIZER_PATH)

# -------------------------------
# CARGA DEL MODELO
# -------------------------------

def cargar_modelo():
    """
    Carga el modelo de ML y el vectorizador desde archivos `.pkl`.
    Si no existen, entrena el modelo automáticamente.
    
    Returns:
        tuple: modelo, vectorizador
    """
    if not os.path.exists(MODEL_PATH) or not os.path.exists(VECTORIZER_PATH):
        entrenar_modelo()

    modelo = joblib.load(MODEL_PATH)
    vectorizer = joblib.load(VECTORIZER_PATH)
    return modelo, vectorizer

# -------------------------------
# PREDICCIÓN DE PRECIO
# -------------------------------

def predecir_precio(product_name: str) -> float:
    """
    Predice el precio estimado de un producto dado su nombre (y opcionalmente sus características).

    Args:
        product_name (str): texto que describe el producto (ej: "iPhone 13 Pro 128GB OLED")

    Returns:
        float: precio estimado redondeado a 2 decimales
    """
    modelo, vectorizer = cargar_modelo()

    # Vectorizar entrada del usuario
    X_input = vectorizer.transform([product_name])

    # Generar predicción
    pred = modelo.predict(X_input)

    # Redondear resultado
    return round(float(pred[0]), 2)
