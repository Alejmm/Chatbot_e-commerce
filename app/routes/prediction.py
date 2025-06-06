from fastapi import APIRouter
from pydantic import BaseModel
from app.ml.price_model import predecir_precio

router = APIRouter()

class ProductRequest(BaseModel):
    product_name: str

@router.post('/price')
def predict_price(data: ProductRequest):
    precio_estimado = predecir_precio(data.product_name)
    return {"predicted_price": precio_estimado}
