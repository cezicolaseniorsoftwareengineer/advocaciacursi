$html = Get-Content index.html -Raw -Encoding UTF8

$newGrid = @'
                <div class="grid grid--2" style="gap: 2.5rem;">

                    <!-- Área 1: Execução Cível e Trabalhista -->
                    <a href="pages/execucao-civel-trabalhista.html" class="image-card">
                        <div class="image-card__img" style="background-image: url('https://images.unsplash.com/photo-1589829085413-56de8ae18c73?q=80&w=800&auto=format&fit=crop');">
                            <div class="image-card__icon" style="color: var(--accent-blue); border: 1px solid rgba(59,130,246,0.5);">EC</div>
                        </div>
                        <div class="image-card__content">
                            <h3 class="image-card__title">Execução Cível e Trabalhista</h3>
                            <div class="image-card__desc">
                                Expertise em execução de <strong>processos trabalhistas e cíveis</strong> aplicando mapeamento patrimonial avançado (IDPJ). Localização estratégica de ativos com foco em desfecho cirúrgico de inadimplência em processos crônicos.
                            </div>
                            <div class="image-card__action" style="color: var(--accent-blue);">
                                Iniciar Recuperação <span style="font-size: 1.2rem;">&rarr;</span>
                            </div>
                        </div>
                    </a>

                    <!-- Área 2: Assessoria de Empresas -->
                    <a href="pages/assessoria-empresas.html" class="image-card">
                        <div class="image-card__img" style="background-image: url('https://images.unsplash.com/photo-1497366216548-37526070297c?q=80&w=800&auto=format&fit=crop');">
                            <div class="image-card__icon" style="color: var(--accent-purple); border: 1px solid rgba(139,92,246,0.5);">AE</div>
                        </div>
                        <div class="image-card__content">
                            <h3 class="image-card__title">Assessoria de Empresas</h3>
                            <div class="image-card__desc">
                                Escudo legal projetado para <strong>empresas de médio e pequeno porte</strong>. Blindagem corporativa, defesas trabalhistas e auditoria focada na perpetuidade e blindagem do seu negócio.
                            </div>
                            <div class="image-card__action" style="color: var(--accent-purple);">
                                Proteger Perímetro <span style="font-size: 1.2rem;">&rarr;</span>
                            </div>
                        </div>
                    </a>

                    <!-- Área 3: Prisões e Defesa Criminal -->
                    <a href="pages/prisoes.html" class="image-card">
                        <div class="image-card__img" style="background-image: url('https://images.unsplash.com/photo-1589391886645-d51941baf7fb?q=80&w=800&auto=format&fit=crop'); filter: grayscale(30%) contrast(120%);">
                            <div class="image-card__icon" style="color: var(--accent-gold); border: 1px solid rgba(199,168,107,0.5);">DC</div>
                        </div>
                        <div class="image-card__content">
                            <h3 class="image-card__title">Defesa Criminal de Urgência</h3>
                            <div class="image-card__desc">
                                Intervenção de contingência <strong>24/7 em delegacias e audiências de custódia</strong>. Arquitetura probatória rigorosa garantindo a integridade dos direitos fundamentais do assistido.
                            </div>
                            <div class="image-card__action" style="color: var(--accent-gold);">
                                Plantão de Defesa <span style="font-size: 1.2rem;">&rarr;</span>
                            </div>
                        </div>
                    </a>

                    <!-- Área 4: Direito da Saúde -->
                    <a href="pages/direito-saude.html" class="image-card">
                        <div class="image-card__img" style="background-image: url('https://images.unsplash.com/photo-1576091160550-2173dba999ef?q=80&w=800&auto=format&fit=crop');">
                            <div class="image-card__icon" style="color: var(--accent-green); border: 1px solid rgba(16,185,129,0.5);">DS</div>
                        </div>
                        <div class="image-card__content">
                            <h3 class="image-card__title">Jurisprudência de Saúde</h3>
                            <div class="image-card__desc">
                                Contencioso de alto risco contra convênios médicos, tutelas antecipadas para liberação de tratamentos urgentes (Oncologia/TEA), além de mediação de erro médico.
                            </div>
                            <div class="image-card__action" style="color: var(--accent-green);">
                                Acionar Urgência <span style="font-size: 1.2rem;">&rarr;</span>
                            </div>
                        </div>
                    </a>

                </div>
'@

$html = $html -replace '(?s)<div class="grid grid--2">.*?</div>\s*</div>\s*</section>', ("$newGrid
            </div>
        </section>")
Set-Content index.html -Value $html -Encoding UTF8
