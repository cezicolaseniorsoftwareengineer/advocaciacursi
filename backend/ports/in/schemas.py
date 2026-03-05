"""
DTOs para requisições e respostas da API.
"""

from pydantic import BaseModel, EmailStr
from typing import Optional, List


class InitChatRequest(BaseModel):
    """Requisição para iniciar uma nova sessão de chat."""
    pass


class InitChatResponse(BaseModel):
    """Resposta com informações da nova sessão."""
    session_token: str
    message: str  # Mensagem inicial do Dr. Estevão


class SendMessageRequest(BaseModel):
    """Requisição para enviar mensagem."""
    session_token: str
    message: str


class SendMessageResponse(BaseModel):
    """Resposta com a mensagem do Dr. Estevão."""
    session_token: str
    response: str
    suggests_contact: bool = False  # Se Dr. Estevão sugerou contato


class CreateContactRequest(BaseModel):
    """Requisição para criar um contact request."""
    session_token: str
    client_name: str
    client_email: EmailStr
    client_phone: str


class CreateContactResponse(BaseModel):
    """Resposta após criar contact request."""
    success: bool
    request_id: str
    message: str


class HealthResponse(BaseModel):
    """Resposta de health check."""
    status: str
    message: str
