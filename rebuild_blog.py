with open('temp_index.html', encoding='utf-16') as f:
    html = f.read()

blog_start = html.rfind('<!-- ============================================================\n       BLOG SECTION')
blog_end = html.find('</section>', blog_start) + len('</section>')
blog_chunk = html[blog_start:blog_end]

footer_str = '<!-- ============================================================\n       FOOTER'
footer_start = html.rfind(footer_str)
footer_end = html.find('</footer>', footer_start) + len('</footer>')
footer_chunk = html[footer_start:footer_end]

hero_pos = html.find('<!-- ============================================================\n       HERO SECTION')  # 7 spaces
header_chunk = html[:hero_pos]

replacements = [
    ('href="#areas"', 'href="index.html#areas"'),
    ('href="#sobre"', 'href="index.html#sobre"'),
    ('href="#contato"', 'href="index.html#contato"'),
    ('href="#blog"', 'href="blog.html"'),
]
for old, new in replacements:
    header_chunk = header_chunk.replace(old, new)

header_chunk = header_chunk.replace(
    '<title>Dr. Estev\u00e3o Cursi - Advocacia de Excel\u00eancia | Especialista em Direito</title>',
    '<title>Blog Jur\u00eddico | Dr. Estev\u00e3o Cursi - Advocacia</title>'
)

result = (header_chunk + '\n    <main id="main" style="padding-top: 180px;">\n'
    + blog_chunk + '\n    </main>\n\n    ' + footer_chunk
    + '\n\n    <!-- JavaScript -->\n    <script src="js/main.js"></script>\n\n</body>\n</html>')

with open('blog.html', 'w', encoding='utf-8') as f:
    f.write(result)

print('blog.html rebuilt OK')
print('blog_chunk length:', len(blog_chunk))
print('footer_chunk length:', len(footer_chunk))
