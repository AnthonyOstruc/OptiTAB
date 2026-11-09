# -*- coding: utf-8 -*-
"""Figures du formulaire « Statistiques »."""

# Boîte à moustaches de la série 3, 4, 5, 6, 6, 7, 8, 9 (min 3, Q1 4, Me 6, Q3 7, max 9).
BOITE = r"""
\begin{tikzpicture}[x=0.78cm,y=1cm]
  \draw[otMuted,line width=0.6pt,-{Stealth[length=2.3mm]}] (1.6,0) -- (10.5,0);
  \foreach \k in {2,...,10} \draw[otMuted,line width=0.5pt] (\k,0.07) -- (\k,-0.07);
  \foreach \k in {2,...,10} \node[anchor=north,font=\otRegular\fontsize{9}{10}\selectfont,text=otMuted,inner sep=1.5pt] at (\k,-0.1) {$\k$};
  \fill[otSky] (4,0.55) rectangle (7,1.35);
  \draw[otNavy,line width=1.1pt] (4,0.55) rectangle (7,1.35);
  \draw[otNavy,line width=1.6pt] (6,0.55) -- (6,1.35);
  \draw[otNavy,line width=1.1pt] (3,0.95) -- (4,0.95) (7,0.95) -- (9,0.95);
  \draw[otNavy,line width=1.1pt] (3,0.75) -- (3,1.15) (9,0.75) -- (9,1.15);
  \node[anchor=south,inner sep=1.5pt,text=otNavy] at (3,1.2) {min};
  \node[anchor=south,inner sep=1.5pt,text=otNavy] at (4,1.4) {$Q_1$};
  \node[anchor=south,inner sep=1.5pt,text=otGreenDark] at (6,1.4) {$\mathrm{Me}$};
  \node[anchor=south,inner sep=1.5pt,text=otNavy] at (7,1.4) {$Q_3$};
  \node[anchor=south,inner sep=1.5pt,text=otNavy] at (9,1.2) {max};
\end{tikzpicture}"""

# Histogramme : classes [0;10[ (4), [10;20[ (10), [20;30[ (6), [30;50[ (8).
HISTOGRAMME = r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=6.6cm, height=3.8cm, xmin=-3, xmax=56, ymin=0, ymax=1.35,
  xtick={0,10,20,30,40,50}, ytick=\empty, axis y line=none, xlabel={}, ylabel={}]
  \draw[fill=otNavy!40,draw=otNavy,line width=0.8pt] (axis cs:0,0) rectangle (axis cs:10,0.4);
  \draw[fill=otNavy!40,draw=otNavy,line width=0.8pt] (axis cs:10,0) rectangle (axis cs:20,1.0);
  \draw[fill=otNavy!40,draw=otNavy,line width=0.8pt] (axis cs:20,0) rectangle (axis cs:30,0.6);
  \draw[fill=otGreen!45,draw=otGreenDark,line width=0.8pt] (axis cs:30,0) rectangle (axis cs:50,0.4);
  \node[anchor=south,inner sep=1.5pt] at (axis cs:5,0.42) {$4$};
  \node[anchor=south,inner sep=1.5pt] at (axis cs:15,1.02) {$10$};
  \node[anchor=south,inner sep=1.5pt] at (axis cs:25,0.62) {$6$};
  \node[anchor=south,inner sep=1.5pt,text=otGreenDark] at (axis cs:40,0.42) {$8$};
\end{axis}
\end{tikzpicture}"""

XS = [1, 2, 3, 4, 5, 6, 7]
YS = [2.1, 2.9, 4.2, 4.8, 6.1, 6.8, 8.1]
N = len(XS)
MX, MY = sum(XS) / N, sum(YS) / N
COV = sum((x - MX) * (y - MY) for x, y in zip(XS, YS)) / N
VX = sum((x - MX) ** 2 for x in XS) / N
A = COV / VX
B = MY - A * MX

NUAGE = r"""
\begin{tikzpicture}
\begin{axis}[otWeb, width=6.2cm, height=4.4cm, xmin=-0.3, xmax=8.2, ymin=-0.3, ymax=9.6,
  xtick={1,2,3,4,5,6,7}, ytick={2,4,6,8}, clip=true, clip mode=individual]
  \addplot[otGreenDark, line width=1.1pt, domain=0.3:7.8] {""" + f"{A:.4f}*x+{B:.4f}" + r"""};
  \addplot[only marks, mark=*, mark size=2.2pt, otNavy] coordinates {""" + " ".join(f"({x},{y})" for x, y in zip(XS, YS)) + r"""};
  \draw[guide] (axis cs:""" + f"{MX},0) -- (axis cs:{MX},{MY:.3f}) -- (axis cs:0,{MY:.3f}" + r""");
  \fill[otOrange!85!black] (axis cs:""" + f"{MX},{MY:.3f}" + r""") circle (2.6pt);
  \node[anchor=north west,text=otOrange!75!black,inner sep=2pt] at (axis cs:""" + f"{MX + 0.15},{MY - 0.25:.3f}" + r""") {$G$};
  \node[anchor=south east,text=otGreenDark,inner sep=1.5pt] at (axis cs:7.7,8.9) {droite d’ajustement};
\end{axis}
\end{tikzpicture}"""

FIGURES = {"boite_moustaches": BOITE, "histogramme": HISTOGRAMME, "nuage_ajustement": NUAGE}
