"""
Modelos SQLAlchemy para persistência em Neon PostgreSQL.
"""

from datetime import datetime
from sqlalchemy import Column, String, Text, DateTime, Integer, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import uuid

Base = declarative_base()


class ChatSessionModel(Base):
    """Modelo de sessão de chat persistida no banco."""

    __tablename__ = "chat_sessions"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    session_token = Column(String(255), unique=True, nullable=False, index=True)
    user_name = Column(String(255), nullable=True)
    user_email = Column(String(255), nullable=True)
    user_phone = Column(String(255), nullable=True)
    legal_area = Column(String(255), nullable=True)
    interest_level = Column(Integer, default=0)  # 0-10 scale
    conversation_count = Column(Integer, default=0)
    contact_requested = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relacionamento com mensagens
    messages = relationship("ChatMessageModel", back_populates="session", cascade="all, delete-orphan")
    contact_request = relationship("ContactRequestModel", back_populates="session", uselist=False, cascade="all, delete-orphan")


class ChatMessageModel(Base):
    """Modelo de mensagem individual no banco."""

    __tablename__ = "chat_messages"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    session_id = Column(String(36), ForeignKey("chat_sessions.id"), nullable=False)
    role = Column(String(50), nullable=False)  # "user" ou "assistant"
    content = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

    # Relacionamento com sessão
    session = relationship("ChatSessionModel", back_populates="messages")


class ContactRequestModel(Base):
    """Modelo de pedido de contato confirmado."""

    __tablename__ = "contact_requests"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    session_id = Column(String(36), ForeignKey("chat_sessions.id"), unique=True, nullable=False)
    client_name = Column(String(255), nullable=False)
    client_email = Column(String(255), nullable=False)
    client_phone = Column(String(255), nullable=False)
    legal_area = Column(String(255), nullable=True)
    interest_level = Column(Integer, default=0)
    status = Column(String(50), default="pending")  # pending, contacted, closed
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relacionamento com sessão
    session = relationship("ChatSessionModel", back_populates="contact_request")


class UserAuthModel(Base):
    """Modelo para autenticação de usuários (escritório)."""

    __tablename__ = "user_accounts"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String(255), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=True)
    role = Column(String(50), default="agent")  # admin, agent, viewer
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
