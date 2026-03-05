$html = Get-Content index.html -Raw -Encoding UTF8
$html = $html -replace '<li><a href="#contato">Direito Tributário</a></li>', "<li><a href="#contato">Direito Tributário</a></li>
                            <li><a href="#contato">Direito Civil</a></li>"
Set-Content index.html -Value $html -Encoding UTF8

foreach ($f in Get-ChildItem pages/*.html) {
    $subHtml = Get-Content $f -Raw -Encoding UTF8
    $subHtml = $subHtml -replace '<li><a href="\.\./index\.html#contato">Direito Tributário</a></li>', "<li><a href="../index.html#contato">Direito Tributário</a></li>
      <li><a href="../index.html#contato">Direito Civil</a></li>"
    Set-Content $f -Value $subHtml -Encoding UTF8
}
