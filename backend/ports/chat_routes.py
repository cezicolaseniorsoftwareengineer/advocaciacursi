from fastapi import APIRouter, HTTPException, status
import uuid
from datetime import datetime

router = APIRouter(prefix="/api/v1/chat", tags=["chat"])

# In-memory storage (temporario - sera Neon em produção)
sessions_store = {}
contacts_store = {}


@router.post("/init")
async def init_chat():
    """Iniciar sessao."""
    try:
        session_token = str(uuid.uuid4())
        sessions_store[session_token] = {
            "token": session_token,
            "messages": [],
            "user_name": None,
            "user_email": None,
            "user_phone": None,
        }

        msg = """Ola! Sou o Dr. Estevao. :)

Fico feliz em conectar com voce! Posso ajuda-lo com uma avaliacao inicial do seu caso e, se quiser, registrar seu pedido de contato com o escritorio para um atendimento prioritario.

Conte-me: qual eh a sua situacao?"""

        sessions_store[session_token]["messages"].append({
            "role": "assistant",
            "content": msg
        })

        return {
            "session_token": session_token,
            "message": msg,
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao inicializar: {str(e)}",
        )


@router.post("/message")
async def send_message(data: dict):
    """Enviar mensagem."""
    try:
        session_token = data.get("session_token")
        user_msg = data.get("message")

        if not session_token or session_token not in sessions_store:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Sessao nao encontrada",
            )

        sessions_store[session_token]["messages"].append({
            "role": "user",
            "content": user_msg
        })

        # Resposta do Dr. Estevao (mock)
        response = f"""Entendo sua situacao: '{user_msg}'.

Para ajuda-lo melhor, gostaria saber:
1. Qual area do direito eh mais relevante?
2. Qual eh a urgencia?
3. Ja consultou outro advogado?

Posso fazer uma avaliacao inicial e registrar seu pedido de contato para uma consulta."""

        sessions_store[session_token]["messages"].append({
            "role": "assistant",
            "content": response
        })

        suggests_contact = any(x in user_msg.lower() for x in ["agendar", "consulta", "contato"])

        return {
            "session_token": session_token,
            "response": response,
            "suggests_contact": suggests_contact,
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro: {str(e)}",
        )


@router.post("/contact")
async def create_contact(data: dict):
    """Criar pedido de contato."""
    try:
        session_token = data.get("session_token")
        name = data.get("client_name")
        email = data.get("client_email")
        phone = data.get("client_phone")

        if not session_token or session_token not in sessions_store:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Sessao nao encontrada",
            )

        contact_id = str(uuid.uuid4())
        contacts_store[contact_id] = {
            "id": contact_id,
            "session_id": session_token,
            "name": name,
            "email": email,
            "phone": phone,
            "created_at": datetime.utcnow().isoformat(),
        }

        sessions_store[session_token]["user_name"] = name
        sessions_store[session_token]["user_email"] = email
        sessions_store[session_token]["user_phone"] = phone

        return {
            "success": True,
            "request_id": contact_id,
            "message": f"Obrigado, {name}! Dr. Estevao entrara em contato em breve.",
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro: {str(e)}",
        )
