"""Plan v4: 6 series (ACE GATE 27, MADE EASY GATE 27/26, ACE ESE 27, MADE EASY ESE 27/26).
Re-planned from Sun Oct 11; weekend 10 h, weekday quota from env WD. Done tests pinned to Oct 11."""
import datetime as dt, json, collections, sys, os
exec(open('catalogue.py').read())          # T, add(), D()
START = dt.date(2026, 10, 11); END = dt.date(2026, 12, 15)
WD, WE = float(os.environ.get('WD', '6.5')), 10.0
P1_END_ENV = os.environ.get('P1', '11-08')
cap = lambda d: WE if d.weekday() >= 5 else WD

# ---------- MADE EASY GATE 27 / 26 ----------
mg_topic = {1:'Solid Mechanics-1',2:'Solid Mechanics-2',3:'Concrete Structures-1',4:'Concrete Structures-2',5:'Environmental-1',6:'Environmental-2',
            7:'FM & Hydraulics-1',8:'FM & Hydraulics-2',9:'Engg Maths-1',10:'Engg Maths-2',11:'General Aptitude-1',12:'General Aptitude-2',
            13:'Transport & Geomatics-1',14:'Transport & Geomatics-2',15:'Structural Analysis-1',16:'Structural Analysis-2',17:'Geotech-1',18:'Geotech-2',
            19:'Geotech-3',20:'Steel Structures-1',21:'Steel Structures-2',22:'Hydrology',23:'Irrigation',24:'Engg Mech + Constr Materials & Mgmt'}
mg_topic_act = {**{k:'01-04-2026' for k in range(1,7)}, **{k:'10-04-2026' for k in range(7,13)}, **{k:'20-04-2026' for k in range(13,19)}, **{k:'30-04-2026' for k in range(19,25)}}
mg_single = {25:'Solid Mechanics',26:'Concrete Structures',27:'Environmental',28:'FM & Hydraulics',29:'Engg Maths',30:'General Aptitude',
             31:'Transport & Geomatics',32:'Structural Analysis',33:'Geotech',34:'Steel Structures',35:'Hydrology & Irrigation',36:'Engg Mech + Constr Materials & Mgmt'}
for k,v in mg_topic.items():
    add(f'H27-T{k:02d}', f'MADE EASY GATE-27 Test {k} {v}', 0.75, D(mg_topic_act[k]), 'ME GATE-27')
    add(f'H26-T{k:02d}', f'MADE EASY GATE-26 Test {k} {v}', 0.75, D('01-01-2026'), 'ME GATE-26', True)
for k,v in mg_single.items():
    add(f'H27-T{k}', f'MADE EASY GATE-27 Test {k} {v} (single)', 1.5, D('15-05-2026' if k <= 30 else '30-05-2026'), 'ME GATE-27')
    add(f'H26-T{k}', f'MADE EASY GATE-26 Test {k} {v} (single)', 1.5, D('01-01-2026'), 'ME GATE-26', True)
mg26_multi = {37:'SOM+SA+Engg Mech',38:'Geotech+Steel',39:'FM+RCC+CMM',40:'Env+Hydrology+Irrigation',41:'Transport+Geomatics',42:'Maths+GA'}
for k,v in mg26_multi.items():
    add(f'H26-T{k}', f'MADE EASY GATE-26 Test {k} {v} (multi)', 1.5, D('01-01-2026'), 'ME GATE-26', True)
for i,k in enumerate(range(37,45), start=1):
    add(f'H27-F{i}', f'MADE EASY GATE-27 Full Syllabus-{i} (T{k}, {"Basic" if i<=4 else "Advance"})', 3.0, D('15-06-2026' if i<=4 else '30-06-2026'), 'ME GATE-27')
for i,k in enumerate(range(45,49), start=1):
    add(f'H27-K{i}', f'MADE EASY GATE-27 Mock-{i} (T{k})', 3.0, D('30-07-2026'), 'ME GATE-27')
for i,k in enumerate(range(43,51), start=1):
    add(f'H26-F{i}', f'MADE EASY GATE-26 Full Syllabus-{i} (T{k}, {"Basic" if i<=4 else "Advance"})', 3.0, D('01-01-2026'), 'ME GATE-26', True)
for i,k in enumerate(range(51,55), start=1):
    add(f'H26-K{i}', f'MADE EASY GATE-26 Mock-{i} (T{k})', 3.0, D('01-01-2026'), 'ME GATE-26', True)

# split ESE practice pairs so they fit weekdays; A27 mocks stay whole (exam days)
def split(pid, p1, p2):
    b = T.pop(pid)
    add(pid+'a', p1, 2.0, b['act'], b['series'], b['practice']); add(pid+'b', p2, 3.0, b['act'], b['series'], b['practice'])
for k in range(1,5): split(f'A26-M{k}', f'ACE ESE-26 Mock-{k} P-I (T{21+2*k})', f'ACE ESE-26 Mock-{k} P-II (T{22+2*k})')
for k in (1,3,5,7): split(f'M27-F{k}', f'MADE EASY ESE-27 Full Syllabus-{k} (P-I, GS)', f'MADE EASY ESE-27 Full Syllabus-{k+1} (P-II, Technical)')
for k in (7,9,11): split(f'M26-F{k}', f'MADE EASY ESE-26 Full Syllabus-{k} (P-I, GS)', f'MADE EASY ESE-26 Full Syllabus-{k+1} (P-II, Technical)')
split('A27-M6', 'ACE ESE-27 Mock-6 P-I (T43)', 'ACE ESE-27 Mock-6 P-II (T44)')
for m in ('A27-M3','A27-M4','A27-M5'): T[m]['act'] = T[m]['act'] + dt.timedelta(1)   # opens 6 PM

DROP = ('G26', 'A26')
for k in [k for k in T if k[:3] in DROP]: del T[k]
keep = lambda L: [t for t in L if t[:3] not in DROP]
DONE_TODAY = ['G27-FLT1', 'G27-T22']   # finished on Sun Oct 11
# ---------- subjects for every test ----------
def SUB(tid):
    s, n = tid[:3], tid[4:]
    import re
    num = int(re.sub(r'\D','',n) or 0)
    if s in ('G27','G26'):
        k = num if s=='G27' or not (37<=num<=42) else num+6
        if n.startswith('T'):
            m = {1:'Maths',2:'Maths',3:'Geotech',4:'Geotech',5:'SA',6:'SA',7:'RCC',8:'Steel',9:'SOM',10:'SOM',11:'FM',12:'FM',13:'Hydro',14:'Hydro',15:'Env',16:'Env',17:'Transport',18:'Transport',19:'Survey',20:'SOM',21:'BM',22:'GA',23:'GA',24:'GA',
                 25:'Maths',26:'SOM',27:'Env',28:'SA',29:['RCC','Steel'],30:'Geotech',31:'Hydro',32:'FM',33:'Transport',34:'Survey',35:'BM',36:'GA',
                 43:['SOM','SA'],44:['Geotech','FM'],45:['BM','RCC','Steel'],46:['Hydro','Env'],47:['Transport','Survey'],48:['Maths','GA']}.get(k, [])
            return m if isinstance(m, list) else [m]
        return []
    if s in ('H27','H26') and n.startswith('T'):
        m = {1:'SOM',2:'SOM',3:'RCC',4:'RCC',5:'Env',6:'Env',7:'FM',8:'FM',9:'Maths',10:'Maths',11:'GA',12:'GA',13:['Transport','Survey'],14:['Transport','Survey'],
             15:'SA',16:'SA',17:'Geotech',18:'Geotech',19:'Geotech',20:'Steel',21:'Steel',22:'Hydro',23:'Hydro',24:['SOM','BM'],
             25:'SOM',26:'RCC',27:'Env',28:'FM',29:'Maths',30:'GA',31:['Transport','Survey'],32:'SA',33:'Geotech',34:'Steel',35:'Hydro',36:['SOM','BM'],
             37:['SOM','SA'],38:['Geotech','Steel'],39:['FM','RCC','BM'],40:['Env','Hydro'],41:['Transport','Survey'],42:['Maths','GA']}[num]
        return m if isinstance(m, list) else [m]
    if s in ('A27','A26') and n.startswith('T'):
        m = {1:'Transport',2:'SOM',3:'FM',4:'Maths',5:'Env',6:'GS:Energy & Environment',7:'SA',8:'GS:Design, Drawing & Safety',9:'Geotech',10:'GS:Ethics',11:'RCC',12:'GS:ICT',13:'Survey',14:'GS:Engg Aptitude',15:'Steel',16:'GS:Material Science',17:'Hydro',18:'GS:Standards & Quality',19:'BM',20:'GS:Project Mgmt',21:'BM',22:'GS:Current Issues',
             27:['FM','Survey'],28:['GS:Energy & Environment','GS:Engg Aptitude'],29:['SOM','BM','Hydro'],30:['Maths','GS:Current Issues'],31:['Steel','Transport','Geotech'],32:['GS:Project Mgmt','GS:Material Science'],33:['Env','SA'],34:['GS:ICT','GS:Design, Drawing & Safety'],35:['BM','RCC','Hydro'],36:['GS:Ethics','GS:Standards & Quality']}[num]
        return m if isinstance(m, list) else [m]
    if s in ('M27','M26') and n.startswith('S'):
        m = {1:'SOM',2:'GS:Engg Aptitude',3:'Env',4:'Maths',5:'SA',6:'GS:Design, Drawing & Safety',7:'Hydro',8:'GS:Energy & Environment',9:'RCC',10:'GS:Project Mgmt',11:'FM',12:'GS:Material Science',13:'Steel',14:'GS:ICT',15:'Geotech',16:'GS:Ethics',17:'BM',18:'GS:Standards & Quality',19:'Transport',20:'GS:Current Issues',21:'BM',22:'Survey'}[num]
        return [m]
    return []

SHORT = {'SOM':'SOM + EM','SA':'SA','RCC':'RCC','Steel':'Steel','Geotech':'Geotech','FM':'FM + Hydraulics','Hydro':'Hydrology + Irrigation','Env':'Env','Transport':'Transport','Survey':'Surveying','BM':'BM + CPM','Maths':'Maths','GA':'GATE aptitude'}
TOP = {'SOM':'SOM: stress–strain, Mohr circle, SFD/BMD, bending & shear stress, torsion, columns; EM: FBD, friction',
 'SA':'SA: indeterminacy, slope-deflection, moment distribution, ILD, energy methods, arches, cables',
 'RCC':'RCC: LSM/WSM, beams, slabs, columns, footings, bond; prestressed basics; masonry',
 'Steel':'Steel: tension/compression members, beams, beam-columns, plate girders, bases, connections, plastic analysis',
 'Geotech':'Geotech: phase relations, seepage, consolidation, shear strength, earth pressure, slopes, bearing capacity, piles',
 'FM':'FM: fluid statics, Bernoulli & momentum, pipe flow, boundary layer, open channel, pumps & turbines, hydropower',
 'Hydro':'Hydrology: hydrographs, flood routing, wells; Irrigation: duty-delta, canals, weirs, dams, spillways',
 'Env':'Env: water quality & treatment, distribution, sewage treatment, sludge, air pollution, solid waste',
 'Transport':'Transport: geometric design, IRC pavement design, traffic & signal design, railways, airports',
 'Survey':'Surveying: levelling, traversing, curves, total station/GNSS, photogrammetry & remote sensing; geology',
 'BM':'BM + CPM: cement, concrete & admixtures, steel, bricks, timber; estimation, PERT/CPM, equipment, contracts',
 'Maths':'Maths: linear algebra, calculus, ODE/PDE, probability & statistics, numerical methods',
 'GA':'GATE aptitude: verbal, quant, reasoning'}

# ---------- subject stream ----------
def ids(prefix, nums, fmt='T{:02d}'): return [f'{prefix}-{fmt.format(n)}' for n in nums]
blocks = [  # key, [2027 tests], [2026 practice], [grand/single tests]
 ('SOM', ids('G27',[9,10,20])+ids('H27',[1,2])+['A27-T02','M27-S01'], ids('G26',[9,10,20])+ids('H26',[1,2])+['A26-T02','M26-S01'], ['G27-T26','H27-T25','G26-T26','H26-T25']),
 ('SA', ids('G27',[5,6])+ids('H27',[15,16])+['A27-T07','M27-S05'], ids('G26',[5,6])+ids('H26',[15,16])+['A26-T07','M26-S05'], ['G27-T28','H27-T32','G26-T28','H26-T32']),
 ('RCC', ids('G27',[7])+ids('H27',[3,4])+['A27-T11','M27-S09'], ids('G26',[7])+ids('H26',[3,4])+['A26-T11','M26-S09'], ['H27-T26','H26-T26']),
 ('Steel', ids('G27',[8])+ids('H27',[20,21])+['A27-T15','M27-S13'], ids('G26',[8])+ids('H26',[20,21])+['A26-T15','M26-S13'], ['G27-T29','H27-T34','G26-T29','H26-T34']),
 ('Geotech', ids('G27',[3,4])+ids('H27',[17,18,19])+['A27-T09','M27-S15'], ids('G26',[3,4])+ids('H26',[17,18,19])+['A26-T09','M26-S15'], ['G27-T30','H27-T33','G26-T30','H26-T33']),
 ('FM', ids('G27',[11,12])+ids('H27',[7,8])+['A27-T03','M27-S11'], ids('G26',[11,12])+ids('H26',[7,8])+['A26-T03','M26-S11'], ['G27-T32','H27-T28','G26-T32','H26-T28']),
 ('Hydro', ids('G27',[13,14])+ids('H27',[22,23])+['A27-T17','M27-S07'], ids('G26',[13,14])+ids('H26',[22,23])+['A26-T17','M26-S07'], ['G27-T31','H27-T35','G26-T31','H26-T35']),
 ('Env', ids('G27',[15,16])+ids('H27',[5,6])+['A27-T05','M27-S03'], ids('G26',[15,16])+ids('H26',[5,6])+['A26-T05','M26-S03'], ['G27-T27','H27-T27','G26-T27','H26-T27']),
 ('Transport', ids('G27',[17,18])+ids('H27',[13,14])+['A27-T01','M27-S19'], ids('G26',[17,18])+ids('H26',[13,14])+['A26-T01','M26-S19'], ['G27-T33','G26-T33']),
 ('Survey', ids('G27',[19])+['A27-T13','M27-S22'], ids('G26',[19])+['A26-T13','M26-S22'], ['G27-T34','H27-T31','G26-T34','H26-T31']),
 ('BM', ids('G27',[21])+ids('H27',[24])+['A27-T19','A27-T21','M27-S21','M27-S17'], ids('G26',[21])+ids('H26',[24])+['A26-T19','A26-T21','M26-S21','M26-S17'], ['G27-T35','H27-T36','G26-T35','H26-T36']),
 ('Maths', ids('G27',[1,2])+ids('H27',[9,10])+['A27-T04','M27-S04'], ids('G26',[1,2])+ids('H26',[9,10])+['A26-T04','M26-S04'], ['G27-T25','H27-T29','G26-T25','H26-T29']),
]
gs_stream = ['A27-T14','M27-S02','G27-T24','G27-T22','G27-T23','H27-T11','H27-T12','A27-T10','M27-S16','A26-T14','M26-S02','G26-T24',
    'A27-T06','M27-S08','A26-T10','M26-S16','G26-T22','G26-T23','H26-T11','H26-T12','A27-T12','M27-S14','A26-T06','M26-S08',
    'A27-T18','M27-S18','A26-T12','M26-S14','A27-T08','M27-S06','G27-T36','H27-T30','A26-T18','M26-S18','A27-T16','M27-S12','A26-T08','M26-S06',
    'A27-T20','M27-S10','G26-T36','H26-T30','A26-T16','M26-S12','A27-T22','M27-S20','A26-T20','M26-S10','A26-T22','M26-S20']
blocks.insert(3, blocks.pop(11))   # Maths earlier: weightier than BM/Surveying, so those take the late slots
_env = next(i for i, b in enumerate(blocks) if b[0] == 'Env'); blocks.insert(0, blocks.pop(_env))   # start with Environmental (user's choice)
tech = [(t, k) for k, a, b, c in blocks for t in keep(a + b + c)]
gs_stream = [t for t in keep(gs_stream) if t not in DONE_TODAY]
th = sum(T[t]['hrs'] for t, _ in tech); gh = sum(T[t]['hrs'] for t in gs_stream)
stream = []; ti = gi = 0; at = ag = 0.0
while ti < len(tech) or gi < len(gs_stream):
    if gi >= len(gs_stream) or (ti < len(tech) and at / th <= ag / gh):
        stream.append(tech[ti]); at += T[tech[ti][0]]['hrs']; ti += 1
    else:
        stream.append((gs_stream[gi], None)); ag += T[gs_stream[gi]]['hrs']; gi += 1
multi = ['G27-T43','H26-T37','A27-T27','A27-T28','G26-T37','G27-T44','H26-T38','A27-T29','A27-T30','G26-T38','G27-ADD1','G27-T45','H26-T39',
         'A27-T31','A27-T32','G26-T39','G27-ADD2','G27-T46','H26-T40','A27-T33','A27-T34','G26-T40','G27-ADD3','G27-T47','H26-T41','A27-T35','A27-T36','G26-T41','G27-T48','H26-T42','G26-T42']
stream += [(t, 'multi') for t in keep(multi)]

# ---------- papers ----------
gate_rr = [ ['G27-FLT%d' % k for k in range(4, 11)], ['G26-FLT%d' % k for k in range(1, 13)], ['H27-F%d' % k for k in range(1, 9)] + ['H27-K%d' % k for k in range(1, 5)],
            ['H26-F%d' % k for k in range(1, 9)] + ['H26-K%d' % k for k in range(1, 5)] ]
gate_rr = [keep(q) for q in gate_rr]
gate_q = []
while any(gate_rr):
    for q in gate_rr:
        if q: gate_q.append(q.pop(0))
ese_q = ['M27-F1a','M27-F1b','A26-M1a','A26-M1b','M26-F2','M27-F3a','M27-F3b','A26-M2a','A26-M2b','M26-F4','M27-F5a','M27-F5b',
         'A26-M3a','A26-M3b','M26-F6','M27-F7a','M27-F7b','A26-M4a','A26-M4b','M26-F7a','M26-F7b','M26-F9a','M26-F9b','M26-F11a','M26-F11b']

ese_q = keep(ese_q)
days = {}
d = START
while d <= END:
    days[d] = dict(date=d, cap=cap(d), tests=[]); d += dt.timedelta(1)
D2 = lambda m, dd: dt.date(2026, m, dd)
anchors = {D2(10,11): DONE_TODAY + ['M26-F1'], D2(10,18): ['A27-M1'], D2(10,25): ['G27-FLT2','M26-F3'], D2(11,1): ['A27-M2'], D2(11,8): ['G27-FLT3','M26-F5'],
           D2(11,28): ['A27-M3'], D2(12,5): ['A27-M4'], D2(12,12): ['A27-M5'], D2(12,15): ['A27-M6b']}
for k, v in anchors.items(): days[k]['tests'] += v
P1_END = D2(*map(int, P1_END_ENV.split('-')))
H = lambda t: T[t]['hrs']
used = lambda o: sum(H(t) for t in o['tests'])
ngate = lambda o: sum(1 for t in o['tests'] if H(t) >= 3 and t[:3] in ('G27','G26','H27','H26'))

def fill_stream(o, d, look=6):
    while stream:
        took = False
        for k in range(min(look, len(stream))):
            t, _ = stream[k]
            if T[t]['act'] <= d and used(o) + H(t) <= o['cap'] + 0.15:
                o['tests'].append(t); stream.pop(k); took = True; break
        if not took: break

def take_paper(o, d, maxgate=2):
    """add one paper (GATE or ESE, alternating by remaining share) if it fits"""
    room = o['cap'] - used(o)
    cands = []
    for q, isg in ((gate_q, True), (ese_q, False)):
        for i, t in enumerate(q[:4]):
            if T[t]['act'] <= d and H(t) <= room + 0.05 and not (isg and ngate(o) >= maxgate):
                if not isg and t.endswith('b') and (t[:-1] + 'a') in [x for x in o['tests']]:
                    pass
                cands.append((q, i, t, isg)); break
    if not cands: return False
    # prefer the queue with more remaining hours per remaining day
    gh_ = sum(H(t) for t in gate_q); eh_ = sum(H(t) for t in ese_q)
    cands.sort(key=lambda c: -(gh_ if c[3] else eh_))
    q, i, t, _ = cands[0]; o['tests'].append(q.pop(i)); return True

for d in sorted(days):
    o = days[d]
    if d <= P1_END:
        fill_stream(o, d)
        continue
    wk = d.weekday() >= 5
    if not o['tests']:
        target = (2 if wk else 1) if stream else (3 if wk else 2)
        for _ in range(target): take_paper(o, d)
    else:   # anchored ESE day: one more paper if room
        take_paper(o, d)
    fill_stream(o, d)
    while o['cap'] - used(o) >= 2 and take_paper(o, d): pass
    fill_stream(o, d)

left = [t for t, _ in stream] + gate_q + ese_q
cnt = collections.Counter(t for o in days.values() for t in o['tests'])
missing = [t for t in T if t not in cnt and t != 'A27-M6a']
ok = not left and not missing
print('left', left); print('missing', missing)
print('dupes', [t for t, c in cnt.items() if c > 1])
print('activation', [(o['date'], t) for o in days.values() for t in o['tests'] if T[t]['act'] > o['date']])
over = [(o['date'], round(used(o), 2), o['cap']) for o in days.values() if used(o) > o['cap'] + 0.15]
print('over', over)
print('FEASIBLE', ok and not over, 'WD', WD)
tot = sum(used(o) for o in days.values()); capt = sum(o['cap'] for o in days.values())
print('total', round(tot, 1), 'cap', capt, 'all tests h', round(sum(v['hrs'] for v in T.values()), 1))
for d in sorted(days):
    o = days[d]
    if '-v' in sys.argv:
        print(d.strftime('%a %d %b'), f"{used(o):4.1f}/{o['cap']}", 'G%d' % ngate(o), '|', ', '.join(o['tests']))
json.dump(dict(T={k: {**v, 'act': v['act'].isoformat()} for k, v in T.items()},
               days=[{'date': o['date'].isoformat(), 'cap': o['cap'], 'tests': o['tests']} for o in (days[d] for d in sorted(days))],
               left=left), open(os.environ.get('OUT', 'plan_v4.json'), 'w'), indent=1)
