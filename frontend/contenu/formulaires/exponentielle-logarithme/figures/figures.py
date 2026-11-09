# -*- coding: utf-8 -*-
"""Figure du formulaire « Exponentielle et logarithme »."""

EXP_LN = r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=6.4cm, height=6.4cm, xmin=-3.2, xmax=6.6, ymin=-3.2, ymax=6.6,
  xtick={1,2.71828}, xticklabels={}, ytick={1,2.71828}, yticklabels={$1$,$\mathrm{e}$}]
  \addplot[otRule,line width=0.7pt,dash pattern=on 3pt off 2pt,domain=-3.2:6.3] {x};
  \addplot[courbe, domain=-3.2:1.86] {exp(x)};
  \addplot[courbe2, domain=0.042:6.4] {ln(x)};
  \pnt{0}{1} \pnt{1}{2.71828}
  \fill[otGreenDark] (axis cs:1,0) circle (2.1pt); \fill[otGreenDark] (axis cs:2.71828,1) circle (2.1pt);
  \draw[guide] (axis cs:1,0) -- (axis cs:1,2.71828) -- (axis cs:0,2.71828);
  \draw[guide] (axis cs:2.71828,0) -- (axis cs:2.71828,1) -- (axis cs:0,1);
  \node[etiq,text=otNavy,anchor=east] at (axis cs:1.35,5.4) {$y=\mathrm{e}^x$};
  \node[etiq,text=otGreenDark,anchor=north] at (axis cs:5.0,1.25) {$y=\ln x$};
  \node[note,anchor=south west,fill=none] at (axis cs:5.0,5.4) {$y=x$};
\end{axis}
\end{tikzpicture}"""

XLAB = {"exp_ln": [(1, "d", r"1"), (2.71828, "d", r"\mathrm{e}")]}

FIGURES = {"exp_ln": EXP_LN}
