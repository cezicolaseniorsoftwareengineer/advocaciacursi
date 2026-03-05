"""
Domain models for the Dr. Estevão AI Chat Agent.
Entities, Value Objects, and Business Logic.
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import uuid4


class ContactRequestStatus(str, Enum):
    """État du contact - pas encore convertis en leads."""
    INTERESTED = "interested"
    CONFIRMED = "confirmed"
    REJECTED = "rejected"


@dataclass
class Message:
    """Valeur object representing a single message in the conversation."""

    role: str
    content: str
    id: str = field(default_factory=lambda: str(uuid4()))
    timestamp: datetime = field(default_factory=datetime.utcnow)


@dataclass
class ConversationContext:
    """Value object para armazenar contexto da conversa."""

    user_name: Optional[str] = None
    user_email: Optional[str] = None
    user_phone: Optional[str] = None
    legal_areas_mentioned: list[str] = field(default_factory=list)
    conversation_summary: str = ""
    contact_interest_level: int = 0  # 0-10 scale


@dataclass
class ChatSession:
    """Aggregate root para uma sessão de chat."""

    id: str = field(default_factory=lambda: str(uuid4()))
    session_token: str = field(default_factory=lambda: str(uuid4()))
    messages: list[Message] = field(default_factory=list)
    context: ConversationContext = field(default_factory=ConversationContext)
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    is_active: bool = True

    def add_message(self, role: str, content: str) -> Message:
        """Add a new message to the conversation."""
        message = Message(role=role, content=content)
        self.messages.append(message)
        self.updated_at = datetime.utcnow()
        return message

    def set_contact_context(
        self,
        name: Optional[str] = None,
        email: Optional[str] = None,
        phone: Optional[str] = None,
    ):
        """Update contact information during conversation."""
        if name:
            self.context.user_name = name
        if email:
            self.context.user_email = email
        if phone:
            self.context.user_phone = phone


@dataclass
class ContactRequest:
    """Aggregate root para um pedido de contato apos confirmacao do cliente."""

    chat_session_id: str
    client_name: str
    client_email: str
    client_phone: str
    legal_areas: list = field(default_factory=list)
    conversation_summary: str = ""
    id: str = field(default_factory=lambda: str(uuid4()))

    def confirm(self):
        """Mark contact request as confirmed by client."""
        self.status = ContactRequestStatus.CONFIRMED

    def reject(self):
        """Mark contact request as rejected."""
        self.status = ContactRequestStatus.REJECTED
