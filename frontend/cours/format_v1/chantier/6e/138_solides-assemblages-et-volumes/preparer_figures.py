# -*- coding: utf-8 -*-
"""Figures de travail et corrigées au style TikZ commun ; aucune tolérance."""
from pathlib import Path
import json
R=Path(__file__).resolve().parent.parent
F={}
def put(n,b):F[n]=r'\begin{tikzpicture}[line cap=round,line join=round]'+ '\n'+b+'\n'+r'\end{tikzpicture}'
cube=r'''\fill[otNavy!6] (0,0) rectangle (2,2);
\fill[otNavy!12] (2,0)--(2.8,.7)--(2.8,2.7)--(2,2)--cycle;
\fill[otNavy!3] (0,2)--(.8,2.7)--(2.8,2.7)--(2,2)--cycle;
\draw[geoTrait] (0,0)--(2,0)--(2,2)--(0,2)--cycle;
\draw[geoTrait] (0,2)--(.8,2.7)--(2.8,2.7)--(2.8,.7)--(2,0);
\draw[geoTrait] (2,2)--(2.8,2.7);
\draw[otNavy,dashed] (0,0)--(.8,.7)--(.8,2.7) (.8,.7)--(2.8,.7);'''
put('cube',cube);put('cube_corrige',cube.replace('otNavy,dashed','otGreenDark,dashed'))
put('vues',r'''\node at (1.1,2.6) {Plan des hauteurs};
\draw[geoTrait] (0,0) rectangle (2.2,2.2);
\draw[geoTrait] (1.1,0)--(1.1,2.2) (0,1.1)--(2.2,1.1);
\node at (.55,1.65) {1}; \node at (1.65,1.65) {2};
\node at (.55,.55) {3}; \node at (1.65,.55) {1};
\node[anchor=north] at (1.1,-.25) {Avant : direction du regard};''')
put('vues_corrige',r'''\node at (1,3.55) {Vue depuis l'avant};
\fill[otGreen!12] (0,0)--(2,0)--(2,2)--(1,2)--(1,3)--(0,3)--cycle;
\draw[otGreenDark,line width=.85pt] (0,0)--(2,0)--(2,2)--(1,2)--(1,3)--(0,3)--cycle;
\draw[otGreenDark] (0,1)--(2,1) (0,2)--(1,2) (1,0)--(1,2);
\node[anchor=east] at (-.25,1.5) {3};\node[anchor=west] at (2.25,1) {2};''')
def net(cells,labels,green=False):
    out=[];co='otGreenDark' if green else 'otNavy'
    for (x,y),label in zip(cells,labels):
        out.append(fr'\fill[{co}!6] ({x},{y}) rectangle ({x+1},{y+1});\draw[{co},line width=.75pt] ({x},{y}) rectangle ({x+1},{y+1});\node[text={co}] at ({x+.5},{y+.5}) {{{label}}};')
    return '\n'.join(out)
cross=[(0,0),(1,0),(2,0),(3,0),(1,1),(1,-1)]
for suffix,g in [('',False),('_corrige',True)]:
    put('patron_croix'+suffix,net(cross,'ABCDEF',g))
    put('boite_ouverte'+suffix,net([(1,1),(0,1),(2,1),(1,0),(1,2)],['Base','','','',''],g))
    put('patron_faux'+suffix,net([(x,y) for y in range(2) for x in range(3)],['']*6,g)+(r'\node[anchor=north,text=otGreenDark] at (1.5,-.3) {Quatre carrés à un sommet intérieur};' if g else ''))
    body=net(cross,'ABCDEF',g)+r'\begin{scope}[xshift=5cm]'+net([(x,y) for y in range(2) for x in range(3)],['']*6,False)+r'\end{scope}'
    body+=r'\node[anchor=north] at (2,-1.3) {Croix};\node[anchor=north] at (6.5,-.3) {Rectangle};'
    put('deux_patrons'+suffix,body)
put('patron_pave',r'''\draw[geoTrait] (0,0) rectangle (5.2,1);
\draw[geoTrait] (1.6,0)--(1.6,1) (2.6,0)--(2.6,1) (4.2,0)--(4.2,1);
\fill[otNavy!5] (1.6,1) rectangle (2.6,2.6);
\fill[otNavy!5] (1.6,-1.6) rectangle (2.6,0);
\draw[geoTrait] (1.6,1) rectangle (2.6,2.6) (1.6,-1.6) rectangle (2.6,0);
\node at (.8,.5) {$5\times2$};\node at (2.1,.5) {$3\times2$};
\node at (3.4,.5) {$5\times2$};\node at (4.7,.5) {$3\times2$};
\node at (2.1,1.8) {$3\times5$};\node at (2.1,-.8) {$3\times5$};
\node[anchor=north] at (2.6,-1.9) {Dimensions des faces en cm ; dessin non à l'échelle};''')
# Cadran : chiffres espacés des traits, aiguille des heures à 3 + 25/60.
clock=r'\draw[geoTrait] (0,0) circle (1.6);'+'\n'
for i in range(1,13):clock+=fr'\node at ({90-30*i}:1.32) {{{i}}};'+'\n'
clock+=r'''\draw[otNavy,line width=1.25pt] (0,0)--(-60:1.05);
\draw[otGreenDark,line width=1.8pt] (0,0)--(-12.5:.72);
\fill[otInk] (0,0) circle (2pt);
\node[anchor=north] at (0,-1.9) {15 h 25};'''
put('horloge_1525',clock)
for suffix,corr in [('',False),('_corrige',True)]:
    txt=r'''\draw[otNavy,-{Latex},line width=.8pt] (0,0)--(6,0);
\foreach \x in {0.3,3,5.7} {\draw[otNavy] (\x,-.1)--(\x,.1);}
\node[anchor=north] at (.3,-.2) {23 h 35};\node[anchor=north] at (3,-.2) {Minuit};\node[anchor=north] at (5.7,-.2) {0 h 20};'''
    if corr:txt+=r'\node[text=otGreenDark] at (1.65,.4) {25 min};\node[text=otGreenDark] at (4.35,.4) {20 min};'
    put('minuit'+suffix,txt)
def bars(name,labels,values,blank=False):
    b=r'\draw[otNavy,-{Latex}] (0,0)--(0,3.4);\draw[otNavy,-{Latex}] (0,0)--(5,0);'+'\n'
    vmax=max(values);unit=.35 if vmax<=8 else .2
    for v in range(0,vmax+1,2):b+=fr'\draw[otNavy!25] (0,{v*unit})--(4.7,{v*unit});\node[anchor=east] at (-.15,{v*unit}) {{{v}}};'+'\n'
    for k,(label,v) in enumerate(zip(labels,values)):
        x=.8+1.5*k
        if not blank:b+=fr'\fill[otGreen!22] ({x-.3},0) rectangle ({x+.3},{v*unit});\draw[otGreenDark] ({x-.3},0) rectangle ({x+.3},{v*unit});'+'\n'
        b+=fr'\node[anchor=north] at ({x},-.25) {{{label}}};'+'\n'
    b+=r'\node[anchor=south west] at (0,3.5) {Effectif};'
    put(name,b)
bars('emprunts_vide',['Lun.','Mar.','Mer.'],[4,6,3],True)
bars('emprunts_corrige',['Lun.','Mar.','Mer.'],[4,6,3])
bars('velos_vide',['Lun.','Mar.','Mer.'],[5,8,6],True)
bars('velos_corrige',['Lun.','Mar.','Mer.'],[5,8,6])
put('temperatures',r'''\draw[otNavy,-{Latex}] (0,0)--(5.2,0);\draw[otNavy,-{Latex}] (0,0)--(0,4);
\foreach \y/\v in {0/0,1/4,2/8,3/12,4/16} {\draw[otNavy!18] (0,\y)--(4.7,\y);\node[anchor=east] at (-.17,\y) {\v};}
\foreach \x/\h in {.5/8,1.8/10,3.1/12,4.4/14} {\node[anchor=north] at (\x,-.22) {\h};}
\draw[otGreenDark,line width=.9pt] (.5,2)--(1.8,3)--(3.1,4)--(4.4,3.5);
\foreach \p in {(.5,2),(1.8,3),(3.1,4),(4.4,3.5)} {\fill[otGreenDark] \p circle (2pt);}
\node[anchor=south west] at (0,4.35) {Température (en degrés Celsius)};
\node[anchor=north] at (2.4,-.7) {Heure};''')
def wheel(name,segments,labels,corr=False):
    b='';angles=[0];s=0
    for a in segments:s+=a;angles.append(s)
    for k,(a,z,label) in enumerate(zip(angles,angles[1:],labels)):
        col=('otNavy!6','otGreen!12','otOrange!12','otNavy!12')[k%4]
        b+=fr'\fill[{col}] (0,0)--({a}:1.5) arc ({a}:{z}:1.5)--cycle;'+'\n'
        b+=fr'\draw[otNavy] (0,0)--({a}:1.5);\node at ({(a+z)/2}:.95) {{{label}}};'+'\n'
    b+=r'\draw[geoTrait] (0,0) circle (1.5);'
    if corr:b+=r'\node[anchor=north,text=otGreenDark] at (0,-1.85) {A : moitié ; autres lettres : un quart};'
    put(name,b)
wheel('roue_reguliere',[90]*4,['A','A','B','C'])
wheel('roue_reguliere_corrige',[90]*4,['A','A','B','C'],True)
wheel('roue_inegale',[180,90,90],['A','B','C'])
wheel('roue_inegale_corrige',[180,90,90],['A','B','C'],True)
put('transports',r'''\fill[otNavy!12] (0,0)--(0:1.5) arc (0:180:1.5)--cycle;
\fill[otGreen!18] (0,0)--(180:1.5) arc (180:270:1.5)--cycle;
\fill[otOrange!14] (0,0)--(270:1.5) arc (270:360:1.5)--cycle;
\draw[geoTrait] (0,0) circle (1.5);\draw[geoTrait] (-1.5,0)--(1.5,0) (0,0)--(0,-1.5);
\node at (0,.8) {Bus};\node at (-.65,-.65) {Vélo};\node at (.65,-.65) {Marche};''')
for name,good in [('deux_lancers',()),('deux_lancers_corrige',('PF','FP')),('au_moins_un',('PP','PF','FP'))]:
    b=r'\draw[otNavy] (0,0) rectangle (3.6,2.4);\draw[otNavy] (1.2,0)--(1.2,2.4) (2.4,0)--(2.4,2.4) (0,.8)--(3.6,.8) (0,1.6)--(3.6,1.6);'+'\n'
    for (x,y),v in [((1.8,2),'P'),((3,2),'F'),((.6,1.2),'P'),((.6,.4),'F'),((1.8,1.2),'PP'),((3,1.2),'PF'),((1.8,.4),'FP'),((3,.4),'FF')]:
        if v in good:b+=fr'\fill[otGreen!18] ({x-.5},{y-.3}) rectangle ({x+.5},{y+.3});'+'\n'
        b+=fr'\node at ({x},{y}) {{{v}}};'+'\n'
    b+=r'\node[anchor=north] at (1.8,-.3) {Lignes : premier lancer ; colonnes : second};'
    put(name,b)
# Quadrillages : coordonnées de cases utilisées comme points repérés.
def grid(name,points=(),size=(5,5),obstacle=False):
    w,h=size;b=fr'\draw[step=.65,otNavy!18] (0,0) grid ({(w-1)*.65},{(h-1)*.65});'+'\n'
    for x in range(w):b+=fr'\node[anchor=north] at ({x*.65},-.18) {{{chr(65+x)}}};'+'\n'
    for y in range(h):b+=fr'\node[anchor=east] at (-.2,{y*.65}) {{{y+1}}};'+'\n'
    if obstacle:b+=r'\fill[otOrange!30] (.47,-.12) rectangle (.83,.12);\node[anchor=south,text=otOrange] at (.65,.2) {Interdit};'
    b+=r'\fill[otNavy] (0,0) circle (2pt);'
    if points:
        coords='--'.join(f'({x*.65},{y*.65})' for x,y in points)
        b+=fr'\draw[otGreenDark,line width=1.4pt,-{{Latex}}] {coords};'+'\n'
    put(name,b)
for base,pts,size,ob in [
('chemin_L',[(0,0),(3,0),(3,2)],(5,5),False),
('carre',[(0,0),(3,0),(3,3),(0,3),(0,0)],(5,5),False),
('escalier',[(0,0),(1,0),(1,1),(2,1),(2,2),(3,2),(3,3)],(5,5),False),
('rectangle',[(0,0),(4,0),(4,2),(0,2),(0,0)],(6,4),False),
('detour',[(0,0),(0,1),(3,1),(3,0)],(5,4),True),
('bug',[(0,0),(2,0),(2,2)],(5,5),False)]:
    grid(base+'_vide',(),size,ob);grid('bug_corrige' if base=='bug' else base,pts,size,ob)
grid('carre_ouvert',[(0,0),(3,0),(3,3),(0,3)])

for n in (138,139,146,147,148,149,152):
    d=next(R.glob(f'{n}_*'));cor=json.loads((d/'figures/correspondance.json').read_text(encoding='utf8'))
    used={v['fichier'][:-4] for maps in cor.values() for positions in maps.values() for v in positions.values()}
    assert used<=F.keys(),used-F.keys()
    (d/'figures/figures.py').write_text('# -*- coding: utf-8 -*-\n"""Figures livre : aucune tolérance de chevauchement."""\nFIGURES = '+repr({k:F[k] for k in sorted(used)})+'\n',encoding='utf8')
