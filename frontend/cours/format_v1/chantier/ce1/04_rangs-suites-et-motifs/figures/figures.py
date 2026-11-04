# -*- coding: utf-8 -*-
"""Figures TikZ ; préambule officiel fourni par figures_livre.py."""
FIGURES = {
    'cours_schema': r"""
\begin{tikzpicture}[x=1cm,y=1cm,font=\large,text=otInk,line width=.8pt]
\node[text=otInk] at (0.0,0) {A};
\node[text=otInk] at (0.75,0) {B};
\node[text=otInk] at (1.5,0) {C};
\node[text=otInk] at (2.25,0) {A};
\node[text=otInk] at (3.0,0) {B};
\node[text=otInk] at (3.75,0) {C};
\node[text=otMuted,font=\normalsize] at (2.6,-0.65) {Départ à gauche ; rangs à partir de 1};
\end{tikzpicture}
""",
    'ex1_schema': r"""
\begin{tikzpicture}[x=1cm,y=1cm,font=\large,text=otInk,line width=.8pt]
\node[text=otInk] at (0.0,0) {A};
\node[text=otInk] at (0.75,0) {B};
\node[text=otInk] at (1.5,0) {A};
\node[text=otInk] at (2.25,0) {B};
\node[text=otInk] at (3.0,0) {A};
\node[text=otInk] at (3.75,0) {B};
\node[text=otMuted,font=\normalsize] at (2.6,-0.65) {Départ à gauche ; rangs à partir de 1};
\end{tikzpicture}
""",
    'ex4_schema': r"""
\begin{tikzpicture}[x=1cm,y=1cm,font=\large,text=otInk,line width=.8pt]
\node[text=otInk] at (0.0,0) {A};
\node[text=otInk] at (0.75,0) {B};
\node[text=otInk] at (1.5,0) {C};
\node[text=otInk] at (2.25,0) {A};
\node[text=otInk] at (3.0,0) {B};
\node[text=otInk] at (3.75,0) {C};
\node[text=otMuted,font=\normalsize] at (2.6,-0.65) {Départ à gauche ; rangs à partir de 1};
\end{tikzpicture}
""",
}
