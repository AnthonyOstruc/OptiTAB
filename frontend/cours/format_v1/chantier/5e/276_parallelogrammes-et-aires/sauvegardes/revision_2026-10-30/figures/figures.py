# -*- coding: utf-8 -*-
"""Figures TikZ au style des livres ; compiler avec outils/figures_livre.py."""
FIGURES = {
'diagonales': r"""\begin{tikzpicture}[line cap=round]
\coordinate (A) at (0,0); \coordinate (B) at (4.6,0);
\coordinate (D) at (1.1,2); \coordinate (C) at (5.7,2);
\fill[otNavy!5] (A)--(B)--(C)--(D)--cycle;
\draw[geoTrait] (A)--(B)--(C)--(D)--cycle;
\node[anchor=north east] at (-.08,-.08) {$A$};
\node[anchor=north west] at (4.68,-.08) {$B$};
\node[anchor=south west] at (5.78,2.08) {$C$};
\node[anchor=south east] at (1.02,2.08) {$D$};
\draw[otGreenDark,dashed,line width=.8pt] (A)--(C) (B)--(D);
\fill[otGreenDark] (2.85,1) circle (1.6pt);
\node[text=otGreenDark,anchor=south west] at (2.95,1.17) {$O$};
\end{tikzpicture}""",
'hauteur': r"""\begin{tikzpicture}[line cap=round]
\coordinate (A) at (0,0); \coordinate (B) at (4.6,0);
\coordinate (D) at (1.1,2); \coordinate (C) at (5.7,2);
\fill[otNavy!5] (A)--(B)--(C)--(D)--cycle;
\draw[geoTrait] (A)--(B)--(C)--(D)--cycle;
\node[anchor=north east] at (-.08,-.08) {$A$};
\node[anchor=north west] at (4.68,-.08) {$B$};
\node[anchor=south west] at (5.78,2.08) {$C$};
\node[anchor=south east] at (1.02,2.08) {$D$};
\draw[otOrange,dashed,line width=.9pt] (1.1,0)--(D);
\draw[otOrange] (1.1,.2)--(1.3,.2)--(1.3,0);
\node[anchor=west,text=otInk] at (1.32,.85) {$h$};
\node[anchor=north] at (2.6,-.23) {base $b=AB$};
\end{tikzpicture}""",
'partage': r"""\begin{tikzpicture}[line cap=round]
\coordinate (A) at (0,0); \coordinate (B) at (4.6,0);
\coordinate (D) at (1.1,2); \coordinate (C) at (5.7,2);
\fill[otNavy!5] (A)--(B)--(C)--(D)--cycle;
\draw[geoTrait] (A)--(B)--(C)--(D)--cycle;
\node[anchor=north east] at (-.08,-.08) {$A$};
\node[anchor=north west] at (4.68,-.08) {$B$};
\node[anchor=south west] at (5.78,2.08) {$C$};
\node[anchor=south east] at (1.02,2.08) {$D$};
\fill[otGreen!14] (A)--(C)--(D)--cycle;
\draw[otGreenDark,line width=1pt] (A)--(C);
\node[text=otGreenDark] at (2.1,1.4) {$\frac{\mathcal A}{2}$};
\node[text=otGreenDark] at (3.65,.55) {$\frac{\mathcal A}{2}$};
\end{tikzpicture}""",
}
