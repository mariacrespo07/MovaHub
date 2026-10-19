# criar uma api

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="MovaHub API",
    description="Backend da plataforma MovaHub",
    version="1.0.0"
)

# Permite a comunicação com o frontend local
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500",
        "http://127.0.0.1:8000",
        "http://localhost:8000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.get("/")
def inicio():
    return {
        "mensagem": "Backend do MovaHub funcionando!"
    }


@app.get("/health")
def verificar_status():
    return {
        "status": "online"
    }
