"""Plan v5: subject revision blocks with spaced test waves (Env first).
Each subject gets 2-4 revision days. Its tests come back in four waves:
  W1 during the block (ACE 2027 tests), W2 about a week later (MADE EASY 2027),
  W3 about two weeks later (2026 practice), W4 about three weeks later (grand/single tests).
Full-length papers are spread through the whole window; multi-subject tests at the end.
Solved with CP-SAT: hard quota per day, soft targets for each test."""
import os, io, contextlib, json, datetime as dt, collections, sys
os.environ['OUT'] = '/dev/null'; os.environ.setdefault('WD', '3.75'); os.environ.setdefault('P1', '10-28')
with contextlib.redirect_stdout(io.StringIO()):
    exec(open('plan_v4.py').read())      # T (6 series), SUB, SHORT, TOP, blocks, keep, DONE_TODAY, gs_stream, multi
from ortools.sat.python import cp_model

WDQ = float(os.environ.get('WDQ', '3.75'))
START = dt.date(2026, 10, 11); END = dt.date(2026, 12, 15)
DAYS = [START + dt.timedelta(i) for i in range((END - START).days + 1)]
DI = {d: i for i, d in enumerate(DAYS)}
capm = lambda d: int(round((10.0 if d.weekday() >= 5 else WDQ) * 60))
M = lambda t: int(round(T[t]['hrs'] * 60))
D2 = lambda m, dd: dt.date(2026, m, dd)

# ---------- revision blocks ----------
LEN = {'Env': 3, 'SOM': 4, 'SA': 3, 'RCC': 3, 'Maths': 3, 'Steel': 3, 'Geotech': 4, 'FM': 4, 'Hydro': 3, 'Transport': 3, 'Survey': 2, 'BM': 2}
BSTART = {}; d = START
for k, *_ in blocks:
    BSTART[k] = d; d += dt.timedelta(LEN[k])
BLOCK_END = d - dt.timedelta(1)

rel, tgt, wt, we, wave, span = {}, {}, {}, {}, {}, {}
def setp(t, r, g, w, wv, e=None, sp=None):
    rel[t] = max(r, START); tgt[t] = max(g, rel[t]); wt[t] = w; we[t] = w if e is None else e; wave[t] = wv; span[t] = sp
for k, a, b, c in blocks:
    s = BSTART[k]
    for t in keep(a):
        if t[:3] in ('G27', 'A27'): setp(t, s, s + dt.timedelta(1), 6, 1, 2, 10)
        else:                       setp(t, s + dt.timedelta(4), s + dt.timedelta(7), 4, 2, 2, 12)
    for t in keep(b): setp(t, s + dt.timedelta(9), s + dt.timedelta(13), 4, 3, 2, 14)
    for t in keep(c): setp(t, s + dt.timedelta(14), s + dt.timedelta(19), 4, 4, 2, 16)
# GS / GATE aptitude stream: evenly through Oct 11 - Nov 26
gs = list(gs_stream)
for i, t in enumerate(gs):
    g = START + dt.timedelta(round(i * 46 / max(1, len(gs) - 1)))
    setp(t, START, g, 2, 0, 1, 14)
# multi-subject tests: after every subject in them has had its third wave
ML = keep(multi)
for i, t in enumerate(ML):
    subs = [s for s in SUB(t) if not s.startswith('GS:')]
    r = max([BSTART[s] + dt.timedelta(13) for s in subs if s in BSTART] + [D2(11, 25)])
    g = D2(12, 2) + dt.timedelta(round(i * 12 / (len(ML) - 1)))
    setp(t, r, g, 2, 5, 2, None)
# full-length papers
gate_order = []
rr = [['G27-FLT%d' % k for k in range(2, 11)], ['H27-F%d' % k for k in range(1, 9)] + ['H27-K%d' % k for k in range(1, 5)],
      ['H26-F%d' % k for k in range(1, 9)] + ['H26-K%d' % k for k in range(1, 5)]]
while any(rr):
    for q in rr:
        if q: gate_order.append(q.pop(0))
ese_order = ['M27-F1a', 'M27-F1b', 'M26-F1', 'M26-F2', 'M27-F3a', 'M27-F3b', 'M26-F3', 'M26-F4', 'M27-F5a', 'M27-F5b', 'M26-F5', 'M26-F6',
             'M27-F7a', 'M27-F7b', 'M26-F7a', 'M26-F7b', 'M26-F9a', 'M26-F9b', 'M26-F11a', 'M26-F11b']
for seq, a0, a1 in ((gate_order, D2(10, 17), D2(12, 13)), (ese_order, D2(10, 12), D2(12, 13))):
    for i, t in enumerate(seq):
        g = a0 + dt.timedelta(round(i * (a1 - a0).days / (len(seq) - 1)))
        setp(t, max(START, g - dt.timedelta(14)), g, 2, 6, 2, 14)
FIX = {t: START for t in DONE_TODAY}
FIX.update({'A27-M1': D2(10, 18), 'A27-M2': D2(11, 1), 'A27-M3': D2(11, 28), 'A27-M4': D2(12, 5), 'A27-M5': D2(12, 12), 'A27-M6b': D2(12, 15)})
ALL = [t for t in T if t != 'A27-M6a']
missing = [t for t in ALL if t not in rel and t not in FIX]
assert not missing, missing

# ---------- model ----------
m = cp_model.CpModel()
x = {}; dayv = {}
for t in ALL:
    if t in FIX:
        dom = [FIX[t]]
    else:
        lo = max(rel[t], T[t]['act'], START)
        hi = tgt[t] + dt.timedelta(span[t]) if span[t] else END
        dom = [d for d in DAYS if lo <= d <= hi]
    assert dom, t
    vs = []
    for d in dom:
        x[t, d] = m.NewBoolVar(''); vs.append(x[t, d])
    m.AddExactlyOne(vs)
    dayv[t] = m.NewIntVar(DI[dom[0]], DI[dom[-1]], '')
    m.Add(dayv[t] == sum(DI[d] * x[t, d] for d in dom))
by_day = collections.defaultdict(list)
for (t, d), v in x.items(): by_day[d].append((t, v))
for d in DAYS:
    m.Add(sum(M(t) * v for t, v in by_day[d]) <= capm(d) + 9)
    m.Add(sum(v for t, v in by_day[d] if T[t]['hrs'] >= 3 and t[:3] in ('G27', 'H27', 'H26')) <= 2)
    m.Add(sum(v for t, v in by_day[d] if T[t]['hrs'] >= 2) <= 3)
    # no more than 3 tests of one subject on a day (keeps waves spread)
    sub_vars = collections.defaultdict(list)
    for t, v in by_day[d]:
        for s in SUB(t):
            if not s.startswith('GS:') and T[t]['hrs'] < 2 and t not in ML: sub_vars[s].append(v)
    for s, vs in sub_vars.items():
        if len(vs) > 3: m.Add(sum(vs) <= 3)
# keep each series' papers in order
for seq in (['G27-FLT%d' % k for k in range(2, 11)], ['H27-F%d' % k for k in range(1, 9)] + ['H27-K%d' % k for k in range(1, 5)],
            ['H26-F%d' % k for k in range(1, 9)] + ['H26-K%d' % k for k in range(1, 5)],
            ['M27-F1a', 'M27-F1b', 'M27-F3a', 'M27-F3b', 'M27-F5a', 'M27-F5b', 'M27-F7a', 'M27-F7b'],
            ['M26-F1', 'M26-F2', 'M26-F3', 'M26-F4', 'M26-F5', 'M26-F6', 'M26-F7a', 'M26-F7b', 'M26-F9a', 'M26-F9b', 'M26-F11a', 'M26-F11b']):
    for a, b in zip(seq, seq[1:]): m.Add(dayv[a] <= dayv[b])
# soft targets
cost = []
for t in ALL:
    if t in FIX: continue
    late = m.NewIntVar(0, 80, ''); early = m.NewIntVar(0, 80, '')
    m.Add(dayv[t] - DI[tgt[t]] == late - early)
    cost += [wt[t] * late, we[t] * early]
m.Minimize(sum(cost))
sv = cp_model.CpSolver(); sv.parameters.max_time_in_seconds = float(os.environ.get('TL', '240')); sv.parameters.num_workers = 8
st = sv.Solve(m)
print('status', sv.StatusName(st), 'obj', sv.ObjectiveValue() if st in (cp_model.OPTIMAL, cp_model.FEASIBLE) else None)
if st not in (cp_model.OPTIMAL, cp_model.FEASIBLE): sys.exit(1)

plan = collections.defaultdict(list)
for (t, d), v in x.items():
    if sv.Value(v): plan[d].append(t)
# order within a day: done first, papers, then by wave
for d in DAYS:
    plan[d].sort(key=lambda t: (t not in DONE_TODAY, -T[t]['hrs'] >= 2 and 0, wave.get(t, 6), t))
lat = collections.defaultdict(list)
for d in DAYS:
    for t in plan[d]:
        if t in tgt: lat[wave[t]].append((d - tgt[t]).days)
for w in sorted(lat): print('wave', w, 'n', len(lat[w]), 'mean dev', round(sum(lat[w]) / len(lat[w]), 1), 'max late', max(lat[w]), 'max early', min(lat[w]))
over = [(d, sum(T[t]['hrs'] for t in plan[d])) for d in DAYS if sum(M(t) for t in plan[d]) > capm(d) + 9]
print('over', over, 'blocks', {k: v.isoformat() for k, v in BSTART.items()}, 'block end', BLOCK_END)
json.dump(dict(days=[{'date': d.isoformat(), 'cap': capm(d) / 60, 'tests': plan[d]} for d in DAYS],
               bstart={k: v.isoformat() for k, v in BSTART.items()}, blen=LEN, wave=wave, block_end=BLOCK_END.isoformat()),
          open('plan_v5.json', 'w'), indent=1)
if '-v' in sys.argv:
    for d in DAYS:
        print(d.strftime('%a %d %b'), f"{sum(T[t]['hrs'] for t in plan[d]):4.1f}", ' '.join(f"{t}{'·' + str(wave.get(t, '')) if t in wave else ''}" for t in plan[d]))
