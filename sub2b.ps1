$html = Get-Content pages/assessoria-empresas.html -Raw -Encoding UTF8
$startIndex = $html.IndexOf('<h3 class="text-center mb-3">Serviços Empresariais</h3>')
$endIndex = $html.IndexOf('<div class="card mt-4">', $startIndex)
if ($startIndex -ge 0 -and $endIndex -gt $startIndex) {
    $substring = $html.Substring($startIndex, $endIndex - $startIndex)
    $html = $html.Replace($substring, "$newHTML

                  ")
    Set-Content pages/assessoria-empresas.html -Value $html -Encoding UTF8
    "Replaced Assessoria!"
} else { "Not found Assessoria" }
