# -*- coding: utf-8 -*-
"""Figure du formulaire « Dérivées usuelles »."""

TANGENTE = r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=7cm, height=4.8cm, xmin=-0.6, xmax=4.7, ymin=-0.4, ymax=4.0,
  xtick={2}, xticklabels={}, ytick=\empty]
  \addplot[courbe, domain=-0.5:4.2] {0.2*x^2+0.5};
  \addplot[courbe2, domain=0.2:4.4] {0.8*(x-2)+1.3};
  \draw[guide] (axis cs:2,0) -- (axis cs:2,1.3) -- (axis cs:0,1.3);
  \draw[otOrange!85!black,line width=0.8pt] (axis cs:2,1.3) -- (axis cs:3,1.3) -- (axis cs:3,2.1);
  \pnt{2}{1.3}
  \node[anchor=north,text=otOrange!75!black,inner sep=1.5pt] at (axis cs:2.5,1.27) {$1$};
  \node[anchor=west,text=otOrange!75!black,inner sep=1.5pt] at (axis cs:3.04,1.7) {$f'(a)$};
  \node[anchor=east,inner sep=1.5pt,font=\otRegular\fontsize{9}{10}\selectfont,text=otMuted] at (axis cs:-0.05,1.3) {$f(a)$};
  \node[anchor=south east,text=otNavy] at (axis cs:1.95,1.35) {$A$};
  \node[anchor=south east,text=otNavy] at (axis cs:4.1,3.95) {$\mathcal{C}_f$};
  \node[anchor=north west,text=otGreenDark] at (axis cs:4.0,3.1) {$T$};
\end{axis}
\end{tikzpicture}"""

XLAB = {"tangente": [(2, "c", r"a")]}

FIGURES = {"tangente": TANGENTE}
