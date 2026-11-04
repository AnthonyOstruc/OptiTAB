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

for text in list(texts.values())[:2]:
 for small,big,hour in re.findall(r'Petite aiguille sur (\d+), grande aiguille sur (\d+) : il est (\d+) heures',text):assert int(small)==int(hour) and int(big)==12
 assert re.search(r'heure entière.*grande aiguille.*12',text,re.S)

report={'statut':'OK','math_OK':True,'anomalies':0,'exercices_verifies':len(blocks),'questions_verifiees':len(results),'egalites_recalculees':len(equations),'controles_modeles':len(traces),'activites_sources_lues':len(source['exercices']),'source':'textes finaux, données structurées et chapitre source ; aucun import des générateurs','portee':'Exactitude et cohérence mathématiques. La lisibilité des PNG et le rendu navigateur sont contrôlés séparément.','empreintes':{n:hashlib.sha256((HERE/n).read_bytes()).hexdigest() for n in [*texts,'donnees_exercices_root.json','sources_locales/chapitre.json']},'details':traces,'egalites':equations}
(HERE/'verification_math.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
(HERE/'RAPPORT_MATHEMATIQUE.md').write_text('# Contrôle mathématique indépendant\n\nStatut : OK. 9 exercices, 45 questions. Les énoncés, méthodes, étapes, résultats et solutions correspondent aux données finales ; les neuf activités sources ont été lues.\n\n'+str(len(equations))+' égalités numériques recalculées et '+str(len(traces))+' contrôles spécifiques des réponses par modèles indépendants. Les propriétés utiles du cours et de la fiche sont contrôlées également. Les détails et empreintes SHA-256 figurent dans verification_math.json.\n\nCes preuves ne remplacent pas la relecture visuelle des figures ni les audits du rendu. Aucune compilation ou navigation n’a été effectuée par ce contrôle.\n',encoding='utf-8')
print(json.dumps({k:v for k,v in report.items() if k not in ('details','egalites','empreintes')},ensure_ascii=False))
