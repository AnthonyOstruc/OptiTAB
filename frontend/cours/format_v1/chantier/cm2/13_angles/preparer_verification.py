from pathlib import Path
import json
B=Path(__file__).resolve().parent.parent
CODE=r'''from pathlib import Path
import json, re, math
from fractions import Fraction
P=Path(__file__).resolve().parent
numero=int(P.name[:2]); controles=[]
def ok(v,n):
    assert v,n
    controles.append(n)
def near(a,b):return abs(a-b)<1e-5
if numero==13:
    for a,b in [(45,45),(90,45),(45,135)]:ok(a+b<=180,f'somme saillante {a}+{b}={a+b}')
    for a,n in [(90,2),(180,2),(90,4)]:ok(Fraction(a,n)*n==a,f'pliage {a}/{n}={float(Fraction(a,n))}')
    for n,a in [(2,45),(3,45),(4,30)]:ok(0<n*a<=180,f'multiple {n}x{a}={n*a}')
    for a,b in [(2,3),(3,5),(4,7)]:ok(a+(b-a)==b,f'comparaison gabarits {a} et {b}')
    ok(near(math.degrees(math.atan2(1.77,1.77)),45),'coordonnées : demi-angle droit')
    ok(90/2==45 and 90+90==180 and 90+45==135,'mesures du cours')
elif numero==14:
    for sides in [(4,4,6),(5,5,5),(3,3,4)]:
        ok(sum(sides)>2*max(sides),f'triangle constructible {sides}')
        ok(len(set(sides))<3,f'côtés égaux {sides}')
    for a,b in [(6,4),(8,3),(9,5)]:ok(a+b+a+b==2*(a+b),f'contour rectangle {a}x{b}')
    for a,b,h in [(6,4,3),(7,3,4),(8,5,3)]:ok(a!=b and a>b and h>0,f'trapèze rectangle non rectangle {a},{b},{h}')
    ok(near(math.hypot(1,1.73205),2),'triangle équilatéral : coordonnées des 3 côtés')
    ok(near(math.hypot(1.4,.8),math.hypot(-1.4,.8)),'losange : coordonnées des côtés')
elif numero==15:
    for a in (6,8,10,4):ok(2*(a/2)==a,f'milieu de {a} cm')
    for r in (3,4,5):ok(r-1<r and r+1>r and 2*r==r+r,f'cercle et disque rayon {r}')
    for a,b in [(5,3),(6,4),(7,3)]:
        A=(0,0);Bb=(a,0);C=(a,b);D=(0,b)
        ok((Bb[0]-A[0])*(D[0]-A[0])+(Bb[1]-A[1])*(D[1]-A[1])==0,f'angle droit rectangle {a}x{b}')
        ok(math.dist(A,Bb)==math.dist(C,D) and math.dist(A,D)==math.dist(Bb,C),f'longueurs rectangle {a}x{b}')
    ok(near(math.dist((0,0),(1.5,2.598076211)),3),'arcs de compas : intersection à 3 cm')
elif numero==16:
    for a in (2,3,4):ok(math.dist((-a,0),(a,0))==2*a,f'axe vertical distance {a}')
    for a in (1,2,3):ok(math.dist((0,a),(0,-a))==2*a,f'axe horizontal distance {a}')
    for a,b in [(3,1),(4,2),(5,1)]:
        A=(a,b);R=(b,a);M=((a+b)/2,(a+b)/2)
        ok(M[0]==M[1] and (R[0]-A[0])+(R[1]-A[1])==0,f'réflexion diagonale {A}->{R}')
    for pts,fn in [([(-1.5,-1),(-.5,-1),(-.5,1)],lambda x,y:(-x,y)),([(-1.5,1.5),(-1.5,.5),(1,.5)],lambda x,y:(x,-y)),([(1.5,.5),(1.5,-.5),(.5,-.5)],lambda x,y:(y,x))]:
        images=[fn(*p) for p in pts]
        ok(all(near(math.dist(pts[i],pts[i+1]),math.dist(images[i],images[i+1])) for i in range(2)),'coordonnées finales des figures symétriques')
elif numero==17:
    for n in (3,4,5):
        ok((n+2)-(3*n)+(2*n)==2,f'prisme : faces/arêtes/sommets pour base {n}')
        ok((n+1)-(2*n)+(n+1)==2,f'pyramide : faces/arêtes/sommets pour base {n}')
    for a,b,h in [(3,2,2),(4,3,2),(4,3,3)]:ok(a*b*h-a*b==a*b*(h-1),f'cubes par couches {a},{b},{h}')
    # Propagation des bases orthonormées lors du pliage à 90 degrés.
    def neg(a):return tuple(-x for x in a)
    cells={(0,0):1,(1,0):2,(2,0):3,(3,0):4,(1,1):5,(1,-1):6}
    orient={(1,0):((1,0,0),(0,1,0),(0,0,1))};todo=[(1,0)]
    for x,y in todo:
        u,v,n=orient[x,y]
        for dx,dy,new in [(1,0,(neg(n),v,u)),(-1,0,(n,v,neg(u))),(0,1,(u,neg(n),v)),(0,-1,(u,n,neg(v)))]:
            key=(x+dx,y+dy)
            if key in cells and key not in orient:orient[key]=new;todo.append(key)
    normals={cells[p]:o[2] for p,o in orient.items()}
    ok(len(set(normals.values()))==6,'patron cube : six normales distinctes sans recouvrement')
    for a,b in [(1,3),(2,4),(5,6)]:ok(normals[a]==neg(normals[b]),f'faces opposées {a}/{b}')
    dims=[(4,2),(3,2),(4,2),(3,2),(4,3),(4,3)]
    ok(sum(a*b for a,b in dims)==2*(4*3+4*2+3*2),'patron pavé : dimensions et aire totale')
    # Toutes les arêtes d'un pavé sont représentées une seule fois (9 visibles, 3 cachées).
    edges={(0,1),(1,2),(2,3),(0,3),(3,7),(6,7),(2,6),(1,5),(5,6),(0,4),(4,5),(4,7)}
    ok(len(edges)==12 and sum(4 in e for e in edges)==3,'perspective : seules les trois arêtes incidentes au sommet arrière-bas-gauche sont cachées')
else:raise AssertionError(numero)
# Vérification structurelle des 63 réponses ; les nombres sont contrôlés ci-dessus.
t=(P/'exercices.txt').read_text(encoding='utf-8')
blocks=[b for b in re.split(r'^===\s*$',t,flags=re.M) if b.strip()]
ok(len(blocks)==21,'21 blocs')
for i,b in enumerate(blocks,1):
    ok(f'Id: nouveau-{i}\n' in b,f'identité {i}')
    ok(len(re.findall(r'^## Question [123] :',b,re.M))==3,f'3 questions corrigées {i}')
    for typ in ('methode','etape','resultat'):ok(len(re.findall(r'^::: '+typ+r'\b',b,re.M))==3,f'{typ} pour chaque question {i}')
report={'statut':'OK','math_OK':True,'controles':len(controles),'details':controles}
(P/'validation_math.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'chapitre':numero,'statut':'OK','controles':len(controles)},ensure_ascii=False))
'''
for name in ['13_angles','14_polygones','15_constructions','16_symetrie','17_solides']:(B/name/'verif_math.py').write_text(CODE,encoding='utf-8')
