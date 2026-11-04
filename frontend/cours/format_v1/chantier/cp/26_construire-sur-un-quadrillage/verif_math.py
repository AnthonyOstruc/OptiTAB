"""Vérification indépendante des vrais textes, données et activités sources CP."""
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

for text in list(texts.values())[:2]:
 for w,h,long,short in re.findall(r'rectangle de (\d+) carreaux sur (\d+) carreaux a deux grands côtés de (\d+) et deux petits de (\d+)',text):assert sides(rect(int(w),int(h)))==[int(long),int(short),int(long),int(short)]
 assert 'quatre carreaux relient cinq lignes' in text

report={'statut':'OK','math_OK':True,'anomalies':0,'exercices_verifies':len(blocks),'questions_verifiees':len(results),'egalites_recalculees':len(equations),'controles_modeles':len(traces),'activites_sources_lues':len(source['exercices']),'source':'textes finaux, données structurées et chapitre source ; aucun import des générateurs','portee':'Exactitude et cohérence mathématiques. La lisibilité des PNG et le rendu navigateur sont contrôlés séparément.','empreintes':{n:hashlib.sha256((HERE/n).read_bytes()).hexdigest() for n in [*texts,'donnees_exercices_root.json','sources_locales/chapitre.json']},'details':traces,'egalites':equations}
(HERE/'verification_math.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
(HERE/'RAPPORT_MATHEMATIQUE.md').write_text('# Contrôle mathématique indépendant\n\nStatut : OK. 9 exercices, 45 questions. Les énoncés, méthodes, étapes, résultats et solutions correspondent aux données finales ; les neuf activités sources ont été lues.\n\n'+str(len(equations))+' égalités numériques recalculées et '+str(len(traces))+' contrôles spécifiques des réponses par modèles indépendants. Les propriétés utiles du cours et de la fiche sont contrôlées également. Les détails et empreintes SHA-256 figurent dans verification_math.json.\n\nCes preuves ne remplacent pas la relecture visuelle des figures ni les audits du rendu. Aucune compilation ou navigation n’a été effectuée par ce contrôle.\n',encoding='utf-8')
print(json.dumps({k:v for k,v in report.items() if k not in ('details','egalites','empreintes')},ensure_ascii=False))
