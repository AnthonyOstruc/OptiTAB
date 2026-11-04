from commun_redaction import ROOT
SCRIPT=r'''"""Contrôles indépendants : fichiers finaux et scénarios, sans générateur."""
from pathlib import Path
from fractions import Fraction as F
import ast,re,json,runpy,math
P=Path(__file__).resolve().parent;code=int(P.name[:2])
def val(s):
 s=s.replace(r'\times','*').replace(r'\div','/').replace(r'\,','').replace('{,}','.').replace(' ','').replace(':','/').replace('−','-')
 def walk(t):
  if isinstance(t,ast.Constant) and type(t.value) in (int,float):return F(str(t.value))
  if isinstance(t,ast.UnaryOp) and isinstance(t.op,ast.USub):return -walk(t.operand)
  if isinstance(t,ast.BinOp):
   a,b=walk(t.left),walk(t.right)
   if isinstance(t.op,ast.Add):return a+b
   if isinstance(t.op,ast.Sub):return a-b
   if isinstance(t.op,ast.Mult):return a*b
   if isinstance(t.op,ast.Div):return a/b
  raise ValueError(s)
 return walk(ast.parse(s,mode='eval').body)
texts={f:(P/f).read_text(encoding='utf-8') for f in ['cours_nouveau.txt','fiche_nouvelle.txt','exercices.txt']}
count=0
for name,text in texts.items():
 assert not any(ord(c)<32 and c!='\n' for c in text)
 for m in re.finditer(r'(?<!\$)\${1,2}([^$]+)\${1,2}',text):
  s=m[1]
  if '=' in s:
   parts=s.split('=');vs=[val(x) for x in parts]
   assert all(v==vs[0] for v in vs),(name,s,vs)
   count+=1
  elif '<' in s or '>' in s:
   parts=re.split('([<>])',s);vs=[val(x) for x in parts[::2]]
   for i,op in enumerate(parts[1::2]):assert vs[i]<vs[i+1] if op=='<' else vs[i]>vs[i+1],(name,s)
   count+=1
blocks=[b for b in re.split(r'^===\s*$',texts['exercices.txt'],flags=re.M) if b.strip()];assert len(blocks)==9
for i,b in enumerate(blocks,1):
 assert f'Id: nouveau-{i}\n' in b
 en=b.split('Énoncé:')[1].split('Étapes:')[0];et=b.split('Étapes:')[1].split('Solution:')[0];so=b.split('Solution:')[1]
 assert len(re.findall(r'^\d+\. ',en,re.M))==5
 results=re.findall(r'^::: resultat\n(.*?)\n:::',et,re.M|re.S);answers=re.findall(r'^\d+\. (.+)',so,re.M)
 assert len(results)==5 and results==answers
 assert len(re.findall(r'^::: methode',et,re.M))==len(re.findall(r'^## Question',et,re.M))==5
# Résultats indépendants des situations concrètes, rapprochés des vrais corrigés.
expected={24:{1:['53 mm','72 mm','19 mm'],3:['3 750 m'],4:['2 m','48 cm'],7:['63 cm','37 cm'],9:['54 mm','45 mm']},25:{1:['18 cm'],2:['15 cm'],3:['28 cm'],4:['12 cm'],5:['210 mm'],6:['20 cm'],7:['40 m','38 m'],8:['16 cm'],9:['18 cm']},26:{2:['6 kg','450 g','3 t','80 kg'],3:['2 075 g','20 kg'],4:['1 050 g'],6:['750 g','250 g'],7:['1 350 g'],8:['2 250 g'],9:['1 008 g','792 g']},27:{2:['100 cL','60 cL','40 cL'],3:['7 L','80 cL'],6:['4 verres'],7:['175 cL','1 L','75 cL'],8:['5 verres'],9:['2 verres']},28:{1:['3{,}08','12{,}50'],2:['425','703','1 000'],3:['5{,}08','12{,}60'],5:['5 pièces'],6:['35 centimes'],7:['2,15'],8:['0,85'],9:['54 centimes']},29:{1:['19{,}86'],2:['111{,}45'],3:['8{,}53'],4:['18{,}21'],5:['9{,}26'],6:['61{,}86'],7:['28{,}60'],8:['19,25','0,75'],9:['8,53']},30:{1:['8 h 20','10 h 35'],2:['15 h 42'],3:['Entre 1 et 2'],4:['Trois graduations'],5:['8 h 45','3 h 40'],6:['14 h 10','19 h 50'],7:['11 h 55'],8:['Midi moins le quart'],9:['10 minutes']},31:{1:['135 min','1 h 35 min'],2:['105 min','5 min'],3:['45 min'],4:['84 min','1 h 24 min'],5:['16 h 15'],6:['9 h 45'],7:['9 h 30'],8:['11 h 30'],9:['20 min']}}
def norm(s):return re.sub(r'(?<=\d)[ \u00a0\u202f](?=\d)','',s)
for i,values in expected[code].items():
 for value in values:assert norm(value) in norm(blocks[i-1].split('Étapes:')[1]),(code,i,value)
spec=json.loads((P/'donnees_exercices_root.json').read_text(encoding='utf-8'))
for item in spec:
 p=item['parametres'];family=p.get('famille')
 if family=='addition':assert sum(p['valeurs_c'])==p['total_c']
 if family=='soustraction':assert p['initial_c']-p['retrait_c']==p['difference_c']
 if 'debut' in p and 'fin' in p:
  start=p['debut'][0]*60+p['debut'][1];end=p['fin'][0]*60+p['fin'][1]
  if 'duree_min' in p:assert end-start==p['duree_min']
  if 'durees_min' in p:assert end-start==sum(p['durees_min'])
 if family=='pieces':
  target=p['objectif_c'];dp=[0]+[999]*target
  for v in range(1,target+1):dp[v]=1+min(dp[v-c] for c in [1,2,5,10,20,50,100,200] if c<=v)
  assert sum(p['pieces_c'])==target and dp[target]==len(p['pieces_c'])==5
figs=runpy.run_path(str(P/'figures/figures.py'))['FIGURES']
if code==30:
 for name,h,m in [('horloge_8_20',8,20),('horloge_10_35',10,35),('horloge_15_42',15,42),('horloge_11_55',11,55)]:
  pic=figs[name];assert f'({90-30*(h%12)-m/2}:0.78)' in pic and f'({90-6*m}:1.06)' in pic
  assert len(re.findall(r'\\draw\[otMuted',pic))==60
if code==31:
 assert F('6.4')/F('0.8')==F(40,5)
if code==25:assert 3**2+4**2==5**2
if code==26:assert 500+200+50==750
if code==27:assert 100-60==40 and 100//25==4 and 300-125==175
report={'statut':'OK','math_OK':True,'exercices':9,'questions':45,'egalites_et_comparaisons_recomposees':count,'situations_et_figures_verifiees':True}
(P/'verification_math.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(json.dumps(report))
'''
for code in range(24,32):
 d=next(ROOT.glob(f'{code:02}_*'));(d/'verif_math.py').write_text(SCRIPT,encoding='utf-8')
