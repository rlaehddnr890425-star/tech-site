import re, sys, pathlib, difflib, html

HZ = pathlib.Path.home() / '.hermes/profiles/1p/skills/humanize-korean/references'
sys.path.insert(0, str(HZ))

base = pathlib.Path('/Users/rlaehddnr425/Orca-P-Mac/p1/work/techsite/site/ops/hz_verify/2026-10-12-passkeys-trap')
orig = (base / 'original.html').read_text(encoding='utf-8')
work = (base / 'working.html').read_text(encoding='utf-8')

def text_of(raw):
    body = re.search(r'<main>.*?</main>', raw, re.S).group(0)
    body = re.sub(r'<[^>]+>', ' ', body)
    return html.unescape(body)

otxt, wtxt = text_of(orig), text_of(work)

def toks(t):
    a = set(re.findall(r'\d[\d.,:]*', t))
    b = set(re.findall(r'https?://\S+?(?=["\s<])', t))
    c = set(re.findall(r'[A-Za-z][A-Za-z0-9_.:/-]{3,}', t))
    return a | b | c

def norm(x):
    return x.rstrip('.,;)')

missing = sorted(t for t in toks(otxt) if norm(t) not in {norm(x) for x in toks(wtxt)})
print('수치·고유명·URL 누락:', missing if missing else '없음')

try:
    import metrics_v2 as m
    print('change_rate =', round(m.change_rate(otxt, wtxt), 4))
except Exception as e:
    r = difflib.SequenceMatcher(None, otxt, wtxt).ratio()
    print('change_rate(difflib 기준) =', round(1 - r, 4))

src = open('/Users/rlaehddnr425/.hermes/profiles/1p/cache/scratch/passkey_body.txt', encoding='utf-8').read()
def words(t):
    return [w.lower() for w in re.findall(r"[A-Za-z0-9가-힣_.:%/'-]+", t)]
sw = '\u0001'.join(words(src))
dw = words(wtxt)
hits = 0
for i in range(0, len(dw) - 7):
    if '\u0001'.join(dw[i:i+8]) in sw:
        hits += 1
print('윤문본 8연속 일치 개수:', hits)

han = re.findall(r'[一-龥]+', work)
print('한자 혼입:', set(han) if han else '없음')
print('본문 글자수(공백 제외):', len(re.sub(r'\s', '', re.sub(r'<[^>]+>', '', re.search(r'<main>.*?</main>', work, re.S).group(0)))))
