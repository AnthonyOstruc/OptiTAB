# -*- coding: utf-8 -*-
"""Figures exactes de la révision du 30 octobre 2026."""
FIGURES={
'r30_pommes_corrige': r"""
\begin{tikzpicture}
\begin{scope}[x=2.0cm,y=0.3888888888888889cm]
\draw[otRule,line width=.3pt] (1,0)--(1,9);\node[coteTexte,anchor=north,font=\small] at (1,0) {$ 1 $};
\draw[otRule,line width=.3pt] (2,0)--(2,9);\node[coteTexte,anchor=north,font=\small] at (2,0) {$ 2 $};
\draw[otRule,line width=.3pt] (2.5,0)--(2.5,9);\node[coteTexte,anchor=north,font=\small] at (2.5,0) {$ 2{,}5 $};
\draw[otRule,line width=.3pt] (3,0)--(3,9);\node[coteTexte,anchor=north,font=\small] at (3,0) {$ 3 $};
\draw[otRule,line width=.3pt] (0,3)--(3,3);\node[coteTexte,anchor=east,font=\small] at (0,3) {$ 3 $};
\draw[otRule,line width=.3pt] (0,6)--(3,6);\node[coteTexte,anchor=east,font=\small] at (0,6) {$ 6 $};
\draw[otRule,line width=.3pt] (0,7.5)--(3,7.5);\node[coteTexte,anchor=east,font=\small] at (0,7.5) {$ 7{,}5 $};
\draw[otRule,line width=.3pt] (0,9)--(3,9);\node[coteTexte,anchor=east,font=\small] at (0,9) {$ 9 $};
\draw[geoVecteur] (0,0)--(3.18,0);\draw[geoVecteur] (0,0)--(0,9.72);\node[anchor=north east,text=otInk,inner sep=4pt] at (0,0) {$ 0 $};
\node[anchor=north,text=otInk,inner sep=4pt] at (1.5,-1.6199999999999999) {$ \text{Masse (kg)} $};
\node[anchor=south west,text=otInk,inner sep=4pt] at (0,9.9) {$ \text{Prix (€)} $};
\draw[otGreenDark,line width=1pt] (0,0)--(1,3)--(2,6)--(3,9);
\fill[otGreenDark] (0,0) circle (2pt);
\fill[otGreenDark] (1,3) circle (2pt);
\fill[otGreenDark] (2,6) circle (2pt);
\fill[otGreenDark] (3,9) circle (2pt);
\draw[geoAide] (2.5,0)--(2.5,7.5)--(0,7.5);\fill[otGreenDark] (2.5,7.5) circle (2.5pt);

\end{scope}
\end{tikzpicture}
""",
}
