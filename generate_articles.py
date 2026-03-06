#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generate 20 full article pages + update blog.html buttons.
"""
import os
import re

os.makedirs('pages/artigos', exist_ok=True)

NAV_TEMPLATE = '''<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no">
    <meta name="description" content="{meta_desc}">
    <meta name="author" content="Dr. Estevão Cursi">
    <meta name="robots" content="index, follow">
    <title>{title} | Dr. Estevão Cursi - Advocacia</title>
    <link rel="stylesheet" href="../../css/main.css">
    <link rel="icon" type="image/png" href="../../img.png">
    <style>
        .article-hero {{
            background: linear-gradient(135deg, rgba(10,13,17,0.95) 60%, rgba(59,130,246,0.15) 100%),
                        url('{img_url}') center/cover no-repeat;
            padding: 180px 0 80px;
            border-bottom: 1px solid rgba(255,255,255,0.07);
        }}
        .article-hero__badge {{
            display: inline-block;
            font-size: 0.72rem;
            text-transform: uppercase;
            letter-spacing: 2px;
            color: var(--accent-blue);
            background: rgba(59,130,246,0.1);
            border: 1px solid rgba(59,130,246,0.3);
            padding: 0.3rem 0.9rem;
            border-radius: 20px;
            margin-bottom: 1.2rem;
        }}
        .article-hero__title {{
            font-size: clamp(1.8rem, 4vw, 2.8rem);
            font-weight: 800;
            line-height: 1.25;
            margin-bottom: 1rem;
        }}
        .article-hero__meta {{
            font-size: 0.88rem;
            color: var(--text-secondary);
        }}
        .article-body {{
            max-width: 780px;
            margin: 0 auto;
            padding: 3rem var(--spacing-md);
        }}
        .article-body h2 {{
            font-size: 1.45rem;
            color: var(--text-primary);
            margin: 2.5rem 0 1rem;
            border-left: 3px solid var(--accent-blue);
            padding-left: 1rem;
        }}
        .article-body h3 {{
            font-size: 1.15rem;
            color: var(--accent-blue);
            margin: 1.8rem 0 0.8rem;
        }}
        .article-body p {{
            font-size: 1.05rem;
            line-height: 1.85;
            color: var(--text-secondary);
            margin-bottom: 1.2rem;
        }}
        .article-body ul, .article-body ol {{
            padding-left: 1.5rem;
            margin-bottom: 1.2rem;
        }}
        .article-body li {{
            font-size: 1.02rem;
            line-height: 1.75;
            color: var(--text-secondary);
            margin-bottom: 0.4rem;
        }}
        .article-body .highlight-box {{
            background: rgba(59,130,246,0.07);
            border-left: 4px solid var(--accent-blue);
            padding: 1.2rem 1.5rem;
            border-radius: 0 8px 8px 0;
            margin: 1.5rem 0;
        }}
        .article-body .highlight-box p {{
            margin-bottom: 0;
            color: var(--text-primary);
        }}
        .article-author-box {{
            border-top: 1px solid rgba(255,255,255,0.08);
            padding-top: 2rem;
            margin-top: 3rem;
            display: flex;
            align-items: center;
            gap: 1.2rem;
        }}
        .article-author-box img {{
            width: 64px;
            height: 64px;
            border-radius: 50%;
            border: 2px solid var(--accent-blue);
            object-fit: cover;
        }}
        .article-author-box .author-info h4 {{
            font-size: 1rem;
            color: var(--accent-blue);
            margin-bottom: 0.2rem;
        }}
        .article-author-box .author-info span {{
            font-size: 0.82rem;
            color: var(--text-secondary);
        }}
        .article-cta-bar {{
            background: rgba(59,130,246,0.06);
            border: 1px solid rgba(59,130,246,0.15);
            border-radius: var(--radius-md);
            padding: 2rem;
            text-align: center;
            margin: 3rem 0;
        }}
        .article-cta-bar h3 {{
            color: var(--text-primary);
            font-size: 1.25rem;
            margin-bottom: 0.6rem;
        }}
        .article-cta-bar p {{
            font-size: 0.95rem;
            margin-bottom: 1.5rem;
        }}
        .article-nav-buttons {{
            display: flex;
            gap: 1rem;
            justify-content: center;
            flex-wrap: wrap;
            margin-top: 1rem;
        }}
        .btn--back {{
            background: transparent;
            color: var(--text-secondary);
            border: 1px solid rgba(255,255,255,0.15);
            padding: 0.65rem 1.5rem;
            border-radius: var(--radius-sm);
            font-size: 0.9rem;
            text-decoration: none;
            transition: all 0.3s ease;
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
        }}
        .btn--back:hover {{
            border-color: var(--accent-blue);
            color: var(--accent-blue);
        }}
    </style>
</head>
<body>
    <a href="#main" class="skip-link sr-only">Ir para o conteúdo principal</a>

    <header class="header">
        <nav class="nav container" aria-label="Navegação principal">
            <a href="../../index.html" class="nav__logo" aria-label="Dr. Estevão Cursi - Página inicial">
                <img src="../../img.png" alt="Logo Dr. Estevão Cursi">
            </a>
            <button class="nav__toggle" aria-label="Abrir menu de navegação" aria-expanded="false">
                <span></span><span></span><span></span>
            </button>
            <ul class="nav__menu" role="list">
                <li><a href="../../index.html#areas" class="nav__link">Áreas de Atuação</a></li>
                <li><a href="../../blog.html" class="nav__link">Blog e Artigos</a></li>
                <li><a href="../../index.html#sobre" class="nav__link">Sobre</a></li>
                <li><a href="../../index.html#contato" class="nav__link">Contato</a></li>
            </ul>
        </nav>
    </header>

    <main id="main">
        <div class="article-hero">
            <div class="container">
                <span class="article-hero__badge">{area}</span>
                <h1 class="article-hero__title">{title}</h1>
                <p class="article-hero__meta">Por <strong style="color:var(--accent-blue);">Dr. Estevão Cursi</strong> &nbsp;·&nbsp; OAB 378065 &nbsp;·&nbsp; Publicado em março de 2026</p>
            </div>
        </div>

        <div class="article-body">
            <div class="article-nav-buttons" style="justify-content:flex-start; margin-bottom:2rem;">
                <a href="../../blog.html" class="btn--back">&#8592; Voltar para os Artigos</a>
            </div>

            {content}

            <div class="article-author-box">
                <img src="../../img.png" alt="Dr. Estevão Cursi">
                <div class="author-info">
                    <h4>Dr. Estevão Cursi</h4>
                    <span>Advogado | OAB 378065 | Especialista nas áreas do Direito apontadas abaixo</span>
                </div>
            </div>

            <div class="article-cta-bar">
                <h3>Ficou com dúvidas? Fale diretamente com o Dr. Estevão Cursi.</h3>
                <p>Atendimento personalizado, sem custo inicial. Explique seu caso e receba uma orientação especializada.</p>
                <div class="article-nav-buttons">
                    <a href="../../blog.html" class="btn--back">&#8592; Voltar para os Artigos</a>
                    <a href="../../index.html#contato" class="btn btn--primary">Falar com o Advogado</a>
                </div>
            </div>
        </div>
    </main>

    <footer class="footer">
        <div class="container">
            <div class="footer__content">
                <div class="footer__section">
                    <h4>Dr. Estevão Cursi</h4>
                    <p style="color:var(--text-secondary);line-height:1.7;">Advocacia de excelência com compromisso ético e foco em resultados concretos.</p>
                </div>
                <div class="footer__section">
                    <h4>Áreas de Atuação</h4>
                    <ul>
                        <li><a href="../../pages/execucao-civel-trabalhista.html">Execução Cível e Trabalhista</a></li>
                        <li><a href="../../pages/assessoria-empresas.html">Assessoria de Empresas</a></li>
                        <li><a href="../../pages/prisoes.html">Prisões e Defesa Criminal</a></li>
                        <li><a href="../../pages/direito-saude.html">Direito da Saúde</a></li>
                        <li><a href="../../blog.html">Blog e Artigos</a></li>
                    </ul>
                </div>
                <div class="footer__section">
                    <h4>Contato</h4>
                    <ul>
                        <li>E-mail: contato@estevaocursi.adv.br</li>
                        <li>Telefone: (XX) XXXXX-XXXX</li>
                        <li>Endereço: Escritório físico</li>
                    </ul>
                </div>
            </div>
            <div class="footer__bottom">
                <p>Desenvolvido por <strong>Bio Code Technology ltda.</strong> Todos os Direitos Reservados 2026</p>
            </div>
        </div>
    </footer>

    <script src="../../js/main.js"></script>
</body>
</html>
'''

ARTICLES = [
    {
        "slug": "execucao-trabalhista-eficiente",
        "title": "A Importância da Execução Trabalhista Eficiente",
        "area": "Direito Trabalhista",
        "lock": 12,
        "meta_desc": "Entenda por que a execução trabalhista eficiente é essencial para garantir seus direitos e como um advogado especializado pode fazer a diferença.",
        "content": '''
<p>Quando uma decisão judicial trabalhista é proferida a seu favor, muitos acreditam que o problema está resolvido. Na prática, no entanto, o maior desafio começa exatamente nesse momento: a <strong>execução da sentença</strong>. Infelizmente, muitos direitos conquistados no mérito acabam não sendo satisfeitos pela falta de uma condução técnica e ágil da fase executória.</p>

<h2>O que é Execução Trabalhista?</h2>
<p>A execução trabalhista é a fase do processo em que se busca, na prática, o cumprimento da sentença ou do acordo homologado pela Justiça do Trabalho. Ou seja, é o momento em que o credor (trabalhador ou empresa) precisa receber o que lhe foi reconhecido por decisão judicial.</p>
<p>Na Consolidação das Leis do Trabalho (CLT) e no Código de Processo Civil, existem ferramentas específicas para isso — ferramentas que, em mãos erradas, costumam ser subutilizadas.</p>

<h2>Por que muitas execuções falham?</h2>
<p>Os motivos são variados, mas os mais comuns são:</p>
<ul>
    <li>Ausência de rastreamento patrimonial do devedor (ferramentas como Sisbajud, Infojud e Renajud);</li>
    <li>Falta de agilidade na penhora de ativos disponíveis;</li>
    <li>Desconhecimento de técnicas como a desconsideração da personalidade jurídica (IDPJ);</li>
    <li>Omissão em detectar fraudes à execução praticadas pelo devedor;</li>
    <li>Não requerimento de atualização correta dos cálculos ao longo do tempo.</li>
</ul>

<div class="highlight-box">
    <p><strong>Dado importante:</strong> Estima-se que mais de 60% das execuções trabalhistas no Brasil apresentam algum nível de dificuldade no recebimento do crédito, segundo dados do Conselho Nacional de Justiça (CNJ).</p>
</div>

<h2>Ferramentas legais para uma execução eficiente</h2>
<h3>1. Sisbajud (antigo BacenJud)</h3>
<p>Sistema que permite ao juiz ordenar o bloqueio de valores em contas bancárias do devedor de forma eletrônica e imediata. É uma das ferramentas mais efetivas para garantir o crédito trabalhista em curto prazo.</p>

<h3>2. Renajud</h3>
<p>Permite a penhora on-line de veículos registrados em nome do devedor. Funciona diretamente com o banco de dados do Departamento Nacional de Trânsito (DENATRAN).</p>

<h3>3. Infojud</h3>
<p>Ferramenta vinculada à Receita Federal que permite ao juiz verificar bens imóveis, declarações de Imposto de Renda e outras informações patrimoniais do executado.</p>

<h3>4. Desconsideração da Personalidade Jurídica (IDPJ)</h3>
<p>Quando a empresa devedora não possui bens suficientes, a lei permite atingir o patrimônio pessoal dos sócios em determinadas situações — como desvio de finalidade ou confusão patrimonial. Esse incidente pode ser determinante para a satisfação do crédito.</p>

<h2>O papel do advogado na execução</h2>
<p>Uma execução trabalhista bem conduzida requer monitoramento constante, requerimentos estratégicos e conhecimento profundo das ferramentas disponíveis. O advogado especializado:</p>
<ul>
    <li>Solicita diligências como rastreamento bancário e imobiliário;</li>
    <li>Identifica movimentações suspeitas que possam caracterizar fraude;</li>
    <li>Requer a atualização do débito com correção monetária e juros corretos;</li>
    <li>Acompanha o andamento diário dos autos para não perder prazos críticos.</li>
</ul>

<h2>O que você deve fazer agora?</h2>
<p>Se você tem um crédito trabalhista reconhecido e ainda não recebeu, ou se está com um processo parado na fase de execução, é fundamental consultar um advogado especializado imediatamente. O tempo é um fator crítico: bens podem ser alienados, contas zeradas e a satisfação do crédito pode se tornar cada vez mais difícil.</p>
<p>Não aguarde. A execução trabalhista tem prazo de prescrição intercorrente (<em>prescrição que corre durante o processo</em>), o que pode extinguir seu direito mesmo com sentença favorável.</p>
'''
    },
    {
        "slug": "evitar-passivos-trabalhistas",
        "title": "Como Evitar Passivos Trabalhistas em Sua Empresa",
        "area": "Direito Trabalhista",
        "lock": 13,
        "meta_desc": "Saiba como implementar um compliance trabalhista eficaz para reduzir ações judiciais e proteger o patrimônio da sua empresa.",
        "content": '''
<p>Passivo trabalhista é o nome dado ao conjunto de obrigações que uma empresa tem com seus empregados — e que, quando não cumpridas corretamente, transformam-se em processos judiciais custosos. A boa notícia é que a maioria dessas ações pode ser evitada com prevenção jurídica adequada.</p>

<h2>O que gera passivo trabalhista?</h2>
<p>As causas mais frequentes de ações trabalhistas no Brasil incluem:</p>
<ul>
    <li>Controle irregular de jornada de trabalho (ponto eletrônico mal configurado);</li>
    <li>Ausência ou irregularidade nos exames médicos admissional, periódico e demissional;</li>
    <li>Pagamento incorreto de horas extras, adicionais noturno e insalubridade;</li>
    <li>Rescisão contratual com verbas calculadas de forma errada;</li>
    <li>Ausência de registro formal de funcionários (carteira assinada);</li>
    <li>Assédio moral ou sexual não tratado institucional pela empresa.</li>
</ul>

<div class="highlight-box">
    <p><strong>Atenção:</strong> A Reforma Trabalhista (Lei 13.467/2017) trouxe mudanças importantes, mas não eliminou — e em muitos casos até ampliou — a responsabilidade do empregador em diversas situações.</p>
</div>

<h2>Compliance Trabalhista: o que é e como funciona</h2>
<p>Compliance trabalhista é o conjunto de práticas, políticas internas e treinamentos que garantem que a empresa atua em conformidade com a legislação do trabalho. Na prática, significa:</p>
<ul>
    <li>Ter controles de ponto confiáveis e auditáveis;</li>
    <li>Manter prontuários de saúde ocupacional atualizados;</li>
    <li>Ter contratos de trabalho adequados à função real exercida;</li>
    <li>Treinar gestores para evitar situações que caracterizem assédio;</li>
    <li>Revisar periodicamente os acordos coletivos e convenções vigentes.</li>
</ul>

<h2>Auditoria Trabalhista Preventiva</h2>
<p>Uma auditoria trabalhista é a análise técnica completa das obrigações da empresa com seus colaboradores. Ela identifica riscos latentes antes que virem ações judiciais. O resultado é um relatório com os pontos críticos e um plano de ação para regularizar cada item.</p>
<p>Para pequenas e médias empresas, uma auditoria anual pode representar uma economia significativa frente ao custo de uma ação trabalhista — que inclui honorários, custas processuais e o valor da condenação em si.</p>

<h2>Pontos de maior risco em 2026</h2>
<h3>Teletrabalho e Home Office</h3>
<p>A CLT exige que o contrato de trabalho remoto contenha cláusulas específicas sobre responsabilidade por equipamentos, custos de internet e controle de jornada. Empresas que ignoram isso estão expostas a ações por horas extras não pagas.</p>

<h3>Terceirização</h3>
<p>A empresa tomadora de serviços responde subsidiariamente pelas verbas trabalhistas da empresa terceirizante em caso de inadimplência. Um contrato mal redigido ou sem cláusulas de proteção pode gerar responsabilidade direta.</p>

<h2>Conclusão</h2>
<p>Investir em prevenção jurídica trabalhista é uma decisão empresarial estratégica. O custo de um programa de compliance é significativamente inferior ao custo médio de uma ação trabalhista com condenação, que no Brasil gira em torno de R$ 15.000 por processo, sem contar os custos reputacionais e operacionais.</p>
'''
    },
    {
        "slug": "teletrabalho-home-office",
        "title": "Nova Lei Trabalhista e o Teletrabalho (Home Office)",
        "area": "Direito Trabalhista",
        "lock": 14,
        "meta_desc": "Entenda as regras atuais do teletrabalho no Brasil, os direitos do trabalhador e as obrigações do empregador no modelo home office.",
        "content": '''
<p>O teletrabalho deixou de ser uma exceção para se tornar uma realidade permanente em muitas empresas. Após a pandemia de COVID-19, a legislação trabalhista brasileira foi atualizada para regulamentar com mais precisão este modelo — e os impactos jurídicos são significativos tanto para empregadores quanto para trabalhadores.</p>

<h2>O que diz a CLT sobre o Teletrabalho?</h2>
<p>A Consolidação das Leis do Trabalho (CLT), especialmente após as modificações da Lei 14.442/2022, estabelece que o teletrabalho deve ser formalizado por <strong>contrato escrito</strong> contendo, no mínimo:</p>
<ul>
    <li>Atividades que serão realizadas remotamente;</li>
    <li>Definição de responsabilidade por equipamentos e infraestrutura;</li>
    <li>Reembolso das despesas do empregado (internet, luz, equipamentos);</li>
    <li>Meios de monitoramento da produção ou das horas trabalhadas.</li>
</ul>

<div class="highlight-box">
    <p><strong>Ponto crítico:</strong> Trabalhadores em home office que comprovem jornada superior a 8h diárias têm direito às horas extras, independentemente de cláusula contratual em contrário.</p>
</div>

<h2>Controle de Jornada no Teletrabalho</h2>
<p>É um dos maiores focos de litígio. A empresa que não adota nenhuma forma de controle de jornada fica sujeita a presumir que o empregado trabalhava no máximo legal — o que pode ser contestado com provas de e-mails tardios, mensagens de WhatsApp fora do horário e outros registros digitais.</p>
<p>Para se proteger, o empregador deve:</p>
<ul>
    <li>Implementar sistema de ponto eletrônico remoto (muitos softwares de RH já oferecem isso);</li>
    <li>Definir expressamente os horários de trabalho e os de descanso;</li>
    <li>Proibir por escrito que gestores acionem colaboradores fora do expediente.</li>
</ul>

<h2>Fornecimento de Equipamentos</h2>
<p>A lei permite que a empresa e o empregado firmem acordo sobre quem fornecerá os equipamentos. Contudo, se o empregado arcar com os custos de infraestrutura, ele tem direito a ressarcimento.</p>
<p>Na prática, empresas que ignoram esse ponto acabam respondendo por ações de reembolso de despesas — valores que, acumulados durante anos de contrato, podem ser expressivos.</p>

<h2>Acidente de Trabalho em Home Office</h2>
<p>Sim, acidentes em casa durante o trabalho remoto podem ser reconhecidos como acidentes de trabalho. Queda de escada ao buscar documentos, lesão por esforço repetitivo (LER/DORT) e problemas causados por ergonomia inadequada são exemplos reconhecidos pela jurisprudência.</p>
<p>A empresa deve fornecer orientações de ergonomia e, em alguns casos, realizar vistorias nas condições do ambiente de trabalho do empregado.</p>

<h2>O que o Trabalhador Pode Reivindicar?</h2>
<ul>
    <li>Horas extras não pagas, demonstradas por provas digitais;</li>
    <li>Reembolso de despesas com internet e energia não pagas;</li>
    <li>Indenização por acidente de trabalho ocorrido no ambiente doméstico;</li>
    <li>Reconhecimento de vínculo empregatício em casos de trabalho disfarçado como "prestação de serviços".</li>
</ul>
'''
    },
    {
        "slug": "recuperacao-credito-estrategias",
        "title": "Recuperação de Crédito: Estratégias Legais",
        "area": "Assessoria Empresarial",
        "lock": 15,
        "meta_desc": "Como recuperar créditos por vias legais? Conheça as ferramentas de rastreamento patrimonial como Sisbajud e os caminhos jurídicos para receber o que é seu.",
        "content": '''
<p>Devedores que somem, empresas que fecham e sócios que transferem patrimônio às vésperas de uma cobrança judicial: esse é o cenário enfrentado por inúmeras empresas credoras no Brasil. A boa notícia é que o direito oferece ferramentas potentes para quem sabe utilizá-las.</p>

<h2>Qual é o melhor caminho para cobrar uma dívida?</h2>
<p>A resposta depende de alguns fatores: o valor da dívida, se existe título executivo, e se o devedor possui patrimônio rastreável. Em geral, os caminhos são:</p>
<ul>
    <li><strong>Ação de Conhecimento (Cobrança Ordinária):</strong> Para dívidas sem contrato formal ou título executivo. Mais demorada, pois exige provar a dívida em juízo;</li>
    <li><strong>Ação Monitória:</strong> Para dívidas documentadas sem força executiva (cheques prescritos, contratos sem assinatura de testemunhas);</li>
    <li><strong>Execução de Título Extrajudicial:</strong> Para cheques, notas promissórias e contratos com firmas reconhecidas — começa direto na fase de cobrança;</li>
    <li><strong>Execução de Sentença:</strong> Quando já existe decisão judicial favorável transitada em julgado.</li>
</ul>

<div class="highlight-box">
    <p><strong>Importante:</strong> A prescrição da maioria dos créditos empresariais é de 5 anos. Aguardar demais pode significar a perda do direito de cobrar judicialmente.</p>
</div>

<h2>Rastreamento Patrimonial: as ferramentas do judiciário</h2>
<p>Uma vez ajuizada a ação, existem recursos poderosíssimos para localizar bens do devedor:</p>

<h3>Sisbajud</h3>
<p>Antigo BacenJud. Permite o bloqueio imediato de valores em contas bancárias do devedor em todo o sistema financeiro nacional. Em casos urgentes, pode ser solicitada tutela antecipada para bloqueio antes mesmo do devedor ser citado.</p>

<h3>Renajud</h3>
<p>Bloqueia transferência e venda de veículos do devedor diretamente no DENATRAN/SENATRAN. Impede que o devedor venda o carro antes da penhora ser efetivada.</p>

<h3>CNIB (Central Nacional de Indisponibilidade de Bens)</h3>
<p>Permite registrar a indisponibilidade de bens imóveis em todos os cartórios do Brasil, impedindo alienação ou gravame de imóveis pelo devedor.</p>

<h2>Fraude à Execução e Fraude Contra Credores</h2>
<p>Se o devedor transferiu bens a terceiros durante o processo ou quando já sabia da dívida, é possível requerer a <strong>declaração de fraude à execução</strong>, tornando o ato de transferência ineficaz e permitindo a penhora mesmo que o bem já não esteja mais no nome do devedor.</p>
<p>O reconhecimento de fraude exige prova do dano ao credor (insolvência real ou presumida do devedor) e do conhecimento da dívida pelo terceiro adquirente. Um advogado experiente sabe como construir essa prova.</p>

<h2>Desconsideração da Personalidade Jurídica (IDPJ)</h2>
<p>Quando a empresa devedora está sem bens suficientes, é possível redirecionar a execução para o patrimônio pessoal dos sócios se houver prova de abuso da personalidade jurídica, descanso de atividades, confusão patrimonial ou desvio de finalidade.</p>
<p>Em processos trabalhistas e de consumidor, os critérios para a IDPJ são mais amplos ainda — muitas vezes bastando o simples encerramento irregular da empresa.</p>
'''
    },
    {
        "slug": "protecao-patrimonial-holding-familiar",
        "title": "Proteção Patrimonial e Holding Familiar",
        "area": "Assessoria Empresarial",
        "lock": 16,
        "meta_desc": "Entenda como funciona a proteção patrimonial via holding familiar, suas vantagens e os limites legais para não confundir planejamento com fraude.",
        "content": '''
<p>Proteger o patrimônio construído ao longo de uma vida é uma preocupação natural e legítima. Quando feita dentro dos parâmetros legais, a proteção patrimonial é uma estratégia plenamente válida — e a holding familiar é uma das ferramentas mais eficazes para isso.</p>

<h2>O que é uma Holding Familiar?</h2>
<p>Uma holding familiar é uma empresa (geralmente do tipo Sociedade Limitada ou Sociedade Anônima) criada para <strong>concentrar e administrar o patrimônio de uma família</strong> — imóveis, participações em outras empresas, aplicações financeiras, etc.</p>
<p>Os bens são integralizados ao capital social da holding, e os membros da família recebem cotas ou ações em proporção ao que foi aportado.</p>

<div class="highlight-box">
    <p><strong>Blindagem não é fraude:</strong> A holding familiar é 100% legal quando constituída antes de qualquer evento danoso (dívidas, processos). Criá-la após ter dívidas pode ser enquadrado como fraude à execução.</p>
</div>

<h2>Vantagens da Holding Familiar</h2>
<h3>1. Proteção patrimonial</h3>
<p>Em casos de processos trabalhistas, cíveis ou fiscais contra a pessoa física dos sócios, os bens dentro da holding geralmente ficam protegidos — pois pertencem à pessoa jurídica, não ao indivíduo.</p>

<h3>2. Planejamento sucessório simplificado</h3>
<p>A transmissão de cotas da holding é muito mais simples e barata do que um inventário convencional de imóveis. O ITCMD (imposto sobre doação/herança) incide sobre as cotas, e a partilha pode ser feita em vida com muito mais controle.</p>

<h3>3. Cláusulas restritivas protetoras</h3>
<p>Na doação das cotas aos herdeiros, o doador pode inserir cláusulas de <strong>inalienabilidade</strong> (proíbe venda das cotas), <strong>impenhorabilidade</strong> (protege de dívidas dos herdeiros) e <strong>incomunicabilidade</strong> (as cotas não entram na comunhão com cônjuge em caso de divórcio).</p>

<h3>4. Vantagens tributárias</h3>
<p>Dependendo do regime tributário escolhido (Lucro Presumido), empresas holding podem recolher menos impostos sobre rendimentos de aluguel, por exemplo, comparado à tributação de pessoa física — que pode chegar a 27,5% no IR.</p>

<h2>Limites legais e riscos</h2>
<p>A holding familiar não é uma solução perfeita. Existem situações em que os bens da holding podem ser atingidos por credores:</p>
<ul>
    <li>Se a holding for criada após o surgimento da dívida (fraude à execução);</li>
    <li>Se houver confusão patrimonial (mistura de contas pessoais com as da empresa);</li>
    <li>Se a desconsideração da personalidade jurídica for deferida em processo judicial;</li>
    <li>Se as cotas forem penhoradas diretamente em execução contra o sócio.</li>
</ul>

<h2>Como dar o primeiro passo?</h2>
<p>Antes de constituir uma holding, é necessário um estudo patrimonial completo: levantamento de todos os bens, análise de passivos existentes, escolha do regime tributário mais vantajoso e estruturação das cláusulas societárias e sucessórias. Esse trabalho deve ser feito por um advogado com experiência societária e tributária para garantir segurança e eficácia.</p>
'''
    },
    {
        "slug": "clausulas-abusivas-plano-saude",
        "title": "Cláusulas Abusivas em Contratos de Planos de Saúde",
        "area": "Defesa do Consumidor",
        "lock": 17,
        "meta_desc": "Saiba quais cláusulas são consideradas abusivas em contratos de planos de saúde e como exigir judicialmente a cobertura que você tem direito.",
        "content": '''
<p>O contrato de plano de saúde deveria dar segurança ao consumidor. Na prática, muitas operadoras inserem cláusulas que limitam coberturas, criam exclusões abusivas e aplicam reajustes despropositados — tudo de forma a reduzir custos em detrimento da saúde do segurado.</p>

<h2>O que é uma cláusula abusiva?</h2>
<p>De acordo com o Código de Defesa do Consumidor (CDC) e a Lei 9.656/98 (Lei dos Planos de Saúde), uma cláusula é abusiva quando coloca o consumidor em desvantagem exagerada ou é incompatível com a boa-fé e a equidade. As principais situações são:</p>
<ul>
    <li>Negativa de cobertura de procedimento previsto no rol da ANS;</li>
    <li>Exigência de carência para situações de urgência e emergência;</li>
    <li>Limitação de dias de internação hospitalar;</li>
    <li>Exclusão de doenças preexistentes declaradas na adesão;</li>
    <li>Reajuste por faixa etária em percentuais não previstos ou não informados.</li>
</ul>

<div class="highlight-box">
    <p><strong>STJ Sumulou:</strong> A Súmula 608 do STJ determina que é abusiva a negativa de cobertura em atendimento de urgência ou emergência a associado de plano de saúde — mesmo em rede não credenciada.</p>
</div>

<h2>Reajuste por faixa etária: quando é abusivo?</h2>
<p>A ANS autoriza reajustes por faixa etária, mas esses aumentos devem seguir regras claras:</p>
<ul>
    <li>Os percentuais de reajuste devem constar expressamente no contrato;</li>
    <li>O aumento não pode ser superior a 6 vezes o valor da menor faixa;</li>
    <li>A partir dos 60 anos, qualquer reajuste deve ser comunicado com antecedência e justificação.</li>
</ul>
<p>Reajustes que violem essas condições podem ser revisados judicialmente, com devolução dos valores cobrados a maior.</p>

<h2>Negativa de cobertura: como proceder?</h2>
<p>Se seu plano negou um procedimento, exame ou internação, siga esses passos:</p>
<ol>
    <li><strong>Solicite a negativa por escrito</strong> — a operadora é obrigada a fornecer justificativa formal;</li>
    <li><strong>Consulte o Rol da ANS</strong> — verifique se o procedimento está coberto pela lista de cobertura obrigatória;</li>
    <li><strong>Registre reclamação na ANS</strong> — abre processo administrativo que pode gerar multa à operadora;</li>
    <li><strong>Ajuíze ação com pedido de tutela antecipada</strong> — em casos urgentes, o juiz pode ordenar a cobertura em 24 horas.</li>
</ol>

<h2>Danos morais por negativa indevida</h2>
<p>A jurisprudência é consolidada: a negativa indevida de cobertura por plano de saúde gera direito à indenização por danos morais, além da obrigação de custear o procedimento. Os valores variam, mas costumam ficar entre R$ 5.000 e R$ 30.000 dependendo da situação.</p>
<p>Se você sofreu negativa de cobertura, não aceite sem antes consultar um advogado especializado. Na maioria dos casos, existe fundamentação legal para reverter a situação.</p>
'''
    },
    {
        "slug": "voo-cancelado-direitos",
        "title": "Voo Cancelado ou Atrasado: Quais são os seus Direitos?",
        "area": "Defesa do Consumidor",
        "lock": 18,
        "meta_desc": "Conheça seus direitos como passageiro em casos de voo cancelado, atrasado ou overbooking e como pleitear indenização na Justiça.",
        "content": '''
<p>Aeroporto lotado, painel mostrando "cancelado" ou "atrasado" — e a companhia aérea simplesmente ignorando você. Essa situação é mais comum do que deveria, mas o consumidor brasileiro tem ampla proteção legal nesses casos.</p>

<h2>O que diz a legislação brasileira?</h2>
<p>A Resolução 400/2016 da ANAC (Agência Nacional de Aviação Civil) estabelece os direitos mínimos dos passageiros. Além dela, o Código de Defesa do Consumidor (CDC) oferece proteção adicional.</p>

<h2>Atraso de voo: quais são seus direitos?</h2>
<p>A partir de 1 hora de atraso:</p>
<ul>
    <li><strong>Comunicação imediata</strong> sobre o motivo do atraso e nova previsão;</li>
    <li><strong>Facilidades de comunicação</strong> (telefone, internet).</li>
</ul>
<p>A partir de 2 horas de atraso:</p>
<ul>
    <li><strong>Alimentação</strong> adequada (voucher ou refeição fornecida pela companhia).</li>
</ul>
<p>A partir de 4 horas de atraso:</p>
<ul>
    <li>Reacomodação em outro voo, reembolso integral ou execução do serviço por outra modalidade;</li>
    <li><strong>Hospedagem</strong> e <strong>translado</strong> quando necessário pernoitar.</li>
</ul>

<div class="highlight-box">
    <p><strong>Importante:</strong> Caso o passageiro já tenha chegado ao portão de embarque, a obrigação da empresa começa no atraso de 1 hora, independentemente das condições.</p>
</div>

<h2>Voo Cancelado</h2>
<p>Em caso de cancelamento, a companhia deve oferecer, à escolha do passageiro:</p>
<ul>
    <li>Reacomodação no próximo voo disponível com mesmo destino;</li>
    <li>Reembolso integral, inclusive de trechos já realizados em caso de viagem de conexão;</li>
    <li>Execução do serviço por outra empresa ou meio de transporte alternativo.</li>
</ul>

<h2>Overbooking (preterição de embarque)</h2>
<p>Overbooking ocorre quando a companhia vende mais passagens do que assentos disponíveis. Nessa situação, o passageiro preterido tem direito a:</p>
<ul>
    <li>Reacomodação imediata em outro voo com o mesmo destino;</li>
    <li>Reembolso integral caso não queira aguardar;</li>
    <li>Compensação financeira imediata (varia conforme o atraso gerado).</li>
</ul>

<h2>Quando cabe indenização por danos morais?</h2>
<p>O simples cancelamento ou atraso nem sempre gera dano moral. Mas algumas situações específicas costurumam ser reconhecidas pelos tribunais:</p>
<ul>
    <li>Perda de evento importante (casamento, funeral, formatura, cirurgia);</li>
    <li>Passageiro abandonado sem assistência material por horas;</li>
    <li>Criança ou idoso sem acompanhamento e sem atendimento da companhia;</li>
    <li>Bagagem extraviada com itens essenciais ou de alto valor.</li>
</ul>
<p>O prazo para ajuizar ação é de <strong>5 anos</strong> (CDC) a contar do evento. Guarde todos os documentos: bilhetes, comprovantes de gastos e registros de comunicação com a companhia.</p>
'''
    },
    {
        "slug": "renegociacao-dividas-superendividamento",
        "title": "Renegociação de Dívidas e o Superendividamento",
        "area": "Defesa do Consumidor",
        "lock": 19,
        "meta_desc": "Entenda a Lei do Superendividamento e como renegociar dívidas em bloco judicialmente para proteger sua dignidade e renda mínima.",
        "content": '''
<p>Em 2021, o Brasil passou a ter legislação específica para proteger o consumidor que se encontra em situação de superendividamento — aquela em que a soma das dívidas supera a capacidade de pagamento, comprometendo a subsistência do devedor e de sua família.</p>

<h2>O que é superendividamento?</h2>
<p>O superendividamento é definido pela Lei 14.181/2021 como a impossibilidade manifesta do consumidor, de boa-fé, de pagar a totalidade de suas dívidas de consumo, vencidas e vincendas, sem comprometer seu <strong>mínimo existencial</strong>.</p>

<div class="highlight-box">
    <p><strong>Mínimo existencial:</strong> É o valor mínimo necessário para que o devedor mantenha sua dignidade e a de sua família — alimentação, moradia, transporte e saúde básica. Esse valor não pode ser comprometido pelos credores.</p>
</div>

<h2>Como funciona o processo judicial de renegociação?</h2>
<p>O procedimento é chamado de <strong>Repactuação de Dívidas</strong> e funciona assim:</p>
<ol>
    <li>O consumidor protocola petição no Juizado Especial Cível requerendo a abertura do processo;</li>
    <li>Todos os credores são convocados para uma audiência de conciliação simultânea;</li>
    <li>Um plano de pagamento é elaborado com prazo máximo de 5 anos e parcelas compatíveis com a renda do devedor;</li>
    <li>Se houver acordo, é homologado judicialmente e vale como título executivo;</li>
    <li>Se não houver acordo com algum credor, o juiz pode impor o plano de pagamento compulsoriamente.</li>
</ol>

<h2>Quem pode se beneficiar?</h2>
<p>A lei protege o consumidor <strong>pessoa física</strong> que contraiu dívidas para consumo pessoal, não empresarial. Também é necessária a demonstração de <strong>boa-fé</strong> — quem contraiu dívidas deliberadamente para não pagar não é protegido.</p>
<p>Dívidas excluídas da proteção:</p>
<ul>
    <li>Dívidas oriundas de atividade empresarial ou profissional;</li>
    <li>Financiamentos com garantia real (hipoteca, alienação fiduciária de imóveis);</li>
    <li>Contratos de crédito imobiliário para habitação.</li>
</ul>

<h2>Práticas abusivas na cobrança de dívidas</h2>
<p>Mesmo sem superendividamento, a lei proíbe diversas práticas na cobrança:</p>
<ul>
    <li>Ligar repetidamente no mesmo dia ou em horários inconsistentes;</li>
    <li>Ameaçar ou constranger o devedor;</li>
    <li>Contato com parentes, amigos ou colegas de trabalho sobre a dívida;</li>
    <li>Proposta de acordo no momento da concessão do crédito que comprometa o mínimo existencial;</li>
    <li>Atrelar benefícios (como desconto) à renúncia de direitos legais.</li>
</ul>
<p>Cada violação a essas regras pode gerar direito a indenização por danos morais.</p>
'''
    },
    {
        "slug": "acao-indenizacao-danos-morais",
        "title": "Ação de Indenização por Danos Morais",
        "area": "Direito Civil",
        "lock": 20,
        "meta_desc": "Entenda quando cabe ação de indenização por danos morais, como comprovar e quais os valores que os tribunais costumam fixar.",
        "content": '''
<p>Dano moral é a lesão que atinge a dignidade, a honra, a intimidade, a imagem ou o bem-estar psicológico de uma pessoa. Ao contrário do dano material — que é calculado com base em prejuízos financeiros concretos —, o dano moral tem natureza subjetiva e exige avaliação criteriosa.</p>

<h2>O que é preciso provar para obter indenização?</h2>
<p>Para que o pedido de danos morais seja acolhido pela Justiça, é necessário demonstrar três elementos:</p>
<ol>
    <li><strong>Conduta ilícita:</strong> Um ato ou omissão que viole direito da vítima;</li>
    <li><strong>Nexo de causalidade:</strong> Relação de causa e efeito entre a conduta e o dano;</li>
    <li><strong>Dano efetivo:</strong> Sofrimento, constrangimento, humilhação ou abalo real à dignidade da vítima.</li>
</ol>

<div class="highlight-box">
    <p><strong>Observação:</strong> Nem todo dissabor do cotidiano gera dano moral indenizável. Os tribunais distinguem o "mero aborrecimento" — tolerável na vida social — da lesão real à personalidade.</p>
</div>

<h2>Situações mais comuns que geram dano moral</h2>
<ul>
    <li>Inclusão indevida em cadastro de devedores (SPC, Serasa) sem dívida existente;</li>
    <li>Calúnia, injúria ou difamação em redes sociais ou meios de comunicação;</li>
    <li>Assédio moral no trabalho;</li>
    <li>Violação de dados pessoais (LGPD);</li>
    <li>Descumprimento de contrato com grave repercussão pessoal (plano de saúde, seguro, banco);</li>
    <li>Acidente de trânsito com danos psíquicos;</li>
    <li>Exposição vexatória em ambiente público ou digital.</li>
</ul>

<h2>Como é calculado o valor do dano moral?</h2>
<p>O juiz tem discricionariedade para fixar o valor, mas deve considerar os seguintes critérios:</p>
<ul>
    <li><strong>Gravidade da conduta</strong> do agressor;</li>
    <li><strong>Extensão do dano</strong> e repercussão na vida da vítima;</li>
    <li><strong>Capacidade econômica</strong> do causador do dano (caráter punitivo);</li>
    <li><strong>Situação da vítima</strong> e a proporcionalidade com sua condição social;</li>
    <li><strong>Caráter pedagógico</strong> da condenação para desestimular reincidência.</li>
</ul>

<h2>Inclusão indevida no SPC/Serasa</h2>
<p>É um dos temas mais sumulados pelo Superior Tribunal de Justiça (STJ). A Súmula 385 do STJ, por exemplo, diz que o consumidor com anotações preexistentes legítimas não pode pedir dano moral por uma nova anotação indevida. Mas se a negativação for a única ou a primária, o dano é presumido e não precisa ser provado.</p>
<p>Nessas ações, os valores costumam variar entre R$ 3.000 e R$ 15.000, podendo ser maiores em casos de reincidência por parte da empresa credora.</p>
'''
    },
    {
        "slug": "usucapiao-judicial-extrajudicial",
        "title": "Usucapião Judicial e Extrajudicial (Cartório)",
        "area": "Direito Civil",
        "lock": 21,
        "meta_desc": "Saiba como funciona o processo de usucapião judicial e extrajudicial, os requisitos de cada modalidade e o que é necessário para formalizar a posse de um imóvel.",
        "content": '''
<p>Usucapião é o meio pelo qual uma pessoa que possui um bem de forma contínua, pacífica e com ânimo de dono, por determinado período, pode ter a propriedade reconhecida judicialmente ou em cartório. É um importante instrumento de regularização fundiária no Brasil.</p>

<h2>Modalidades de Usucapião no Brasil</h2>
<p>O Código Civil e leis específicas preveem diversas modalidades, com requisitos diferentes:</p>

<h3>Usucapião Ordinária (art. 1.242, CC)</h3>
<ul>
    <li>10 anos de posse contínua e ininterrupta com justo título e boa-fé;</li>
    <li>5 anos se o possuidor estabeleceu moradia habitual ou realizou obras de interesse social ou econômico.</li>
</ul>

<h3>Usucapião Extraordinária (art. 1.238, CC)</h3>
<ul>
    <li>15 anos de posse ininterrupta, sem oposição — independente de justo título ou boa-fé;</li>
    <li>Reduzido para 10 anos se usou o imóvel como moradia ou realizou obras.</li>
</ul>

<h3>Usucapião Especial Urbana (art. 183, CF / art. 1.240, CC)</h3>
<ul>
    <li>5 anos de posse ininterrupta em área urbana de até 250m²;</li>
    <li>Uso para moradia própria ou familiar;</li>
    <li>Possuidor não pode ser proprietário de outro imóvel.</li>
</ul>

<h3>Usucapião Especial Rural (art. 191, CF)</h3>
<ul>
    <li>5 anos de posse em área rural de até 50 hectares;</li>
    <li>Tornando a área produtiva com trabalho próprio ou familiar;</li>
    <li>Não possuir outro imóvel.</li>
</ul>

<div class="highlight-box">
    <p><strong>Usucapião Familiar (art. 1.240-A, CC):</strong> 2 anos de posse em imóvel urbano de até 250m², quando o cônjuge ou companheiro abandona o lar. Mais curto prazo do ordenamento brasileiro.</p>
</div>

<h2>Usucapião Extrajudicial (Cartório)</h2>
<p>Introduzida pelo Novo CPC (Lei 13.105/2015), a usucapião extrajudicial permite regularizar a posse diretamente no Cartório de Registro de Imóveis, sem precisar entrar na fila da Justiça.</p>
<p>Para isso, é necessário:</p>
<ul>
    <li>Ata notarial lavrada por tabelião atestando o tempo e as circunstâncias da posse;</li>
    <li>Planta e memorial descritivo do imóvel elaborados por engenheiro ou arquiteto;</li>
    <li>Certidões negativas de débitos tributários;</li>
    <li>Concordância de todos os confinantes (vizinhos lindeiros) com firma reconhecida;</li>
    <li>Publicação de edital para ciência de terceiros interessados.</li>
</ul>

<h2>Quando é melhor ir à Justiça?</h2>
<p>A via judicial é necessária quando há discordância de algum vizinho, oposição de um eventual proprietário registrado ou impossibilidade de obter algum documento exigido para a via extrajudicial. A ação de usucapião judicial tem rito próprio e pode durar de 2 a 5 anos dependendo da complexidade e do volume processual da comarca.</p>
<p>O advogado é indispensável nas duas vias — tanto para organizar a documentação quanto para defender os interesses do possuidor em caso de impugnações.</p>
'''
    },
    {
        "slug": "distrato-imobiliario",
        "title": "Distrato Imobiliário: Como Receber Seu Dinheiro de Volta",
        "area": "Direito Imobiliário",
        "lock": 22,
        "meta_desc": "Entenda os direitos do comprador em casos de distrato imobiliário, atraso de obra e quando a construtora pode ser responsabilizada.",
        "content": '''
<p>Comprar um imóvel na planta é uma das decisões financeiras mais importantes da vida. Quando a construtora atrasa a entrega ou quando o comprador precisa desistir, as regras de devolução do dinheiro são determinadas por lei — e muitas vezes as construtoras tentam aplicar condições mais desfavoráveis do que as previstas.</p>

<h2>O que é distrato imobiliário?</h2>
<p>Distrato é a dissolução de um contrato de compra e venda de imóvel por vontade de uma ou ambas as partes antes de sua conclusão. A Lei 13.786/2018, conhecida como "Lei do Distrato", regulamentou as regras para essa situação.</p>

<h2>Distrato por iniciativa do comprador</h2>
<p>Se você desistir do imóvel, a lei prevê que a construtora pode reter parte do valor pago para cobrir despesas administrativas. Os percentuais variam:</p>
<ul>
    <li><strong>Até 25%</strong> das parcelas pagas em empreendimentos incorporados (financiados pela própria incorporadora), acrescidos da corretagem;</li>
    <li><strong>Até 50%</strong> se o imóvel integrar patrimônio de afetação (mecanismo específico de proteção do comprador).</li>
</ul>
<p>O restante deve ser restituído em até 180 dias após a assinatura do distrato, corrigido pelo índice contratual.</p>

<div class="highlight-box">
    <p><strong>Atenção:</strong> Construtoras que inserem cláusulas de retenção superiores aos percentuais legais têm essas cláusulas declaradas nulas pelos tribunais.</p>
</div>

<h2>Distrato por culpa da construtora</h2>
<p>Se o atraso for causado pela construtora, o comprador tem direito a muito mais. Segundo o STJ e a própria Lei do Distrato:</p>
<ul>
    <li>Devolução de <strong>100% dos valores pagos</strong>, corrigidos monetariamente, em até 60 dias;</li>
    <li>Indenização de <strong>1% do valor do contrato</strong> por mês de atraso;</li>
    <li>Indenização por todos os aluguéis pagos pelo comprador durante o período do atraso;</li>
    <li>Indenização por danos morais nos casos de atraso injustificado e longo.</li>
</ul>

<h2>Prazo de tolerância de 180 dias</h2>
<p>A Lei do Distrato dá à construtora um prazo de tolerância de até 180 dias corridos após a data original de entrega para concluir a obra, sem que isso caracterize inadimplência. Esse prazo deve estar expresso no contrato.</p>
<p>Após esses 180 dias, começa a correr a multa de 1% ao mês.</p>

<h2>O que fazer se a construtora não devolver o dinheiro?</h2>
<ol>
    <li>Notifique a construtora por escrito (carta com aviso de recebimento) exigindo a devolução;</li>
    <li>Registre queixa no órgão de defesa do consumidor (Procon);</li>
    <li>Ajuíze ação com pedido de tutela antecipada para bloqueio de valores caso a construtora esteja em dificuldades financeiras.</li>
</ol>
<p>Muitos casos de distrato são resolvidos com acordos judiciais, mas a presença de um advogado especializado desde o início garante que os percentuais legais de retenção não sejam extrapolados.</p>
'''
    },
    {
        "slug": "locacao-comercial-despejo",
        "title": "Locação Comercial e Despejo",
        "area": "Direito Imobiliário",
        "lock": 23,
        "meta_desc": "Entenda as regras específicas da locação comercial, o direito à renovação compulsória e como funciona uma ação de despejo no Brasil.",
        "content": '''
<p>A locação comercial tem regras específicas que diferem — e muito — das regras da locação residencial. Lojistas, empresários e proprietários de imóveis precisam conhecer a Lei do Inquilinato (Lei 8.245/91) para proteger seus interesses e evitar surpresas custosas.</p>

<h2>Contrato de Locação Comercial: o básico</h2>
<p>Diferente da locação residencial, o contrato comercial permite às partes maior liberdade para estabelecer índices de reajuste, prazos e penalidades. No entanto, algumas regras são imperativas (não podem ser afastadas pelas partes):</p>
<ul>
    <li>O prazo mínimo para assegurar direito à renovação é de 5 anos de locação ininterrupta;</li>
    <li>O locatário tem preferência de compra em caso de venda do imóvel;</li>
    <li>Algumas benfeitorias realizadas pelo locatário podem gerar direito a indenização.</li>
</ul>

<h2>Ação Renovatória: protegendo o ponto comercial</h2>
<p>O ponto comercial tem valor econômico real — é lá que o empresário construiu sua clientela, sua reputação e seu fundo de comércio. A Lei do Inquilinato protege esse patrimônio intangível por meio da <strong>Ação Renovatória</strong>.</p>
<p>Para ter direito à renovação compulsória do contrato, o locatário deve cumprir cumulativamente:</p>
<ul>
    <li>O contrato a renovar deve ter sido escrito e com prazo mínimo de 5 anos (ou somatório de contratos que totalizem 5 anos);</li>
    <li>O prazo mínimo de 5 anos de exploração do mesmo ramo no local;</li>
    <li>Estar em dia com as obrigações do contrato.</li>
</ul>

<div class="highlight-box">
    <p><strong>Prazo fatal:</strong> A ação renovatória deve ser ajuizada entre 1 ano e 6 meses antes do término do contrato. Perder esse prazo significa perder o direito à renovação compulsória.</p>
</div>

<h2>Quando o locador pode retomar o imóvel?</h2>
<p>Mesmo com direito à renovatória, existem situações em que o locador pode retomar o imóvel:</p>
<ul>
    <li>Uso próprio ou de parente do locador (com restrições);</li>
    <li>Obras que resultem em efetiva valorização do imóvel e que inviabilizem a continuidade da locação;</li>
    <li>Proposta melhor de terceiro (com direito de igualar a proposta pelo locatário).</li>
</ul>

<h2>Ação de Despejo: como funciona?</h2>
<p>A ação de despejo é o instrumento para o locador retomar judicialmente a posse do imóvel quando o locatário não o entrega voluntariamente. As causas mais comuns são:</p>
<ul>
    <li>Inadimplência de aluguel e/ou encargos (ação de despejo por falta de pagamento);</li>
    <li>Término do prazo contratual sem renovação;</li>
    <li>Infração contratual (sublocação não autorizada, uso diferente do contratado, danos ao imóvel).</li>
</ul>
<p>O procedimento pode ser rápido: em casos de inadimplência, o locatário tem 15 dias para pagar os valores devidos ou deixar o imóvel. Se não o fizer, o expedido de despejo é expedido.</p>
'''
    },
    {
        "slug": "revisao-vida-toda-inss",
        "title": "Revisão da Vida Toda no INSS: Entenda",
        "area": "Direito Previdenciário",
        "lock": 24,
        "meta_desc": "Entenda o que é a Revisão da Vida Toda do INSS, quem tem direito e como solicitar o recálculo da aposentadoria com todos os salários de contribuição.",
        "content": '''
<p>A Revisão da Vida Toda é uma das maiores oportunidades para aposentados do INSS de revisitar o cálculo do benefício e, em muitos casos, aumentar significativamente o valor recebido mensalmente.</p>

<h2>O que é a Revisão da Vida Toda?</h2>
<p>Quando a Previdência Social foi reformada em 1994 (Plano Real), o INSS passou a considerar apenas os salários de contribuição a partir de julho de 1994 para calcular a aposentadoria — ignorando os valores pagos antes dessa data.</p>
<p>A Revisão da Vida Toda é a possibilidade de incluir <strong>todos os salários de contribuição, inclusive os anteriores a 1994</strong>, no cálculo do benefício. Muitas pessoas contribuíram com altos valores antes desse corte e foram prejudicadas ao não tê-los considerados.</p>

<div class="highlight-box">
    <p><strong>Posição do STF:</strong> Em fevereiro de 2023, o STF decidiu por maioria que a revisão é possível, mas apenas para segurados que se aposentaram antes da Reforma da Previdência de 2019. O tema ainda evolui na jurisprudência.</p>
</div>

<h2>Quem pode pedir a revisão?</h2>
<p>Para ter direito à revisão, o segurado precisa reunir as seguintes condições:</p>
<ul>
    <li>Ter se aposentado antes de novembro de 2019 (data da Reforma da Previdência);</li>
    <li>Ter contribuído com altos salários antes de julho de 1994 — pois só assim a inclusão gera aumento;</li>
    <li>Respeitar o prazo de <strong>10 anos contados da concessão do benefício</strong> (prazo decadencial do art. 103 da Lei 8.213/91).</li>
</ul>

<h2>Como calcular se vale a pena?</h2>
<p>A análise técnica é fundamental. Incluir todos os salários anteriores a 1994 <strong>nem sempre</strong> é vantajoso — dependendo dos valores, o novo cálculo pode resultar em benefício menor. Por isso, é necessário um estudo atuarial individual antes de ingressar com qualquer revisão.</p>
<p>O advogado previdenciário extrai o Cnis (Cadastro Nacional de Informações Sociais) do cliente, simula o novo cálculo com e sem a inclusão dos salários pré-94, e só recomenda a revisão quando há ganho financeiro real.</p>

<h2>Prazo para pedir a revisão</h2>
<p>O prazo é de <strong>10 anos</strong> a contar da concessão original do benefício. Após esse prazo, o direito se extingue (decadência). Aposentados que estão próximos do décimo aniversário do benefício devem agir com urgência.</p>

<h2>Como solicitar?</h2>
<ol>
    <li>Administrativamente: pedido de revisão junto ao INSS (mais demorado e com alta taxa de indeferimento);</li>
    <li>Judicialmente: ação de revisão de benefício previdenciário na Justiça Federal ou no Juizado Especial Federal.</li>
</ol>
<p>A via judicial costuma ser mais eficaz, especialmente quando acompanhada de cálculos bem fundamentados elaborados por contador previdenciário.</p>
'''
    },
    {
        "slug": "bpc-loas",
        "title": "Benefício de Prestação Continuada (BPC / LOAS)",
        "area": "Direito Previdenciário",
        "lock": 25,
        "meta_desc": "Saiba como funciona o BPC-LOAS, os critérios de renda para concessão e como a via judicial pode ampliar as possibilidades de aprovação.",
        "content": '''
<p>O Benefício de Prestação Continuada (BPC), também chamado de LOAS (Lei Orgânica da Assistência Social), é um benefício assistencial — não previdenciário — que garante um salário mínimo mensal para idosos acima de 65 anos e para Pessoas com Deficiência (PcD) de qualquer idade que comprovem hipossuficiência financeira.</p>

<h2>Quem tem direito ao BPC?</h2>
<p>Para ter direito ao benefício, é necessário:</p>
<ul>
    <li><strong>Idosos:</strong> ter 65 anos ou mais e renda familiar per capita inferior a 1/4 do salário mínimo;</li>
    <li><strong>PcD:</strong> ter deficiência de longo prazo (mínimo 2 anos) que impeça ou dificulte a participação plena na sociedade — e a mesma regra de renda;</li>
    <li>Não receber outro benefício do regime geral ou especial de previdência social (com exceções).</li>
</ul>

<div class="highlight-box">
    <p><strong>Renda per capita:</strong> divide-se a renda mensal total da família (moradores do mesmo domicílio) pelo número de integrantes. Se o resultado for inferior a 1/4 do salário mínimo (cerca de R$ 330 em 2026), o critério econômico é atendido.</p>
</div>

<h2>Gastos médicos podem reduzir a renda computada</h2>
<p>Uma das possibilidades mais desconhecidas é que, por entendimento dos tribunais (em especial STJ e TNU — Turma Nacional de Uniformização dos Juizados Especiais Federais), <strong>despesas médicas e de medicamentos</strong> comprovadas podem ser deduzidas da renda familiar para efeito do cálculo.</p>
<p>Isso significa que famílias com renda levemente superior ao limite de 1/4 do salário mínimo, mas com gastos pesados com saúde de um familiar, podem ter o direito ao BPC reconhecido judicialmente.</p>

<h2>BPC sendo negado pelo INSS: o que fazer?</h2>
<p>O INSS aplica os critérios legais de forma rígida e frequentemente nega o benefício a pessoas que, com uma análise mais aprofundada, fariam jus a ele. As principais razões de negativa são:</p>
<ul>
    <li>Renda per capita acima do limite (1/4 do salário mínimo);</li>
    <li>Deficiência não reconhecida como "de longo prazo" pelos peritos do INSS;</li>
    <li>Composição familiar incorretamente considerada;</li>
    <li>Documentação insuficiente.</li>
</ul>
<p>Nesses casos, a ação judicial no Juizado Especial Federal é o caminho mais eficaz. O juiz pode determinar avaliação biopsicossocial e considerar critérios mais amplos do que os usados pelo INSS administrativamente.</p>

<h2>Cumulação com outros benefícios</h2>
<p>Via de regra, o BPC não pode ser acumulado com aposentadoria ou pensão. No entanto, existe a possibilidade de o cônjuge ou filho com deficiência acumular com benefício de membro da família — tema que já foi objeto de decisão favorável nos tribunais em determinadas situações.</p>
'''
    },
    {
        "slug": "erro-medico-tratamento-indevido",
        "title": "Erro Médico e Tratamento Indevido",
        "area": "Direito da Saúde",
        "lock": 26,
        "meta_desc": "Como funciona juridicamente uma ação por erro médico? Entenda o nexo de causalidade, a responsabilidade subjetiva e as providências que devem ser tomadas.",
        "content": '''
<p>Ações por erro médico estão entre as mais complexas do direito. Elas envolvem conhecimento técnico especializado, documentação extensa e prazos que não podem ser ignorados. Se você ou alguém da sua família sofreu danos em decorrência de um procedimento médico mal executado, é essencial conhecer seus direitos.</p>

<h2>O que é erro médico juridicamente?</h2>
<p>O erro médico, do ponto de vista jurídico, é a conduta culposa do profissional de saúde — por imperícia, negligência ou imprudência — que cause danos ao paciente. Difere-se do chamado <strong>insucesso terapêutico</strong>, que é o resultado negativo de um procedimento tecnicamente correto.</p>

<div class="highlight-box">
    <p><strong>Responsabilidade Subjetiva:</strong> O médico (profissional liberal) tem responsabilidade subjetiva, o que significa que o paciente precisa provar a culpa — diferente da responsabilidade objetiva, onde basta provar o dano e o nexo causal.</p>
</div>

<h2>Obrigação de Meio x Obrigação de Resultado</h2>
<p>O médico, em geral, tem <strong>obrigação de meio</strong>, não de resultado — ou seja, deve agir com todas as técnicas e diligências adequadas para buscar a cura, mas não é responsável pelo insucesso quando age corretamente.</p>
<p>Exceção importante: procedimentos estéticos geram <strong>obrigação de resultado</strong>. O cirurgião plástico que promete determinado resultado e não o entrega pode ser responsabilizado independentemente de culpa.</p>

<h2>Como provar o erro médico?</h2>
<p>A prova é a parte mais crítica. Os principais documentos e medidas são:</p>
<ul>
    <li><strong>Prontuário médico completo:</strong> É obrigação do hospital/clínica fornecer; guarda todas as informações sobre o tratamento;</li>
    <li><strong>Laudo médico de outro especialista</strong> que aponte o erro;</li>
    <li><strong>Perícia médica judicial:</strong> O juiz nomeia um perito independente para avaliar o caso;</li>
    <li><strong>Boletim de Ocorrência</strong> e notificação ao CRM (Conselho Regional de Medicina) do profissional.</li>
</ul>

<h2>Responsabilidade do Hospital</h2>
<p>Se o erro foi cometido por um médico que é funcionário do hospital ou em produto ou serviço do hospital (anestesia, enfermagem, equipamentos), o estabelecimento pode ser responsabilizado de forma objetiva (sem necessidade de provar culpa), conforme o CDC.</p>
<p>Médicos autônomos que apenas utilizam as instalações do hospital, porém, têm sua responsabilidade analisada individualmente.</p>

<h2>Prazos para agir</h2>
<ul>
    <li><strong>Ação civil de reparação:</strong> 3 anos a contar do conhecimento do dano e de sua autoria (art. 206, §3º, V, CC);</li>
    <li><strong>Ação contra o Estado / médico de hospital público:</strong> 5 anos (Decreto 20.910/32);</li>
    <li><strong>Processo no CRM:</strong> 5 anos a contar do ato que gerou a reclamação.</li>
</ul>
<p>Não espere. Quanto antes a documentação for coletada e preservada, maiores as chances de sucesso em eventual ação.</p>
'''
    },
    {
        "slug": "medicamentos-alto-custo",
        "title": "Acesso a Medicamentos de Alto Custo (SUS e Convênio)",
        "area": "Direito da Saúde",
        "lock": 27,
        "meta_desc": "Como funciona a judicialização de medicamentos de alto custo? Entenda como obter remédios pelo SUS ou pelo plano de saúde com apoio jurídico.",
        "content": '''
<p>Medicamentos de alto custo — como os utilizados em oncologia, doenças raras, terapias com canabidiol e imunobiológicos — podem custar dezenas de milhares de reais por mês. Quando o sistema público ou o plano de saúde nega o fornecimento, a via judicial muitas vezes é o único caminho real.</p>

<h2>Medicamentos pelo SUS</h2>
<p>O Sistema Único de Saúde (SUS) possui um Componente Especializado da Assistência Farmacêutica (CEAF) que disponibiliza medicamentos de alto custo para certas condições clínicas. Quando o medicamento está na lista do CEAF e o estado nega o fornecimento, cabe ação judicial imediata.</p>
<p>Quando o medicamento <strong>não está no CEAF</strong>, a jurisprudência exige, em geral, que o paciente comprove:</p>
<ul>
    <li>Comprovação médica da necessidade (laudo detalhado com CID);</li>
    <li>Inefetividade ou inadequação das alternativas disponíveis no SUS;</li>
    <li>Registro do medicamento na Anvisa (ou autorização excepcional);</li>
    <li>Incapacidade financeira do paciente de arcar com o custo.</li>
</ul>

<div class="highlight-box">
    <p><strong>Tese do STJ/STF:</strong> A jurisprudência tem evoluído para exigir que o medicamento esteja registrado na Anvisa como condição para fornecimento compulsório pelo Estado, salvo casos excepcionais com recomendação de organismo internacional.</p>
</div>

<h2>Medicamentos pelo Plano de Saúde</h2>
<p>Os planos de saúde devem cobrir medicamentos prescritos para uso durante internação hospitalar. Para uso domiciliar, a cobertura depende do contrato e do Rol da ANS.</p>
<p>A Agência Nacional de Saúde Suplementar tem ampliado o rol de cobertura obrigatória, incluindo medicamentos oncológicos orais de uso domiciliar. Negativas nessa área costumam ser facilmente revertidas judicialmente.</p>

<h2>Ação judicial: Mandado de Segurança ou Ação Ordinária?</h2>
<h3>Mandado de Segurança (contra o Estado)</h3>
<p>Adequado quando o órgão público (Secretaria de Saúde estadual ou municipal) nega o fornecimento. O prazo de resposta é curto — o juiz pode conceder a liminar em 48 horas em casos urgentes.</p>

<h3>Ação Ordinária com Tutela Antecipada de Urgência</h3>
<p>Usada tanto contra o Estado quanto contra planos de saúde. Permite obter a liminar em plantão judicial, inclusive nos finais de semana, nos casos mais graves (risco imediato de morte ou agravamento irreversível da condição).</p>

<h2>Como preparar o pedido judicial?</h2>
<ul>
    <li>Laudo médico detalhado com diagnóstico (CID), justificativa para o medicamento específico e registro de tentativas com medicamentos alternativos;</li>
    <li>Orçamentos do medicamento comprovando o custo;</li>
    <li>Documentos pessoais do paciente e comprovação de incapacidade financeira (para ações contra o SUS);</li>
    <li>Comprovante de negativa do plano ou do órgão público (formal, por escrito).</li>
</ul>
<p>Com esses documentos em mãos, um advogado especializado em saúde pode ingressar com a ação e obter a liminar em prazo muito curto — muitas vezes em menos de 48 horas.</p>
'''
    },
    {
        "slug": "inventario-extrajudicial",
        "title": "Inventário Extrajudicial: Velocidade na Partilha",
        "area": "Família e Sucessões",
        "lock": 28,
        "meta_desc": "Como funciona o inventário extrajudicial em cartório? Saiba os requisitos, os impostos envolvidos e as vantagens em relação ao inventário judicial.",
        "content": '''
<p>Perder um familiar já é uma experiência difícil. Ter que enfrentar anos de inventário judicial então pode ser devastador — tanto emocional quanto financeiramente. O inventário extrajudicial, realizado diretamente em cartório, nasceu para tornar esse processo muito mais rápido e menos oneroso.</p>

<h2>O que é o inventário extrajudicial?</h2>
<p>O inventário extrajudicial é o procedimento realizado em Cartório de Notas para partilhar os bens deixados pelo falecido, sem necessidade de processo judicial. Foi regulamentado pelo art. 610 do CPC de 2015 e pela Resolução 35 do CNJ.</p>

<h2>Quais são os requisitos?</h2>
<p>Para que o inventário possa ser feito em cartório, é necessário:</p>
<ul>
    <li>Todos os herdeiros devem ser maiores e capazes (maiores de 18 anos e sem impedimento mental);</li>
    <li>Não pode haver testamento (ou o testamento deve ter sido previamente aberto e cumprido judicialmente);</li>
    <li>Todos os herdeiros devem estar de acordo com a partilha;</li>
    <li>Todos devem estar representados por advogado;</li>
    <li>Capacidade tributária: pagamento do ITCMD (imposto sobre herança/doação).</li>
</ul>

<div class="highlight-box">
    <p><strong>Prazo comparativo:</strong> Um inventário judicial médio leva de 2 a 5 anos. Um inventário extrajudicial bem preparado pode ser concluído em 30 a 90 dias.</p>
</div>

<h2>Quais impostos incidem?</h2>
<h3>ITCMD (Imposto sobre Transmissão Causa Mortis e Doação)</h3>
<p>É o imposto estadual que incide sobre heranças e doações. Cada estado tem sua própria alíquota e legislação. No estado de São Paulo, por exemplo, a alíquota é de 4% sobre o valor dos bens. No Rio de Janeiro, pode chegar a 8% progressivo.</p>

<h3>ITBI (Imposto sobre Transmissão de Bens Imóveis)</h3>
<p>Em geral não incide no inventário, pois é tributo municipal cobrado sobre a <em>compra e venda</em> de imóveis. Mas pode haver cobrança na partilha de imóveis em situações específicas que o advogado deve avaliar.</p>

<h2>Quais bens podem ser partilhados no cartório?</h2>
<ul>
    <li>Imóveis (casa, apartamento, terreno, rural);</li>
    <li>Veículos;</li>
    <li>Saldo em contas bancárias e investimentos;</li>
    <li>Cotas de empresas e participações societárias;</li>
    <li>Jóias, obras de arte e outros bens de valor declarados.</li>
</ul>

<h2>Papel do advogado no inventário extrajudicial</h2>
<p>A presença de um advogado é obrigatória no inventário extrajudicial — e não é burocracia: o advogado garante que os interesses de cada herdeiro sejam protegidos, que os cálculos de tributos sejam feitos corretamente e que o resultado registrado em escritura pública seja juridicamente correto e irrevogável.</p>
'''
    },
    {
        "slug": "guarda-compartilhada-unilateral",
        "title": "Guarda Compartilhada vs Guarda Unilateral",
        "area": "Família e Sucessões",
        "lock": 29,
        "meta_desc": "Entenda as diferenças entre guarda compartilhada e unilateral, como a lei brasileira atual trata o tema e os impactos na pensão alimentícia.",
        "content": '''
<p>O fim de um relacionamento é sempre um momento difícil. Quando há filhos envolvidos, a definição da guarda é uma das decisões mais importantes — e mais carregadas de emoção — que os pais precisam tomar. O direito brasileiro tem regras claras sobre o assunto, com foco no bem-estar da criança.</p>

<h2>O que é guarda compartilhada?</h2>
<p>A guarda compartilhada, regulamentada pela Lei 13.058/2014, é o modelo em que ambos os pais exercem a guarda de forma igualitária — ou seja, ambos participam ativamente das decisões sobre educação, saúde, lazer e criação dos filhos.</p>
<p>Isso <strong>não significa</strong> que a criança ficará metade do tempo com o pai e metade com a mãe. A residência habitual pode ser definida em acordo, e a convivência com o outro genitor é estabelecida de forma equilibrada.</p>

<div class="highlight-box">
    <p><strong>Regra legal:</strong> Desde 2014, a guarda compartilhada é a regra preferencial no Brasil — mesmo quando os pais não concordam entre si. O juiz só opta pela guarda unilateral quando há razão específica que comprometa o bem-estar da criança (violência doméstica, uso de drogas, incapacidade parental comprovada).</p>
</div>

<h2>O que é guarda unilateral?</h2>
<p>Na guarda unilateral, apenas um dos pais tem a guarda legal — ficando responsável pelas decisões cotidianas sobre a criança. O outro genitor tem o direito de visita regulamentado, mas não participa das decisões.</p>
<p>O pai ou mãe sem a guarda paga alimentos à criança como contribuição para as despesas que o guardião arca no dia a dia.</p>

<h2>Guarda compartilhada e pensão alimentícia</h2>
<p>Um dos pontos mais controversos: a guarda compartilhada elimina a obrigação de pagar pensão alimentícia?</p>
<p><strong>Não automaticamente.</strong> A pensão é calculada com base no <strong>binômio necessidade/possibilidade</strong>:</p>
<ul>
    <li><strong>Necessidade:</strong> O quanto a criança precisa para manter seu padrão de vida (educação, saúde, vestuário, lazer);</li>
    <li><strong>Possibilidade:</strong> A capacidade econômica de cada genitor para contribuir com essas despesas.</li>
</ul>
<p>Se um dos pais ganha muito mais que o outro, o mais abastado continuará pagando alimentos mesmo na guarda compartilhada — pois a igualdade de tempo não implica igualdade financeira automática.</p>

<h2>Como é definida a guarda em disputas judiciais?</h2>
<p>O juiz sempre decide com base no <strong>melhor interesse da criança</strong>, analisando:</p>
<ul>
    <li>Laços afetivos com cada genitor;</li>
    <li>Capacidade de cada um de prover as necessidades da criança;</li>
    <li>Histórico de continuidade das rotinas (escola, amigos, atividades);</li>
    <li>Saúde física e mental de cada genitor;</li>
    <li>Disposição de cada genitor para facilitar o convívio com o outro.</li>
</ul>
<p>Em casos complexos, o juiz pode determinar estudo social, avaliação psicológica e oitiva da criança para fundamentar a decisão.</p>
'''
    },
    {
        "slug": "exclusao-icms-pis-cofins",
        "title": "Exclusão do ICMS da base do PIS/COFINS",
        "area": "Direito Tributário",
        "lock": 30,
        "meta_desc": "Entenda a 'tese do século': como a exclusão do ICMS da base do PIS/COFINS funciona e como sua empresa pode recuperar créditos tributários.",
        "content": '''
<p>A chamada "tese do século" foi decidida pelo Supremo Tribunal Federal em 2021: o ICMS não compõe a base de cálculo do PIS e da COFINS. Empresas que contribuíram com valores incorretos têm direito à restituição — um impacto bilionário que as corporações brasileiras ainda estão absorvendo.</p>

<h2>O que é a tese do século?</h2>
<p>Durante décadas, o fisco brasileiro exigiu que as empresas calculassem o PIS e a COFINS sobre o faturamento bruto, que incluía o ICMS. Ocorre que o ICMS — um imposto estadual cobrado "por dentro" do preço — nunca pertence à empresa: ela apenas o repassa ao Estado.</p>
<p>O STF, ao decidir o Recurso Extraordinário 574.706/PR em repercussão geral, reconheceu que incluir o ICMS na base do PIS/COFINS é inconstitucional, pois o ICMS não é receita da empresa.</p>

<div class="highlight-box">
    <p><strong>Modulação dos efeitos:</strong> O STF modulou os efeitos da decisão para 2017, salvo para quem já tinha ação ou pedido administrativo anterior. Isso limita o período de recuperação para quem não ajuizou a tempo.</p>
</div>

<h2>Quem tem direito à restituição?</h2>
<p>Empresas tributadas pelo Lucro Real e pelo Lucro Presumido que pagaram PIS/COFINS sobre uma base que incluía o ICMS. As empresas do Simples Nacional <strong>não são contempladas</strong> por esse regime específico.</p>

<h2>Quanto podem recuperar?</h2>
<p>O valor depende do porte da empresa e do período em que o ICMS foi indevidamente incluído na base. Para grandes varejistas, distribuidoras e indústrias, os valores costumam ser expressivos — na ordem de centenas de milhares a milhões de reais.</p>
<p>Para calcular, é necessário levantar todas as guias de PIS/COFINS pagas e os registros de ICMS do período recuperável, o que demanda trabalho contábil especializado.</p>

<h2>Como recuperar os créditos?</h2>
<p>Existem dois caminhos:</p>
<ul>
    <li><strong>Via administrativa (Receita Federal):</strong> Pedido de restituição ou compensação via PERDCOMP. Mais lento e sujeito a revisão pela Receita;</li>
    <li><strong>Via judicial:</strong> Ação de repetição de indébito tributário. Mais seguro para preservar o direito, especialmente quando há risco de a Receita questionar a metodologia de cálculo.</li>
</ul>
<p>A compensação é a forma mais prática: em vez de receber o dinheiro de volta, a empresa abate o crédito de tributos futuros — melhorando imediatamente o fluxo de caixa.</p>

<h2>Atenção ao prazo prescricional</h2>
<p>O prazo para pedir restituição de tributos é de <strong>5 anos</strong> a contar do pagamento indevido. Empresas que ainda não ajuizaram a ação devem fazê-lo com urgência para não perder os créditos mais antigos.</p>
'''
    },
    {
        "slug": "doacao-reserva-usufruto",
        "title": "Doação com Reserva de Usufruto",
        "area": "Planejamento Sucessório",
        "lock": 31,
        "meta_desc": "Como funciona a doação com reserva de usufruto e por que é uma das estratégias mais vantajosas de planejamento sucessório e proteção patrimonial.",
        "content": '''
<p>Planejar a sucessão enquanto ainda se está em plena atividade é um ato de responsabilidade e amor pela família. A doação com reserva de usufruto é uma das ferramentas mais eficientes para transmitir patrimônio aos herdeiros em vida, com segurança e economia tributária.</p>

<h2>O que é doação com reserva de usufruto?</h2>
<p>É uma operação em dois passos:</p>
<ol>
    <li>O proprietário (doador) transmite o <strong>bem em si</strong> (a "nua-propriedade") ao herdeiro (donatário);</li>
    <li>Mas <strong>reserva para si o usufruto</strong>, que é o direito de usar, usufruir e perceber os frutos (aluguéis, por exemplo) do bem enquanto viver.</li>
</ol>
<p>Na prática: o filho recebe o imóvel no papel, mas os pais continuam morando nele ou recebendo o aluguel até a morte — quando então o usufruto se extingue e o filho passa a ter a propriedade plena automaticamente.</p>

<h2>Por que é vantajoso do ponto de vista tributário?</h2>
<p>A doação com reserva de usufruto <strong>evita o inventário</strong>. Quando o doador falece, o imóvel não entra no espólio — pois já foi transmitido ao donatário em vida. Isso significa:</p>
<ul>
    <li>Sem necessidade de inventário judicial ou extrajudicial para esse bem;</li>
    <li>Economia nos honorários advocatícios e custas cartoriais do inventário;</li>
    <li>Menor base de cálculo do ITCMD no момент da doação versus o valor no momento da morte (bens podem valorizar muito);</li>
    <li>Rapidez na transmissão — o herdeiro já tem o bem registrado em seu nome antes da morte do doador.</li>
</ul>

<div class="highlight-box">
    <p><strong>Atenção ao ITCMD:</strong> A doação gera incidência do ITCMD. Porém, o imposto é calculado sobre o valor da nua-propriedade (descontado o usufruto), que é menor que o valor integral do bem — resultando em economia real.</p>
</div>

<h2>Cláusulas protetoras que podem ser inseridas</h2>
<h3>Inalienabilidade</h3>
<p>O donatário (filho) fica impedido de vender, hipotecar ou dar o bem em garantia enquanto a cláusula vigorar. Protege contra decisões precipitadas ou pressão de credores.</p>

<h3>Impenhorabilidade</h3>
<p>O bem não pode ser penhorado por dívidas do donatário — exceto dívidas de alimentos e tributos incidentes sobre o próprio bem.</p>

<h3>Incomunicabilidade</h3>
<p>O bem não entra na comunhão com o cônjuge ou companheiro do donatário. Se ele se separar, o bem permanece exclusivamente seu.</p>

<h2>Revogação da doação é possível?</h2>
<p>A lei permite a revogação da doação em casos de <strong>ingratidão</strong> do donatário (atentado contra a vida, crimes, injúria grave). Isso serve como proteção adicional ao doador, que pode desfazer a doação em situações extremas.</p>
<p>A revogação também é possível quando a doação compromete o sustento do doador — uma proteção legal para garantir que o ato de generosidade não coloque o doador em situação de indigência.</p>

<h2>Conclusão</h2>
<p>A doação com reserva de usufruto é uma estratégia elegante e eficaz que une planejamento sucessório, proteção patrimonial e economia tributária. Mas exige assessoria jurídica especializada para que os documentos — especialmente a escritura pública — sejam redigidos com as cláusulas e proteções corretas.</p>
'''
    },
]

def build_article_page(article):
    img_url = f"https://picsum.photos/seed/cursi-artigo-{article['lock']}/1200/600"
    return NAV_TEMPLATE.format(
        meta_desc=article['meta_desc'],
        title=article['title'],
        area=article['area'],
        img_url=img_url,
        content=article['content']
    )

# Generate all article pages
for art in ARTICLES:
    page_html = build_article_page(art)
    path = f"pages/artigos/{art['slug']}.html"
    with open(path, 'w', encoding='utf-8') as f:
        f.write(page_html)
    print(f"  Created: {path}")

print(f"\n{len(ARTICLES)} article pages generated.")

# Now update blog.html
# Build slug lookup by lock number
lock_to_slug = {art['lock']: art['slug'] for art in ARTICLES}

with open('blog.html', 'r', encoding='utf-8') as f:
    blog_html = f.read()

import re

def replace_card_button(html, lock_num, slug):
    """Update each card's button href and text."""
    # Find the pattern: lock=XX in image-card__img and the associated button
    # Strategy: split by card, process each
    new_href = f"pages/artigos/{slug}.html"
    # Replace the button that follows a card with lock=XX
    # The button currently links to #contato
    # Pattern: within the same card block that has lock=XX, find the btn--primary that says "Tirar"
    # We do it section by section to be safe
    pattern = re.compile(
        r'(lock=' + str(lock_num) + r'.*?<a href="[^"]*" class="btn btn--primary"[^>]*>)[^<]*(</a>)',
        re.DOTALL
    )
    replacement = r'\g<1>Abrir o Artigo Completo</\g<2>'

    # More precise approach: find each card block
    # Replace href and text for the button in the card with the given lock
    def replacer(m):
        block = m.group(0)
        # Replace href
        block = re.sub(r'<a href="[^"]*" class="btn btn--primary"', f'<a href="{new_href}" class="btn btn--primary"', block)
        # Replace button text (between > and </a>)
        block = re.sub(r'(class="btn btn--primary"[^>]*>)[^<]*(</a>)', r'\1Abrir o Artigo Completo\2', block)
        return block

    card_pattern = re.compile(
        r'<div class="image-card".*?</div>\s*</div>',
        re.DOTALL
    )

    return html

# Better approach: replace all button texts and hrefs in cards
# Each card has a specific lock=NN value, find the card containing that lock
for lock_num, slug in lock_to_slug.items():
    new_href = f"pages/artigos/{slug}.html"
    # Find div containing this lock and update its button
    # Pattern: find the card block containing lock=XX
    card_re = re.compile(
        r'(<div class="image-card".*?lock=' + str(lock_num) + r'.*?<a\s+href=")[^"]*(".*?class="btn btn--primary"[^>]*>)[^<]*(</a>)',
        re.DOTALL
    )

    def make_replacer(href, slug_name):
        def replacer(m):
            return m.group(1) + href + m.group(2) + 'Abrir o Artigo Completo' + m.group(3)
        return replacer

    blog_html = card_re.sub(make_replacer(new_href, slug), blog_html)

# Also fix the section CTA button at the bottom
blog_html = blog_html.replace(
    '<a href="#contato" class="btn btn--primary" style="margin-top: 2rem;">Entre em Contato Conosco</a>',
    '<a href="index.html#contato" class="btn btn--primary" style="margin-top: 2rem;">Fale com o Dr. Estevão Cursi</a>'
)

with open('blog.html', 'w', encoding='utf-8') as f:
    f.write(blog_html)

print("\nblog.html updated with article links and new button text.")
print("\nDone!")
