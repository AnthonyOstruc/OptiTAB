# -*- coding: utf-8 -*-
"""Figures TikZ ; pr?ambule officiel fourni par outils/figures_livre.py."""
FIGURES = {
    'cours_schema': r"""
\begin{tikzpicture}[x=1cm,y=1cm,font=\large,text=otInk,line width=0.8pt]
\node[font=\normalsize,text=otNavy] at (1.0,1.25) {milliers};
\draw[otRule] (0.1,.85)--(1.9,.85);
\node[] at (1.0,0.45) {2};
\node[font=\normalsize,text=otNavy] at (2.9,1.25) {centaines};
\draw[otRule] (2.0,.85)--(3.8,.85);
\node[] at (2.9,0.45) {3};
\node[font=\normalsize,text=otNavy] at (4.8,1.25) {dizaines};
\draw[otRule] (3.9,.85)--(5.699999999999999,.85);
\node[] at (4.8,0.45) {4};
\node[font=\normalsize,text=otNavy] at (6.699999999999999,1.25) {unités};
\draw[otRule] (5.799999999999999,.85)--(7.6,.85);
\node[] at (6.699999999999999,0.45) {6};
\end{tikzpicture}
""",
    'ex1_enonce': r"""
\begin{tikzpicture}[x=1cm,y=1cm,font=\large,text=otInk,line width=0.8pt]
\node[font=\normalsize,text=otNavy] at (1.0,1.25) {milliers};
\draw[otRule] (0.1,.85)--(1.9,.85);
\node[] at (1.0,0.45) {4};
\node[font=\normalsize,text=otNavy] at (2.9,1.25) {centaines};
\draw[otRule] (2.0,.85)--(3.8,.85);
\node[] at (2.9,0.45) {2};
\node[font=\normalsize,text=otNavy] at (4.8,1.25) {dizaines};
\draw[otRule] (3.9,.85)--(5.699999999999999,.85);
\node[] at (4.8,0.45) {0};
\node[font=\normalsize,text=otNavy] at (6.699999999999999,1.25) {unités};
\draw[otRule] (5.799999999999999,.85)--(7.6,.85);
\node[] at (6.699999999999999,0.45) {5};
\end{tikzpicture}
""",
}
