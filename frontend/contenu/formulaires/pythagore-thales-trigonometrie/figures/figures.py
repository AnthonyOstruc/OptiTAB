# -*- coding: utf-8 -*-
"""Figures de « Pythagore, Thalès et trigonométrie »."""

# Triangle 3-4-5 rectangle en A, carrés construits vers l'extérieur.
PYTHAGORE = r"""
\begin{tikzpicture}[scale=0.62]
  \coordinate (A) at (0,0); \coordinate (B) at (3,0); \coordinate (C) at (0,4);
  \fill[otGreen!22] (0,0) rectangle (3,-3);
  \fill[otSky] (0,0) rectangle (-4,4);
  \fill[otOrange!22] (3,0) -- (0,4) -- (4,7) -- (7,3) -- cycle;
  \draw[geoTrait] (0,0) rectangle (3,-3);
  \draw[geoTrait] (0,0) rectangle (-4,4);
  \draw[geoTrait] (3,0) -- (0,4) -- (4,7) -- (7,3) -- cycle;
  \fill[white] (A) -- (B) -- (C) -- cycle;
  \draw[otNavy,line width=1.3pt,line join=round] (A) -- (B) -- (C) -- cycle;
  \angledroit{B}{A}{C}
  \node[text=otGreenDark] at (1.5,-1.5) {\large $AB^2$};
  \node[text=otNavy] at (-2,2) {\large $AC^2$};
  \node[text=otOrange!75!black] at (3.5,3.5) {\large $BC^2$};
  \node[anchor=north east,text=otInk] at (-0.05,-0.05) {$A$};
  \node[anchor=north west,text=otInk] at (3.05,-0.05) {$B$};
  \node[anchor=south east,text=otInk] at (-0.05,4.05) {$C$};
\end{tikzpicture}"""

# Thalès : triangles emboîtés et papillon.
THALES = r"""
\begin{tikzpicture}
  % emboîtés
  \coordinate (A) at (0,0); \coordinate (B) at (2.6,2.2); \coordinate (C) at (3.7,0);
  \coordinate (M) at ($(A)!0.55!(B)$); \coordinate (N) at ($(A)!0.55!(C)$);
  \fill[otSky] (A) -- (B) -- (C) -- cycle;
  \fill[otGreen!22] (A) -- (M) -- (N) -- cycle;
  \draw[geoTrait] (A) -- (B) -- (C) -- cycle;
  \draw[otGreenDark,line width=1.1pt] (M) -- (N);
  \foreach \p in {A,B,C,M,N} \fill[otNavy] (\p) circle (1.6pt);
  \node[anchor=east] at (A) {$A$};
  \node[anchor=south] at ($(B)+(0,0.05)$) {$B$};
  \node[anchor=west] at (C) {$C$};
  \node[anchor=south east] at (M) {$M$};
  \node[anchor=north] at ($(N)+(0,-0.05)$) {$N$};
  \node[note,anchor=north] at (1.85,-0.75) {Triangles emboîtés};
  % papillon
  \begin{scope}[xshift=2.1cm,yshift=-3.4cm]
    \coordinate (A) at (0,0); \coordinate (B) at (2.6,1.5); \coordinate (C) at (2.9,-1.2);
    \coordinate (M) at ($(A)!-0.6!(B)$); \coordinate (N) at ($(A)!-0.6!(C)$);
    \fill[otSky] (A) -- (B) -- (C) -- cycle;
    \fill[otGreen!22] (A) -- (M) -- (N) -- cycle;
    \draw[geoTrait] (M) -- (B); \draw[geoTrait] (N) -- (C); \draw[geoTrait] (B) -- (C);
    \draw[otGreenDark,line width=1.1pt] (M) -- (N);
    \foreach \p in {A,B,C,M,N} \fill[otNavy] (\p) circle (1.6pt);
    \node[anchor=south] at ($(A)+(0,0.12)$) {$A$};
    \node[anchor=south west] at (B) {$B$};
    \node[anchor=north west] at (C) {$C$};
    \node[anchor=north east] at (M) {$M$};
    \node[anchor=south east] at (N) {$N$};
    \node[note,anchor=north] at (0.4,-1.75) {Configuration papillon};
  \end{scope}
\end{tikzpicture}"""

# Triangle rectangle en B, angle α en A.
TRIGO = r"""
\begin{tikzpicture}
  \coordinate (A) at (0,0); \coordinate (B) at (4.4,0); \coordinate (C) at (4.4,2.8);
  \fill[otSky] (A) -- (B) -- (C) -- cycle;
  \draw[geoTrait] (A) -- (B) -- (C) -- cycle;
  \angledroit{A}{B}{C}
  \draw[otOrange!85!black,line width=1pt] (0.95,0) arc[start angle=0,end angle={atan(2.8/4.4)},radius=0.95];
  \node[text=otOrange!75!black] at ({1.3*cos(16)},{1.3*sin(16)}) {$\alpha$};
  \node[anchor=east] at (A) {$A$};
  \node[anchor=north west] at (B) {$B$};
  \node[anchor=south west] at (C) {$C$};
  \node[anchor=north,text=otNavy,align=center] at (2.2,-0.12) {côté adjacent à $\alpha$};
  \node[anchor=west,text=otGreenDark,align=left] at (4.55,1.4) {côté opposé\\à $\alpha$};
  \node[anchor=south east,text=otOrange!75!black] at (2.0,1.5) {hypoténuse};
\end{tikzpicture}"""

FIGURES = {"pythagore_carres": PYTHAGORE, "thales_configurations": THALES, "triangle_trigo": TRIGO}
