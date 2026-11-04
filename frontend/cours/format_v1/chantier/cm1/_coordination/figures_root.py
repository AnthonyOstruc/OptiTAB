from pathlib import Path
import json,subprocess,sys,ast
ICI=Path(__file__).resolve().parent;ROOT=ICI.parent
# Réutilisation de deux fonctions pures du chantier CM2, sans exécuter ce chantier.
old=(ROOT.parent/'cm2/_coordination/figures_root.py').read_text(encoding='utf-8');tree=ast.parse(old)
ns={}
for node in tree.body:
 if isinstance(node,ast.FunctionDef) and node.name in ('tikz','graph'):exec(compile(ast.Module(body=[node],type_ignores=[]),'<fonctions-graphiques>','exec'),ns)
tikz=ns['tikz'];graph=ns['graph']
def clock(h,m):
 lines=[r'\draw[otRule,line width=.8pt] (0,0) circle (2);']
 for i in range(60):
  a=90-6*i;inner=1.84 if i%5==0 else 1.93
  lines.append(rf'\draw[otMuted,line width=.5pt] ({a}:{inner})--({a}:2);')
 for i in range(1,13):lines.append(rf'\node[text=otInk] at ({90-30*i}:1.58) {{{i}}};')
 for a,l,col,w in [(90-30*((h%12)+m/60),.98,'otNavy',1.8),(90-6*m,1.4,'otGreenDark',1.4)]:lines.append(rf'\draw[{col},line width={w}pt,-{{Stealth[length=2mm]}}] (0,0)--({a}:{l});')
 lines.append(r'\fill[otInk] (0,0) circle (1.5pt);')
 return tikz('\n'.join(lines))
figs={c:{} for c in (11,12,13,14,20,21)}
lines=[]
for i in range(81):
 x=i*.075;lines.append(rf'\draw[otMuted] ({x},0)--({x},{-.22 if i%10==0 else -.1});')
 if i%10==0:lines.append(rf'\node[anchor=north,text=otMuted] at ({x},-.3) {{{i}}};')
lines += [r'\draw[otMuted] (0,0)--(6,0);',r'\draw[otNavy,line width=1.5pt] (1.125,.6)--(5.1,.6);',r'\draw[otNavy,dashed] (1.125,.1)--(1.125,.9);',r'\draw[otNavy,dashed] (5.1,.1)--(5.1,.9);',r'\node[anchor=south] at (1.125,1.05) {15 mm};',r'\node[anchor=south] at (5.1,1.05) {68 mm};',r'\node at (3,-1) {Graduations en millimètres};']
figs[11]['regle']=tikz('\n'.join(lines))
for t in range(3):
 a=10+5*t;b=65+10*t;lines=[]
 for i in range(91):
  x=i*.065;lines.append(rf'\draw[otMuted] ({x},0)--({x},{-.22 if i%10==0 else -.1});')
  if i%10==0:lines.append(rf'\node[anchor=north,text=otMuted] at ({x},-.3) {{{i}}};')
 lines += [r'\draw[otMuted] (0,0)--(5.85,0);',rf'\draw[otNavy,line width=1.5pt] ({a*.065},.6)--({b*.065},.6);',rf'\draw[otNavy,dashed] ({a*.065},.1)--({a*.065},.9);',rf'\draw[otNavy,dashed] ({b*.065},.1)--({b*.065},.9);',rf'\node[anchor=south] at ({a*.065},1.05) {{{a} mm}};',rf'\node[anchor=south] at ({b*.065},1.05) {{{b} mm}};',r'\node at (2.925,-1) {Graduations en millimètres};']
 figs[11][f'regle_{t}']=tikz('\n'.join(lines))
figs[11]['contour']=tikz(r'''\draw[otNavy,line width=1.2pt] (0,0) rectangle (5,3);
\node[anchor=south] at (2.5,3.3) {5 cm};
\node[anchor=west] at (5.3,1.5) {3 cm};
\node[anchor=north,text=otGreenDark] at (2.5,-.35) {Le contour suit quatre côtés.};''')
figs[12]['balance']=tikz(r'''\draw[otNavy,line width=1pt] (-2.5,1.6)--(2.5,1.6);
\draw[otNavy,line width=1pt] (0,1.6)--(-.65,0)--(.65,0)--cycle;
\draw[otMuted] (-2.1,1.6)--(-2.7,.25)--(-1.5,.25)--cycle;
\draw[otMuted] (2.1,1.6)--(1.5,.25)--(2.7,.25)--cycle;
\node[anchor=south] at (-2.1,1.95) {Sac};
\node[anchor=south] at (2.1,1.95) {500 g + 200 g + 50 g};
\node[anchor=north,text=otGreenDark] at (0,-.4) {Équilibre : masses égales.};''')
for t in range(3):
 L=4+t
 figs[13][f'surface_l_{t}']=tikz(rf'''\fill[otNavy!12] (0,0)--({L},0)--({L},2)--({L-2},2)--({L-2},3)--(0,3)--cycle;
\draw[step=1,otRule] (0,0) grid ({L},3);
\draw[otNavy,line width=1.1pt] (0,0)--({L},0)--({L},2)--({L-2},2)--({L-2},3)--(0,3)--cycle;
\draw[otMuted,dashed] ({L-2},3)--({L},3)--({L},2);
\node[anchor=north] at ({L/2},-.4) {{Chaque carreau est une unité d’aire.}};''')
figs[13]['angles_comparaison']=tikz(r'''\draw[otNavy,line width=1.1pt] (1.1,1.1)--(0,0)--(1.5,0);
\draw[otNavy] (.42,0) arc (0:45:.42);
\node[anchor=north] at (.6,-.35) {A};
\draw[otNavy,line width=1.1pt] (3,1.5)--(3,0)--(4.5,0);
\draw[otNavy] (3,.3)--(3.3,.3)--(3.3,0);
\node[anchor=north] at (3.6,-.35) {B};
\draw[otNavy,line width=1.1pt] (5.1,1.2)--(6,0)--(7.5,0);
\draw[otNavy] (6.42,0) arc (0:127:.42);
\node[anchor=north] at (6.5,-.35) {C};''')
for t in range(3):figs[14][f'horloge_{t}']=clock(8+t,20+10*t)
figs[14]['frise']=tikz(r'''\draw[otRule,-{Stealth}] (0,0)--(6.3,0);
\fill[otNavy] (0,0) circle (1.8pt) (3.2,0) circle (1.8pt) (5.6,0) circle (1.8pt);
\node[anchor=south] at (0,.4) {9 h 40};
\node[anchor=south] at (3.2,.4) {10 h};
\node[anchor=south] at (5.6,.4) {10 h 15};
\node[anchor=north,text=otGreenDark] at (1.6,-.35) {20 min};
\node[anchor=north,text=otGreenDark] at (4.4,-.35) {15 min};''')
for t in range(3):
 figs[20][f'barres_{t}']=graph([4+2*t,8+2*t,6+2*t])
 figs[20][f'courbe_{t}']=graph([6+2*t,10+2*t,12+2*t,18+2*t],True)
 lost=4-t;bonbon=3;toy=1+t;lines=[]
 for i in range(8):
  a=90-45*i;b=a-45;col='otNavy!15' if i<lost else 'otGreen!20' if i<lost+bonbon else 'otOrange!22'
  lines.append(rf'\filldraw[fill={col},draw=otNavy,line width=.7pt] (0,0)--({a}:1.7) arc ({a}:{b}:1.7)--cycle;')
  lines.append(rf'\node[text=otInk] at ({a-22.5}:1.17) {{{i+1}}};')
 lines += [rf'\node[anchor=north] at (0,-2.05) {{1 à {lost} : perdu}};',rf'\node[anchor=north,text=otGreenDark] at (0,-2.6) {{{lost+1} à {lost+bonbon} : bonbon}};',rf'\node[anchor=north] at (0,-3.15) {{{"8" if toy==1 else str(lost+bonbon+1)+" à 8"} : peluche}};',r'\node[anchor=south] at (0,2) {Huit secteurs égaux};']
 figs[21][f'roue_{t}']=tikz('\n'.join(lines))
docs={11:['regle','contour'],12:['balance'],13:['surface_l_0','angles_comparaison'],14:['horloge_0','frise'],20:['barres_0','courbe_0'],21:['roue_0']}
alts={'regle':'Règle graduée en millimètres et segment de la graduation 15 à la graduation 68.','contour':'Rectangle dont les côtés mesurent 5 cm et 3 cm ; le contour suit ses quatre côtés.','balance':'Balance en équilibre entre un sac et trois masses de 500 g, 200 g et 50 g.','angles_comparaison':'Trois angles A, B et C, respectivement moins ouvert, égal et plus ouvert que l’angle droit.','frise':'Frise proportionnelle de 9 h 40 à 10 h 15, avec une étape à 10 h et des durées de 20 min et 15 min.'}
for code,fig in figs.items():
 d=next(ROOT.glob(f'{code:02}_*'));folder=d/'figures'
 text='from pathlib import Path\nFIGURES = '+repr(fig)+'\nTOLERE = {}\n'
 (folder/'figures.py').write_text(text,encoding='utf-8')
 def alt(name):
  if name in alts:return alts[name]
  t=int(name.rsplit('_',1)[-1])
  if name.startswith('regle_'):return f'Règle graduée en millimètres et segment de la graduation {10+5*t} à la graduation {65+10*t}.'
  if name.startswith('horloge'):return f'Horloge à deux aiguilles indiquant {8+t} h {20+10*t} min le matin.'
  if name.startswith('surface_l'):return f'Rectangle de trois rangées de {4+t} carreaux auquel deux carreaux du coin supérieur droit ont été retirés.'
  if name.startswith('barres'):return f'Diagramme des prêts de lundi, mardi et mercredi : {4+2*t}, {8+2*t} et {6+2*t} prêts.'
  if name.startswith('courbe'):return f'Courbe de la hauteur d’une plante aux semaines 1 à 4 : {6+2*t}, {10+2*t}, {12+2*t} et {18+2*t} cm.'
  return f'Roue de huit secteurs égaux, avec {4-t} secteurs perdu, trois secteurs bonbon et {1+t} secteurs peluche.'
 def spec(name):return {'fichier':name+'.png','alt':alt(name)}
 corr={'cours':{'nouveau':{str(i):spec(name) for i,name in enumerate(docs[code],1)}},'fiches':{},'exercices':{}}
 for item in json.loads((d/'donnees_exercices_root.json').read_text(encoding='utf-8')):
  if item['figures']:corr['exercices'][item['id']]={p:spec(Path(name).stem) for p,name in item['figures'].items()}
 (folder/'correspondance.json').write_text(json.dumps(corr,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 print(code,len(fig),'figures préparées',flush=True)
 if '--compiler' in sys.argv:subprocess.run([sys.executable,'-X','utf8',str(ROOT.parents[1]/'outils/figures_livre.py'),str(d),'--jobs','1'],check=True)
