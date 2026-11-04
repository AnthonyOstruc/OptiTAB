# -*- coding: utf-8 -*-
"""Figures TikZ originales, palette et polices communes du chantier."""
FIGURES = {
'cours_modele': r"""\begin{tikzpicture}
\foreach \x in {0,1,2} {\draw[geoTrait] (\x,0) rectangle +(1,1);}
\node[anchor=south] at (1.5,1.25) {3 carrés accolés};
\node[anchor=north,text=otGreenDark] at (1.5,-.25) {$4+3+3=10$ allumettes};
\end{tikzpicture}""",
}


# Figures de la révision pédagogique du 30 octobre 2026.
FIGURES.update({
'bordure_enonce': r"""\begin{tikzpicture}
\fill[otSky] (0,0) rectangle (3,3);
\fill[white] (.6,.6) rectangle (2.4,2.4);
\draw[otNavy!55,line width=.45pt] (0.0,0)--(0.0,3) (0,0.0)--(3,0.0);
\draw[otNavy!55,line width=.45pt] (0.6,0)--(0.6,3) (0,0.6)--(3,0.6);
\draw[otNavy!55,line width=.45pt] (1.2,0)--(1.2,3) (0,1.2)--(3,1.2);
\draw[otNavy!55,line width=.45pt] (1.8,0)--(1.8,3) (0,1.8)--(3,1.8);
\draw[otNavy!55,line width=.45pt] (2.4,0)--(2.4,3) (0,2.4)--(3,2.4);
\draw[otNavy!55,line width=.45pt] (3.0,0)--(3.0,3) (0,3.0)--(3,3.0);
\draw[geoTrait] (0,0) rectangle (3,3);
\draw[geoTrait] (.6,.6) rectangle (2.4,2.4);
\node[anchor=south] at (1.5,3.25) {Rang $3$};
\node[anchor=north,text=otMuted] at (1.5,-.25) {Le carré central est exclu};
\end{tikzpicture}""",
'bordure_corrige': r"""\begin{tikzpicture}
\fill[otSky] (0,0) rectangle (3,3);
\fill[white] (.6,.6) rectangle (2.4,2.4);
\fill[otGreen!25] (0,0) rectangle (3,.6);
\fill[otGreen!25] (0,2.4) rectangle (3,3);
\fill[otNavy!15] (0,.6) rectangle (.6,2.4);
\fill[otNavy!15] (2.4,.6) rectangle (3,2.4);
\draw[otNavy!55,line width=.45pt] (0.0,0)--(0.0,3) (0,0.0)--(3,0.0);
\draw[otNavy!55,line width=.45pt] (0.6,0)--(0.6,3) (0,0.6)--(3,0.6);
\draw[otNavy!55,line width=.45pt] (1.2,0)--(1.2,3) (0,1.2)--(3,1.2);
\draw[otNavy!55,line width=.45pt] (1.8,0)--(1.8,3) (0,1.8)--(3,1.8);
\draw[otNavy!55,line width=.45pt] (2.4,0)--(2.4,3) (0,2.4)--(3,2.4);
\draw[otNavy!55,line width=.45pt] (3.0,0)--(3.0,3) (0,3.0)--(3,3.0);
\draw[geoTrait] (0,0) rectangle (3,3);
\draw[geoTrait] (.6,.6) rectangle (2.4,2.4);
\node[anchor=south] at (1.5,3.25) {Rang $3$};
\node[anchor=west,text=otGreenDark,align=left] at (3.5,2.6) {Haut : $5$\\Bas : $5$};
\node[anchor=west,text=otNavy,align=left] at (3.5,1.2) {Gauche : $3$\\Droite : $3$};
\node[anchor=north,text=otGreenDark] at (1.5,-.25) {$5+5+3+3=16$ carreaux};
\end{tikzpicture}""",
})
