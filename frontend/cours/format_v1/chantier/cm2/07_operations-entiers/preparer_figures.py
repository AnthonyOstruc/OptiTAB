# -*- coding: utf-8 -*-
from pathlib import Path
import json
BASE=Path(__file__).resolve().parent.parent
DATA={
'07_operations-entiers':{'groupes':r'''
\begin{tikzpicture}[x=1cm,y=1cm]
\node[text=otNavy] at (3.6,1.8) {Quatre cartons de 125 livres};
\foreach \x in {0,1.8,3.6,5.4}{
  \draw[draw=otNavy,fill=otSky,line width=.8pt] (\x,0) rectangle +(1.5,1.1);
  \node[text=otNavy] at (\x+.75,.55) {125};
}
\node[text=otGreenDark] at (3.45,-.65) {$4\times125=500$ livres};
\end{tikzpicture}
'''},
'08_division':{'partage':r'''
\begin{tikzpicture}[x=1cm,y=1cm]
\node[text=otNavy] at (3.3,2.1) {37 jetons : cinq parts de sept};
\foreach \x in {0,1.35,2.7,4.05,5.4}{
 \draw[otRule,fill=otSky] (\x,0) rectangle +(1.1,1.5);
 \foreach \a/\b in {.25/.3,.55/.3,.85/.3,.25/.7,.55/.7,.85/.7,.55/1.1}{
  \fill[otNavy] (\x+\a,\b) circle (.08);
 }
}
\fill[otOrange] (2.95,-.5) circle (.09);
\fill[otOrange] (3.35,-.5) circle (.09);
\node[text=otInk] at (3.3,-1.0) {Deux jetons restent};
\node[text=otGreenDark] at (3.3,-1.55) {$37=5\times7+2$};
\end{tikzpicture}
'''},
'09_calculs-decimaux':{'rangs':r'''
\begin{tikzpicture}[x=1cm,y=1cm]
\node[text=otNavy] at (3.2,2.35) {Additionner dans les mêmes rangs};
\node[text=otMuted] at (.8,1.55) {Unités};
\node[text=otMuted] at (3,1.55) {Dixièmes};
\node[text=otMuted] at (5.4,1.55) {Centièmes};
\foreach \x in {-.1,2.1,4.5}{\draw[otRule,fill=otSky] (\x,-.1) rectangle +(1.8,1.2);}
\node at (.8,.75) {12}; \node at (3,.75) {7}; \node at (5.4,.75) {0};
\node at (.8,.25) {3}; \node at (3,.25) {8}; \node at (5.4,.25) {5};
\node[text=otGreenDark] at (3.1,-.7) {$12{,}70+3{,}85=16{,}55$};
\end{tikzpicture}
'''},
'10_proportionnalite':{'doubler':r'''
\begin{tikzpicture}[x=1cm,y=1cm]
\node[anchor=west,text=otNavy] at (0,1.6) {4 cahiers : 6 euros};
\foreach \x in {0,.6,1.2,1.8}{\draw[otNavy,fill=otSky] (\x,.1) rectangle +(.43,.9);}
\node[anchor=west,text=otNavy] at (0,-.6) {8 cahiers : deux lots identiques};
\foreach \x in {0,.6,1.2,1.8,3,3.6,4.2,4.8}{\draw[otNavy,fill=otSky] (\x,-2) rectangle +(.43,.9);}
\node[text=otGreenDark] at (2.65,-2.7) {Le double de cahiers coûte le double : 12 euros};
\end{tikzpicture}
'''},
'21_regularites':{'motifs':r'''
\begin{tikzpicture}[x=.4cm,y=.4cm]
\foreach \k/\cx in {1/0,2/6,3/14}{
 \foreach \j in {-\k,...,\k}{
  \draw[otNavy,fill=otSky] (\cx+\j,0) rectangle +(1,1);
 }
 \foreach \j in {-\k,...,-1,1,...,\k}{
  \draw[otNavy,fill=otSky] (\cx,\j) rectangle +(1,1);
 }
}
\node[text=otNavy] at (.5,-4.2) {Étape 1};
\node[text=otNavy] at (6.5,-4.2) {Étape 2};
\node[text=otNavy] at (14.5,-4.2) {Étape 3};
\node[text=otGreenDark] at (.5,-5.5) {5};
\node[text=otGreenDark] at (6.5,-5.5) {9};
\node[text=otGreenDark] at (14.5,-5.5) {13};
\end{tikzpicture}
''','quadrillage':r'''
\begin{tikzpicture}[x=.8cm,y=.8cm]
\draw[step=1,otRule,line width=.4pt] (0,0) grid (6,6);
\foreach \x/\lab in {.5/A,1.5/B,2.5/C,3.5/D,4.5/E,5.5/F}{\node[text=otNavy] at (\x,-.5) {\lab};}
\foreach \y/\lab in {.5/1,1.5/2,2.5/3,3.5/4,4.5/5,5.5/6}{\node[text=otNavy] at (-.5,\y) {\lab};}
\draw[otNavy,-{Stealth[length=2mm]},line width=1.1pt] (1.2,1.5)--(1.8,1.5);
\draw[otGreenDark,-{Stealth[length=2mm]},line width=1.1pt] (1.9,1.5)--(3.5,1.5)--(3.5,2.65);
\node[text=otNavy,anchor=west] at (6.4,4.4) {Départ B2};
\node[text=otNavy,anchor=west] at (6.4,3.5) {Regard à droite};
\node[text=otGreenDark,anchor=west] at (6.4,2.3) {Arrivée D3};
\node[text=otMuted,anchor=west] at (6.4,1.4) {2 pas, gauche, 1 pas};
\end{tikzpicture}
'''}
}
ALTS={'groupes':'Quatre cartons égaux de 125 livres représentent 500 livres.', 'partage':'Trente-sept jetons partagés en cinq groupes de sept avec deux jetons restants.', 'rangs':'Addition de 12,70 et 3,85 en alignant unités, dixièmes et centièmes.', 'doubler':'Quatre cahiers coûtent six euros ; deux lots de quatre coûtent douze euros.', 'motifs':'Trois croix de cinq, neuf et treize carreaux gagnent quatre carreaux à chaque étape.', 'quadrillage':'Chemin de B2 à D3 sur un quadrillage repéré, avec orientation initiale vers la droite.'}
# Dérouler explicitement les carreaux : les listes à plusieurs intervalles de
# pgffor ne doivent pas être employées pour les deux branches verticales.
motif=[r'\begin{tikzpicture}[x=.4cm,y=.4cm]']
for k,cx in [(1,0),(2,6),(3,14)]:
    cells={(cx+j,0) for j in range(-k,k+1)}|{(cx,j) for j in range(-k,k+1)}
    assert len(cells)==4*k+1
    for x,y in sorted(cells):motif.append(rf'\draw[otNavy,fill=otSky] ({x},{y}) rectangle +(1,1);')
    motif.append(rf'\node[text=otNavy] at ({cx+.5},-4.2) {{Étape {k}}};')
    motif.append(rf'\node[text=otGreenDark] at ({cx+.5},-5.5) {{{4*k+1}}};')
motif.append(r'\end{tikzpicture}')
DATA['21_regularites']['motifs']='\n'.join(motif)
for n,figs in DATA.items():
    d=BASE/n/'figures';d.mkdir(exist_ok=True)
    (d/'figures.py').write_text('# -*- coding: utf-8 -*-\nFIGURES = '+repr(figs)+'\n',encoding='utf-8')
    course={str(i):{'fichier':f'{name}.png','alt':ALTS[name]} for i,name in enumerate(figs,1)}
    mapping={'cours':{'nouveau':course},'fiches':{'nouvelle':{}},'exercices':{}}
    (d/'correspondance.json').write_text(json.dumps(mapping,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('Six figures TikZ préparées.')
