"""Figures nécessaires aux notions attribuées, géométrie et données cohérentes."""
from pathlib import Path
import json, math
BASE=Path(__file__).resolve().parent.parent
IDS=(132,134,135,136,137,284,285)
D={n:next(BASE.glob(str(n)+'_*')) for n in IDS}
FIG={n:{} for n in IDS}; MAP={n:{'cours':{},'fiches':{},'exercices':{}} for n in IDS}
def fig(n,name,tex): FIG[n][name]=tex
def link(n,genre,eid,pos,name,alt):
    MAP[n][genre].setdefault(str(eid),{})[str(pos)]={'fichier':name+'.png','alt':alt}
def image(n,name,tex,refs,alt):
    fig(n,name,tex)
    for genre,eid,pos in refs: link(n,genre,eid,pos,name,alt)
image(132,'trois_quarts',r'''\begin{tikzpicture}[x=1.35cm,y=0.7cm]
\foreach \y in {0,1.1,2.2}{
\fill[otGreen!22] (0,\y) rectangle (0.75,\y+0.6);
\draw[geoTrait] (0,\y) rectangle (3,\y+0.6);
\foreach \x in {0.75,1.5,2.25}{\draw[geoAide] (\x,\y)--(\x,\y+0.6);}
\node[geoLabel,anchor=west] at (3.2,\y+0.3) {1 m};}
\node[geoLabel] at (1.5,-0.7) {3 morceaux de $\frac14$ m : $\frac34$ m};
\end{tikzpicture}''',[('cours',135,1)],'Trois rubans de un mètre partagés en quarts ; un quart de chaque ruban forme trois quarts de mètre.')
image(132,'droite_quarts',r'''\begin{tikzpicture}[x=0.8cm,y=1cm]
\draw[geoVecteur] (0,0)--(8.6,0);
\foreach \x in {0,...,8}{\draw[geoTrait] (\x,-0.08)--(\x,0.08);}
\foreach \x/\lab in {0/0,4/1,8/2}{\node[geoLabel,below=7pt] at (\x,0) {$\lab$};}
\fill[otGreenDark] (3,0) circle (2pt) (7,0) circle (2pt);
\node[geoLabel,text=otGreenDark,above=12pt] at (3,0) {$A\!\left(\frac34\right)$};
\node[geoLabel,text=otGreenDark,above=12pt] at (7,0) {$B\!\left(\frac74\right)$};
\end{tikzpicture}''',[('cours',135,2),('exercices',3273,1)],'Demi-droite graduée en quarts, avec A à trois quarts et B à sept quarts, une unité les sépare.')
image(132,'guide_ane',r'''\begin{tikzpicture}[x=1cm,y=1cm]
\foreach \k in {0,...,7}{\draw[geoAide] (-0.3,0.32*\k)--(3.5,0.32*\k);}
\draw[geoReponse] (0,0)--(3,2.24);
\foreach \k in {0,...,7}{\fill[otGreenDark] (3*\k/7,0.32*\k) circle (1.7pt);}
\node[geoLabel,below=8pt] at (0,0) {$A$};
\node[geoLabel,above=8pt] at (3,2.24) {$B$};
\node[geoLabel,anchor=west] at (3.9,1.12) {7 intervalles égaux};
\node[geoLabel] at (1.5,-0.85) {$AB=3$ cm, chaque part mesure $\frac37$ cm};
\end{tikzpicture}''',[('cours',135,3),('exercices',3280,1)],'Guide-âne avec huit parallèles et sept intervalles égaux ; le segment de trois centimètres est partagé en sept.')
image(134,'carte',r'''\begin{tikzpicture}[x=0.7cm,y=1cm]
\draw[geoTrait] (0,0)--(6.5,0);
\draw[geoTrait] (0,-0.12)--(0,0.12) (6.5,-0.12)--(6.5,0.12);
\node[geoLabel,above=9pt] at (3.25,0) {6,5 cm sur la carte};
\node[geoLabel,below=10pt] at (3.25,0) {325 m dans la réalité};
\node[geoLabel] at (3.25,-1.1) {1 cm représente 50 m};
\end{tikzpicture}''',[('cours',136,1)],'Correspondance des longueurs : six virgule cinq centimètres sur la carte pour trois cent vingt-cinq mètres réels.')
image(135,'rectangle',r'''\begin{tikzpicture}[x=1cm,y=1cm]
\draw[geoTrait] (0,0) rectangle (4,1.6);
\node[geoLabel,below=8pt] at (2,0) {2 m};
\node[geoLabel,right=9pt] at (4,0.8) {80 cm};
\end{tikzpicture}''',[('cours',137,1)],'Rectangle dont la longueur est deux mètres et la largeur quatre-vingts centimètres ; proportions respectées.')
circle=lambda radius,diam:r'''\begin{tikzpicture}[x=1cm,y=1cm]
\draw[geoTrait] (0,0) circle (1.5);
\draw[geoAide] (-1.5,0)--(1.5,0);
\fill[otNavy] (0,0) circle (1.5pt);
\node[geoLabel,below=7pt] at (0,0) {$O$};
\draw[geoReponse] (0,0)--(0.9,1.2);
\node[geoLabel] at (0,2.1) {rayon : '''+radius+r'''};
\node[geoLabel] at (0,-2.1) {diamètre : '''+diam+r'''};
\end{tikzpicture}'''
image(135,'cercle_dix',circle('5 cm','10 cm'),[('cours',137,2)],'Cercle de rayon cinq centimètres ; diamètre de dix centimètres, rayon mis en évidence.')
composite=r'''\begin{tikzpicture}[x=0.65cm,y=0.65cm]
\fill[otSky] (0,0)--(6,0) arc[start angle=-90,end angle=90,radius=2]--(0,4)--cycle;
\draw[geoTrait] (0,0)--(6,0) arc[start angle=-90,end angle=90,radius=2]--(0,4)--cycle;
\draw[geoAide] (6,0)--(6,4);
\node[geoLabel,below=9pt] at (3,0) {6 cm};
\node[geoLabel,left=9pt] at (0,2) {4 cm};
\node[geoLabel] at (3,-1.3) {diamètre commun intérieur : 4 cm};
\end{tikzpicture}'''
image(135,'demi_disque',composite,[('cours',137,3),('exercices',3390,1)],'Rectangle six centimètres sur quatre prolongé par un demi-disque de diamètre quatre ; frontière commune en pointillé.')

# Pentagone cyclique dont les cinq côtés mesurent exactement 4, 5, 6, 4 et 7 unités.
sides=[4,5,6,4,7];lo=3.50000001;hi=20
for _ in range(90):
    mid=(lo+hi)/2
    if sum(2*math.asin(s/(2*mid)) for s in sides)>2*math.pi: lo=mid
    else: hi=mid
R=(lo+hi)/2;a=-math.pi/2;pts=[]
for s in sides:
    pts.append((R*math.cos(a),R*math.sin(a)));a+=2*math.asin(s/(2*R))
tex=[r'\begin{tikzpicture}[x=0.43cm,y=0.43cm]']
tex.append(r'\draw[geoTrait] '+'--'.join(f'({x:.6f},{y:.6f})' for x,y in pts)+'--cycle;')
for i,s in enumerate(sides):
    x,y=pts[i];u,v=pts[(i+1)%5];dx=u-x;dy=v-y
    lx=(x+u)/2+dy/s*.9;ly=(y+v)/2-dx/s*.9
    tex.append(rf'\node[geoLabel] at ({lx:.6f},{ly:.6f}) {{{s} cm}};')
tex.append(r'\end{tikzpicture}')
image(136,'pentagone','\n'.join(tex),[('cours',144,1),('exercices','nouveau-1',1)],'Pentagone de côtés successifs quatre, cinq, six, quatre et sept centimètres ; périmètre vingt-six centimètres.')
image(136,'cercle_six',circle('3 cm','6 cm'),[('cours',144,2)],'Cercle de rayon trois centimètres et de diamètre six centimètres ; le centre est nommé O.')
notch=r'''\begin{tikzpicture}[x=0.65cm,y=0.65cm]
\draw[geoTrait] (0,0)--(8,0)--(8,5)--(5,5)--(5,4)--(3,4)--(3,5)--(0,5)--cycle;
\draw[geoAide] (3,5)--(5,5);
\node[geoLabel,below=9pt] at (4,0) {8 cm};
\node[geoLabel,left=9pt] at (0,2.5) {5 cm};
\node[geoLabel,above=10pt] at (4,5) {2 cm};
\draw[geoAide] (5.2,4.5)--(6.1,4.1);
\node[geoLabel,anchor=west] at (6.2,4.1) {1 cm};
\end{tikzpicture}'''
image(136,'encoche',notch,[('cours',144,3),('exercices','nouveau-5',1)],'Rectangle huit sur cinq avec une encoche centrale de deux centimètres de largeur et un centimètre de profondeur.')
image(137,'recollement',r'''\begin{tikzpicture}[x=0.8cm,y=0.8cm]
\fill[otSky] (0,0) rectangle (2,2);\draw[geoTrait] (0,0) rectangle (2,2);
\draw[geoAide] (1,0)--(1,2) (0,1)--(2,1);
\fill[otGreen!20] (3.5,0.5) rectangle (7.5,1.5);\draw[geoTrait] (3.5,0.5) rectangle (7.5,1.5);
\foreach \x in {4.5,5.5,6.5}{\draw[geoAide] (\x,0.5)--(\x,1.5);}
\node[geoLabel] at (1,-0.6) {4 unités d’aire};
\node[geoLabel] at (5.5,-0.6) {4 unités d’aire};
\end{tikzpicture}''',[('cours',145,1)],'Quatre carrés unités assemblés en carré ou en bande ; même aire totale, contours différents.')
image(137,'unites_aire',r'''\begin{tikzpicture}[x=0.33cm,y=0.33cm]
\fill[otSky] (0,0) rectangle (10,10);\draw[geoTrait] (0,0) rectangle (10,10);
\draw[otRule,step=1] (0,0) grid (10,10);
\fill[otGreen!30] (0,0) rectangle (1,1);\draw[geoReponse] (0,0) rectangle (1,1);
\node[geoLabel,below=11pt] at (5,0) {1 dm = 10 cm};
\node[geoLabel,anchor=west] at (12,7) {10 lignes de 10 carrés};
\node[geoLabel,anchor=west] at (12,4) {$1$ dm$^2=100$ cm$^2$};
\node[geoLabel,anchor=west] at (12,1) {un petit carré : $1$ cm$^2$};
\end{tikzpicture}''',[('cours',145,2)],'Un carré de un décimètre de côté contient dix lignes de dix carrés de un centimètre de côté, soit cent centimètres carrés.')
L=r'''\begin{tikzpicture}[x=0.6cm,y=0.6cm]
\fill[otSky] (0,0)--(8,0)--(8,3)--(5,3)--(5,5)--(0,5)--cycle;
\draw[geoTrait] (0,0)--(8,0)--(8,3)--(5,3)--(5,5)--(0,5)--cycle;
\draw[geoAide] (5,5)--(8,5)--(8,3);
\draw[geoAide] (0,3)--(5,3);
\node[geoLabel,below=9pt] at (4,0) {8 cm};
\node[geoLabel,left=9pt] at (0,2.5) {5 cm};
\node[geoLabel,above=10pt] at (6.5,5) {3 cm};
\node[geoLabel,right=10pt] at (8,4) {2 cm};
\end{tikzpicture}'''
image(137,'surface_L',L,[('cours',145,3),('exercices',3406,1)],'Grand rectangle huit sur cinq auquel on retire le coin supérieur droit trois sur deux ; découpage possible indiqué en pointillé.')
image(137,'demi_carreaux',r'''\begin{tikzpicture}[x=0.7cm,y=0.7cm]
\fill[otSky] (0,2) rectangle (4,4);
\foreach \y in {0,1}{\foreach \x in {0,1,2}{\fill[otGreen!25] (\x,\y)--(\x+1,\y)--(\x,\y+1)--cycle;\draw[geoTrait] (\x,\y)--(\x+1,\y)--(\x,\y+1)--cycle;}}
\draw[otRule,step=1] (0,0) grid (4,4);
\draw[geoTrait] (0,2) rectangle (4,4);
\node[geoLabel,anchor=west] at (4.7,3) {8 carreaux entiers};
\node[geoLabel,anchor=west] at (4.7,1) {6 demi-carreaux};
\node[geoLabel] at (2,-0.7) {un carreau entier : $1$ cm$^2$};
\end{tikzpicture}''',[('exercices',3399,1)],'Huit carreaux entiers bleus et six demi-carreaux verts ; chaque carreau entier représente un centimètre carré.')

image(284,'fractions_egales',r'''\begin{tikzpicture}[x=0.48cm,y=1cm]
\fill[otNavy!18] (0,1.2) rectangle (8,1.7);
\fill[otGreen!20] (0,0) rectangle (8,0.5);
\draw[geoTrait] (0,1.2) rectangle (12,1.7);
\foreach \x in {4,8}{\draw[geoAide] (\x,1.2)--(\x,1.7);}
\draw[geoTrait] (0,0) rectangle (12,0.5);
\foreach \x in {1,...,11}{\draw[geoAide] (\x,0)--(\x,0.5);}
\node[geoLabel,anchor=west] at (13,1.45) {$\frac23$};
\node[geoLabel,anchor=west] at (13,0.25) {$\frac8{12}$};
\end{tikzpicture}''',[('cours',280,1)],'Deux bandes de même longueur colorées aux deux tiers ou aux huit douzièmes : la partie colorée est identique.')
image(285,'grille_pourcentage',r'''\begin{tikzpicture}[x=0.3cm,y=0.3cm]
\fill[otSky] (0,0) rectangle (10,10);
\fill[otNavy!35] (0,0) rectangle (10,3);
\fill[otNavy!35] (0,3) rectangle (5,4);
\draw[otRule,step=1] (0,0) grid (10,10);
\draw[geoTrait] (0,0) rectangle (10,10);
\node[geoLabel,anchor=west] at (12,7) {35 cases sur 100};
\node[geoLabel,anchor=west] at (12,3) {$\frac{35}{100}=0{,}35=35\,\%$};
\end{tikzpicture}''',[('cours',281,1)],'Grille de cent carrés dont trente-cinq sont colorés ; trente-cinq centièmes correspondent à zéro virgule trente-cinq et trente-cinq pour cent.')
image(285,'trente_pourcent',r'''\begin{tikzpicture}[x=0.58cm,y=1cm]
\fill[otGreen!25] (0,0) rectangle (3,0.5);
\draw[geoTrait] (0,0) rectangle (10,0.5);
\foreach \x in {1,...,9}{\draw[geoAide] (\x,0)--(\x,0.5);}
\node[geoLabel,above=11pt] at (1.5,0.5) {30 \% : 24 membres};
\node[geoLabel,below=11pt] at (5,0) {100 \% : 80 membres};
\end{tikzpicture}''',[('cours',281,2)],'Bande de quatre-vingts membres partagée en dix parties de huit ; trois parties représentent trente pour cent, soit vingt-quatre membres.')
for n,d in D.items():
    fd=d/'figures';fd.mkdir(exist_ok=True)
    (fd/'figures.py').write_text('"""Figures TikZ originales ; textes séparés des traits."""\nFIGURES = '+repr(FIG[n])+'\n',encoding='utf-8')
    (fd/'correspondance.json').write_text(json.dumps(MAP[n],ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(n,len(FIG[n]),'figures')
