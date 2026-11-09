# -*- coding: utf-8 -*-
"""Figure de « Primitive de ln(x) » : aire sous ln entre 1 et e, égale à 1."""

AIRE = r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=7.4cm, height=4.6cm, xmin=-0.4, xmax=5.6, ymin=-1.7, ymax=2.0,
  xtick={1,2.71828}, xticklabels={}, ytick={-1,1}, yticklabels={$-1$,$1$}]
  \addplot[fill=otSky, draw=none, domain=1:2.71828, samples=120] {ln(x)} \closedcycle;
  \draw[guide] (axis cs:2.71828,0) -- (axis cs:2.71828,1) -- (axis cs:0,1);
  \addplot[courbe, domain=0.19:5.4, samples=200] {ln(x)};
  \pnt{1}{0} \pnt{2.71828}{1}
  \node[text=otNavy,font=\small] at (axis cs:2.12,0.32) {$\mathcal{A} = 1$};
  \node[etiq,text=otNavy,anchor=north west] at (axis cs:4.0,0.86) {$y = \ln x$};
\end{axis}
\end{tikzpicture}"""

XLAB = {"aire_ln": [(1, "d", r"1"), (2.71828, "d", r"\mathrm{e}")]}

FIGURES = {"aire_ln": AIRE}
