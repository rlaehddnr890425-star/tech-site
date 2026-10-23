#!/usr/bin/env python3
"""테크한잔 다중 소스 수집기 (HN·GitHub·HuggingFace·Reddit·Lobsters) — 2026-09-22.
원칙: 원문 저장만. 요약/선별은 JEV 게이트와 크론이 따로 한다.
출력: ops/sources/latest.json  {ts, count, errors, items:[{src,id,title,url,points,createdAt,capturedAt}]}
실행: python3 ops/collect_sources.py  (테한 크론 런 직전 1회)
"""
import json, os, time, datetime as dt, urllib.request, xml.etree.ElementTree as ET

OUT = os.path.join(os.path.dirname(__file__), 'sources', 'latest.json')
UA = {'User-Agent': 'orca-1p-research/0.1 (contact: lead.n.uk)'}
NOW = int(time.time())

def get(url, timeout=20):
    req = urllib.request.Request(url, headers=UA)
    return urllib.request.urlopen(req, timeout=timeout).read().decode('utf-8', 'ignore')

def iso(ts):
    return time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime(ts))

def hn():
    d = json.loads(get('https://hn.algolia.com/api/v1/search_by_date?tags=story&numericFilters=points%3E50&hitsPerPage=40'))
    return [dict(src='hn', id=str(h['objectID']), title=h.get('title',''),
                 url=h.get('url') or f"https://news.ycombinator.com/item?id={h['objectID']}",
                 points=h.get('points',0), createdAt=h.get('created_at','')) for h in d['hits']]

def github():
    day = (dt.datetime.utcnow() - dt.timedelta(days=2)).strftime('%Y-%m-%d')
    d = json.loads(get(f'https://api.github.com/search/repositories?q=created:%3E{day}&sort=stars&per_page=25'))
    return [dict(src='github', id=str(r['id']), title=r['full_name'], url=r['html_url'],
                 points=r['stargazers_count'], createdAt=r['created_at'][:19]+'Z') for r in d.get('items', [])]

def huggingface():
    d = json.loads(get('https://huggingface.co/api/models?sort=createdAt&direction=-1&limit=60'))
    return [dict(src='huggingface', id=m['modelId'], url=f"https://huggingface.co/{m['modelId']}",
                 title=m['modelId'], points=m.get('downloads',0), createdAt=m.get('createdAt','')[:19]+'Z') for m in d]

def reddit(sub='LocalLLaMA'):
    raw = get(f'https://www.reddit.com/r/{sub}/hot.rss')
    root = ET.fromstring(raw)
    out = []
    for e in [x for x in root.iter('{http://www.w3.org/2005/Atom}entry')][:15]:
        t = e.find('{http://www.w3.org/2005/Atom}title')
        l = e.find('{http://www.w3.org/2005/Atom}link')
        pub = e.find('{http://www.w3.org/2005/Atom}published')
        href = l.get('href') if l is not None else ''
        out.append(dict(src='reddit:'+sub, id=(href or '')[-14:], title=(t.text if t is not None else '')[:160],
                        url=href, points=0, createdAt=(pub.text if pub is not None else '')[:19]))
    return out

def lobsters():
    root = ET.fromstring(get('https://lobste.rs/rss'))
    out = []
    for it in list(root.iter('item'))[:15]:
        t = it.find('title'); l = it.find('link'); pd = it.find('pubDate')
        out.append(dict(src='lobsters', id=(l.text if l is not None else '')[-12:], title=(t.text if t is not None else ''),
                        url=(l.text if l is not None else ''), points=0, createdAt=(pd.text if pd is not None else '')))
    return out

def main():
    items, errors = [], []
    for name, fn in [('hn', hn), ('github', github), ('huggingface', huggingface),
                     ('reddit', reddit), ('lobsters', lobsters)]:
        try:
            items += fn()
        except Exception as e:
            errors.append(f'{name}: {type(e).__name__} {str(e)[:60]}')   # 429 등 개별 실패는 계속 진행
    seen, uniq = set(), []
    for it in items:
        k = (it['src'], it['id'])
        if k not in seen:
            seen.add(k)
            it['capturedAt'] = iso(NOW)
            uniq.append(it)
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    json.dump(dict(ts=iso(NOW), count=len(uniq), errors=errors, items=uniq),
              open(OUT, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    by = {}
    for it in uniq: by[it['src']] = by.get(it['src'], 0) + 1
    print('수집:', by, '| errors:', errors or '없음', '->', OUT)

if __name__ == '__main__':
    main()
