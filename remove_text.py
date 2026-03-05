import os
import re

files_to_edit = [
    'index.html',
    'pages/assessoria-empresas.html',
    'pages/direito-saude.html',
    'pages/execucao-civel-trabalhista.html',
    'pages/prisoes.html'
]

pattern = re.compile(
    r'<div\s+style="display:\s*flex;\s*flex-direction:\s*column;\s*align-items:\s*center;">\s*' +
    r'<span\s+style="font-size:\s*1\.1rem;\s*color:\s*var\(--accent-gold\);">Dr\. Estevão Cursi</span>\s*' +
    r'<span\s*' +
    r'style="font-size:\s*0\.85rem;\s*color:\s*var\(--accent-gold\);\s*font-weight:\s*500;\s*font-family:\s*var\(--font-primary\);\s*letter-spacing:\s*0\.5px;">OAB\s*' +
    r'378065</span>\s*' +
    r'</div>', re.DOTALL | re.IGNORECASE)

for fp in files_to_edit:
    if not os.path.exists(fp): continue
    with open(fp, 'r', encoding='utf-8') as f:
        content = f.read()
    
    new_content = pattern.sub('', content)
    
    with open(fp, 'w', encoding='utf-8') as f:
        f.write(new_content)
