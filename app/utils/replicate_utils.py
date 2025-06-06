import requests

# TOKEN de Hugging Face (reemplaza por el tuyo si cambia)
HUGGINGFACE_TOKEN = "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"

def describir_imagen_ruta(ruta_local: str) -> str:
    """
    Envía una imagen directamente como binario al modelo BLIP de Hugging Face y devuelve una descripción.
    """
    try:
        # Cargar imagen como binario
        with open(ruta_local, "rb") as f:
            imagen = f.read()

        # Endpoint funcional del modelo BLIP en Hugging Face
        url = "https://api-inference.huggingface.co/models/Salesforce/blip-image-captioning-base"

        headers = {
            "Authorization": f"Bearer {HUGGINGFACE_TOKEN}",
            "Content-Type": "image/jpeg"
        }

        # Realizar la solicitud POST con la imagen
        response = requests.post(url, headers=headers, data=imagen)

        # Validar respuesta HTTP
        if response.status_code != 200:
            print("❌ Error desde Hugging Face:", response.text)
        response.raise_for_status()

        # Procesar respuesta JSON esperada
        resultado = response.json()
        if isinstance(resultado, list) and "generated_text" in resultado[0]:
            return resultado[0]["generated_text"]
        else:
            raise Exception("❌ Respuesta inesperada:", resultado)

    except Exception as e:
        print("⚠️ Error analizando la imagen:", e)
        raise
