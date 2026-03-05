#!/usr/bin/env python3
import re

with open('blog.html', 'r', encoding='utf-8') as f:
    raw = f.read()

lock_to_slug = {
    12: 'execucao-trabalhista-eficiente',
    13: 'evitar-passivos-trabalhistas',
    14: 'teletrabalho-home-office',
    15: 'recuperacao-credito-estrategias',
    16: 'protecao-patrimonial-holding-familiar',
    17: 'clausulas-abusivas-plano-saude',
    18: 'voo-cancelado-direitos',
    19: 'renegociacao-dividas-superendividamento',
    20: 'acao-indenizacao-danos-morais',
    21: 'usucapiao-judicial-extrajudicial',
    22: 'distrato-imobiliario',
    23: 'locacao-comercial-despejo',
    24: 'revisao-vida-toda-inss',
    25: 'bpc-loas',
    26: 'erro-medico-tratamento-indevido',
    27: 'medicamentos-alto-custo',
    28: 'inventario-extrajudicial',
    29: 'guarda-compartilhada-unilateral',
    30: 'exclusao-icms-pis-cofins',
    31: 'doacao-reserva-usufruto',
}

card_split_pattern = re.compile(r'(?=<div class="image-card")')
parts = card_split_pattern.split(raw)
updated_parts = []
updated_count = 0

for part in parts:
    lock_match = re.search(r'\?lock=(\d+)', part)
    if lock_match:
        lock_num = int(lock_match.group(1))
        slug = lock_to_slug.get(lock_num)
        if slug:
            new_href = f'pages/artigos/{slug}.html'
            def update_btn(m):
                original = m.group(0)
                updated = re.sub(r'href="[^"]*"', f'href="{new_href}"', original, count=1)
                updated = re.sub(r'>([^<]+)</a>', '>Abrir o Artigo Completo</a>', updated, count=1)
                return updated
            btn_pattern = re.compile(r'<a\s+href="[^"]*"\s+class="btn btn--primary"[^>]*>[\s\S]*?</a>', re.DOTALL)
            new_part, n = btn_pattern.subn(update_btn, part)
            if n > 0:
                part = new_part
                updated_count += n
                print(f'lock={lock_num} -> {slug}')
    updated_parts.append(part)

result = ''.join(updated_parts)
with open('blog.html', 'w', encoding='utf-8') as f:
    f.write(result)

print(f'Done. {updated_count} buttons updated.')
