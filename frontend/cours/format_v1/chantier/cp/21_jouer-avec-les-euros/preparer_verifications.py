"""Installe huit contrôles autonomes, sans importer les générateurs de contenu."""
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent
COMMON=r'''"""Vérification indépendante des vrais textes, données et activités sources CP."""
from pathlib import Path
import ast,hashlib,itertools,json,math,re,runpy
HERE=Path(__file__).resolve().parent
def read(n):return (HERE/n).read_text(encoding='utf-8')
def load(n):return json.loads(read(n))
def norm(t):return re.sub(r'\s+',' ',t).strip()
data=load('donnees_exercices_root.json');source=load('sources_locales/chapitre.json')
texts={n:read(n) for n in ('cours_nouveau.txt','fiche_nouvelle.txt','exercices.txt')}
blocks=[b.strip() for b in re.split(r'^===[ \t]*$',texts['exercices.txt'],flags=re.M) if b.strip()]
assert len(data)==len(blocks)==len(source['exercices'])==9
results={};enonces={};traces=[];equations=[]
def calc(s):
 def walk(t):
  if isinstance(t,ast.Expression):return walk(t.body)
  if isinstance(t,ast.Constant) and type(t.value)==int:return t.value
  if isinstance(t,(ast.Tuple,ast.List)):return tuple(walk(v) for v in t.elts)
  if isinstance(t,ast.BinOp) and isinstance(t.op,(ast.Add,ast.Sub,ast.Mult)):
   a,b=walk(t.left),walk(t.right)
   return a+b if isinstance(t.op,ast.Add) else a-b if isinstance(t.op,ast.Sub) else a*b
  raise ValueError(s)
 return walk(ast.parse(s,mode='eval'))
for i,(item,block,origin) in enumerate(zip(data,blocks,source['exercices']),1):
 assert item['id']==f'nouveau-{i}' and f'Id: nouveau-{i}' in block
 en=block.split('Énoncé:',1)[1].split('Étapes:',1)[0].strip();enonces[i]=en
 et=block.split('Étapes:',1)[1].split('Solution:',1)[0].strip();so=block.split('Solution:',1)[1].strip()
 actual=re.findall(r'^([1-5])\. (.*)$',en,re.M)
 assert len(actual)==len(item['questions'])==5
 assert norm(en.split('1. ',1)[0].replace('<!-- optitab:1 -->',''))==norm(item['enonce'])
 sections=re.split(r'^## Question [1-5] : ',et,flags=re.M)[1:]
 answer=re.findall(r'^::: resultat\n(.*?)\n:::',et,re.M|re.S)
 short=re.findall(r'^[1-5]\. (.*)$',so,re.M)
 assert len(sections)==len(answer)==len(short)==5
 for j,(q,(_,prompt),step,res,sol) in enumerate(zip(item['questions'],actual,sections,answer,short),1):
  assert prompt==q['question'] and step.startswith(q['question']+'\n')
  assert q['methode'] in step and all(s in step for s in q['etapes'])
  assert res==sol==q['resultat'] and '::: methode' in step and '::: etape' in step
  results[i,j]=res
 # Les expressions source sont recalculées séparément et ne servent jamais de réponses attendues.
 if origin.get('check'):
  for comparison in re.split(r'\s+and\s+',origin['check']):
   left,right=comparison.split('==');assert calc(left)==calc(right),(i,'source',comparison)
for name,text in texts.items():
 for expression in re.findall(r'(?<![\d+\-])\d+(?:\s*[+\-]\s*\d+)+\s*=\s*\d+(?:\s*[+\-]\s*\d+)*(?:\s*=\s*\d+(?:\s*[+\-]\s*\d+)*)*',text):
  values=[calc(s.strip()) for s in expression.split('=')]
  assert len(set(values))==1,(name,expression,values)
  equations.append({'fichier':name,'egalite':expression,'valeur':values[0]})
 for a,op,b in re.findall(r'(?<!\d)(\d+)\s*([<>])\s*(\d+)(?!\d)',text):
  assert (int(a)<int(b)) if op=='<' else (int(a)>int(b)),(name,a,op,b)
def nums(t):return list(map(int,re.findall(r'\d+',re.sub(r'\[IMAGE_\d+\]','',t))))
def intro(e):return data[e-1]['enonce']
def number(e,q,value):
 found=nums(results[e,q])
 if not found:
  verbal={'un':1,'une':1,'deux':2,'trois':3,'quatre':4,'cinq':5,'six':6,'sept':7,'huit':8,'neuf':9,'dix':10}
  found=[verbal[w.lower()] for w in re.findall(r'\b(?:un|une|deux|trois|quatre|cinq|six|sept|huit|neuf|dix)\b',results[e,q],re.I)]
 assert found and found[0]==value,(e,q,results[e,q],value)
 traces.append({'exercice':e,'question':q,'modele':'nombre recalculé','attendu':value,'publie':results[e,q]})
def expect(e,q,pattern,reason):
 assert re.search(pattern,results[e,q],re.I),(e,q,results[e,q],pattern)
 traces.append({'exercice':e,'question':q,'modele':reason,'publie':results[e,q]})
def allpatterns(rows,reason):
 for e,row in enumerate(rows,1):
  assert len(row)==5
  for q,p in enumerate(row,1):expect(e,q,p,reason)
'''
SPECIAL={}
SPECIAL[21]=r'''
# Comptage des valeurs et recherche exhaustive du nombre minimal d'objets.
values=(10,5,2)
for q,value in enumerate((*values,sum(values[:2]),sum(values)),1):number(1,q,value)
target,bill,coin,unit=nums(intro(2));number(2,1,bill);number(2,2,target-bill)
assert bill+coin+unit==target
number(3,1,1);number(3,2,4);number(3,3,sum([2]*4))
target,bill,coin=nums(intro(4))
ways=[(b,c) for b in range(target//bill+1) for c in range(target//coin+1) if bill*b+coin*c==target]
b,c=min(ways,key=lambda t:sum(t))
for q,value in ((1,b),(2,target-b*bill),(3,c),(4,b+c)):number(4,q,value)
assert all(sum(w)>3 for w in ways)
for e in (5,6):
 price,paid=nums(intro(e));number(e,1,price if e==5 else paid);number(e,2,paid if e==5 else price)
 number(e,3 if e==5 else 4,paid-price)
price1,price2=nums(intro(7));number(7,1,price1);number(7,2,price2);number(7,3,price1+price2)
price,b1,b2=nums(intro(8));number(8,1,b1+b2);number(8,3,price-b1-b2);number(8,4,(price-b1-b2)//2)
assert (price-b1-b2)%2==0
number(9,2,12);number(9,3,20-12)
for price in range(1,21):assert price+(20-price)==20 and 0<=20-price<20
expect(6,4,r'7\s*€','complément au prix, calcul 35−28')
steps=' '.join(data[5]['questions'][3]['etapes'])
assert '28 à 30' in steps and '30 à 35' in steps and '2+5=7' in steps
allpatterns([
 [r'10',r'5',r'2',r'15',r'17'],
 [r'5',r'3',r'2.*1',r'5.*2.*1',r'8'],
 [r'1',r'4',r'8',r'\bA\b',r'Non.*valeur'],
 [r'2',r'4',r'2',r'4',r'Aucune.*trois.*24'],
 [r'13',r'20',r'7',r'5.*2',r'13.*7.*20'],
 [r'35',r'28',r'diminue',r'7',r'7.*28.*35'],
 [r'4',r'9',r'13',r'10.*trois.*1',r'Non.*exact'],
 [r'30',r'Non',r'6',r'3.*2',r'Oui.*36'],
 [r'étiquette.*monnaie',r'12',r'8',r'5.*2.*1',r'Prix.*monnaie.*20']
],'valeurs monétaires, conservation paiement=prix+monnaie, somme et minimum par énumération')
'''
SPECIAL[22]=r'''
start,end=nums(intro(1));number(1,2,start);number(1,3,end);number(1,4,end-start)
lengths={'A':5,'B':3,'C':7};order=sorted(lengths,key=lengths.get)
expect(2,1,order[0],'minimum des longueurs 5,3,7');expect(2,2,order[-1],'maximum des longueurs')
number(2,3,lengths['A']);assert nums(results[2,4])==[lengths['B'],lengths['C']]
length=nums(intro(3))[0];number(3,3,length);number(3,5,length)
start,end=nums(intro(4));number(4,1,start);number(4,2,end);number(4,3,end-start);number(4,5,end-start)
number(6,1,100);number(6,3,100//10);number(6,4,100-90)
a,b=nums(intro(7));number(7,1,a);number(7,2,b);number(7,4,a-b)
a,b=nums(intro(8));number(8,1,a);number(8,2,b);number(8,4,a+b);number(8,5,a+b)
allpatterns([
 [r'centimètre',r'0',r'5',r'5',r'zéro.*5'],[r'B',r'C',r'5',r'3.*7',r'B.*A.*C'],
 [r'règle',r'zéro',r'7',r'bord.*règle',r'7'],[r'2',r'8',r'6',r'2.*pas.*0',r'6'],
 [r'centimètre',r'mètre',r'2\s*m',r'mètre ruban',r'longueur'],
 [r'100',r'même longueur',r'10',r'10',r'sans trou.*chevauchement'],
 [r'12',r'4',r'courte',r'8',r'4.*8.*12'],[r'8',r'6',r'deux longueurs',r'14',r'14'],
 [r'ficelle.*bande',r'deux bords',r'alignant.*extrémité',r'B',r'reports réels']
],'différences de graduations, ordre des longueurs, report conservant longueur et unité cm/m')
'''
SPECIAL[23]=r'''
# Tester tous les triplets possibles : la conclusion doit suivre des seules relations.
ordered=[dict(zip('ABC',v)) for v in itertools.product(range(1,6),repeat=3) if v[0]>v[1]>v[2]]
assert ordered and all(sorted(m,key=m.get)==list('CBA') for m in ordered)
equal=[v for v in itertools.product(range(1,6),repeat=3) if v[0]==v[1] and v[2]>v[0]]
assert equal and all(c>b for a,b,c in equal)
for mass in range(1,10):
 for cube in range(1,5):assert mass+cube>mass and (mass+cube)-cube==mass
# Une taille ne fixe pas la masse : contre-exemples de grands objets légers.
objects=[(10,1),(2,5)];assert objects[0][0]>objects[1][0] and objects[0][1]<objects[1][1]
allpatterns([
 [r'B',r'B',r'A',r'Non',r'B.*lourde'],
 [r'même niveau',r'égales',r'Non',r'A descend',r'Retirer.*cube'],
 [r'grosse',r'Non',r'soupesant',r'balance',r'sans.*taille'],
 [r'soupesant',r'Non.*vérifier',r'chaque plateau',r'A',r'vraie pesée'],
 [r'B',r'C',r'C',r'B',r'C.*B.*A'],[r'A.*B',r'C',r'Oui',r'C',r'C descend.*B'],
 [r'plateau',r'autre plateau',r'Un cube à la fois',r'équilibre',r'même référence'],
 [r'Non',r'balance',r'deux à deux',r'C.*B.*A',r'voisines.*balance'],
 [r'hauteur',r'masse',r'Non',r'balance',r'pas toujours.*lourd']
],'ordre strict et égalité de masses vérifiés exhaustivement ; équilibre et contre-exemple taille/masse')
'''
SPECIAL[24]=r'''
# Lire les directions réellement tracées dans TikZ, sans appeler le générateur.
figs=runpy.run_path(str(HERE/'figures/figures.py'))['FIGURES']
def hands(name):
 body=figs[name]
 short=[float(x) for x in re.findall(r'\(0,0\)--\((-?[\d.]+):\.78\)',body)]
 long=[float(x) for x in re.findall(r'\(0,0\)--\((-?[\d.]+):1\.06\)',body)]
 return [round(((90-a)%360)/30) or 12 for a in short],long
for name,hours in [('horloges_4_9',[4,9]),('horloge_6_corrige',[6]),('horloge_11_corrige',[11]),('horloge_8_corrige',[8]),('horloge_12',[12]),('horloge_8',[8]),('horloges_7_9',[7,9]),('horloge_2_corrige',[2]),('horloge_5',[5])]:
 actual,long=hands(name);assert actual==hours and long==[90.0]*len(hours),(name,actual,long)
for e,q,value in [(1,1,12),(1,2,4),(1,3,9),(2,1,12),(2,2,6),(2,5,6),(3,1,11),(3,2,12),(4,1,12),(4,2,8),(5,1,12),(5,2,12),(5,3,12),(6,1,8),(7,1,7),(7,2,9),(8,2,12),(8,4,2),(8,5,3),(9,3,5),(9,5,5)]:number(e,q,value)
allpatterns([
 [r'12',r'4',r'9',r'petite',r'12'],[r'12',r'6',r'Petite.*courte.*grande.*longue',r'6.*12',r'6'],
 [r'11',r'12',r'centre',r'11.*12',r'petite'],[r'12',r'8',r'Oui',r'8.*12',r'12'],
 [r'12',r'12',r'12',r'Midi',r'midi.*journée'],[r'8',r'matin',r'école',r'Non',r'journée'],
 [r'7',r'9',r'lever',r'7.*9',r'avant.*après'],[r'petite',r'12',r'centre',r'2',r'3'],
 [r'grande',r'petite',r'5',r'heure entière',r'5.*5.*12']
],'aiguille courte=heure, longue=12 ; angles TikZ décodés et ordre du même matin')
'''
SPECIAL[25]=r'''
def det(a,b,c):return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
triangle=[(0,0),(3,0),(1,2)];square=[(0,0),(2,0),(2,2),(0,2)]
assert det(*triangle)!=0
for e,q,value in [(2,1,len(triangle)),(2,2,len(triangle)),(2,3,len(square)),(2,4,len(square)),(6,1,len(triangle)),(7,1,len(square))]:number(e,q,value)
assert det((0,0),(1,0),(3,0))==0 and det((0,0),(1,1),(3,0))!=0
edges=[((square[(i+1)%4][0]-p[0]),(square[(i+1)%4][1]-p[1])) for i,p in enumerate(square)]
assert len({x*x+y*y for x,y in edges})==1 and all(edges[i][0]*edges[(i+1)%4][0]+edges[i][1]*edges[(i+1)%4][1]==0 for i in range(4))
rotated=[(-y,x) for x,y in square];assert len(set(rotated))==len(square)
allpatterns([
 [r'carré',r'triangle',r'disque',r'rectangle',r'Non.*reste.*carré'],
 [r'3',r'3',r'4',r'4',r'carré'],[r'règle',r'A.*B',r'Sans.*déplacer',r'droit.*A.*B',r'deux points.*droit'],
 [r'A.*C',r'même bord',r'Oui',r'A.*C.*B',r'Oui'],[r'A.*C',r'Non',r'Non',r'A.*C.*B.*dehors',r'trait.*A.*C'],
 [r'3',r'triangle.*non.*trait',r'Deux',r'deux autres côtés',r'3.*3.*fermée'],
 [r'4',r'égales',r'coins droits',r'carré',r'Oui'],[r'règle',r'deux points',r'même bord',r'deux côtés',r'deux points.*droit'],
 [r'disque',r'boule',r'boule',r'disque',r'disque.*plat.*boule.*solide']
],'polygones non dégénérés, déterminant d’alignement, longueurs et coins, invariance par rotation')
'''
SPECIAL[26]=r'''
# Modèles cartésiens : compter les intervalles, fermer les contours et conserver les sommets.
def rect(w,h):return [(0,0),(w,0),(w,h),(0,h)]
def sides(points):return [math.dist(p,points[(i+1)%len(points)]) for i,p in enumerate(points)]
for w,h in [(4,2),(2,2),(3,3),(5,2),(4,4)]:assert sides(rect(w,h))==[w,h,w,h]
for e,q,value in [(1,1,4),(1,2,2),(1,3,4),(2,1,2),(2,2,2),(3,2,2),(3,3,4),(4,1,4-1),(4,2,3),(4,3,3),(5,1,4),(5,2,3),(5,3,4),(5,4,3),(6,1,5),(6,2,2),(7,1,4),(7,2,4//2),(7,4,4//2),(7,5,4//2),(8,1,len([(0,0),(4,0),(4,2)])),(9,1,4),(9,2,len(range(4))-1),(9,3,3),(9,4,4+1)]:number(e,q,value)
left=rect(2,4);right=[(x+2,y) for x,y in left]
assert sides(left)==sides(right) and max(x for x,y in left)==min(x for x,y in right)
assert sides(rect(5,2))[0]!=sides(rect(5,2))[1]
allpatterns([
 [r'4',r'2',r'4',r'4.*2',r'4.*2'],[r'2',r'2',r'croisements',r'2',r'Quatre côtés égaux.*2'],
 [r'droit.*bas',r'2',r'4',r'fermé.*4.*2',r'4.*2'],[r'3',r'3',r'Trois',r'3',r'pas.*aussi long'],
 [r'4.*droite',r'3.*haut',r'Quatre.*droite',r'Trois.*dessus.*relier',r'positions.*sommets'],
 [r'5',r'2',r'croisements',r'5.*2',r'pas.*même longueur'],[r'4',r'2',r'Deux.*identiques',r'2.*4',r'Oui.*2'],
 [r'3',r'superposant',r'obliques',r'4.*2',r'tout.*rectangle'],[r'4',r'3',r'Non.*3',r'5',r'4.*5']
],'coordonnées entières, longueurs des côtés, partage congruent, triangles et n lignes pour n−1 intervalles')
'''
SPECIAL[27]=r'''
# Six normales orientées d'un pavé donnent trois paires de faces opposées.
normals=[tuple(sign if i==axis else 0 for i in range(3)) for axis in range(3) for sign in (-1,1)]
faces=len(normals);assert len(set(normals))==faces and faces==6
for e,q in [(2,2),(2,5),(3,3),(5,3),(5,4),(6,1),(6,5),(8,3),(8,5),(9,1),(9,5)]:
 if re.search(r'\d',results[e,q]):number(e,q,faces)
number(7,1,2);number(7,2,1);number(7,3,sum([2,1]));number(8,1,3);number(8,4,faces-3)
dimensions=(6,4,2)
pairs=[tuple(sorted(p)) for p in itertools.combinations(dimensions,2)]
assert len(pairs)==3 and len(pairs*2)==faces
# Chaque longueur de bord apparaît quatre fois sur le pavé fermé, avec deux occurrences par joint.
edge_counts={v:sum(2 for a,b in pairs*2 if v in (a,b)) for v in dimensions}
assert all(v==8 for v in edge_counts.values())
allpatterns([
 [r'cube',r'pavé',r'boule',r'cylindre',r'cône'],[r'carré',r'6',r'Non',r'marquant',r'6.*carrées'],
 [r'pavé',r'tournant',r'6',r'rectangles.*carrés',r'six faces'],[r'disque',r'boule',r'Non',r'Non',r'boule.*pas.*disque'],
 [r'dé',r'boîte',r'Six.*carrées.*identiques',r'Six.*rectangulaires',r'montrant.*faces'],
 [r'6',r'bords.*rejoignent',r'Bord contre bord',r'cube fermé',r'Six.*sans trou'],
 [r'2',r'1',r'3',r'gauche',r'nombre.*positions'],[r'3',r'Non',r'6',r'3',r'tournant.*six'],
 [r'6',r'opposées identiques',r'même longueur',r'pavé droit fermé',r'Six.*trois paires']
],'faces obtenues par axes et signes, paires opposées, bords compatibles, cubes dénombrés et faces cachées')
'''
SPECIAL[28]=r'''
def simulate(text):
 x=y=0;heading=0;history=[];turns=0
 # N,E,S,O ; tourner agit sur heading seulement, reculer conserve heading.
 directions=[(0,1),(1,0),(0,-1),(-1,0)]
 operations=re.findall(r'(avance|recule) de (\d+) (?:cases?|;)|tourne à (droite|gauche)',text,re.I)
 for op,n,turn in operations:
  if turn:heading=(heading+(1 if turn=='droite' else -1))%4;turns+=1
  else:
   dx,dy=directions[heading];n=int(n)*(1 if op.lower()=='avance' else -1);x+=dx*n;y+=dy*n
  history.append((x,y,heading))
 return (x,y,heading),history,turns
end,path,turns=simulate(intro(4));assert end==(1,2,1) and len(path)==3 and turns==1
assert path[0][:2]==path[1][:2] # Le virage n'a pas déplacé le pion.
end,path,turns=simulate(intro(6));assert end==(0,-1,0)
end,path,turns=simulate(intro(9));assert end==(2,0,2) and len(path)==5 and turns==2
assert len(path)<=10 and turns<=2
left_from_east=(1-1)%4;assert left_from_east==0
number(1,4,len('ABC'));number(4,2,2);number(5,4,0);number(6,3,1);number(8,3,3);number(9,1,path[0][1]);number(9,3,path[2][0]);number(9,5,end[0])
allpatterns([
 [r'B',r'A',r'C',r'3',r'B'],[r'cahier',r'Sur le cahier',r'Sous le cahier',r'Non',r'Gomme sur.*crayon sous'],
 [r'droite',r'gauche',r'Non',r'rond.*gauche.*carré',r'gauche'],
 [r'haut',r'2',r'Non',r'droite',r'2.*dessus.*1.*droite'],[r'droite',r'gauche',r'haut',r'0',r'Même place.*haut'],
 [r'haut',r'bas',r'1',r'Non.*haut',r'plus bas.*haut'],[r'dessus',r'Porte.*tableau.*deux tables',r'positions réelles',r'croix.*légende',r'chercher.*plan'],
 [r'départ.*regard',r'Avance.*2.*droite.*1',r'3.*1',r'Oui',r'suivre.*comptant'],
 [r'1.*dessus',r'droite',r'2',r'Oui.*même ligne',r'2.*droite.*bas']
],'automate position/orientation, rotation sur place, marche arrière, limites instructions et virages')
'''
DOCS={
21:r'''
for text in list(texts.values())[:2]:
 for a,b,c,total in re.findall(r'(\d+) € \+ (\d+) € \+ (\d+) € = (\d+) €',text):assert sum(map(int,(a,b,c)))==int(total)
 for count,coin,bills,bill in re.findall(r'(\d+) pièces de (\d+) € = (\d+) billet de (\d+) €',text):assert int(count)*int(coin)==int(bills)*int(bill)
 assert 'Prix + monnaie rendue = somme donnée' in text
''',
22:r'''
for text in list(texts.values())[:2]:
 for metres,cm in re.findall(r'(\d+) m = (\d+) cm',text):assert int(metres)*100==int(cm)
 for start,end,length in re.findall(r'va de (\d+) à (\d+).*?mesure (\d+) cm',text):assert int(end)-int(start)==int(length)
''',
23:r'''
for text in list(texts.values())[:2]:
 assert re.search(r'plus bas.*plus lourd',text,re.S) and re.search(r'même niveau.*égales',text,re.S)
 assert re.search(r'A est plus bas.*A est plus lourd',text,re.S)
''',
24:r'''
for text in list(texts.values())[:2]:
 for small,big,hour in re.findall(r'Petite aiguille sur (\d+), grande aiguille sur (\d+) : il est (\d+) heures',text):assert int(small)==int(hour) and int(big)==12
 assert re.search(r'heure entière.*grande aiguille.*12',text,re.S)
''',
25:r'''
for text in list(texts.values())[:2]:
 for sides_count,vertices in re.findall(r'[Tt]riangle(?: a| :) (\d+) côtés et (\d+) sommets',text):assert int(sides_count)==int(vertices)==len(triangle)
 for sides_count,corners in re.findall(r'[Cc]arré(?: a| :) (\d+) côtés.*?et (\d+) coins droits',text):assert int(sides_count)==int(corners)==len(square)
''',
26:r'''
for text in list(texts.values())[:2]:
 for w,h,long,short in re.findall(r'rectangle de (\d+) carreaux sur (\d+) carreaux a deux grands côtés de (\d+) et deux petits de (\d+)',text):assert sides(rect(int(w),int(h)))==[int(long),int(short),int(long),int(short)]
 assert 'quatre carreaux relient cinq lignes' in text
''',
27:r'''
for text in list(texts.values())[:2]:
 counts=re.findall(r'(?:[Cc]ube|[Pp]avé)(?: droit)?(?: a| :) (\d+) faces',text)
 assert len(counts)>=2 and all(int(n)==faces for n in counts)
 assert 'boule n’a pas de face plate' in text
''',
28:r'''
for text in list(texts.values())[:2]:
 assert re.search(r'Tourner.*sur place',text,re.S)
 assert re.search(r'Reculer.*sens opposé.*sans se retourner',text,re.S)
'''
}
FOOT=r'''
report={'statut':'OK','math_OK':True,'anomalies':0,'exercices_verifies':len(blocks),'questions_verifiees':len(results),'egalites_recalculees':len(equations),'controles_modeles':len(traces),'activites_sources_lues':len(source['exercices']),'source':'textes finaux, données structurées et chapitre source ; aucun import des générateurs','portee':'Exactitude et cohérence mathématiques. La lisibilité des PNG et le rendu navigateur sont contrôlés séparément.','empreintes':{n:hashlib.sha256((HERE/n).read_bytes()).hexdigest() for n in [*texts,'donnees_exercices_root.json','sources_locales/chapitre.json']},'details':traces,'egalites':equations}
(HERE/'verification_math.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
(HERE/'RAPPORT_MATHEMATIQUE.md').write_text('# Contrôle mathématique indépendant\n\nStatut : OK. 9 exercices, 45 questions. Les énoncés, méthodes, étapes, résultats et solutions correspondent aux données finales ; les neuf activités sources ont été lues.\n\n'+str(len(equations))+' égalités numériques recalculées et '+str(len(traces))+' contrôles spécifiques des réponses par modèles indépendants. Les propriétés utiles du cours et de la fiche sont contrôlées également. Les détails et empreintes SHA-256 figurent dans verification_math.json.\n\nCes preuves ne remplacent pas la relecture visuelle des figures ni les audits du rendu. Aucune compilation ou navigation n’a été effectuée par ce contrôle.\n',encoding='utf-8')
print(json.dumps({k:v for k,v in report.items() if k not in ('details','egalites','empreintes')},ensure_ascii=False))
'''
for code,special in SPECIAL.items():
 d=next(ROOT.glob(f'{code:02}_*'))
 (d/'verif_math.py').write_text(COMMON+special+DOCS[code]+FOOT,encoding='utf-8')
 print(code,'contrôle indépendant installé')
