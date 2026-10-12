import re, pathlib, subprocess
site = pathlib.Path.home()/'Orca-P-Mac/p1/work/techsite/site'
post = (site/'posts/ai-10min-persistence-rct-2026.html').read_text()
idx  = (site/'index.html').read_text()
sm   = (site/'sitemap.xml').read_text()
print('post-canonical:', 'https://tech.hub77a.com/posts/ai-10min-persistence-rct-2026.html' in post)
print('style.css:', '../style.css?v=' in post)
print('index-entry:', idx.count('posts/ai-10min-persistence-rct-2026.html'))
print('sitemap-entry:', sm.count('ai-10min-persistence-rct-2026.html'))
print('hero-file:', (site/'assets/ai-10min-persistence-rct-2026.svg').stat().st_size)
# 8-consecutive-word check against the source material sentences (english original + berkeley prose)
src_en = """using ai for just 10 minutes erodes your ability to persist at hard things
ai assistance improves immediate performance but it comes at a heavy cognitive cost
people perform significantly worse without ai and are more likely to give up
the rapid rise of ai chatbots promises immediate and effective help
overreliance on ai for answers erodes our cognitive fitness
removes what the team called productive struggle
using ai for hints or clarifications did not produce significant impairments
the reference point for how long a task should take can shift
"""
body = re.search(r'<main>.*</main>', post, re.S).group(0)
txt = re.sub(r'\s+',' ', re.sub(r'<[^>]+>',' ', body)).lower()
bad=0
for line in src_en.strip().split('\n'):
    w = line.split()
    for i in range(0, max(1,len(w)-7)):
        chunk = ' '.join(w[i:i+8])
        if chunk in txt:
            print('8WORD HIT:', chunk); bad+=1
print('8word hits:', bad)
