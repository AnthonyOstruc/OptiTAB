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


# Figures pédagogiques ajoutées lors de la révision du 30 octobre 2026.
FIGURES.update({
'trajet_l': r"""\begin{tikzpicture}[line cap=round,line join=round]
\draw[otGreenDark,line width=.9pt] (0,0)--(3,0);
\draw[otGreenDark,line width=.9pt,-{Stealth[length=1.8mm,width=1.4mm]}] (1.1400000000000001,0.0)--(1.8599999999999999,0.0);
\draw[otGreenDark,line width=.9pt] (3,0)--(3,2);
\draw[otGreenDark,line width=.9pt,-{Stealth[length=1.8mm,width=1.4mm]}] (3.0,0.76)--(3.0,1.24);
\node[anchor=north east,text=otGreenDark] at (-0.1,-0.1) {$A$};
\node[anchor=north west,text=otGreenDark] at (3.1,-0.1) {$B$};
\node[anchor=south west,text=otGreenDark] at (3.1,2.1) {$C$};
\node[anchor=north,text=otGreenDark] at (1.5,-0.36) {30 pas};
\node[anchor=west,text=otGreenDark] at (3.3,1.0) {20 pas};

\end{tikzpicture}""",
'rectangle_30_20': r"""\begin{tikzpicture}[line cap=round,line join=round]
\draw[otGreenDark,line width=.9pt] (0,0)--(3,0);
\draw[otGreenDark,line width=.9pt,-{Stealth[length=1.8mm,width=1.4mm]}] (1.1400000000000001,0.0)--(1.8599999999999999,0.0);
\draw[otGreenDark,line width=.9pt] (3,0)--(3,2);
\draw[otGreenDark,line width=.9pt,-{Stealth[length=1.8mm,width=1.4mm]}] (3.0,0.76)--(3.0,1.24);
\draw[otGreenDark,line width=.9pt] (3,2)--(0,2);
\draw[otGreenDark,line width=.9pt,-{Stealth[length=1.8mm,width=1.4mm]}] (1.8599999999999999,2.0)--(1.1400000000000001,2.0);
\draw[otGreenDark,line width=.9pt] (0,2)--(0,0);
\draw[otGreenDark,line width=.9pt,-{Stealth[length=1.8mm,width=1.4mm]}] (0.0,1.24)--(0.0,0.76);
\node[anchor=north east,text=otGreenDark] at (-0.1,-0.1) {$A$};
\node[anchor=north west,text=otGreenDark] at (3.1,-0.1) {$B$};
\node[anchor=south west,text=otGreenDark] at (3.1,2.1) {$C$};
\node[anchor=south west,text=otGreenDark] at (0.1,2.1) {$D$};
\node[anchor=north,text=otGreenDark] at (1.5,-0.36) {30 pas};
\node[anchor=west,text=otGreenDark] at (3.3,1.0) {20 pas};

\end{tikzpicture}""",
'carre_incomplet': r"""\begin{tikzpicture}[line cap=round,line join=round]
\draw[otGreenDark,line width=.9pt] (0,0)--(2.6,0);
\draw[otGreenDark,line width=.9pt,-{Stealth[length=1.8mm,width=1.4mm]}] (0.9880000000000001,0.0)--(1.612,0.0);
\draw[otGreenDark,line width=.9pt] (2.6,0)--(2.6,2.6);
\draw[otGreenDark,line width=.9pt,-{Stealth[length=1.8mm,width=1.4mm]}] (2.6,0.9880000000000001)--(2.6,1.612);
\draw[otGreenDark,line width=.9pt] (2.6,2.6)--(0,2.6);
\draw[otGreenDark,line width=.9pt,-{Stealth[length=1.8mm,width=1.4mm]}] (1.612,2.6)--(0.988,2.6);
\node[anchor=north east,text=otGreenDark] at (-0.1,-0.1) {$A$};
\node[anchor=north west,text=otGreenDark] at (2.7,-0.1) {$B$};
\node[anchor=south west,text=otGreenDark] at (2.7,2.7) {$C$};
\node[anchor=south west,text=otGreenDark] at (0.1,2.7) {$D$};
\node[anchor=north,text=otGreenDark] at (1.3,-0.36) {20 pas};
\node[anchor=west,text=otGreenDark] at (2.9,1.3) {20 pas};

\end{tikzpicture}""",
'carre_20': r"""\begin{tikzpicture}[line cap=round,line join=round]
\draw[otGreenDark,line width=.9pt] (0,0)--(2.6,0);
\draw[otGreenDark,line width=.9pt,-{Stealth[length=1.8mm,width=1.4mm]}] (0.9880000000000001,0.0)--(1.612,0.0);
\draw[otGreenDark,line width=.9pt] (2.6,0)--(2.6,2.6);
\draw[otGreenDark,line width=.9pt,-{Stealth[length=1.8mm,width=1.4mm]}] (2.6,0.9880000000000001)--(2.6,1.612);
\draw[otGreenDark,line width=.9pt] (2.6,2.6)--(0,2.6);
\draw[otGreenDark,line width=.9pt,-{Stealth[length=1.8mm,width=1.4mm]}] (1.612,2.6)--(0.988,2.6);
\draw[otGreenDark,line width=.9pt] (0,2.6)--(0,0);
\draw[otGreenDark,line width=.9pt,-{Stealth[length=1.8mm,width=1.4mm]}] (0.0,1.612)--(0.0,0.988);
\node[anchor=north east,text=otGreenDark] at (-0.1,-0.1) {$A$};
\node[anchor=north west,text=otGreenDark] at (2.7,-0.1) {$B$};
\node[anchor=south west,text=otGreenDark] at (2.7,2.7) {$C$};
\node[anchor=south west,text=otGreenDark] at (0.1,2.7) {$D$};
\node[anchor=north,text=otGreenDark] at (1.3,-0.36) {20 pas};
\node[anchor=west,text=otGreenDark] at (2.9,1.3) {20 pas};

\end{tikzpicture}""",
'escalier': r"""\begin{tikzpicture}[line cap=round,line join=round]
\draw[otGreenDark,line width=.9pt] (0,0)--(3,0);
\draw[otGreenDark,line width=.9pt,-{Stealth[length=1.8mm,width=1.4mm]}] (1.1400000000000001,0.0)--(1.8599999999999999,0.0);
\draw[otGreenDark,line width=.9pt] (3,0)--(3,1.2);
\draw[otGreenDark,line width=.9pt,-{Stealth[length=1.8mm,width=1.4mm]}] (3.0,0.45599999999999996)--(3.0,0.744);
\draw[otGreenDark,line width=.9pt] (3,1.2)--(6,1.2);
\draw[otGreenDark,line width=.9pt,-{Stealth[length=1.8mm,width=1.4mm]}] (4.140000000000001,1.2)--(4.859999999999999,1.2);
\draw[otGreenDark,line width=.9pt] (6,1.2)--(6,2.4);
\draw[otGreenDark,line width=.9pt,-{Stealth[length=1.8mm,width=1.4mm]}] (6.0,1.656)--(6.0,1.944);
\node[anchor=north east,text=otGreenDark] at (-0.1,-0.1) {$A$};
\node[anchor=north west,text=otGreenDark] at (3.1,-0.1) {$B$};
\node[anchor=south west,text=otGreenDark] at (3.1,1.3) {$C$};
\node[anchor=south west,text=otGreenDark] at (6.1,1.3) {$D$};
\node[anchor=south west,text=otGreenDark] at (6.1,2.5) {$E$};
\node[anchor=north,text=otGreenDark] at (1.5,-0.36) {50 pas};
\node[anchor=west,text=otGreenDark] at (3.3,0.6) {20 pas};

\end{tikzpicture}""",
'rectangle_50_20': r"""\begin{tikzpicture}[line cap=round,line join=round]
\draw[otGreenDark,line width=.9pt] (0,0)--(4,0);
\draw[otGreenDark,line width=.9pt,-{Stealth[length=1.8mm,width=1.4mm]}] (1.52,0.0)--(2.48,0.0);
\draw[otGreenDark,line width=.9pt] (4,0)--(4,1.6);
\draw[otGreenDark,line width=.9pt,-{Stealth[length=1.8mm,width=1.4mm]}] (4.0,0.6080000000000001)--(4.0,0.992);
\draw[otGreenDark,line width=.9pt] (4,1.6)--(0,1.6);
\draw[otGreenDark,line width=.9pt,-{Stealth[length=1.8mm,width=1.4mm]}] (2.48,1.6)--(1.52,1.6);
\draw[otGreenDark,line width=.9pt] (0,1.6)--(0,0);
\draw[otGreenDark,line width=.9pt,-{Stealth[length=1.8mm,width=1.4mm]}] (0.0,0.992)--(0.0,0.6080000000000001);
\node[anchor=north east,text=otGreenDark] at (-0.1,-0.1) {$A$};
\node[anchor=north west,text=otGreenDark] at (4.1,-0.1) {$B$};
\node[anchor=south west,text=otGreenDark] at (4.1,1.7000000000000002) {$C$};
\node[anchor=south west,text=otGreenDark] at (0.1,1.7000000000000002) {$D$};
\node[anchor=north,text=otGreenDark] at (2.0,-0.36) {50 pas};
\node[anchor=west,text=otGreenDark] at (4.3,0.8) {20 pas};

\end{tikzpicture}""",
'rectangle_8_5': r"""\begin{tikzpicture}[line cap=round,line join=round]
\draw[otGreenDark,line width=.9pt] (0,0)--(4,0);
\draw[otGreenDark,line width=.9pt,-{Stealth[length=1.8mm,width=1.4mm]}] (1.52,0.0)--(2.48,0.0);
\draw[otGreenDark,line width=.9pt] (4,0)--(4,2.5);
\draw[otGreenDark,line width=.9pt,-{Stealth[length=1.8mm,width=1.4mm]}] (4.0,0.95)--(4.0,1.55);
\draw[otGreenDark,line width=.9pt] (4,2.5)--(0,2.5);
\draw[otGreenDark,line width=.9pt,-{Stealth[length=1.8mm,width=1.4mm]}] (2.48,2.5)--(1.52,2.5);
\draw[otGreenDark,line width=.9pt] (0,2.5)--(0,0);
\draw[otGreenDark,line width=.9pt,-{Stealth[length=1.8mm,width=1.4mm]}] (0.0,1.55)--(0.0,0.95);
\node[anchor=north east,text=otGreenDark] at (-0.1,-0.1) {$A$};
\node[anchor=north west,text=otGreenDark] at (4.1,-0.1) {$B$};
\node[anchor=south west,text=otGreenDark] at (4.1,2.6) {$C$};
\node[anchor=south west,text=otGreenDark] at (0.1,2.6) {$D$};
\node[anchor=north,text=otGreenDark] at (2.0,-0.36) {$8\,\mathrm m$};
\node[anchor=west,text=otGreenDark] at (4.3,1.25) {$5\,\mathrm m$};

\end{tikzpicture}""",
'triangle_40': r"""\begin{tikzpicture}[line cap=round,line join=round]
\draw[otGreenDark,line width=.9pt] (0,0)--(4,0);
\draw[otGreenDark,line width=.9pt,-{Stealth[length=1.8mm,width=1.4mm]}] (1.52,0.0)--(2.48,0.0);
\draw[otGreenDark,line width=.9pt] (4,0)--(2,3.4641);
\draw[otGreenDark,line width=.9pt,-{Stealth[length=1.8mm,width=1.4mm]}] (3.24,1.3163580000000001)--(2.76,2.147742);
\draw[otGreenDark,line width=.9pt] (2,3.4641)--(0,0);
\draw[otGreenDark,line width=.9pt,-{Stealth[length=1.8mm,width=1.4mm]}] (1.24,2.147742)--(0.76,1.3163580000000001);
\node[anchor=north east,text=otGreenDark] at (-0.1,-0.1) {$A$};
\node[anchor=north west,text=otGreenDark] at (4.1,-0.1) {$B$};
\node[anchor=south west,text=otGreenDark] at (2.1,3.5641000000000003) {$C$};
\node[anchor=north,text=otGreenDark] at (2.0,-0.36) {40 pas};

\draw[otMuted,line width=.9pt,dashed] (4,0)--(5.3,0);
\draw[otOrange,line width=.8pt] (4.55,0) arc[start angle=0,end angle=120,radius=.55];
\node[anchor=west,text=otOrange] at (4.75,0.8) {$120^\circ$};
\end{tikzpicture}""",
})
