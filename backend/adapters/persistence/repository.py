"""
Repositorios para persistencia com SQLAlchemy (Neon PostgreSQL).
"""

from sqlalchemy.orm import Session
from backend.domain.chat import ChatSession, ContactRequest, Message
from backend.domain.models import (
    ChatSessionModel,
    ChatMessageModel,
    ContactRequestModel,
)
from typing import Optional


class ChatSessionRepository:
    """Repositorio para ChatSessions."""

    def __init__(self, db: Session):
        self.db = db

    def create(self, session: ChatSession):
        """Criar nova sessao."""
        db_session = ChatSessionModel(
            session_token=session.session_token,
            user_name=session.context.user_name,
            user_email=session.context.user_email,
            user_phone=session.context.user_phone,
            legal_area=session.context.legal_area,
            interest_level=session.context.contact_interest_level,
        )
        for msg in session.messages:
            db_msg = ChatMessageModel(role=msg.role, content=msg.content)
            db_session.messages.append(db_msg)
        self.db.add(db_session)
        self.db.commit()
        self.db.refresh(db_session)
        return self._to_domain(db_session)

    def get_by_token(self, session_token: str):
        """Obter sessao pelo token."""
        db = self.db.query(ChatSessionModel).filter(
            ChatSessionModel.session_token == session_token
        ).first()
        if not db:
            return None
        return self._to_domain(db)

    def save(self, session: ChatSession):
        """Salvar sessao."""
        db = self.db.query(ChatSessionModel).filter(
            ChatSessionModel.session_token == session.session_token
        ).first()
        if db:
            db.user_name = session.context.user_name
            db.user_email = session.context.user_email
            db.user_phone = session.context.user_phone
            db.legal_area = session.context.legal_area
            db.interest_level = session.context.contact_interest_level
            db.conversation_count = len(session.messages)
            db.messages.clear()
            for msg in session.messages:
                db_msg = ChatMessageModel(role=msg.role, content=msg.content)
                db.messages.append(db_msg)
            self.db.commit()

    def _to_domain(self, db_session):
        """Converter para dominio."""
        from backend.domain.chat import ConversationContext
        ctx = ConversationContext(
            user_name=db_session.user_name,
            user_email=db_session.user_email,
            user_phone=db_session.user_phone,
            legal_area=db_session.legal_area,
            contact_interest_level=db_session.interest_level,
        )
        messages = [
            Message(role=msg.role, content=msg.content)
            for msg in db_session.messages
        ]
        session = ChatSession(session_token=db_session.session_token, context=ctx)
        session.messages = messages
        return session


class ContactRequestRepository:
    """Repositorio para ContactRequests."""

    def __init__(self, db: Session):
        self.db = db

    def create(self, contact):
        """Criar pedido de contato."""
        db_contact = ContactRequestModel(
            session_id=contact.chat_session_id,
            client_name=contact.client_name,
            client_email=contact.client_email,
            client_phone=contact.client_phone,
        )
        self.db.add(db_contact)
        self.db.commit()
        self.db.refresh(db_contact)
        return self._to_domain(db_contact)

    def get_by_session_id(self, session_id: str):
        """Obter por sessao."""
        db = self.db.query(ContactRequestModel).filter(
            ContactRequestModel.session_id == session_id
        ).first()
        if not db:
            return None
        return self._to_domain(db)

    def _to_domain(self, db_contact):
        """Converter para dominio."""
        return ContactRequest(
            chat_session_id=db_contact.session_id,
            client_name=db_contact.client_name,
            client_email=db_contact.client_email,
            client_phone=db_contact.client_phone,
        )
