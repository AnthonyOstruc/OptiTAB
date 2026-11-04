# -*- coding: utf-8 -*-
"""Figures TikZ au style des livres ; compiler avec outils/figures_livre.py."""
FIGURES = {
'carre': r"""\begin{tikzpicture}[line cap=round]
\draw[otGreenDark,line width=1pt] (0,0)--(3,0)--(3,3)--(0,3)--cycle;
\draw[otGreenDark,->,line width=1pt] (.45,0)--(1.35,0);
\draw[otGreenDark,->,line width=1pt] (3,.5)--(3,1.4);
\draw[otGreenDark,->,line width=1pt] (2.6,3)--(1.7,3);
\draw[otGreenDark,->,line width=1pt] (0,2.6)--(0,1.7);
\node[anchor=north east] at (-.08,-.08) {$A$};
\node[anchor=north] at (1.5,-.2) {$c$};
\node[anchor=west] at (3.2,1.5) {$c$};
\node[anchor=south] at (1.5,3.2) {Sens du parcours};
\end{tikzpicture}""",
'rectangle': r"""\begin{tikzpicture}[line cap=round]
\draw[otGreenDark,line width=1pt] (0,0)--(4.5,0)--(4.5,2)--(0,2)--cycle;
\draw[otGreenDark,->,line width=1pt] (.45,0)--(1.35,0);
\draw[otGreenDark,->,line width=1pt] (4.5,.5)--(4.5,1.4);
\draw[otGreenDark,->,line width=1pt] (4.1,2)--(3.2,2);
\draw[otGreenDark,->,line width=1pt] (0,1.6)--(0,0.7);
\node[anchor=north east] at (-.08,-.08) {$A$};
\node[anchor=north] at (2.25,-.2) {$L$};
\node[anchor=west] at (4.7,1.0) {$\ell$};
\node[anchor=south] at (2.25,2.2) {Sens du parcours};
\end{tikzpicture}""",
}
