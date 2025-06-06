from fastapi import APIRouter
from pydantic import BaseModel
from app.utils.nlp_utils import extraer_nombre_producto
from app.routes.prediction import predict_price, ProductRequest  # <- Importamos desde prediction.py

router = APIRouter()

class Message(BaseModel):
    message: str

@router.post("/")
def chatbot(message: Message):
    user_msg = message.message.lower()

    if any(keyword in user_msg for keyword in ["precio", "cuánto cuesta", "vale", "valor"]):
        producto = extraer_nombre_producto(user_msg)
        if producto:
            try:
                # Construimos el request con la clase que ya tienes definida
                req = ProductRequest(product_name=producto)
                resp = predict_price(req)
                precio = resp.get("predicted_price", "desconocido")
                return {"message": f"💰 El precio estimado de '{producto}' es ${precio}."}
            except Exception:
                return {"message": f"⚠️ Ocurrió un error al obtener el precio de '{producto}'."}

        return {"message": "💰 Por favor indícame el nombre o una foto del producto del cual deseas conocer el precio."}

    elif any(keyword in user_msg for keyword in ["recomienda", "sugerencia", "producto"]):
        return {"message": "📦 Claro, ¿qué tipo de producto estás buscando? Puedes enviarme una descripción o una imagen."}

    elif any(greeting in user_msg for greeting in ["hola", "buenas"]):
        return {"message": "👋 ¡Hola! Soy tu asistente de compras. ¿Buscas productos o precios?"}

    else:
        return {"message": "🤖 No entendí muy bien. Puedes pedirme recomendaciones o preguntar precios. ¡Estoy aquí para ayudarte!"}
