import os
import re

files_to_edit = [
    'index.html',
    'pages/assessoria-empresas.html',
    'pages/direito-saude.html',
    'pages/execucao-civel-trabalhista.html',
    'pages/prisoes.html'
]

for fp in files_to_edit:
    if not os.path.exists(fp): continue
    with open(fp, 'r', encoding='utf-8') as f:
        content = f.read()

    # Remove flex-direction from nav__logo
    content = re.sub(
        r'<a href="(.*?)" class="nav__logo" style="flex-direction:\s*column;\s*text-align:\s*center;\s*gap:\s*0\.2rem;"',
        r'<a href="\1" class="nav__logo"',
        content
    )
    
    # Remove margin from img
    content = re.sub(
        r'<img src="(.*?)" alt="Logo Dr\. Estevão Cursi" style="margin-bottom:\s*0\.2rem;">',
        r'<img src="\1" alt="Logo Dr. Estevão Cursi">',
        content
    )
    
    with open(fp, 'w', encoding='utf-8') as f:
        f.write(content)
