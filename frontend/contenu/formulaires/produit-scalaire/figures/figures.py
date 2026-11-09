# -*- coding: utf-8 -*-
"""Figures du formulaire « Produit scalaire et géométrie repérée »."""

# Projeté orthogonal H de C sur (AB) : AB · AC = AB · AH.
PROJETE = r"""
\begin{tikzpicture}
  \coordinate (A) at (0,0); \coordinate (B) at (5.2,0); \coordinate (C) at (3.2,2.4); \coordinate (H) at (3.2,0);
  \draw[geoAide] (C) -- (H);
  \angledroit[0.22]{C}{H}{B}
  \draw[geoVecteur,line width=1.1pt] (A) -- (B);
  \draw[geoVecteur,line width=1.1pt,otGreenDark] (A) -- (C);
  \draw[otOrange!85!black,line width=2.2pt,line cap=round] (A) -- (H);
  \draw[otNavy!60,line width=0.7pt] (0.75,0) arc (0:36.87:0.75);
  \node[text=otNavy] at (18:1.12) {$\theta$};
  \foreach \p/\pos in {A/south west, B/south east, C/south, H/south}{}
  \node[anchor=north east,xshift=-1pt] at (A) {$A$};
  \node[anchor=north west,xshift=1pt] at (B) {$B$};
  \node[anchor=south,yshift=2pt] at (C) {$C$};
  \node[anchor=north,yshift=-2pt] at (H) {$H$};
\end{tikzpicture}"""

# Droite d'équation 2x - y - 1 = 0 avec un vecteur normal et un vecteur directeur.
DROITE = r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=5cm, height=5cm, xmin=-2, xmax=3.5, ymin=-2, ymax=3.5,
  xtick={1,2,3}, ytick={1,2,3}, yticklabels={}, clip=true, clip mode=individual]
  \addplot[courbe, domain=-0.5:2.25] {2*x - 1};
  \pnt{1}{1}
  \draw[otGreenDark,line width=1.2pt,-{Stealth[length=2.6mm]}] (axis cs:1,1) -- (axis cs:-1,2);
  \draw[otOrange!85!black,line width=1.6pt,-{Stealth[length=2.6mm]}] (axis cs:1,1) -- (axis cs:2,3);
  \node[anchor=south,text=otGreenDark,inner sep=1.5pt] at (axis cs:-1.1,2.1) {$\vec{n}\,(-2\,;1)$};
  \node[anchor=west,text=otOrange!75!black,inner sep=1.5pt] at (axis cs:1.75,2.2) {$\vec{u}\,(1\,;2)$};
  \node[anchor=west,text=otNavy,inner sep=1.5pt] at (axis cs:0.35,-1.4) {$2x - y - 1 = 0$};
\end{axis}
\end{tikzpicture}"""

FIGURES = {"projete_orthogonal": PROJETE, "droite_normale": DROITE}
