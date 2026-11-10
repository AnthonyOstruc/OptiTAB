# -*- coding: utf-8 -*-
"""Figures de « Produit en croix et proportionnalité »."""

# Tableau 3 kg → 7,50 € ; 5 kg → x. Diagonale 5 × 7,50 (vert), division par 3 (orange).
PRODUIT = r"""
\begin{tikzpicture}
  \fill[otSky] (0,0) rectangle (2.5,1.7);
  \fill[otOrange!30] (2.5,0.85) rectangle (4.1,1.7);
  \fill[otGreen!25] (4.1,0.85) rectangle (5.7,1.7);
  \fill[otGreen!25] (2.5,0) rectangle (4.1,0.85);
  \draw[otNavy,line width=0.7pt] (0,0) rectangle (5.7,1.7);
  \draw[otNavy,line width=0.7pt] (0,0.85) -- (5.7,0.85);
  \draw[otNavy,line width=0.7pt] (2.5,0) -- (2.5,1.7);
  \draw[otNavy,line width=0.7pt] (4.1,0) -- (4.1,1.7);
  \node[text=otInk] at (1.25,1.275) {Masse (kg)};
  \node[text=otInk] at (1.25,0.425) {Prix (€)};
  \node[text=otInk] at (3.3,1.275) {$3$};
  \node[text=otInk] at (4.9,1.275) {$5$};
  \node[text=otInk] at (3.3,0.425) {$7{,}50$};
  \node[text=otNavy] at (4.9,0.425) {$\boldsymbol{x}$};
  \draw[otGreenDark,line width=1.1pt,{Stealth[length=2mm]}-{Stealth[length=2mm]}] (4.62,1.1) -- (3.75,0.6);
  \node[anchor=north,text=otInk] at (2.85,-0.3) {$x = \dfrac{5 \times 7{,}50}{3} = 12{,}50$ €};
\end{tikzpicture}"""

GRAPHIQUE = r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=6.6cm, height=4.8cm, xmin=-0.6, xmax=6.4, ymin=-2, ymax=17.5,
  xtick={1,2,3,4,5}, ytick={5,10,15}, xlabel={masse (kg)}, ylabel={prix (€)}]
  \addplot[courbe, domain=0:5.9] {2.5*x};
  \addplot[otOrange!85!black,line width=1.3pt,dash pattern=on 5pt off 3pt, domain=0:5.9] {4+2*x};
  \pnt{0}{0} \pnt{2}{5} \pnt{4}{10}
  \pnt[otOrange!85!black]{0}{4}
  \node[etiq,text=otNavy,anchor=north west] at (axis cs:4.4,9.6) {proportionnel};
  \node[etiq,text=otOrange!75!black,anchor=south east] at (axis cs:3.3,11.8) {avec frais fixes};
\end{axis}
\end{tikzpicture}"""

FIGURES = {"produit_croix": PRODUIT, "graphique_proportionnalite": GRAPHIQUE}
