# -*- coding: utf-8 -*-
"""Figure du formulaire « Développements limités usuels »."""

DL_EXP = r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=5.6cm, height=5cm, xmin=-2.4, xmax=1.9, ymin=-1.2, ymax=5.6,
  xtick={-2,-1,1}, ytick={1,2,3,4,5}]
  \addplot[otOrange!85!black, line width=1.1pt, domain=-2.4:1.65] {1+x+x^2/2};
  \addplot[courbe2, domain=-2.2:1.65] {1+x};
  \addplot[courbe, domain=-2.4:1.65] {exp(x)};
  \pnt{0}{1}
  \node[anchor=west,text=otNavy] at (axis cs:1.68,5.21) {$y=\mathrm{e}^x$};
  \node[anchor=west,text=otOrange!75!black] at (axis cs:1.68,3.98) {$y=1+x+\frac{x^2}{2}$};
  \node[anchor=west,text=otGreenDark] at (axis cs:1.68,2.65) {$y=1+x$};
\end{axis}
\end{tikzpicture}"""

FIGURES = {"dl_exp": DL_EXP}
