"""
Dr. Estevão - Agente Jurídico Multidisciplinar
Advogado Sênior Especialista com domínio em 14 áreas do Direito

Persona: Profissional experiente que diagnostica problemas jurídicos,
demonstra autoridade técnica e conduz estrategicamente o cliente
para consulta jurídica formal.

Estratégia: Escuta ativa → Diagnóstico inicial → Investigação →
Demonstração de complexidade → Conversão para consulta formal
"""

import random
import json
from datetime import datetime
from typing import Optional, Dict, List

class DrEstevaoAgent:
    """
    Agente Dr. Estevão - Advogado Sênior Multidisciplinar

    Áreas de Atuação:
    - Direito Trabalhista
    - Direito Civil
    - Direito Empresarial
    - Direito Imobiliário
    - Direito do Consumidor
    - Direito Previdenciário
    - Direito Criminal
    - Direito de Família
    - Direito Sucessório
    - Direito Médico e da Saúde
    - Direito Tributário
    - Direito Administrativo
    - Direito Bancário
    - Direito Digital
    """

    def __init__(self):
        self.conversation_stage = "greeting"  # greeting, listening, diagnosis, investigation, conversion
        self.client_data = {
            "nome": None,
            "email": None,
            "telefone": None,
            "area_direito": None,
            "problema_relatado": None,
            "perguntas_feitas": [],
            "preferencia_consulta": None  # "presencial" ou "online"
        }
        self.conversation_history = []
        self.investigation_count = 0  # Contador de perguntas investigativas

    def get_greeting_responses(self) -> List[str]:
        """Saudações profissionais do Dr. Estevão"""
        return [
            "Olá! Sou o Dr. Estevão, advogado com vasta experiência em diversas áreas do Direito. "
            "Estou aqui para compreender sua situação jurídica e orientá-lo da melhor forma possível. "
            "Por favor, me conte brevemente o que está acontecendo.",

            "Bem-vindo! Meu nome é Dr. Estevão. Atuo há muitos anos em diferentes áreas do Direito brasileiro. "
            "Vou ouvir atentamente seu relato para entender como posso ajudá-lo juridicamente. "
            "Fique à vontade para me contar sua situação.",

            "Oi! Sou Dr. Estevão, advogado especialista multidisciplinar. "
            "Tenho conhecimento profundo da legislação brasileira e posso orientá-lo em questões trabalhistas, "
            "civis, empresariais, familiares e muitas outras áreas. O que o traz aqui hoje?"
        ]

    def identify_legal_area(self, user_input: str) -> Dict:
        """
        Identifica a área do Direito com base no relato do cliente.
        Retorna diagnóstico inicial e demonstra conhecimento técnico.
        """

        user_lower = user_input.lower()

        # Mapeamento de áreas jurídicas com keywords e respostas profissionais
        legal_areas = {
            "trabalhista": {
                "keywords": ["demitido", "demissão", "despedido", "trabalho", "emprego", "patrão",
                            "horas extras", "hora extra", "fgts", "rescisão", "aviso prévio",
                            "assédio moral", "assedio", "carteira assinada", "férias", "13º"],
                "response": (
                    "Entendi sua situação, e esse tipo de caso realmente aparece com bastante frequência "
                    "no direito trabalhista brasileiro. A legislação trabalhista possui diversos mecanismos "
                    "de proteção ao trabalhador, e dependendo dos detalhes do seu caso, você pode ter "
                    "direitos importantes a serem preservados."
                ),
                "area": "Direito Trabalhista"
            },

            "consumidor": {
                "keywords": ["comprei", "compra", "produto defeituoso", "serviço ruim", "empresa",
                            "loja", "cancelamento", "reembolso", "cobrança indevida", "negativação",
                            "spc", "serasa", "plano de saúde", "telefonia"],
                "response": (
                    "Sua situação envolve uma relação de consumo, área em que o Código de Defesa do Consumidor "
                    "oferece proteção robusta ao consumidor. Esse tipo de caso costuma ter prazos específicos "
                    "e exige análise cuidadosa das circunstâncias, documentos e direitos envolvidos."
                ),
                "area": "Direito do Consumidor"
            },

            "familia": {
                "keywords": ["divórcio", "separação", "pensão alimentícia", "guarda", "filho", "filha",
                            "casamento", "união estável", "cônjuge", "ex-marido", "ex-mulher", "paternidade"],
                "response": (
                    "Questões de família são sempre delicadas e envolvem aspectos emocionais e jurídicos importantes. "
                    "A legislação brasileira possui regras específicas que protegem os direitos de todos os envolvidos, "
                    "especialmente quando há crianças ou patrimônio em questão. Cada caso familiar é único e "
                    "exige análise individualizada."
                ),
                "area": "Direito de Família"
            },

            "civil": {
                "keywords": ["contrato", "dívida", "empréstimo", "acidente", "indenização", "danos",
                            "responsabilidade civil", "prejuízo", "acordo", "calote"],
                "response": (
                    "Sua situação envolve questões de direito civil, área ampla que regula relações entre particulares. "
                    "Existem diversos aspectos legais que precisam ser considerados: prazos prescricionais, "
                    "responsabilidades, possibilidades de reparação e estratégias processuais cabíveis."
                ),
                "area": "Direito Civil"
            },

            "criminal": {
                "keywords": ["denúncia", "processo criminal", "polícia", "crime", "furto", "roubo",
                            "ameaça", "agressão", "difamação", "calúnia", "boletim de ocorrência"],
                "response": (
                    "Questões criminais exigem atenção imediata e acompanhamento jurídico especializado. "
                    "A legislação penal brasileira possui procedimentos específicos, prazos processuais "
                    "e garantias constitucionais que precisam ser observados rigorosamente. "
                    "Cada caso criminal tem suas particularidades."
                ),
                "area": "Direito Criminal"
            },

            "previdenciario": {
                "keywords": ["inss", "aposentadoria", "benefício", "auxílio-doença", "perícia",
                            "previdência", "segurado", "contribuição"],
                "response": (
                    "Questões previdenciárias envolvem direitos sociais fundamentais e exigem conhecimento "
                    "técnico da legislação do INSS, jurisprudência dos tribunais e procedimentos administrativos. "
                    "Muitas vezes há prazos importantes e documentação específica que precisa ser analisada."
                ),
                "area": "Direito Previdenciário"
            },

            "imobiliario": {
                "keywords": ["imóvel", "casa", "apartamento", "aluguel", "inquilino", "proprietário",
                            "despejo", "compra e venda", "financiamento", "construtora"],
                "response": (
                    "Questões imobiliárias envolvem patrimônio importante e exigem análise cuidadosa de contratos, "
                    "documentação do imóvel e legislação específica. Existem diversas nuances jurídicas "
                    "que podem fazer diferença no resultado do seu caso."
                ),
                "area": "Direito Imobiliário"
            },

            "empresarial": {
                "keywords": ["empresa", "societário", "cnpj", "sócio", "contrato social", "mei",
                            "sociedade", "negócio", "empresa fechou"],
                "response": (
                    "Questões empresariais exigem visão estratégica e conhecimento da legislação comercial, "
                    "tributária e societária. Dependendo da situação, existem diferentes caminhos jurídicos "
                    "que podem ser adotados para proteger seus interesses."
                ),
                "area": "Direito Empresarial"
            }
        }

        # Identificar área pela análise de keywords
        for area_key, area_data in legal_areas.items():
            for keyword in area_data["keywords"]:
                if keyword in user_lower:
                    self.client_data["area_direito"] = area_data["area"]
                    return {
                        "area": area_data["area"],
                        "response": area_data["response"],
                        "identified": True
                    }

        # Se não identificou área específica
        return {
            "area": "Análise Necessária",
            "response": (
                "Entendi. O relato que você me traz pode envolver diferentes aspectos jurídicos. "
                "Para eu conseguir te orientar corretamente, preciso entender melhor alguns detalhes "
                "da sua situação."
            ),
            "identified": False
        }

    def strategic_investigation(self, user_input: str) -> Dict:
        """
        Realiza investigação estratégica fazendo perguntas inteligentes
        para demonstrar expertise e coletar informações cruciais.
        """

        area = self.client_data.get("area_direito", "Geral")

        # Perguntas estratégicas por área do direito
        investigation_questions = {
            "Direito Trabalhista": [
                "Quando exatamente isso aconteceu? É importante verificarmos os prazos legais.",
                "Você possui algum documento ou registro que comprove sua situação? "
                "Emails, mensagens, controle de ponto ou testemunhas?",
                "Durante quanto tempo você trabalhou nessa empresa? "
                "Isso pode influenciar significativamente seus direitos."
            ],

            "Direito do Consumidor": [
                "Você chegou a registrar alguma reclamação formal à empresa ou ao Procon?",
                "Possui nota fiscal, contrato ou algum comprovante da relação de consumo?",
                "Quando ocorreu o problema? Dependendo do prazo, existem diferentes caminhos jurídicos."
            ],

            "Direito de Família": [
                "Existem filhos envolvidos nessa situação?",
                "Vocês possuem bens em comum que precisam ser considerados?",
                "Já houve alguma tentativa de acordo ou mediação entre as partes?"
            ],

            "Direito Civil": [
                "Existe algum contrato ou documento escrito relacionado a essa situação?",
                "Você tentou resolver isso de forma amigável antes?",
                "Há testemunhas ou outros envolvidos que possam corroborar sua versão?"
            ],

            "Direito Criminal": [
                "Foi registrado boletim de ocorrência? Isso é fundamental para a análise do caso.",
                "Existem provas materiais ou testemunhas do ocorrido?",
                "Quando exatamente isso aconteceu? Prazos são cruciais em matéria penal."
            ],

            "Direito Previdenciário": [
                "Você já deu entrada em algum pedido administrativo no INSS?",
                "Possui toda a documentação médica e comprovantes de contribuição?",
                "Já passou por perícia médica do INSS?"
            ],

            "Direito Imobiliário": [
                "O imóvel possui toda a documentação regularizada?",
                "Existe contrato de compra e venda ou locação formalizado?",
                "Há alguma ação judicial ou protesto relacionado ao imóvel?"
            ],

            "Direito Empresarial": [
                "A empresa possui contrato social atualizado e registrado?",
                "Existem débitos tributários ou trabalhistas pendentes?",
                "Quantos sócios estão envolvidos e qual a participação de cada um?"
            ]
        }

        questions = investigation_questions.get(area, [
            "Para eu entender melhor, você pode me dar mais detalhes sobre quando isso aconteceu?",
            "Existe alguma documentação ou registro relacionado à sua situação?",
            "Houve alguma tentativa de resolver isso de forma amigável?"
        ])

        # Selecionar pergunta com base no contador de investigação
        if self.investigation_count < len(questions):
            question = questions[self.investigation_count]
            self.investigation_count += 1
        else:
            question = "Entendo. Baseado no que você me contou, vejo que sua situação tem particularidades importantes."

        return {
            "question": question,
            "stage": "investigation"
        }

    def demonstrate_complexity(self, user_input: str) -> str:
        """
        Demonstra a complexidade jurídica do caso, mostrando que
        é necessária análise formal com um advogado.
        """

        area = self.client_data.get("area_direito", "Essa área")

        complexity_statements = [
            f"Sua situação envolve aspectos jurídicos que exigem análise cuidadosa. "
            f"{area} possui interpretações jurisprudenciais específicas que podem fazer "
            f"toda a diferença no resultado do seu caso.",

            f"Esse tipo de situação em {area} pode ter implicações jurídicas importantes. "
            f"Existem prazos legais, documentação necessária e estratégias processuais "
            f"que precisam ser avaliadas com precisão.",

            f"Baseado no que você me relatou, vejo que existem variáveis jurídicas relevantes. "
            f"Em {area}, cada detalhe pode alterar o caminho jurídico mais adequado para você.",

            f"Compreendo sua situação. Casos como o seu em {area} normalmente exigem "
            f"uma avaliação técnica detalhada, verificação de prazos legais e análise documental "
            f"para determinar a melhor estratégia jurídica."
        ]

        return random.choice(complexity_statements)

    def conversion_strategy(self) -> Dict:
        """
        Estratégia de conversão: conduz o cliente para consulta jurídica formal
        de forma profissional e persuasiva, sem ser agressivo.
        """

        conversion_messages = [
            {
                "message": (
                    "Para eu te orientar com precisão jurídica e analisar seu caso com segurança, "
                    "o ideal é fazermos uma consulta jurídica formal. Nessa consulta consigo avaliar "
                    "documentos, verificar prazos legais e te orientar exatamente sobre o melhor caminho jurídico."
                ),
                "cta": "Se quiser, você pode me enviar uma mensagem no WhatsApp para agendarmos a análise do seu caso."
            },

            {
                "message": (
                    "Esse tipo de situação realmente exige uma análise jurídica mais detalhada. "
                    "Preciso verificar alguns documentos, analisar prazos e entender melhor todas as circunstâncias "
                    "para te dar uma orientação jurídica segura e responsável."
                ),
                "cta": "Podemos agendar uma consulta para eu avaliar seu caso com a atenção que ele merece. "
                       "Assim consigo te orientar corretamente."
            },

            {
                "message": (
                    "Para te dar uma orientação jurídica completa e responsável, preciso analisar "
                    "seu caso com mais profundidade. Cada situação jurídica tem suas particularidades, "
                    "e só com uma análise adequada consigo te indicar os melhores caminhos."
                ),
                "cta": "Se desejar, podemos marcar uma consulta. Me envie uma mensagem no WhatsApp "
                       "e organizamos um horário para conversarmos com calma sobre seu caso."
            },

            {
                "message": (
                    "Vejo que sua situação tem aspectos importantes que merecem atenção jurídica adequada. "
                    "Para eu te orientar com a segurança jurídica necessária, o correto é fazermos "
                    "uma consulta formal onde posso analisar documentos e detalhes do seu caso."
                ),
                "cta": "Você prefere uma consulta **presencial** aqui no escritório ou **online** por videochamada? "
                       "Ambas têm a mesma qualidade de atendimento."
            }
        ]

        selected = random.choice(conversion_messages)

        return {
            "message": selected["message"],
            "cta": selected["cta"],
            "stage": "conversion"
        }
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
        """
        Orquestra a conversa seguindo a estratégia do Dr. Estevão:
        Escuta ativa → Diagnóstico → Investigação → Demonstração de complexidade → Conversão
        """

        # Registrar no histórico
        self.conversation_history.append({
            "timestamp": datetime.now().isoformat(),
            "role": "user",
            "content": user_input
        })

        # Máquina de estados conversacional

        # 1. GREETING - Primeira interação
        if self.conversation_stage == "greeting":
            response_text = random.choice(self.get_greeting_responses())
            self.conversation_stage = "listening"
            response = {
                "text": response_text,
                "stage": "listening"
            }

        # 2. LISTENING - Escuta ativa e diagnóstico inicial
        elif self.conversation_stage == "listening":
            diagnosis = self.identify_legal_area(user_input)
            self.client_data["problema_relatado"] = user_input

            response_text = diagnosis["response"] + "\n\n"

            if diagnosis["identified"]:
                # Se identificou a área, inicia investigação
                investigation = self.strategic_investigation(user_input)
                response_text += investigation["question"]
                self.conversation_stage = "investigation"
                response = {
                    "text": response_text,
                    "stage": "investigation",
                    "area_identificada": diagnosis["area"]
                }
            else:
                # Se não identificou, pede mais informações
                response_text += "\n\nPode me contar com mais detalhes o que aconteceu?"
                response = {
                    "text": response_text,
                    "stage": "listening"
                }

        # 3. INVESTIGATION - Perguntas estratégicas (até 3 perguntas)
        elif self.conversation_stage == "investigation":
            if self.investigation_count < 2:
                # Continua investigação
                investigation = self.strategic_investigation(user_input)
                response_text = "Entendo. " + investigation["question"]
                response = {
                    "text": response_text,
                    "stage": "investigation"
                }
            else:
                # Após 2-3 perguntas, demonstra complexidade e converte
                complexity = self.demonstrate_complexity(user_input)
                conversion = self.conversion_strategy()

                response_text = complexity + "\n\n" + conversion["message"] + "\n\n" + conversion["cta"]
                self.conversation_stage = "conversion"
                response = {
                    "text": response_text,
                    "stage": "conversion",
                    "action": "request_consultation"
                }

        # 4. CONVERSION - Cliente interessado em consulta
        elif self.conversation_stage == "conversion":
            # Cliente demonstrou interesse, coletar dados
            response_text = (
                "Perfeito! Vou precisar de algumas informações para agendarmos sua consulta:\n\n"
                "• Seu nome completo\n"
                "• E-mail\n"
                "• Telefone (WhatsApp)\n"
                "• Preferência: Presencial ou Online?\n\n"
                "Pode preencher o formulário abaixo que já entro em contato!"
            )
            self.conversation_stage = "data_collection"
            response = {
                "text": response_text,
                "stage": "data_collection",
                "action": "collect_data"
            }

        # Fallback - Cliente continua conversando
        else:
            response_text = (
                "Compreendo. Para eu conseguir te ajudar da forma correta, "
                "o ideal é agendarmos uma consulta jurídica. "
                "Assim posso analisar seu caso com a atenção que ele merece. "
                "Podemos fazer isso agora?"
            )
            response = {
                "text": response_text,
                "stage": "conversion"
            }

        # Registrar resposta no histórico
        self.conversation_history.append({
            "timestamp": datetime.now().isoformat(),
            "role": "assistant",
            "content": response["text"]
        })

        return response

    def collect_client_data(self, data: Dict) -> Dict:
        """Coleta dados do cliente para agendamento de consulta"""

        update_fields = ["nome", "email", "telefone", "preferencia_consulta"]

        for field in update_fields:
            if field in data:
                self.client_data[field] = data[field]

        area = self.client_data.get("area_direito", "Direito")
        nome = self.client_data.get("nome", "Cliente")
        preferencia = self.client_data.get("preferencia_consulta", "online")

        return {
            "status": "collected",
            "client_data": self.client_data,
            "next_action": "send_whatsapp",
            "message": (
                f"Excelente, {nome}! Recebi seus dados. "
                f"Vou preparar uma mensagem de confirmação para você via WhatsApp "
                f"para agendarmos sua consulta {"presencial" if preferencia == "presencial" else "online"} "
                f"sobre {area}."
            )
        }

    def generate_whatsapp_message(self) -> str:
        """Gera mensagem profissional de confirmação para WhatsApp"""

        nome = self.client_data.get("nome", "Cliente")
        area = self.client_data.get("area_direito", "Questão Jurídica")
        preferencia = self.client_data.get("preferencia_consulta", "online").title()
        email = self.client_data.get("email", "não informado")

        message = (
            f"Olá, {nome}!\n\n"
            f"Aqui é o *Dr. Estevão*. "
            f"Recebi seu contato através do nosso chat e vi que você precisa de orientação jurídica em *{area}*.\n\n"
            f"📋 *Resumo da sua solicitação:*\n"
            f"• Área: {area}\n"
            f"• Tipo de consulta: {preferencia}\n"
            f"• E-mail: {email}\n\n"
            f"🗓️ *Próximos passos:*\n"
            f"Vou analisar inicialmente o relato que você me passou e em breve entrarei em contato "
            f"para agendarmos sua consulta jurídica.\n\n"
            f"⚖️ *Compromisso profissional:*\n"
            f"Como advogado, meu objetivo é analisar juridicamente seu caso com profundidade, "
            f"verificar prazos legais e te orientar sobre os melhores caminhos jurídicos disponíveis.\n\n"
            f"Em caso de dúvidas, pode responder esta mensagem!\n\n"
            f"Atenciosamente,\n"
            f"*Dr. Estevão*\n"
            f"Advogado - OAB/SP"
        )

        return message


# Exemplo de uso e teste
if __name__ == "__main__":
    agent = DrEstevaoAgent()

    print("🎓 Dr. Estevão - Agente Jurídico Multidisciplinar\n")
    print("=" * 70)

    # Simulação de conversa 1: Direito Trabalhista
    print("\n📋 CENÁRIO 1: Direito Trabalhista\n")

    resp1 = agent.process_message("Iniciar")
    print(f"Dr. Estevão: {resp1['text'][:100]}...\n")

    resp2 = agent.process_message("Fui demitido sem justa causa e não recebi minhas verbas rescisórias")
    print(f"Dr. Estevão: {resp2['text'][:150]}...")
    print(f"[Stage: {resp2['stage']}]\n")

    resp3 = agent.process_message("Sim, tenho emails e mensagens comprovando tudo")
    print(f"Dr. Estevão: {resp3['text'][:150]}...")
    print(f"[Stage: {resp3['stage']}]\n")

    resp4 = agent.process_message("Trabalhei lá por 3 anos")
    print(f"Dr. Estevão: Demonstração de complexidade + Conversão...")
    print(f"[Stage: {resp4['stage']}]\n")

    print("=" * 70)
    print("✅ Agente Dr. Estevão reconstruído com persona profissional!")

