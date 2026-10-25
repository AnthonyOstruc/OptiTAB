"""Contrôles de présence et de cohérence des figures du CM1."""
from pathlib import Path
from math import isclose
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
        if c.numero in [13,15,16,17,18]:check(bool(e.figure),f'presence necessaire {c.numero}.{i}')
    for co in c.cours:
        for m in re.findall(r'@FIG:([^@]+)@',co):check(m in FIGURES,f'cours {c.numero} figure {m}')
# Demi-droites : points et solutions dans les bornes.
for name,data in META.items():
    if data.get('type')=='droite':
        lo,hi=data['bornes']
        for v in data['points']+data['solutions']:
            check(lo-1e-9<=v<=hi+1e-9,f'{name} valeur {v} dans les bornes')
# Symétries : images correctes et dans la grille.
for name,data in META.items():
    if data.get('type')=='symetrie':
        o,v=data['axe'];gw,gh=data['grille']
        for (x,y),(u,w) in zip(data['originaux'],data['images']):
            if o=='v':ok=isclose(u,2*v-x) and isclose(w,y)
            else:ok=isclose(u,x) and isclose(w,2*v-y)
            check(ok,f'{name} image de ({x},{y})')
            check(0<=u<=gw and 0<=w<=gh,f'{name} image dans la grille')
# Secteurs : tour complet.
for name,data in META.items():
    if data.get('type')=='secteurs':check(sum(data['angles'])==360,name+' tour complet')
# Valeurs des diagrammes citées dans les corrigés.
check(META['don-4']['valeurs']==[8,12,10,18,14] and max(META['don-4']['valeurs'])==18,'don-4 valeurs')
check(META['don-5']['valeurs'][1]==12 and max(META['don-5']['valeurs'])==21,'don-5 valeurs')
check(META['don-6']['valeurs']==[7,9,5,4],'don-6 valeurs')
check(META['don-7']['donnees']==[(1,1),(2,2),(4,3),(6,5)],'don-7 points')
vals=META['don-9']['valeurs'];check(max(vals)==22 and min(vals)==4 and vals.index(22)==6 and vals.index(4)==0,'don-9 extremes')
check(META['don-10']['valeurs']==[8,12,6],'don-10 valeurs')
v13=META['don-13']['valeurs'];check(v13[3]==6 and v13[4]<10<v13[5] and v13[5]==13,'don-13 seuil des 10 cm')
check(META['don-14']['valeurs']==[7,12,18,10] and META['don-14']['second']==[3,14,24,9],'don-14 deux villes')
# Bandes de fractions.
check(META['frac-2']['parts']==5 and META['frac-2']['sol']==2,'frac-2')
check(META['frac-12']['parts']==20 and META['frac-12']['sol']==5,'frac-12')
# Urnes et roues : compositions annoncées.
check(META['pro-7']['items'].count('R')==1 and META['pro-7']['items'].count('B')==3,'pro-7 urne')
check(META['pro-9']['items'].count('R')==5 and META['pro-9']['items'].count('B')==2,'pro-9 urne')
it=META['pro-15']['items'];check(it.count('R')==2 and it.count('V')==3 and it.count('N')==5,'pro-15 urne')
check(META['pro-8']['angles']==[180,120,60],'pro-8 angles')
check(META['pro-13']['angles']==[45]*8,'pro-13 angles')
# Assemblages de cubes.
check(META['sol-9']['cubes']==10,'sol-9 dix cubes')
check(META['sol-12']['cubes']==7,'sol-12 sept cubes')
# Patrons du cube : six cases, en croix pour les patrons complets.
croix={(1,0),(1,1),(0,1),(2,1),(1,2),(1,3)}
for name in ['sol-7','sol-15','cours-patron']:
    check(set(map(tuple,META[name]['cells']))==croix,name+' croix de six cases')
def carre2x2(cells):
    s=set(map(tuple,cells))
    return any((c,r) in s and (c+1,r) in s and (c,r+1) in s and (c+1,r+1) in s for (c,r) in s)
nets=META['sol-6']['nets']
check(len(nets)==3 and all(len(n)==6 for n in nets),'sol-6 trois dispositions de six')
check(not carre2x2(nets[0]) and not carre2x2(nets[1]),'sol-6 patrons valides sans bloc 2x2')
check(carre2x2(nets[2]),'sol-6 contre-exemple avec bloc 2x2')
# Scripts : exécutions conformes aux corrigés.
from donnees_scripts import verifier_scripts,executer,SCRIPTS
check(verifier_scripts()==10,'scripts executes')
check(executer(SCRIPTS[9])['trace'][-1]==(0,-1),'sol-13 arrivee')
check(executer(SCRIPTS[10])['trace'][-1]==(1,2),'sol-14 arrivee')
check(executer(SCRIPTS[1],6)['sorties'][-1]==32 and executer(SCRIPTS[1],10)['sorties'][-1]==48,'prog-4 sorties')
# Les constructions annoncées en vert portent bien une solution conditionnelle.
avec_solution=['frac-2','frac-12','fd-2','fd-9','dec9-6','hor-2','geo-2','geo-6','geo-7','geo-10','geo-11','geo-12','geo-13','geo-14','geo-15','tri-2','tri-3','tri-6','tri-7','tri-8','tri-9','tri-10','tri-11','tri-15','sym-4','sym-5','sym-6','sym-7','sym-9','sym-10','sym-11','sym-12','sym-13','sym-14','sym-15','sol-8','sol-11','sol-14','sol-15','don-6','don-10','pro-5','pro-6','num-8']
for name in avec_solution:
    if name=='num-8':check(r'\geoSolution' not in FIGURES[name]['tex'],'num-8 sans solution inutile')
    else:check(r'\geoSolution' in FIGURES[name]['tex'],name+' porte sa solution')
# Angles : ouvertures cohérentes avec les classements des corrigés.
m=META['aa-6']['mesures'];check(m[1]<m[0]<m[2],'aa-6 ordre des angles')
m=META['aa-10']['mesures'];check(m[0]==m[2] and m[1]<m[0]<m[3],'aa-10 calque sur E')
check(META['aa-9']['aires']==[5,9],'aa-9 aires')
check(META['aa-13']['aires']==[4,16],'aa-13 quadruple')
check(META['aa-15']['aires']==[9,9],'aa-15 aires egales')
check(META['cours-produit'] is not None and META['motifs-14']['etapes']==[5,9,13],'motifs-14 etapes')
check(META['motifs-13']['etapes']==[1,2,3],'motifs-13 etapes')
(ROOT/'build').mkdir(exist_ok=True)
r={'controles_figures':count,'erreurs':errors,'details':details}
(ROOT/'build/controles-figures.json').write_text(json.dumps(r,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps({k:v for k,v in r.items() if k!='details'},ensure_ascii=True,indent=2))
assert not errors
