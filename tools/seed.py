import json, re
src=open('table10.py').read()
exec(src[:src.index("seen=set()")])   # gives T, days, subj(), lab(), SHORT, pref
R=json.load(open('rows10.json'))
rev={r['date']:r['rev'] for ph in R for r in R[ph]}
SER={'G27':'ACE GATE-27','G26':'ACE GATE-26','A27':'ACE ESE-27','A26':'ACE ESE-26','M27':'MADE EASY ESE-27','M26':'MADE EASY ESE-26'}
def kind(t,h):
    if 'FLT' in t or (t[:3] in('A27','A26') and '-M' in t) or '-F' in t: return 'mock'
    if 'ADD' in t: return 'add'
    if 'multi' in T[t]['label']: return 'multi'
    if 'grand' in T[t]['label']: return 'grand'
    return 'subject'
tests=[]
order=0
for d in days:
    for t in d['tests']:
        order+=1
        sj=[s for s in subj(t)]
        tech=[SHORT[s] for s in sj if not s.startswith('GS:')]
        gs=[s[3:] for s in sj if s.startswith('GS:')]
        tests.append(dict(id=t, s=t[:3], n=lab(t), h=T[t]['hrs'], act=T[t]['act'], d=d['date'], o=order, k=kind(t,T[t]['hrs']), sub=tech, gs=gs))
# the one test outside the window
t='A27-M6a'; tests.append(dict(id=t,s='A27',n=lab(t),h=2.0,act='2026-12-15',d='2026-12-16',o=order+1,k='mock',sub=[],gs=[]))
caps={d['date']:d['cap'] for d in days}
seed=dict(version=1, start='2026-10-10', end='2026-12-16', series=SER, tests=tests,
          rev={k:v for k,v in rev.items()}, caps=caps)
open('/home/claude/examapp/web/seed.js','w').write('window.SEED='+json.dumps(seed,ensure_ascii=False,separators=(',',':'))+';')
print(len(tests), sum(x['h'] for x in tests))
import collections; print(collections.Counter(x['k'] for x in tests)); print(collections.Counter(x['s'] for x in tests))
print(tests[0]); print([x for x in tests if x['id']=='A27-M3'])
