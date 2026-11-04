# -*- coding: utf-8 -*-
"""Figures TikZ au style des livres ; compiler avec outils/figures_livre.py."""
FIGURES = {
'barres': r"""\begin{tikzpicture}
\draw[otRule] (0,1.2)--(5.1,1.2) (0,2.4)--(5.1,2.4) (0,3)--(5.1,3);
\draw[otMuted,->] (0,0)--(0,3.6);
\draw[otMuted,->] (0,0)--(5.3,0);
\node[anchor=south west,text=otMuted] at (0,3.75) {Nombre d'élèves};
\fill[otNavy] (.55,0) rectangle (1.45,3);
\fill[otGreenDark] (2.15,0) rectangle (3.05,1.8);
\fill[otOrange] (3.75,0) rectangle (4.65,1.2);
\node[anchor=south] at (1,3.1) {$10$};
\node[anchor=south] at (2.6,1.9) {$6$};
\node[anchor=south] at (4.2,1.3) {$4$};
\node[anchor=north] at (1,-.18) {À pied};
\node[anchor=north] at (2.6,-.18) {Vélo};
\node[anchor=north] at (4.2,-.18) {Bus};
\node[anchor=east] at (-.15,0) {$0$};
\node[anchor=east] at (-.15,1.2) {$4$};
\node[anchor=east] at (-.15,2.4) {$8$};
\node[anchor=east] at (-.15,3) {$10$};
\end{tikzpicture}""",
'secteurs': r"""\begin{tikzpicture}
\fill[otNavy!75] (0,0)--(1.6,0) arc[start angle=0,end angle=180,radius=1.6]--cycle;
\fill[otGreen!75] (0,0)--(-1.6,0) arc[start angle=180,end angle=288,radius=1.6]--cycle;
\fill[otOrange!80] (0,0)--({1.6*cos(288)},{1.6*sin(288)}) arc[start angle=288,end angle=360,radius=1.6]--cycle;
\draw[white,line width=.8pt] (0,0)--(1.6,0) (0,0)--(-1.6,0) (0,0)--({1.6*cos(288)},{1.6*sin(288)});
\node[anchor=west] at (2,.8) {À pied : $50\,\%$};
\node[anchor=west] at (2,0) {Vélo : $30\,\%$};
\node[anchor=west] at (2,-.8) {Bus : $20\,\%$};
\end{tikzpicture}""",
}
