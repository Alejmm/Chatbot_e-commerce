import torch
from sentence_transformers import SentenceTransformer, util
import logging

clip_model = SentenceTransformer("clip-ViT-B-32")

def generar_embedding_texto(texto: str):
    return clip_model.encode(texto, convert_to_tensor=True)

def buscar_productos_similares(texto, productos, top_k=5):
    try:
        # Embedding del texto
        texto_emb = generar_embedding_texto(texto)
        texto_emb = torch.nn.functional.normalize(texto_emb, p=2, dim=0)

        # Embeddings ponderados de productos: nombre (peso 2) + descripción
        embeddings_productos = []
        for nombre, descripcion, *_ in productos:
            combinado = f"{nombre} {nombre} {descripcion}"
            emb = generar_embedding_texto(combinado)
            embeddings_productos.append(torch.nn.functional.normalize(emb, p=2, dim=0))

        # Matriz de similitud
        productos_emb_tensor = torch.stack(embeddings_productos)
        similitudes = util.pytorch_cos_sim(texto_emb, productos_emb_tensor)[0]

        # Filtrar los más relevantes
        top_resultados = torch.topk(similitudes, k=min(top_k, len(productos)))

        mejores = []
        for idx in top_resultados.indices:
            mejores.append(productos[idx.item()])  # (nombre, desc, precio, img)

        return mejores

    except Exception as e:
        logging.error("Error en buscar_productos_similares: " + str(e))
        return []
