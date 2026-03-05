from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from backend.adapters.persistence.database import init_db
from backend.ports.chat_routes import router as chat_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Inicializar banco de dados ao ligar o app."""
    print("🚀 Inicializando Neon PostgreSQL...")
    try:
        init_db()
        print("✅ Banco de dados inicializado com sucesso!")
    except Exception as e:
        print(f"❌ Erro ao inicializar banco: {str(e)}")
    yield
    # Cleanup (se necessário) depois que o app desligar
    print("🔴 Encerrando aplicação")


app = FastAPI(
    title="Dr. Estevao AI Agent",
    description="Backend para o agente de IA Dr. Estevao.",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5500",
        "http://127.0.0.1:5500",
        "https://*.onrender.com",
        "http://advocaciacursi.com.br",
        "https://advocaciacursi.com.br",
    ],
    allow_credentials=True,
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
        "database": "Neon PostgreSQL"
    }
