# -*- coding: utf-8 -*-
"""Figures de « Méthodes d'intégration » : quart de disque, sommes de Riemann."""

QUART = r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=5.2cm, height=5.2cm, xmin=-0.3, xmax=1.45, ymin=-0.3, ymax=1.4,
  xtick={1}, xticklabels={}, ytick={1}, yticklabels={$1$}]
  \addplot[fill=otSky, draw=none, domain=0:1, samples=200] {sqrt(1-x^2)} \closedcycle;
  \addplot[courbe, domain=0:1, samples=300] {sqrt(1-x^2)};
  \node[text=otNavy] at (axis cs:0.38,0.36) {\large $\dfrac{\pi}{4}$};
  \node[etiq,text=otNavy,anchor=south west] at (axis cs:0.74,0.74) {$y = \sqrt{1 - x^2}$};
\end{axis}
\end{tikzpicture}"""

XLAB = {"quart_disque": [(1, "d", r"1")]}

N = 6
A, B = 0.4, 3.4
H = (B - A) / N


def f(x):
    return 0.35 + 0.22 * x * x


RECTS = "\n".join(
    rf"  \draw[otNavy!70,fill=otGreen!22,line width=0.6pt] (axis cs:{A + k * H:.4f},0) rectangle (axis cs:{A + (k + 1) * H:.4f},{f(A + k * H):.4f});"
    for k in range(N))

RIEMANN = rf"""
\begin{{tikzpicture}}
\begin{{axis}}[otWeb, width=7cm, height=4.6cm, xmin=-0.3, xmax=4.1, ymin=-0.3, ymax=3.4,
  xtick={{{A},{B}}}, xticklabels={{}}, ytick=\empty]
{RECTS}
  \addplot[courbe, domain=0.1:3.7, samples=200] {{0.35+0.22*x^2}};
  \node[etiq,text=otNavy,anchor=south east] at (axis cs:3.0,2.75) {{$\mathcal{{C}}_f$}};
\end{{axis}}
\end{{tikzpicture}}"""

XLAB["riemann"] = [(A, "c", r"a"), (B, "c", r"b")]

FIGURES = {"quart_disque": QUART, "riemann": RIEMANN}
