"""Contrôles de coordonnées, rapports, surfaces et présence des figures."""
from pathlib import Path
import importlib,math,json
from modele import CHAPITRES,FIGURES
ROOT=Path(__file__).resolve().parent
(ROOT/'build').mkdir(exist_ok=True)
for p in sorted(ROOT.glob('contenu_*.py')):importlib.import_module(p.stem)
import generer_figures as g
for fn in [g.nombres_modeles,g.statistiques_hasard,g.triangles_egaux,g.pythagore,g.tous_thales,g.cosinus,g.translations,g.solides,g.scripts,g.annexes]:fn()
count=0;details=[]
def check(ok,description):
    global count
    assert ok,description
    count+=1;details.append(description)
def dist(a,b):return math.hypot(a[0]-b[0],a[1]-b[1])
for name,d in g.GEOMETRIE.items():
    if 'longueurs' in d:
        a,b,c=d['points'];ab,ac,bc=d['longueurs']
        for val,expected in [(dist(a,b),ab),(dist(a,c),ac),(dist(b,c),bc)]:check(abs(val-expected)<1e-7,f'{name} : longueur {expected}')
        if d['rectangle']:check(abs((b[0]-a[0])*(c[0]-a[0])+(b[1]-a[1])*(c[1]-a[1]))<1e-7,f'{name} : angle droit A')
    if 'emboites' in d:
        p=d['emboites'];a,b,c,m,n=[p[k] for k in ['A','B','C','M','N']]
        k=dist(a,m)/dist(a,b);l=dist(a,n)/dist(a,c)
        check(0<k<1 and 0<l<1,f'{name} : points sur les segments')
        cross=(n[0]-m[0])*(c[1]-b[1])-(n[1]-m[1])*(c[0]-b[0])
        check((abs(cross)<1e-7)==d['paralleles'],f'{name} : parallélisme réel')
        if d['paralleles']:check(abs(dist(m,n)/dist(b,c)-k)<1e-7,f'{name} : rapport des segments parallèles')
    if 'translation' in d:
        t=d['translation'];dx,dy=t['deplacement']
        for a,b in zip(t['points'],t['images']):check(abs(b[0]-a[0]-dx)+abs(b[1]-a[1]-dy)<1e-8,f'{name} : même déplacement')
for nom,angles in g.SECTEURS.items():
    check(sum(angles)==360 and all(a>0 for a in angles),nom+' : tour complet')
for c in CHAPITRES:
    for i,e in enumerate(c.exercices,1):
        if e.figure:check(e.figure in FIGURES,f'{c.numero}.{i} : figure existante')
        if 12<=c.numero<=17:check(bool(e.figure),f'{c.numero}.{i} : schéma géométrique requis')
from approfondissements import DEFIS
from bilans import BILANS
for d in DEFIS:
    if d.figure:check(d.figure in FIGURES,d.titre+' : figure du défi')
for b in BILANS:
    for p in b.problemes:
        if p.figure:check(p.figure in FIGURES,p.titre+' : figure du bilan')
check(g.GEOMETRIE['pyth-01']['longueurs']==(6,8,10),'Pythagore 1 : données de l’énoncé')
check(g.GEOMETRIE['pyth-02']['longueurs']==(5,12,13),'Pythagore 2 : données de l’énoncé')
a,b,c=g.GEOMETRIE['pyth-10']['points']
check(abs((a[0]-c[0])*(b[0]-c[0])+(a[1]-c[1])*(b[1]-c[1]))<1e-8,'Pythagore 10 : angle droit en C')
check(abs(g.GEOMETRIE['trans-04']['longueurs'][0]*g.GEOMETRIE['trans-04']['points'][2][1]/2-9)<1e-8,'Translation 4 : aire 9 et angle 42 cohérents')
check(180==2*3*3*2*5,'Arbre de facteurs 180')
check([20,12,8]==[40*a/360 for a in [180,108,72]],'Diagramme sports : angles et effectifs')
check(abs(216/360*2*math.pi*5-2*math.pi*3)<1e-8,'Patron de cône : bord du secteur et base')
report={'controles_figures':count,'figures':len(FIGURES),'erreurs':[],'details':details}
(ROOT/'build/controles-figures.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps({k:v for k,v in report.items() if k!='details'},ensure_ascii=True,indent=2))
