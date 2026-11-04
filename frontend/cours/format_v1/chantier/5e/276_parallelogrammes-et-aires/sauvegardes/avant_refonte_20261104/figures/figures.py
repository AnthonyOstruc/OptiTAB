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


# Figures pédagogiques ajoutées lors de la révision du 30 octobre 2026.
FIGURES.update({
'construction_depart': r"""\begin{tikzpicture}[line cap=round,line join=round]
\draw[otNavy,line width=.9pt] (0,0)--(4.6,0)--(5.7,2);
\node[anchor=north east,text=otInk] at (0,-0.08) {$A$};
\node[anchor=north west,text=otInk] at (4.68,-0.08) {$B$};
\node[anchor=south west,text=otInk] at (5.78,2.08) {$C$};

\end{tikzpicture}""",
'construction_fin': r"""\begin{tikzpicture}[line cap=round,line join=round]
\draw[otNavy,line width=.9pt] (0,0)--(4.6,0)--(5.7,2);
\draw[otGreenDark,line width=.9pt] (0,0)--(1.1,2)--(5.7,2);
\node[anchor=north east,text=otInk] at (0,-0.08) {$A$};
\node[anchor=north west,text=otInk] at (4.68,-0.08) {$B$};
\node[anchor=south west,text=otInk] at (5.78,2.08) {$C$};
\node[anchor=south east,text=otGreenDark] at (1.02,2.08) {$D$};

\end{tikzpicture}""",
'construction_diagonales': r"""\begin{tikzpicture}[line cap=round,line join=round]
\draw[otNavy,line width=.9pt] (0,0)--(4.6,0)--(5.7,2);
\draw[otGreenDark,line width=.9pt] (0,0)--(1.1,2)--(5.7,2);
\node[anchor=north east,text=otInk] at (0,-0.08) {$A$};
\node[anchor=north west,text=otInk] at (4.68,-0.08) {$B$};
\node[anchor=south west,text=otInk] at (5.78,2.08) {$C$};
\node[anchor=south east,text=otGreenDark] at (1.02,2.08) {$D$};
\draw[otGreenDark,line width=.9pt,dashed] (0,0)--(5.7,2);
\draw[otGreenDark,line width=.9pt,dashed] (1.1,2)--(4.6,0);
\fill[otGreenDark] (2.85,1) circle (1.5pt);
\node[anchor=south west,text=otGreenDark] at (3,1.22) {$O$};

\end{tikzpicture}""",
'parcelle': r"""\begin{tikzpicture}[line cap=round,line join=round]
\fill[otNavy!6] (0,0)--(4.2,0)--(4.9,1.4)--(.7,1.4)--cycle;
\fill[otGreen!12] (.7,1.4)--(4.9,1.4)--(2.8,2.8)--cycle;
\draw[otNavy,line width=.9pt] (0,0)--(4.2,0)--(4.9,1.4)--(2.8,2.8)--(0.7,1.4)--(0,0);
\draw[otMuted,line width=.9pt,dashed] (0.7,1.4)--(4.9,1.4);
\node[anchor=north east,text=otInk] at (-0.05,-0.08) {$A$};
\node[anchor=north west,text=otInk] at (4.25,-0.08) {$B$};
\node[anchor=south west,text=otInk] at (5.02,1.55) {$C$};
\node[anchor=south east,text=otInk] at (0.58,1.52) {$D$};
\node[anchor=south,text=otInk] at (2.8,2.95) {$E$};
\draw[cote] (-.65,0)--(-.65,1.4) node[coteTexte,midway] {$2\,\mathrm m$};
\draw[cote] (5.75,1.4)--(5.75,2.8) node[coteTexte,midway] {$2\,\mathrm m$};
\draw[otMuted,line width=.9pt,dashed] (-0.8,0)--(0,0);
\draw[otMuted,line width=.9pt,dashed] (-0.8,1.4)--(0.45,1.4);
\draw[otMuted,line width=.9pt,dashed] (4.9,1.4)--(5.9,1.4);
\draw[otMuted,line width=.9pt,dashed] (3.05,2.8)--(5.9,2.8);
\node[anchor=north,text=otInk] at (2.1,-0.25) {$6\,\mathrm m$};

\end{tikzpicture}""",
'parcelle_corrige': r"""\begin{tikzpicture}[line cap=round,line join=round]
\fill[otNavy!6] (0,0)--(4.2,0)--(4.9,1.4)--(.7,1.4)--cycle;
\fill[otGreen!12] (.7,1.4)--(4.9,1.4)--(2.8,2.8)--cycle;
\draw[otNavy,line width=.9pt] (0,0)--(4.2,0)--(4.9,1.4)--(2.8,2.8)--(0.7,1.4)--(0,0);
\draw[otMuted,line width=.9pt,dashed] (0.7,1.4)--(4.9,1.4);
\node[anchor=north east,text=otInk] at (-0.05,-0.08) {$A$};
\node[anchor=north west,text=otInk] at (4.25,-0.08) {$B$};
\node[anchor=south west,text=otInk] at (5.02,1.55) {$C$};
\node[anchor=south east,text=otInk] at (0.58,1.52) {$D$};
\node[anchor=south,text=otInk] at (2.8,2.95) {$E$};
\draw[cote] (-.65,0)--(-.65,1.4) node[coteTexte,midway] {$2\,\mathrm m$};
\draw[cote] (5.75,1.4)--(5.75,2.8) node[coteTexte,midway] {$2\,\mathrm m$};
\draw[otMuted,line width=.9pt,dashed] (-0.8,0)--(0,0);
\draw[otMuted,line width=.9pt,dashed] (-0.8,1.4)--(0.45,1.4);
\draw[otMuted,line width=.9pt,dashed] (4.9,1.4)--(5.9,1.4);
\draw[otMuted,line width=.9pt,dashed] (3.05,2.8)--(5.9,2.8);
\node[anchor=north,text=otInk] at (2.1,-0.25) {$6\,\mathrm m$};
\node[anchor=center,text=otGreenDark] at (2.5,0.65) {$12\,\mathrm m^2$};
\node[anchor=center,text=otGreenDark] at (2.8,1.95) {$6\,\mathrm m^2$};

\end{tikzpicture}""",
'terrasse': r"""\begin{tikzpicture}[line cap=round,line join=round]
\fill[otNavy!5] (0,0) rectangle (4.8,3.2);
\fill[otGreen!20] (1,.8)--(3.4,.8)--(4,2.4)--(1.6,2.4)--cycle;
\draw[otNavy,line width=.9pt] (0,0)--(4.8,0)--(4.8,3.2)--(0,3.2)--(0,0);
\draw[otGreenDark,line width=.9pt] (1,0.8)--(3.4,0.8)--(4,2.4)--(1.6,2.4)--(1,0.8);
\draw[cote] (-.55,0)--(-.55,3.2) node[coteTexte,midway] {$4\,\mathrm m$};
\draw[cote] (4.3,.8)--(4.3,2.4) node[coteTexte,midway] {$2\,\mathrm m$};
\node[anchor=north,text=otInk] at (2.4,-0.2) {$6\,\mathrm m$};
\node[anchor=north,text=otInk] at (2.2,0.57) {$3\,\mathrm m$};
\node[anchor=center,text=otGreenDark] at (2.5,1.65) {Massif};

\end{tikzpicture}""",
'terrasse_corrige': r"""\begin{tikzpicture}[line cap=round,line join=round]
\fill[otNavy!5] (0,0) rectangle (4.8,3.2);
\fill[otGreen!20] (1,.8)--(3.4,.8)--(4,2.4)--(1.6,2.4)--cycle;
\draw[otNavy,line width=.9pt] (0,0)--(4.8,0)--(4.8,3.2)--(0,3.2)--(0,0);
\draw[otGreenDark,line width=.9pt] (1,0.8)--(3.4,0.8)--(4,2.4)--(1.6,2.4)--(1,0.8);
\draw[cote] (-.55,0)--(-.55,3.2) node[coteTexte,midway] {$4\,\mathrm m$};
\draw[cote] (4.3,.8)--(4.3,2.4) node[coteTexte,midway] {$2\,\mathrm m$};
\node[anchor=north,text=otInk] at (2.4,-0.2) {$6\,\mathrm m$};
\node[anchor=north,text=otInk] at (2.2,0.57) {$3\,\mathrm m$};
\node[anchor=center,text=otGreenDark] at (2.5,1.65) {$6\,\mathrm m^2$};
\node[anchor=north,text=otGreenDark] at (2.4,-0.85) {Surface à daller : $18\,\mathrm m^2$};

\end{tikzpicture}""",
})
