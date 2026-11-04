from pathlib import Path
import re,json,ast,operator
D=Path(__file__).resolve().parent
def calc(s):
 tree=ast.parse(s,mode='eval')
 def visit(t):
  if isinstance(t,ast.Expression):return visit(t.body)
  if isinstance(t,ast.Constant) and type(t.value)==int:return t.value
  if isinstance(t,ast.BinOp) and type(t.op) in (ast.Add,ast.Sub):return (operator.add if isinstance(t.op,ast.Add) else operator.sub)(visit(t.left),visit(t.right))
  raise AssertionError(s)
 return visit(tree)
checks=0
for name in ['cours_nouveau.txt','fiche_nouvelle.txt','exercices.txt']:
 text=(D/name).read_text(encoding='utf-8')
 for a,b in re.findall(r'(?<![\d+\-])([0-9]+(?:[+\-][0-9]+)+)=([0-9]+)',text):
  assert calc(a)==int(b),(name,a,b);checks+=1
 for a,b in re.findall(r'(?<![\d+\-])([0-9]+)=([0-9]+(?:[+\-][0-9]+)+)',text):
  assert int(a)==calc(b),(name,a,b);checks+=1
blocks=re.split(r'^===\s*$',(D/'exercices.txt').read_text(encoding='utf-8'),flags=re.M)[1:]
assert len(blocks)==9
figs=ast.literal_eval((D/'figures/figures.py').read_text(encoding='utf-8').split('=',1)[1])
corr=json.loads((D/'figures/correspondance.json').read_text(encoding='utf-8'))
def corrected(i):return figs[corr['exercices'][f'nouveau-{i}']['2']['fichier'].removesuffix('.png')]
code=int(D.name[:2])
for i,b in enumerate(blocks,1):
 en=b.split('Énoncé:',1)[1].split('Étapes:',1)[0]
 st=b.split('Étapes:',1)[1].split('Solution:',1)[0]
 sol=b.split('Solution:',1)[1]
 assert len(re.findall(r'^\d+\. ',en,re.M))>=5
 results=re.findall(r'::: resultat\n([\s\S]*?)\n:::',st)
 assert len(results)>=5
 for result in results:assert result in sol,(i,result)
 if code==17:
  intro=en.split('[IMAGE_1]')[0]
  numbers=list(map(int,re.findall(r'\d+',intro.split('<!-- optitab:1 -->')[-1])))
  if i in (4,9):expected=numbers[0]+numbers[1]
  elif i==5:expected=numbers[1]-numbers[0]
  elif i==7:expected=numbers[0]-numbers[1]-numbers[2]
  elif i==2:expected=numbers[1]-numbers[0];assert numbers[3]-numbers[2]==expected
  else:expected=numbers[0]-numbers[1]
  assert re.search(r'\b'+str(expected)+r'\b',results[3]),(i,expected,results[3])
  f=corrected(i);assert ('{'+str(expected)+'}' in f or '{'+str(expected)+' en tout}' in f),(i,expected)
 if code in (18,19):
  f=corrected(i);dots=len(re.findall(r'\\fill\[',f))
  equations=re.findall(r'([0-9]+(?:\+[0-9]+)+)=([0-9]+)',st)
  assert any(int(value)==dots for _,value in equations),(i,dots,equations)
  if code==18 and i==9:
   repair=figs[corr['exercices']['nouveau-9']['3']['fichier'].removesuffix('.png')]
   assert len(re.findall(r'\\fill\[',repair))==dots-1
  if code==19:assert dots<=30
 if code==20:
  fig=corrected(i);nums=list(map(int,re.findall(r'\{([0-9]+)\};',fig)))
  assert len(nums)==3 and all(0<=n<=30 for n in nums),(i,nums)
  eqs=[(a,int(v)) for a,v in re.findall(r'([0-9]+[+\-][0-9]+)=([0-9]+)',st)]
  assert any(calc(a)==nums[1] for a,_ in eqs) and any(calc(a)==nums[2] for a,_ in eqs)
 if code==29 and i!=5:
  matches=re.findall(r'Relevé : ([^.]+)\.',en)
  assert matches,(i,'relevé absent')
  votes=[v.strip() for v in matches[-1].split(',')]
  categories=list(dict.fromkeys(votes));assert 2<=len(categories)<=5 and len(votes)<40
  counts=[votes.count(x) for x in categories]
  fig=corrected(i);fills=len(re.findall(r'\\fill\[',fig))
  assert fills==sum(counts),(i,fills,counts)
  for label,n in zip(categories,counts):assert str(n) in st,(i,label,n)
  # Chaque colonne contient exactement le nombre de cases colorées attendu.
  coords=re.findall(r'\\fill\[[^\]]+\] \(([^,]+),',fig)
  for k,n in enumerate(counts):assert sum(abs(float(x)-(k*2+.03))<.001 for x in coords)==n,(i,k,n)
 checks+=len(results)
report={'statut':'OK','math_OK':True,'verifications':checks,'anomalies':0,'methode':'Recalcul indépendant des égalités des textes, contrôle des réponses des solutions et dénombrement des figures ; recomptage des relevés et colonnes des diagrammes.'}
(D/'verification_math.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(report,ensure_ascii=False))
