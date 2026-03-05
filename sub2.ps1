$html = Get-Content pages/assessoria-empresas.html -Raw -Encoding UTF8

$newHTML = @'
<h3 class="text-center mb-3">Serviços Empresariais</h3>

<div class="grid grid--2" style="gap: 2.5rem;">
    <!-- 1 -->
    <div class="image-card">
        <div class="image-card__img" style="background-image: url('https://images.unsplash.com/photo-1556761175-5973dc0f32d7?q=80&w=800&auto=format&fit=crop');"></div>
        <div class="image-card__content">
            <h4 class="image-card__title">Contratos e Negociação</h4>
            <div class="image-card__desc">
                <ul style="color: var(--text-secondary); line-height: 1.8; margin-left: var(--spacing-md); padding: 0;">
                    <li>Elaboração e revisão de contratos</li>
                    <li>Contratos comerciais e prestação de serviços</li>
                    <li>Acordos de confidencialidade (NDA)</li>
                    <li>Contratos de parceria e joint ventures</li>
                    <li>Negociação com fornecedores e clientes</li>
                </ul>
            </div>
        </div>
    </div>
    <!-- 2 -->
    <div class="image-card">
        <div class="image-card__img" style="background-image: url('https://images.unsplash.com/photo-1573164713988-8665fc963095?q=80&w=800&auto=format&fit=crop');"></div>
        <div class="image-card__content">
            <h4 class="image-card__title">Direito Trabalhista Empresarial</h4>
            <div class="image-card__desc">
                <ul style="color: var(--text-secondary); line-height: 1.8; margin-left: var(--spacing-md); padding: 0;">
                    <li>Consultoria em relações de trabalho</li>
                    <li>Defesa em ações trabalhistas</li>
                    <li>Políticas internas e compliance</li>
                    <li>Rescisões e acordos trabalhistas</li>
                    <li>Adequação às normas da CLT</li>
                </ul>
            </div>
        </div>
    </div>
    <!-- 3 -->
    <div class="image-card">
        <div class="image-card__img" style="background-image: url('https://images.unsplash.com/photo-1554224155-8d04cb21cd6c?q=80&w=800&auto=format&fit=crop');"></div>
        <div class="image-card__content">
            <h4 class="image-card__title">Recuperação de Créditos</h4>
            <div class="image-card__desc">
                <ul style="color: var(--text-secondary); line-height: 1.8; margin-left: var(--spacing-md); padding: 0;">
                    <li>Cobrança extrajudicial</li>
                    <li>Ações de cobrança judicial</li>
                    <li>Execução de títulos de crédito</li>
                    <li>Protesto de dívidas</li>
                    <li>Negociação de débitos empresariais</li>
                </ul>
            </div>
        </div>
    </div>
    <!-- 4 -->
    <div class="image-card">
        <div class="image-card__img" style="background-image: url('https://images.unsplash.com/photo-1454165804606-c3d57bc86b40?q=80&w=800&auto=format&fit=crop');"></div>
        <div class="image-card__content">
            <h4 class="image-card__title">Regularização e Compliance</h4>
            <div class="image-card__desc">
                <ul style="color: var(--text-secondary); line-height: 1.8; margin-left: var(--spacing-md); padding: 0;">
                    <li>Adequação à LGPD</li>
                    <li>Regularização fiscal e tributária</li>
                    <li>Compliance empresarial</li>
                    <li>Políticas de governança</li>
                    <li>Auditorias jurídicas preventivas</li>
                </ul>
            </div>
        </div>
    </div>
</div>
'@

$html = $html -replace '(?s)<h3 class="text-center mb-3">Serviços Empresariais</h3>.*?<div class="card mt-4">', ("$newHTML

                <div class="card mt-4">")
Set-Content pages/assessoria-empresas.html -Value $html -Encoding UTF8
