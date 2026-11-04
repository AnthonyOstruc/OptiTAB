# -*- coding: utf-8 -*-
"""Figures TikZ ; pr?ambule officiel fourni par outils/figures_livre.py."""
FIGURES = {
    'cours_schema': r"""
\begin{tikzpicture}[x=1cm,y=1cm,font=\large,text=otInk,line width=0.8pt]
\draw[otNavy,->] (-.15,0)--(8.2,0);
\draw[otNavy] (0.0,-.09)--(0.0,.09);
\node[font=\normalsize] at (0.0,-0.4) {$2\,000$};
\draw[otNavy] (0.8,-.09)--(0.8,.09);
\draw[otNavy] (1.6,-.09)--(1.6,.09);
\node[font=\normalsize] at (1.6,-0.4) {$2\,200$};
\draw[otNavy] (2.4,-.09)--(2.4,.09);
\draw[otNavy] (3.2,-.09)--(3.2,.09);
\node[font=\normalsize] at (3.2,-0.4) {$2\,400$};
\draw[otNavy] (4.0,-.09)--(4.0,.09);
\draw[otNavy] (4.8,-.09)--(4.8,.09);
\node[font=\normalsize] at (4.8,-0.4) {$2\,600$};
\draw[otNavy] (5.6,-.09)--(5.6,.09);
\draw[otNavy] (6.4,-.09)--(6.4,.09);
\node[font=\normalsize] at (6.4,-0.4) {$2\,800$};
\draw[otNavy] (7.2,-.09)--(7.2,.09);
\draw[otNavy] (8.0,-.09)--(8.0,.09);
\node[font=\normalsize] at (8.0,-0.4) {$3\,000$};
\node[font=\normalsize,text=otMuted] at (4,0.6) {Graduations régulièrement espacées};
\end{tikzpicture}
""",
    'ex1_enonce': r"""
\begin{tikzpicture}[x=1cm,y=1cm,font=\large,text=otInk,line width=0.8pt]
\draw[otNavy,->] (-.15,0)--(8.2,0);
\draw[otNavy] (0.0,-.09)--(0.0,.09);
\node[font=\normalsize] at (0.0,-0.4) {$3\,000$};
\draw[otNavy] (1.0,-.09)--(1.0,.09);
\node[font=\normalsize] at (1.0,-0.4) {$3\,100$};
\draw[otNavy] (2.0,-.09)--(2.0,.09);
\node[font=\normalsize] at (2.0,-0.4) {$?$};
\draw[otNavy] (3.0,-.09)--(3.0,.09);
\node[font=\normalsize] at (3.0,-0.4) {$3\,300$};
\draw[otNavy] (4.0,-.09)--(4.0,.09);
\node[font=\normalsize] at (4.0,-0.4) {$3\,400$};
\draw[otNavy] (5.0,-.09)--(5.0,.09);
\node[font=\normalsize] at (5.0,-0.4) {$?$};
\draw[otNavy] (6.0,-.09)--(6.0,.09);
\node[font=\normalsize] at (6.0,-0.4) {$3\,600$};
\draw[otNavy] (7.0,-.09)--(7.0,.09);
\node[font=\normalsize] at (7.0,-0.4) {$?$};
\draw[otNavy] (8.0,-.09)--(8.0,.09);
\node[font=\normalsize] at (8.0,-0.4) {$3\,800$};
\node[font=\normalsize,text=otMuted] at (4,0.6) {Graduations régulièrement espacées};
\end{tikzpicture}
""",
    'ex6_enonce': r"""
\begin{tikzpicture}[x=1cm,y=1cm,font=\large,text=otInk,line width=0.8pt]
\draw[otNavy,->] (-.15,0)--(8.2,0);
\draw[otNavy] (0.0,-.09)--(0.0,.09);
\node[font=\normalsize] at (0.0,-0.4) {$6\,000$};
\draw[otNavy] (0.8,-.09)--(0.8,.09);
\draw[otNavy] (1.6,-.09)--(1.6,.09);
\node[font=\normalsize] at (1.6,-0.4) {$6\,200$};
\draw[otNavy] (2.4,-.09)--(2.4,.09);
\draw[otNavy] (3.2,-.09)--(3.2,.09);
\node[font=\normalsize] at (3.2,-0.4) {$6\,400$};
\draw[otNavy] (4.0,-.09)--(4.0,.09);
\node[font=\normalsize] at (4.0,-0.95) {$6\,500$};
\fill[otGreenDark] (4.0,0) circle (3pt);
\draw[otNavy] (4.8,-.09)--(4.8,.09);
\node[font=\normalsize] at (4.8,-0.4) {$6\,600$};
\draw[otNavy] (5.6,-.09)--(5.6,.09);
\draw[otNavy] (6.4,-.09)--(6.4,.09);
\node[font=\normalsize] at (6.4,-0.4) {$6\,800$};
\draw[otNavy] (7.2,-.09)--(7.2,.09);
\draw[otNavy] (8.0,-.09)--(8.0,.09);
\node[font=\normalsize] at (8.0,-0.4) {$7\,000$};
\node[font=\normalsize,text=otMuted] at (4,0.6) {Graduations régulièrement espacées};
\end{tikzpicture}
""",
}
