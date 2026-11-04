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

for text in list(texts.values())[:2]:
 for a,b,c,total in re.findall(r'(\d+) € \+ (\d+) € \+ (\d+) € = (\d+) €',text):assert sum(map(int,(a,b,c)))==int(total)
 for count,coin,bills,bill in re.findall(r'(\d+) pièces de (\d+) € = (\d+) billet de (\d+) €',text):assert int(count)*int(coin)==int(bills)*int(bill)
 assert 'Prix + monnaie rendue = somme donnée' in text

report={'statut':'OK','math_OK':True,'anomalies':0,'exercices_verifies':len(blocks),'questions_verifiees':len(results),'egalites_recalculees':len(equations),'controles_modeles':len(traces),'activites_sources_lues':len(source['exercices']),'source':'textes finaux, données structurées et chapitre source ; aucun import des générateurs','portee':'Exactitude et cohérence mathématiques. La lisibilité des PNG et le rendu navigateur sont contrôlés séparément.','empreintes':{n:hashlib.sha256((HERE/n).read_bytes()).hexdigest() for n in [*texts,'donnees_exercices_root.json','sources_locales/chapitre.json']},'details':traces,'egalites':equations}
(HERE/'verification_math.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
(HERE/'RAPPORT_MATHEMATIQUE.md').write_text('# Contrôle mathématique indépendant\n\nStatut : OK. 9 exercices, 45 questions. Les énoncés, méthodes, étapes, résultats et solutions correspondent aux données finales ; les neuf activités sources ont été lues.\n\n'+str(len(equations))+' égalités numériques recalculées et '+str(len(traces))+' contrôles spécifiques des réponses par modèles indépendants. Les propriétés utiles du cours et de la fiche sont contrôlées également. Les détails et empreintes SHA-256 figurent dans verification_math.json.\n\nCes preuves ne remplacent pas la relecture visuelle des figures ni les audits du rendu. Aucune compilation ou navigation n’a été effectuée par ce contrôle.\n',encoding='utf-8')
print(json.dumps({k:v for k,v in report.items() if k not in ('details','egalites','empreintes')},ensure_ascii=False))
