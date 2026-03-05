$html = Get-Content index.html -Raw -Encoding UTF8
$newGrid = @'
<div class="grid grid--2" style="gap: 2.5rem;">
    <!-- Área 1: Execução Cível e Trabalhista -->
    <a href="pages/execucao-civel-trabalhista.html" class="image-card">
        <div class="image-card__img" style="background-image: url('https://images.unsplash.com/photo-1589829085413-56de8ae18c73?q=80&w=800&auto=format&fit=crop');"></div>
        <div class="image-card__content">
            <div style="font-size: 0.75rem; text-transform: uppercase; color: var(--accent-blue); letter-spacing: 1px; margin-bottom: 0.8rem; font-weight: bold;">Atuação Especializada</div>
            <h3 class="image-card__title">Execução Cível e Trabalhista</h3>
            <div class="image-card__desc">Expertise em execução de <strong>processos trabalhistas e cíveis</strong> aplicando mapeamento patrimonial avançado (IDPJ). Localização estratégica de ativos com foco em desfecho cirúrgico de inadimplência em processos crônicos.</div>
            <div class="image-card__action" style="color: var(--accent-blue);">Iniciar Recuperação <span style="font-size: 1.2rem; margin-left: 5px;">&rarr;</span></div>
        </div>
    </a>

    <!-- Área 2: Assessoria de Empresas -->
    <a href="pages/assessoria-empresas.html" class="image-card">
        <div class="image-card__img" style="background-image: url('https://images.unsplash.com/photo-1497366216548-37526070297c?q=80&w=800&auto=format&fit=crop');"></div>
        <div class="image-card__content">
            <div style="font-size: 0.75rem; text-transform: uppercase; color: var(--accent-purple); letter-spacing: 1px; margin-bottom: 0.8rem; font-weight: bold;">Atuação Especializada</div>
            <h3 class="image-card__title">Assessoria de Empresas</h3>
            <div class="image-card__desc">Escudo legal projetado para <strong>empresas de médio e pequeno porte</strong>. Blindagem corporativa, defesas trabalhistas e auditoria focada na perpetuidade e blindagem do seu negócio.</div>
            <div class="image-card__action" style="color: var(--accent-purple);">Proteger Perímetro <span style="font-size: 1.2rem; margin-left: 5px;">&rarr;</span></div>
        </div>
    </a>

    <!-- Área 3: Prisões e Defesa Criminal -->
    <a href="pages/prisoes.html" class="image-card">
        <div class="image-card__img" style="background-image: url('https://images.unsplash.com/photo-1589391886645-d51941baf7fb?q=80&w=800&auto=format&fit=crop'); filter: grayscale(30%) contrast(120%);"></div>
        <div class="image-card__content">
            <div style="font-size: 0.75rem; text-transform: uppercase; color: var(--accent-gold); letter-spacing: 1px; margin-bottom: 0.8rem; font-weight: bold;">Atuação Especializada</div>
            <h3 class="image-card__title">Defesa Criminal de Urgência</h3>
            <div class="image-card__desc">Intervenção de contingência <strong>24/7 em delegacias e audiências de custódia</strong>. Arquitetura probatória rigorosa garantindo a integridade dos direitos fundamentais do assistido.</div>
            <div class="image-card__action" style="color: var(--accent-gold);">Plantão de Defesa <span style="font-size: 1.2rem; margin-left: 5px;">&rarr;</span></div>
        </div>
    </a>

    <!-- Área 4: Direito da Saúde -->
    <a href="pages/direito-saude.html" class="image-card">
        <div class="image-card__img" style="background-image: url('https://images.unsplash.com/photo-1576091160550-2173dba999ef?q=80&w=800&auto=format&fit=crop');"></div>
        <div class="image-card__content">
            <div style="font-size: 0.75rem; text-transform: uppercase; color: var(--accent-green); letter-spacing: 1px; margin-bottom: 0.8rem; font-weight: bold;">Atuação Especializada</div>
            <h3 class="image-card__title">Jurisprudência de Saúde</h3>
            <div class="image-card__desc">Contencioso de alto risco contra convênios médicos, tutelas antecipadas para liberação de tratamentos urgentes (Oncologia/TEA), além de mediação de erro médico.</div>
            <div class="image-card__action" style="color: var(--accent-green);">Acionar Urgência <span style="font-size: 1.2rem; margin-left: 5px;">&rarr;</span></div>
        </div>
    </a>

    <!-- Área 5: Família e Sucessões -->
    <a href="#contato" class="image-card">
        <div class="image-card__img" style="background-image: url('https://images.unsplash.com/photo-1600880292203-757bb62b4baf?q=80&w=800&auto=format&fit=crop');"></div>
        <div class="image-card__content">
            <div style="font-size: 0.75rem; text-transform: uppercase; color: #a1a1aa; letter-spacing: 1px; margin-bottom: 0.8rem; font-weight: bold;">Atuação Geral</div>
            <h3 class="image-card__title">Direito de Família e Sucessões</h3>
            <div class="image-card__desc">Resolução estratégica de divórcios, partilha de bens, planejamento sucessório e inventários. Atuação ágil buscando a integridade do patrimônio e conciliação do núcleo familiar.</div>
            <div class="image-card__action" style="color: #e4e4e7;">Consultar Causa Familiar <span style="font-size: 1.2rem; margin-left: 5px;">&rarr;</span></div>
        </div>
    </a>

    <!-- Área 6: Direito Imobiliário -->
    <a href="#contato" class="image-card">
        <div class="image-card__img" style="background-image: url('https://images.unsplash.com/photo-1560518883-ce09059eeffa?q=80&w=800&auto=format&fit=crop');"></div>
        <div class="image-card__content">
            <div style="font-size: 0.75rem; text-transform: uppercase; color: #a1a1aa; letter-spacing: 1px; margin-bottom: 0.8rem; font-weight: bold;">Atuação Geral</div>
            <h3 class="image-card__title">Direito Imobiliário e Contratos</h3>
            <div class="image-card__desc">Assessoria técnica em transações de imóveis, auditoria de contratos de compra e venda, ações de usucapião, regularização fundiária e gerenciamento de distratos.</div>
            <div class="image-card__action" style="color: #e4e4e7;">Garantir Propriedade <span style="font-size: 1.2rem; margin-left: 5px;">&rarr;</span></div>
        </div>
    </a>

    <!-- Área 7: Direito do Consumidor e Bancário -->
    <a href="#contato" class="image-card">
        <div class="image-card__img" style="background-image: url('https://images.unsplash.com/photo-1505373877841-8d25f7d46678?q=80&w=800&auto=format&fit=crop');"></div>
        <div class="image-card__content">
            <div style="font-size: 0.75rem; text-transform: uppercase; color: #a1a1aa; letter-spacing: 1px; margin-bottom: 0.8rem; font-weight: bold;">Atuação Geral</div>
            <h3 class="image-card__title">Defesa do Consumidor e Bancário</h3>
            <div class="image-card__desc">Combate judicial a juros bancários abusivos, suspensão de negativações indevidas, fraudes financeiras e proteção do consumidor frente às grandes corporações.</div>
            <div class="image-card__action" style="color: #e4e4e7;">Restaurar Direitos <span style="font-size: 1.2rem; margin-left: 5px;">&rarr;</span></div>
        </div>
    </a>

    <!-- Área 8: Planejamento Tributário / Previdenciário -->
    <a href="#contato" class="image-card">
        <div class="image-card__img" style="background-image: url('https://images.unsplash.com/photo-1554224155-6726b3ff858f?q=80&w=800&auto=format&fit=crop'); filter: brightness(0.8) contrast(1.1);"></div>
        <div class="image-card__content">
            <div style="font-size: 0.75rem; text-transform: uppercase; color: #a1a1aa; letter-spacing: 1px; margin-bottom: 0.8rem; font-weight: bold;">Atuação Geral</div>
            <h3 class="image-card__title">Direito Tributário Consultivo</h3>
            <div class="image-card__desc">Atuação em defesas de execuções fiscais, recuperação de créditos impositivos e teses complexas com escopo focado em mitigação lícita de carga tributária e passivos.</div>
            <div class="image-card__action" style="color: #e4e4e7;">Blindagem Fiscal <span style="font-size: 1.2rem; margin-left: 5px;">&rarr;</span></div>
        </div>
    </a>
</div>
'@

$html = $html -replace '(?s)<div class="grid grid--2" style="gap: 2.5rem;">.*?</section>', ("$newGrid
              </div>
          </section>")
Set-Content index.html -Value $html -Encoding UTF8
Write-Host "Atualizacao Concluida"
