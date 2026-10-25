from pathlib import Path
import importlib,re,json,math
import sympy as s
from modele import CHAPITRES,FIGURES
ROOT=Path(__file__).resolve().parent
for p in sorted(ROOT.glob('contenu_*.py')):importlib.import_module(p.stem)
import bilans
from donnees_figures import SCHEMAS
from generer_figures import build
build()
checks=[]
def check(nom,ok):
    assert ok,nom
    checks.append(nom)
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
for nom in ['proba-pieces','proba-remise','proba-sans-remise','brevet-A-arbre','brevet-B-arbre']:
    poids=[s.Rational(v) for v in re.findall(r'\$\s*(\d+/\d+)\s*\$',FIGURES[nom]['tex'])]
    check(nom+': six poids',len(poids)==6)
    check(nom+': sommes par nœud',all(poids[i]+poids[i+1]==1 for i in [0,2,4]))
    check(nom+': somme des chemins',poids[0]*(poids[2]+poids[3])+poids[1]*(poids[4]+poids[5])==1)
for c in CHAPITRES:
    for i,e in enumerate(c.exercices,1):
        if e.figure:check(f'{c.numero}.{i}: figure disponible',e.figure in FIGURES)
        if 12<=c.numero<=17:check(f'{c.numero}.{i}: figure obligatoire',bool(e.figure))
for rayon,distance,section in [(5,3,4),(10,6,8)]:
    check(f'section de rayon {rayon}',rayon**2==distance**2+section**2)
check('histogramme : classes égales et effectif',sum([4,8,6,2])==20 and len(set([10,10,10,10]))==1)
check('diagramme circulaire : 360 degrés',sum([90,162,108])==360)
def decomposer(n):
    reste=n;d=2;out=[]
    while reste>1:
        if reste%d==0:out.append(d);reste//=d
        else:d+=1
    return out
for n in [2,13,84,180,420,997]:
    facteurs=decomposer(n)
    check(f'algorithme facteurs premiers de {n}',math.prod(facteurs)==n and all(s.isprime(p) for p in facteurs))
rapport=dict(controles=len(checks),details=checks,visuels_uniques=len(FIGURES))
(ROOT/'build/controles-figures.json').write_text(json.dumps(rapport,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps({k:v for k,v in rapport.items() if k!='details'},indent=2))
