"""
Adapter para integração com OpenRouter API.
"""

import requests
import json
from typing import Optional
from backend.shared.config import Config
from backend.domain.chat import Message


class OpenRouterAdapter:
    """Adapter para comunicar com a API OpenRouter."""

    def __init__(self):
        self.api_key = Config.OPENROUTER_API_KEY
        self.base_url = Config.OPENROUTER_BASE_URL
        self.model = Config.OPENROUTER_MODEL

    def send_message(
        self,
        messages: list[Message],
        system_prompt: str,
    ) -> Optional[str]:
        """
        Enviar mensagens para o OpenRouter e obter resposta do Dr. Estevão.

        Args:
            messages: Lista de mensagens da conversa
            system_prompt: System prompt com a persona do Dr. Estevão

        Returns:
            Resposta do modelo ou None em caso de erro
        """

        try:
            # Formatar mensagens para o OpenRouter
            formatted_messages = [
                {"role": msg.role, "content": msg.content}
                for msg in messages
            ]

            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
                "HTTP-Referer": "http://advocaciacursi.com.br",
                "X-Title": "Dr. Estevão Cursi AI Chat",
            }

            payload = {
                "model": self.model,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    *formatted_messages,
                ],
                "temperature": 0.7,
                "max_tokens": 1024,
            }

            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=headers,
                json=payload,
                timeout=30,
            )

            if response.status_code != 200:
                print(f"OpenRouter error: {response.status_code} - {response.text}")
                return None

            data = response.json()
            return data["choices"][0]["message"]["content"]

        except Exception as e:
            print(f"Error communicating with OpenRouter: {str(e)}")
            return None
