"""Figures TikZ du lot root, compilation officielle avec contrôle des intersections."""
from pathlib import Path
import json,sys,subprocess
ROOT=Path(__file__).resolve().parent.parent
def tikz(body,options=''):return r'\begin{tikzpicture}['+options+']\n'+body+'\n'+r'\end{tikzpicture}'
def clock(h,m,s,label=''):
 lines=[r'\draw[otRule,line width=.9pt] (0,0) circle (2.1);']
 for i in range(60):
  a=90-i*6;inside=1.94 if i%5==0 else 2.02
  lines.append(rf'\draw[otMuted,line width=.5pt] ({a}:{inside}) -- ({a}:2.1);')
 for i in range(1,13):lines.append(rf'\node[text=otInk] at ({90-30*i}:1.7) {{{i}}};')
 for angle,length,color,width in [(90-30*((h%12)+m/60+s/3600),1.03,'otNavy',1.8),(90-6*(m+s/60),1.4,'otGreenDark',1.3),(90-6*s,1.55,'otOrange',.9)]:
  lines.append(rf'\draw[{color},line width={width}pt,-{{Stealth[length=2mm]}}] (0,0)--({angle}:{length});')
 lines.append(r'\fill[otInk] (0,0) circle (1.5pt);')
 if label:lines.append(rf'\node[text=otNavy] at (0,2.65) {{{label}}};')
 return tikz('\n'.join(lines))
def graph(values,curve=False):
 n=len(values);top=max(values)+2;lines=[]
 for v in range(0,top+1,2):
  lines.append(rf'\draw[otRule,line width=.35pt] (0,{v*.17})--({n*1.15+.5},{v*.17});')
  lines.append(rf'\node[anchor=east,text=otMuted] at (-.15,{v*.17}) {{{v}}};')
 lines.append(rf'\draw[otMuted,-{{Stealth}}] (0,0)--({n*1.15+.8},0);')
 lines.append(rf'\draw[otMuted,-{{Stealth}}] (0,0)--(0,{top*.17+.25});')
 lines.append(rf'\node[anchor=west,text=otInk] at (0,{top*.17+.7}) {{{"Hauteur (cm)" if curve else "Nombre de prêts"}}};')
 for i,v in enumerate(values):
  x=(i+1)*1.15
  lines.append(rf'\node[anchor=north,text=otMuted] at ({x},-.18) {{{i+1 if curve else ["Lun","Mar","Mer"][i]}}};')
  if curve:lines.append(rf'\fill[otNavy] ({x},{v*.17}) circle (2pt);')
  else:lines.append(rf'\filldraw[fill=otNavy!18,draw=otNavy,line width=.8pt] ({x-.32},0) rectangle ({x+.32},{v*.17});')
 if curve:
  coords='--'.join(f'({(i+1)*1.15},{v*.17})' for i,v in enumerate(values));lines.append(rf'\draw[otNavy,line width=1pt] {coords};')
  lines.append(rf'\node[anchor=west,text=otMuted] at ({n*1.15+.45},-.55) {{Semaine}};')
 return tikz('\n'.join(lines))

FIGS={11:{},12:{},18:{},19:{},20:{}}
regle=[]
for x in range(0,81):
 xx=x*.075;h=.22 if x%10==0 else .12
 regle.append(rf'\draw[otMuted] ({xx},0)--({xx},{-h});')
 if x%10==0:regle.append(rf'\node[anchor=north,text=otMuted] at ({xx},-.3) {{{x}}};')
regle += [r'\draw[otMuted] (0,0)--(6,0);',r'\draw[otNavy,line width=1.5pt] (1.125,.55)--(5.1,.55);',r'\draw[otNavy,dashed] (1.125,.1)--(1.125,.85);',r'\draw[otNavy,dashed] (5.1,.1)--(5.1,.85);',r'\node[anchor=south,text=otNavy] at (1.125,1) {15 mm};',r'\node[anchor=south,text=otNavy] at (5.1,1) {68 mm};',r'\node[text=otMuted] at (3,-1) {Graduations en millimètres};']
FIGS[11]['regle_decalee']=tikz('\n'.join(regle))
FIGS[11]['rectangle_contour']=tikz(r'''\draw[otNavy,line width=1.2pt] (0,0) rectangle (5,3);
\node[anchor=south] at (2.5,3.3) {5 cm};
\node[anchor=west] at (5.3,1.5) {3 cm};
\node[text=otGreenDark] at (2.5,-.6) {Le contour suit les quatre côtés.};''')
FIGS[12]['unite_aire']=tikz(r'''\fill[otNavy!6] (0,0) rectangle (4,4);
\fill[otGreen!45] (0,0) rectangle (.4,.4);
\draw[step=.4,otRule,line width=.35pt] (0,0) grid (4,4);
\draw[otNavy,line width=1pt] (0,0) rectangle (4,4);
\draw[otMuted,<->] (0,-.5)--(4,-.5);
\node[anchor=north] at (2,-.7) {1 dm = 10 cm};
\node[anchor=west,text=otGreenDark] at (4.3,.2) {1 cm$^2$};
\node[anchor=south] at (2,4.3) {10 rangées de 10 petits carrés};''')
FIGS[12]['rectangle_aire']=tikz(r'''\fill[otNavy!10] (0,0) rectangle (4,3);
\draw[step=1,otRule,line width=.5pt] (0,0) grid (4,3);
\draw[otNavy,line width=1pt] (0,0) rectangle (4,3);
\node[anchor=south] at (2,3.3) {4 cm};
\node[anchor=west] at (4.3,1.5) {3 cm};
\node[text=otMuted] at (2,-.6) {Chaque petit carré vaut 1 cm$^2$.};''')
FIGS[12]['aire_contours']=tikz(r'''\filldraw[fill=otNavy!10,draw=otNavy] (0,0) rectangle (4,.5);
\filldraw[fill=otGreen!14,draw=otGreenDark] (0,-2) rectangle (2,-1);
\node[anchor=south] at (2,.8) {8 cm sur 1 cm};
\node[anchor=north] at (1,-2.3) {4 cm sur 2 cm};
\node[anchor=west,text=otInk] at (4.5,-.7) {Même aire,};
\node[anchor=west,text=otInk] at (4.5,-1.3) {contours différents.};''')
for t in range(3):
 l=8+t;w=6+t;a=3+t;b=2;s=.43
 FIGS[12][f'piece_l_{t}']=tikz(rf'''\filldraw[fill=otNavy!10,draw=otNavy,line width=1pt] (0,0)--({l*s},0)--({l*s},{(w-b)*s})--({(l-a)*s},{(w-b)*s})--({(l-a)*s},{w*s})--(0,{w*s})--cycle;
\draw[otMuted,dashed] ({(l-a)*s},{w*s})--({l*s},{w*s})--({l*s},{(w-b)*s});
\node[anchor=north] at ({l*s/2},-.25) {{{l} m}};
\node[anchor=east] at (-.25,{w*s/2}) {{{w} m}};
\node[anchor=south] at ({(l-a/2)*s},{w*s+.25}) {{{a} m}};
\node[anchor=west] at ({l*s+.25},{(w-b/2)*s}) {{{b} m}};''')
FIGS[18]['horloge_cours']=clock(10,10,30)
for t,(h,m,s) in enumerate([(8,20,15),(11,45,30),(16,10,45)]):FIGS[18][f'horloge_{t}']=clock(h,m,s,'Cadran '+'ABC'[t])
FIGS[18]['frise_duree']=tikz(r'''\draw[otMuted,-{Stealth}] (0,0)--(7.9,0);
\fill[otNavy] (0,0) circle (2pt);\fill[otNavy] (1.2,0) circle (2pt);\fill[otNavy] (6,0) circle (2pt);\fill[otNavy] (7.6,0) circle (2pt);
\node[anchor=south] at (0,.35) {13 h 45};\node[anchor=south] at (1.2,1.05) {14 h};
\node[anchor=south] at (6,.35) {15 h};\node[anchor=south] at (7.6,1.05) {15 h 20};
\node[text=otGreenDark] at (.6,-.7) {15 min};\node[text=otGreenDark] at (3.6,-.7) {1 h};\node[text=otGreenDark] at (6.8,-.7) {20 min};''')
for t in range(3):
 FIGS[19][f'barres_{t}']=graph([4+2*t,8+2*t,6+2*t])
 FIGS[19][f'courbe_{t}']=graph([6+2*t,10+2*t,12+2*t,18+2*t],True)
FIGS[19]['disque_parts']=tikz(r'''\fill[otNavy!25] (0,0)--(90:1.8) arc (90:270:1.8)--cycle;
\fill[otGreen!30] (0,0)--(270:1.8) arc (270:360:1.8)--cycle;
\fill[otOrange!35] (0,0)--(0:1.8) arc (0:90:1.8)--cycle;
\draw[otNavy,line width=.8pt] (0,0) circle(1.8);
\draw[otNavy] (0,-1.8)--(0,1.8);\draw[otNavy] (0,0)--(1.8,0);
\node[text=otInk] at (-.85,0) {A};\node[text=otInk] at (.8,-.8) {B};\node[text=otInk] at (.8,.8) {C};
\node[anchor=west] at (2.3,.9) {A : moitié};\node[anchor=west] at (2.3,0) {B : quart};\node[anchor=west] at (2.3,-.9) {C : quart};''')
FIGS[20]['roue_quatre']=tikz(r'''\fill[otNavy!18] (0,0)--(0:1.8) arc(0:90:1.8)--cycle;
\fill[otGreen!25] (0,0)--(90:1.8) arc(90:180:1.8)--cycle;
\fill[otOrange!28] (0,0)--(180:1.8) arc(180:270:1.8)--cycle;
\fill[otNavy!8] (0,0)--(270:1.8) arc(270:360:1.8)--cycle;
\draw[otNavy] (0,0) circle(1.8);\draw[otNavy] (-1.8,0)--(1.8,0);\draw[otNavy] (0,-1.8)--(0,1.8);
\node at (.8,.8) {1};\node at (-.8,.8) {2};\node at (-.8,-.8) {3};\node at (.8,-.8) {4};
\draw[otOrange,line width=1pt,-{Stealth[length=2.5mm]}] (0,2.7)--(0,2);
\node[anchor=west,text=otMuted] at (2.3,0) {Quatre secteurs égaux};''')
FIGS[20]['arbre_pieces']=tikz(r'''\draw[otMuted] (0,0)--(2,1.2);\draw[otMuted] (0,0)--(2,-1.2);
\draw[otMuted] (2.4,1.2)--(4.4,1.9);\draw[otMuted] (2.4,1.2)--(4.4,.5);
\draw[otMuted] (2.4,-1.2)--(4.4,-.5);\draw[otMuted] (2.4,-1.2)--(4.4,-1.9);
\node[text=otNavy] at (2.2,1.2) {P};\node[text=otNavy] at (2.2,-1.2) {F};
\node[anchor=west] at (4.7,1.9) {PP};\node[anchor=west,text=otGreenDark] at (4.7,.5) {PF};
\node[anchor=west,text=otGreenDark] at (4.7,-.5) {FP};\node[anchor=west] at (4.7,-1.9) {FF};
\node[text=otMuted] at (2.2,2.8) {Premier lancer};\node[text=otMuted] at (5,2.8) {Deux lancers};''')
neutral=FIGS[20]['arbre_pieces'].replace('anchor=west,text=otGreenDark','anchor=west')
for tier,favorables in [(1,['PP','FF']),(2,['PF','FP','FF'])]:
 body=neutral
 for label in favorables:body=body.replace(r'\node[anchor=west] at '+{'PP':'(4.7,1.9)','PF':'(4.7,.5)','FP':'(4.7,-.5)','FF':'(4.7,-1.9)'}[label],r'\node[anchor=west,text=otGreenDark] at '+{'PP':'(4.7,1.9)','PF':'(4.7,.5)','FP':'(4.7,-.5)','FF':'(4.7,-1.9)'}[label])
 FIGS[20][f'arbre_pieces_{tier}']=body

COURSE={11:['regle_decalee','rectangle_contour'],12:['unite_aire','rectangle_aire','aire_contours'],18:['horloge_cours','frise_duree'],19:['barres_0','courbe_0','disque_parts'],20:['roue_quatre','arbre_pieces']}
ALTS={'regle_decalee':'Segment allant de 15 à 68 millimètres sur une règle graduée.','rectangle_contour':'Rectangle de 5 centimètres sur 3 centimètres dont les quatre côtés forment le contour.','unite_aire':'Carré de dix centimètres de côté partagé en cent petits carrés de un centimètre carré.','rectangle_aire':'Rectangle de quatre centimètres sur trois, partagé en douze centimètres carrés.','aire_contours':'Deux rectangles de même aire, huit centimètres carrés, avec des contours différents.','horloge_cours':'Horloge montrant dix heures dix minutes et trente secondes.','frise_duree':'Frise de treize heures quarante-cinq à quinze heures vingt, décomposée en trois étapes.','disque_parts':'Disque partagé en une moitié A et deux quarts B et C.','roue_quatre':'Roue équilibrée partagée en quatre secteurs égaux numérotés de un à quatre.','arbre_pieces':'Arbre des quatre issues ordonnées de deux lancers successifs d’une pièce équilibrée.'}
def alt(code,name):
 if name.startswith('arbre_pieces_'):
  return 'Arbre des quatre issues de deux lancers, avec en vert '+('les deux résultats identiques.' if name.endswith('1') else 'les trois issues contenant au moins une fois face.')
 if name in ALTS:return ALTS[name]
 if name.startswith('piece_l_'):
  t=int(name[-1]);return f'Pièce en L obtenue en retirant un coin de {3+t} mètres sur 2 à un rectangle de {8+t} mètres sur {6+t}.'
 if name.startswith('horloge_'):
  t=int(name[-1]);h,m,s=[(8,20,15),(11,45,30),(16,10,45)][t];return f'Cadran {"ABC"[t]} indiquant {h} heures {m} minutes et {s} secondes.'
 if name.startswith('barres_'):
  t=int(name[-1]);return f'Prêts de livres le lundi, mardi et mercredi : {4+2*t}, {8+2*t} et {6+2*t} livres.'
 if name.startswith('courbe_'):
  t=int(name[-1]);return f'Hauteurs d’une plante en quatre semaines : {6+2*t}, {10+2*t}, {12+2*t} et {18+2*t} centimètres.'
 raise ValueError(name)
if __name__=='__main__':
 codes=[int(a) for a in sys.argv[1:] if a.isdigit()] or list(FIGS)
 for code in codes:
  d=next(ROOT.glob(f'{code:02}_*'));f=d/'figures';f.mkdir(exist_ok=True)
  script='from pathlib import Path\nimport sys\nsys.path.insert(0,str(Path(__file__).resolve().parents[4]/"outils"))\nfrom figures_livre import compiler\nFIGURES = '+repr(FIGS[code])+'\nif __name__=="__main__":\n noms=sys.argv[1:] or list(FIGURES)\n assert len(compiler(FIGURES,Path(__file__).parent,noms,jobs=1))==len(noms)\n'
  (f/'figures.py').write_text(script,encoding='utf-8')
  corr={'cours':{'nouveau':{str(i):{'fichier':name+'.png','alt':alt(code,name)} for i,name in enumerate(COURSE[code],1)}},'fiches':{},'exercices':{}}
  for item in json.loads((d/'donnees_exercices_root.json').read_text(encoding='utf-8')):
   name=item['figure']
   if name:corr['exercices'][item['id']]={'1':{'fichier':name+'.png','alt':alt(code,name)}}
  (f/'correspondance.json').write_text(json.dumps(corr,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
  if '--compiler' in sys.argv:
   result=subprocess.run([sys.executable,str(f/'figures.py')],capture_output=True,text=True,encoding='utf-8')
   (d/'compilation_figures.log').write_text(result.stdout+result.stderr,encoding='utf-8');print(code,result.stdout,flush=True)
   assert result.returncode==0,result.stderr
