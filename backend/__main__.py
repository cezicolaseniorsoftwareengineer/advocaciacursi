"""
Entry point para executar o backend Dr. Estevão AI Chat.
"""

import uvicorn
from backend.shared.config import Config

if __name__ == "__main__":
    uvicorn.run(
        "backend.app.main:app",
        host=Config.HOST,
        port=Config.PORT,
        reload=Config.DEBUG,
        log_level="info",
    )
