"""Contrôles de présence et de cohérence des figures du CM2."""
from pathlib import Path
from math import isclose,hypot
import importlib,json,re
from modele import CHAPITRES,FIGURES
from generer_figures import write_all,META
ROOT=Path(__file__).resolve().parent
for p in sorted(ROOT.glob('contenu_*.py')):importlib.import_module(p.stem)
import tempfile
with tempfile.TemporaryDirectory() as d:write_all(Path(d))
count=0;errors=[];details=[]
def check(ok,label):
    global count
    count+=1
    if not ok:errors.append(label)
    details.append({'controle':label,'reussi':bool(ok)})
# Présence des figures demandées par les textes.
for c in CHAPITRES:
    for i,e in enumerate(c.exercices,1):
        if e.figure:check(e.figure in FIGURES,f'figure {c.numero}.{i}')
        if c.numero in [15,16,17,18]:check(bool(e.figure),f'presence necessaire {c.numero}.{i}')
    for co in c.cours:
        for m in re.findall(r'@FIG:([^@]+)@',co):check(m in FIGURES,f'cours {c.numero} figure {m}')
check('preuve-fractions' in FIGURES,'figure des preuves')
# Demi-droites : points et solutions dans les bornes.
for name,data in META.items():
    if data.get('type')=='droite':
        lo,hi=data['bornes']
        for v in data['points']+data['solutions']:
            check(lo-1e-9<=v<=hi+1e-9,f'{name} valeur {v} dans les bornes')
# Symétries d'axe horizontal ou vertical.
for name,data in META.items():
    if data.get('type')=='symetrie':
        o,v=data['axe'];gw,gh=data['grille']
        for (x,y),(u,w) in zip(data['originaux'],data['images']):
            ok=(isclose(u,2*v-x) and isclose(w,y)) if o=='v' else (isclose(u,x) and isclose(w,2*v-y))
            check(ok,f'{name} image de ({x},{y})')
            check(0<=u<=gw and 0<=w<=gh,f'{name} image dans la grille')
# Symétries d'axe diagonal : les coordonnées s'échangent.
for name,data in META.items():
    if data.get('type')=='symdiag':
        g=data['grille']
        for (x,y),(u,w) in zip(data['originaux'],data['images']):
            check((u,w)==(y,x),f'{name} échange des coordonnées ({x},{y})')
            check(0<=u<=g and 0<=w<=g,f'{name} image dans la grille')
check(META['sym-4']['images']==[(1,3),(2,5),(0,4)],'sym-4 images citées au corrigé')
check(META['sym-5']['images'][-2:]==[(0,2),(2,3)],'sym-5 images citées au corrigé')
# Secteurs : tour complet.
for name,data in META.items():
    if data.get('type')=='secteurs':check(isclose(sum(data['angles']),360),name+' tour complet')
check(META['pro-4']['angles']==[180,90,45,45],'pro-4 roue B inégale')
check([round(a) for a in META['don-5']['angles']]==[180,90,90],'don-5 moitié, quart, quart')
# Données citées dans les corrigés.
check(META['don-3']['valeurs'][0]==15 and META['don-3']['valeurs'][3]==35 and max(META['don-3']['valeurs'])==35,'don-3 lundi et jeudi')
v=META['don-4']['valeurs'];check(v[0]==3 and v[6]==23 and min(v)==3 and max(v)==23,'don-4 extrêmes')
check(META['don-6']['valeurs']==[12,9,5,4],'don-6 effectifs')
d=META['don-8']['donnees'];ecarts=[d[k+1][1]-d[k][1] for k in range(len(d)-1)]
check(d[1][1]==14 and d[4][1]==38 and max(ecarts)==12 and ecarts.index(12)==2,'don-8 plus forte croissance entre 3 et 4')
v=META['don-10']['valeurs'];check(v[2]==48 and v[-1]==76,'don-10 cumul midi et fermeture')
check(META['don-11']['valeurs']==[22,26,24],'don-11 valeurs du tableau')
# Urnes, arbres et tableaux de probabilités.
it=META['pro-2']['items'];check(it.count('R')==2 and it.count('V')==3 and it.count('N')==5,'pro-2 composition')
check(META['pro-7']['issues']==4 and META['pro-11']['issues']==4 and META['cours-arbre']['issues']==4,'arbres à quatre issues')
check(META['pro-8']['aires']==[6],'pro-8 six sommes égales à 7')
# Assemblages de cubes.
check(META['sol-10']['cubes']==14,'sol-10 quatorze cubes')
check(META['sol-11']['cubes']==7,'sol-11 sept cubes')
check(META['sol-12']['cubes']==20,'sol-12 vingt cubes')
check(META['sol-15']['cubes']==27,'sol-15 cube 3 sur 3 sur 3')
# Patrons du cube.
croix={(1,0),(1,1),(0,1),(2,1),(1,2),(1,3)}
for name in ['sol-6','sol-8']:check(set(map(tuple,META[name]['cells']))==croix,name+' croix de six cases')
def carre2x2(cells):
    s=set(map(tuple,cells))
    return any((c,r) in s and (c+1,r) in s and (c,r+1) in s and (c+1,r+1) in s for (c,r) in s)
nets=META['sol-5']['nets']
check(len(nets)==3 and all(len(n)==6 for n in nets),'sol-5 trois dispositions')
check(not carre2x2(nets[0]) and not carre2x2(nets[1]) and carre2x2(nets[2]),'sol-5 deux patrons et un contre-exemple')
# Hexagone régulier : six côtés égaux au rayon.
pts=META['tri-9']['points']
cotes=[hypot(pts[(k+1)%6][0]-pts[k][0],pts[(k+1)%6][1]-pts[k][1]) for k in range(6)]
check(all(isclose(c,1.8,abs_tol=1e-9) for c in cotes),'tri-9 côté égal au rayon')
for name in ['tri-3','geo-6']:
    p=META[name]['points']
    check(abs(p[0][1]-p[1][1])<1e-9,name+' base horizontale')
p=META['tri-3']['points'];check(isclose(hypot(p[2][0],p[2][1]),hypot(p[2][0]-p[1][0],p[2][1]),rel_tol=1e-6),'tri-3 isocèle')
p=META['geo-6']['points'];check(isclose(hypot(p[2][0],p[2][1]),hypot(p[2][0]-p[1][0],p[2][1]),rel_tol=1e-6),'geo-6 isocèle en G')
# Angles cités dans les corrigés.
check(META['ang-2']['mesures'][1]<META['ang-2']['mesures'][0]<META['ang-2']['mesures'][2],'ang-2 ordre B<A<C')
m=META['ang-10']['mesures'];check(m[0]<90==m[1]<m[2]<m[3]<180,'ang-10 classement autour de l’angle droit')
check(sum(META['ang-6']['mesures'])==100 and sum(META['ang-7']['mesures'])==70,'ang-6 et ang-7 sommes')
check(sum(META['ang-9']['mesures'])==135 and sum(META['ang-13']['mesures'])==180,'ang-9 et ang-13')
m=META['ang-15']['mesures'];check(m[0]<m[1],'ang-15 E plus petit que F')
check(META['aire-1']['aires']==[28] and META['aire-5']['aires']==[100] and META['cours-dm2']['aires']==[100],'aires citées')
check(META['motifs-11']['etapes']==[5,9,13],'motifs-11 étapes')
# Scripts : exécutions conformes aux corrigés.
from donnees_scripts import verifier_scripts,executer,SCRIPTS
check(verifier_scripts()==10,'scripts exécutés')
check(executer(SCRIPTS[7])['trace'][-1]==(5,0),'sol-13 arrivée au but')
check(max(y for _,y in executer(SCRIPTS[7])['trace'])<=3,'sol-13 chemin dans la grille')
s=executer(SCRIPTS[9]);check(s['trace'][-1]==(0,0) and s['cap']=='S','sol-14 retour au départ, tourné vers le bas')
check(executer(SCRIPTS[1],6)['sorties'][-1]==29 and executer(SCRIPTS[1],10)['sorties'][-1]==45,'prog-2 sorties')
# Les figures annoncées « en vert » portent bien une solution conditionnelle.
for name in ['frac-2','fd-7','dec-10','ang-3','ang-6','ang-7','ang-8','ang-9','ang-14','geo-2','geo-3','geo-5','geo-6','geo-10','geo-12','geo-14','tri-3','tri-6','tri-7','tri-8','tri-9','tri-11','tri-12','sym-2','sym-3','sym-4','sym-5','sym-6','sym-7','sym-9','sym-10','sym-11','sym-12','sym-13','sym-14','sym-15','sol-8','sol-9','sol-14','don-6','don-11']:
    check(r'\geoSolution' in FIGURES[name]['tex'],name+' porte sa solution')
(ROOT/'build').mkdir(exist_ok=True)
r={'controles_figures':count,'erreurs':errors,'details':details}
(ROOT/'build/controles-figures.json').write_text(json.dumps(r,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps({k:v for k,v in r.items() if k!='details'},ensure_ascii=True,indent=2))
assert not errors
