# -*- coding: utf-8 -*-
"""Figure de « Tableaux de signes et de variations » : courbe de x³ − 3x."""

COURBE = r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=6.4cm, height=5.6cm, xmin=-2.6, xmax=2.8, ymin=-3.2, ymax=3.4,
  xtick={-1,1}, xticklabels={}, ytick={-2,2}, yticklabels={$-2$,$2$}]
  \draw[guide] (axis cs:-1,0) -- (axis cs:-1,2) -- (axis cs:0,2);
  \draw[guide] (axis cs:1,0) -- (axis cs:1,-2) -- (axis cs:0,-2);
  \draw[otOrange,line width=1pt] (axis cs:-1.55,2) -- (axis cs:-0.45,2);
  \draw[otOrange,line width=1pt] (axis cs:0.45,-2) -- (axis cs:1.55,-2);
  \addplot[courbe, domain=-2.1:2.1, samples=200] {x^3-3*x};
  \pnt{-1}{2} \pnt{1}{-2}
  \node[etiq,text=otNavy,anchor=west] at (axis cs:1.85,-1.2) {$y = x^3 - 3x$};
\end{axis}
\end{tikzpicture}"""

XLAB = {"courbe_variations": [(-1, "c", r"-1"), (1, "h", r"1")]}

FIGURES = {"courbe_variations": COURBE}
