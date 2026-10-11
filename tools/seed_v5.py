import json, io, contextlib, datetime as dt, collections, os
os.environ['OUT'] = '/dev/null'; os.environ['WD'] = '3.75'; os.environ['P1'] = '10-28'
with contextlib.redirect_stdout(io.StringIO()):
    exec(open('plan_v4.py').read())          # T, SUB, SHORT, TOP, DONE_TODAY, DROP
P = json.load(open('plan_v5.json'))
WAVE = P['wave']; BST = {k: dt.date.fromisoformat(v) for k, v in P['bstart'].items()}; BLEN = P['blen']
BEND = dt.date.fromisoformat(P['block_end'])
pref = {'G27': 'ACE GATE-27 ', 'H27': 'MADE EASY GATE-27 ', 'H26': 'MADE EASY GATE-26 ', 'A27': 'ACE ESE-27 ', 'M27': 'MADE EASY ESE-27 ', 'M26': 'MADE EASY ESE-26 '}
def lab(t):
    s = T[t]['label'].replace(pref[t[:3]], '')
    return s.replace('Full Syllabus', 'FS').replace(', Technical', '').replace(', GS', '').replace(' (new syllabus)', '').replace('Test-', 'Test ')
def kind(t):
    L = T[t]['label']
    if 'FLT' in t or '-K' in t or (t[:3] == 'A27' and '-M' in t) or '-F' in t: return 'mock'
    if 'ADD' in t: return 'add'
    if 'multi' in L: return 'multi'
    if 'grand' in L or 'single' in L: return 'grand'
    return 'subject'
cycle = ['SOM + Engg Mech; GS: Ethics', 'SA + Maths; GS: Aptitude', 'RCC + Steel; GS: Energy & Env', 'Geotech; GS: ICT', 'FM + Hydraulics; GS: Standards',
         'Hydrology + Irrigation; GS: Design & Safety', 'Environmental; GS: Material Science', 'Transportation; GS: Project Mgmt', 'Surveying + BM + CPM; GS: Current Issues']
days_l = []
for o in P['days']:
    ts = sorted(o['tests'], key=lambda t: (t not in DONE_TODAY, 0 if T[t]['hrs'] >= 2 else 1, WAVE.get(t, 6), t))
    days_l.append(dict(date=o['date'], cap=o['cap'], tests=ts))
rev = {}; ci = 0
for o in days_l:
    d = dt.date.fromisoformat(o['date']); ts = o['tests']
    blk = next((k for k in BST if BST[k] <= d < BST[k] + dt.timedelta(BLEN[k])), None)
    parts = []
    if blk:
        i = (d - BST[blk]).days + 1; L = BLEN[blk]
        if i == 1: parts.append(f'**Revise (day 1 of {L}) — {TOP[blk]}**')
        elif i < L: parts.append(f'**Revise (day {i} of {L}) — {SHORT[blk]}**: next set of topics, then PYQs')
        else: parts.append(f'**Revise (day {L} of {L}) — {SHORT[blk]}**: finish the topics, make the formula sheet')
    tech, gs = [], []
    for t in ts:
        if t in DONE_TODAY: continue
        for s in SUB(t):
            if s.startswith('GS:'):
                if s[3:] not in gs: gs.append(s[3:])
            elif s != blk and s not in tech: tech.append(s)
    if tech: parts.append('Refresh: ' + ', '.join(SHORT[s] for s in tech))
    if gs: parts.append('GS: ' + ', '.join(gs))
    if d > BEND: parts.append('Rotation: ' + cycle[ci % 9]); ci += 1
    if any(T[t]['hrs'] >= 2 for t in ts if t not in DONE_TODAY): parts.append('Mock prep: skim your formula sheets')
    rev[o['date']] = '. '.join(parts)
tests = []; order = 0
for o in days_l:
    for t in o['tests']:
        order += 1; sj = SUB(t)
        tests.append(dict(id=t, s=t[:3], n=lab(t), h=T[t]['hrs'], act=T[t]['act'].isoformat(), d=o['date'], o=order, k=kind(t),
                          sub=[SHORT[s] for s in sj if not s.startswith('GS:')], gs=[s[3:] for s in sj if s.startswith('GS:')]))
t = 'A27-M6a'; tests.append(dict(id=t, s='A27', n=lab(t), h=2.0, act='2026-12-15', d='2026-12-16', o=order + 1, k='mock', sub=[], gs=[]))
prev = {}
for f in ('seed_v2_backup.js', 'seed_v3_backup.js', 'seed_v4_backup.js'):
    old = open(f).read()
    for x in json.loads(old[old.index('=') + 1:].rstrip(';'))['tests']:
        if x['s'] not in DROP and x['d'] not in prev.setdefault(x['id'], []): prev[x['id']].append(x['d'])
BLK = {t: k for k, a_, b_, c_ in blocks for t in a_ + b_ + c_}
waves = {k: {} for k in BST}
for x in tests:
    w = WAVE.get(x['id'])
    if w in (1, 2, 3, 4):
        k = BLK[x['id']]
        waves[k].setdefault(w, []).append(x['d'])
wmap = [dict(sub=SHORT[k], rev=[BST[k].isoformat(), (BST[k] + dt.timedelta(BLEN[k] - 1)).isoformat()],
             w={w: [min(v), max(v)] for w, v in sorted(waves[k].items())}) for k in BST]
seed = dict(version=5, start='2026-10-11', end='2026-12-16', tests=tests, rev=rev, caps={o['date']: o['cap'] for o in days_l}, prev=prev)
open('/home/claude/examapp/web/seed.js', 'w').write('window.SEED=' + json.dumps(seed, ensure_ascii=False, separators=(',', ':')) + ';')
json.dump(dict(rev=rev, days=days_l, wmap=wmap), open('plan_v5_rev.json', 'w'), indent=1)
print(len(tests), round(sum(x['h'] for x in tests), 1))
for d in ('2026-10-11', '2026-10-12', '2026-10-17', '2026-11-20'): print(d, rev[d])
for w in wmap: print(w)
