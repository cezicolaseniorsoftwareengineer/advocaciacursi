"""
Application service - Orquestra a lógica de conversação e captura de leads.
"""

from typing import Optional
from sqlalchemy.orm import Session
from backend.domain.chat import ChatSession, ContactRequest, Message
from backend.adapters.external.openrouter import OpenRouterAdapter
from backend.adapters.persistence.repository import (
    ChatSessionRepository,
    ContactRequestRepository,
)
from backend.shared.config import DrEstevaoPrompt


class ChatService:
    """Serviço de aplicação para gerenciar chat sessions."""

    def __init__(self, db: Session):
        self.db = db
        self.openrouter = OpenRouterAdapter()
        self.session_repo = ChatSessionRepository(db)
        self.contact_repo = ContactRequestRepository(db)
        self.dr_estevao_prompt = DrEstevaoPrompt.SYSTEM_PROMPT

    def create_session(self) -> ChatSession:
        """Criar uma nova sessão de chat."""
        session = ChatSession()
        self.session_repo.create(session)
        return session

    def get_session(self, session_token: str) -> Optional[ChatSession]:
        """Recuperar uma sessão pelo token."""
        return self.session_repo.get_by_token(session_token)

    def send_message(self, session: ChatSession, user_message: str) -> Optional[str]:
        """
        Processar mensagem do usuário e obter resposta do Dr. Estevão.
        """
        # Adicionar mensagem do usuário
        session.add_message("user", user_message)

        # Analisar intenção (detecção simples de palavras-chave)
        self._analyze_user_intent(session, user_message)

        # Obter resposta do OpenRouter
        response = self.openrouter.send_message(
            messages=session.messages,
            system_prompt=self.dr_estevao_prompt,
        )

        if response:
            # Adicionar resposta do assistente
            session.add_message("assistant", response)
            self.session_repo.save(session)
            return response

        return None

    def _analyze_user_intent(self, session: ChatSession, message: str):
        """Analisar a mensagem do usuário para extrair contexto."""
        msg_lower = message.lower()

        # Palavras-chave por área legal
        legal_areas_keywords = {
            "Execução Cível e Trabalhista": [
                "trabalhista", "rescisão", "aviso prévio", "fgts", "execução",
                "cível", "dívida", "contrato", "cobrança",
            ],
            "Assessoria Empresarial": [
                "empresa", "negócio", "contrato", "sócio", "constituição",
                "sociedade", "consultoria",
            ],
            "Prisões e Defesa Criminal": [
                "crime", "criminal", "preso", "prisão", "acusado", "defesa",
                "devido processo",
            ],
            "Direito da Saúde": [
                "médico", "erro médico", "saúde", "medicamento", "tratamento",
                "hospital", "plano de saúde",
            ],
            "Direito do Consumidor": [
                "consumidor", "produto", "vício", "devolução", "abuso",
                "publicidade enganosa",
            ],
            "Direito Imobiliário": [
                "imóvel", "propriedade", "aluguel", "locação", "compra",
                "venda", "moradia", "terreno",
            ],
            "Direito Tributário": [
                "imposto", "IRPF", "empresa", "fiscal", "receita", "tributo",
                "tax",
            ],
            "Direito Previdenciário": [
                "aposentadoria", "inss", "pensão", "benefício", "contribuição",
                "previdência",
            ],
            "Direito de Família": [
                "família", "casamento", "divórcio", "guarda", "pensão", "filhos",
                "herança", "sucessão",
            ],
        }

        for area, keywords in legal_areas_keywords.items():
            for keyword in keywords:
                if keyword in msg_lower and area not in session.context.legal_areas_mentioned:
                    session.context.legal_areas_mentioned.append(area)
                    break

        # Detectar interesse em contato (palavras-chave)
        contact_interest_keywords = [
            "agendar", "consulta", "contato", "telefone", "email",
            "preciso", "gostaria", "pode me ajudar",
        ]
        for keyword in contact_interest_keywords:
            if keyword in msg_lower:
                session.context.contact_interest_level = min(
                    10, session.context.contact_interest_level + 2
                )

    def create_contact_request(
        self,
        session: ChatSession,
        client_name: str,
        client_email: str,
        client_phone: str,
    ) -> ContactRequest:
        """
        Criar um pedido de contato confirmado pelo cliente.
        """
        if not session.context.legal_areas_mentioned:
            # Se não temos áreas identificadas, assume contato geral
            session.context.legal_areas_mentioned = ["Contato Geral"]

        contact_request = ContactRequest(
            chat_session_id=session.id,
            client_name=client_name,
            client_email=client_email,
            client_phone=client_phone,
            legal_areas=session.context.legal_areas_mentioned,
            conversation_summary=self._summarize_conversation(session),
        )

        contact_request.confirm()
        self.contact_repo.save(contact_request)
        session.is_active = False
        self.session_repo.save(session)

        return contact_request

    def _summarize_conversation(self, session: ChatSession) -> str:
        """Criar um resumo da conversa."""
        if not session.messages:
            return "Nova conversa iniciada."

        # Simples: pegar os últimos 3 mensagens do usuário como contexto
        user_messages = [m.content for m in session.messages if m.role == "user"][-3:]
        return " | ".join(user_messages) if user_messages else "Sem mensagens de usuário."
