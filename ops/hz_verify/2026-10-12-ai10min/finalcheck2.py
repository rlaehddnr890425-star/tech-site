import re, pathlib, subprocess
site = pathlib.Path.home()/'Orca-P-Mac/p1/work/techsite/site'
post = (site/'posts/ai-10min-persistence-rct-2026.html').read_text()
idx  = (site/'index.html').read_text()
sm   = (site/'sitemap.xml').read_text()
print('post-canonical:', 'https://tech.hub77a.com/posts/ai-10min-persistence-rct-2026.html' in post)
print('style.css:', '../style.css?v=' in post)
print('index-entry:', idx.count('posts/ai-10min-persistence-rct-2026.html'))
print('sitemap-entry:', sm.count('ai-10min-persistence-rct-2026.html'))
hero = site/'assets/ai-10min-persistence-rct-2026.svg'
print('hero-file:', hero.stat().st_size, hero.read_text().startswith('<svg'))
body = re.search(r'<main>.*</main>', post, re.S).group(0)
txt  = re.sub(r'\s+',' ', re.sub(r'<[^>]+>',' ', body))
plain = txt
print('body-chars(no-space):', len(re.sub(r'\s','',plain)))
for pat in ['조문','원문 대조','출처:','마지막 검증','고시 제','검증 시각','작성자:','lead.n.uk','placeholder','공식']:
    if pat in plain: print('FORBIDDEN HIT:', pat, re.findall(r'.{14}'+re.escape(pat)+r'.{14}', plain))
for m in re.findall(r'href="\./([a-z0-9-]+\.html)"', post):
    print('innerlink', m, (site/'posts'/m).exists())
