from pathlib import Path
import importlib,re,json,math
import sympy as s
from modele import CHAPITRES,FIGURES
ROOT=Path(__file__).resolve().parent
for p in sorted(ROOT.glob('contenu_*.py')):importlib.import_module(p.stem)
import bilans
from approfondissements import DEFIS
from donnees_figures import SCHEMAS
from donnees_vecteurs import QUADRILLAGES,vecteur,point
from generer_figures import build
build()
checks=[]
def check(nom,ok):
    assert ok,nom
    checks.append(nom)
# Schémas de triangles : angles droits codés et configurations de Thalès.
for nom,d in SCHEMAS.items():
    pts=d['points']
    for a,b in d['segments']:check(nom+': sommets '+a+b,a in pts and b in pts and pts[a]!=pts[b])
    if d['droits']:
        a,b,c=[pts[k] for k in 'ABC']
        dot=(b[0]-a[0])*(c[0]-a[0])+(b[1]-a[1])*(c[1]-a[1])
        check(nom+': angle A effectivement droit',abs(dot)<1e-7)
    if nom.startswith('thales-'):
        a,b,c,m,n=[pts[k] for k in ['A','B','C','M','N']]
        cross=(n[0]-m[0])*(c[1]-b[1])-(n[1]-m[1])*(c[0]-b[0])
        check(nom+': parallélisme conforme',abs(cross)>1e-3 if nom=='thales-07' else abs(cross)<1e-7)
# Quadrillages des vecteurs : égalités et parallélogrammes annoncés.
def egal(f,a,b,c,d):return vecteur(f,a,b)==vecteur(f,c,d)
def parallelogramme(f,a,b,c,d):
    A,B,C,D=[point(f,p) for p in (a,b,c,d)]
    return (A[0]+C[0],A[1]+C[1])==(B[0]+D[0],B[1]+D[1]) and (B[0]-A[0])*(D[1]-A[1])-(B[1]-A[1])*(D[0]-A[0])!=0
P=lambda f,p:point(f,p)
for p,q in [('A',"A'"),('B',"B'"),('C',"C'")]:
    check('vect-01: symétrique par rapport à (d) '+q,P('vect-01',p)[1]==P('vect-01',q)[1] and P('vect-01',p)[0]+P('vect-01',q)[0]==14)
for p,q in [('A',"A''"),('B',"B''"),('C',"C''")]:
    check('vect-01: demi-tour de centre O '+q,(P('vect-01',p)[0]+P('vect-01',q)[0],P('vect-01',p)[1]+P('vect-01',q)[1])==(10,8))
check('vect-02: CD = AB',egal('vect-02','C','D','A','B'))
check('vect-03: AB = CD = IJ',egal('vect-03','A','B','C','D') and egal('vect-03','A','B','I','J'))
check('vect-03: EF = BA',egal('vect-03','E','F','B','A'))
check('vect-03: GH de direction différente',vecteur('vect-03','G','H')[0]*vecteur('vect-03','A','B')[1]!=vecteur('vect-03','G','H')[1]*vecteur('vect-03','A','B')[0])
check('vect-04: ABDC parallélogramme',parallelogramme('vect-04','A','B','D','C') and egal('vect-04','C','D','A','B'))
check('vect-06: ABCD parallélogramme',parallelogramme('vect-06','A','B','C','D'))
check('vect-07: EF = HG et EFGH parallélogramme',egal('vect-07','E','F','H','G') and parallelogramme('vect-07','E','F','G','H'))
check('vect-08: Chasles',tuple(a+b for a,b in zip(vecteur('vect-08','A','B'),vecteur('vect-08','B','C')))==vecteur('vect-08','A','C'))
d=QUADRILLAGES['vect-09']['vecteurs_libres']
u=(d[0][1][0]-d[0][0][0],d[0][1][1]-d[0][0][1]);v=(d[1][1][0]-d[1][0][0],d[1][1][1]-d[1][0][1])
check('vect-09: OP = u, PS = v, OS = u + v',vecteur('vect-09','O','P')==u and vecteur('vect-09','P','S')==v and vecteur('vect-09','O','S')==(u[0]+v[0],u[1]+v[1]))
check('vect-10: MM\'\' = AC',vecteur('vect-10','M',"M''")==vecteur('vect-10','A','C') and egal('vect-10','M',"M'",'A','B'))
check('vect-11: AB + AD = AC',tuple(a+b for a,b in zip(vecteur('vect-11','A','B'),vecteur('vect-11','A','D')))==vecteur('vect-11','A','C'))
check('vect-12: I milieu',egal('vect-12','A','I','I','B'))
check('vect-13: 60 m puis 80 m',vecteur('vect-13','D','E')==(3,0) and vecteur('vect-13','E','F')==(0,4))
check('vect-15: DCEB parallélogramme',egal('vect-15','D','C','B','E') and egal('vect-15','B','E','A','B') and parallelogramme('vect-15','D','C','E','B'))
# Sections et solides.
for rayon,distance,section in [(5,3,4),(10,6,8)]:
    check(f'section de rayon {rayon}',rayon**2==distance**2+section**2)
check('cylindre d’Archimède',s.Rational(4,3)*27/(9*6)==s.Rational(2,3))
check('demi-cercle : A sur le cercle',abs(math.hypot(-6.5+25/13,60/13)-6.5)<1e-9)
# Statistiques : les boîtes dessinées correspondent aux séries des énoncés.
def quartiles(v):
    v=sorted(v);n=len(v)
    me=v[n//2] if n%2 else s.Rational(v[n//2-1]+v[n//2],2)
    return (v[0],v[math.ceil(n/4)-1],me,v[math.ceil(3*n/4)-1],v[-1])
check('boîte à construire',quartiles([3,5,6,8,9,10,12,13,15,18,20])==(3,6,10,15,20))
check('diagramme en barres',quartiles([1]*3+[2]*7+[3]*9+[4]*6+[5]*5)==(1,2,3,4,5))
check('fiche outil pointures',quartiles([36,37,37,38,38,38,39,40,40,42,43,44])==(36,37,s.Rational(77,2),40,44))
# Probabilités : tableaux de dénombrement.
check('arbre de deux pièces',len([a+b for a in 'PF' for b in 'PF'])==4)
check('tableau des boules : 9 couples RR',sum(a[0]==b[0]=='R' for a in ['R1','R2','R3','B1','B2'] for b in ['R1','R2','R3','B1','B2'])==9)
check('brevet B : 8 issues dont 4 gagnantes',sum((sct[0]=='A' and c=='rouge') or (sct=='B' and c=='bleue') for sct in ['A1','A2','A3','B'] for c in ['rouge','bleue'])==4)
# Présence des figures obligatoires.
for c in CHAPITRES:
    for i,e in enumerate(c.exercices,1):
        if e.figure:check(f'{c.numero}.{i}: figure disponible',e.figure in FIGURES)
        if 12<=c.numero<=17:check(f'{c.numero}.{i}: figure obligatoire',bool(e.figure))
for i,dd in enumerate(DEFIS,1):
    if dd.figure:check(f'défi {i}: figure disponible',dd.figure in FIGURES)
for b in bilans.BILANS:
    for i,p in enumerate(b.problemes,1):
        if p.figure:check(f'brevet {b.lettre}{i}: figure disponible',p.figure in FIGURES)
# Algorithme de décomposition de la fiche outil.
def decomposer(n):
    reste=n;d=2;out=[]
    while reste>1:
        if reste%d==0:out.append(d);reste//=d
        else:d+=1
    return out
for n in [2,13,84,180,420,997]:
    facteurs=decomposer(n)
    check(f'algorithme facteurs premiers de {n}',math.prod(facteurs)==n and all(s.isprime(p) for p in facteurs))
# Aucune figure générée sans usage.
utilisees={e.figure for c in CHAPITRES for e in c.exercices if e.figure}|{dd.figure for dd in DEFIS if dd.figure}|{p.figure for b in bilans.BILANS for p in b.problemes if p.figure}
check('toutes les figures générées sont utilisées',set(FIGURES)==utilisees)
rapport=dict(controles=len(checks),details=checks,visuels_uniques=len(FIGURES))
(ROOT/'build').mkdir(exist_ok=True)
(ROOT/'build/controles-figures.json').write_text(json.dumps(rapport,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps({k:v for k,v in rapport.items() if k!='details'},indent=2))
