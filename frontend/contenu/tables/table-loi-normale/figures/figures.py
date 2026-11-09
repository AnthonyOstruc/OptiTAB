# -*- coding: utf-8 -*-
"""Figures de la « Table de la loi normale »."""

DENS = r"exp(-x^2/2)/sqrt(2*pi)"

AIRE_PHI = r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=7cm, height=3.6cm, xmin=-3.8, xmax=3.8, ymin=0, ymax=0.47,
  xtick={0,1.2}, xticklabels={}, ytick=\empty, axis y line=none, xlabel={}, ylabel={}]
  \addplot[fill=otSky, draw=none, domain=-3.8:1.2, samples=160] {""" + DENS + r"""} \closedcycle;
  \draw[otNavy!60,line width=0.6pt] (axis cs:1.2,0) -- (axis cs:1.2,0.1942);
  \addplot[courbe, domain=-3.8:3.8, samples=200] {""" + DENS + r"""};
  \node[text=otNavy,align=center] at (axis cs:-0.15,0.15) {$\Phi(1{,}2)$\\$\approx 0{,}8849$};
  \node[anchor=south west,text=otOrange!75!black,inner sep=1.5pt] at (axis cs:2.0,0.12) {$1 - \Phi(1{,}2)$};
\end{axis}
\end{tikzpicture}"""

SYMETRIE = r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=7cm, height=3.6cm, xmin=-3.8, xmax=3.8, ymin=0, ymax=0.47,
  xtick={-1.5,0,1.5}, xticklabels={}, ytick=\empty, axis y line=none, xlabel={}, ylabel={}]
  \addplot[fill=otOrange!30, draw=none, domain=-3.8:-1.5, samples=100] {""" + DENS + r"""} \closedcycle;
  \addplot[fill=otOrange!30, draw=none, domain=1.5:3.8, samples=100] {""" + DENS + r"""} \closedcycle;
  \draw[otNavy!50,line width=0.5pt] (axis cs:-1.5,0) -- (axis cs:-1.5,0.1295);
  \draw[otNavy!50,line width=0.5pt] (axis cs:1.5,0) -- (axis cs:1.5,0.1295);
  \draw[guide] (axis cs:0,0) -- (axis cs:0,0.399);
  \addplot[courbe, domain=-3.8:3.8, samples=200] {""" + DENS + r"""};
  \node[anchor=south,text=otOrange!75!black,inner sep=1.5pt] at (axis cs:-2.55,0.05) {aires};
  \node[anchor=south,text=otOrange!75!black,inner sep=1.5pt] at (axis cs:2.55,0.05) {égales};
\end{axis}
\end{tikzpicture}"""

FIGURES = {"aire_phi": AIRE_PHI, "symetrie": SYMETRIE}

XLAB = {
    "aire_phi": [(0, "c", r"0"), (1.2, "c", r"z = 1{,}2")],
    "symetrie": [(-1.5, "c", r"-z"), (0, "c", r"0"), (1.5, "c", r"z")],
}
