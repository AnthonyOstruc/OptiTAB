"""Présence et cohérence des figures de géométrie réellement incluses."""
from pathlib import Path
import math,re,json
ROOT=Path(__file__).resolve().parent
checks=[]
def check(name,value):
    assert value,name
    checks.append(name)
def close(a,b):return math.isclose(a,b,abs_tol=3e-6)
def source(key):return (ROOT/'figures'/f'{key}.tex').read_text(encoding='utf-8')
def points(key):
    return {n:tuple(map(float,(x,y))) for n,x,y in re.findall(r'\\coordinate \((\w+)\) at \(([-\d.]+),([-\d.]+)\)',source(key))}
def circle_points(key,center,radius,names):
    p=points(key)
    for name in names:check(f'{key} : {name} sur le cercle',close(math.dist(p[name],center),radius))

insertions=0
for folder,kind in [('chapitres','exercice'),('corriges','corrige')]:
    for ch in ('07','08'):
        p=next((ROOT/folder).glob(ch+'-*.tex'))
        blocks=re.findall(r'\\begin\{'+kind+r'\}.*?\\end\{'+kind+r'\}',p.read_text(encoding='utf-8'),re.S)
        check(f'{folder} {ch} : 15 blocs',len(blocks)==15)
        for n,block in enumerate(blocks,1):
            refs=re.findall(r'\\figureGeo(?:\[([^]]+)\])?\{([^}]+)\}',block)
            check(f'{folder} {ch}.{n} : figure présente',len(refs)==1 and refs[0][1]==f'{ch}-{n:02}')
            check(f'{folder} {ch}.{n} : bonne version',refs[0][0]==('corrige' if folder=='corriges' else ''))
            insertions+=1
    p=ROOT/folder/'06-trigonometrie.tex'
    blocks=re.findall(r'\\begin\{'+kind+r'\}.*?\\end\{'+kind+r'\}',p.read_text(encoding='utf-8'),re.S)
    for n in (9,10,12,13,14,15):
        check(f'{folder} 06.{n} : figure présente',f'{{06-{n:02}}}' in blocks[n-1])
        insertions+=1

for p in (ROOT/'figures').glob('*.tex'):
    text=p.read_text(encoding='utf-8')
    check(f'{p.stem} : caractères valides',not any(ord(c)<32 and c not in '\r\n' for c in text))
    for n,match in enumerate(re.finditer(r'\\draw\[otGreenDark,line width=\.65pt\]\(([-\d.]+),([-\d.]+)\)--\(([-\d.]+),([-\d.]+)\)--\(([-\d.]+),([-\d.]+)\)',text),1):
        x1,y1,x2,y2,x3,y3=map(float,match.groups())
        u=(x1-x2,y1-y2);v=(x3-x2,y3-y2)
        check(f'{p.stem} : codage droit {n}',close(u[0]*v[0]+u[1]*v[1],0) and close(math.hypot(*u),math.hypot(*v)))

circle_points('07-13',(0,0),2,'ABP')
check('07-13 : Q intérieur',math.dist(points('07-13')['Q'],(0,0))<2)
circle_points('07-15',(3,0),math.sqrt(14),'M')
circle_points('07-cours-cercle',(0,0),2,'ABM')
circle_points('08-03',(2,-1),3,'AB')
circle_points('08-04',(2,-3),5,'PQ')
circle_points('08-08',(1,-2),5,'ABCD')
circle_points('08-10',(1,2),5,'A')
circle_points('08-12',(3,1),math.sqrt(10),'ABC')
circle_points('08-13',(2,1),math.sqrt(5),'PQ')
circle_points('08-14',(1,3),3,'PQ')

line_equations={
 '08-01':[(3,-2,5)],'08-02':[(3,4,-2)],'08-04':[(1,0,-2)],
 '08-06':[(2,1,-5)],'08-07':[(3,-2,1),(6,-4,-7),(2,3,-5),(2,3,-8)],
 '08-08':[(0,1,-1),(1,0,-1)],'08-10':[(3,4,-36)],'08-11':[(3,1,-5)],
 '08-12':[(1,0,-2),(1,-1,0),(1,0,-3)],'08-13':[(1,1,-4)],
 '08-14':[(0,1,0),(0,1,-2),(0,1,-6),(0,1,-7)],'08-15':[(2,-1,-3)]}
for key,equations in line_equations.items():
    lines=[tuple(map(float,m)) for m in re.findall(r'\\draw\[(?:geoTrait|geoAide|geoReponse|otMuted,dotted|otNavy,dashed)\]\(([-\d.]+),([-\d.]+)\)--\(([-\d.]+),([-\d.]+)\)',source(key))]
    for a,b,c in equations:
        check(f'{key} : droite {a}x+{b}y+{c}=0',any(close(a*x+b*y+c,0) and close(a*z+b*t+c,0) for x,y,z,t in lines))

report={'insertions_exercices_corriges':insertions,'configurations_exercices':36,'controles_reussis':len(checks),'controles':checks}
(ROOT/'build').mkdir(exist_ok=True)
(ROOT/'build/verification-figures.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(f'{len(checks)} contrôles réussis ; 30 exercices de géométrie et 6 de trigonométrie illustrés avec leurs corrigés.')
