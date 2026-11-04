"""Recalcul indépendant : données des vraies questions, résultats et égalités des textes."""
from pathlib import Path
import json,re,hashlib,runpy
D=Path(__file__).resolve().parent
small=['zéro','un','deux','trois','quatre','cinq','six','sept','huit','neuf','dix','onze','douze','treize','quatorze','quinze','seize']
def french(n):
 if n<=16:return small[n]
 if n<20:return 'dix-'+small[n-10]
 if n==100:return 'cent'
 if n>=80:
  r=n-80;return 'quatre-vingts' if r==0 else 'quatre-vingt-'+french(r)
 if n>=70:return 'soixante-et-onze' if n==71 else 'soixante-'+french(n-60)
 tens={2:'vingt',3:'trente',4:'quarante',5:'cinquante',6:'soixante'}
 t,r=divmod(n,10)
 return tens[t]+('' if r==0 else '-et-un' if r==1 else '-'+french(r))
ordinals=['premier','deuxième','troisième','quatrième','cinquième','sixième','septième','huitième','neuvième','dixième','onzième','douzième','treizième','quatorzième','quinzième','seizième','dix-septième','dix-huitième','dix-neuvième','vingtième']
data=json.loads((D/'donnees_exercices_root.json').read_text(encoding='utf-8'))
text=(D/'exercices.txt').read_text(encoding='utf-8')
checked=0
for i,item in enumerate(data,1):
 assert len(item['questions'])>=5
 for j,q in enumerate(item['questions'],1):
  c=q['controle'];op=c['operation'];a=c['entrees'];v=c['attendu'];result=q['resultat']
  if op=='identity':r=a[0]
  elif op in ('sum','shift'):r=a[0]+a[1]
  elif op=='difference':r=a[0]-a[1]
  elif op=='decompose':r=[a[0]//10,a[0]%10]
  elif op=='compare':r='<' if a[0]<a[1] else '>' if a[0]>a[1] else '='
  elif op=='sort':r=sorted(a[0],reverse=a[1])
  elif op=='max':r=max(a[0])
  elif op=='word':r=next(n for n in range(101) if french(n)==a[0])
  elif op=='name':r=french(a[0])
  elif op=='choose':r=chr(65+a[0].index(a[1]))
  elif op=='sequence':r=[a[0]+k*a[1] for k in a[2]]
  elif op=='less_owner':r='Noé' if a[0]<a[1] else 'Inès'
  elif op=='more_owner':r='Mina' if a[0]>a[1] else 'Adam'
  elif op=='rank':r=a[0][a[1]-1]
  elif op=='pattern':r=a[0][(a[1]-1)%len(a[0])]
  elif op=='ordinal':r=ordinals[a[0]-1]
  elif op=='reverse_rank':r=a[0]-a[1]+1
  elif op=='regroup':r=10*a[0]+a[1]
  elif op=='digit':r=a[1]*10 if a[0]//10==a[1] else a[1]
  elif op=='between':r=a[0]+1;assert a[0]<r<a[1]
  elif op=='bound':r=[a[0]//10*10,a[0]//10*10+10]
  else:raise AssertionError(op)
  assert r==v,(i,j,op,r,v)
  if op in ('decompose','bound','sequence','sort'):
   nums=list(map(int,re.findall(r'\d+',result)));assert all(x in nums for x in r),(i,j,result,r)
  elif isinstance(r,int):assert r in list(map(int,re.findall(r'\d+',result))),(i,j,result,r)
  else:assert str(r) in (result+' '.join(q['etapes']) if op=='compare' else result),(i,j,result,r)
  assert result in text,(i,j,'réponse absente')
  assert q['question'] in text and q['methode'] in text
  checked+=1
assert len(data)==9 and checked>=45
# Les expressions numériques sont relues depuis les trois vrais fichiers finaux.
arithmetic=0
for name in ['cours_nouveau.txt','fiche_nouvelle.txt','exercices.txt']:
 content=(D/name).read_text(encoding='utf-8')
 for match in re.finditer(r'(?<![\d+])\b(\d+(?:\s*\+\s*\d+)*)\s*=\s*(\d+(?:\s*\+\s*\d+)*)\b',content):
  if re.match(r'\s*\+\s*…',content[match.end():]):continue # égalité à compléter dans une question
  left=sum(map(int,re.findall(r'\d+',match[1])));right=sum(map(int,re.findall(r'\d+',match[2])))
  assert left==right,(name,match[0]);arithmetic+=1
 for match in re.finditer(r'\b(\d+)\s*([<>])\s*(\d+)\b',content):
  x,y=int(match[1]),int(match[3]);assert (x<y if match[2]=='<' else x>y),(name,match[0]);arithmetic+=1
 hashes={n:hashlib.sha256((D/n).read_bytes()).hexdigest() for n in ['cours_nouveau.txt','fiche_nouvelle.txt','exercices.txt','donnees_exercices_root.json']}
figs=runpy.run_path(str(D/'figures/figures.py'))['FIGURES'];code=int(D.name[:2]);fig_checked=0
dot_expected={1:{'ex1_enonce':5,'ex1_corrige':5,'ex2_enonce':1,'ex2_corrige':6,'ex5_enonce':8,'ex5_corrige':8,'ex8_enonce':4,'ex8_corrige':4,'ex9_enonce':5,'ex9_corrige':10,'lecon':4},2:{'ex1_enonce':9,'ex1_corrige':9,'ex2_enonce':0,'ex2_corrige':6,'ex8_enonce':8,'ex8_corrige':8,'ex9_enonce':0,'ex9_corrige':10,'lecon':8},3:{'ex1_enonce':12,'ex1_corrige':12,'ex5_enonce':6,'ex5_corrige':12,'ex7_enonce':12,'ex7_corrige':12,'ex9_enonce':10,'ex9_corrige':10,'lecon':10}}
if code in dot_expected:
 for key,wanted in dot_expected[code].items():
  found=len(re.findall(r'\\fill\[',figs[key]));assert found==wanted,(key,found,wanted);fig_checked+=1
base_expected={7:{'ex1_enonce':18,'ex1_corrige':18,'ex3_enonce':10,'ex3_corrige':14,'ex9_enonce':14,'ex9_corrige':14,'lecon':16},9:{'ex1_enonce':52,'ex1_corrige':52,'ex6_enonce':30,'ex6_corrige':42,'ex9_enonce':77,'ex9_corrige':77,'lecon':34},13:{'ex1_enonce':71,'ex1_corrige':71,'ex8_enonce':80,'ex8_corrige':92,'lecon':86}}
if code in base_expected:
 for key,wanted in base_expected[code].items():
  rectangles=re.findall(r'\\draw\[otNavy,fill=otSky\] \(([-\d.]+),([-\d.]+)\) rectangle \(([-\d.]+),([-\d.]+)\)',figs[key])
  found=sum(10 if abs(float(y2)-float(y1))>1 else 1 for x1,y1,x2,y2 in rectangles)
  assert found==wanted,(key,found,wanted);fig_checked+=1
if code==8:
 for key,count in [('ex8_enonce',3),('ex8_corrige',8)]:
  assert figs[key].count(r'\draw[otNavy,fill=otSky]')==count;fig_checked+=1
 for key,count in [('ex1_enonce',5),('ex1_corrige',5),('ex4_enonce',9),('ex4_corrige',9),('ex6_enonce',10),('ex6_corrige',20),('ex9_enonce',20),('ex9_corrige',20),('lecon',6)]:
  letters=re.findall(r'\\node\[text=otNavy\] at \([^)]+\) \{([A-Z?o])\}',figs[key]);assert len(letters)==count,(key,len(letters));fig_checked+=1
if code==10:
 for key,source in figs.items():
  labels=re.findall(r'\\node\[text=(?:otNavy|otGreenDark)\] at \(([-\d.]+),-0.42\) \{(\d+)\}',source)
  # Chaque nombre est exactement à 0,6 cm de son voisin numérique.
  for (x,a),(y,b) in zip(labels,labels[1:]):assert abs((float(y)-float(x))-.6*(int(b)-int(a)))<.00001,(key,a,b)
  fig_checked+=1
report={'statut':'OK','math_OK':True,'questions_recalculees':checked,'egalites_comparaisons_recalculees':arithmetic,'figures_donnees_recalculees':fig_checked,'empreintes':hashes}
(D/'verification_math.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(report,ensure_ascii=False))
