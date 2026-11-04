# -*- coding: utf-8 -*-
"""Figures TikZ originales, palette et polices communes du chantier."""
FIGURES = {
'cours_modele': r"""\begin{tikzpicture}
\foreach \x in {0,1,2} {\draw[geoTrait] (\x,0) rectangle +(1,1);}
\node[anchor=south] at (1.5,1.25) {3 carrés accolés};
\node[anchor=north,text=otGreenDark] at (1.5,-.25) {$4+3+3=10$ allumettes};
\end{tikzpicture}""",
}
