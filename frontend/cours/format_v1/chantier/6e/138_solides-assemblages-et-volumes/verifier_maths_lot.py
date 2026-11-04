# -*- coding: utf-8 -*-
"""Recalcule chaque résultat déclaré ; contrôle les données et la structure finale."""
from pathlib import Path
from fractions import Fraction
import ast,json,re
R=Path(__file__).resolve().parent.parent
def exact(node):
 if isinstance(node,ast.Expression):return exact(node.body)
 if isinstance(node,ast.Constant):return Fraction(str(node.value))
 if isinstance(node,ast.UnaryOp) and isinstance(node.op,ast.USub):return -exact(node.operand)
 if isinstance(node,ast.BinOp):
  a,b=exact(node.left),exact(node.right)
  if isinstance(node.op,ast.Add):return a+b
  if isinstance(node.op,ast.Sub):return a-b
  if isinstance(node.op,ast.Mult):return a*b
  if isinstance(node.op,ast.Div):return a/b
 if isinstance(node,ast.Call) and isinstance(node.func,ast.Name) and node.func.id=='max':return max(exact(x) for x in node.args)
 raise ValueError(ast.dump(node))
grand=0
for n in (138,139,146,147,148,149,152):
 d=next(R.glob(f'{n}_*'));data=json.loads((d/'manifest_pedagogique.json').read_text(encoding='utf8'));t=(d/'exercices.txt').read_text(encoding='utf8')
 source=json.loads((d/'source_en_ligne/meta.json').read_text(encoding='utf8'));ids=re.findall(r'^Id: (\S+)',t,re.M);old=[str(e['id']) for e in source['exercices']]
 assert ids==(old or [f'nouveau-{i}' for i in range(1,22)]),(n,ids)
 assert len(ids)==len(set(ids))==21
 titles=re.findall(r'^=== (.+)',t,re.M);assert len(titles)==len(set(titles))==21
 enonces=[];count=0
 for block,item in zip(re.split(r'^===\s*$',t,flags=re.M),data):
  assert all(x in block for x in ('Énoncé:','Étapes:','Solution:'))
  en=block.split('Énoncé:',1)[1].split('Étapes:',1)[0];enonces.append(re.sub(r'\s+','',en))
  for k,q in enumerate(item['questions'],1):
   assert f'{k}. '+q['question'] in en
   assert f'## Question {k} : ' in block
   for value in (q['methode'],q['raisonnement'],q['resultat']):assert value in block
  assert block.count('::: methode')==len(item['questions'])
  assert block.count('::: etape')==len(item['questions'])
  assert block.count('::: resultat')==len(item['questions'])
  assert '::: retenir' in block
  for expr,expected in item['calculs']:
   result=exact(ast.parse(expr,mode='eval'));assert result==Fraction(str(expected)),(n,item['titre'],expr,result,expected)
   count+=1
 assert len(enonces)==len(set(enonces)),('Énoncés en doublon',n)
 for p in d.glob('*.txt'):
  txt=p.read_text(encoding='utf8');assert not re.search(r'[\x00-\x08\x0b\x0c\x0e-\x1f]',txt),p
  assert '<!-- optitab:1 -->' in txt,p
 # Exemples numériques des cours et fiches, recalculés en fractions exactes.
 cours_calculs={138:[('4*3',12),('2*12',24),('1+2+3+1',7),('24-3',21),('2*2*2',8)],139:[('60*60',3600),('60-15+5',50),('35-15',20),('25+20',45),('60+30',90),('90/60',1.5),('0.75*60',45),('0.30*60',18)],146:[('2+3',5),('1+4',5),('4*2',8),('3*2',6)],147:[('12+9',21),('8+12',20),('30-28',2),('250-240',10)],148:[('3+7+5',15),('3*0+7*1+5*2',17),('4+6+3',13),('40-16-11',13),('6/24',0.25),('10/20',0.5),('12/30',0.4)],149:[('3/6',0.5),('2/4',0.5),('12/20',0.6)],152:[('5+3',8),('8*2',16),('5*2',10),('10+3',13),('6+2',8),('8*2',16),('2+3*4',14),('3+2',5),('4*3',12)]}
 for expr,expected in cours_calculs[n]:
  assert exact(ast.parse(expr,mode='eval'))==Fraction(str(expected));count+=1
 # Contrôle indépendant des expériences classiques et déplacements.
 if n==138:
  assert sum([1,2,3,1])==7 and [max(1,3),max(2,1)]==[3,2];count+=2
 if n==139:
  assert (17*60+10)-(60+45)==15*60+25;assert (24*60-(23*60+35))+20==45;count+=2
 if n==146:
  # Pliage exact : transport des vecteurs normaux selon les arêtes du patron.
  def fold(cells):
   cells=set(cells);seen={next(iter(cells)):((1,0,0),(0,1,0),(0,0,1))};pending=list(seen)
   neg=lambda v:tuple(-a for a in v)
   while pending:
    x,y=pending.pop();u,v,w=seen[(x,y)]
    for target,frame in [((x+1,y),(neg(w),v,u)),((x-1,y),(w,v,neg(u))),((x,y+1),(u,neg(w),v)),((x,y-1),(u,w,neg(v)))]:
     if target in cells:
      if target in seen and seen[target]!=frame:return False
      if target not in seen:seen[target]=frame;pending.append(target)
   return len(seen)==6 and len({f[2] for f in seen.values()})==6
  assert fold([(0,0),(1,0),(2,0),(3,0),(1,1),(1,-1)])
  assert not fold([(x,y) for x in range(3) for y in range(2)]);count+=2
 if n==147:
  assert [v[0] for v in [('Musée',30,240),('Ferme',25,200),('Parc',32,270)] if v[1]>=28 and v[2]<=250]==['Musée'];count+=1
 if n==148:
  assert sum([3,7,5])==15 and sum(v*f for v,f in zip([0,1,2],[3,7,5]))==17;count+=1
 if n==149:
  couples=[a+b for a in 'PF' for b in 'PF'];assert sum(s.count('P')==1 for s in couples)==2;assert sum('P' in s for s in couples)==3;count+=2
 if n==152:
  def turtle(reps,a,b=None):
   x=y=0;direction=0;vectors=[(1,0),(0,1),(-1,0),(0,-1)];distance=0
   for _ in range(reps):
    for step in ([a] if b is None else [a,b]):
     u,v=vectors[direction];x+=u*step;y+=v*step;distance+=step;direction=(direction+1)%4
   return x,y,direction,distance
  assert turtle(4,3)==(0,0,0,12);assert turtle(2,4,2)==(0,0,0,12)
  assert turtle(3,3)==(0,3,3,9);count+=3
 result={'statut':'OK','exercices':21,'questions':sum(len(e['questions']) for e in data),'calculs_et_modeles_verifies':count,'ids_conserves':bool(old),'nouveaux':0 if old else 21,'controles':['fractions exactes','identifiants','énoncés uniques','questions/méthode/étapes/résultat','contrôles C0','modèle indépendant du domaine']}
 (d/'verification_maths.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf8');grand+=count
 print(n,result,flush=True)
print('TOTAL',grand)
