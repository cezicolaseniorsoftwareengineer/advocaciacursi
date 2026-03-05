$html = Get-Content pages/execucao-civel-trabalhista.html -Raw -Encoding UTF8

$newGrid = @'
<div class="grid grid--2" style="gap: 2.5rem;">
    <!-- 1 -->
    <div class="image-card">
        <div class="image-card__img" style="background-image: url('https://images.unsplash.com/photo-1521791136064-7986c2920216?q=80&w=800&auto=format&fit=crop');"></div>
        <div class="image-card__content">
            <h4 class="image-card__title">Execução Trabalhista</h4>
            <div class="image-card__desc">
                <ul style="color: var(--text-secondary); line-height: 1.8; margin-left: var(--spacing-md); padding: 0;">
                    <li>Recuperação de créditos trabalhistas</li>
                    <li>Penhora de bens e valores</li>
                    <li>Análise patrimonial de devedores</li>
                    <li>Negociação de acordos</li>
                    <li>Acompanhamento via IDPJ</li>
                </ul>
            </div>
        </div>
    </div>
    <!-- 2 -->
    <div class="image-card">
        <div class="image-card__img" style="background-image: url('https://images.unsplash.com/photo-1589829085413-56de8ae18c73?q=80&w=800&auto=format&fit=crop');"></div>
        <div class="image-card__content">
            <h4 class="image-card__title">Execução Cível</h4>
            <div class="image-card__desc">
                <ul style="color: var(--text-secondary); line-height: 1.8; margin-left: var(--spacing-md); padding: 0;">
                    <li>Execução de títulos executivos</li>
                    <li>Busca e apreensão de bens</li>
                    <li>Bloqueio judicial de ativos</li>
                    <li>Defesa em execuções</li>
                    <li>Estratégias de recuperação</li>
                </ul>
            </div>
        </div>
    </div>
    <!-- 3 -->
    <div class="image-card">
        <div class="image-card__img" style="background-image: url('https://images.unsplash.com/photo-1580582932707-520aed937b7b?q=80&w=800&auto=format&fit=crop');"></div>
        <div class="image-card__content">
            <h4 class="image-card__title">Casos Difíceis</h4>
            <div class="image-card__desc">
                <ul style="color: var(--text-secondary); line-height: 1.8; margin-left: var(--spacing-md); padding: 0;">
                    <li>Avaliação técnica de casos complexos</li>
                    <li>Devedores em recuperação judicial</li>
                    <li>Patrimônio oculto ou fraudado</li>
                    <li>Execuções antigas</li>
                    <li>Soluções criativas e legais</li>
                </ul>
            </div>
        </div>
    </div>
    <!-- 4 -->
    <div class="image-card">
        <div class="image-card__img" style="background-image: url('https://images.unsplash.com/photo-1451187580459-43490279c0fa?q=80&w=800&auto=format&fit=crop');"></div>
        <div class="image-card__content">
            <h4 class="image-card__title">Tecnologia IDPJ</h4>
            <div class="image-card__desc">
                <ul style="color: var(--text-secondary); line-height: 1.8; margin-left: var(--spacing-md); padding: 0;">
                    <li>Intimações digitais automáticas</li>
                    <li>Monitoramento processual 24/7</li>
                    <li>Redução de prazos processuais</li>
                    <li>Maior controle e transparência</li>
                    <li>Eficiência e agilidade comprovadas</li>
                </ul>
            </div>
        </div>
    </div>
</div>
'@

$html = $html -replace '(?s)<div class="grid grid--2">.*?</div>\s*</div>\s*<div class="card mt-4"', ("$newGrid
                <div class="card mt-4"")
Set-Content pages/execucao-civel-trabalhista.html -Value $html -Encoding UTF8
