# -*- coding: utf-8 -*-
"""Figures TikZ au style des livres ; compiler avec outils/figures_livre.py."""
FIGURES = {
'pave_aretes': r"""\begin{tikzpicture}[line cap=round]
\fill[otNavy!5] (0,0)--(4,0)--(4,2.2)--(0,2.2)--cycle;
\draw[otMuted,dashed] (0,0)--(.9,.8)--(4.9,.8) (.9,.8)--(.9,3);
\draw[geoTrait] (0,0)--(4,0)--(4,2.2)--(0,2.2)--cycle;
\draw[geoTrait] (0,2.2)--(.9,3)--(4.9,3)--(4,2.2);
\draw[geoTrait] (4.9,3)--(4.9,.8)--(4,0);
\node[anchor=north] at (2,-.25) {$L$};
\node[anchor=north west] at (4.6,.1) {$\ell$};
\node[anchor=west] at (5.1,1.8) {$h$};
\end{tikzpicture}""",
'prisme_aretes': r"""\begin{tikzpicture}[line cap=round]
\fill[otNavy!8] (0,0)--(4,0)--(0,2)--cycle;
\draw[otMuted,dashed] (0,0)--(1.3,.9)--(5.3,.9) (1.3,.9)--(1.3,2.9);
\draw[geoTrait] (0,0)--(4,0)--(0,2)--cycle;
\draw[geoTrait] (0,2)--(1.3,2.9)--(5.3,.9)--(4,0);
\draw[otOrange] (0,.2)--(.2,.2)--(.2,0);
\node[anchor=north] at (2,-.2) {$a$};
\node[anchor=east] at (-.2,1) {$b$};
\node[anchor=north west] at (4.85,.25) {$L$};
\end{tikzpicture}""",
'cylindre_rayon': r"""\begin{tikzpicture}[line cap=round]
\fill[otNavy!5] (-1.3,0) rectangle (1.3,3);
\fill[white] (0,3) ellipse (1.3 and .4);
\draw[geoTrait] (0,3) ellipse (1.3 and .4);
\draw[geoTrait] (-1.3,3)--(-1.3,0) (1.3,3)--(1.3,0);
\draw[otMuted,dashed] (-1.3,0) arc[start angle=180,end angle=0,x radius=1.3,y radius=.4];
\draw[geoTrait] (-1.3,0) arc[start angle=180,end angle=360,x radius=1.3,y radius=.4];
\draw[otOrange,line width=.9pt] (0,3)--(1.3,3);
\fill[otNavy] (0,3) circle (1.2pt);
\node[anchor=south] at (.63,3.48) {$r$};
\draw[cote] (1.85,0)--(1.85,3) node[coteTexte,midway] {$h$};
\end{tikzpicture}""",
'patron': r"""\begin{tikzpicture}
\fill[otNavy!5] (0,0) rectangle (4.2,1.7);
\draw[geoTrait] (0,0) rectangle (4.2,1.7);
\draw[geoTrait] (2.1,2.37) circle (.67);
\draw[geoTrait] (2.1,-.67) circle (.67);
\draw[otOrange] (2.1,2.37)--(2.77,2.37);
\node[anchor=south] at (2.4,2.47) {$r$};
\draw[cote] (4.65,0)--(4.65,1.7) node[coteTexte,midway] {$h$};
\draw[cote] (0,-1.8)--(4.2,-1.8) node[coteTexte,midway] {$2\pi r$};
\end{tikzpicture}""",
}
