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
