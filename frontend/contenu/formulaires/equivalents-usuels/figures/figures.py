# -*- coding: utf-8 -*-
"""Figure de « Équivalents usuels » : sin x et x se confondent près de 0."""

SINUS = r"""
\begin{tikzpicture}
\begin{axis}[otTrig, width=7.4cm, height=4.6cm, xmin=-3.6, xmax=3.9, ymin=-2.3, ymax=2.5,
  xtick={-3.14159,3.14159}, xticklabels={}, ytick={-1,1}, yticklabels={$-1$,$1$}]
  \fill[otGreen, fill opacity=0.13] (axis cs:-0.55,-2.3) rectangle (axis cs:0.55,2.5);
  \addplot[courbe2, domain=-2.3:2.3, samples=60] {x};
  \addplot[courbe, domain=-3.6:3.6, samples=200] {sin(x)};
  \node[etiq,text=otGreenDark,anchor=east] at (axis cs:-2.2,-1.75) {$y = x$};
  \node[etiq,text=otNavy,anchor=north] at (axis cs:1.75,0.62) {$y = \sin x$};
\end{axis}
\end{tikzpicture}"""

XLAB = {"sinus_equivalent": [(-3.14159, "g", r"-\pi"), (3.14159, "g", r"\pi")]}

FIGURES = {"sinus_equivalent": SINUS}
