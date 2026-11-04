# -*- coding: utf-8 -*-
"""Figures TikZ ; pr?ambule officiel fourni par outils/figures_livre.py."""
FIGURES = {
    'cours_schema': r"""
\begin{tikzpicture}[x=1cm,y=1cm,font=\large,text=otInk,line width=0.8pt]
\draw[otNavy,fill=otSky] (0,0) rectangle (7.5,.6);\draw[otNavy] (2.8800,0)--(2.8800,.6);
\node[] at (1.44,0.3) {480};
\node[text=otGreenDark] at (5.1899999999999995,0.3) {?};
\node[text=otNavy] at (3.75,1.2) {Tout : 1 250 livres};
\end{tikzpicture}
""",
    'ex1_schema': r"""
\begin{tikzpicture}[x=1cm,y=1cm,font=\large,text=otInk,line width=0.8pt]
\draw[otNavy,fill=otSky] (0,0) rectangle (7.5,.6);\draw[otNavy] (4.4024,0)--(4.4024,.6);
\node[] at (2.2012022630834513,0.3) {1 245};
\node[text=otGreenDark] at (5.951202263083451,0.3) {?};
\node[text=otNavy] at (3.75,1.2) {Tout : 2 121 cahiers};
\end{tikzpicture}
""",
    'ex5_schema': r"""
\begin{tikzpicture}[x=1cm,y=1cm,font=\large,text=otInk,line width=0.8pt]
\draw[otNavy,fill=otSky] (0,0) rectangle (7.5,.6);\draw[otNavy] (2.7724,0)--(2.7724,.6);
\node[] at (1.3862068965517242,0.3) {268};
\node[text=otGreenDark] at (5.136206896551724,0.3) {?};
\node[text=otNavy] at (3.75,1.2) {Tout : 725 billes};
\end{tikzpicture}
""",
    'ex9_schema': r"""
\begin{tikzpicture}[x=1cm,y=1cm,font=\large,text=otInk,line width=0.8pt]
\draw[otNavy,fill=otSky] (0,0) rectangle (7.5,.6);\draw[otNavy] (1.4211,0)--(1.4211,.6);
\node[] at (0.7105263157894737,0.3) {18};
\node[text=otGreenDark] at (4.4605263157894735,0.3) {?};
\node[text=otNavy] at (3.75,1.2) {Tout : 95 cartes};
\end{tikzpicture}
""",
}
