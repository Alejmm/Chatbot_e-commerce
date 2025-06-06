import spacy
import re

# Cargar modelo de spaCy en español
nlp = spacy.load("es_core_news_md")

# Lista ampliada de patrones regex para fallback
PATRONES_PRODUCTO = [
    # Smartphones
    r"(iphone\s?\d+\s?(pro)?\s?(max)?\s?\d*\s?gb?)",
    r"(samsung\s?(galaxy)?\s?\w+)",
    r"(motorola\s?\w+)",
    r"(xiaomi\s?\w+)",
    r"(huawei\s?\w+)",
    r"(nokia\s?\w+)",

    # Laptops
    r"(laptop\s?(asus|hp|lenovo|dell|acer)\s?\w*)",
    r"(notebook\s?(asus|hp|lenovo|dell|acer)\s?\w*)",
    r"(macbook\s?(air|pro)?\s?\d*\w*)",

    # Televisores y pantallas
    r"(televisor\s?\w+\s?\d{2,3} pulgadas?)",
    r"(tv\s?(samsung|lg|sony|philips)\s?\w*)",
    r"(monitor\s?(asus|lg|samsung|acer|benq)\s?\w*)",

    # Accesorios
    r"(mouse\s?(gamer|inalámbrico|bluetooth)?\s?\w*)",
    r"(teclado\s?(gamer|mecánico)?\s?\w*)",
    r"(auriculares\s?(bluetooth|sony|jbl|xiaomi|samsung)\s?\w*)",

    # Otros
    r"(tablet\s?(samsung|huawei|ipad|lenovo)\s?\w*)",
    r"(impresora\s?\w+)",
    r"(reloj\s?(inteligente|smartwatch|xiaomi|huawei|apple)\s?\w*)",
    r"(consola\s?(ps5|playstation|xbox|nintendo)\s?\w*)",
    r"(router\s?(tp-link|huawei|netgear|asus|tplink)\s?\w*)"
]

import re
from app.utils.spacy_model import nlp  # o como hayas importado tu modelo

# Patrones para limpiar preguntas comunes
PATRONES_LIMPIEZA = [
    r"cu[aá]nto cuesta\s*(el|la)?\s*",
    r"cu[aá]l es el precio\s*(de|del|de la)?\s*",
    r"precio de\s*(el|la)?\s*",
    r"vale\s*(el|la)?\s*",
    r"cu[aá]nto vale\s*(el|la)?\s*"
]

# Opcionales: patrones simples como fallback
PATRONES_PRODUCTO = [
    r"(iphone \d{1,2}( pro)?)",
    r"(galaxy s\d{1,2})",
    r"(macbook air|macbook pro)",
    r"(playstation \d|ps\d)",
    r"(motorola .*?)",
    r"(redmi .*?)"
]

def extraer_nombre_producto(texto: str) -> str | None:
    texto = texto.lower()

    # Limpieza inicial de frases comunes
    for patron in PATRONES_LIMPIEZA:
        texto = re.sub(patron, '', texto).strip()

    doc = nlp(texto)

    # 1. Entidades nombradas relevantes
    entidades = [ent.text for ent in doc.ents if ent.label_ in ("PRODUCT", "ORG", "MISC")]
    if entidades:
        return " ".join(entidades).strip()

    # 2. Grupos de sustantivos si no se detectan entidades
    sustantivos = [token.text for token in doc if token.pos_ in ("NOUN", "PROPN")]
    if sustantivos:
        return " ".join(sustantivos).strip()

    # 3. Fallback con expresiones regulares
    for patron in PATRONES_PRODUCTO:
        match = re.search(patron, texto)
        if match:
            return match.group(0).strip()

    return None

