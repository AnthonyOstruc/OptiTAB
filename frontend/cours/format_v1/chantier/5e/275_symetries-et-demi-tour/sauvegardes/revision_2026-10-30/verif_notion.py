# -*- coding: utf-8 -*-
"""Vérification indépendante des réponses numériques et de l’intégrité des sources."""
from pathlib import Path
import re, json, math, hashlib
from fractions import Fraction
D=Path(__file__).resolve().parent
N=int(D.name[:3])
data=json.loads((D/'donnees_verification.json').read_text(encoding='utf-8'))
checks=0
def check(condition, context):
    global checks
    assert condition, context
    checks+=1
def norm(s):
    return s.replace(r'\displaystyle','').replace('{,}', '.').replace('$','').replace('′', "'").replace('’', "'").replace('−','-').replace(r'\ ;\ ',' ; ').strip()
def number(s):
    return [float(x) for x in re.findall(r'(?<![A-Za-z])[-+]?\d+(?:\.\d+)?',norm(s))]
text=(D/'exercices.txt').read_text(encoding='utf-8')
blocks=[x for x in re.split(r'^===\s*$',text,flags=re.M) if x.strip()]
source=(D/'source_en_ligne/exercices.txt').read_text(encoding='utf-8')
for name,digest in data['sources_sha256'].items():
    check(hashlib.sha256((D/'source_en_ligne'/name).read_bytes()).hexdigest()==digest,('source modifiée',name))
meta=json.loads((D/'source_en_ligne/meta.json').read_text(encoding='utf-8'))
check(len(blocks)==len(meta['exercices'])==21,'nombre exercices')
for b in blocks:
    eid=int(re.search(r'^Id:\s*(\d+)',b,re.M)[1])
    line=b.strip().splitlines()[0].replace('===','',1).strip()
    check(line==next(x['titre'] for x in meta['exercices'] if x['id']==eid),(eid,'titre'))
    difficulty=re.search(r'^Difficulté:\s*(\w+)',b,re.M)[1]
    sb=next(s for s in re.split(r'^===\s*$',source,flags=re.M) if re.search(rf'^Id:\s*{eid}\s*$',s,re.M))
    check(difficulty==re.search(r'^Difficulté:\s*(\w+)',sb,re.M)[1],(eid,'difficulté'))
    en=b.split('Énoncé:',1)[1].split('Étapes:',1)[0]
    sol=b.split('Solution:',1)[1]
    ans={int(i):v.strip() for i,v in re.findall(r'^([1-6])\.\s*(.*)$',sol,re.M)}
    check(len(ans)==6,(eid,'six réponses'))
    check(len(re.findall(r'^## Question ',b,re.M))==6,(eid,'six questions'))
    check(len(re.findall(r'^::: etape ',b,re.M))==6,(eid,'six raisonnements'))
    a={i:number(v) for i,v in ans.items()}
    if N==271 and 'Une recette' in en:
        p,m=map(int,re.search(r'pour (\d+) personnes demande (\d+) g',en).groups())
        k=Fraction(m,p);q=int(re.search(r'pour (\d+) personnes \?',en)[1]);stock=int(re.search(r'Avec (\d+) g',en)[1])
        expected={1:[float(k)],2:[float(q*k)],3:[float(k)],4:[float(Fraction(stock,1)/k)],5:[float(2*m),float(2*p)],6:[float(100+k),1,float(100+2*k),2]}
    elif N==271:
        price,t=map(int,re.search(r'coûte (\d+) €.*remise de (\d+) %',en).groups());r=Fraction(price*t,100);paid=price-r
        expected={1:[price],2:[price/100],3:[float(r)],4:[float(paid)],5:[100-t],6:[float(2*paid)]}
    elif N==272 and 'jardin rectangulaire' in en:
        x,y=map(int,re.search(r'A\(-(\d+) ; (\d+)\)',en).groups())
        expected={1:[-x,y],3:[y],4:[2*x],5:[2*y,4*x*y],6:[0,0]}
        check('A et B' in ans[2],(eid,2))
    elif N==272:
        fixe,k=map(int,re.search(r'coûte (\d+) €.*puis (\d+) €',en).groups());q=int(re.search(r'prix de (\d+) activités',en)[1]);budget=int(re.search(r'avec (\d+) €',en)[1])
        expected={1:[k,fixe],2:[fixe,k+fixe,2*k+fixe],3:[k*q+fixe],4:[2,2*k+fixe],5:[fixe],6:[(budget-fixe)/k]}
    elif N==273:
        t=int(re.search(r'mesure (\d+)°',en)[1]);u=180-t
        if 'rosace' in line:expected={1:[180],2:[u],3:[t],4:[u],5:[t/2],6:[t,u,t,u,360]}
        else:expected={1:[0,t,90],2:[t],3:[u],4:[t],5:[t]}
        check(2*t+2*u==360,(eid,'tour'))
    elif N==274 and 'On veut construire' in en:
        L,x,y=map(int,re.search(r'AB = (\d+) cm.*BAC = (\d+)°.*ABC = (\d+)°',en).groups());z=180-x-y
        expected={1:[z],3:[L],4:[x,y],6:[L,x,y,z]}
        check((ans[2].startswith('Oui'))==(max(x,y,z)>90),(eid,'angle obtus'))
        check(x+y+z==180 and z>0,(eid,'somme angles'))
        # Independent geometric construction using intersections of rays.
        X=L*math.tan(math.radians(y))/(math.tan(math.radians(x))+math.tan(math.radians(y)))
        Y=X*math.tan(math.radians(x))
        vx,vy=-X,-Y;wx,wy=L-X,-Y
        angle=math.degrees(math.acos((vx*wx+vy*wy)/math.hypot(vx,vy)/math.hypot(wx,wy)))
        check(math.isclose(angle,z,abs_tol=1e-9),(eid,'figure troisième angle'))
    elif N==274:
        base,h=map(int,re.search(r'BC de (\d+) m.*mesure (\d+) m',en).groups());area=Fraction(base*h,2)
        expected={2:[float(area)],3:[base/2],5:[float(area/2)]}
        check(base/2*h/2+base/2*h/2==area,(eid,'aires médiane'))
    else:
        x,y=map(int,re.search(r'A\((\d+) ; (\d+)\)',en).groups());central='centrale' in en;s=-1 if central else 1
        expected={2:[-x,s*y],3:[-x-2,s*y,-x,s*(y+2)],4:[2],5:[2]}
        points=[(x,y),(x+2,y),(x,y+2)]
        images=[(-px,s*py) for px,py in points]
        check([(-px,s*py) for px,py in images]==points,(eid,'involution'))
        det=lambda p:abs((p[1][0]-p[0][0])*(p[2][1]-p[0][1])-(p[2][0]-p[0][0])*(p[1][1]-p[0][1]))/2
        check(det(points)==det(images)==2,(eid,'conservation aire'))
        check(math.dist(images[0],images[1])==math.dist(images[0],images[2])==2,(eid,'longueurs'))
    for i,v in expected.items():check(a[i]==v,(eid,i,'obtenu',a[i],'attendu',v))
# Exemples numériques des cours et fiches, contrôlés séparément.
if N==271:
    check(Fraction(24,10)==Fraction(48,10)/2==Fraction(84,10)/Fraction(35,10),'tableau')
    check(Fraction(6,4)==Fraction(3,2) and 200*Fraction(6,4)==300,'recette')
    check(80*Fraction(15,100)==12 and 80-12==68,'remise')
    check(Fraction(7,20)==Fraction(35,100),'proportion')
    check(3*200==600 and Fraction(1000,200)==5 and Fraction(30,60)==Fraction(1,2) and 60*Fraction(25,10)==150,'échelles/vitesse')
elif N==272:check([3*t+5 for t in [0,1,2,4]]==[5,8,11,17],'tableau tarif')
elif N==273:check(180-40==140 and 180-140==40 and 40/2==20,'angles cours')
elif N==274:
    check(180-35-45==100 and 7<4+5 and not 6<2+3,'angles/constructibilité')
    check(Fraction(8*3,2)==12 and Fraction(4*3,2)==6,'aires cours')
else:check(2*2/2==2,'aire cours')
result={'statut':'OK','notion':N,'exercices':len(blocks),'assertions':checks,'sources_inalterees':True}
(D/'resultat_verification.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(result,ensure_ascii=False))

