"""Figures TikZ exactes du lot numérique ; compilation commune sans modification."""
from pathlib import Path
from fractions import Fraction as F
import json,sys
ROOT=Path(__file__).resolve().parent.parent
sys.path.insert(0,str(Path(__file__).resolve().parent))
from rediger_exercices_coordination import d

def axis(origin,pas):
 text=[r'\begin{tikzpicture}[x=0.65cm,y=1cm]',r'\draw[otMuted,-{Stealth}] (-0.2,0)--(10.6,0);']
 for i in range(11):text.append(rf'\draw[otMuted] ({i},-0.08)--({i},0.08);')
 for i in (0,5,10):text.append(rf'\node[below=7pt,text=otMuted] at ({i},0) {{${d(origin+i*pas)}$}};')
 for pos,name in [(3,'A'),(8,'B')]:
  text+=[rf'\fill[otNavy] ({pos},0) circle (1.5pt);',rf'\node[above=8pt,text=otNavy] at ({pos},0) {{${name}$}};']
 text.append(r'\end{tikzpicture}');return '\n'.join(text)
def bars(k,total):
 s=[r'\begin{tikzpicture}[x=1cm,y=1cm]']
 s.append(r'\node[anchor=east,text=otInk] at (-0.2,1.55) {Mia};')
 s.append(r'\draw[otNavy,fill=otSky] (0,1.3) rectangle (1.25,1.8);')
 s.append(r'\node[anchor=east,text=otInk] at (-0.2,0.55) {Léo};')
 for i in range(k):s.append(rf'\draw[otNavy,fill=otSky] ({i*1.25},0.3) rectangle ({(i+1)*1.25},0.8);')
 s+=[rf'\node[anchor=west,text=otInk] at ({k*1.25+0.3},1.05) {{Total : {total}}};',r'\node[below,text=otMuted] at (0.625,0) {Une case = une part};',r'\end{tikzpicture}']
 return '\n'.join(s)
def write(folder,figures,corr):
 p=folder/'figures';p.mkdir(exist_ok=True)
 (p/'figures.py').write_text('# Figures originales du chantier 6e, palette commune.\nFIGURES = '+repr(figures)+'\n',encoding='utf-8')
 (p/'correspondance.json').write_text(json.dumps(corr,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
for code in (129,130,131,133,150,151):
 folder=next(ROOT.glob(str(code)+'_*'));meta=json.loads((folder/'source_en_ligne/meta.json').read_text(encoding='utf-8'))
 figs={};corr={'cours':{},'fiches':{},'exercices':{}}
 def add(genre,oid,pos,name,alt):corr[genre].setdefault(str(oid),{})[str(pos)]={'fichier':name+'.png','alt':alt}
 cid=meta['cours'][0]['id']
 if code==129:
  name='unite_dixieme_centieme';s=[r'\begin{tikzpicture}[x=0.37cm,y=0.37cm]']
  for offset,rows,title in [(0,1,'Un dixième'),(14,0,'Un centième')]:
   if rows:s.append(rf'\fill[otNavy!55] ({offset},9) rectangle ({offset+10},10);')
   else:s.append(rf'\fill[otGreenDark!65] ({offset},9) rectangle ({offset+1},10);')
   s+=[rf'\draw[step=0.37cm,otRule] ({offset},0) grid ({offset+10},10);',rf'\draw[otNavy] ({offset},0) rectangle ({offset+10},10);',rf'\node[below=9pt,text=otInk] at ({offset+5},0) {{{title}}};']
  s.append(r'\end{tikzpicture}');figs[name]='\n'.join(s)
  add('cours',cid,1,name,'Deux unités quadrillées en cent parts : un dixième représente dix cases et un centième une case.')
 if code==130:
  for l in range(3):
   origin=F([2,37,403][l],[1,10,100][l]);pas=F(1,[10,100,1000][l]);name=f'graduation_{l+1}';figs[name]=axis(origin,pas)
   eid=meta['exercices'][l*7]['id'];add('exercices',eid,1,name,'Graduation régulière en dix intervalles ; A est au troisième intervalle et B au huitième.')
  add('cours',cid,1,'graduation_1','Portion de demi-droite graduée de 2 à 3 en dixièmes, points A et B au troisième et au huitième intervalle.')
  figs['arrondi_7364']=r'''\begin{tikzpicture}[x=0.65cm,y=1cm]
\draw[otMuted,-{Stealth}] (-0.2,0)--(10.5,0);
\foreach \i in {0,...,10} {\draw[otMuted] (\i,-0.07)--(\i,0.07);}
\node[below=8pt,text=otMuted] at (0,0) {$7{,}36$};
\node[below=8pt,text=otMuted] at (10,0) {$7{,}37$};
\fill[otGreenDark] (4,0) circle (1.8pt);
\node[above=9pt,text=otGreenDark] at (4,0) {$7{,}364$};
\draw[otOrange,dashed] (5,-0.12)--(5,0.42);
\node[above=20pt,text=otMuted] at (5,0) {Milieu : $7{,}365$};
\end{tikzpicture}'''
  add('cours',cid,2,'arrondi_7364','Le nombre 7,364 est situé entre 7,36 et 7,37 et à gauche de leur milieu 7,365.')
 if code==131:
  figs['produit_23_14']=r'''\begin{tikzpicture}[x=2cm,y=2cm]
\fill[otSky] (0,0) rectangle (2,1);
\fill[otNavy!18] (2,0) rectangle (2.3,1);
\fill[otGreen!22] (0,1) rectangle (2,1.4);
\fill[otOrange!35] (2,1) rectangle (2.3,1.4);
\draw[otNavy] (0,0) rectangle (2.3,1.4);
\draw[otRule] (2,0)--(2,1.4) (0,1)--(2.3,1);
\node[text=otInk] at (1,0.5) {$2$};
\node[text=otInk] at (1,1.2) {$0{,}8$};
\node[anchor=west,text=otInk] at (2.65,0.5) {$0{,}3$};
\draw[otMuted] (2.33,0.5)--(2.6,0.5);
\node[anchor=west,text=otInk] at (2.65,1.2) {$0{,}12$};
\draw[otMuted] (2.33,1.2)--(2.6,1.2);
\node[below=8pt,text=otMuted] at (1,0) {$2\ \mathrm{cm}$};
\node[below=8pt,text=otMuted] at (2.15,0) {$0{,}3$};
\node[left=8pt,text=otMuted] at (0,0.5) {$1\ \mathrm{cm}$};
\node[left=8pt,text=otMuted] at (0,1.2) {$0{,}4$};
\end{tikzpicture}'''
  add('cours',cid,1,'produit_23_14','Rectangle de 2,3 cm sur 1,4 cm décomposé en quatre aires de 2 ; 0,8 ; 0,3 et 0,12 cm carré.')
 if code==151:
  for l in range(3):
   k=2+l;small=12+3*l;name=f'parts_egales_{k}';figs[name]=bars(k,small*(k+1));eid=meta['exercices'][l*7+1]['id'];add('exercices',eid,1,name,f'Mia possède une part et Léo {k} parts égales, soit un total de {small*(k+1)} objets.')
  figs['parts_cours_48']=bars(3,48)
  add('cours',cid,1,'parts_cours_48','Schéma en barres : Mia possède une part et Léo trois parts égales ; le total des quatre parts est 48.')
  s=[r'\begin{tikzpicture}[x=0.7cm,y=0.7cm]']
  for y,n in [(4,1),(2,2),(0,3)]:
   for i in range(n):s+=[rf'\draw[otNavy,line width=1.2pt] ({i},{y})--({i+1},{y}) ({i},{y+1})--({i+1},{y+1});']
   for i in range(n+1):s.append(rf'\draw[otNavy,line width=1.2pt] ({i},{y})--({i},{y+1});')
   label='carré' if n==1 else 'carrés'
   s.append(rf'\node[anchor=west,text=otInk] at (4,{y+0.5}) {{{n} {label} : {1+3*n} allumettes}};')
  s.append(r'\end{tikzpicture}');figs['carres_accoles']='\n'.join(s)
  add('cours',cid,2,'carres_accoles','Un, deux puis trois carrés accolés utilisent quatre, sept puis dix allumettes, car un côté est partagé.')
  for l in range(3):add('exercices',meta['exercices'][l*7+4]['id'],2,'carres_accoles','Les trois premiers motifs de carrés accolés : quatre, sept et dix allumettes.')
 write(folder,figs,corr)
 print(code,len(figs),'figures',flush=True)
