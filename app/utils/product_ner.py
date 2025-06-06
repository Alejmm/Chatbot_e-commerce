from transformers import AutoTokenizer, AutoModelForTokenClassification
from transformers import pipeline

# Carga modelo BETO entrenado para NER
model_name = "mrm8488/bert-spanish-cased-finetuned-ner"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForTokenClassification.from_pretrained(model_name)

# Pipeline de NER
ner_pipeline = pipeline("ner", model=model, tokenizer=tokenizer, aggregation_strategy="simple")

def extraer_producto_transformer(texto):
    entidades = ner_pipeline(texto)
    productos = [ent['word'] for ent in entidades if ent['entity_group'] == "MISC"]
    return productos[0] if productos else None
