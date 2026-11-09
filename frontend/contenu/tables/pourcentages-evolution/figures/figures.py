# -*- coding: utf-8 -*-
"""Figure « Pourcentages d'évolution » : 100 € → 120 € (+20 %), et le retour."""

SCHEMA = r"""
\begin{tikzpicture}
  \node[draw=otNavy,line width=1.1pt,fill=otSky,rounded corners=4pt,minimum width=2.4cm,minimum height=1cm,align=center] (A) at (0,0) {Prix initial\\$100$ €};
  \node[draw=otNavy,line width=1.1pt,fill=otSky,rounded corners=4pt,minimum width=2.4cm,minimum height=1cm,align=center] (B) at (5.6,0) {Prix final\\$120$ €};
  \draw[otGreenDark,line width=1.1pt,-{Stealth[length=2.6mm]}] (A.north east) to[bend left=28] (B.north west);
  \node[anchor=south,text=otGreenDark,align=center] at (2.8,0.95) {hausse de $20\,\%$ : $\times 1{,}2$};
  \draw[otOrange!85!black,line width=1.1pt,-{Stealth[length=2.6mm]}] (B.south west) to[bend left=28] (A.south east);
  \node[anchor=north,text=otOrange!75!black,align=center] at (2.8,-0.95) {retour : $\div 1{,}2$, soit $\approx -16{,}7\,\%$};
\end{tikzpicture}"""

FIGURES = {"hausse_retour": SCHEMA}
