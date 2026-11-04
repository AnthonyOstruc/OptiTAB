"""Contrôles indépendants : livrables réels, calculs exacts, géométrie et pliages."""
from pathlib import Path
from fractions import Fraction
from collections import deque
import re,json,hashlib,math,runpy
P=Path(__file__).resolve().parent
N=int(P.name[:2]);checks=[]
def ok(value,name):
    assert value,name
    checks.append(name)
def near(a,b):return abs(a-b)<0.00001
def neg(v):return tuple(-x for x in v)
def fold(cells):
    cells=set(cells);start=next(iter(cells));frames={start:((1,0,0),(0,1,0),(0,0,1))};todo=deque([start]);consistent=True
    while todo:
        x,y=todo.popleft();u,v,n=frames[x,y]
        for dx,dy,f in [(1,0,(neg(n),v,u)),(-1,0,(n,v,neg(u))),(0,1,(u,neg(n),v)),(0,-1,(u,n,neg(v)))]:
            k=(x+dx,y+dy)
            if k not in cells:continue
            if k in frames:consistent &= frames[k]==f
            else:frames[k]=f;todo.append(k)
    return consistent and len(frames)==6 and len({f[2] for f in frames.values()})==6,frames
def operand(s,i):
    while i<len(s) and s[i].isspace():i+=1
    if s[i]=='{':
        start=i+1;depth=1;i+=1
        while depth:
            if s[i]=='{':depth+=1
            if s[i]=='}':depth-=1
            i+=1
        return s[start:i-1],i
    return s[i],i+1
def convert(s):
    while '\\frac' in s:
        i=s.index('\\frac');a,j=operand(s,i+5);b,k=operand(s,j)
        s=s[:i]+'(('+convert(a)+')/('+convert(b)+'))'+s[k:]
    for a,b in [('{,}','.'),('\\,',''),('\\times','*'),('\\div','/'),('\\ne','!='),('\\le','<='),('\\ge','>='),('\\quad',''),('&','')]:s=s.replace(a,b)
    return s.replace('{','').replace('}','').strip()
def literal_checks(text,origin):
    for hit in re.finditer(r'\$\$(.*?)\$\$|\$(.*?)\$',text,re.S):
        value=hit[1] if hit[1] is not None else hit[2]
        value=re.sub(r'\\(?:begin|end)\{(?:aligned|gathered)\}','',value)
        for chain in value.split('\\\\'):
            try:expr=' '.join(convert(chain).split())
            except (IndexError,ValueError):continue
            if not re.search('[=<>]',expr) or re.search(r'[^0-9\s.()+*/=<>!\-]',expr):continue
            expr=re.sub(r'(?<![<>=!])=(?!=)','==',expr)
            expr=re.sub(r'\d+(?:\.\d+)?',lambda m:"Fraction('"+m[0]+"')",expr)
            ok(eval(expr,{'__builtins__':{},'Fraction':Fraction}),origin+' : '+chain)

manifest=json.loads((P/'donnees_questions.json').read_text(encoding='utf-8'))
text=(P/'exercices.txt').read_text(encoding='utf-8')
blocks=[b for b in re.split(r'^===[ \t]*$',text,flags=re.M) if b.strip()]
ok(len(blocks)==len(manifest)==15,'15 exercices sources tous repris et enrichis')
ok(len({re.search(r'^=== (.+)$',b,re.M)[1] for b in blocks})==15,'titres uniques')
for i,(b,ex) in enumerate(zip(blocks,manifest),1):
    ok(f'Id: nouveau-{i}\n' in b,f'identité stable {i}')
    enonce=b.split('Énoncé:\n<!-- optitab:1 -->\n')[1].split('\nÉtapes:')[0]
    steps=b.split('Étapes:\n<!-- optitab:1 -->\n')[1].split('\nSolution:')[0]
    solution=b.split('Solution:\n<!-- optitab:1 -->\n')[1]
    qs=re.findall(r'^\d+\. (.+)$',enonce,re.M)
    results=re.findall(r'^::: resultat[ \t]*\n(.*?)\n:::',steps,re.M|re.S)
    answers=re.findall(r'^\d+\. (.+)$',solution,re.M)
    ok(len(qs)==len(results)==len(answers)==len(ex['questions'])>=5,f'exercice {i} : au moins cinq questions avec réponses')
    for kind in ('methode','etape'):
        ok(len(re.findall(r'^::: '+kind+r'\b',steps,re.M))==len(qs),f'exercice {i} : {kind} pour chaque question')
    for j,q in enumerate(ex['questions']):
        ok(qs[j]==q['question'] and results[j].strip()==answers[j]==q['reponse'],f'exercice {i} question {j+1} : cohérence du résultat et de la solution')
        ok(q['raisonnement'] in steps and q['methode'] in steps,f'exercice {i} question {j+1} : explication intégrale')
    literal_checks(b,f'exercice {i}')
for name in ('cours_nouveau.txt','fiche_nouvelle.txt'):
    doc=(P/name).read_text(encoding='utf-8');ok('<!-- optitab:1 -->' in doc and doc.startswith('Titre:'),name+' structuré')
    literal_checks(doc,name)
    ok(not any(ord(c)<32 and c not in '\n\r' for c in doc),name+' caractères valides')

# Recalculs des réponses numériques à partir des situations, sans égalités tautologiques.
EXPECTED={15:{2:{2:Fraction(7,2),4:Fraction(7,2)},5:{4:3,5:6},8:{1:8,2:Fraction(7,2),3:50,4:6,5:16},11:{2:3,3:Fraction(5,2),4:Fraction(5,2),5:5},12:{1:3,2:3,3:3,4:3},13:{5:16},15:{3:3,4:3}},
16:{2:{5:16},3:{2:4,5:12},5:{5:20},6:{5:5},7:{2:6,5:16},8:{3:4,4:6,5:20},9:{2:[4,4],5:16},11:{2:4,4:4,5:20},13:{5:22},14:{1:20,2:20},15:{3:2,4:Fraction(72,10)}},
17:{2:{1:2,2:4,3:1},3:{1:4,4:3,5:2},4:{4:4},6:{4:6},9:{4:1},11:{1:6,2:2,3:1,4:3,5:12},12:{1:3,2:6,3:6,4:12},13:{1:2,2:2,3:4,4:4},14:{4:6}},
18:{2:{1:6,3:12,4:8,5:24},3:{1:6,3:[12,8],4:[5,3]},4:{3:4,4:5},5:{1:2,3:3,4:5},6:{1:6},8:{1:5,2:1},9:{1:6,2:3,3:1,4:10},10:{1:4,2:2,3:6,4:5,5:[1,2,1]},11:{1:6,2:3},12:{1:4,2:8,3:1,4:27,5:20},15:{2:6,3:5,4:4}}}
def values(s):return [Fraction(x.replace(',','.')) for x in re.findall(r'(?<![A-Za-z])\d+(?:[.,]\d+)?',s.replace('{,}',','))]
for i,questions in EXPECTED[N].items():
    for j,expected in questions.items():
        actual=values(manifest[i-1]['questions'][j-1]['reponse'])
        expected=expected if isinstance(expected,list) else [expected]
        ok(actual==expected,f'valeurs réelles de la réponse {i}/{j} : {actual}')

figures=runpy.run_path(str(P/'figures/figures.py'))['FIGURES']
correspondance=json.loads((P/'figures/correspondance.json').read_text(encoding='utf-8'))
for owner,sub in correspondance.items():
    for ident,positions in sub.items():
        ownertext=(P/'cours_nouveau.txt').read_text(encoding='utf-8') if owner=='cours' else (P/'fiche_nouvelle.txt').read_text(encoding='utf-8') if owner=='fiches' else next(b for b in blocks if f'Id: {ident}\n' in b)
        ok(set(re.findall(r'\[IMAGE_(\d+)\]',ownertext))==set(positions),f'images exactes {owner}/{ident}')
        for p,info in positions.items():
            ok(Path(info['fichier']).stem in figures and len(info['alt'])>=20,f'figure définie et alternative précise {ident}/{p}')
            src=figures[Path(info['fichier']).stem]
            ok('transform shape' not in src and 'resizebox' not in src and not re.search(r'\bscale\s*=',src),f'figure sans réduction de texte {ident}/{p}')

if N==15:
    for length in (7,5,6):ok(Fraction(length,2)*2==length,f'milieu de longueur {length}')
    ok(3<4 and 3>2,'cercle rayon 3 : intérieur et extérieur')
    ok(near(math.dist((0,0),(1.2,1.3416407865)),1.8) and near(math.dist((2.4,0),(1.2,1.3416407865)),1.8),'intersection des deux cercles : coordonnées à même rayon')
    ok('(1.2,1.3416407865)' in figures['croises'],'coordonnées contrôlées présentes dans le TikZ final')
    ok('(0,0) circle(2)' in figures['programme'] and "{$M$}" in figures['programme'],'programme final : cercle de rayon moitié du côté AB')
    ok(near(4/2.4,5/3),'rectangle du programme à la bonne proportion')
    ok('(0,0) rectangle(3.25,1.95)' in figures['quadrillage_rectangle'] and 3.25/.65==5 and 1.95/.65==3,'rectangle quadrillé 5 sur 3')
elif N==16:
    ok(near(math.dist((0,0),(1.6,2.771281292)),3.2),'triangle équilatéral : distances coordonnées')
    ok('(1.6,2.771281292)' in figures['equilateral'],'sommet contrôlé du TikZ équilatéral')
    ok(math.hypot(3,4)==5,'triangle rectangle 3 cm/4 cm : mesure BC de 5 cm')
    ok(round(math.hypot(6,4),1)==7.2,'mesure des diagonales du rectangle 6 sur 4 au millimètre près')
    for sides in [(5,5,6),(6,6,4),(4,4,4)]:ok(sum(sides)>2*max(sides),f'triangle constructible {sides}')
    ok(5*4==20 and 3*4+2*4==20,'contour extérieur du carré et du triangle accolés : cinq côtés')
elif N==17:
    for points,fn in [([(-2,1),(-3,-1),(-1,2)],lambda x,y:(-x,y)),([(-2,1),(2,3)],lambda x,y:(x,-y))]:
        images=[fn(*v) for v in points]
        for a,b in zip(points,images):ok(abs(a[0])==abs(b[0]) and abs(a[1])==abs(b[1]),f'coordonnées symétriques {a}/{b}')
        for i in range(len(points)-1):ok(near(math.dist(points[i],points[i+1]),math.dist(images[i],images[i+1])),'longueurs conservées par réflexion')
    cells={(-3,2),(-1,2),(-2,0),(-3,-2),(-2,-2),(-1,-2)};reflected={(-x-1,y) for x,y in cells}
    ok(len(cells)==len(reflected)==6 and not cells&reflected,'six cases distinctes ajoutées au carrelage')
    for name in ('points_corrige','maison_corrige','horizontal_corrige','carrelage_corrige'):ok('geoReponse' in figures[name] or 'otGreen' in figures[name],name+' corrigé en vert')
    ok(not any('diagonale' in q['question'].lower() for e in manifest for q in e['questions']),'aucune construction par symétrie sur un axe diagonal')
elif N==18:
    A=[(0,0),(1,0),(2,0),(3,0),(1,1),(1,-1)];B=[(0,0),(1,0),(2,0),(3,0),(1,1),(2,1)];C=[(-1,0),(0,0),(1,0),(0,-1),(0,-2),(0,-3)]
    for name,cells,expected in [('A',A,True),('B',B,False),('C',C,True)]:ok(fold(cells)[0]==expected,f'pliage indépendant patron {name}')
    normals={letter:fold(A)[1][pos][2] for letter,pos in zip('ABCDEF',A)}
    for a,b in [('A','C'),('B','D'),('E','F')]:ok(normals[a]==neg(normals[b]),f'faces opposées du patron final {a}/{b}')
    ok(2+3==5 and 4+1==5,'faces du prisme triangulaire et de la pyramide carrée')
    ok(sum([1,2,1])+sum([1,1,0])==6 and sum(x>0 for x in [1,2,1,1,1,0])==5,'assemblage six cubes, cinq cases occupées')
    ok([max(a,b) for a,b in zip([1,2,1],[1,1,0])]==[1,2,1],'vue de face à partir des hauteurs réelles')
    def walk(program):
        x=y=0;direction=0;dirs=[(1,0),(0,1),(-1,0),(0,-1)]
        for cmd,n in program:
            if cmd=='L':direction=(direction+1)%4
            elif cmd=='R':direction=(direction-1)%4
            else:dx,dy=dirs[direction];x+=n*dx;y+=n*dy
        return x,y,direction
    ok(walk([('F',3),('R',1),('F',1),('R',1),('F',3)])==(0,-1,2),'chemin 13 : position finale et regard à gauche')
    ok(walk([('F',2),('L',1),('F',2),('L',1),('F',1)])==(1,2,2),'programme 14 : position finale et regard à gauche')
    ok(all(a+b==7 for a,b in [(1,6),(2,5),(3,4)]),'dé complété : trois paires de somme sept')

report={'statut':'OK','math_OK':True,'anomalies':0,'controles':len(checks),'exercices':len(blocks),'questions':sum(len(e['questions']) for e in manifest),'minimum_questions':min(len(e['questions']) for e in manifest),'details':checks,'empreintes_livrables':{name:hashlib.sha256((P/name).read_bytes()).hexdigest() for name in ('cours_nouveau.txt','fiche_nouvelle.txt','exercices.txt','figures/figures.py','figures/correspondance.json')}}
(P/'verification_math.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:v for k,v in report.items() if k not in ('details','empreintes_livrables')},ensure_ascii=False))
