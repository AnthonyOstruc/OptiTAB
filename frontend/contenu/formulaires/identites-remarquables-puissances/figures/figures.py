# -*- coding: utf-8 -*-
"""Figure du formulaire « Identités remarquables, puissances et racines »."""

CARRE_IDENTITE = r"""
\begin{tikzpicture}
  \def\a{2.6} \def\b{1.4}
  \fill[otSky] (0,\b) rectangle (\a,\a+\b);
  \fill[otGreen!22] (\a,\b) rectangle (\a+\b,\a+\b);
  \fill[otGreen!22] (0,0) rectangle (\a,\b);
  \fill[otOrange!28] (\a,0) rectangle (\a+\b,\b);
  \draw[otNavy,line width=0.7pt] (\a,0) -- (\a,\a+\b) (0,\b) -- (\a+\b,\b);
  \draw[geoTrait,line width=1.2pt] (0,0) rectangle (\a+\b,\a+\b);
  \node[text=otNavy] at (\a/2,\b+\a/2) {$a^2$};
  \node[text=otGreenDark] at (\a+\b/2,\b+\a/2) {$ab$};
  \node[text=otGreenDark] at (\a/2,\b/2) {$ab$};
  \node[text=otOrange!75!black] at (\a+\b/2,\b/2) {$b^2$};
  \node[anchor=south,yshift=2pt] at (\a/2,\a+\b) {$a$};
  \node[anchor=south,yshift=2pt] at (\a+\b/2,\a+\b) {$b$};
  \node[anchor=east,xshift=-2pt] at (0,\b+\a/2) {$a$};
  \node[anchor=east,xshift=-2pt] at (0,\b/2) {$b$};
  \node[anchor=north,yshift=-3pt,font=\otMedium\fontsize{9}{10}\selectfont,text=otMuted] at ({(\a+\b)/2},0) {aire du carré de côté $a+b$};
\end{tikzpicture}"""

FIGURES = {"carre_identite": CARRE_IDENTITE}
