# -*- coding: utf-8 -*-
"""Audit autonome : relit les vrais textes, recompose chaque égalité et réponse.
Ne charge pas le générateur. Analyse AST arithmétique indépendante et Fraction.
"""
from pathlib import Path
from fractions import Fraction
import ast,json,re,hashlib,runpy
P=Path(__file__).resolve().parent
def value(s):
 s=s.replace(r'\,','').replace(r'\times','*').replace(r'\div','/').replace(' ','')
 t=ast.parse(s,mode='eval').body
 def walk(x):
  if isinstance(x,ast.Constant) and isinstance(x.value,int):return Fraction(x.value)
  if isinstance(x,ast.UnaryOp) and isinstance(x.op,ast.USub):return -walk(x.operand)
  if isinstance(x,ast.BinOp):
   a,b=walk(x.left),walk(x.right)
   if isinstance(x.op,ast.Add):return a+b
   if isinstance(x.op,ast.Sub):return a-b
   if isinstance(x.op,ast.Mult):return a*b
   if isinstance(x.op,ast.Div):return a/b
   if isinstance(x.op,ast.FloorDiv):return a//b
   if isinstance(x.op,ast.Mod):return a%b
  raise ValueError(s)
 return walk(t)
texts={f:(P/f).read_text(encoding='utf8') for f in ('cours_nouveau.txt','fiche_nouvelle.txt','exercices.txt')}
equalities=0
for f,content in texts.items():
 for m in re.finditer(r'(?<!\$)\${1,2}([^$]+)\${1,2}',content):
  s=m[1].strip()
  if '=' not in s:continue
  parts=s.split('=')
  try: vals=list(map(value,parts))
  except (ValueError,SyntaxError):raise AssertionError((f,'égalité non vérifiée',s))
  assert all(x==vals[0] for x in vals),(f,s,vals)
  assert all(0<=v<=10000 for v in vals),(f,'borne CE2',s)
  equalities+=1
blocks=re.split(r'^===[ \t]*$',texts['exercices.txt'],flags=re.M)
blocks=[b for b in blocks if b.strip()]
assert len(blocks)==9
source=json.loads((P/'sources_locales/chapitre.json').read_text(encoding='utf8'))
questions=0
for i,b in enumerate(blocks,1):
 assert re.search(r'^Id: nouveau-'+str(i)+r'$',b,re.M)
 enonce=b.split('Énoncé:\n')[1].split('Étapes:\n')[0]
 steps=b.split('Étapes:\n')[1].split('Solution:\n')[0]
 solution=b.split('Solution:\n')[1]
 qs=re.findall(r'^(\d+)\. (.+)',enonce,re.M)
 assert len(qs)==5,(i,len(qs))
 assert [int(k) for k,_ in qs]==[1,2,3,4,5]
 assert len(re.findall(r'^## Question ',steps,re.M))==5
 assert len(re.findall(r'^::: methode',steps,re.M))==5
 assert len(re.findall(r'^::: resultat',steps,re.M))==5
 # Les réponses de chaque question sont identiques dans résultat et solution.
 results=re.findall(r'^::: resultat\n([\s\S]*?)\n:::',steps,re.M)
 sols=re.findall(r'^\d+\. (.*)',solution,re.M)
 assert results==sols,(i,'résultat/solution')
 assert results[0]==source['exercices'][i-1]['reponse'],(i,'réponse source altérée')
 assert source['exercices'][i-1]['consigne'] in enonce,(i,'couverture source')
 # Les calculs issus du livre sont recomposés indépendamment depuis leur AST.
 for check in source['exercices'][i-1]['check'].split(' and '):
  if not check:continue
  lhs,rhs=check.split('==');assert value(lhs)==value(rhs),(i,check)
  if '%' not in lhs:
   actual_numbers=[int(x.replace(' ','')) for x in re.findall(r'\d+(?: \d{3})*',results[0])]
   if int(value(rhs)) not in actual_numbers:
    assert source['exercices'][i-1]['consigne'].startswith('Complète'),(i,'résultat numérique absent de la réponse',rhs,results[0])
    # Pour une égalité à compléter, la réponse est un terme ou un facteur.
    assert set(map(int,re.findall(r'\d+',lhs))) & set(actual_numbers),(i,'terme ou facteur manquant non retrouvé')
 questions+=len(qs)
figures=runpy.run_path(str(P/'figures/figures.py'))['FIGURES']
figures_checked=0
for name,tikz in figures.items():
 # Recomposer les opérations posées depuis les chiffres réellement dessinés.
 rows={}
 for color,x,y,digit in re.findall(r'\\node\[text=(otInk|otGreenDark)\] at \((\d+),(-?[\d.]+)\) \{\$(\d)\$\};',tikz):
  rows.setdefault((color,float(y)),{})[int(x)]=int(digit)
 if not rows:continue
 def number(ds):return sum(d*10**(3-k) for k,d in ds.items())
 inputs=[number(v) for (color,y),v in sorted(rows.items(),key=lambda kv:-kv[0][1]) if color=='otInk']
 result=[number(v) for (color,y),v in rows.items() if color=='otGreenDark']
 if not result:continue
 if r'\times' in tikz:
  assert inputs[0]*inputs[1]==result[0],(name,inputs,result)
  if len(inputs)==4:
   assert inputs[2]==inputs[0]*(inputs[1]%10)
   assert inputs[3]==inputs[0]*(inputs[1]//10)*10
   assert inputs[2]+inputs[3]==result[0]
 elif '{$-$}' in tikz:assert inputs[0]-inputs[1]==result[0]
 else:assert sum(inputs)==result[0]
 figures_checked+=1
report={'statut':'OK','math_OK':True,'exercices':len(blocks),'questions':questions,'egalites_recomposees':equalities,'empreintes':{f:hashlib.sha256(s.encode('utf8')).hexdigest() for f,s in texts.items()}}
report['figures_operations_recomposees']=figures_checked
(P/'verification_math.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print(json.dumps(report,ensure_ascii=False))
