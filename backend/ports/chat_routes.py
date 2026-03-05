from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
import uuid
from datetime import datetime
import sys
import os

# Adicionar path para importar agentes
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../'))

from backend.agents.dr_estevao import DrEstevaoAgent

router = APIRouter(prefix="/api/v1/chat", tags=["chat"])

# In-memory storage (temporario - sera Neon em produção)
sessions_store = {}
contacts_store = {}
agents_store = {}  # Armazenar instâncias do agente por sessão


class MessageRequest(BaseModel):
    session_token: str
    message: str


class ContactRequest(BaseModel):
    session_token: str
    client_name: str
    client_email: str
    client_phone: str
    preferencia_consulta: str = "online"


@router.post("/init")
async def init_chat():
    """Iniciar sessao do chat com Dr. Estevao."""
    try:
        session_token = str(uuid.uuid4())

        # Criar instância do agente para esta sessão
        agent = DrEstevaoAgent()
        agents_store[session_token] = agent

        # Inicializar o agente (já coloca saudação)
        agent.process_message("Iniciar conversa")

        # Pegar a mensagem de saudação
        greeting_msg = agent.conversation_history[-1]["content"]

        sessions_store[session_token] = {
            "token": session_token,
            "messages": [
                {"role": "assistant", "content": greeting_msg}
            ],
            "user_name": None,
            "user_email": None,
            "user_phone": None,
            "stage": "greeting",
            "created_at": datetime.utcnow().isoformat(),
        }

        return {
            "session_token": session_token,
            "message": greeting_msg,
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao inicializar: {str(e)}",
        )


@router.post("/message")
async def send_message(data: MessageRequest):
    """Enviar mensagem e obter resposta do Dr. Estevao."""
    try:
        session_token = data.session_token
        user_msg = data.message

        if not session_token or session_token not in sessions_store:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Sessao nao encontrada",
            )

        # Adicionar mensagem do usuário
        sessions_store[session_token]["messages"].append({
            "role": "user",
            "content": user_msg
        })

        # Obter agente da sessão
        agent = agents_store.get(session_token)
        if not agent:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Agente nao encontrado para questa sessao",
            )

        # Processar mensagem com o agente
        response_data = agent.process_message(user_msg)

        # Adicionar resposta do Dr. Estevao
        sessions_store[session_token]["messages"].append({
            "role": "assistant",
            "content": response_data["text"]
        })

        # Atualizar estágio
        sessions_store[session_token]["stage"] = response_data.get("stage", "qualification")

        # Definir flag para sugerir coleta de contato
        suggests_contact = response_data.get("stage") == "data_collection"

        return {
            "session_token": session_token,
            "response": response_data["text"],
            "suggests_contact": suggests_contact,
            "stage": response_data.get("stage"),
            "action": response_data.get("action")
        }
    except HTTPException:
        raise
    except Exception as e:
        print(f"Erro em send_message: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro: {str(e)}",
        )


@router.post("/contact")
async def create_contact(data: ContactRequest):
    """Criar pedido de contato e gerar mensagem WhatsApp."""
    try:
        session_token = data.session_token
        name = data.client_name
        email = data.client_email
        phone = data.client_phone
        preferencia_consulta = data.preferencia_consulta

        if not session_token or session_token not in sessions_store:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Sessao nao encontrada",
            )

        # Obter agente da sessão e coletar dados
        agent = agents_store.get(session_token)
        if agent:
            data_collected = agent.collect_client_data({
                "nome": name,
                "email": email,
                "telefone": phone,
                "preferencia_consulta": preferencia_consulta
            })

        contact_id = str(uuid.uuid4())

        # Gerar mensagem WhatsApp
        whatsapp_msg = agent.generate_whatsapp_message() if agent else f"Olá {name}, confirmo seu contato!"

        contacts_store[contact_id] = {
            "id": contact_id,
            "session_id": session_token,
            "name": name,
            "email": email,
            "phone": phone,
            "preferencia_consulta": preferencia_consulta,
            "created_at": datetime.utcnow().isoformat(),
            "whatsapp_message": whatsapp_msg,
        }

        sessions_store[session_token]["user_name"] = name
        sessions_store[session_token]["user_email"] = email
        sessions_store[session_token]["user_phone"] = phone
        sessions_store[session_token]["stage"] = "contact_registered"

        # Construir URL de WhatsApp para enviar a mensagem
        whatsapp_url = f"https://wa.me/5511985773185?text={whatsapp_msg.replace(' ', '%20').replace('\n', '%0A')}"

        return {
            "success": True,
            "request_id": contact_id,
            "client_name": name,
            "message": f"Perfeito, {name}! Vamos conectar via WhatsApp para confirmar sua consulta.",
            "whatsapp_link": whatsapp_url,
            "whatsapp_message": whatsapp_msg,
        }
    except HTTPException:
        raise
    except Exception as e:
        print(f"Erro em create_contact: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro: {str(e)}",
        )
