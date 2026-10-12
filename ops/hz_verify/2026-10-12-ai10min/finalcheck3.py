import re, pathlib, json
site = pathlib.Path.home()/'Orca-P-Mac/p1/work/techsite/site'
post = (site/'posts/ai-10min-persistence-rct-2026.html').read_text()
idx  = (site/'index.html').read_text()
sm   = (site/'sitemap.xml').read_text()
st   = json.loads((site/'state/jev-skip-tech.json').read_text())
hero = site/'assets/ai-10min-persistence-rct-2026.svg'
print('canonical:', 'https://tech.hub77a.com/posts/ai-10min-persistence-rct-2026.html' in post)
print('index:', idx.count('posts/ai-10min-persistence-rct-2026.html'), 'sitemap:', sm.count('ai-10min-persistence-rct-2026'))
print('hero bytes:', hero.stat().st_size)
body = re.search(r'<main>.*</main>', post, re.S).group(0)
print('body chars:', len(re.sub(r'\s','',re.sub(r'<[^>]+>',' ',body))))
print('state slug/date/skip:', st['slug'], st['date'], st['consecutive_skip'])
