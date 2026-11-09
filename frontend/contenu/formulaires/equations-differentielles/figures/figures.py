# -*- coding: utf-8 -*-
"""Figures du formulaire « Équations différentielles »."""

# Famille de solutions de y' = -y + 2 : y = C e^{-x} + 2.
FAMILLE = r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=7cm, height=4.6cm, xmin=-0.6, xmax=4.4, ymin=-1.3, ymax=5.6,
  xtick={1,2,3,4}, ytick=\empty, clip=true, clip mode=individual]
  \addplot[otNavy!40, line width=0.9pt, domain=-0.6:4.4] {3*exp(-x)+2};
  \addplot[otNavy!40, line width=0.9pt, domain=-0.6:4.4] {1.5*exp(-x)+2};
  \addplot[otNavy!40, line width=0.9pt, domain=-0.6:4.4] {-1*exp(-x)+2};
  \addplot[otNavy!40, line width=0.9pt, domain=-0.6:4.4] {-2.2*exp(-x)+2};
  \addplot[courbe, domain=-0.6:4.4] {2.2*exp(-x)+2};
  \addplot[courbe2, domain=-0.6:4.4] {2};
  \pnt{0}{4.2}
  \node[anchor=south west,text=otGreenDark,inner sep=1.5pt] at (axis cs:0.1,2.08) {$y = 2$};
\end{axis}
\end{tikzpicture}"""

# Oscillations amorties : solution de y'' + 0,6 y' + 4,09 y = 0.
AMORTIES = r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=7cm, height=3.8cm, xmin=-0.3, xmax=9.6, ymin=-1.35, ymax=1.35,
  xtick=\empty, ytick={-1,1}, clip=true, clip mode=individual, xlabel={$t$}]
  \addplot[seuil, domain=0:9.4, samples=100] {exp(-0.3*x)};
  \addplot[seuil, domain=0:9.4, samples=100] {-exp(-0.3*x)};
  \addplot[courbe, domain=0:9.4, samples=400] {exp(-0.3*x)*cos(deg(2*x))};
  \node[anchor=west,text=otOrange!75!black,inner sep=1.5pt] at (axis cs:3.3,0.62) {$\pm\,\mathrm{e}^{-0{,}3t}$};
\end{axis}
\end{tikzpicture}"""

FIGURES = {"famille_solutions": FAMILLE, "oscillations_amorties": AMORTIES}
