# -*- coding: utf-8 -*-
"""Figure du formulaire « Limites et continuité »."""

# f(x) = (2x + 1)/(x - 1) : asymptote verticale x = 1, horizontale y = 2.
ASYMPTOTES = r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=7cm, height=5cm, xmin=-4.2, xmax=6.4, ymin=-4.6, ymax=8.4,
  xtick={-2,1,2,4}, xticklabels={}, ytick={-2,4,6}, clip=true, clip mode=individual]
  \draw[asymptote] (axis cs:1,-4.6) -- (axis cs:1,8.4);
  \draw[asymptote] (axis cs:-4.2,2) -- (axis cs:6.4,2);
  \addplot[courbe, domain=-4.2:0.62, samples=200] {(2*x+1)/(x-1)};
  \addplot[courbe, domain=1.47:6.4, samples=200] {(2*x+1)/(x-1)};
  \node[anchor=south west,text=otRed!85!black,inner sep=1.5pt] at (axis cs:-4.1,2.1) {$y = 2$};
  \node[anchor=south west,text=otRed!85!black,inner sep=1.5pt] at (axis cs:1.12,-4.4) {$x = 1$};
\end{axis}
\end{tikzpicture}"""

XLAB = {"asymptotes": [(-2, "c", r"-2"), (1, "d", r"1"), (2, "c", r"2"), (4, "c", r"4")]}

FIGURES = {"asymptotes": ASYMPTOTES}
