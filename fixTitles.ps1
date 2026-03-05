$html = Get-Content index.html -Raw -Encoding UTF8

$html = $html -replace '<h3 class="image-card__title">Jurisprudência de Saúde</h3>', '<h3 class="image-card__title">Direito da Saúde</h3>'

$html = $html -replace '<!-- Área 7: Direito do Consumidor e Bancário -->', '<!-- Área 7: Direito do Consumidor -->'

$html = $html -replace '<h3 class="image-card__title">Defesa do Consumidor e Bancário</h3>', '<h3 class="image-card__title">Defesa do Consumidor</h3>'

$html = $html -replace 'Combate judicial a juros bancários abusivos, suspensão de', 'Combate judicial a práticas abusivas, suspensão de'

Set-Content index.html -Value $html -Encoding UTF8
