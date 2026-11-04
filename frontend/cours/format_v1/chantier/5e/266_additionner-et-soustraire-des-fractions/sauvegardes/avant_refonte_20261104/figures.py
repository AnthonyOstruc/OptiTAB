# -*- coding: utf-8 -*-
"""Figures TikZ originales, palette et polices communes du chantier."""
FIGURES = {
'cours_modele': r"""\begin{tikzpicture}
\fill[otNavy!22] (0,0) rectangle (3,.7);
\fill[otGreen!25] (0,-1.5) rectangle (3.33333,-.8);
\draw[geoTrait] (0,0) rectangle (4,.7);
\draw[geoTrait] (0,-1.5) rectangle (4,-.8);
\foreach \x in {1,2,3} {\draw[otNavy!55] (\x,0)--(\x,.7);}
\foreach \x in {.66667,1.33333,2,2.66667,3.33333} {\draw[otNavy!55] (\x,-1.5)--(\x,-.8);}
\node[anchor=west] at (4.25,.35) {$\frac34$};
\node[anchor=west] at (4.25,-1.15) {$\frac56$};
\node[anchor=south,text=otMuted] at (2,1) {Même unité, partages différents};
\end{tikzpicture}""",
}


# Figures de la révision pédagogique du 30 octobre 2026.
FIGURES.update({
'lecture_bilan': r"""\begin{tikzpicture}
\fill[otNavy!20] (0,0) rectangle (2.25,.65);
\fill[otGreen!25] (2.25,0) rectangle (4.75,.65);
\fill[otOrange!30] (4.75,0) rectangle (5.25,.65);
\draw[geoTrait] (0,0) rectangle (6,.65);
\draw[otNavy!60] (2.25,0)--(2.25,.65) (4.75,0)--(4.75,.65) (5.25,0)--(5.25,.65);
\node[anchor=south,text=otNavy] at (1.125,.85) {Lundi};
\node[anchor=south,text=otGreenDark] at (3.5,.85) {Mardi};
\node[anchor=south east,text=otOrange!80!black] at (5.45,1.5) {Mercredi};
\draw[otOrange!80!black,line width=.5pt] (5,1.45)--(5,.85);
\node[anchor=north] at (1.125,-.15) {90 pages};
\node[anchor=north] at (3.5,-.15) {100 pages};
\node[anchor=north] at (5,-.75) {20 pages};
\node[anchor=south west] at (5.4,1.5) {Reste};
\draw[otMuted,line width=.5pt] (5.7,1.45)--(5.7,.85);
\node[anchor=north west] at (5.32,-.15) {30 pages};
\node[anchor=north,text=otGreenDark] at (3,-1.35) {210 pages lues sur 240 : $\frac78$ du livre};
\end{tikzpicture}""",
})
