from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from backend.application.chat_service import ChatService
from backend.adapters.persistence.database import get_db
from backend.ports.in.schemas import (
    InitChatRequest,
    InitChatResponse,
    SendMessageRequest,
    SendMessageResponse,
    CreateContactRequest,
    CreateContactResponse,
)

router = APIRouter(prefix="/api/v1/chat", tags=["chat"])


@router.post("/init", response_model=InitChatResponse)
async def init_chat(request: InitChatRequest, db: Session = Depends(get_db)):
    """Iniciar sessao de chat."""
    try:
        chat_service = ChatService(db)
        session = chat_service.create_session()
        initial_message = "Ola! Sou o Dr. Estevao.\n\nFico feliz em conectar! Posso ajuda-lo com uma avaliacao inicial do seu caso.\n\nQual eh a sua situacao?"
        session.add_message("assistant", initial_message)
        chat_service.session_repo.save(session)
        return InitChatResponse(
            session_token=session.session_token,
            message=initial_message,
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


@router.post("/message", response_model=SendMessageResponse)
async def send_message(request: SendMessageRequest, db: Session = Depends(get_db)):
    """Enviar mensagem."""
    try:
        chat_service = ChatService(db)
        session = chat_service.get_session(request.session_token)
        if not session:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Sessao nao encontrada",
            )
        response = chat_service.send_message(session, request.message)
        if not response:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Erro IA",
            )
        suggests_contact = "agendar" in response.lower()
        return SendMessageResponse(
            session_token=session.session_token,
            response=response,
            suggests_contact=suggests_contact,
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


@router.post("/contact", response_model=CreateContactResponse)
async def create_contact(request: CreateContactRequest, db: Session = Depends(get_db)):
    """Criar pedido de contato."""
    try:
        chat_service = ChatService(db)
        session = chat_service.get_session(request.session_token)
        if not session:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Sessao nao encontrada",
            )
        contact = chat_service.create_contact_request(
            session=session,
            client_name=request.client_name,
            client_email=request.client_email,
            client_phone=request.client_phone,
        )
        return CreateContactResponse(
            success=True,
            request_id=contact.id,
            message=f"Obrigado! Entraremos em contato.",
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )
