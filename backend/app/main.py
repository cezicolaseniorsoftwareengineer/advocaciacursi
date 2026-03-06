from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.ports.chat_routes import router as chat_router

app = FastAPI(
    title="Dr. Estevao AI Agent",
    description="Backend para o agente de IA Dr. Estevao.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir rotas de chat
app.include_router(chat_router)


@app.get("/api/v1/health")
async def health_check():
    return {
        "status": "ok",
        "message": "Dr. Estevao AI Agent rodando com sucesso 🚀",
        "database": "In-memory (MVP - Neon em produção)",
    }
