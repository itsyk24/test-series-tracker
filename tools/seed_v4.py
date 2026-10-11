import json, io, contextlib, datetime as dt, re, collections
import os
os.environ.setdefault('WD', '3.75'); os.environ.setdefault('P1', '10-25'); os.environ['OUT'] = 'plan_v4.json'
src = open('plan_v4.py').read()
with contextlib.redirect_stdout(io.StringIO()):
    exec(src)
P = json.load(open('plan_v4.json'))
P1D = P1_END.isoformat()
days_l = P['days']
pref = {'G27':'ACE GATE-27 ','G26':'ACE GATE-26 ','H27':'MADE EASY GATE-27 ','H26':'MADE EASY GATE-26 ','A27':'ACE ESE-27 ','A26':'ACE ESE-26 ','M27':'MADE EASY ESE-27 ','M26':'MADE EASY ESE-26 '}
def lab(t):
    s = T[t]['label'].replace(pref[t[:3]], '')
    return s.replace('Full Syllabus', 'FS').replace(', Technical', '').replace(', GS', '').replace(' (new syllabus)', '').replace('Test-', 'Test ')
def kind(t):
    L = T[t]['label']
    if 'FLT' in t or '-K' in t or (t[:3] in ('A27','A26') and '-M' in t) or '-F' in t: return 'mock'
    if 'ADD' in t: return 'add'
    if 'multi' in L: return 'multi'
    if 'grand' in L or 'single' in L: return 'grand'
    return 'subject'
cycle = ['SOM + Engg Mech; GS: Ethics','SA + Maths; GS: Aptitude','RCC + Steel; GS: Energy & Env','Geotech; GS: ICT','FM + Hydraulics; GS: Standards',
         'Hydrology + Irrigation; GS: Design & Safety','Environmental; GS: Material Science','Transportation; GS: Project Mgmt','Surveying + BM + CPM; GS: Current Issues']
seen = set(); rev = {}; ci = 0
for o in days_l:
    d = o['date']; ts = o['tests']
    tech = []; gs = []; big = False
    for t in ts:
        if T[t]['hrs'] >= 2: big = True
        for s in SUB(t):
            if s.startswith('GS:'):
                if s[3:] not in gs: gs.append(s[3:])
            elif s not in tech: tech.append(s)
    parts = []; recap = []
    for s in tech:
        if s not in seen: parts.append(f'**New — {TOP[s]}**'); seen.add(s)
        else: recap.append(SHORT[s]); seen.add(s)
    if recap: parts.append('Recap: ' + ', '.join(recap))
    if gs: parts.append('GS: ' + ', '.join(gs))
    if not ts: parts.append('Buffer day: catch up on anything missed, else your 3 weakest topics from mock analysis')
    elif d > P1D: parts.append('Rotation: ' + cycle[ci % 9]); ci += 1
    elif big: parts.append("Mock prep: this week's formula sheets")
    rev[d] = '. '.join(parts)
tests = []; order = 0
for o in days_l:
    for t in o['tests']:
        order += 1
        sj = SUB(t)
        tests.append(dict(id=t, s=t[:3], n=lab(t), h=T[t]['hrs'], act=T[t]['act'].isoformat(), d=o['date'], o=order, k=kind(t),
                          sub=[SHORT[s] for s in sj if not s.startswith('GS:')], gs=[s[3:] for s in sj if s.startswith('GS:')]))
t = 'A27-M6a'; tests.append(dict(id=t, s='A27', n=lab(t), h=2.0, act='2026-12-15', d='2026-12-16', o=order + 1, k='mock', sub=[], gs=[]))
# previous (v2) planned dates for migration
v1 = {}
old = open('/home/claude/work/seed_v2_backup.js').read()
for x in json.loads(old[old.index('=') + 1:].rstrip(';'))['tests']:
    if x['s'] not in DROP: v1[x['id']] = x['d']
missing_in_v3 = [k for k in v1 if k not in {x['id'] for x in tests}]
print('v2 ids not in v3:', missing_in_v3)
seed = dict(version=3, start='2026-10-11', end='2026-12-16', tests=tests, rev=rev, caps={o['date']: o['cap'] for o in days_l}, prev=v1)
open('/home/claude/examapp/web/seed.js', 'w').write('window.SEED=' + json.dumps(seed, ensure_ascii=False, separators=(',', ':')) + ';')
json.dump(dict(rev=rev, days=days_l), open('plan_v4_rev.json', 'w'), indent=1)
print(len(tests), round(sum(x['h'] for x in tests), 1), collections.Counter(x['s'] for x in tests))
print('Oct11:', rev['2026-10-11'][:300]); print('Dec06:', rev['2026-12-06']); print('Nov20:', rev['2026-11-20'])
