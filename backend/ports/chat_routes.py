from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from backend.application.chat_service import ChatService
from backend.adapters.persistence.database import get_db

router = APIRouter(prefix="/api/v1/chat", tags=["chat"])


@router.post("/init")
async def init_chat(db: Session = Depends(get_db)):
    """Iniciar sessao."""
    try:
        chat_service = ChatService(db)
        session = chat_service.create_session()
        msg = "Ola! Sou o Dr. Estevao. Como posso ajudar?"
        session.add_message("assistant", msg)
        chat_service.session_repo.save(session)
        return {
            "session_token": session.session_token,
            "message": msg,
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


@router.post("/message")
async def send_message(request_data: dict, db: Session = Depends(get_db)):
    """Enviar msg."""
    try:
        chat_service = ChatService(db)
        session = chat_service.get_session(request_data.get("session_token"))
        if not session:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Session not found",
            )
        response = chat_service.send_message(session, request_data.get("message"))
        if not response:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="IA error",
            )
        suggests_contact = "agendar" in response.lower()
        return {
            "session_token": session.session_token,
            "response": response,
            "suggests_contact": suggests_contact,
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


@router.post("/contact")
async def create_contact(request_data: dict, db: Session = Depends(get_db)):
    """Create contact."""
    try:
        chat_service = ChatService(db)
        session = chat_service.get_session(request_data.get("session_token"))
        if not session:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Session error",
            )
        contact = chat_service.create_contact_request(
            session=session,
            client_name=request_data.get("client_name"),
            client_email=request_data.get("client_email"),
            client_phone=request_data.get("client_phone"),
        )
        return {
            "success": True,
            "request_id": contact.id,
            "message": "OK!",
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )
