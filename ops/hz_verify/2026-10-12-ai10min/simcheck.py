import re, sys, pathlib, difflib
sys.path.insert(0, str(pathlib.Path.home()/'.hermes/profiles/1p/skills/humanize-korean/references'))
import metrics_v2 as m

base = pathlib.Path.home()/'Orca-P-Mac/p1/work/techsite/site/ops/hz_verify/2026-10-12-ai10min'
src = (base/'original.html').read_text()
hz  = (base/'working.html').read_text()

def body(t):
    return re.search(r'<main>.*</main>', t, re.S).group(0)

def toks(t):
    b = body(t)
    nums = set(re.findall(r'[0-9][0-9.,]*', b))
    urls = set(re.findall(r'https?://[^\s"<>]+', b))
    return nums, urls

for tag, t in (('original', src), ('working', hz)):
    r = m.compute_all_v2(body(t), genre='blog')
    print(tag, 'risk =', r['risk_score'])

n1,u1 = toks(src); n2,u2 = toks(hz)
miss_n = [x for x in n1 if x not in n2]
miss_u = [x for x in u1 if x not in u2]
print('missing numbers:', miss_n)
print('missing urls:', miss_u)

a = re.sub(r'<[^>]+>','',body(src)); b = re.sub(r'<[^>]+>','',body(hz))
ratio = difflib.SequenceMatcher(None, a, b).ratio()
print('similarity ratio:', round(ratio,3), '(change rate', round((1-ratio)*100,1),'%)')

# 8-consecutive-word similarity vs source material phrases
src_phrases = [
 "using ai for just 10 minutes erodes your ability to persist",
 "ai assistance reduces persistence and hurts independent performance",
 "erodes our cognitive fitness",
 "productive struggle",
]
bl = re.sub(r'\s+',' ', re.sub(r'<[^>]+>',' ',body(hz))).lower()
for p in src_phrases:
    if p in bl: print('PHRASE HIT:', p)
print('done')
