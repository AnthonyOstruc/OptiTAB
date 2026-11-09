# -*- coding: utf-8 -*-
"""Figure du formulaire « Primitives et intégrales »."""

AIRE = r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=7cm, height=4.4cm, xmin=-0.4, xmax=6.2, ymin=-0.4, ymax=3.3,
  xtick={1,4.6}, xticklabels={}, ytick=\empty]
  \addplot[fill=otSky, draw=none, domain=1:4.6, samples=120] {1.7+0.7*sin(deg(x))} \closedcycle;
  \draw[otNavy!50,line width=0.6pt] (axis cs:1,0) -- (axis cs:1,{1.7+0.7*sin(deg(1))});
  \draw[otNavy!50,line width=0.6pt] (axis cs:4.6,0) -- (axis cs:4.6,{1.7+0.7*sin(deg(4.6))});
  \addplot[courbe, domain=0.2:5.8, samples=160] {1.7+0.7*sin(deg(x))};
  \node[text=otNavy] at (axis cs:2.8,1.05) {$\displaystyle\int_a^b f(x)\,\mathrm{d}x$};
  \node[anchor=south,text=otNavy] at (axis cs:1.7,2.42) {$\mathcal{C}_f$};
\end{axis}
\end{tikzpicture}"""

XLAB = {"aire_integrale": [(1, "c", r"a"), (4.6, "c", r"b")]}

FIGURES = {"aire_integrale": AIRE}
