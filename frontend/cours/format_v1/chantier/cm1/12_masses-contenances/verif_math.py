"""Contrôles exacts des livrables CM1 et recomposition indépendante des situations."""
from pathlib import Path
from fractions import Fraction as F
import json,re,sys
import sympy as sp
D=Path(sys.argv[1]).resolve() if len(sys.argv)>1 else Path(__file__).resolve().parent
code=int(D.name.split('_')[0]);checks=0
def numeric(s):
 s=s.replace('{,}','.').replace(r'\,','').replace(r'\times','*').replace(r'\div','/')
 if not re.fullmatch(r'[\d.\s+*/()\-]+',s) or not re.search(r'\d',s):return None
 return sp.sympify(' '.join(s.split()),rational=True)
def equalities(s):
 global checks
 for text in re.findall(r'(?<!\$)\$([^$]+)\$(?!\$)',s):
  if '=' not in text:continue
  vals=[numeric(x) for x in text.split('=')]
  if all(v is not None for v in vals):assert len(set(vals))==1,(code,text);checks+=1
def has(ans,i,value):
 global checks
 val=F(value);expected=str(val.numerator) if val.denominator==1 else str(float(val)).rstrip('0').rstrip('.').replace('.',',')
 assert re.search(r'(?<![\d,])'+re.escape(expected)+r'(?!\d|,\d)',ans[i].replace('{,}',',')),(code,i,expected,ans[i]);checks+=1
def at(ans,i,minutes):
 global checks
 match=re.search(r'(\d+) h (\d+) min',ans[i]);assert match,(ans[i],minutes)
 assert tuple(map(int,match.groups()))==divmod(minutes,60),(ans[i],minutes);checks+=1
raw=(D/'exercices.txt').read_text(encoding='utf-8');blocks=[x for x in re.split(r'^===[ \t]*$',raw,flags=re.M) if x.strip()]
data=json.loads((D/'donnees_exercices_root.json').read_text(encoding='utf-8'));assert len(data)==len(blocks)==15
for i,(b,spec) in enumerate(zip(blocks,data)):
 t,k=divmod(i,5);en=b.split('Énoncé:')[1].split('Étapes:')[0].strip();steps=b.split('Étapes:')[1].split('Solution:')[0].strip();sol=b.split('Solution:')[1].strip()
 assert en.split('1. ')[0].replace('<!-- optitab:1 -->','').strip()==spec['enonce'].strip()
 qs=re.findall(r'^\d+\. (.+)',en,re.M);ans=re.findall(r'^\d+\. (.+)',sol,re.M);res=[x.strip() for x in re.findall(r'^::: resultat\n(.*?)\n:::',steps,re.M|re.S)]
 assert len(qs)==len(ans)==len(res)==5 and qs==[q['question'] for q in spec['questions']]
 assert ans==res==[q['resultat'] for q in spec['questions']]
 assert steps.count('::: methode')==steps.count('## Question ')==5
 assert re.search(r'^Id: (.+)',b,re.M)[1]==f'nouveau-{i+1}'
 equalities(steps)
 if code==11:
  if k==0:has(ans,1,(18+2*t)*10);has(ans,2,(2+t)*100);has(ans,3,F(45+5*t,10))
  elif k==1:has(ans,1,55+5*t);has(ans,2,F(55+5*t,10));has(ans,3,85+10*t);has(ans,4,5)
  elif k==2:
   total=(2+t)*100;cut=50+25*t;has(ans,1,total);has(ans,2,total-cut);has(ans,3,F(total-cut,5));has(ans,4,total)
  elif k==3:has(ans,1,2*(11+3*t));has(ans,2,4*(5+t));has(ans,3,4*(5+t));assert ans[4].startswith('Non')
  else:
   perimeter=2*(20+3*t);fence=perimeter-2;rolls=(fence+9)//10
   has(ans,0,perimeter);has(ans,1,fence);has(ans,2,rolls);has(ans,3,rolls*10-fence);has(ans,4,2*fence)
 elif code==12:
  if k==0:
   total=(2+t)*1000+250+50*t;has(ans,1,(2+t)*1000);has(ans,2,total);has(ans,3,F(total,1000));assert 'égales' in ans[4]
  elif k==1:
   rest=100*(3+t)-120-30*t;has(ans,1,100*(3+t));has(ans,2,rest);has(ans,3,100*rest)
  elif k==2:has(ans,0,750+100*t);has(ans,1,250-100*t);has(ans,2,500);has(ans,3,500)
  elif k==3:has(ans,0,(6+2*t)*25);has(ans,1,6+2*t);has(ans,2,(4+2*t)*25);has(ans,3,F(1,2));has(ans,4,3)
  else:
   weight=4*(72+5*t)+15;limit=300+50*t
   has(ans,0,4*(72+5*t));has(ans,1,weight);assert ans[2].startswith('Non' if weight>limit else 'Oui');has(ans,3,2400+300*t);has(ans,4,8+t)
 elif code==13:
  if k==0:has(ans,0,2+t);has(ans,1,8+3*t);has(ans,3,1);has(ans,4,8+3*t)
  elif k==1:has(ans,0,4+t);has(ans,1,3*(4+t));has(ans,2,3*(4+t)-2);has(ans,3,3*(4+t));assert ans[4].startswith('Oui')
  elif k==2:has(ans,0,2*(2+t));has(ans,1,(2+t)**2);has(ans,2,4*(2+t)**2);has(ans,3,4);has(ans,4,(2+t)**2)
  elif k==3:assert ans[0]==f'Le sommet est {"BN S".replace(" ","")[t]}.';assert ans[1]=='A, puis B, puis C.' and ans[3].startswith('Non')
  else:has(ans,0,2*(9+2*t));has(ans,1,4*(3+t));has(ans,2,8+2*t);has(ans,2,(3+t)**2);assert ans[3].startswith('Non')
 elif code==14:
  if k==0:
   instant=60*(8+t)+20+10*t;at(ans,1,instant);at(ans,2,instant+720);has(ans,3,40-10*t);at(ans,4,instant+15)
  elif k==1:
   a=95+25*t;b=120+5*t;at(ans,1,a);has(ans,2,b);has(ans,3,abs(a-b))
  elif k==2:
   start=9*60+40+5*t;end=11*60+15+10*t;dur=end-start
   has(ans,0,60-start%60);has(ans,1,60+end%60);at(ans,2,dur);at(ans,3,840+dur);at(ans,4,1080-dur)
  elif k==3:
   start=14*60+50+5*t;dur=105+10*t
   at(ans,0,dur);at(ans,1,start+dur);at(ans,2,start-15);at(ans,3,start-45)
  else:
   alltimes=re.findall(r'(\d+) h (\d+) min',ans[0]);assert [60*int(h)+int(m) for h,m in alltimes]==[420+j*(20+5*t) for j in range(4)]
   has(ans,1,3);has(ans,2,3*(20+5*t));has(ans,3,50+5*t);has(ans,4,5)
 elif code==20:
  if k==0:
   values=[7+2*t,9+2*t,5+2*t,4+2*t];has(ans,0,values[1]);has(ans,1,sum(values));has(ans,3,2);assert ans[4].startswith('Non') and 2*values[1]<sum(values)
  elif k==1:has(ans,0,14+t);has(ans,1,20+2*t);has(ans,2,25+2*t);has(ans,3,51+4*t);assert ans[4].startswith('Oui')
  elif k==2:has(ans,1,8+2*t);has(ans,2,18+6*t);has(ans,3,4);has(ans,4,8+2*t)
  elif k==3:has(ans,1,12+2*t);has(ans,2,12);has(ans,3,6);assert ans[4].startswith('Non')
  else:has(ans,0,5);has(ans,0,3);has(ans,0,2+t);has(ans,1,10+t);has(ans,3,279+20*t);assert ans[4].startswith('Non')
 elif code==21:
  if k==0:assert ans[1]=='1, 2, 3, 4, 5 et 6.' and ans[2]=='C’est impossible.' and ans[3].startswith('Oui') and ans[4].startswith('Obtenir un nombre pair')
  elif k==1:has(ans,1,4+2*t);assert ans[2].startswith('Non') and ans[3].endswith('peu probable.');has(ans,4,2)
  elif k==2:has(ans,2,16);assert ans[3].startswith('Oui') and ans[4].startswith('Tirer une carte rouge')
  elif k==3:has(ans,2,4+t);assert ans[3].startswith('Autant' if t==0 else 'Plus') and ans[4].startswith('Non')
  else:has(ans,1,490-5*t);assert ans[2].startswith('Non') and 'peu probable' in ans[3] and ans[4].startswith('Non')
 checks+=1
for file in ('cours_nouveau.txt','fiche_nouvelle.txt'):equalities((D/file).read_text(encoding='utf-8'))
report={'statut':'OK','exercices':15,'questions':75,'verifications_exactes':checks,'fichiers_finaux_relus':True}
(D/'verification_math.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(report,ensure_ascii=False))
