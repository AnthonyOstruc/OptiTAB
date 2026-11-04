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


# Figures pédagogiques ajoutées lors de la révision du 30 octobre 2026.
FIGURES.update({
'patrons_cube': r"""\begin{tikzpicture}[line cap=round,line join=round]
\draw[otNavy,fill=otNavy!5] (1,0) rectangle (2,1);
\draw[otNavy,fill=otNavy!5] (0,1) rectangle (1,2);
\draw[otNavy,fill=otNavy!5] (1,1) rectangle (2,2);
\draw[otNavy,fill=otNavy!5] (2,1) rectangle (3,2);
\draw[otNavy,fill=otNavy!5] (1,2) rectangle (2,3);
\draw[otNavy,fill=otNavy!5] (1,3) rectangle (2,4);
\draw[otMuted,fill=otRule!30] (4.6,1) rectangle (5.6,2);
\draw[otMuted,fill=otRule!30] (4.6,2) rectangle (5.6,3);
\draw[otMuted,fill=otRule!30] (5.6,1) rectangle (6.6,2);
\draw[otMuted,fill=otRule!30] (5.6,2) rectangle (6.6,3);
\draw[otMuted,fill=otRule!30] (6.6,1) rectangle (7.6,2);
\draw[otMuted,fill=otRule!30] (6.6,2) rectangle (7.6,3);
\node[anchor=north,text=otInk] at (1.5,-0.25) {A};
\node[anchor=north,text=otInk] at (6.1,-0.25) {B};

\end{tikzpicture}""",
'patron_cube_corrige': r"""\begin{tikzpicture}[line cap=round,line join=round]
\draw[otGreenDark,fill=otGreen!12] (1,0) rectangle (2,1);
\draw[otGreenDark,fill=otGreen!12] (0,1) rectangle (1,2);
\draw[otGreenDark,fill=otGreen!12] (1,1) rectangle (2,2);
\draw[otGreenDark,fill=otGreen!12] (2,1) rectangle (3,2);
\draw[otGreenDark,fill=otGreen!12] (1,2) rectangle (2,3);
\draw[otGreenDark,fill=otGreen!12] (1,3) rectangle (2,4);
\draw[otMuted,fill=otRule!30] (4.6,1) rectangle (5.6,2);
\draw[otMuted,fill=otRule!30] (4.6,2) rectangle (5.6,3);
\draw[otMuted,fill=otRule!30] (5.6,1) rectangle (6.6,2);
\draw[otMuted,fill=otRule!30] (5.6,2) rectangle (6.6,3);
\draw[otMuted,fill=otRule!30] (6.6,1) rectangle (7.6,2);
\draw[otMuted,fill=otRule!30] (6.6,2) rectangle (7.6,3);
\node[anchor=north,text=otGreenDark] at (1.5,-0.25) {A};
\node[anchor=north,text=otInk] at (6.1,-0.25) {B};
\node[anchor=center,text=otGreenDark] at (1.5,1.5) {Base};
\draw[otOrange,line width=1.2pt] (5.6,2) circle (.13);
\node[anchor=south,text=otMuted] at (6.1,3.3) {4 carrés au même point};

\end{tikzpicture}""",
'patron_cylindre_mesure': r"""\begin{tikzpicture}[line cap=round,line join=round]
\fill[otNavy!5] (0,0) rectangle (4.18879,1.66667);
\draw[geoTrait] (0,0) rectangle (4.18879,1.66667);
\draw[geoTrait] (2.0944,2.33334) circle (.66667);
\draw[geoTrait] (2.0944,-.66667) circle (.66667);
\draw[otOrange] (2.0944,2.33334)--(2.76107,2.33334);
\draw[cote] (4.8,0)--(4.8,1.66667) node[coteTexte,midway] {$5\,\mathrm{cm}$};
\draw[cote] (0,-1.8)--(4.18879,-1.8) node[coteTexte,midway] {$4\pi\,\mathrm{cm}$};
\node[anchor=south,text=otInk] at (2.0944,3.12) {$r=2\,\mathrm{cm}$};

\end{tikzpicture}""",
'empilement_face': r"""\begin{tikzpicture}[line cap=round,line join=round]
\draw[otGreenDark,fill=otGreen!12] (0,0) rectangle (1,1);
\draw[otGreenDark,fill=otGreen!12] (0,1) rectangle (1,2);
\draw[otGreenDark,fill=otGreen!12] (0,2) rectangle (1,3);
\node[anchor=north,text=otInk] at (0.5,-0.2) {1};
\draw[otGreenDark,fill=otGreen!12] (1,0) rectangle (2,1);
\draw[otGreenDark,fill=otGreen!12] (1,1) rectangle (2,2);
\node[anchor=north,text=otInk] at (1.5,-0.2) {2};
\draw[otGreenDark,fill=otGreen!12] (2,0) rectangle (3,1);
\draw[otGreenDark,fill=otGreen!12] (2,1) rectangle (3,2);
\node[anchor=north,text=otInk] at (2.5,-0.2) {3};
\node[anchor=south,text=otGreenDark] at (1.5,3.4) {Vue de face};
\node[anchor=north,text=otInk] at (1.5,-0.8) {Colonnes};

\end{tikzpicture}""",
})
