$html = Get-Content index.html -Raw -Encoding UTF8

$oldLogo = '<a href="index.html" class="nav__logo" aria-label="Dr. Estevão Cursi - Página inicial">
                <img src="img.png" alt="Logo Dr. Estevão Cursi">
                <div style="display: flex; flex-direction: column;">
                    <span>Dr. Estevão Cursi</span>
                    <span
                        style="font-size: 0.8rem; color: var(--accent-gold); font-weight: 500; font-family: var(--font-primary); letter-spacing: 0.5px;">OAB
                        378065</span>
                </div>
            </a>'
            
$newLogo = '<a href="index.html" class="nav__logo" style="flex-direction: column; text-align: center; gap: 0.1rem;" aria-label="Dr. Estevão Cursi - Página inicial">
                <img src="img.png" alt="Logo Dr. Estevão Cursi" style="margin-bottom: 0.2rem;">
                <div style="display: flex; flex-direction: column; align-items: center;">
                    <span style="font-size: 1.1rem; color: var(--accent-gold);">Dr. Estevão Cursi</span>
                    <span style="font-size: 0.85rem; color: var(--accent-gold); font-weight: 500; font-family: var(--font-primary); letter-spacing: 0.5px;">OAB 378065</span>
                </div>
            </a>'

$html = $html.Replace($oldLogo, $newLogo)
Set-Content index.html -Value $html -Encoding UTF8
