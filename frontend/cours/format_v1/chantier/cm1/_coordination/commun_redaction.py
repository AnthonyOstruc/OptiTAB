"""Rédaction et vérification indépendantes des exercices structurés CM1."""
from pathlib import Path
from fractions import Fraction as F
import json,re
ROOT=Path(__file__).resolve().parent.parent
def n(x):
 x=F(x)
 return str(x.numerator) if x.denominator==1 else str(float(x)).rstrip('0').rstrip('.').replace('.',r'{,}')
def eq(expr,value):return '$'+expr+'='+n(value)+'$'
def q(prompt,method,steps,result):return dict(question=prompt,methode=method,etapes=steps if isinstance(steps,list) else [steps],resultat=result)
def ex(title,intro,questions,checks=None,figures=None):
 assert len(questions)>=5
 return dict(titre=title,enonce=intro,questions=questions,verifications=checks or [],figures=figures or {})
def table(headers,rows):return '\n'.join(['| '+' | '.join(headers)+' |','|'+'---|'*len(headers)]+['| '+' | '.join(map(str,r))+' |' for r in rows])
def write(code,items):
 d=next(ROOT.glob(f'{code:02}_*'));assert len(items)>=15
 blocks=[]
 for i,item in enumerate(items,1):
  item['enonce']='$'.join(part.replace('{,}',',') if k%2==0 else part for k,part in enumerate(item['enonce'].split('$')))
  level='easy' if i<=5 else 'medium' if i<=10 else 'hard';kind={'easy':'Découverte','medium':'Entraînement','hard':'Problème'}[level]
  item['id']=f'nouveau-{i}';item['titre']=kind+' - '+item['titre']
  en='<!-- optitab:1 -->\n'+item['enonce']+'\n\n'+'\n'.join(f"{j}. {p['question']}" for j,p in enumerate(item['questions'],1))
  steps='<!-- optitab:1 -->\n'
  for j,p in enumerate(item['questions'],1):
   steps+=f"\n## Question {j} : {p['question']}\n\n::: methode\n{p['methode']}\n:::\n"
   for k,text in enumerate(p['etapes'],1):steps+=f'\n::: etape '+('Raisonner' if k==1 else 'Vérifier')+f'\n{text}\n:::\n'
   steps+=f"\n::: resultat\n{p['resultat']}\n:::\n"
  sol='<!-- optitab:1 -->\n'+'\n'.join(f"{j}. {p['resultat']}" for j,p in enumerate(item['questions'],1))
  blocks.append(f"===\n{item['titre']}\nId: {item['id']}\nDifficulté: {level}\n\nÉnoncé:\n{en}\n\nÉtapes:\n{steps}\nSolution:\n{sol}\n")
 (d/'exercices.txt').write_text('\n'.join(blocks),encoding='utf-8')
 (d/'donnees_exercices_root.json').write_text(json.dumps(items,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 print(code,len(items),'exercices',sum(len(x['questions']) for x in items),'questions')
