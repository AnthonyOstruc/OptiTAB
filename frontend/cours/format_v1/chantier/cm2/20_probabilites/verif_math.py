"""Relecture des fichiers livrés, sans exécuter leurs générateurs."""
from pathlib import Path
from fractions import Fraction as F
import re,json,sys,math,runpy
import sympy as s
sys.stdout.reconfigure(encoding='utf-8')
D=Path(sys.argv[1]).resolve() if len(sys.argv)>1 else Path(__file__).resolve().parent
CODE=int(D.name.split('_')[0]);checks=0
def number(raw):
 raw=raw.replace('{,}','.').replace(r'\,','').replace(r'\times','*').replace(r'\div','/').replace(r'\left','').replace(r'\right','').replace('^','**')
 if not re.fullmatch(r'[\d.\s+*/()\-]+',raw) or not re.search(r'\d',raw):return None
 return s.sympify(raw,rational=True)
def equalities(text):
 global checks
 blocks=re.findall(r'\$\$(.*?)\$\$',text,re.S)
 inline=re.sub(r'\$\$.*?\$\$','',text,flags=re.S)
 blocks+=re.findall(r'(?<!\$)\$([^$\n]+)\$(?!\$)',inline)
 for block in blocks:
  block=block.replace(r'\begin{aligned}','').replace(r'\end{aligned}','').replace('&','')
  last=None
  for row in block.split(r'\\'):
   if '=' not in row:continue
   parts=row.strip().split('=');values=[number(p) for p in parts]
   if not parts[0].strip() and last is not None:values[0]=last
   if all(v is not None for v in values):
    assert all(v==values[0] for v in values),(CODE,'egalite fausse',row,values)
    checks+=1;last=values[-1]
def norm(value):
 value=F(value)
 if value.denominator==1:return str(value.numerator)
 return str(float(value)).rstrip('0').rstrip('.').replace('.',',')
def has(answers,index,value):
 global checks
 text=answers[index].replace('{,}',',').replace(r'\,','')
 assert re.search(r'(?<![\d,])'+re.escape(norm(value))+r'(?!\d|,\d)',text),(CODE,index,value,text)
 checks+=1
raw=(D/'exercices.txt').read_text(encoding='utf-8')
blocks=[b for b in re.split(r'^===[ \t]*$',raw,flags=re.M) if b.strip()]
specs=json.loads((D/'donnees_exercices_root.json').read_text(encoding='utf-8'))
assert len(blocks)==len(specs)==21
ids=[];titles=[];statements=[];questions=0
for block,spec in zip(blocks,specs):
 eid=re.search(r'^Id: (.+)',block,re.M)[1];assert eid==spec['id'];ids.append(eid)
 titles.append(block.strip().splitlines()[0]);en=block.split('Énoncé:')[1].split('Étapes:')[0].strip();et=block.split('Étapes:')[1].split('Solution:')[0].strip();so=block.split('Solution:')[1].strip()
 assert all(t.startswith('<!-- optitab:1 -->') for t in (en,et,so))
 assert en.split('1. ')[0].replace('<!-- optitab:1 -->','').strip()==spec['enonce'].strip()
 qs=re.findall(r'^\d+\. (.+)',en,re.M);answers=re.findall(r'^\d+\. (.+)',so,re.M);results=re.findall(r'^::: resultat\n(.*?)\n:::',et,re.M|re.S)
 assert qs==[q['question'] for q in spec['questions']]
 assert answers==results==[q['resultat'] for q in spec['questions']]
 assert len(qs)==len(answers)==et.count('## Question ')==et.count('::: methode')==3
 questions+=len(qs);statements.append(re.sub(r'\s+',' ',en));equalities(re.sub(r'^## Question.*$','',et,flags=re.M))
 p=spec['parametres'];family=p['famille']
 if CODE==11:
  if family=='unites':has(answers,1,p['cm']*10);has(answers,2,p['cl']*10)
  elif family=='regle':has(answers,0,p['fin']-p['debut']);has(answers,1,F(p['fin']-p['debut'],10))
  elif family=='ruban':
   total=100*p['m'];has(answers,0,total);has(answers,1,total-p['coupe_cm']);has(answers,2,F(total-p['coupe_cm'],5))
  elif family=='masse':
   net=p['total_g']-p['tare_g'];has(answers,0,p['total_g']);has(answers,1,net);has(answers,2,F(net,p['sachets']))
  elif family=='contenance':has(answers,0,p['litres']*1000);has(answers,1,p['verre_cl']*10);has(answers,2,F(p['litres']*100,p['verre_cl']))
  elif family=='contour':has(answers,0,sum(p['cotes']));has(answers,1,3*sum(p['cotes']));assert max(p['cotes'])*2<sum(p['cotes'])
  elif family=='cloture':
   perimeter=2*(p['longueur']+p['largeur']);has(answers,0,perimeter);has(answers,1,perimeter-p['portail']);has(answers,2,math.ceil((perimeter-p['portail'])/10))
 elif CODE==12:
  if family=='carreaux':has(answers,0,F(p['demis'],2));has(answers,1,p['entiers']+F(p['demis'],2));assert answers[2].startswith('Non')
  elif family=='rectangle':
   length=100*p['longueur_m'];area=length*p['largeur_cm'];has(answers,0,length);has(answers,1,area);has(answers,2,F(area,10000))
  elif family=='conversions':has(answers,0,F(p['dm2'])*100);has(answers,1,F(p['cm2'],100));has(answers,2,p['m2']*10000)
  elif family=='decomposition':
   outer=p['L']*p['l'];cut=p['coinL']*p['coinl'];has(answers,0,outer);has(answers,1,cut);has(answers,2,outer-cut);assert 0<p['coinL']<p['L'] and 0<p['coinl']<p['l']
  elif family=='aire_perimetre':
   assert math.prod(p['A'])==math.prod(p['B']);has(answers,0,math.prod(p['A']));has(answers,1,2*sum(p['A']));has(answers,1,2*sum(p['B']));assert answers[2].startswith('Non')
  elif family=='pavage':
   area=p['longueur']*p['largeur'];tiles=area*p['dalles_m2'];has(answers,0,area);has(answers,1,tiles);has(answers,2,math.ceil(tiles/p['boite']))
  elif family=='dimension':
   width=F(p['aire'],p['longueur']);has(answers,0,width);has(answers,1,p['aire']);has(answers,2,2*(p['longueur']+width))
 elif CODE==18:
  def instant(answer,seconds):
   h,rest=divmod(seconds%86400,3600);m,sec=divmod(rest,60)
   actual=re.search(r'(\d+) h (\d+) min(?: (\d+) s)?',answer);assert actual,answer
   assert tuple(map(int,[actual[1],actual[2],actual[3] or 0]))==(h,m,sec),(answer,h,m,sec)
  if family=='conversions':
   h,m=divmod(p['minutes'],60);a,b=divmod(p['secondes'],60);has(answers,0,h);has(answers,0,m);has(answers,1,a);has(answers,1,b);has(answers,2,p['minutes']*60)
  elif family=='horloge':
   total=p['h']*3600+p['m']*60+p['s'];instant(answers[0],total);instant(answers[1],total+45);has(answers,2,60-p['s'])
  elif family=='ecoulee':has(answers,0,60-(p['debut_s']//60)%60);has(answers,2,F(p['fin_s']-p['debut_s'],60))
  elif family=='minuit':has(answers,0,F(86400-p['depart_s'],60));has(answers,1,F(86400-p['depart_s']+p['arrivee_s'],60))
  elif family=='arrivee':has(answers,0,p['duree_s']);has(answers,1,75);instant(answers[2],p['depart_s']+p['duree_s'])
  elif family=='depart':instant(answers[0],p['rdv_s']-p['marge_s']);instant(answers[1],p['rdv_s']-p['marge_s']-p['trajet_s'])
  elif family=='decimal':
   hours=F(p['heures']);has(answers,0,hours*60);assert answers[2].startswith('Oui' if hours.denominator==1 else 'Non')
 elif CODE==19:
  v=p.get('valeurs')
  if family=='tableau':has(answers,0,sum(v));has(answers,1,v[2]-v[0]);assert v[2]==max(v) and 2*v[2]<=sum(v) and answers[2].startswith('Non')
  elif family=='double_entree':has(answers,0,v[3]);has(answers,1,v[1]+v[3]);has(answers,2,sum(v))
  elif family=='barres':has(answers,0,v[1]);has(answers,1,sum(v));has(answers,2,v[1]-v[0])
  elif family=='courbe':has(answers,0,v[2]);has(answers,1,v[3]-v[0]);assert v[3]-v[2]>max(v[1]-v[0],v[2]-v[1]);has(answers,2,v[3]-v[2])
  elif family=='disque':has(answers,0,F(p['total'],2));has(answers,1,F(p['total'],4));has(answers,2,p['total'])
  elif family=='enquete':
   counts=[p['reponses'].count(x) for x in 'ABC'];assert answers[0]==f'A : {counts[0]} ; B : {counts[1]} ; C : {counts[2]}.';has(answers,1,sum(counts))
  elif family=='critique':has(answers,0,v[1]);has(answers,1,sum(v));has(answers,2,v[1]+v[2])
 elif CODE==20:
  if family=='de':assert set(p['favorables'])<=set(range(1,7));has(answers,1,len(p['favorables']));has(answers,1,6)
  elif family=='sac':
   total=p['verts']+p['orange'];has(answers,0,total);has(answers,1,p['verts']);has(answers,1,total);assert p['verts']<p['orange'] and answers[2].startswith('Non')
  elif family=='independance':assert '1 chance sur 2' in answers[1] and answers[2].startswith('Non')
  elif family=='deux_pieces':
   pairs=['PP','PF','FP','FF'];test=[lambda x:x.count('F')==1,lambda x:x[0]==x[1],lambda x:'F' in x][p['evenement']];fav=[x for x in pairs if test(x)]
   assert all(x in answers[1] for x in fav);has(answers,2,len(fav));has(answers,2,4)
  elif family=='roue':has(answers,1,p['borne']);has(answers,2,p['borne']);has(answers,2,4)
  elif family=='couples':
   fav=[(a,b) for a in (1,2,3) for b in (1,2,3) if a+b==p['somme']];has(answers,1,len(fav));has(answers,2,len(fav));has(answers,2,9)
  elif family=='comparer':has(answers,0,p['rouges']);has(answers,0,2*p['rouges']);has(answers,1,p['rouges']);has(answers,1,3*p['rouges']);assert 'sac A' in answers[2]
 checks+=1
assert len(set(ids))==len(set(titles))==len(set(statements))==21
for file in [D/'cours_nouveau.txt',D/'fiche_nouvelle.txt']:
 text=file.read_text(encoding='utf-8');equalities(text)
 assert not re.search(r'TODO|FIXME|à compléter|\\displaystyle',text)
report={'statut':'OK','notion':CODE,'exercices':21,'questions':questions,'verifications_exactes':checks,'familles':7,'comparaison_des_fichiers_finaux':True}
(D/'verification_math.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(report,ensure_ascii=False))
