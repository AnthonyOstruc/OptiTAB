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


# Figures pédagogiques ajoutées lors de la révision du 30 octobre 2026.
FIGURES.update({
'bibliotheque': r"""\begin{tikzpicture}[line cap=round,line join=round]
\draw[otRule,line width=.9pt] (0,0.0)--(5.8,0.0);
\node[anchor=east,text=otInk] at (-0.16,0.0) {$0$};
\draw[otRule,line width=.9pt] (0,1.0)--(5.8,1.0);
\node[anchor=east,text=otInk] at (-0.16,1.0) {$6$};
\draw[otRule,line width=.9pt] (0,2.0)--(5.8,2.0);
\node[anchor=east,text=otInk] at (-0.16,2.0) {$12$};
\draw[otRule,line width=.9pt] (0,3.0)--(5.8,3.0);
\node[anchor=east,text=otInk] at (-0.16,3.0) {$18$};
\draw[otMuted,line width=.9pt,-{Stealth[length=1.8mm]}] (0,0)--(0,3.5);
\draw[otMuted,line width=.9pt,-{Stealth[length=1.8mm]}] (0,0)--(5.9,0);
\fill[otNavy] (0.5,0) rectangle (1.1,2.0);
\node[anchor=north,text=otInk] at (0.8,-0.18) {Lun};
\fill[otNavy] (1.5,0) rectangle (2.1,3.0);
\node[anchor=north,text=otInk] at (1.8,-0.18) {Mar};
\fill[otNavy] (2.5,0) rectangle (3.0999999999999996,2.5);
\node[anchor=north,text=otInk] at (2.8,-0.18) {Mer};
\fill[otNavy] (3.5,0) rectangle (4.1,1.5);
\node[anchor=north,text=otInk] at (3.8,-0.18) {Jeu};
\fill[otNavy] (4.5,0) rectangle (5.1,1.0);
\node[anchor=north,text=otInk] at (4.8,-0.18) {Ven};
\node[anchor=south west,text=otMuted] at (0,3.7) {Livres empruntés};

\end{tikzpicture}""",
'bibliotheque_corrige': r"""\begin{tikzpicture}[line cap=round,line join=round]
\draw[otRule,line width=.9pt] (0,0.0)--(5.8,0.0);
\node[anchor=east,text=otInk] at (-0.16,0.0) {$0$};
\draw[otRule,line width=.9pt] (0,1.0)--(5.8,1.0);
\node[anchor=east,text=otInk] at (-0.16,1.0) {$6$};
\draw[otRule,line width=.9pt] (0,2.0)--(5.8,2.0);
\node[anchor=east,text=otInk] at (-0.16,2.0) {$12$};
\draw[otRule,line width=.9pt] (0,3.0)--(5.8,3.0);
\node[anchor=east,text=otInk] at (-0.16,3.0) {$18$};
\draw[otMuted,line width=.9pt,-{Stealth[length=1.8mm]}] (0,0)--(0,3.5);
\draw[otMuted,line width=.9pt,-{Stealth[length=1.8mm]}] (0,0)--(5.9,0);
\fill[otNavy] (0.5,0) rectangle (1.1,2.0);
\node[anchor=north,text=otInk] at (0.8,-0.18) {Lun};
\node[anchor=south,text=otGreenDark] at (0.8,2.12) {$12$};
\fill[otNavy] (1.5,0) rectangle (2.1,3.0);
\node[anchor=north,text=otInk] at (1.8,-0.18) {Mar};
\node[anchor=south,text=otGreenDark] at (1.8,3.12) {$18$};
\fill[otGreenDark] (2.5,0) rectangle (3.0999999999999996,2.5);
\node[anchor=north,text=otInk] at (2.8,-0.18) {Mer};
\node[anchor=south,text=otGreenDark] at (2.8,2.62) {$15$};
\fill[otNavy] (3.5,0) rectangle (4.1,1.5);
\node[anchor=north,text=otInk] at (3.8,-0.18) {Jeu};
\node[anchor=south,text=otGreenDark] at (3.8,1.62) {$9$};
\fill[otGreenDark] (4.5,0) rectangle (5.1,1.0);
\node[anchor=north,text=otInk] at (4.8,-0.18) {Ven};
\node[anchor=south,text=otGreenDark] at (4.8,1.12) {$6$};
\node[anchor=south west,text=otMuted] at (0,3.7) {Livres empruntés};

\end{tikzpicture}""",
'transports40': r"""\begin{tikzpicture}[line cap=round,line join=round]
\fill[otNavy!65] (0,0)--(1.40000,0.00000) arc[start angle=0,end angle=90,radius=1.4]--cycle;
\draw[white,line width=.9pt] (0,0)--(1.4,0.0);
\node[anchor=west,text=otInk] at (1.85,0.8) {À pied : $25\,\%$};
\fill[otGreen!65] (0,0)--(0.00000,1.40000) arc[start angle=90,end angle=252,radius=1.4]--cycle;
\draw[white,line width=.9pt] (0,0)--(8.572527594031472e-17,1.4);
\node[anchor=west,text=otInk] at (1.85,0.0) {Vélo : $45\,\%$};
\fill[otOrange!75] (0,0)--(-0.43262,-1.33148) arc[start angle=252,end angle=360,radius=1.4]--cycle;
\draw[white,line width=.9pt] (0,0)--(-0.4326237921249266,-1.3314791228132148);
\node[anchor=west,text=otInk] at (1.85,-0.8) {Bus : $30\,\%$};

\end{tikzpicture}""",
'temperatures': r"""\begin{tikzpicture}[line cap=round,line join=round]
\draw[otRule,line width=.9pt] (0,0.0)--(5.2,0.0);
\node[anchor=east,text=otInk] at (-0.15,0.0) {$0$};
\draw[otRule,line width=.9pt] (0,0.8)--(5.2,0.8);
\node[anchor=east,text=otInk] at (-0.15,0.8) {$4$};
\draw[otRule,line width=.9pt] (0,1.6)--(5.2,1.6);
\node[anchor=east,text=otInk] at (-0.15,1.6) {$8$};
\draw[otRule,line width=.9pt] (0,2.4)--(5.2,2.4);
\node[anchor=east,text=otInk] at (-0.15,2.4) {$12$};
\draw[otRule,line width=.9pt] (0,3.2)--(5.2,3.2);
\node[anchor=east,text=otInk] at (-0.15,3.2) {$16$};
\draw[otMuted,line width=.9pt,-{Stealth[length=1.8mm]}] (0,0)--(0,3.8);
\draw[otMuted,line width=.9pt,-{Stealth[length=1.8mm]}] (0,0)--(5.4,0);
\draw[otNavy,line width=.9pt] (0.2,1.6)--(1.4,2.4)--(2.6,3.2)--(3.8,2.8)--(5.0,2.0);
\fill[otNavy] (0.2,1.6) circle (1.7pt);
\node[anchor=north,text=otInk] at (0.2,-0.18) {$8$ h};
\fill[otNavy] (1.4,2.4) circle (1.7pt);
\node[anchor=north,text=otInk] at (1.4,-0.18) {$10$ h};
\fill[otNavy] (2.6,3.2) circle (1.7pt);
\node[anchor=north,text=otInk] at (2.6,-0.18) {$12$ h};
\fill[otNavy] (3.8,2.8) circle (1.7pt);
\node[anchor=north,text=otInk] at (3.8,-0.18) {$14$ h};
\fill[otNavy] (5.0,2.0) circle (1.7pt);
\node[anchor=north,text=otInk] at (5.0,-0.18) {$16$ h};
\node[anchor=south west,text=otMuted] at (0,4.0) {Température (°C)};

\end{tikzpicture}""",
'temperatures_corrige': r"""\begin{tikzpicture}[line cap=round,line join=round]
\draw[otRule,line width=.9pt] (0,0.0)--(5.2,0.0);
\node[anchor=east,text=otInk] at (-0.15,0.0) {$0$};
\draw[otRule,line width=.9pt] (0,0.8)--(5.2,0.8);
\node[anchor=east,text=otInk] at (-0.15,0.8) {$4$};
\draw[otRule,line width=.9pt] (0,1.6)--(5.2,1.6);
\node[anchor=east,text=otInk] at (-0.15,1.6) {$8$};
\draw[otRule,line width=.9pt] (0,2.4)--(5.2,2.4);
\node[anchor=east,text=otInk] at (-0.15,2.4) {$12$};
\draw[otRule,line width=.9pt] (0,3.2)--(5.2,3.2);
\node[anchor=east,text=otInk] at (-0.15,3.2) {$16$};
\draw[otMuted,line width=.9pt,-{Stealth[length=1.8mm]}] (0,0)--(0,3.8);
\draw[otMuted,line width=.9pt,-{Stealth[length=1.8mm]}] (0,0)--(5.4,0);
\draw[otGreenDark,line width=.9pt] (0.2,1.6)--(1.4,2.4)--(2.6,3.2)--(3.8,2.8)--(5.0,2.0);
\fill[otGreenDark] (0.2,1.6) circle (1.7pt);
\node[anchor=north,text=otInk] at (0.2,-0.18) {$8$ h};
\node[anchor=south,text=otGreenDark] at (0.2,1.75) {$8$};
\fill[otGreenDark] (1.4,2.4) circle (1.7pt);
\node[anchor=north,text=otInk] at (1.4,-0.18) {$10$ h};
\node[anchor=south,text=otGreenDark] at (1.4,2.55) {$12$};
\fill[otGreenDark] (2.6,3.2) circle (1.7pt);
\node[anchor=north,text=otInk] at (2.6,-0.18) {$12$ h};
\node[anchor=south,text=otGreenDark] at (2.6,3.35) {$16$};
\fill[otGreenDark] (3.8,2.8) circle (1.7pt);
\node[anchor=north,text=otInk] at (3.8,-0.18) {$14$ h};
\node[anchor=west,text=otGreenDark] at (4.2,2.8499999999999996) {$14$};
\fill[otGreenDark] (5.0,2.0) circle (1.7pt);
\node[anchor=north,text=otInk] at (5.0,-0.18) {$16$ h};
\node[anchor=west,text=otGreenDark] at (5.2,2.05) {$10$};
\node[anchor=south west,text=otMuted] at (0,4.0) {Température (°C)};

\end{tikzpicture}""",
})
