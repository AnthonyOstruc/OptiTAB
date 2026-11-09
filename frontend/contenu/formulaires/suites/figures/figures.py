# -*- coding: utf-8 -*-
"""Figure du formulaire « Suites arithmétiques et géométriques »."""

ARITH = " ".join(f"({n},{1 + 0.5 * n:.3f})" for n in range(9))
GEOM = " ".join(f"({n},{0.4 * 1.4 ** n:.3f})" for n in range(9))

SUITES_POINTS = r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=6.2cm, height=4.6cm, xmin=-0.4, xmax=8.7, ymin=-0.4, ymax=6.6,
  xtick={1,2,3,4,5,6,7,8}, ytick={1,2,3,4,5,6}, xlabel={$n$}, ylabel={}]
  \addplot[otNavy!40,line width=0.6pt,dash pattern=on 3pt off 2pt,domain=0:8.4] {1+0.5*x};
  \addplot[only marks,mark=*,mark size=2.1pt,otNavy] coordinates {""" + ARITH + r"""};
  \addplot[only marks,mark=*,mark size=2.1pt,otGreenDark] coordinates {""" + GEOM + r"""};
  \node[anchor=west,text=otGreenDark,align=left] at (axis cs:8.25,5.9) {suite\\géométrique};
  \node[anchor=west,text=otNavy,align=left] at (axis cs:8.6,4.2) {suite\\arithmétique};
\end{axis}
\end{tikzpicture}"""

FIGURES = {"suites_points": SUITES_POINTS}
