"""Relecture indépendante : arithmétique exacte, structure et réponses du lot 6e.

Ne lance pas le générateur. Lit les fichiers réellement livrés et compare
les calculs à SymPy/Fraction ; contrôle aussi les cas textuels par scénario.
"""
from pathlib import Path
from fractions import Fraction as F
from decimal import Decimal,ROUND_HALF_UP
import json,re,sys
import sympy as s
sys.stdout.reconfigure(encoding='utf-8')
D=Path(sys.argv[1]).resolve() if len(sys.argv)>1 else Path(__file__).resolve().parent
CODE=int(D.name.split('_')[0]);count=0
def num(x):
 x=x.replace('{,}','.').replace(r'\,','').replace(r'\left','').replace(r'\right','').replace(r'\dfrac',r'\frac').replace(r'\times','*').replace(r'\div','/').replace('^','**')
 for _ in range(20):
  old=x
  for pat in (r'\\frac\{([^{}]*)\}\{([^{}]*)\}',r'\\frac(\d)\{([^{}]*)\}',r'\\frac\{([^{}]*)\}(\d)',r'\\frac(\d)(\d)'):
   x=re.sub(pat,lambda m:'(('+m[1]+')/('+m[2]+'))',x)
  if x==old:break
 x=x.replace('{','(').replace('}',')')
 if not re.fullmatch(r'[\d.\s+*/()\-]+',x) or not re.search(r'\d',x):return None
 return s.sympify(x,rational=True)
def check_equalities(text):
 global count
 displays=re.findall(r'\$\$(.*?)\$\$',text,re.S)
 inline=re.sub(r'\$\$.*?\$\$','',text,flags=re.S)
 for block in displays+re.findall(r'(?<!\$)\$([^$\n]+)\$(?!\$)',inline):
  block=block.replace(r'\begin{aligned}','').replace(r'\end{aligned}','').replace('\\\\','').replace('&','').replace(r'\quad','')
  block=re.sub(r'^[AB]:','',block.strip())
  if '=' not in block:continue
  # Un signe de comparaison, une proposition à réfuter ou une formule littérale n'est pas une chaîne d'égalités.
  if any(z in block for z in (r'\ne',r'\le',r'\ge',r'\lt',r'\gt',r'\approx')):continue
  parts=[num(x) for x in block.split('=')]
  if len(parts)>1 and all(x is not None for x in parts):
   assert all(x==parts[0] for x in parts),(CODE,'egalite fausse',block,parts)
   count+=1

meta=json.loads((D/'source_en_ligne/meta.json').read_text(encoding='utf-8'))
raw=(D/'exercices.txt').read_text(encoding='utf-8')
bs=[b for b in re.split(r'^===[ \t]*$',raw,flags=re.M) if b.strip()]
assert len(bs)==21
ids=[];titles=[];enonces=[];questions=0
data=json.loads((D/'revision_pedagogique_6e.json').read_text(encoding='utf-8'))['exercices']
for idx,b in enumerate(bs):
 eid=re.search(r'^Id: (.+)',b,re.M)[1];ids.append(eid)
 title=b.strip().splitlines()[0];titles.append(title)
 en=b.split('Énoncé:\n')[1].split('Étapes:\n')[0].strip()
 et=b.split('Étapes:\n')[1].split('Solution:\n')[0].strip();so=b.split('Solution:\n')[1].strip()
 assert en.startswith('<!-- optitab:1 -->') and et.startswith('<!-- optitab:1 -->') and so.startswith('<!-- optitab:1 -->')
 qs=re.findall(r'^\d+\. (.+)',en,re.M);answers=re.findall(r'^\d+\. (.+)',so,re.M)
 results=re.findall(r'^::: resultat\n(.*?)\n:::',et,re.S|re.M)
 assert len(qs)==len(answers)==len(results)==et.count('## Question ')==et.count('::: methode')==et.count('::: etape')
 assert results==answers,(CODE,eid,'resultat/solution')
 assert len(qs)>=4
 questions+=len(qs);enonces.append(re.sub(r'\s+',' ',en))
 # Les données de rédaction doivent être celles du fichier livré, et non d'une ancienne génération.
 spec=data[idx];assert str(spec['id'])==eid
 assert [x['question'] for x in spec['questions']]==qs
 assert [x['resultat'] for x in spec['questions']]==answers
 check_equalities(re.sub(r'^## Question.*$', '',et,flags=re.M))
 l,j=divmod(idx,7)
 def has(i,value):assert str(value) in answers[i],(CODE,eid,i,value,answers[i])
 if CODE==129:
  if j==0:
   n=int(re.search(r'indique ([\d ]+) consultations',en)[1].replace(' ',''));a=int(re.search(r'augmente de ([\d ]+) consultations',en)[1].replace(' ',''))
   for v in (n//10**9,n//10**6%1000,n//1000%1000,n%1000):has(0,v)
   has(1,n//10**6);assert str(n+a) in answers[3].replace(' ','')
  elif j==1:
   x=F(re.search(r'affiche \$([^$]+)',en)[1].replace('{,}','.'));has(2,int(x*1000))
  elif j==3:
   a,b,den=map(int,re.search(r'\$(\d+)\+\\frac\{(\d+)\}\{(\d+)\}',en).groups());x=F(a)+F(b,den)
   has(1,a*den+b);has(2,int(x*10))
  elif j==4:
   x=F(re.search(r'nombre \$([^$]+)',en)[1].replace('{,}','.'));has(1,int(x*100));has(0,int(x*100)%10)
  elif j==5:
   assert r'\approx' in answers[3] and 'indéfiniment' not in answers[1]
 elif CODE==130:
  if j==0:
   vals=[F(x.replace('{,}','.')) for x in re.findall(r'\$([\d{},]+)\$',en.split('1.')[0])]
   pas=(vals[1]-vals[0])/10;assert pas==F(1,10**(l+1))
  elif j==2:
   x=Decimal(re.search(r'étudie \$([^$]+)',en)[1].replace('{,}','.'));rd=x.quantize(Decimal('.01'),rounding=ROUND_HALF_UP)
   assert str(rd).replace('.','{,}') in answers[3]
  elif j==4:
   x=Decimal(re.search(r'vaut \$([^$]+)',en)[1].replace('{,}','.'))
   for i,unit in enumerate(('1','.1','.01')):assert str(x.quantize(Decimal(unit),rounding=ROUND_HALF_UP)).replace('.','{,}') in answers[i]
 elif CODE==133:
  if j in (0,2):
   vals=list(map(int,re.findall(r'\d+',en.split('1.')[0].replace('<!-- optitab:1 -->',''))));n,b=vals[:2];qq,rr=divmod(n,b)
   if j==0:has(1,qq);has(1,rr);has(3,b-rr)
   else:has(0,qq);has(0,rr);has(1,qq+bool(rr));has(2,(-n)%b)
  elif j==4:
   n=int(re.search(r'de (\d+) cartes',en)[1])
   for i,div in enumerate((2,3,5)):assert answers[i].startswith('Oui' if n%div==0 else 'Non')
 elif CODE==151:
  if j==1:
   k=int(re.search(r'possède (\d+) fois',en)[1]);total=int(re.search(r'ont (\d+)',en)[1]);assert total%(k+1)==0
   has(0,k+1);has(1,total//(k+1));has(2,k*total//(k+1))
  if j==2:
   total=int(re.search(r'ensemble (\d+)',en)[1]);gap=int(re.search(r'contient (\d+) billes',en)[1]);assert (total-gap)%2==0
   has(1,(total-gap)//2);has(2,(total+gap)//2)
assert len(set(ids))==len(ids) and len(set(titles))==len(titles) and len(set(enonces))==len(enonces)
assert {str(e['id']) for e in meta['exercices']}<={x for x in ids if x.isdigit()}
assert all(x.isdigit() or re.fullmatch(r'nouveau-\d+',x) for x in ids)
# Cours : égalités exactes hors des encadrés annonçant une erreur à réfuter.
for p in list(D.glob('cours_*.txt'))+list(D.glob('fiche_*.txt')):
 text=p.read_text(encoding='utf-8');assert text.count('<!-- optitab:1 -->')==1
 assert not re.search(r'(?i)TODO|FIXME|à compléter|\\displaystyle',text)
 cleaned=re.sub(r'::: attention.*?\n:::', '',text,flags=re.S)
 # L'exemple de notation 5=8=16=12 est explicitement annoncé comme faux.
 cleaned=cleaned.replace('$5=8=16=12$','')
 check_equalities(cleaned)
report={'notion':CODE,'statut':'OK','exercices':len(bs),'questions_corrigees':questions,'egalites_numeriques_exactes':count,'identifiants_conserves':len(meta['exercices']),'nouveaux_exercices':sum(not x.isdigit() for x in ids),'familles':7}
(D/'verification_math_6e.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(report,ensure_ascii=False))
