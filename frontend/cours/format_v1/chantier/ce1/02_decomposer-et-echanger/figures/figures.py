# -*- coding: utf-8 -*-
"""Figures TikZ ; préambule officiel fourni par figures_livre.py."""
FIGURES = {
    'cours_schema': r"""
\begin{tikzpicture}[x=1cm,y=1cm,font=\large,text=otInk,line width=.8pt]
\draw[otNavy,fill=otSky] (0.0,0) rectangle (2.2,1.35);
\node[text=otInk] at (1.1,1.9) {Centaines};
\node[text=otInk] at (1.1,0.68) {2};
\draw[otNavy,fill=otSky] (2.35,0) rectangle (4.550000000000001,1.35);
\node[text=otInk] at (3.45,1.9) {Dizaines};
\node[text=otInk] at (3.45,0.68) {4};
\draw[otNavy,fill=otSky] (4.7,0) rectangle (6.9,1.35);
\node[text=otInk] at (5.800000000000001,1.9) {Unités};
\node[text=otInk] at (5.800000000000001,0.68) {3};
\end{tikzpicture}
""",
    'ex1_schema': r"""
\begin{tikzpicture}[x=1cm,y=1cm,font=\large,text=otInk,line width=.8pt]
\draw[otNavy,fill=otSky] (0.0,0) rectangle (2.2,1.35);
\node[text=otInk] at (1.1,1.9) {Centaines};
\node[text=otInk] at (1.1,0.68) {4};
\draw[otNavy,fill=otSky] (2.35,0) rectangle (4.550000000000001,1.35);
\node[text=otInk] at (3.45,1.9) {Dizaines};
\node[text=otInk] at (3.45,0.68) {1};
\draw[otNavy,fill=otSky] (4.7,0) rectangle (6.9,1.35);
\node[text=otInk] at (5.800000000000001,1.9) {Unités};
\node[text=otInk] at (5.800000000000001,0.68) {6};
\end{tikzpicture}
""",
}
