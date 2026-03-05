$html = Get-Content pages/prisoes.html -Raw -Encoding UTF8

$newGrid = @'
<div class="grid grid--2" style="gap: 2.5rem;">
    <!-- 1 -->
    <div class="image-card">
        <div class="image-card__img" style="background-image: url('https://images.unsplash.com/photo-1589391886645-d51941baf7fb?q=80&w=800&auto=format&fit=crop'); filter: grayscale(30%) contrast(120%);"></div>
        <div class="image-card__content">
            <h4 class="image-card__title">Atendimento em Delegacias</h4>
            <div class="image-card__desc">
                <ul style="color: var(--text-secondary); line-height: 1.8; margin-left: var(--spacing-md); padding: 0;">
                    <li><strong>Atendimento imediato 24h</strong></li>
                    <li>Acompanhamento em depoimentos</li>
                    <li>Orientação técnica desde a prisão</li>
                    <li>Proteção de direitos na fase policial</li>
                    <li>Pedidos de liberdade provisória</li>
                </ul>
            </div>
        </div>
    </div>
    <!-- 2 -->
    <div class="image-card">
        <div class="image-card__img" style="background-image: url('https://images.unsplash.com/photo-1628151016629-9e8cbb0c5d79?q=80&w=800&auto=format&fit=crop');"></div>
        <div class="image-card__content">
            <h4 class="image-card__title">Audiências de Custódia</h4>
            <div class="image-card__desc">
                <ul style="color: var(--text-secondary); line-height: 1.8; margin-left: var(--spacing-md); padding: 0;">
                    <li>Defesa especializada na audiência</li>
                    <li>Demonstração de ilegalidades da prisão</li>
                    <li>Requerimento de liberdade ou medidas cautelares</li>
                    <li>Preservação da integridade do detido</li>
                    <li>Contato constante com a família</li>
                </ul>
            </div>
        </div>
    </div>
    <!-- 3 -->
    <div class="image-card">
        <div class="image-card__img" style="background-image: url('https://images.unsplash.com/photo-1589829085413-56de8ae18c73?q=80&w=800&auto=format&fit=crop');"></div>
        <div class="image-card__content">
            <h4 class="image-card__title">Estratégia de Defesa</h4>
            <div class="image-card__desc">
                <ul style="color: var(--text-secondary); line-height: 1.8; margin-left: var(--spacing-md); padding: 0;">
                    <li>Análise detalhada do inquérito policial</li>
                    <li>Busca de provas favoráveis (assistência técnica)</li>
                    <li>Habeas Corpus em diferentes instâncias</li>
                    <li>Preparação para interrogatórios</li>
                    <li>Estratégias para absolvição ou redução de pena</li>
                </ul>
            </div>
        </div>
    </div>
    <!-- 4 -->
    <div class="image-card">
        <div class="image-card__img" style="background-image: url('https://images.unsplash.com/photo-1593115057322-e94b77572f20?q=80&w=800&auto=format&fit=crop');"></div>
        <div class="image-card__content">
            <h4 class="image-card__title">Defesa Judicial</h4>
            <div class="image-card__desc">
                <ul style="color: var(--text-secondary); line-height: 1.8; margin-left: var(--spacing-md); padding: 0;">
                    <li>Defesa em processos criminais em todas as varas</li>
                    <li>Tribunal do Júri</li>
                    <li>Recursos criminais (TJ, STJ, STF)</li>
                    <li>Execução penal (progressão de regime)</li>
                    <li>Sustentações orais</li>
                </ul>
            </div>
        </div>
    </div>
</div>
'@

$html = $html -replace '(?s)<div class="grid grid--2">.*?</div>\s*<div class="card mt-4"', ("$newGrid

                  <div class="card mt-4"")
Set-Content pages/prisoes.html -Value $html -Encoding UTF8
