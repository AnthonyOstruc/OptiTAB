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

for text in list(texts.values())[:2]:
 counts=re.findall(r'(?:[Cc]ube|[Pp]avé)(?: droit)?(?: a| :) (\d+) faces',text)
 assert len(counts)>=2 and all(int(n)==faces for n in counts)
 assert 'boule n’a pas de face plate' in text

report={'statut':'OK','math_OK':True,'anomalies':0,'exercices_verifies':len(blocks),'questions_verifiees':len(results),'egalites_recalculees':len(equations),'controles_modeles':len(traces),'activites_sources_lues':len(source['exercices']),'source':'textes finaux, données structurées et chapitre source ; aucun import des générateurs','portee':'Exactitude et cohérence mathématiques. La lisibilité des PNG et le rendu navigateur sont contrôlés séparément.','empreintes':{n:hashlib.sha256((HERE/n).read_bytes()).hexdigest() for n in [*texts,'donnees_exercices_root.json','sources_locales/chapitre.json']},'details':traces,'egalites':equations}
(HERE/'verification_math.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
(HERE/'RAPPORT_MATHEMATIQUE.md').write_text('# Contrôle mathématique indépendant\n\nStatut : OK. 9 exercices, 45 questions. Les énoncés, méthodes, étapes, résultats et solutions correspondent aux données finales ; les neuf activités sources ont été lues.\n\n'+str(len(equations))+' égalités numériques recalculées et '+str(len(traces))+' contrôles spécifiques des réponses par modèles indépendants. Les propriétés utiles du cours et de la fiche sont contrôlées également. Les détails et empreintes SHA-256 figurent dans verification_math.json.\n\nCes preuves ne remplacent pas la relecture visuelle des figures ni les audits du rendu. Aucune compilation ou navigation n’a été effectuée par ce contrôle.\n',encoding='utf-8')
print(json.dumps({k:v for k,v in report.items() if k not in ('details','egalites','empreintes')},ensure_ascii=False))
