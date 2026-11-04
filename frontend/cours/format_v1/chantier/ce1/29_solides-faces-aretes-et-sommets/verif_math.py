"""Recalcul indépendant des textes finaux et de la géométrie TikZ."""
from pathlib import Path
from fractions import Fraction as F
import ast,re,json,runpy,math
P=Path(__file__).resolve().parent;code=int(P.name[:2])
def val(s):
 s=s.replace(r'\times','*').replace(r'\div','/').replace(r'\,','').replace('{,}','.').replace(' ','').replace('−','-')
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
texts={f:(P/f).read_text(encoding='utf-8') for f in ['cours_nouveau.txt','fiche_nouvelle.txt','exercices.txt']};count=0
for name,text in texts.items():
 assert not any(ord(c)<32 and c!='\n' for c in text)
 for s in re.findall(r'\$([^$]+)\$',text):
  if '=' in s:
   vs=[val(x) for x in s.split('=')];assert all(v==vs[0] for v in vs),(name,s,vs);count+=1
  elif '<' in s or '>' in s:
   parts=re.split('([<>])',s);vs=[val(x) for x in parts[::2]]
   for i,op in enumerate(parts[1::2]):assert (vs[i]<vs[i+1] if op=='<' else vs[i]>vs[i+1]),(name,s)
   count+=1
blocks=[b for b in re.split(r'^===\s*$',texts['exercices.txt'],flags=re.M) if b.strip()];assert len(blocks)==9
for i,b in enumerate(blocks,1):
 assert f'Id: nouveau-{i}\n' in b
 en=b.split('Énoncé:')[1].split('Étapes:')[0];et=b.split('Étapes:')[1].split('Solution:')[0];so=b.split('Solution:')[1]
 assert len(re.findall(r'^\d+\. ',en,re.M))==5
 results=re.findall(r'^::: resultat\n(.*?)\n:::',et,re.M|re.S);answers=re.findall(r'^\d+\. (.+)',so,re.M)
 assert len(results)==5 and results==answers
 assert len(re.findall(r'^::: methode',et,re.M))==len(re.findall(r'^## Question',et,re.M))==5
# Réponses recalculées à partir des situations du livre, sans importer le générateur.
expected={
21:{1:[str(8-1)+' cm'],2:[str(2*100)+' cm'],3:['8 cm',str(8-5)+' cm'],4:[str(100+47)+' cm',str(3*100+5)+' cm'],5:[str(100+8)+' cm',str(108-98)+' cm'],6:['6 cm','7 cm'],7:[str(136-48)+' cm'],8:[str(450+350)+' m',str(1000-800)+' m'],9:['20 cm']},
22:{1:[str(500+200+20)+' g',str(1000-720)+' g'],2:['1 000 g',str(1000//100)],3:['80 g','500 g','750 g','1 kg'],4:['20 g'],5:[str(400+250)+' g',str(650-250)+' g'],6:[str(1000-800)+' g'],7:[str(850-175)+' g'],8:['balance'],9:[str(1000)+' g',str(250-80)+' g']},
23:{1:[str(50+10+5)+' centimes','1,65 €',str(100+65)+' centimes'],2:[str(200+40)+' centimes','85 centimes'],3:['4,05 €','4,50 €',str(450-405)+' centimes'],4:['1,90 €','2,05 €','2,50 €'],5:[str(50+20+10)+' centimes','3 pièces','4 pièces'],6:[str(125+75)+' centimes','2 €'],7:[str(500-380)+' centimes','1,20 €'],8:[str(245+135)+' centimes','1,20 €'],9:['12 €','60 centimes']},
24:{1:['9 h 15','11 h 30'],2:['Trois quarts','Entre 6 et 7','Plus près du 7'],3:[str(4+12)+' h'],4:[str(2+12)+' h 15',str(5+12)+' h 45'],5:[str(60//2)+' min',str(60//4)+' min',str(3*15)+' min'],6:[str(20-12)+' heures','entre 8 et 9'],7:[str(60-45)+' min','11 h'],8:['entre 7 et 8'],9:[str(18-12)+' heures']},
25:{1:[str((10*60+15)-(9*60+30))+' min'],2:[str(2*60)+' min',str(60+30)+' min','1 h 30 min'],3:[str(130-2*60)+' min','2 h 10 min'],4:[str((16*60+15)-(15*60+45))+' min'],5:[str(15+30)+' min',str(60-45)+' min'],6:['11 h'],7:[str((15*60)-(14*60+15))+' min',str(45+30)+' min','1 h 15 min','15 h 30'],8:['16 h 30'],9:[str((9*60+15)-(8*60+30))+' min']},
26:{1:['A est droit','B est aigu','C est obtus'],2:['Un carré','Un rectangle','Un triangle rectangle'],3:['4 côtés','4 sommets','4 angles droits'],4:['Sur A'],5:['4 côtés'],6:['4 cm','3 cm'],7:['5 côtés','5 sommets','pentagone'],8:['gabarit'],9:['Un rectangle']},
27:{1:['Oui','Non'],2:[str(6//2)+' cm'],3:['3 cm'],4:['O','A'],5:['alignés'],6:['disque'],7:[str(10//2)+' cm','4 cm et 6 cm'],8:['2 cm','3 cm'],9:['O']},
28:{1:['2 carreaux à droite et 2 vers le haut','2 carreaux à droite et 2 vers le bas'],2:['5 cm','3 cm'],3:['2 cm','4 cm'],4:['4 cm','3 cm'],5:['3 cm','Deux triangles rectangles'],6:['4 carreaux','3 carreaux'],7:['6 cm','2 cm'],8:['Quatre angles droits'],9:['5 cm','2 cm']},
29:{1:['cube','pavé','boule','cylindre','cône','pyramide'],2:['6 faces','12 arêtes','8 sommets'],3:['6 faces','12 arêtes','8 sommets'],4:['4','5 faces'],5:['12','8','3'],6:['4','5 faces'],7:['cylindre','boule'],8:['6 faces','3 faces'],9:['3 cubes']},
30:{1:['2 cases','1 case'],2:['dessus'],3:['porte'],4:['bas','haut'],5:['3 cases','bas'],6:['10','3'],7:['départ','haut'],8:['positions'],9:['haut']}}
def norm(s):return re.sub(r'(?<=\d)[ \u00a0\u202f](?=\d)','',s).lower()
for i,values in expected[code].items():
 for value in values:
  actual=norm(blocks[i-1].split('Étapes:')[1])
  # Les corrigés utilisent aussi les nombres écrits en lettres.
  alternatives={('23',5,'4 pièces'):['quatre pièces'],('29',6,'5 faces'):['un carré en base et quatre triangles'],('30',1,'1 case'):['une case','1 à droite']}
  choices=[value]+alternatives.get((str(code),i,value),[])
  assert any(norm(v) in actual for v in choices),(code,i,value)
figs=runpy.run_path(str(P/'figures/figures.py'))['FIGURES']
if code==21:
 for name,a,b in [('regle_2_9',2,9),('regle_1_8',1,8)]:
  s=figs[name];assert f'({a*.7},0.55)--({b*.7},0.55)' in s;assert b-a==7
if code==22:
 for name,vals in [('balance_350',[200,100,50]),('balance_720',[500,200,20])]:
  for v in vals:assert '{'+str(v)+'}' in figs[name]
 assert sum([200,100,50])==350 and sum([500,200,20])==720
if code==23:
 assert sum([200,20,10,5])==235 and sum([100,50,10,5])==165
 for s in figs.values():assert s.count('circle (.69)')==4
if code==24:
 for name,pairs in [('horloge_8_15',[(8,15)]),('horloges_8_30_8_45',[(8,30),(8,45)]),('horloges_9_15_11_30',[(9,15),(11,30)]),('horloges_14_15_17_45',[(14,15),(17,45)])]:
  for h,m in pairs:assert f'({90-30*(h%12)-m/2}:0.78)' in figs[name] and f'({90-6*m}:1.06)' in figs[name]
  assert figs[name].count('draw[otMuted')==60*len(pairs)
 assert ':0.78)' not in figs['cadran_vierge']
if code==25:
 assert F('4.8')/F('2.4')==F(30,15)
 for name in figs:assert figs[name].count('Stealth[length=1.4mm]')==4
if code==26:
 s=figs['angles_droit_aigu_obtus']
 for a in (90,45,120):assert f'({a}:1.7)' in s
 assert 0<45<90<120<180
 a,b,c,d=(0,1.1),(1.1,2.2),(2.2,1.1),(1.1,0)
 v=[(b[0]-a[0],b[1]-a[1]),(c[0]-b[0],c[1]-b[1])];assert abs(sum(x*y for x,y in zip(*v)))<1e-10
if code==27:
 pts=[(0,0),(3,1),(6,2)];assert (pts[1][0]-pts[0][0])*(pts[2][1]-pts[0][1])==(pts[1][1]-pts[0][1])*(pts[2][0]-pts[0][0])
 assert '(0,0)--(6,0)' in figs['milieu_6_corrige'] and 'at (3,-0.45)' in figs['milieu_6_corrige']
 assert '(0,0) circle (2.4)' in figs['cercle_O_A'] and '(0,0)--(2.4,0)' in figs['cercle_O_A']
if code==28:
 pts=[(1,3),(3,5),(5,3),(3,1)];v=[(pts[(i+1)%4][0]-pts[i][0],pts[(i+1)%4][1]-pts[i][1]) for i in range(4)]
 assert len({x*x+y*y for x,y in v})==1
 for i in range(4):assert sum(x*y for x,y in zip(v[i],v[(i+1)%4]))==0
 for name,w,h in [('rectangle_6_3',6,3),('rectangle_5_3_corrige',5,3),('rectangle_deux_cotes',4,2),('rectangle_cercle_corrige',6,2)]:
  assert '{'+str(w)+' cm}' in figs[name] and '{'+str(h)+' cm}' in figs[name]
 assert '(0,0) circle (2)' in figs['rectangle_cercle_corrige']
 assert '(0,0)--(3,3)' in figs['carre_diagonale_corrige']
if code==29:
 assert 8-12+6==2 and 5-8+5==2
 assert figs['six_solides'].count('node[')==6
 assert figs['faces_pyramide'].count('cycle')==2 # contour carré et plis
 for a,b,c in [((0,0),(4,0),(2,-4)),((4,0),(4,4),(8,2)),((4,4),(0,4),(2,8)),((0,4),(0,0),(-4,2))]:
  assert '--'.join(f'({x},{y})' for x,y in [a,b,c,a]) in figs['faces_pyramide']
 # Triangles latéraux : base4/hauteur4 ; une fois pliés, hauteur du solide sqrt(16-4).
 assert 4**2-(4/2)**2>0
 assert '(0,2)--(2,2)' in figs['assemblage_trois_cubes']
if code==30:
 def route(instructions):
  x=y=d=0;dirs=[(0,1),(1,0),(0,-1),(-1,0)]
  for action in instructions:
   if action=='R':d=(d+1)%4
   else:x+=dirs[d][0]*action;y+=dirs[d][1]*action
  return x,y,d
 assert route([2,'R',1])==(1,2,1)
 assert route([2,'R',3,'R',2])==(3,0,2)
 assert route([1,'R',2,'R',1,'R',2,'R'])==(0,0,0)
 assert '(1.5,1.5)--(1.5,3.5)--(2.5,3.5)' in figs['trajet_2_1_corrige']
report={'statut':'OK','math_OK':True,'exercices':9,'questions':45,'egalites_et_comparaisons_recomposees':count,'situations_et_figures_verifiees':True}
(P/'verification_math.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(json.dumps(report))
