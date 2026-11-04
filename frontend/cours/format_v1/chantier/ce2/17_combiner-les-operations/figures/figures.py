# -*- coding: utf-8 -*-
"""Figures TikZ ; pr?ambule officiel fourni par outils/figures_livre.py."""
FIGURES = {
    'cours_schema': r"""
\begin{tikzpicture}[x=1cm,y=1cm,font=\large,text=otInk,line width=0.8pt]
\draw[otNavy,fill=otSky] (0.0,1.4) rectangle (2.42,2.05);
\node[] at (1.21,1.7249999999999999) {8};
\draw[otNavy,fill=otSky] (2.6,1.4) rectangle (5.0200000000000005,2.05);
\node[] at (3.81,1.7249999999999999) {8};
\draw[otNavy,fill=otSky] (5.2,1.4) rectangle (7.620000000000001,2.05);
\node[] at (6.41,1.7249999999999999) {8};
\draw[otNavy,fill=otSky] (0.0,0.0) rectangle (2.42,0.65);
\node[] at (1.21,0.325) {6};
\draw[otNavy,fill=otSky] (2.6,0.0) rectangle (5.0200000000000005,0.65);
\node[] at (3.81,0.325) {6};
\node[font=\normalsize] at (3.5,-0.65) {Chaque cadre représente un groupe};
\end{tikzpicture}
""",
    'ex1_schema': r"""
\begin{tikzpicture}[x=1cm,y=1cm,font=\large,text=otInk,line width=0.8pt]
\draw[otNavy,fill=otSky] (0.0,1.4) rectangle (1.3800000000000001,2.05);
\node[] at (0.6900000000000001,1.7249999999999999) {6};
\draw[otNavy,fill=otSky] (1.56,1.4) rectangle (2.94,2.05);
\node[] at (2.25,1.7249999999999999) {6};
\draw[otNavy,fill=otSky] (3.12,1.4) rectangle (4.5,2.05);
\node[] at (3.81,1.7249999999999999) {6};
\draw[otNavy,fill=otSky] (4.68,1.4) rectangle (6.0600000000000005,2.05);
\node[] at (5.37,1.7249999999999999) {6};
\draw[otNavy,fill=otSky] (6.24,1.4) rectangle (7.620000000000001,2.05);
\node[] at (6.930000000000001,1.7249999999999999) {6};
\draw[otNavy,fill=otSky] (0.0,0.0) rectangle (1.3800000000000001,0.65);
\node[] at (0.6900000000000001,0.325) {4};
\draw[otNavy,fill=otSky] (1.56,0.0) rectangle (2.94,0.65);
\node[] at (2.25,0.325) {4};
\draw[otNavy,fill=otSky] (3.12,0.0) rectangle (4.5,0.65);
\node[] at (3.81,0.325) {4};
\draw[otNavy,fill=otSky] (4.68,0.0) rectangle (6.0600000000000005,0.65);
\node[] at (5.37,0.325) {4};
\node[font=\normalsize] at (3.5,-0.65) {Chaque cadre représente un groupe};
\end{tikzpicture}
""",
    'ex5_schema': r"""
\begin{tikzpicture}[x=1cm,y=1cm,font=\large,text=otInk,line width=0.8pt]
\draw[otNavy,fill=otSky] (0,0) rectangle (7.5,.6);\draw[otNavy] (5.6250,0)--(5.6250,.6);
\node[] at (2.8125,0.3) {36};
\node[text=otGreenDark] at (6.5625,0.3) {?};
\node[text=otNavy] at (3.75,1.2) {Tout : 48 pommes};
\end{tikzpicture}
""",
    'ex9_schema': r"""
\begin{tikzpicture}[x=1cm,y=1cm,font=\large,text=otInk,line width=0.8pt]
\draw[otNavy,fill=otSky] (0,0) rectangle (7.5,.6);\draw[otNavy] (1.0714,0)--(1.0714,.6);
\node[] at (0.5357142857142857,0.3) {6};
\node[text=otGreenDark] at (4.285714285714286,0.3) {?};
\node[text=otNavy] at (3.75,1.2) {Tout : 42 crayons};
\end{tikzpicture}
""",
}
