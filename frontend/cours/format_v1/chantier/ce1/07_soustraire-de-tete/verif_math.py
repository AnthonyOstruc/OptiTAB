"""Vérification autonome : relit et recalcule les égalités des vrais fichiers finaux."""
from pathlib import Path
import ast,json,re
P=Path(__file__).resolve().parent
def compute(s):
 tree=ast.parse(s,mode='eval')
 def rec(n):
  if isinstance(n,ast.Expression):return rec(n.body)
  if isinstance(n,ast.Constant) and isinstance(n.value,int):return n.value
  if isinstance(n,ast.BinOp) and isinstance(n.op,(ast.Add,ast.Sub,ast.Mult)):
   a,b=rec(n.left),rec(n.right)
   return a+b if isinstance(n.op,ast.Add) else a-b if isinstance(n.op,ast.Sub) else a*b
  raise ValueError(s)
 return rec(tree)
total=0
for name in ('cours_nouveau.txt','fiche_nouvelle.txt','exercices.txt'):
 text=(P/name).read_text(encoding='utf-8');assert '\x0c' not in text and '\x08' not in text
 for m in re.finditer(r'\${1,2}([^$]+)\${1,2}',text):
  formula=m[1].strip().replace('\\times','*').replace(' ','')
  if '=' not in formula or '\\' in formula:continue
  parts=formula.split('=')
  if all(re.fullmatch(r'[0-9+*()\-]+',p) for p in parts):
   values=[compute(p) for p in parts];assert len(set(values))==1,(name,m[1],values);total+=1
  assert not any(int(v)>1000 for v in re.findall(r'\d+',formula)),(name,formula)
 # Les phrases de partage et de parité sont vérifiées dans les textes produits.
 for a,b in re.findall(r'[Ll]a moitié de (\d+) est (\d+)',text):assert int(a)==2*int(b),(name,a,b)
 for a,b in re.findall(r'[Ll]e double de (\d+) est (\d+)',text):assert 2*int(a)==int(b),(name,a,b)
text=(P/'exercices.txt').read_text(encoding='utf-8')
blocks=re.split(r'^===\n',text,flags=re.M)[1:];assert len(blocks)==9,len(blocks)
for i,block in enumerate(blocks,1):
 assert f'Id: nouveau-{i}\n' in block
 en,rest=block.split('Énoncé:\n',1)[1].split('Étapes:\n',1);steps,sol=rest.split('Solution:\n',1)
 qs=re.findall(r'^\d+\. ',en,re.M);assert len(qs)>=5,(i,len(qs))
 assert len(re.findall(r'^## Question \d+ :',steps,re.M))==len(qs)
 assert steps.count('::: methode\n')==steps.count('::: resultat\n')==len(qs)
 results=re.findall(r'::: resultat\n(.*?)\n:::',steps,re.S)
 answers=re.findall(r'^\d+\. (.*)$',sol,re.M)
 assert results==answers,(i,'Résultats et solutions différents')
 for p in re.findall(r'## Question .*?(?=\n## Question |\Z)',steps,re.S):
  assert len(re.search(r'::: etape .*?\n(.*?)\n:::',p,re.S)[1])>=40
  # Résoudre à nouveau les calculs à trou à partir des vraies questions finales.
  prompt=p.split('\n',1)[0]
  hole=re.search(r'\$([^$]*\\ldots[^$]*)\$',prompt)
  if hole:
   formula=hole[1].replace('\\times','*').replace('\\ldots','X').replace(' ','')
   left,right=formula.split('=')
   difference=lambda x:compute(left.replace('X',str(x)))-compute(right.replace('X',str(x)))
   intercept=difference(0);slope=difference(1)-intercept
   assert slope and difference(2)==intercept+2*slope,(i,prompt,'Relation non affine')
   candidates=[-intercept//slope] if (-intercept)%slope==0 and 0<=-intercept//slope<=1000 else []
   assert len(candidates)==1,(i,prompt,candidates)
   result=re.search(r'::: resultat\n(.*?)\n:::',p,re.S)[1]
   assert re.findall(r'\d+',result)==[str(candidates[0])],(i,prompt,result)
 # Les calculs numériques des neuf compétences sources doivent être présents
 # dans le raisonnement final et y avoir leur bonne valeur.
 source=json.loads((P/'sources_locales/chapitre.json').read_text(encoding='utf-8'))['exercices'][i-1]
 first=re.search(r'## Question 1 :.*?(?=\n## Question 2 :)',steps,re.S)[0]
 final_formulas=[s.replace('\\times','*').replace(' ','') for s in re.findall(r'\$([^$]+)\$',first)]
 for condition in source.get('check','').split(' and '):
  expr=condition.split('==')[0]
  if re.fullmatch(r'\d+(?:[+*\-]\d+)+',expr):
   expected=compute(expr)
   assert any(t==expr+'='+str(expected) for t in final_formulas),(i,expr,expected,'Calcul source absent')
 if P.name.startswith('09_') and i==4:
  result=re.search(r'::: resultat\n(.*?)\n:::',first,re.S)[1]
  even,odd=result.split('Impairs :')
  assert all(int(x)%2==0 for x in re.findall(r'\d+',even))
  assert all(int(x)%2==1 for x in re.findall(r'\d+',odd))
 if P.name.startswith('09_') and i==5:
  result=re.search(r'::: resultat\n(.*?)\n:::',first,re.S)[1]
  bounds=list(map(int,re.findall(r'\d+',source['consigne'])))
  assert list(map(int,re.findall(r'\d+',result)))==list(range(bounds[0],bounds[1]+1,2))
mapping=json.loads((P/'figures/correspondance.json').read_text(encoding='utf-8'))
assert 'nouveau' in mapping['cours'] and 'nouvelle' in mapping['fiches']
assert len(re.findall(r'^\| \d+ \|', (P/'COUVERTURE.md').read_text(encoding='utf-8'),re.M))==9
ns={};exec((P/'figures/figures.py').read_text(encoding='utf-8'),ns)
for section in mapping.values():
 for places in section.values():
  for pic in places.values():assert Path(pic['fichier']).stem in ns['FIGURES']
assert 'multiplication posée' not in (P/'cours_nouveau.txt').read_text(encoding='utf-8').lower()
print(P.name,': 9 exercices,',sum(len(re.findall(r'^## Question ',b,re.M)) for b in blocks),'questions ;',total,'égalités recalculées ; solutions identiques ; correspondances TikZ valides.')
