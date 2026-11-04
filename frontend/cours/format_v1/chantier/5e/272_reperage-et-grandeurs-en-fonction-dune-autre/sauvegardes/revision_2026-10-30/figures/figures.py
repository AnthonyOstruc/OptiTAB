# -*- coding: utf-8 -*-
"""Schémas de travail mutualisés, sans échelle numérique."""
FIGURES = {
'cours_repere': r"""

\begin{tikzpicture}
\begin{scope}[x=0.58cm,y=0.58cm]
\draw[otRule,line width=.25pt,step=1] (-3,-3) grid (4,4);
\draw[geoVecteur] (-3,0)--(4.4,0);\draw[geoVecteur] (0,-3)--(0,4.5);
\node[coteTexte,anchor=north,font=\small] at (-3,0) {$ -3 $};
\node[coteTexte,anchor=north,font=\small] at (-2,0) {$ -2 $};
\node[coteTexte,anchor=north,font=\small] at (-1,0) {$ -1 $};
\node[coteTexte,anchor=north,font=\small] at (1,0) {$ 1 $};
\node[coteTexte,anchor=north,font=\small] at (2,0) {$ 2 $};
\node[coteTexte,anchor=south,font=\small] at (3,0) {$ 3 $};
\node[coteTexte,anchor=north,font=\small] at (4,0) {$ 4 $};
\node[coteTexte,anchor=east,font=\small] at (0,-3) {$ -3 $};
\node[coteTexte,anchor=east,font=\small] at (0,-2) {$ -2 $};
\node[coteTexte,anchor=east,font=\small] at (0,-1) {$ -1 $};
\node[coteTexte,anchor=east,font=\small] at (0,1) {$ 1 $};
\node[coteTexte,anchor=east,font=\small] at (0,2) {$ 2 $};
\node[coteTexte,anchor=east,font=\small] at (0,3) {$ 3 $};
\node[coteTexte,anchor=east,font=\small] at (0,4) {$ 4 $};
\node[anchor=north east,text=otInk,inner sep=3pt] at (0,0) {$ O $};
\draw[geoAide] (3,0)--(3,-2)--(0,-2);\fill[otNavy] (3,-2) circle (2pt);\node[anchor=south west,text=otInk,inner sep=3pt] at (3,-2) {$ A $};
\node[anchor=south west,text=otInk,inner sep=3pt] at (-2,3) {$ B $};
\fill[otGreenDark] (-2,3) circle (2pt);
\end{scope}
\end{tikzpicture}

""",
'jardin_schema': r"""
\begin{tikzpicture}
\draw[geoVecteur] (-3.3,0)--(3.3,0);\draw[geoVecteur] (0,-2.4)--(0,2.4);
\draw[geoTrait,fill=otSky,fill opacity=.4] (-2.5,1.6)--(2.5,1.6)--(2.5,-1.6)--(-2.5,-1.6)--cycle;
\node[anchor=south east,inner sep=4pt] at (-2.5,1.6) {$A$};
\node[anchor=south west,inner sep=4pt] at (2.5,1.6) {$B$};
\node[anchor=north west,inner sep=4pt] at (2.5,-1.6) {$C$};
\node[anchor=north east,inner sep=4pt] at (-2.5,-1.6) {$D$};
\node[anchor=north east,inner sep=4pt] at (0,0) {$O$};
\end{tikzpicture}
""",
}
