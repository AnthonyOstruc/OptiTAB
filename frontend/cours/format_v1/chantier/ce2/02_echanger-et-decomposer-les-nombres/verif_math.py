"""Vérification autonome des fichiers livrés et des opérations des situations."""
from pathlib import Path
import ast,json,re,hashlib,operator
from fractions import Fraction as F
P=Path(__file__).resolve().parent
def evaluate(n):
 if isinstance(n,ast.Expression):return evaluate(n.body)
 if isinstance(n,ast.Constant) and isinstance(n.value,(int,bool)):return n.value if isinstance(n.value,bool) else F(n.value)
 if isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id=='F':return F(*(evaluate(a) for a in n.args))
 if isinstance(n,ast.BinOp):return {ast.Add:operator.add,ast.Sub:operator.sub,ast.Mult:operator.mul,ast.FloorDiv:operator.floordiv,ast.Div:operator.truediv}[type(n.op)](evaluate(n.left),evaluate(n.right))
 if isinstance(n,ast.BoolOp):return all(evaluate(x) for x in n.values)
 if isinstance(n,ast.Compare):
  vals=[evaluate(n.left)]+[evaluate(c) for c in n.comparators]
  ops={ast.Eq:operator.eq,ast.NotEq:operator.ne,ast.Lt:operator.lt,ast.LtE:operator.le,ast.Gt:operator.gt,ast.GtE:operator.ge}
  return all(ops[type(o)](a,b) for o,a,b in zip(n.ops,vals,vals[1:]))
 raise ValueError(ast.dump(n))
def frac(s):return re.sub(r'(?<![\w\\])(\d+)/(\d+)(?!\w)',lambda m:r'$\dfrac{'+m[1]+'}{'+m[2]+'}$',s)
source=json.loads((P/'sources_locales/chapitre.json').read_text(encoding='utf-8'))
plan=json.loads((P/'situations_verifiees.json').read_text(encoding='utf-8'))
txt=(P/'exercices.txt').read_text(encoding='utf-8')
blocks=[x for x in re.split(r'^===[ \t]*$',txt,flags=re.M) if x.strip()]
assert len(blocks)==len(source['exercices'])==len(plan)==9
checks=0
for i,(b,model,original) in enumerate(zip(blocks,plan,source['exercices']),1):
 assert f'Id: nouveau-{i}\n' in b
 enonce=b.split('Énoncé:\n',1)[1].split('\nÉtapes:',1)[0]
 steps=b.split('Étapes:\n',1)[1].split('\nSolution:',1)[0]
 sol=b.split('Solution:\n',1)[1]
 assert len(re.findall(r'^\d+\. ',enonce,re.M))==5
 assert len(re.findall(r'^## Question \d+ :',steps,re.M))==5
 assert frac(original['consigne']) in enonce,(i,'couverture source')
 if original.get('check'):assert evaluate(ast.parse(original['check'],mode='eval')),(i,'source fausse');checks+=1
 for j,q in enumerate(model,1):
  assert f'{j}. '+frac(q['q']) in enonce,(i,j,'énoncé modifié')
  answer=frac(q['a'])
  actual=re.search(rf'^{j}\. (.*)$',sol,re.M)
  assert actual and actual[1]==answer,(i,j,'solution numérique ou verbale différente')
  section=re.search(rf'^## Question {j} :[\s\S]*?(?=^## Question |\Z)',steps,re.M)[0]
  assert answer in section and '::: methode' in section and '::: etape' in section and '::: resultat' in section
  if q['check']:
   assert evaluate(ast.parse(q['check'],mode='eval')),(i,j,q['check'])
   checks+=1
 # Toutes les fractions simples restent dans le domaine CE2.
 for a,d in re.findall(r'\\dfrac\{(\d+)\}\{(\d+)\}',enonce+steps+sol):assert 0<=int(a)<=int(d)<=12
for name in ['cours_nouveau.txt','fiche_nouvelle.txt']:
 t=(P/name).read_text(encoding='utf-8');assert '<!-- optitab:1 -->' in t
 for a,d in re.findall(r'\\dfrac\{(\d+)\}\{(\d+)\}',t):assert 0<=int(a)<=int(d)<=12
numeric_equalities=0
corrections='\n'.join(b.split('Étapes:\n',1)[1] for b in blocks)
# Un intitulé peut citer l’égalité fausse d’un élève : ce sont les raisonnements qui sont affirmés vrais.
corrections=re.sub(r'^## Question[^\n]*','',corrections,flags=re.M)
corrections=re.sub(r'\\dfrac\{(\d+)\}\{(\d+)\}',r'\1/\2',corrections).replace('$','')
number=r'\d+(?:[ \u00a0]\d{3})*(?:/\d+)?'
expression=rf'{number}(?:[ ]*[+×÷-][ ]*{number})*'
pattern=rf'(?<![\w/,])({expression})[ ]*=[ ]*({expression})(?![\d/,])'
def value(s):return evaluate(ast.parse(s.replace(' ','').replace('\u00a0','').replace('×','*').replace('÷','/'),mode='eval'))
for m in re.finditer(pattern,corrections):
 a,c=m.groups()
 assert value(a)==value(c),(m[0],'égalité fausse dans le fichier réellement livré')
 numeric_equalities+=1
report={'math_OK':True,'exercices':9,'questions':45,'situations_recalculees':checks,'egalites_lues_et_recalculees':numeric_equalities,'fichiers_sha256':{n:hashlib.sha256((P/n).read_bytes()).hexdigest() for n in ['cours_nouveau.txt','fiche_nouvelle.txt','exercices.txt','situations_verifiees.json']}}
(P/'resultats_math.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(report,ensure_ascii=False))
