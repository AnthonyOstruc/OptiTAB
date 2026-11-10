# -*- coding: utf-8 -*-
"""Figure de « Fonctions affines et équations de droites » : y = 2x + 1, pente et ordonnée à l'origine."""

DROITE = r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=6cm, height=6.6cm, xmin=-1.8, xmax=3.6, ymin=-1.6, ymax=7.8,
  xtick={-1,1,2,3}, ytick={3,5,7}]
  \addplot[courbe, domain=-1.3:3.2] {2*x+1};
  \draw[otGreenDark,line width=1.2pt,-{Stealth[length=2.2mm]}] (axis cs:1,3) -- (axis cs:2,3);
  \draw[otOrange!85!black,line width=1.2pt,-{Stealth[length=2.2mm]}] (axis cs:2,3) -- (axis cs:2,5);
  \node[anchor=north,text=otGreenDark] at (axis cs:1.5,2.9) {$+1$};
  \node[anchor=west,text=otOrange!75!black] at (axis cs:2.05,4) {$+2 = a$};
  \pnt{0}{1}
  \pnt{1}{3} \pnt{2}{5}
  \node[etiq,anchor=east,text=otNavy,font=\small] at (axis cs:-0.12,1.35) {$b = 1$};
  \node[etiq,text=otNavy,anchor=south east] at (axis cs:2.2,6.3) {$y = 2x + 1$};
\end{axis}
\end{tikzpicture}"""

FIGURES = {"droite_affine": DROITE}
