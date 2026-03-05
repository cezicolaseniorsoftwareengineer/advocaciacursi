import os
import re
import random

urls = [
    'https://images.unsplash.com/photo-1497366216548-37526070297c?q=80&w=800&auto=format&fit=crop',
    'https://images.unsplash.com/photo-1505373877841-8d25f7d46678?q=80&w=800&auto=format&fit=crop',
    'https://images.unsplash.com/photo-1505664194779-8beaceb93744?q=80&w=800&auto=format&fit=crop',
    'https://images.unsplash.com/photo-1521791136064-7986c2920216?q=80&w=800&auto=format&fit=crop',
    'https://images.unsplash.com/photo-1554224155-6726b3ff858f?q=80&w=800&auto=format&fit=crop',
    'https://images.unsplash.com/photo-1554224155-8d04cb21cd6c?q=80&w=800&auto=format&fit=crop',
    'https://images.unsplash.com/photo-1576091160550-2173dba999ef?q=80&w=800&auto=format&fit=crop',
    'https://images.unsplash.com/photo-1589391886645-d51941baf7fb?q=80&w=800&auto=format&fit=crop',
    'https://images.unsplash.com/photo-1600880292203-757bb62b4baf?q=80&w=800&auto=format&fit=crop',
    'https://images.unsplash.com/photo-1556761175-5973dc0f32d7?q=80&w=800&auto=format&fit=crop',
    'https://images.unsplash.com/photo-1573164713988-8665fc963095?q=80&w=800&auto=format&fit=crop',
    'https://images.unsplash.com/photo-1454165804606-c3d57bc86b40?q=80&w=800&auto=format&fit=crop',
    'https://images.unsplash.com/photo-1526628953301-3e589a6a8b74?q=80&w=800&auto=format&fit=crop',
    'https://images.unsplash.com/photo-1628151016629-9e8cbb0c5d79?q=80&w=800&auto=format&fit=crop'
]

# regex strategy: match everything between <div class="card"> and its matching closing </div>
# Actually, iterating through lines is safer if regex is tricky with nested tags.
# In these pages, the <div class="card"> typically contains an h4, a ul, and lis.
import glob
for filepath in glob.glob('pages/*.html'):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Let's fix grid--2 gap on these grids to match the new image card size
    content = content.replace('<div class="grid grid--2">', '<div class="grid grid--2" style="gap: 2.5rem;">')

    def replace_card(match):
        inner_content = match.group(1) # inside <div class="card">
        # Extract title
        title_match = re.search(r'<h4 class="card__title">(.*?)</h4>', inner_content, re.DOTALL)
        if not title_match:
             return match.group(0) # fail safe
        
        title = title_match.group(1)
        # Everything else goes into desc
        desc = inner_content.replace(title_match.group(0), '')
        
        img_url = random.choice(urls)
        
        return f'''<div class="image-card">
                        <div class="image-card__img" style="background-image: url('{img_url}');"></div>
                        <div class="image-card__content">
                            <h4 class="image-card__title" style="margin-top:0;">{title}</h4>
                            <div class="image-card__desc">
                                {desc.strip()}
                            </div>
                        </div>
                    </div>'''

    new_content = re.sub(r'<div class="card">\s*(.*?)\s*</div>\s*(<!--|<div|<\/div>|\Z)', lambda m: replace_card(m) + m.group(2), content, flags=re.DOTALL)
    
    # If the sub page is one of the ones that already had image-cards, we skip or it won't match anyway.
    if new_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f'Refatorado: {filepath}')

