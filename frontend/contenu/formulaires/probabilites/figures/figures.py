# -*- coding: utf-8 -*-
"""Figures du formulaire « Probabilités »."""
from math import comb

ARBRE = r"""
\begin{tikzpicture}[x=1cm,y=1cm]
  \coordinate (O) at (0,0);
  \coordinate (A) at (2.1,1.25); \coordinate (Ab) at (2.1,-1.25);
  \coordinate (AB) at (4.2,1.95); \coordinate (ABb) at (4.2,0.55);
  \coordinate (AbB) at (4.2,-0.55); \coordinate (AbBb) at (4.2,-1.95);
  \draw[otNavy,line width=0.9pt] (O) -- (A) (O) -- (Ab);
  \draw[otNavy,line width=0.9pt] (A) -- (AB) (A) -- (ABb) (Ab) -- (AbB) (Ab) -- (AbBb);
  \fill[otInk] (O) circle (1.6pt);
  \node[fill=white,inner sep=2pt] at (A) {$A$};
  \node[fill=white,inner sep=2pt] at (Ab) {$\overline{A}$};
  \node[fill=white,inner sep=2pt,anchor=west] at (AB) {$B$};
  \node[fill=white,inner sep=2pt,anchor=west] at (ABb) {$\overline{B}$};
  \node[fill=white,inner sep=2pt,anchor=west] at (AbB) {$B$};
  \node[fill=white,inner sep=2pt,anchor=west] at (AbBb) {$\overline{B}$};
  % probabilités des branches (au-dessus des branches montantes, en dessous des descendantes)
  \node[anchor=south east,text=otGreenDark,inner sep=1.5pt] at (1.0,0.62) {$P(A)$};
  \node[anchor=north east,text=otGreenDark,inner sep=1.5pt] at (1.0,-0.62) {$P(\overline{A})$};
  \node[anchor=south east,text=otGreenDark,inner sep=1.5pt] at (3.1,1.62) {$P_A(B)$};
  \node[anchor=north east,text=otGreenDark,inner sep=1.5pt] at (3.1,0.88) {$P_A(\overline{B})$};
  \node[anchor=south east,text=otGreenDark,inner sep=1.5pt] at (3.1,-0.88) {$P_{\overline{A}}(B)$};
  \node[anchor=north east,text=otGreenDark,inner sep=1.5pt] at (3.1,-1.62) {$P_{\overline{A}}(\overline{B})$};
\end{tikzpicture}"""

P = [comb(10, k) * 0.3 ** k * 0.7 ** (10 - k) for k in range(11)]
BINOMIALE = r"""
\begin{tikzpicture}
\begin{axis}[otBarres, width=7.2cm, height=3.8cm, bar width=11pt, ymax=0.3, enlarge x limits=0.06,
  xtick={0,1,2,3,4,5,6,7,8,9,10}, ytick={0.1,0.2}, yticklabels={$0{,}1$,$0{,}2$},
  xlabel={$k$}, ylabel={$P(X = k)$}]
  \addplot[fill=otNavy!60, draw=otNavy] coordinates {""" + " ".join(f"({k},{p:.4f})" for k, p in enumerate(P)) + r"""};
\end{axis}
\end{tikzpicture}"""

NORMALE = r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=7.2cm, height=3.6cm, xmin=-3.6, xmax=3.6, ymin=0, ymax=0.47,
  xtick={-2,-1,0,1,2}, xticklabels={}, ytick=\empty, axis y line=none, xlabel={}, ylabel={}]
  \addplot[fill=otSky!60!white, draw=none, domain=-2:2, samples=120] {exp(-x^2/2)/sqrt(2*pi)} \closedcycle;
  \addplot[fill=otSky, draw=none, domain=-1:1, samples=120] {exp(-x^2/2)/sqrt(2*pi)} \closedcycle;
  \draw[otNavy!45,line width=0.5pt] (axis cs:-1,0) -- (axis cs:-1,0.242);
  \draw[otNavy!45,line width=0.5pt] (axis cs:1,0) -- (axis cs:1,0.242);
  \draw[otNavy!30,line width=0.5pt] (axis cs:-2,0) -- (axis cs:-2,0.054);
  \draw[otNavy!30,line width=0.5pt] (axis cs:2,0) -- (axis cs:2,0.054);
  \draw[guide] (axis cs:0,0) -- (axis cs:0,0.399);
  \addplot[courbe, domain=-3.6:3.6, samples=200] {exp(-x^2/2)/sqrt(2*pi)};
  \node[text=otNavy] at (axis cs:0.5,0.12) {$68\,\%$};
  \node[text=otNavy!80] at (axis cs:-1.5,0.03) {$13{,}6\,\%$};
\end{axis}
\end{tikzpicture}"""

FIGURES = {"arbre_pondere": ARBRE, "loi_binomiale": BINOMIALE, "loi_normale": NORMALE}

XLAB = {"loi_normale": [(-2, "c", r"\mu - 2\sigma"), (-1, "c", r"\mu - \sigma"), (0, "c", r"\mu"),
                        (1, "c", r"\mu + \sigma"), (2, "c", r"\mu + 2\sigma")]}
