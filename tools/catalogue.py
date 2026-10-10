import datetime as dt, json, collections

D = lambda s: dt.date(2026, int(s.split('-')[1]), int(s.split('-')[0]))
START, END = dt.date(2026, 10, 8), dt.date(2026, 12, 15)

# ---------------- Test catalogue ----------------
T = {}  # id -> dict(label, hrs, act, series, practice)
def add(i, label, hrs, act, series, practice=False):
    T[i] = dict(id=i, label=label, hrs=hrs, act=act, series=series, practice=practice)

# ACE GATE-27 / GATE-26 topic + subject grand + multi
gate_topic = {1:'Maths-1',2:'Maths-2',3:'Geotech-1',4:'Geotech-2',5:'SA-1',6:'SA-2',7:'RCC',8:'Steel',
              9:'SOM-1',10:'SOM-2',11:'Fluid Mech',12:'Hydraulics',13:'Hydrology',14:'Irrigation',
              15:'Env-1',16:'Env-2',17:'Transport-1',18:'Transport-2',19:'Geomatics',20:'Engg Mech',
              21:'Constr Mat & Mgmt',22:'Verbal',23:'Quant',24:'Analytical'}
g27_topic_act = {**{k:'13-04-2026' for k in (1,2,3,4)}, **{k:'21-04-2026' for k in (5,6,7,8)},
                 **{k:'28-04-2026' for k in (9,10,11,12)}, 13:'05-05-2026',14:'05-05-2026',
                 15:'12-05-2026',16:'12-05-2026',17:'19-05-2026',18:'19-05-2026',19:'26-05-2026',20:'26-05-2026',
                 21:'02-06-2026',22:'02-06-2026',23:'02-06-2026',24:'02-06-2026'}
grand = {25:'Maths',26:'EM+SOM',27:'Env',28:'SA',29:'RCC+Steel',30:'Geotech',31:'Hydrology+Irrigation',
         32:'FM+Hydraulics',33:'Transport',34:'Geomatics',35:'Constr Mat & CPM',36:'General Aptitude'}
multi = {43:'EM+SOM+SA',44:'Geotech+FM',45:'CM+RCC+Steel',46:'Hydro+Irr+Env',47:'Transport+Geomatics',48:'Maths+GA'}
for k,v in gate_topic.items():
    add(f'G27-T{k:02d}', f'ACE GATE-27 T{k:02d} {v}', 0.7, D(g27_topic_act[k]), 'ACE GATE-27')
    add(f'G26-T{k:02d}', f'ACE GATE-26 T{k:02d} {v}', 0.7, D('25-03-2026'), 'ACE GATE-26', True)
g27_grand_act = {25:'09-06-2026',26:'09-06-2026',27:'16-06-2026',28:'16-06-2026',29:'23-06-2026',30:'23-06-2026',
                 31:'30-06-2026',32:'30-06-2026',33:'07-07-2026',34:'07-07-2026',35:'14-07-2026',36:'21-07-2026'}
for k,v in grand.items():
    add(f'G27-T{k}', f'ACE GATE-27 T{k} {v} (grand)', 1.4, D(g27_grand_act[k]), 'ACE GATE-27')
    add(f'G26-T{k}', f'ACE GATE-26 T{k} {v} (grand)', 1.4, D('25-03-2026'), 'ACE GATE-26', True)
g27_multi_act = {43:'29-09-2026',44:'29-09-2026',45:'06-10-2026',46:'06-10-2026',47:'13-10-2026',48:'13-10-2026'}
for k,v in multi.items():
    add(f'G27-T{k}', f'ACE GATE-27 T{k} {v} (multi)', 1.4, D(g27_multi_act[k]), 'ACE GATE-27')
    k26 = k-6
    add(f'G26-T{k26}', f'ACE GATE-26 T{k26} {v} (multi)', 1.4, D('01-04-2026'), 'ACE GATE-26', True)
g27_flt_act = {1:'04-08-2026',2:'11-08-2026',3:'18-08-2026',4:'25-08-2026',5:'01-09-2026',6:'08-09-2026',
               7:'27-10-2026',8:'03-11-2026',9:'10-11-2026',10:'17-11-2026'}
for k,a in g27_flt_act.items():
    add(f'G27-FLT{k}', f'ACE GATE-27 Full Mock-{k} (T{36+k if k<=6 else 42+k})', 3.0, D(a), 'ACE GATE-27')
for k in range(1,13):
    add(f'G26-FLT{k}', f'ACE GATE-26 Full Mock-{k} (T{42+k})', 3.0, D('10-04-2026'), 'ACE GATE-26', True)
add('G27-ADD1', 'ACE GATE-27 Add-01 (new syllabus)', 0.7, D('08-09-2026'), 'ACE GATE-27')
add('G27-ADD2', 'ACE GATE-27 Add-02 (new syllabus)', 0.7, D('10-09-2026'), 'ACE GATE-27')
add('G27-ADD3', 'ACE GATE-27 Add-03 (new syllabus)', 0.7, D('12-09-2026'), 'ACE GATE-27')

# ACE ESE-27 / ESE-26 subject tests
ace_ese = {1:('Transportation',1),2:('Solid Mechanics',1),3:('FM, Hyd Machines & Hydropower',1),4:('Engg Maths',0.67),
           5:('Environmental',1),6:('Energy & Environment',0.67),7:('Structural Analysis',1),8:('Design, Drawing & Safety',0.67),
           9:('Geotech & Foundation',1),10:('Ethics',0.67),11:('Concrete & Masonry',1),12:('ICT',0.67),
           13:('Surveying & Geology',1),14:('Engg Aptitude',0.67),15:('Steel Structures',1),16:('Material Science',0.67),
           17:('Hydrology & WRE',1),18:('Standards & Quality',0.67),19:('Building Materials',1),20:('Project Mgmt',0.67),
           21:('Constr Practice & Mgmt',1),22:('Current Issues',0.67)}
ace_dates = ['01-07-2026','10-07-2026','17-07-2026','24-07-2026','31-07-2026','07-08-2026','14-08-2026','21-08-2026','28-08-2026','04-09-2026','11-09-2026']
for k,(v,h) in ace_ese.items():
    add(f'A27-T{k:02d}', f'ACE ESE-27 T{k:02d} {v}', h, D(ace_dates[(k-1)//2]), 'ACE ESE-27')
    add(f'A26-T{k:02d}', f'ACE ESE-26 T{k:02d} {v}', h, D('01-05-2026'), 'ACE ESE-26', True)
ace_multi = {27:('FM+Surveying',1),28:('Energy+Aptitude',0.67),29:('SOM+CPM+WRE',1),30:('Maths+Current Issues',0.67),
             31:('Steel+Transport+Geotech',1),32:('Project Mgmt+Material Sci',0.67),33:('Env+SA',1),34:('ICT+Design/Safety',0.67),
             35:('BM+RCC+Hydrology',1),36:('Ethics+Standards',0.67)}
am_act = {27:'09-10-2026',28:'09-10-2026',29:'16-10-2026',30:'16-10-2026',31:'23-10-2026',32:'23-10-2026',33:'30-10-2026',34:'30-10-2026',35:'06-11-2026',36:'06-11-2026'}
for k,(v,h) in ace_multi.items():
    add(f'A27-T{k}', f'ACE ESE-27 T{k} {v} (multi)', h, D(am_act[k]), 'ACE ESE-27')
a27_mock_act = {1:'18-09-2026',2:'25-09-2026',3:'24-11-2026',4:'01-12-2026',5:'08-12-2026',6:'15-12-2026'}
mock_tno = {1:(23,24),2:(25,26),3:(37,38),4:(39,40),5:(41,42),6:(43,44)}
for k,a in a27_mock_act.items():
    p1,p2 = mock_tno[k]
    add(f'A27-M{k}', f'ACE ESE-27 Mock-{k} P-I + P-II (T{p1}+T{p2})', 5.0, D(a), 'ACE ESE-27')
for k in range(1,5):
    add(f'A26-M{k}', f'ACE ESE-26 Mock-{k} P-I + P-II (T{21+2*k}+T{22+2*k})', 5.0, D('10-05-2026'), 'ACE ESE-26', True)

# MADE EASY ESE-27 / ESE-26 (structure per MADE EASY CE schedule: 22 subject tests + 12 full syllabus)
me_sub = {1:('Solid Mechanics',0.75),2:('Engg Aptitude',0.5),3:('Environmental',0.75),4:('Engg Maths',0.5),5:('Structural Analysis',0.75),
          6:('Design, Drawing & Safety',0.5),7:('Hydrology & WRE',0.75),8:('Energy & Environment',0.5),9:('Concrete & Masonry',0.75),
          10:('Project Mgmt',0.5),11:('FM, Hyd Machines & Hydropower',0.75),12:('Material Science',0.5),13:('Steel Structures',0.75),
          14:('ICT',0.5),15:('Geotech & Foundation',0.75),16:('Ethics',0.5),17:('Constr Practice & Mgmt',0.75),18:('Standards & Quality',0.5),
          19:('Transportation',0.75),20:('Current Issues',0.5),21:('Building Materials',0.75),22:('Surveying & Geology',0.75)}
for k,(v,h) in me_sub.items():
    add(f'M27-S{k:02d}', f'MADE EASY ESE-27 Test-{k} {v}', h, D('15-08-2026'), 'ME ESE-27')
    add(f'M26-S{k:02d}', f'MADE EASY ESE-26 Test-{k} {v}', h, D('01-01-2026'), 'ME ESE-26', True)
for k in (1,3,5,7):   # FST pairs 1-2,3-4,5-6,7-8 (Tests 23-30)
    add(f'M27-F{k}', f'MADE EASY ESE-27 Full Syllabus {k}+{k+1} (P-I + P-II)', 5.0, D('15-09-2026'), 'ME ESE-27')
for k in (1,3,5):     # ME-26 P-I and P-II taken on separate days
    add(f'M26-F{k}', f'MADE EASY ESE-26 Full Syllabus-{k} (P-I, GS)', 2.0, D('01-01-2026'), 'ME ESE-26', True)
    add(f'M26-F{k+1}', f'MADE EASY ESE-26 Full Syllabus-{k+1} (P-II, Technical)', 3.0, D('01-01-2026'), 'ME ESE-26', True)
for k in (7,9,11):
    add(f'M26-F{k}', f'MADE EASY ESE-26 Full Syllabus {k}+{k+1} (P-I + P-II)', 5.0, D('01-01-2026'), 'ME ESE-26', True)

