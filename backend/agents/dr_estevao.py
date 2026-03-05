"""
Dr. Estevão - AI Agent para atendimento jurídico
Especializado em: Direito Trabalhista, Consultoria Legal
Objetivo: Qualificar leads, coletar dados e agendar consultas
"""

import random
import json
from datetime import datetime
from typing import Optional, Dict, List

class DrEstevaoAgent:
    """Agente IA para atendimento jurídico fluido e vendas consultivas"""

    def __init__(self):
        self.conversation_stage = "greeting"  # Estágios: greeting, qualification, solution, closing, follow_up
        self.client_data = {
            "nome": None,
            "email": None,
            "telefone": None,
            "tipo_caso": None,
            "descricao": None,
            "urgencia": None,
            "preferencia_consulta": None  # "presencial" ou "online"
        }
        self.conversation_history = []
        self.ai_responses_attempt = 0

    def get_greeting_responses(self) -> List[str]:
        """Saudações variadas e acolhedoras"""
        return [
            "Olá! Sou o Dr. Estevão, advogado especializado em Direito Trabalhista. "
            "Como posso ajudá-lo hoje?",

            "Bem-vindo! Meu nome é Dr. Estevão. Estou aqui para ouvir sobre sua situação "
            "e ajudá-lo com questões trabalhistas e legais. O que o traz aqui?",

            "Oi! Sou Dr. Estevão. Tenho mais de 15 anos de experiência em casos trabalhistas. "
            "Gostaria de saber: qual é o seu caso?",
        ]

    def get_qualification_responses(self, user_input: str) -> Dict:
        """Qualifica o lead com respostas fluidas e perguntas estratégicas"""

        # Mapeamento de palavras-chave e sua intenção
        intent_keywords = {
            "demissao": {
                "keywords": ["demitido", "demissão", "despedido", "demitem", "desligamento"],
                "response": "Entendi. Demissões sem justa causa são muito comuns e temos "
                           "ampla jurisprudência a favor do trabalhador. Você recebeu "
                           "aviso prévio ou foi demitido sem justificativa?",
                "intent": "demissao"
            },
            "assedio": {
                "keywords": ["assédio", "assedio", "humilhação", "constrangimento", "perseguição"],
                "response": "Assédio moral é extremamente grave e temos muitos casos ganhos. "
                           "Você tem documentação ou testemunhas? Por quanto tempo isso vem acontecendo?",
                "intent": "assedio_moral"
            },
            "horas_extras": {
                "keywords": ["horas extras", "hora extra", "horas adicionais", "trabalho extra"],
                "response": "Horas extras não pagas é direito seu! Você tem controle de ponto "
                           "ou alguma forma de comprovar essas horas?",
                "intent": "horas_extras"
            },
            "rescisao": {
                "keywords": ["rescisão", "rescisao", "acertos", "fgts", "13º"],
                "response": "Rescisão indevida é frequente. Você recebeu seu FGTS, 13º e acertos? "
                           "Temos uma análise rápida que fazemos.",
                "intent": "rescisao_irregular"
            },
            "discriminacao": {
                "keywords": ["discriminação", "discriminacao", "preconceito", "racismo", "homofobia"],
                "response": "Discriminação no trabalho é vedada por lei. Você tem registros ou "
                           "testemunhas dessa discriminação?",
                "intent": "discriminacao"
            },
            "beneficio": {
                "keywords": ["seguro desemprego", "desemprego", "bolsa família", "benefício", "beneficio"],
                "response": "Temos equipe especializada em benefícios trabalhistas. Sua demissão "
                           "foi registrada na carteira?",
                "intent": "beneficio_trabalhista"
            }
        }

        user_lower = user_input.lower()

        # Procurar por palavras-chave de forma inteligente
        for case_type, case_info in intent_keywords.items():
            for keyword in case_info["keywords"]:
                if keyword in user_lower:
                    self.client_data["tipo_caso"] = case_info["intent"]
                    return {
                        "response": case_info["response"],
                        "stage": "deeper_qualification",
                        "intent": case_info["intent"]
                    }

        # Se não encontrar palavra-chave, fazer pergunta genérica
        return {
            "response": (
                "Entendi. Para que eu possa melhor ajudá-lo, poderia me contar mais detalhes "
                "sobre seu caso? Tenho experiência em: demissões, assédio moral, horas extras, "
                "rescisão indevida, discriminação, benéfícios trabalhistas. Como posso ajudar?"
            ),
            "stage": "deeper_qualification",
            "intent": "generic"
        }

    def get_solution_response(self, user_input: str) -> Dict:
        """Apresenta solução consultiva"""

        solutions = {
            "demissao": (
                "Baseado no que você me contou, você pode ter direito a:\n"
                "• Aviso prévio indenizado\n"
                "• Fundo de Garantia (FGTS)\n"
                "• 13º salário proporcional\n"
                "• Indenização por danos morais\n\n"
                "Normalmente conquistamos entre 2 a 12 meses de salário em indenizações. "
                "Gostaria de entender melhor seu caso com uma consulta?"
            ),
            "assedio_moral": (
                "Assédio moral é crime! Você pode receber:\n"
                "• Indenização por dano moral (normalmente R$ 5mil a 50mil)\n"
                "• Rescisão indireta com direitos trabalhistas\n"
                "• Reintegração ao emprego se desejar\n\n"
                "Temos vários casos ganhos. Preciso de mais detalhes via consulta completa."
            ),
            "horas_extras": (
                "Horas extras não pagas geram:\n"
                "• Pagamento das horas + 50% adicional (RSR)\n"
                "• Possível multa ao empregador\n"
                "• Efeito cascata (FGTS, 13º, férias)\n\n"
                "Você lembra aproximadamente quantas horas extras mensais acumula?"
            ),
            "rescisao_irregular": (
                "Rescisão irregular pode render:\n"
                "• Reconhecimento da relação de emprego\n"
                "• Remuneração integral do período\n"
                "• Indenizações adicionais\n\n"
                "Para isso, precisarei de documentos. Podemos agendar uma consulta para análise?"
            ),
            "discriminacao": (
                "Discriminação tem penas severas:\n"
                "• Indenização por dano moral (valor alto)\n"
                "• Possível reintegração\n"
                "• Rescisão indireta com benefícios\n\n"
                "Você teria como documentar esses casos de discriminação?"
            ),
            "beneficio_trabalhista": (
                "Conheço bem os trâmites do seguro-desemprego e benefícios:\n"
                "• Análise do direito ao benefício\n"
                "• Recursos em caso de negado\n"
                "• Amparo jurídico durante análise\n\n"
                "Quando foi sua demissão exatamente?"
            )
        }

        intent = self.client_data.get("tipo_caso", "generic")
        response = solutions.get(intent,
            "Com base no seu relato, acredito que podemos ajudar! "
            "Você tem direitos que precisam ser protegidos. "
            "Vamos marcar uma consulta para análise completa?"
        )

        return {
            "response": response,
            "stage": "closing",
            "intent": intent
        }

    def get_closing_response(self) -> Dict:
        """Fecha a venda de uma consulta"""

        closing_scripts = [
            (
                "Perfeito! Vejo que temos oportunidade real de recuperar seus direitos. "
                "Como próximo passo, gostaria de agendar uma consulta? "
                "Você prefere **presencial** aqui no escritório ou **online** (mais rápido)?\n\n"
                "Posso coletar seus dados e já agendar?"
            ),
            (
                "Sua situação é bem clara e recuperável! "
                "Recomendo uma consulta de 30min onde vamos:\n"
                "1) Analisar documentos\n"
                "2) Calcular possível indenização\n"
                "3) Definir estratégia\n\n"
                "Qual formato funciona melhor: **presencial** ou **por vídeo**?"
            ),
            (
                "Excelente! Tenho certeza que conseguinos reverter essa situação. "
                "Consulta comigo é sem custo inicial e sem compromisso.\n\n"
                "Me passa seus dados (nome, email, whatsapp) e sua preferência de horário?"
            )
        ]

        return {
            "response": random.choice(closing_scripts),
            "stage": "data_collection",
            "action": "collect_data"
        }

    def process_message(self, user_input: str) -> Dict:
        """Processa mensagem do usuário e retorna resposta do agente"""

        # Registrar no histórico
        self.conversation_history.append({
            "timestamp": datetime.now().isoformat(),
            "role": "user",
            "content": user_input
        })

        # Determinar próximo estágio
        if self.conversation_stage == "greeting":
            response = {
                "text": random.choice(self.get_greeting_responses()),
                "stage": "qualification"
            }
            self.conversation_stage = "qualification"

        elif self.conversation_stage == "qualification":
            result = self.get_qualification_responses(user_input)
            response = {
                "text": result["response"],
                "stage": result["stage"],
                "intent": result.get("intent")
            }
            self.conversation_stage = "deeper_qualification"

        elif self.conversation_stage in ["deeper_qualification", "deeper_info"]:
            # Coletar mais informações antes de apresentar solução
            if self.ai_responses_attempt < 2:
                result = self.get_qualification_responses(user_input)
                response = {
                    "text": result["response"],
                    "stage": "deeper_qualification",
                    "intent": result.get("intent")
                }
                self.ai_responses_attempt += 1
            else:
                # Apresentar solução
                result = self.get_solution_response(user_input)
                response = {
                    "text": result["response"] + "\n\n🎯 **Vamos agendar sua consulta?**",
                    "stage": "closing",
                    "action": "present_solution"
                }
                self.conversation_stage = "closing"
                self.ai_responses_attempt = 0

        elif self.conversation_stage == "closing":
            result = self.get_closing_response()
            response = {
                "text": result["response"],
                "stage": "data_collection",
                "action": "collect_data"
            }
            self.conversation_stage = "data_collection"

        else:
            response = {
                "text": "Como posso continuar ajudando?",
                "stage": self.conversation_stage
            }

        # Registrar resposta
        self.conversation_history.append({
            "timestamp": datetime.now().isoformat(),
            "role": "assistant",
            "content": response["text"]
        })

        return response

    def collect_client_data(self, data: Dict) -> Dict:
        """Coleta dados do cliente após qualificação"""

        update_fields = ["nome", "email", "telefone", "preferencia_consulta"]

        for field in update_fields:
            if field in data:
                self.client_data[field] = data[field]

        return {
            "status": "collected",
            "client_data": self.client_data,
            "next_action": "send_whatsapp",
            "message": f"Ótimo {self.client_data.get('nome', 'Cliente')}! "
                      f"Vou confirmar sua consulta {"presencial"
                      if self.client_data.get('preferencia_consulta') == 'presencial'
                      else 'online'} via WhatsApp!"
        }

    def generate_whatsapp_message(self) -> str:
        """Gera mensagem de confirmação para enviar via WhatsApp"""

        consulta_tipo = self.client_data.get("preferencia_consulta", "online")
        tipo_caso = self.client_data.get("tipo_caso", "Direito Trabalhista").replace("_", " ").title()

        message = (
            f"Olá {self.client_data.get('nome', 'Cliente')}!\n\n"
            f"Confirmo sua consulta *{consulta_tipo.title()}* com o Dr. Estevão!\n"
            f"📋 Tipo de caso: {tipo_caso}\n"
            f"📅 Nos próximos 2 dias úteis você receberá um horário disponível\n"
            f"💰 Consulta inicial sem custo\n\n"
            f"Para qualquer dúvida, é só chamar! 😊"
        )

        return message


# Exemplo de uso
if __name__ == "__main__":
    agent = DrEstevaoAgent()

    # Simulação de conversa
    print("🤖 Dr. Estevão iniciando...\n")

    # Primeira mensagem (saudação)
    response = agent.process_message("Oi, tenho um problema no trabalho")
    print(f"Dr.E: {response['text']}\n")

    # Segunda mensagem (qualificação)
    response = agent.process_message("Fui demitido sem justa causa")
    print(f"Dr.E: {response['text']}\n")

    # Terceira mensagem (aprofundamento)
    response = agent.process_message("Não recebi aviso, só me chamaram para assinar rescisão")
    print(f"Dr.E: {response['text']}\n")

    # Quarta mensagem (solução)
    response = agent.process_message("Tenho registros de tudo isso")
    print(f"Dr.E: {response['text']}\n")
