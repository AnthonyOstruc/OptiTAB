# -*- coding: utf-8 -*-
"""Figures TikZ ; préambule officiel fourni par figures_livre.py."""
FIGURES = {
    'cours_schema': r"""
\begin{tikzpicture}[x=1cm,y=1cm,font=\large,text=otInk,line width=.8pt]
\node[text=otInk] at (0,0) {83};
\draw[otNavy,-{Stealth}] (.65,0) -- (2.5,0);
\node[text=otInk] at (1.6,0.55) {+25};
\node[text=otGreenDark] at (3.2,0) {108};
\draw[otNavy,-{Stealth}] (3.85,0) -- (5.7,0);
\node[text=otInk] at (4.75,0.55) {-46};
\node[text=otGreenDark] at (6.5,0) {62};
\end{tikzpicture}
""",
    'ex1_schema': r"""
\begin{tikzpicture}[x=1cm,y=1cm,font=\large,text=otInk,line width=.8pt]
\node[text=otInk] at (0,0) {125};
\draw[otNavy,-{Stealth}] (.65,0) -- (2.5,0);
\node[text=otInk] at (1.6,0.55) {+38};
\node[text=otInk] at (3.2,0) {?};
\draw[otNavy,-{Stealth}] (3.85,0) -- (5.7,0);
\node[text=otInk] at (4.75,0.55) {-47};
\node[text=otInk] at (6.5,0) {?};
\end{tikzpicture}
""",
    'ex1_corrige': r"""
\begin{tikzpicture}[x=1cm,y=1cm,font=\large,text=otInk,line width=.8pt]
\node[text=otInk] at (0,0) {125};
\draw[otNavy,-{Stealth}] (.65,0) -- (2.5,0);
\node[text=otInk] at (1.6,0.55) {+38};
\node[text=otGreenDark] at (3.2,0) {163};
\draw[otNavy,-{Stealth}] (3.85,0) -- (5.7,0);
\node[text=otInk] at (4.75,0.55) {-47};
\node[text=otGreenDark] at (6.5,0) {116};
\end{tikzpicture}
""",
}
