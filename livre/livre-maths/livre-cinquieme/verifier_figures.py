"""Contrôles de présence et de cohérence des dessins à partir de leurs données."""
from pathlib import Path
from math import hypot,atan2,degrees,acos,isclose
import importlib,json
from modele import CHAPITRES,FIGURES
from generer_figures import write_all,META
ROOT=Path(__file__).resolve().parent
for p in sorted(ROOT.glob('contenu_*.py')):importlib.import_module(p.stem)
# Les fichiers sont comparés, pas modifiés, par ce vérificateur.
import tempfile
with tempfile.TemporaryDirectory() as d:write_all(Path(d))
count=0;errors=[];details=[]
def check(ok,label):
    global count
    count+=1
    if not ok:errors.append(label)
    details.append({'controle':label,'reussi':bool(ok)})
for c in CHAPITRES:
    for i,e in enumerate(c.exercices,1):
        if e.figure:check(e.figure in FIGURES,f'figure {c.numero}.{i}')
        if c.numero in [12,13,14,15,16,17,20]:check(bool(e.figure),f'presence necessaire {c.numero}.{i}')
for name,data in META.items():
    check(name in FIGURES,name+' defini')
    typ=data['type']
    if typ in ['repere','symetrie']:
        (x0,x1),(y0,y1)=data['bornes']
        for lab,x,y in data['points']+data['solutions']:
            check(x0<=x<=x1 and y0<=y<=y1,name+' point '+lab+' dans le repere')
    if typ=='symetrie':
        for a,b in zip(data['originaux'],data['images']):
            _,x,y=a;_,u,v=b;kind=data['nature'];cx,cy=data['centre']
            if kind=='centrale':ok=isclose((x+u)/2,cx) and isclose((y+v)/2,cy)
            elif kind=='verticale':ok=isclose(x,-u) and isclose(y,v)
            elif kind=='horizontale':ok=isclose(x,u) and isclose(y,-v)
            else:ok=isclose(x,v) and isclose(y,u)
            check(ok,name+' definition de la symetrie '+a[0])
    if typ=='secteurs':check(sum(data['angles'])==360,name+' tour complet')
    if typ in ['parallelogramme','losange']:
        a,b,c,d=data['points']
        check(all(isclose(a[k]+c[k],b[k]+d[k]) for k in [0,1]),name+' diagonales meme milieu')
        if typ=='losange':
            sides=[hypot(data['points'][(i+1)%4][0]-p[0],data['points'][(i+1)%4][1]-p[1]) for i,p in enumerate(data['points'])]
            check(max(sides)-min(sides)<1e-8,name+' quatre cotes egaux')
    if typ=='triangle':
        a,b,c=data['points'];det=(b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
        check(abs(det)>1e-8,name+' non aplati')
        if 'orthocentre' in data:
            h=data['orthocentre'];pts=data['points']
            for i,o in enumerate(pts):
                u=(h[0]-o[0],h[1]-o[1]);a=pts[(i+1)%3];b=pts[(i+2)%3];v=(b[0]-a[0],b[1]-a[1])
                check(abs(u[0]*v[0]+u[1]*v[1])<1e-8,name+' hauteur '+str(i))
def length(name,i,j):
    p=META[name]['points'];return hypot(p[i][0]-p[j][0],p[i][1]-p[j][1])
def angle(name,i):
    p=META[name]['points'];a=p[(i+1)%3];o=p[i];b=p[(i+2)%3]
    u=(a[0]-o[0],a[1]-o[1]);v=(b[0]-o[0],b[1]-o[1])
    return degrees(acos(max(-1,min(1,(u[0]*v[0]+u[1]*v[1])/(hypot(*u)*hypot(*v))))))
for name,i,expected in [('tri-1',0,48),('tri-1',1,67),('tri-1',2,65),('tri-2',2,44),('tri-2',0,68),('tri-6',0,60),('tri-7',0,50),('tri-7',1,60),('tri-12',0,90)]:
    check(abs(angle(name,i)-expected)<1e-7,name+' angle '+str(i))
for name,i,j,expected in [('tri-3',0,1,6),('tri-3',0,2,4),('tri-3',1,2,5),('tri-6',0,2,3),('tri-13',0,2,5),('tri-13',1,2,5),('tri-15',1,2,10)]:
    check(abs(length(name,i,j)-expected)<1e-7,name+' longueur '+str((i,j)))
for p in META['tri-9']['points']:check(abs(hypot(p[0]-3,p[1]-1)-10**.5)<1e-8,'tri-9 equidistance centre')
# Audit 2026-10-23 : figures ajoutées ou modifiées.
(cx,cy),r=META['tri-12']['cercle'];b,c=META['tri-12']['points'][1:]
check(isclose(cx,(b[0]+c[0])/2) and isclose(cy,(b[1]+c[1])/2),'tri-12 centre au milieu de l hypotenuse')
for p in META['tri-12']['points']:check(abs(hypot(p[0]-cx,p[1]-cy)-r)<1e-9,'tri-12 cercle passe par '+str(p))
check(META['ang-14']['theta']==90,'ang-14 secante perpendiculaire aux deux droites')
P=META['sol-14']['points'];vec=lambda u,v:(round(P[v][0]-P[u][0],9),round(P[v][1]-P[u][1],9))
check(vec('A','D')==vec('B','E')==vec('C','F'),'sol-14 fuyantes paralleles et de meme longueur')
check(vec('A','B')==vec('D','E') and vec('A','C')==vec('D','F'),'sol-14 face arriere identique a la face avant')
pl=META['proba-3']['places']
check(pl['A']==0 and pl['B']==1 and pl['C']==.5 and 0<pl['E']<.1 and .9<pl['D']<1,'proba-3 positions sur l echelle')
for name in ['tri-2','tri-5','tri-11','tri-13']:
    check(META[name].get('noms')==['B','C','A'],name+' sommet A et base BC')
for c in CHAPITRES:
    for i,e in enumerate(c.exercices,1):
        if e.figure and (c.numero,i)!=(14,14) and ('Construire' in e.enonce or 'Placer' in e.enonce or 'construire' in e.enonce):
            check(r'\geoSolution' in FIGURES[e.figure]['tex'],f'construction ajoutee en correction {c.numero}.{i}')
for name in ['sol-9','sol-10','sol-15','cours-patrons']:check(name in FIGURES,'patron '+name)
from donnees_scripts import verifier_scripts
check(verifier_scripts()==20,'scripts et traces executes')
(ROOT/'build').mkdir(exist_ok=True)
r={'controles_figures':count,'erreurs':errors,'details':details}
(ROOT/'build/controles-figures.json').write_text(json.dumps(r,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps({k:v for k,v in r.items() if k!='details'},ensure_ascii=True,indent=2))
assert not errors
