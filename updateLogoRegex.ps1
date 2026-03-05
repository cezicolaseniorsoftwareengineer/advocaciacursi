$html = Get-Content index.html -Raw -Encoding UTF8

$newLogo = '<a href="index.html" class="nav__logo" style="flex-direction: column; text-align: center; gap: 0.2rem;" aria-label="Dr. Estevão Cursi - Página inicial">
                <img src="img.png" alt="Logo Dr. Estevão Cursi" style="margin-bottom: 0.2rem;">
                <div style="display: flex; flex-direction: column; align-items: center;">
                    <span style="font-size: 1.1rem; color: var(--accent-gold);">Dr. Estevão Cursi</span>
                    <span style="font-size: 0.85rem; color: var(--accent-gold); font-weight: 500; font-family: var(--font-primary); letter-spacing: 0.5px;">OAB 378065</span>
                </div>
            </a>'

$html = $html -replace '(?s)<a href="index\.html" class="nav__logo".*?</a>', $newLogo
Set-Content index.html -Value $html -Encoding UTF8

$newLogoSub = '<a href="../index.html" class="nav__logo" style="flex-direction: column; text-align: center; gap: 0.2rem;" aria-label="Dr. Estevão Cursi - Página inicial">
                <img src="../img.png" alt="Logo Dr. Estevão Cursi" style="margin-bottom: 0.2rem;">
                <div style="display: flex; flex-direction: column; align-items: center;">
                    <span style="font-size: 1.1rem; color: var(--accent-gold);">Dr. Estevão Cursi</span>
                    <span style="font-size: 0.85rem; color: var(--accent-gold); font-weight: 500; font-family: var(--font-primary); letter-spacing: 0.5px;">OAB 378065</span>
                </div>
            </a>'

foreach ($f in Get-ChildItem pages/*.html) {
    $subHtml = Get-Content $f -Raw -Encoding UTF8
    $subHtml = $subHtml -replace '(?s)<a href="\.\./index\.html" class="nav__logo".*?</a>', $newLogoSub
    Set-Content $f -Value $subHtml -Encoding UTF8
}
