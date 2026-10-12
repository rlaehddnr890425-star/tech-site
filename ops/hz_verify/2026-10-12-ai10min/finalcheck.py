import re, pathlib
p = pathlib.Path.home()/'Orca-P-Mac/p1/work/techsite/site/posts/ai-10min-persistence-rct-2026.html'
t = p.read_text()
b = (p.parent.parent/'ops/hz_verify/2026-10-12-ai10min/working.html').read_text()
p.write_text(b)
# forbidden patterns
for pat in ['조문','원문 대조','출처:','마지막 검증','고시 제','검증 시각','작성자:','lead.n.uk','http://localhost','placeholder','PLACEHOLDER','공식 발표','공식 발표']:
    hits = [m for m in re.findall(r'.{16}'+re.escape(pat)+r'.{16}', b)]
    if hits: print('FORBIDDEN', pat, hits)
# internal links exist
for m in re.findall(r'href="\./([a-z0-9-]+\.html)"', b):
    print('link', m, (p.parent/m).exists())
# hero img path
print('hero', (p.parent.parent/'assets/ai-10min-persistence-rct-2026.svg').exists())
print('chars', len(re.sub(r'\s','',re.sub(r'<[^>]+>',' ',re.search(r'<main>.*</main>',b,re.S).group(0)))))
