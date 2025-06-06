# 🤖 E-Commerce Chatbot Machine Learning

## 📌 Descripción General
Este proyecto implementa un chatbot para Telegram que permite a los usuarios consultar productos mediante texto o imágenes, obteniendo:
- Descripción automática de imágenes con IA
- Sugerencias de productos similares 
- Predicción de precios mediante aprendizaje automático
- Acceso a la base de datos de productos (Oracle DB)

### Componentes principales:

- 🤖 **Bot de Telegram**: Interactúa con el usuario, acepta texto e imágenes, y responde con productos, precios y recomendaciones.
- 🧠 **Modelo de Visión (CLIP)**: Extrae características de imágenes para realizar búsqueda por similitud visual.
- 📈 **Modelo de Predicción de Precios**: Entrenado en Python y almacenado en formato `.pkl` (modelo regresivo).
- 🗃️ **Base de Datos Oracle**: Contiene todos los productos, imágenes, precios históricos y categorías.
- 🌐 **UI/Dashboard Web**: Interfaz para que el administrador visualice las predicciones generadas y ajuste precios.

## 🏗️ Arquitectura del Sistema
```
+----------------+           +------------------+         +----------------------+
| Usuario Telegram| <------> | Bot Telegram (Python) | <--> | API HuggingFace / CLIP|
+----------------+           +------------------+         +----------------------+
                                      |                         
                                      v
                             +------------------+
                             | Oracle SQL DB     |
                             +------------------+
```

## 🛠️ Tecnologías Utilizadas
- Python 3.11+
- Telegram Bot API
- Oracle Database + cx_Oracle
- CLIP (OpenAI) para similitud de imágenes
- scikit-learn para el modelo de predicción
- FastAPI (opcional, para endpoints locales)
- `python-telegram-bot` v20+
- Matplotlib + Pandas para análisis
- Streamlit para el dashboard

## ▶️ ¿Cómo ejecutar localmente?

### 1. Clonar el repositorio
```bash
git clone https://github.com/tu_usuario/ecommerce-chatbot-ml.git
cd ecommerce-chatbot-ml
```

### 2. Instalar dependencias
Uso de archivo requirements.txt

# Telegram bot
python-telegram-bot==20.3

# Comunicación HTTP
aiohttp==3.9.3
httpx==0.27.0
requests==2.31.0

# Machine Learning y Preprocesamiento
scikit-learn==1.4.2
pandas==2.2.2
numpy==1.26.4
joblib==1.4.2

# Procesamiento de lenguaje natural
spacy==3.7.4
torch==2.3.0
transformers==4.40.1
sentence-transformers==2.7.0

# Oracle DB
cx_Oracle==8.3.0

# Utilidades
tqdm==4.66.4
Pillow==10.3.0

# Para CLIP
ftfy==6.1.3
regex==2023.12.25

##Comando para instalar todas las dependencias 
pip install -r requirements.txt

### 3. Configurar variables de entorno `.env`
```env
TELEGRAM_TOKEN= "7900344173:AAHhduYOZobjvZ_2xNm7MVTt2rw3ZseDaVE"
HUGGINGFACE_TOKEN= "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"
ORACLE_USER= CHAT
ORACLE_PASS= CHAT1
```

### 4. Ejecutar el bot
```bash
python telegram_bot.py
```

### 5. Ejecución del servidor web local usando FastApi
```bash
uvicorn app.main:app --reload
```
### 6. Ejecución del dashboard (Dueño del negocio)
```bash
streamlit run dashboard.py
```

## 🧠 ¿Cómo entrenar o regenerar predicciones?

1. Ejecuta el script `prediccion_periodica.py` para reentrenar el modelo y actualizar precios en base de datos:
```bash
python prediccion_periodica.py
```
•	Ejecución periódica del script creado prediccion_periodica.py, generado para utilizar en Sistema Operativo Windows 11. Utilizando el programador de tareas para que este se ejecute cada día/semanalmente. 
![alt text](image-9.png)

2. El modelo usa los archivos:
- `modelo_precio.pkl` (modelo predictivo)
- `vectorizer.pkl` (vectorizador de texto)

## 📸 Capturas del Bot


- Inicio de conversación con saludo, y consulta por nombre: Su funcionamiento consiste que al momento de consultar un producto lo buscará y mostrará si fue satisfactorio, brindando así 4 sugerencias más de productos que puedan interesar al cliente.  
![alt text](image.png)

- Consulta anterior y consulta por imagen: Al haber  ya realizado una consulta pregunta y brinda la opción a seguir consultando, al realizar un envió de imagen analiza la misma, obtiene una descripción y muestra la coincidencia encontrada, brindando así 4 sugerencias más de productos que puedan interesar al cliente. 
![alt text](image-1.png)
![alt text](image-2.png)

- Uso de comando /ayuda: Al utilizar el comando ayuda brindara soporte sobre el uso del ChatBot, utilizando el comando de ayuda /destacados, brindando 5 productos destacados. 
![alt text](image-3.png)

- Uso de categorías: El comando /ayuda también brinda las categorías disponbibles del sistema, al escribir alguna de estas categorías mostrará los productos de la categoría seleccionada.
![alt text](image-4.png)

## 📥 Archivos importantes
- `telegram_bot.py`: lógica principal del bot.
- `replicate_utils.py`: Descrición de imagen utilizando HUGGINGFACE.
- `oracledb_utils.py`: conexión y consultas a Oracle. 
- `prediccion_periodica.py`: actualización diaria del modelo. 
### 

  ## 📊 Dashboard de Predicción de Precios
  
  El dashboard fue desarrollado con **Streamlit** y permite al propietario del sistema visualizar las predicciones generadas automáticamente, evaluar tendencias y establecer el precio final que será mostrado por el bot.
  
  ### Funcionalidades:
  
  - 📅 Visualización de predicciones mensuales por categoría
  - 📊 Comparación entre precio histórico y predicción ML
  - ✏️ Campo editable para establecer "Precio Final"
  - 🔄 Actualización automática desde base de datos Oracle
  
  ### Capturas:
  
  1. **Vista general del dashboard:**
 ![alt text](image-5.png)
  
  2. **Comparativa de precios por categoría:**
 ![alt text](image-6.png)
  
  3. **Edición de precio sugerido:**
![alt text](image-7.png)

 4. **Comparación de Precios Actuales vs Predicciones:**
![alt text](image-8.png)
