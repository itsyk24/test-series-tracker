/* Test Series Tracker — offline single-page app (Android WebView or browser). */
(() => {
'use strict';

// ---------- constants ----------
const SERIES = [
  { k: 'G27', name: 'ACE GATE-27', short: 'GATE-27', ring: false },
  { k: 'G26', name: 'ACE GATE-26', short: 'GATE-26', ring: true },
  { k: 'H27', name: 'MADE EASY GATE-27', short: 'ME GATE-27', ring: false },
  { k: 'H26', name: 'MADE EASY GATE-26', short: 'ME GATE-26', ring: true },
  { k: 'A27', name: 'ACE ESE-27', short: 'ESE-27', ring: false },
  { k: 'A26', name: 'ACE ESE-26', short: 'ESE-26', ring: true },
  { k: 'M27', name: 'MADE EASY ESE-27', short: 'ME ESE-27', ring: false },
  { k: 'M26', name: 'MADE EASY ESE-26', short: 'ME ESE-26', ring: true },
];
const SER = Object.fromEntries(SERIES.map(s => [s.k, s]));
const KIND = { subject: 'Subject test', grand: 'Subject grand test', multi: 'Multi-subject test', mock: 'Full-length paper', add: 'New-syllabus test' };
const TOPICS = {
  'SOM + EM': ['Stress–strain, elastic constants', 'Mohr circle, principal stresses', 'SFD and BMD', 'Bending and shear stress, shear centre', 'Torsion', 'Deflection of beams', 'Columns and buckling', 'Combined stresses, theories of failure', 'Engg mechanics: FBD, friction, centroid, MI'],
  'SA': ['Static and kinematic indeterminacy', 'Consistent deformation', 'Slope-deflection', 'Moment distribution', 'ILD and moving loads', 'Energy methods (virtual work, Castigliano)', 'Arches and cables', 'Stiffness and flexibility methods'],
  'RCC': ['WSM vs LSM, partial safety factors', 'Singly, doubly reinforced and flanged beams', 'Shear, torsion, bond, development length', 'One-way and two-way slabs', 'Short and long columns', 'Isolated footings', 'Prestressed concrete basics', 'Masonry design'],
  'Steel': ['Tension members', 'Compression members', 'Laterally restrained and unrestrained beams', 'Beam-columns', 'Column bases', 'Bolted connections', 'Welded connections, eccentric', 'Plastic analysis'],
  'Geotech': ['Phase relations, index properties, classification', 'Permeability, seepage, flow nets', 'Effective stress', 'Compaction', 'Consolidation', 'Shear strength', 'Earth pressure', 'Slope stability', 'Bearing capacity, settlement', 'Pile foundations', 'Ground improvement'],
  'FM + Hydraulics': ['Fluid properties and statics', 'Kinematics', 'Bernoulli and momentum', 'Pipe flow and networks', 'Laminar and turbulent flow', 'Boundary layer, lift and drag', 'Dimensional analysis', 'Open channel, hydraulic jump, GVF', 'Pumps and turbines', 'Hydropower'],
  'Hydrology + Irrigation': ['Precipitation, evaporation, infiltration', 'Hydrographs, unit hydrograph', 'Flood estimation and routing', 'Wells and aquifers', 'Duty, delta, crop water', 'Canals and lining', 'Weirs on permeable foundations', 'Dams and spillways', 'River training'],
  'Env': ['Water demand and quality', 'Water treatment units', 'Distribution systems', 'Sewerage and wastewater treatment', 'Sludge treatment', 'Air pollution and AQI', 'Noise pollution', 'Solid waste and landfills'],
  'Transport': ['Highway geometric design (IRC)', 'Pavement materials and tests', 'Flexible pavement design', 'Rigid pavement design', 'Traffic studies, flow fundamentals', 'Signal design (Webster)', 'Intersections', 'Railways: speed, cant', 'Airports: runway length, corrections'],
  'Surveying': ['Chain, compass, levelling', 'Theodolite, traversing, triangulation', 'Curves', 'Total station, GNSS', 'Errors and adjustment', 'Photogrammetry, remote sensing', 'GIS basics', 'Engineering geology'],
  'BM + CPM': ['Cement, hydration, admixtures', 'Concrete mix design and properties', 'Steel, bricks, stone, timber, lime', 'Estimation and rate analysis', 'PERT and CPM, crashing', 'Construction equipment', 'Contracts'],
  'Maths': ['Linear algebra', 'Calculus and vector calculus', 'ODE and PDE', 'Probability and statistics', 'Numerical methods'],
  'GATE aptitude': ['Verbal ability', 'Quantitative aptitude', 'Analytical reasoning', 'Spatial reasoning'],
};
const SUBJECT_NAMES = { 'SOM + EM': 'Solid Mechanics + Engg Mechanics', 'SA': 'Structural Analysis', 'RCC': 'RCC + Masonry', 'Steel': 'Steel Structures', 'Geotech': 'Geotechnical + Foundation', 'FM + Hydraulics': 'Fluid Mechanics + Hydraulics', 'Hydrology + Irrigation': 'Hydrology + Irrigation', 'Env': 'Environmental', 'Transport': 'Transportation', 'Surveying': 'Surveying + Geology', 'BM + CPM': 'Building Materials + CPM', 'Maths': 'Engineering Maths', 'GATE aptitude': 'GATE General Aptitude' };
const STORE_KEY = 'tst_state_v1';

// ---------- native bridge ----------
const Native = window.Android || null;
const store = {
  load() { try { return Native ? Native.load() : localStorage.getItem(STORE_KEY); } catch (e) { return null; } },
  save(s) { try { Native ? Native.save(s) : localStorage.setItem(STORE_KEY, s); } catch (e) { } },
};
const vibrate = ms => { try { navigator.vibrate && navigator.vibrate(ms); } catch (e) { } };

// ---------- dates ----------
const pad = n => String(n).padStart(2, '0');
const iso = dt => `${dt.getFullYear()}-${pad(dt.getMonth() + 1)}-${pad(dt.getDate())}`;
const parse = s => { const [y, m, d] = s.split('-').map(Number); return new Date(y, m - 1, d); };
const addDays = (s, n) => { const d = parse(s); d.setDate(d.getDate() + n); return iso(d); };
const diffDays = (a, b) => Math.round((parse(b) - parse(a)) / 864e5);
const WD = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];
const WDL = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];
const MO = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
const MOL = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];
const fmtShort = s => { const d = parse(s); return `${WD[d.getDay()]} ${d.getDate()} ${MO[d.getMonth()]}`; };
const fmtDM = s => { const d = parse(s); return `${d.getDate()} ${MO[d.getMonth()]}`; };
const isWeekend = s => { const g = parse(s).getDay(); return g === 0 || g === 6; };
const urlToday = new URLSearchParams(location.search).get('today');
const TODAY = () => urlToday || iso(new Date());

const fmtH = h => {
  const m = Math.round(h * 60);
  if (m < 60) return `${m} min`;
  const hh = Math.floor(m / 60), mm = m % 60;
  return mm ? `${hh} h ${mm} min` : `${hh} h`;
};
const fmtHd = h => (Math.round(h * 10) / 10).toString().replace(/\.0$/, '');
const esc = s => String(s ?? '').replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));

// ---------- state ----------
const SEEDMAP = Object.fromEntries(SEED.tests.map(t => [t.id, t]));
let S = loadState();

function freshState() { return { v: 1, seed: 0, theme: 'dark', tests: {}, topics: {}, created: TODAY() }; }
function loadState() {
  let st = null;
  try { const raw = store.load(); if (raw) st = JSON.parse(raw); } catch (e) { st = null; }
  if (!st || typeof st !== 'object' || !st.tests) st = freshState();
  // plan update: tests you haven't touched follow the new plan; done, skipped or moved tests stay as they are
  if ((st.seed || 0) < SEED.version && SEED.prev) {
    for (const t of SEED.tests) {
      const x = st.tests[t.id];
      if (x && x.st === 'todo' && SEED.prev[t.id] && x.d === SEED.prev[t.id]) { x.d = t.d; x.o = t.o; }
    }
  }
  for (const t of SEED.tests) if (!st.tests[t.id]) st.tests[t.id] = { d: t.d, st: 'todo', o: t.o };
  st.seed = SEED.version;
  st.topics = st.topics || {};
  return st;
}
let saveTimer = null;
function save() { clearTimeout(saveTimer); saveTimer = setTimeout(() => store.save(JSON.stringify(S)), 120); }
function saveNow() { clearTimeout(saveTimer); store.save(JSON.stringify(S)); }

const T = id => ({ ...SEEDMAP[id], ...S.tests[id] });
const allTests = () => SEED.tests.map(t => T(t.id));
function testsOn(date) { return allTests().filter(t => t.d === date).sort((a, b) => a.o - b.o); }
function loadOf(date) { return testsOn(date).reduce((a, t) => a + t.h, 0); }
function capOf(date) { return SEED.caps[date] ?? (isWeekend(date) ? 10 : 6.5); }
function maxOrder() { return Math.max(...Object.values(S.tests).map(x => x.o || 0)); }
function planDays() {
  const out = []; let d = SEED.start; const last = allTests().reduce((m, t) => t.d > m ? t.d : m, SEED.end);
  while (d <= last) { out.push(d); d = addDays(d, 1); }
  return out;
}

// ---------- history (undo) ----------
let undoFn = null;
function toast(msg, undo) {
  const el = document.getElementById('toast');
  el.innerHTML = `<span>${esc(msg)}</span>${undo ? '<button type="button" id="undo-btn">Undo</button>' : ''}`;
  el.classList.add('in');
  undoFn = undo || null;
  if (undo) document.getElementById('undo-btn').onclick = () => { const f = undoFn; undoFn = null; el.classList.remove('in'); f && f(); };
  clearTimeout(toast._t); toast._t = setTimeout(() => { el.classList.remove('in'); undoFn = null; }, undo ? 4500 : 2600);
}

// ---------- mutations ----------
function setStatus(id, st, quiet) {
  const prev = { ...S.tests[id] };
  S.tests[id].st = st;
  S.tests[id].doneAt = st === 'done' ? TODAY() : undefined;
  save(); render();
  if (st === 'done') vibrate(12);
  if (!quiet) {
    const label = st === 'done' ? 'Marked done' : st === 'skip' ? 'Marked skipped' : 'Marked to do';
    toast(label, () => { S.tests[id] = prev; save(); render(); });
  }
}
function moveTest(id, date) {
  const t = T(id);
  if (date === t.d) return false;
  if (date < t.act) { toast(`Opens ${fmtShort(t.act)}, 6 PM. Pick a later day.`); vibrate([20, 40, 20]); return false; }
  const prev = { ...S.tests[id] };
  S.tests[id].d = date; S.tests[id].o = maxOrder() + 1;
  save(); render();
  const over = loadOf(date) > capOf(date) + 0.15;
  toast(`Moved to ${fmtShort(date)}${over ? ', over quota' : ''}`, () => { S.tests[id] = prev; save(); render(); });
  return true;
}

// ---------- rendering helpers ----------
const CHECK_SVG = '<svg viewBox="0 0 16 16"><path d="M3.2 8.4 6.6 11.6 12.8 4.6"/></svg>';
const dot = k => `<span class="dot s-${k}${SER[k].ring ? ' ring' : ''}" aria-hidden="true"></span>`;

function scale(total, filled, done, opts = {}) {
  const cap = Math.max(total, 0.01);
  const span = opts.span || Math.max(cap, filled);
  const pct = v => Math.min(100, (v / span) * 100);
  const major = opts.major || 1, minor = opts.minor || 0.5;
  const style = `--major:${(major / span) * 100}%;--minor:${(minor / span) * 100}%`;
  let html = `<div class="scale${opts.small ? ' small' : ''}" style="${style}"><div class="ticks"></div>`;
  html += `<div class="fill" style="width:${pct(Math.min(filled, cap))}%"></div>`;
  if (filled > cap + 0.05) html += `<div class="over" style="left:${pct(cap)}%;width:${pct(filled) - pct(cap)}%"></div>`;
  html += `<div class="done" style="width:${pct(done)}%"></div>`;
  if (opts.notch != null) html += `<div class="notch" style="left:calc(${pct(opts.notch)}% - 1px)"></div>`;
  if (opts.expected != null) html += `<div class="notch expected" style="left:calc(${pct(opts.expected)}% - 1px)"></div>`;
  return html + '</div>';
}

function trow(t, showDate) {
  const s = SER[t.s];
  const meta = [s.name, fmtH(t.h)];
  if (showDate) meta.push(fmtShort(t.d));
  const warn = t.st === 'todo' && t.d < TODAY() ? '<span class="warn">Overdue</span>' : '';
  return `<li><div class="trow ${t.st}" data-id="${t.id}">
    ${dot(t.s)}
    <button class="main" data-open="${t.id}"><div class="t">${esc(t.n)}</div><div class="m">${meta.map(x => `<span>${esc(x)}</span>`).join('')}${t.score ? `<span>Score ${esc(t.score)}</span>` : ''}${warn}</div></button>
    <button class="check" data-toggle="${t.id}" aria-label="${t.st === 'done' ? 'Mark not done' : 'Mark done'}">${CHECK_SVG}</button>
  </div></li>`;
}

function parseRev(rev) {
  if (!rev) return [];
  return rev.split(/\.\s(?=\*\*New|Recap:|GS:|Mock prep:|Rotation:|Buffer)/).map(seg => {
    seg = seg.replace(/\.$/, '');
    let m = seg.match(/^\*\*New — ([^:]+):\s*(.+?)\*\*$/);
    if (m) return { kind: 'New', title: m[1], det: m[2] };
    m = seg.match(/^(Recap|GS|Mock prep|Rotation|Buffer day):\s*(.+)$/);
    if (m) return { kind: m[1] === 'Buffer day' ? 'Buffer' : m[1], title: m[2].replace(/, GS /, ' + GS: ') };
    return { kind: 'Note', title: seg.replace(/\*\*/g, '') };
  });
}

// ---------- views ----------
let tab = 'today';
const scrollPos = {};

function viewToday() {
  const today = TODAY();
  const todays = testsOn(today);
  const load = todays.reduce((a, t) => a + t.h, 0);
  const done = todays.filter(t => t.st === 'done').reduce((a, t) => a + t.h, 0);
  const cap = capOf(today);
  const d = parse(today);
  const dayNo = diffDays(SEED.start, today) + 1, totalDays = diffDays(SEED.start, SEED.end) + 1;
  const overdue = allTests().filter(t => t.st === 'todo' && t.d < today).sort((a, b) => a.d.localeCompare(b.d) || a.o - b.o);
  const tomorrow = addDays(today, 1);
  const tmr = testsOn(tomorrow);
  const rev = parseRev(SEED.rev[today]);
  const subj = [...new Set(todays.flatMap(t => t.sub))], gs = [...new Set(todays.flatMap(t => t.gs))];
  let dayCount = '';
  if (dayNo >= 1 && dayNo <= totalDays) dayCount = `<b>Day ${dayNo}</b>of ${totalDays}`;
  else if (dayNo < 1) dayCount = `<b>${1 - dayNo} days</b>to start`;
  else dayCount = `<b>Done</b>plan finished`;

  let h = `<section class="hero">
    <div class="row"><div><div class="weekday">${WDL[d.getDay()]}</div><div class="date">${d.getDate()} ${MOL[d.getMonth()]}</div></div>
    <div class="daycount">${dayCount}</div></div>
    <div class="load-label"><span><b>${fmtHd(done)}</b> of ${fmtHd(load)} h done</span><span>Quota ${fmtHd(cap)} h</span></div>
    ${scale(cap, load, done, { span: Math.max(cap, load, 1) })}
  </section>`;

  if (rev.length || subj.length) {
    h += `<section class="section"><h2>Revise first</h2><div class="sheetbox rev">`;
    for (const r of rev) {
      h += `<div class="item"><div class="kind ${r.kind === 'New' ? 'new' : ''}">${esc(r.kind)}</div><div class="what">${r.det ? `<b>${esc(r.title)}</b><span class="det">${esc(r.det)}</span>` : esc(r.title)}</div></div>`;
    }
    if (subj.length || gs.length) h += `<div class="item"><div class="kind">Tested today</div><div class="chips">${[...subj, ...gs].map(x => `<span class="chip-s">${esc(x)}</span>`).join('')}</div></div>`;
    h += `</div></section>`;
  }

  h += `<section class="section"><h2>Today's tests <span>${todays.length ? `${todays.filter(t => t.st === 'done').length} of ${todays.length}` : ''}</span></h2><div class="sheetbox">`;
  h += todays.length ? `<ul class="list">${todays.map(t => trow(t)).join('')}</ul>` : `<div class="empty">Nothing planned today. Pull a test in from the Plan tab, or use the day to revise.</div>`;
  h += `</div></section>`;

  if (overdue.length) {
    h += `<section class="section"><h2>Carried over <span>${overdue.length} tests, ${fmtHd(overdue.reduce((a, t) => a + t.h, 0))} h</span></h2><div class="sheetbox"><ul class="list">${overdue.map(t => trow(t, true)).join('')}</ul></div></section>`;
  }
  if (tmr.length) {
    h += `<section class="section"><h2>Tomorrow <span>${fmtShort(tomorrow)}, ${fmtHd(tmr.reduce((a, t) => a + t.h, 0))} h</span></h2><div class="sheetbox"><ul class="list">${tmr.map(t => trow(t)).join('')}</ul></div></section>`;
  }
  return h;
}

function weekKey(s) { const d = parse(s); const g = (d.getDay() + 6) % 7; return addDays(s, -g); } // Monday
function phaseOf(s) { return s <= '2026-11-08' ? 'Subject sweep' : s <= '2026-11-28' ? 'Integration' : 'Full-length papers'; }

function viewPlan() {
  const today = TODAY();
  const days = planDays();
  const weeks = [];
  for (const d of days) { const k = weekKey(d); if (!weeks.length || weeks[weeks.length - 1].k !== k) weeks.push({ k, days: [] }); weeks[weeks.length - 1].days.push(d); }
  let h = `<div class="planbar"><h1>Plan</h1><button class="btn-ghost" data-jump="today">Jump to today</button></div>
    <p class="legend">Hold a test, then drag it onto another day. Tap a test for details.</p>`;
  for (const w of weeks) {
    const tot = w.days.reduce((a, d) => a + loadOf(d), 0);
    const first = w.days[0], last = w.days[w.days.length - 1];
    h += `<div class="week"><div class="week-h"><span><b>${fmtDM(first)} – ${fmtDM(last)}</b>   ${phaseOf(first)}</span><span>${fmtHd(tot)} h</span></div>`;
    for (const d of w.days) {
      const ts = testsOn(d), load = ts.reduce((a, t) => a + t.h, 0), cap = capOf(d);
      const done = ts.filter(t => t.st === 'done').reduce((a, t) => a + t.h, 0);
      const dd = parse(d);
      const cls = ['day']; if (d === today) cls.push('today'); else if (d < today) cls.push('past');
      h += `<div class="${cls.join(' ')}" data-date="${d}" id="day-${d}">
        <div class="day-h"><div class="dn">${dd.getDate()}</div><div class="dw">${WD[dd.getDay()]} ${MO[dd.getMonth()]}${d === today ? '  <i>Today</i>' : ''}${isWeekend(d) ? '' : ''}</div>
        <div class="ld${load > cap + 0.15 ? ' over' : ''}">${fmtHd(load)} / ${fmtHd(cap)} h</div></div>
        ${scale(cap, load, done, { small: true, span: Math.max(cap, load, 1) })}
        <div class="dchips" style="margin-top:10px">${ts.length ? ts.map(t => `<button class="tchip${t.st === 'done' ? ' done' : ''}" data-chip="${t.id}">${dot(t.s)}<span>${esc(SER[t.s].short)} ${esc(t.n)}</span><span class="h">${fmtHd(t.h)}h</span></button>`).join('') : '<span class="hint">Free day. Drop a test here</span>'}</div>
      </div>`;
    }
    h += `</div>`;
  }
  return h;
}

function seriesStats(k) {
  const ts = allTests().filter(t => t.s === k);
  const done = ts.filter(t => t.st === 'done');
  return { ts, done, n: ts.length, nd: done.length, h: ts.reduce((a, t) => a + t.h, 0), hd: done.reduce((a, t) => a + t.h, 0) };
}
function viewSeries() {
  let h = `<header class="top"><h1>Series</h1><p>Filled dot: 2027 series. Ring: 2026 practice.</p></header><div class="sheetbox"><ul class="list">`;
  for (const s of SERIES) {
    const st = seriesStats(s.k);
    const next = st.ts.filter(t => t.st === 'todo').sort((a, b) => a.d.localeCompare(b.d) || a.o - b.o)[0];
    h += `<li><button class="srow" data-series="${s.k}">${dot(s.k)}<div><div class="name">${esc(s.name)}</div><div class="sub">${next ? `Next: ${esc(next.n)}, ${fmtShort(next.d)}` : 'All done'}</div></div>
      <div class="num">${st.nd}/${st.n}<small>${fmtHd(st.hd)} of ${fmtHd(st.h)} h</small></div>
      <div class="bar s-${s.k}"><div class="pbar"><i style="width:${(st.nd / st.n) * 100}%"></i></div></div></button></li>`;
  }
  return h + `</ul></div><p class="fine">ESE mock pairs (Paper I + Paper II on one day) count as one entry.</p>`;
}

function subjectStats(key, isGS) {
  const ts = allTests().filter(t => isGS ? t.gs.includes(key) : t.sub.includes(key));
  const done = ts.filter(t => t.st === 'done');
  return { ts, n: ts.length, nd: done.length };
}
function viewSubjects() {
  let h = `<header class="top"><h1>Subjects</h1><p>Tests per subject across all series, plus a topic checklist.</p></header>`;
  h += `<section class="section"><h2>Technical and aptitude</h2><div class="sheetbox"><ul class="list">`;
  for (const k of Object.keys(TOPICS)) {
    const st = subjectStats(k, false);
    const tp = TOPICS[k], on = tp.filter(x => S.topics[k + '|' + x]).length;
    h += `<li><button class="srow" data-subject="${esc(k)}"><span></span><div><div class="name">${esc(SUBJECT_NAMES[k] || k)}</div><div class="sub">Topics revised ${on}/${tp.length}</div></div>
      <div class="num">${st.nd}/${st.n}<small>tests</small></div><div class="bar"><div class="pbar"><i style="width:${st.n ? (st.nd / st.n) * 100 : 0}%"></i></div></div></button></li>`;
  }
  h += `</ul></div></section>`;
  const gsKeys = [...new Set(SEED.tests.flatMap(t => t.gs))].sort();
  h += `<section class="section"><h2>ESE Paper I (GS)</h2><div class="sheetbox"><ul class="list">`;
  for (const k of gsKeys) {
    const st = subjectStats(k, true);
    h += `<li><button class="srow" data-gs="${esc(k)}"><span></span><div><div class="name">${esc(k)}</div></div>
      <div class="num">${st.nd}/${st.n}<small>tests</small></div><div class="bar"><div class="pbar"><i style="width:${st.n ? (st.nd / st.n) * 100 : 0}%"></i></div></div></button></li>`;
  }
  return h + `</ul></div></section>`;
}

function viewProgress() {
  const today = TODAY();
  const ts = allTests();
  const H = ts.reduce((a, t) => a + t.h, 0), Hd = ts.filter(t => t.st === 'done').reduce((a, t) => a + t.h, 0);
  const expected = ts.filter(t => t.d < today || (t.d === today && false)).reduce((a, t) => a + t.h, 0);
  const pctRaw = (Hd / H) * 100; const pct = pctRaw < 10 ? (Math.round(pctRaw * 10) / 10).toString() : Math.round(pctRaw).toString();
  const nd = ts.filter(t => t.st === 'done').length;
  const gap = Hd - expected;
  const pace = Math.abs(gap) < 0.3 ? '<b>On pace</b> with the plan.' : gap > 0 ? `<b>${fmtHd(gap)} h ahead</b> of the plan.` : `<b>${fmtHd(-gap)} h behind</b> the plan up to yesterday.`;
  // streak: consecutive days ending yesterday/today with ≥1 done
  const doneDays = new Set(ts.filter(t => t.doneAt).map(t => t.doneAt));
  let streak = 0, cur = doneDays.has(today) ? today : addDays(today, -1);
  while (doneDays.has(cur)) { streak++; cur = addDays(cur, -1); }

  let h = `<header class="top"><h1>Progress</h1></header>
    <div class="big">${pct}<small>%</small></div>
    <div class="pace">${fmtHd(Hd)} of ${fmtHd(H)} h of tests done. ${pace}</div>
    <div style="margin-top:14px">${scale(H, H, Hd, { span: H, major: 50, minor: 10, expected })}</div>
    <section class="section"><div class="sheetbox stats">
      <div><b>${nd}</b><span>of ${ts.length} done</span></div>
      <div><b>${ts.filter(t => t.st === 'todo' && t.d < today).length}</b><span>overdue</span></div>
      <div><b>${streak}</b><span>day streak</span></div>
    </div></section>`;

  // weekly chart
  const weeks = {};
  for (const t of ts) { const k = weekKey(t.d); weeks[k] = weeks[k] || { p: 0, d: 0 }; weeks[k].p += t.h; if (t.st === 'done') weeks[k].d += t.h; }
  const keys = Object.keys(weeks).sort();
  const W = 340, Hc = 150, pl = 22, pb = 22, bw = (W - pl) / keys.length;
  const maxv = Math.max(...keys.map(k => weeks[k].p), 1), sc = v => (v / maxv) * (Hc - pb - 8);
  let svg = `<svg viewBox="0 0 ${W} ${Hc}" role="img" aria-label="Hours planned and done per week">`;
  for (let g = 0; g <= maxv; g += 20) { const y = Hc - pb - sc(g); svg += `<line x1="${pl}" x2="${W}" y1="${y}" y2="${y}" stroke="var(--line)"/><text x="0" y="${y + 3}">${g}</text>`; }
  keys.forEach((k, i) => {
    const x = pl + i * bw + bw * 0.18, w = bw * 0.64, p = weeks[k].p, dn = weeks[k].d;
    svg += `<rect x="${x}" y="${Hc - pb - sc(p)}" width="${w}" height="${sc(p)}" rx="2" fill="none" stroke="var(--line2)"/>`;
    if (dn) svg += `<rect x="${x}" y="${Hc - pb - sc(dn)}" width="${w}" height="${sc(dn)}" rx="2" fill="var(--accent)"/>`;
    if (k <= today && addDays(k, 6) >= today) svg += `<line x1="${x + w / 2}" x2="${x + w / 2}" y1="${Hc - pb + 3}" y2="${Hc - pb + 7}" stroke="var(--text)" stroke-width="2"/>`;
    if (i % 2 === 0) svg += `<text x="${x + w / 2}" y="${Hc - 6}" text-anchor="middle">${fmtDM(k)}</text>`;
  });
  svg += `</svg>`;
  h += `<section class="section"><h2>Hours per week</h2><div class="sheetbox chart"><div class="key"><span><i style="background:var(--accent)"></i>Done</span><span><i style="border:1px solid var(--line2)"></i>Planned</span></div>${svg}</div></section>`;

  const mocks = ts.filter(t => t.k === 'mock' && t.st === 'todo' && t.d >= today).sort((a, b) => a.d.localeCompare(b.d) || a.o - b.o).slice(0, 5);
  if (mocks.length) h += `<section class="section"><h2>Next full-length papers</h2><div class="sheetbox"><ul class="list">${mocks.map(t => trow(t, true)).join('')}</ul></div></section>`;

  h += `<section class="section"><h2>Settings</h2><div class="sheetbox">
    <div class="setrow"><div class="l"><b>Appearance</b><span>Blueprint dark or vellum light</span></div>
      <div class="seg" role="group" aria-label="Theme"><button data-theme-set="dark" aria-pressed="${S.theme !== 'light'}">Dark</button><button data-theme-set="light" aria-pressed="${S.theme === 'light'}">Light</button></div></div>
    <button class="setrow" data-act="export"><div class="l"><b>Export backup</b><span>Save a .json file to Drive, Downloads or WhatsApp</span></div></button>
    <button class="setrow" data-act="import"><div class="l"><b>Import backup</b><span>Restore progress from a backup file</span></div></button>
    <button class="setrow danger" data-act="reset"><div class="l"><b>Reset progress</b><span>Clears ticks, scores and moves</span></div></button>
  </div>
  <p class="fine">Your progress is saved on this phone and kept when the app is updated. Export a backup before uninstalling or changing phones.</p></section>`;
  return h;
}

// ---------- sheets ----------
let sheetStack = [];
function openSheet(html, opts = {}) {
  const root = document.getElementById('sheet-root');
  const scrim = document.createElement('div'); scrim.className = 'scrim';
  const sh = document.createElement('div'); sh.className = 'sheet' + (opts.full ? ' full' : ''); sh.setAttribute('role', 'dialog'); sh.setAttribute('aria-modal', 'true');
  sh.innerHTML = (opts.full ? '' : '<div class="grab"></div>') + html;
  root.append(scrim, sh);
  requestAnimationFrame(() => { scrim.classList.add('in'); sh.classList.add('in'); });
  scrim.onclick = closeSheet;
  const entry = { scrim, sh, rerender: opts.rerender };
  sheetStack.push(entry);
  bindSheet(sh);
  return entry;
}
function closeSheet() {
  const e = sheetStack.pop(); if (!e) return;
  saveNow();
  e.scrim.classList.remove('in'); e.sh.classList.remove('in');
  setTimeout(() => { e.scrim.remove(); e.sh.remove(); }, 260);
}
function refreshSheets() { for (const e of sheetStack) if (e.rerender) { const y = e.sh.scrollTop; e.sh.innerHTML = (e.sh.classList.contains('full') ? '' : '<div class="grab"></div>') + e.rerender(); bindSheet(e.sh); e.sh.scrollTop = y; } }

function testSheetHtml(id) {
  const t = T(id), s = SER[t.s], today = TODAY();
  const start = t.act > today ? t.act : (t.d < today ? today : addDays(t.d, -3) < today ? today : addDays(t.d, -3));
  let picks = '';
  for (let i = 0; i < 21; i++) {
    const d = addDays(start, i);
    if (d > '2026-12-31') break;
    const ld = loadOf(d) + (d === t.d ? 0 : t.h), cap = capOf(d), dd = parse(d);
    picks += `<button class="dpick${d === t.d ? ' cur' : ''}${d < t.act ? ' no' : ''}${ld > cap + 0.15 ? ' heavy' : ''}" data-move="${d}"><small>${WD[dd.getDay()]}</small><b>${dd.getDate()}</b><em>${fmtHd(loadOf(d))}/${fmtHd(cap)}h</em></button>`;
  }
  return `<div>${dot(t.s)} <span style="color:var(--muted);font-size:13px;font-weight:600;margin-left:6px">${esc(s.name)}</span></div>
    <h3 style="margin-top:8px">${esc(t.n)}</h3>
    <div class="meta"><span>${KIND[t.k] || ''}</span><span>${fmtH(t.h)}</span><span>Planned ${fmtShort(t.d)}</span>${t.act > SEED.start ? `<span>Opens ${fmtShort(t.act)}, 6 PM</span>` : ''}</div>
    ${t.sub.length || t.gs.length ? `<div class="chips" style="margin-top:12px">${[...t.sub, ...t.gs].map(x => `<span class="chip-s">${esc(x)}</span>`).join('')}</div>` : ''}
    <div class="status3" role="group" aria-label="Status">
      <button data-st="todo" aria-pressed="${t.st === 'todo'}">To do</button>
      <button class="donebtn" data-st="done" aria-pressed="${t.st === 'done'}">Done</button>
      <button data-st="skip" aria-pressed="${t.st === 'skip'}">Skipped</button>
    </div>
    <label class="f" for="score">Score</label>
    <input class="field" id="score" data-field="score" inputmode="text" placeholder="e.g. 48 / 76" value="${esc(t.score || '')}" autocomplete="off">
    <label class="f" for="note">Notes</label>
    <textarea class="field" id="note" data-field="note" placeholder="Weak topics, silly mistakes, time taken">${esc(t.note || '')}</textarea>
    <label class="f">Move to another day</label>
    <div class="days">${picks}</div>
    <div class="row2"><input class="field" type="date" id="movedate" min="${t.act}" value="${t.d}"><button class="btn alt" data-move-pick="1">Move</button></div>`;
}
function openTest(id) { const e = openSheet(testSheetHtml(id), { rerender: () => testSheetHtml(id) }); e.sh.dataset.test = id; }

function listSheetHtml(title, sub, tests, filterKey) {
  const f = listFilter[filterKey] || 'all';
  const shown = tests.filter(t => f === 'all' ? true : f === 'left' ? t.st !== 'done' : t.st === 'done').sort((a, b) => a.d.localeCompare(b.d) || a.o - b.o);
  let body = '', curD = '';
  for (const t of shown) {
    if (t.d !== curD) { if (curD) body += '</ul></div>'; curD = t.d; body += `<div class="datehead">${fmtShort(t.d)}${t.d === TODAY() ? ', today' : ''}</div><div class="sheetbox"><ul class="list">`; }
    body += trow(t);
  }
  if (curD) body += '</ul></div>';
  if (!shown.length) body = `<div class="empty">${f === 'done' ? 'Nothing ticked off yet.' : 'Everything here is done.'}</div>`;
  return `<div class="sheet-top"><button class="back" data-close="1" aria-label="Back"><svg viewBox="0 0 24 24"><path d="M15 5l-7 7 7 7"/></svg></button><div class="tt"><b>${esc(title)}</b><span>${esc(sub)}</span></div></div>
    <div style="margin:14px 0 2px"><div class="seg" role="group" aria-label="Filter">
      <button data-filter="all" data-fk="${filterKey}" aria-pressed="${f === 'all'}">All</button><button data-filter="left" data-fk="${filterKey}" aria-pressed="${f === 'left'}">To do</button><button data-filter="done" data-fk="${filterKey}" aria-pressed="${f === 'done'}">Done</button></div></div>
    ${body}`;
}
const listFilter = {};
function openSeries(k) {
  const render = () => { const st = seriesStats(k); return listSheetHtml(SER[k].name, `${st.nd} of ${st.n} done, ${fmtHd(st.hd)} of ${fmtHd(st.h)} h`, st.ts, 's' + k); };
  openSheet(render(), { full: true, rerender: render });
}
function openSubject(k, isGS) {
  const render = () => {
    const st = subjectStats(k, isGS);
    let topics = '';
    if (!isGS && TOPICS[k]) {
      topics = `<div class="datehead">Topic checklist</div><div class="sheetbox">${TOPICS[k].map(x => { const on = !!S.topics[k + '|' + x]; return `<button class="topic${on ? ' on' : ''}" data-topic="${esc(k + '|' + x)}"><span class="box">${CHECK_SVG}</span><span>${esc(x)}</span></button>`; }).join('')}</div>`;
    }
    const lst = listSheetHtml(isGS ? k : (SUBJECT_NAMES[k] || k), `${st.nd} of ${st.n} tests done`, st.ts, (isGS ? 'g' : 'u') + k);
    const cut = lst.indexOf('<div style="margin:14px 0 2px">');
    return lst.slice(0, cut) + topics + '<div class="datehead" style="padding-top:20px">Tests</div>' + lst.slice(cut);
  };
  openSheet(render(), { full: true, rerender: render });
}

function bindSheet(sh) {
  sh.querySelectorAll('[data-close]').forEach(b => b.onclick = closeSheet);
  sh.querySelectorAll('[data-st]').forEach(b => b.onclick = () => { setStatus(sh.dataset.test, b.dataset.st); });
  sh.querySelectorAll('[data-field]').forEach(inp => inp.oninput = () => { S.tests[sh.dataset.test][inp.dataset.field] = inp.value.trim() || undefined; save(); });
  sh.querySelectorAll('[data-move]').forEach(b => b.onclick = () => { if (moveTest(sh.dataset.test, b.dataset.move)) closeSheet(); });
  const mp = sh.querySelector('[data-move-pick]');
  if (mp) mp.onclick = () => { const v = sh.querySelector('#movedate').value; if (v && moveTest(sh.dataset.test, v)) closeSheet(); };
  sh.querySelectorAll('[data-filter]').forEach(b => b.onclick = () => { listFilter[b.dataset.fk] = b.dataset.filter; refreshSheets(); });
  sh.querySelectorAll('[data-topic]').forEach(b => b.onclick = () => { const k = b.dataset.topic; S.topics[k] = !S.topics[k]; if (!S.topics[k]) delete S.topics[k]; vibrate(8); save(); refreshSheets(); render(); });
  bindRows(sh);
}
function bindRows(root) {
  root.querySelectorAll('[data-toggle]').forEach(b => b.onclick = e => { e.stopPropagation(); const id = b.dataset.toggle; setStatus(id, T(id).st === 'done' ? 'todo' : 'done'); });
  root.querySelectorAll('[data-open]').forEach(b => b.onclick = () => openTest(b.dataset.open));
}

// ---------- drag & drop (Plan) ----------
const drag = { id: null, timer: null, ghost: null, startX: 0, startY: 0, x: 0, y: 0, target: null, raf: 0, chip: null, moved: false };
function bindPlanDrag(root) {
  root.querySelectorAll('[data-chip]').forEach(chip => {
    chip.addEventListener('touchstart', e => beginPress(chip, e.touches[0].clientX, e.touches[0].clientY), { passive: true });
    chip.addEventListener('mousedown', e => { if (e.button === 0) beginPress(chip, e.clientX, e.clientY); });
    chip.addEventListener('click', e => { if (drag.suppressClick) { e.preventDefault(); drag.suppressClick = false; return; } openTest(chip.dataset.chip); });
    chip.addEventListener('contextmenu', e => e.preventDefault());
  });
}
function beginPress(chip, x, y) {
  cancelPress();
  drag.chip = chip; drag.startX = drag.x = x; drag.startY = drag.y = y;
  drag.timer = setTimeout(() => startDrag(), 380);
}
function cancelPress() { clearTimeout(drag.timer); drag.timer = null; }
function startDrag() {
  const chip = drag.chip; if (!chip) return;
  drag.id = chip.dataset.chip;
  vibrate(18);
  const g = chip.cloneNode(true); g.classList.add('ghost'); g.removeAttribute('data-chip');
  document.body.appendChild(g); drag.ghost = g;
  chip.classList.add('lifting');
  positionGhost();
  drag.raf = requestAnimationFrame(autoScroll);
}
function positionGhost() { if (drag.ghost) { drag.ghost.style.left = drag.x + 'px'; drag.ghost.style.top = drag.y + 'px'; } updateTarget(); }
function updateTarget() {
  const el = document.elementFromPoint(drag.x, drag.y);
  const day = el && el.closest ? el.closest('.day[data-date]') : null;
  if (drag.target && drag.target !== day) drag.target.classList.remove('drop', 'blocked');
  drag.target = day;
  if (day) { day.classList.add('drop'); day.classList.toggle('blocked', day.dataset.date < T(drag.id).act); }
}
function autoScroll() {
  if (!drag.id) return;
  const edge = 110, vh = window.innerHeight; let dy = 0;
  if (drag.y < edge) dy = -Math.ceil((edge - drag.y) / 6);
  else if (drag.y > vh - edge - 70) dy = Math.ceil((drag.y - (vh - edge - 70)) / 6);
  if (dy) { window.scrollBy(0, dy); updateTarget(); }
  drag.raf = requestAnimationFrame(autoScroll);
}
function endDrag(drop) {
  cancelPress();
  if (!drag.id) { drag.chip = null; return; }
  cancelAnimationFrame(drag.raf);
  const id = drag.id, target = drag.target;
  drag.ghost && drag.ghost.remove();
  if (target) target.classList.remove('drop', 'blocked');
  drag.chip && drag.chip.classList.remove('lifting');
  drag.id = null; drag.ghost = null; drag.target = null; drag.chip = null; drag.suppressClick = true;
  setTimeout(() => { drag.suppressClick = false; }, 400);
  if (drop && target) moveTest(id, target.dataset.date);
}
document.addEventListener('touchmove', e => {
  const t = e.touches[0]; if (!t) return;
  if (drag.id) { e.preventDefault(); drag.x = t.clientX; drag.y = t.clientY; positionGhost(); }
  else if (drag.timer && (Math.abs(t.clientX - drag.startX) > 8 || Math.abs(t.clientY - drag.startY) > 8)) { cancelPress(); drag.chip = null; }
}, { passive: false });
document.addEventListener('touchend', () => endDrag(true));
document.addEventListener('touchcancel', () => endDrag(false));
document.addEventListener('mousemove', e => {
  if (drag.id) { drag.x = e.clientX; drag.y = e.clientY; positionGhost(); }
  else if (drag.timer && (Math.abs(e.clientX - drag.startX) > 8 || Math.abs(e.clientY - drag.startY) > 8)) { cancelPress(); drag.chip = null; }
});
document.addEventListener('mouseup', () => endDrag(true));

// ---------- main render ----------
function render() {
  const view = document.getElementById('view');
  const html = tab === 'today' ? viewToday() : tab === 'plan' ? viewPlan() : tab === 'series' ? viewSeries() : tab === 'subjects' ? viewSubjects() : viewProgress();
  const y = window.scrollY;
  view.innerHTML = html;
  window.scrollTo(0, y);
  document.querySelectorAll('.tab').forEach(b => b.setAttribute('aria-selected', String(b.dataset.tab === tab)));
  bindRows(view);
  if (tab === 'plan') {
    bindPlanDrag(view);
    const j = view.querySelector('[data-jump]'); if (j) j.onclick = () => jumpToday(true);
  }
  view.querySelectorAll('[data-series]').forEach(b => b.onclick = () => openSeries(b.dataset.series));
  view.querySelectorAll('[data-subject]').forEach(b => b.onclick = () => openSubject(b.dataset.subject, false));
  view.querySelectorAll('[data-gs]').forEach(b => b.onclick = () => openSubject(b.dataset.gs, true));
  view.querySelectorAll('[data-theme-set]').forEach(b => b.onclick = () => { S.theme = b.dataset.themeSet; applyTheme(); save(); render(); });
  view.querySelectorAll('[data-act]').forEach(b => b.onclick = () => actions[b.dataset.act]());
  refreshSheets();
}
function jumpToday(smooth) {
  const el = document.getElementById('day-' + TODAY());
  if (el) window.scrollTo({ top: el.getBoundingClientRect().top + window.scrollY - 70, behavior: smooth ? 'smooth' : 'auto' });
}
function setTab(t) {
  if (t === tab) { if (t === 'plan') jumpToday(true); else window.scrollTo({ top: 0, behavior: 'smooth' }); return; }
  scrollPos[tab] = window.scrollY; tab = t; render();
  if (t === 'plan' && scrollPos.plan == null) jumpToday(false); else window.scrollTo(0, scrollPos[t] || 0);
}
document.querySelectorAll('.tab').forEach(b => b.onclick = () => setTab(b.dataset.tab));

function applyTheme() {
  document.documentElement.dataset.theme = S.theme === 'light' ? 'light' : 'dark';
  try { Native && Native.setTheme && Native.setTheme(S.theme === 'light' ? 'light' : 'dark'); } catch (e) { }
}

// ---------- backup ----------
const actions = {
  export() {
    const name = `test-tracker-backup-${TODAY()}.json`;
    const data = JSON.stringify({ app: 'test-series-tracker', exported: new Date().toISOString(), state: S }, null, 1);
    if (Native && Native.exportBackup) { Native.exportBackup(data, name); return; }
    const a = document.createElement('a'); a.href = URL.createObjectURL(new Blob([data], { type: 'application/json' })); a.download = name; a.click();
    toast('Backup saved');
  },
  import() {
    if (Native && Native.importBackup) { Native.importBackup(); return; }
    const inp = document.getElementById('file-in'); inp.value = ''; inp.onchange = () => { const f = inp.files[0]; if (f) f.text().then(window.__onImport); }; inp.click();
  },
  reset() {
    const html = `<h3>Reset all progress?</h3><p style="color:var(--muted);margin:10px 0 0">Ticks, scores, notes, topic checks and moved dates go back to the original plan. Export a backup first if you might want them later.</p>
      <div class="row2" style="margin-top:22px"><button class="btn alt" data-close="1" style="flex:1">Keep my progress</button><button class="btn" id="do-reset" style="flex:1;background:var(--danger);color:#fff">Reset</button></div>`;
    const e = openSheet(html);
    e.sh.querySelector('#do-reset').onclick = () => { const theme = S.theme; S = freshState(); S.theme = theme; S = (store.save(JSON.stringify(S)), loadState()); saveNow(); closeSheet(); render(); toast('Progress reset'); };
  },
};
window.__onImport = text => {
  try {
    const obj = JSON.parse(text); const st = obj.state || obj;
    if (!st || !st.tests || typeof st.tests !== 'object') throw new Error('bad');
    store.save(JSON.stringify(st)); S = loadState(); saveNow(); applyTheme(); render();
    toast(`Backup restored: ${Object.values(S.tests).filter(x => x.st === 'done').length} tests done`);
  } catch (e) { toast('That file is not a tracker backup. Pick the .json you exported.'); }
};
window.__onExported = ok => toast(ok ? 'Backup saved' : 'Backup not saved');

// ---------- back button (Android) ----------
window.__onBack = () => {
  if (sheetStack.length) { closeSheet(); return true; }
  if (tab !== 'today') { setTab('today'); return true; }
  return false;
};
document.addEventListener('visibilitychange', () => { if (document.hidden) saveNow(); else render(); });

// ---------- start ----------
applyTheme();
render();
saveNow();
})();
