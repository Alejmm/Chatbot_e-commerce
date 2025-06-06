from fastapi import FastAPI
from app.routes import chatbot, prediction

app = FastAPI()

app.include_router(chatbot.router, prefix='/chatbot')
app.include_router(prediction.router, prefix='/predict')

@app.get('/')
def read_root():
    return {"message": "API funcionando"}
