# -*- coding: utf-8 -*-
"""Figures TikZ ; préambule officiel fourni par figures_livre.py."""
FIGURES = {
    'cours_schema': r"""
\begin{tikzpicture}[x=1cm,y=1cm,font=\large,text=otInk,line width=.8pt]
\draw[otNavy,rounded corners=3pt] (0.0,0) rectangle (1.5,1.6);
\fill[otNavy] (0.4,0.3) circle (2.2pt);
\fill[otNavy] (1.05,0.3) circle (2.2pt);
\fill[otNavy] (0.4,0.75) circle (2.2pt);
\fill[otNavy] (1.05,0.75) circle (2.2pt);
\fill[otNavy] (0.4,1.2) circle (2.2pt);
\fill[otNavy] (1.05,1.2) circle (2.2pt);
\draw[otNavy,rounded corners=3pt] (1.8,0) rectangle (3.3,1.6);
\fill[otNavy] (2.2,0.3) circle (2.2pt);
\fill[otNavy] (2.85,0.3) circle (2.2pt);
\fill[otNavy] (2.2,0.75) circle (2.2pt);
\fill[otNavy] (2.85,0.75) circle (2.2pt);
\fill[otNavy] (2.2,1.2) circle (2.2pt);
\fill[otNavy] (2.85,1.2) circle (2.2pt);
\draw[otNavy,rounded corners=3pt] (3.6,0) rectangle (5.1,1.6);
\fill[otNavy] (4.0,0.3) circle (2.2pt);
\fill[otNavy] (4.65,0.3) circle (2.2pt);
\fill[otNavy] (4.0,0.75) circle (2.2pt);
\fill[otNavy] (4.65,0.75) circle (2.2pt);
\fill[otNavy] (4.0,1.2) circle (2.2pt);
\fill[otNavy] (4.65,1.2) circle (2.2pt);
\draw[otNavy,rounded corners=3pt] (5.4,0) rectangle (6.9,1.6);
\fill[otNavy] (5.800000000000001,0.3) circle (2.2pt);
\fill[otNavy] (6.450000000000001,0.3) circle (2.2pt);
\fill[otNavy] (5.800000000000001,0.75) circle (2.2pt);
\fill[otNavy] (6.450000000000001,0.75) circle (2.2pt);
\fill[otNavy] (5.800000000000001,1.2) circle (2.2pt);
\fill[otNavy] (6.450000000000001,1.2) circle (2.2pt);
\node[text=otInk] at (3.45,-0.45) {4 groupes de 6};
\end{tikzpicture}
""",
    'ex1_schema': r"""
\begin{tikzpicture}[x=1cm,y=1cm,font=\large,text=otInk,line width=.8pt]
\draw[otNavy,fill=otSky] (0.0,0) rectangle (1.75,.6);
\node[text=otInk] at (0.875,-0.4) {?};
\draw[otNavy,fill=otSky] (1.75,0) rectangle (3.5,.6);
\node[text=otInk] at (2.625,-0.4) {?};
\draw[otNavy,fill=otSky] (3.5,0) rectangle (5.25,.6);
\node[text=otInk] at (4.375,-0.4) {?};
\draw[otNavy,fill=otSky] (5.25,0) rectangle (7.0,.6);
\node[text=otInk] at (6.125,-0.4) {?};
\node[text=otInk] at (3.5,1.1) {36 cartes, 4 parts égales};
\end{tikzpicture}
""",
    'ex1_corrige': r"""
\begin{tikzpicture}[x=1cm,y=1cm,font=\large,text=otInk,line width=.8pt]
\draw[otNavy,fill=otGreen!25] (0.0,0) rectangle (1.75,.6);
\node[text=otGreenDark] at (0.875,-0.4) {9};
\draw[otNavy,fill=otGreen!25] (1.75,0) rectangle (3.5,.6);
\node[text=otGreenDark] at (2.625,-0.4) {9};
\draw[otNavy,fill=otGreen!25] (3.5,0) rectangle (5.25,.6);
\node[text=otGreenDark] at (4.375,-0.4) {9};
\draw[otNavy,fill=otGreen!25] (5.25,0) rectangle (7.0,.6);
\node[text=otGreenDark] at (6.125,-0.4) {9};
\node[text=otInk] at (3.5,1.1) {36 cartes, 4 parts égales};
\end{tikzpicture}
""",
}
