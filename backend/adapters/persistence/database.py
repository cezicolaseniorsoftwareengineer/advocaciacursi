"""
Configuração de banco de dados com SQLAlchemy para Neon PostgreSQL.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from backend.shared.config import Config
from backend.domain.models import Base
from typing import Generator

# Engine para Neon PostgreSQL
engine = create_engine(
    Config.DATABASE_URL,
    echo=Config.DEBUG,
    pool_pre_ping=True,  # Verifica conexão antes de usar
    pool_recycle=3600,   # Recicla conexões a cada hora
)

# SessionLocal para criar sessões de banco de dados
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db():
    """Inicializa o banco de dados, criando as tabelas."""
    Base.metadata.create_all(bind=engine)


def get_db() -> Generator[Session, None, None]:
    """Dependency injection para sessão do banco de dados."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
