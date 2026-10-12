import json,re,subprocess,pathlib
p = pathlib.Path.home()/'Orca-P-Mac/p1/work/techsite/site/state/jev-skip-tech.json'
raw = p.read_text()
d = json.loads(raw)
want = {
 "site":"tech", "slug":"ai-10min-persistence-rct-2026", "date":"2026-10-12-pm",
 "jev":"picked 2 (useful 0.56, 6후보) — UC 버클리·CMU 'AI 10분 인내력' RCT (HN 71표)",
 "consecutive_skip":0,
 "gate":"first_pass_review PASS — push 허용 (1차 검수 게이트 재확인 2회 PASS)",
 "similarity":"원문(버클리 보도자료·arXiv 2604.04721·프로젝트 페이지) 대비 8연속 단어 일치 0 — ops/hz_verify/2026-10-12-ai10min/simcheck2.py",
 "humanize":"light 윤문 19치환(변경률 7.0%)·수치·URL 전수 대조 PASS(누락 0)",
 "body_chars":"3,794자(공백 제외·main 전체)",
 "facts_verified":"N=354/667/201·풀이율 0.57vs0.73·스킵 0.20vs0.11·실험2 0.71vs0.77·실험3 0.76vs0.89·61% 답직접 유형·Cohen's d·p값 — arXiv 전문과 프로젝트 페이지에서 직접 확인. HN 71표는 스레드 실측. COLM 발표·10/9 버클리 발표는 보도자료 확인",
 "commit":"494c188 (origin main + brand main) — 라이브 포스트 200·홈 카드 1건·sitemap 함유·히어로 SVG 200 실측",
 "type":"이슈 해설 (ops/notes/tech-type-history.txt 갱신)",
}
for k,v in want.items():
    if d.get(k)!=v: print('DIFF',k,'->',repr(d.get(k))[:90])
missing=[k for k in want if k not in d]
print('missing keys:',missing)
print('1,222 in facts:', '1,222' in d.get('facts_verified',''))
