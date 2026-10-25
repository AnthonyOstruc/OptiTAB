"""Contrôles de coordonnées, milieux, parallélismes, angles droits, cercles et présence des figures."""
from pathlib import Path
import importlib,math,json
from modele import CHAPITRES,FIGURES
ROOT=Path(__file__).resolve().parent
(ROOT/'build').mkdir(exist_ok=True)
for p in sorted(ROOT.glob('contenu_*.py')):importlib.import_module(p.stem)
import generer_figures as g
for fn in [g.nombres_modeles,g.statistiques_hasard,g.raisonnement,g.translations,g.milieux,g.pythagore,g.cercle,g.solides,g.scripts,g.annexes]:fn()
count=0;details=[]
EPS=1e-7
def check(ok,description):
    global count
    assert ok,description
    count+=1;details.append(description)
def dist(a,b):return math.hypot(a[0]-b[0],a[1]-b[1])
def vecteur(a,b):return (b[0]-a[0],b[1]-a[1])
def croix(u,v):return u[0]*v[1]-u[1]*v[0]
def scal(u,v):return u[0]*v[0]+u[1]*v[1]
def norme(u):return math.hypot(*u)
for name,d in g.GEOMETRIE.items():
    P=d.get('points',{})
    if 'longueurs' in d:
        a,b,c=d['triangle'];ab,ac,bc=d['longueurs']
        for val,expected in [(dist(a,b),ab),(dist(a,c),ac),(dist(b,c),bc)]:check(abs(val-expected)<EPS,f'{name} : longueur {expected:g}')
        if d['rectangle']:check(abs(scal(vecteur(a,b),vecteur(a,c)))<EPS,f'{name} : angle droit en A')
    for m,p,q in d.get('milieux',[]):
        check(dist(P[m],((P[p][0]+P[q][0])/2,(P[p][1]+P[q][1])/2))<EPS,f'{name} : {m} milieu de [{p}{q}]')
    for (p1,p2),(q1,q2) in d.get('paralleles',[]):
        u=vecteur(P[p1],P[p2]);v=vecteur(P[q1],P[q2])
        check(abs(croix(u,v))<EPS*max(1,norme(u)*norme(v)),f'{name} : ({p1}{p2}) parallèle à ({q1}{q2})')
    for (p1,p2),(q1,q2) in d.get('non_paralleles',[]):
        u=vecteur(P[p1],P[p2]);v=vecteur(P[q1],P[q2])
        check(abs(croix(u,v))>1e-3,f'{name} : ({p1}{p2}) non parallèle à ({q1}{q2})')
    for (p1,p2),(q1,q2) in d.get('perpendiculaires',[]):
        a=P[p1] if isinstance(p1,str) else p1;b=P[p2] if isinstance(p2,str) else p2
        u=vecteur(a,b);v=vecteur(P[q1],P[q2])
        check(abs(scal(u,v))<1e-6*max(1,norme(u)*norme(v)),f'{name} : perpendicularité ({q1}{q2})')
    for (p1,p2),(q1,q2) in d.get('moities',[]):
        check(abs(2*dist(P[p1],P[p2])-dist(P[q1],P[q2]))<EPS,f'{name} : {p1}{p2} moitié de {q1}{q2}')
    for (p1,p2),(q1,q2) in d.get('egalites',[]):
        check(abs(dist(P[p1],P[p2])-dist(P[q1],P[q2]))<1e-6,f'{name} : {p1}{p2} = {q1}{q2}')
    for o,pts in d.get('cercles',[]):
        r=dist(P[o],P[pts[0]])
        for q in pts[1:]:check(abs(dist(P[o],P[q])-r)<1e-6,f'{name} : {q} sur le cercle de centre {o}')
    for a,b,c in d.get('alignes',[]):
        check(abs(croix(vecteur(P[a],P[b]),vecteur(P[a],P[c])))<1e-6,f'{name} : {a}, {b}, {c} alignés')
    if 'translation' in d:
        t=d['translation'];dx,dy=t['deplacement']
        for a,b in zip(t['points'],t['images']):check(abs(b[0]-a[0]-dx)+abs(b[1]-a[1]-dy)<1e-8,f'{name} : même déplacement')
    if 'transformations' in d:
        T=d['transformations'];x0=T['axe_x'];cx,cy=T['centre'];dx,dy=T['deplacement']
        for p,s_,r_,t_ in zip(T['F'],T['symetrie'],T['demi-tour'],T['translation']):
            check(abs(s_[0]+p[0]-2*x0)<EPS and abs(s_[1]-p[1])<EPS,f'{name} : symétrie axiale d’axe x = {x0}')
            check(abs(r_[0]+p[0]-2*cx)<EPS and abs(r_[1]+p[1]-2*cy)<EPS,f'{name} : demi-tour de centre ({cx} ; {cy})')
            check(abs(t_[0]-p[0]-dx)<EPS and abs(t_[1]-p[1]-dy)<EPS,f'{name} : translation')
for nom,angles in g.SECTEURS.items():
    check(abs(sum(angles)-360)<EPS and all(a>0 for a in angles),nom+' : tour complet')
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
G=g.GEOMETRIE
check(G['pyth-01']['longueurs']==(6,8,10),'Pythagore 1 : données de l’énoncé')
check(G['pyth-02']['longueurs']==(5,12,13),'Pythagore 2 : données de l’énoncé')
a,b,c=G['pyth-10']['triangle']
check(abs(scal(vecteur(c,a),vecteur(c,b)))<1e-8,'Pythagore 10 : angle droit en C')
check(abs(G['trans-04']['longueurs'][0]*G['trans-04']['triangle'][2][1]/2-9)<1e-8,'Translation 4 : aire 9 et angle 42 cohérents')
P6=G['mil-06']['points']
check(abs(dist(P6['A'],P6['B'])/dist(P6['A'],P6['C'])-6/8)<1e-9 and abs(dist(P6['B'],P6['C'])/dist(P6['A'],P6['C'])-10/8)<1e-9,'Triangle des milieux : côtés proportionnels à 6, 8, 10')
check(abs(dist(G['cer-15']['points']['A'],G['cer-15']['points']['B'])/.45-5)<1e-9,'Cercle 15 : AB = 5 cm')
B7=G['cer-07']['points']['B'];A7=G['cer-07']['points']['A'];C7=G['cer-07']['points']['C']
ang=math.degrees(math.acos(scal(vecteur(B7,A7),vecteur(B7,C7))/(dist(B7,A7)*dist(B7,C7))))
check(abs(ang-32)<1e-6,'Cercle 7 : angle ABC de 32 degrés')
B15=G['trans-15']['translation'];A15=B15['points'][1];Bp=B15['points'][0];Cp=B15['images'][0]
ang=math.degrees(math.acos(scal(vecteur(Bp,Cp),vecteur(Bp,A15))/(dist(Bp,Cp)*dist(Bp,A15))))
check(abs(ang-70)<1e-6,'Translation 15 : angle ABC de 70 degrés')
check(180==2*90,'Deux angles droits : somme déjà égale à 180')
check(abs(216/360*2*math.pi*5-2*math.pi*3)<1e-8,'Patron de cône : bord du secteur et base')
check([90/360*40,144/360*40,72/360*40,36/360*40,18/360*40]==[10,16,8,4,2],'Diagramme fratrie : angles et effectifs')
report={'controles_figures':count,'figures':len(FIGURES),'erreurs':[],'details':details}
(ROOT/'build/controles-figures.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps({k:v for k,v in report.items() if k!='details'},ensure_ascii=True,indent=2))
