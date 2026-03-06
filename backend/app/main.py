from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from backend.ports.chat_routes import router as chat_router

# Project root = two levels up from this file (backend/app/main.py -> project root)
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent

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

# API routes (must be registered before static files)
app.include_router(chat_router)


@app.get("/api/v1/health")
async def health_check():
    return {
        "status": "ok",
        "message": "Dr. Estevao AI Agent rodando com sucesso",
        "database": "In-memory (MVP - Neon em produção)",
    }


# Serve static frontend assets
app.mount("/css", StaticFiles(directory=str(PROJECT_ROOT / "css")), name="css")
app.mount("/js", StaticFiles(directory=str(PROJECT_ROOT / "js")), name="js")
app.mount("/pages", StaticFiles(directory=str(PROJECT_ROOT / "pages")), name="pages")
app.mount("/admin", StaticFiles(directory=str(PROJECT_ROOT / "admin")), name="admin")


@app.get("/blog.html")
async def serve_blog():
    return FileResponse(str(PROJECT_ROOT / "blog.html"))


@app.get("/img.png")
async def serve_logo():
    return FileResponse(str(PROJECT_ROOT / "img.png"), media_type="image/png")


@app.get("/img_cursi.png")
async def serve_img_cursi():
    return FileResponse(str(PROJECT_ROOT / "img_cursi.png"), media_type="image/png")


@app.get("/video_cursi.mp4")
async def serve_video():
    return FileResponse(str(PROJECT_ROOT / "video_cursi.mp4"), media_type="video/mp4")


@app.get("/")
async def serve_index():
    return FileResponse(str(PROJECT_ROOT / "index.html"))
