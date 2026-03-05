$newFooterLinks = @'
<h4>Áreas de Atuação</h4>
<ul>
    <li><a href="pages/execucao-civel-trabalhista.html">Execução Cível e Trabalhista</a></li>
    <li><a href="pages/assessoria-empresas.html">Assessoria de Empresas</a></li>
    <li><a href="pages/prisoes.html">Prisões e Defesa Criminal</a></li>
    <li><a href="pages/direito-saude.html">Direito da Saúde</a></li>
    <li><a href="#contato">Família e Sucessões</a></li>
    <li><a href="#contato">Direito Imobiliário</a></li>
    <li><a href="#contato">Defesa do Consumidor</a></li>
    <li><a href="#contato">Direito Previdenciário</a></li>
    <li><a href="#contato">Direito Trabalhista</a></li>
    <li><a href="#contato">Direito Tributário</a></li>
</ul>
'@

$html = Get-Content index.html -Raw -Encoding UTF8
$html = $html -replace '(?s)<h4>Áreas de Atuação</h4>\s*<ul>.*?</ul>', $newFooterLinks
Set-Content index.html -Value $html -Encoding UTF8

$newSubFooterLinks = @'
<h4>Áreas de Atuação</h4>
<ul>
    <li><a href="execucao-civel-trabalhista.html">Execução Cível e Trabalhista</a></li>
    <li><a href="assessoria-empresas.html">Assessoria de Empresas</a></li>
    <li><a href="prisoes.html">Prisões e Defesa Criminal</a></li>
    <li><a href="direito-saude.html">Direito da Saúde</a></li>
    <li><a href="../index.html#contato">Família e Sucessões</a></li>
    <li><a href="../index.html#contato">Direito Imobiliário</a></li>
    <li><a href="../index.html#contato">Defesa do Consumidor</a></li>
    <li><a href="../index.html#contato">Direito Previdenciário</a></li>
    <li><a href="../index.html#contato">Direito Trabalhista</a></li>
    <li><a href="../index.html#contato">Direito Tributário</a></li>
</ul>
'@

foreach ($f in Get-ChildItem pages/*.html) {
    $subHtml = Get-Content $f -Raw -Encoding UTF8
    $subHtml = $subHtml -replace '(?s)<h4>Áreas de Atuação</h4>\s*<ul>.*?</ul>', $newSubFooterLinks
    Set-Content $f -Value $subHtml -Encoding UTF8
}
