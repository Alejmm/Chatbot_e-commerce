from transformers import BlipProcessor, BlipForConditionalGeneration
from PIL import Image
import torch

# Usar modelo directamente desde Hugging Face online
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

def describir_imagen_ruta(ruta_imagen):
    try:
        imagen = Image.open(ruta_imagen).convert("RGB")
        inputs = processor(images=imagen, return_tensors="pt")

        with torch.no_grad():
            out = model.generate(**inputs)
        descripcion = processor.decode(out[0], skip_special_tokens=True)
        return descripcion
    except Exception as e:
        print(f"❌ Error al procesar la imagen: {e}")
        return "No se pudo procesar la imagen."
