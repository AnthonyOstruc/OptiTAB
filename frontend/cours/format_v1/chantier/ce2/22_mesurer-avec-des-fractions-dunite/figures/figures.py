# -*- coding: utf-8 -*-
"""Figures TikZ ; pr?ambule officiel fourni par outils/figures_livre.py."""
FIGURES = {
    'cours_schema': r"""
\begin{tikzpicture}[x=1cm,y=1cm,font=\large,text=otInk,line width=0.8pt]
\draw[otNavy,->] (-.1,0)--(8.05,0);
\draw[otNavy] (0.0000,-.1)--(0.0000,.1);
\node[font=\normalsize] at (0.0,-0.4) {0};
\draw[otNavy] (0.6500,-.1)--(0.6500,.1);
\draw[otNavy] (1.3000,-.1)--(1.3000,.1);
\draw[otNavy] (1.9500,-.1)--(1.9500,.1);
\draw[otNavy] (2.6000,-.1)--(2.6000,.1);
\node[font=\normalsize] at (2.6,-0.4) {1 u};
\draw[otNavy] (3.2500,-.1)--(3.2500,.1);
\draw[otNavy] (3.9000,-.1)--(3.9000,.1);
\draw[otNavy] (4.5500,-.1)--(4.5500,.1);
\draw[otNavy] (5.2000,-.1)--(5.2000,.1);
\node[font=\normalsize] at (5.2,-0.4) {2 u};
\draw[otNavy] (5.8500,-.1)--(5.8500,.1);
\draw[otNavy] (6.5000,-.1)--(6.5000,.1);
\draw[otNavy] (7.1500,-.1)--(7.1500,.1);
\draw[otNavy] (7.8000,-.1)--(7.8000,.1);
\node[font=\normalsize] at (7.800000000000001,-0.4) {3 u};
\draw[otGreenDark,line width=3pt] (0,.72)--(7.1500,.72);
\draw[otGreenDark,dashed] (7.1500,.6)--(7.1500,.16);
\node[text=otGreenDark,font=\normalsize] at (3.9,1.3) {Segment à mesurer};
\node[font=\normalsize] at (3.9,-1.05) {Une unité partagée en 4 parts égales};
\end{tikzpicture}
""",
    'ex1_enonce': r"""
\begin{tikzpicture}[x=1cm,y=1cm,font=\large,text=otInk,line width=0.8pt]
\draw[otNavy,->] (-.1,0)--(8.05,0);
\draw[otNavy] (0.0000,-.1)--(0.0000,.1);
\node[font=\normalsize] at (0.0,-0.4) {0};
\draw[otNavy] (0.9750,-.1)--(0.9750,.1);
\draw[otNavy] (1.9500,-.1)--(1.9500,.1);
\draw[otNavy] (2.9250,-.1)--(2.9250,.1);
\draw[otNavy] (3.9000,-.1)--(3.9000,.1);
\node[font=\normalsize] at (3.9,-0.4) {1 u};
\draw[otNavy] (4.8750,-.1)--(4.8750,.1);
\draw[otNavy] (5.8500,-.1)--(5.8500,.1);
\draw[otNavy] (6.8250,-.1)--(6.8250,.1);
\draw[otNavy] (7.8000,-.1)--(7.8000,.1);
\node[font=\normalsize] at (7.8,-0.4) {2 u};
\draw[otGreenDark,line width=3pt] (0,.72)--(6.8250,.72);
\draw[otGreenDark,dashed] (6.8250,.6)--(6.8250,.16);
\node[text=otGreenDark,font=\normalsize] at (3.9,1.3) {Segment à mesurer};
\node[font=\normalsize] at (3.9,-1.05) {Une unité partagée en 4 parts égales};
\end{tikzpicture}
""",
}
