"""Contrôle indépendant : lit les textes finaux, jamais le générateur."""
from pathlib import Path
import ast,json,re
HERE=Path(__file__).resolve().parent
def calc(s):
 tree=ast.parse(s,mode='eval')
 def visit(t):
  if isinstance(t,ast.Expression):return visit(t.body)
  if isinstance(t,ast.Constant) and type(t.value)==int:return t.value
  if isinstance(t,ast.BinOp) and isinstance(t.op,(ast.Add,ast.Sub,ast.Mult,ast.FloorDiv)):
   a,b=visit(t.left),visit(t.right)
   return a+b if isinstance(t.op,ast.Add) else a-b if isinstance(t.op,ast.Sub) else a*b if isinstance(t.op,ast.Mult) else a//b
  raise ValueError(s)
 return visit(tree)
def verify():
 checked=0;answers=0
 for name in ['cours_nouveau.txt','fiche_nouvelle.txt','exercices.txt']:
  text=(HERE/name).read_text(encoding='utf-8')
  for raw in re.findall(r'\$([^$\n]+)\$',text):
   s=raw.replace(' ','')
   if '=' not in s or not re.fullmatch(r'[0-9+\-*=()/]+',s):continue
   values=[calc(x) for x in s.split('=')]
   assert len(set(values))==1,(name,raw,values)
   assert all(0<=v<=100 for v in values),(name,raw)
   checked+=1
  if name=='exercices.txt':
   blocks=re.split(r'^===[ \t]*$',text,flags=re.M)[1:]
   assert len(blocks)==9
   for b in blocks:
    en,steps,sol=b.split('Énoncé:',1)[1].split('Étapes:')[0],b.split('Étapes:')[1].split('Solution:')[0],b.split('Solution:')[1]
    assert len(re.findall(r'^\d+\. ',en,re.M))==5
    assert len(re.findall(r'^## Question ',steps,re.M))==5
    results=re.findall(r'::: resultat\n(.*?)\n:::',steps,re.S)
    for j,r in enumerate(results,1):assert f'{j}. {r}' in sol,(j,r)
    first=re.search(r'^1\. (.*)$',en,re.M)[1]
    listed=re.match(r'((?:\d+\s*;\s*)+\d+)\.',results[0])
    if listed:
     actual=[int(n) for n in re.findall(r'\d+',listed[1])]
     operations=re.findall(r'(\d+)\s*([+\-])\s*(\d+)',first)
     if operations:
      expected=[int(a)+int(c) if op=='+' else int(a)-int(c) for a,op,c in operations]
      assert actual==expected,(first,actual,expected)
     elif 'doubles de' in first:
      ns=[int(n) for n in re.findall(r'\d+',first)];assert actual==[n+n for n in ns]
     elif 'moitiés de' in first:
      ns=[int(n) for n in re.findall(r'\d+',first)];assert [n+n for n in actual]==ns
     elif 'double de …' in first and 'moitié de …' in first:
      ns=[int(n) for n in re.findall(r'\d+',first)];assert actual[0]*2==ns[0] and actual[1]==ns[1]*2
     elif 'nombres 0, 3 et 6' in first:assert actual==[10,7,4]
     elif '+ … = 10' in first:
      ns=[int(n) for n in re.findall(r'(\d+)\s*\+\s*…',first)];assert actual==[10-n for n in ns]
     checked+=len(actual)
    if 'dizaine suivante' in first:
     ns=[int(n) for n in re.findall(r'\d+',first)]
     pairs=[tuple(map(int,t)) for t in re.findall(r'(\d+) pour (\d+)',results[0])]
     assert len(ns)==len(pairs)
     for n,(gap,nextten) in zip(ns,pairs):assert n+gap==nextten and nextten%10==0 and 0<gap<10
    if 'Les deux boîtes contiennent' in results[0]:
     pairs=[tuple(map(int,t)) for t in re.findall(r'(\d+) et (\d+)',results[0])]
     assert len(pairs)==11 and pairs==[(n,10-n) for n in range(11)]
    answers+=len(results)
    # Recalcul des réponses verbales doubles et moitiés réellement publiées.
    for n,v in re.findall(r'Le double de (\d+) est (\d+)',b):assert int(n)+int(n)==int(v)
    for n,v in re.findall(r'La moitié de (\d+) est (\d+)',b):assert int(v)+int(v)==int(n)
 # Toutes les égalités numériques dans les réponses natives sont recalculées aussi.
 text='\n'.join((HERE/x).read_text(encoding='utf-8') for x in ['cours_nouveau.txt','fiche_nouvelle.txt','exercices.txt'])
 native='\n'.join(line for line in text.splitlines() if '…' not in line and r'\ldots' not in line)
 for expression in re.findall(r'(?<![\d+\-])\d+(?:\s*[+\-]\s*\d+)*\s*=\s*\d+(?:\s*[+\-]\s*\d+)*(?:\s*=\s*\d+(?:\s*[+\-]\s*\d+)*)*',native):
  values=[calc(part.strip()) for part in expression.split('=')]
  assert len(set(values))==1,(expression,values)
  checked+=1
 assert checked>=50 and answers==45,(checked,answers)
 result={'statut':'OK','math_OK':True,'egalites_recalculees':checked,'questions_verifiees':answers,'source':'cours, fiche, énoncés, étapes et solutions réellement écrits'}
 (HERE/'verification_math.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 print(json.dumps(result,ensure_ascii=False))
if __name__=='__main__':verify()
