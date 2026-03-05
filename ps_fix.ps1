$html = Get-Content index.html -Raw -Encoding UTF8
$old = "<li><a href="#contato">Direito Trabalhista</a></li>
                          <li><a href="#contato">Direito Tributário</a></li>"
$new = "<li><a href="#contato">Direito Trabalhista</a></li>
                          <li><a href="#contato">Direito Tributário</a></li>
                          <li><a href="#contato">Direito Civil</a></li>"
$html = $html.Replace($old, $new)
Set-Content index.html -Value $html -Encoding UTF8
