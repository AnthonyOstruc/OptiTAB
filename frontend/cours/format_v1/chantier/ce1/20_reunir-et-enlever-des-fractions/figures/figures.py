# -*- coding: utf-8 -*-
"""Figures TikZ ; préambule officiel fourni par figures_livre.py."""
FIGURES = {
    'cours_schema': r"""
\begin{tikzpicture}[x=1cm,y=1cm,font=\large,text=otInk,line width=.8pt]
\fill[otNavy!25] (0.0,3.1) rectangle (1.4,3.6500000000000004);
\fill[otNavy!25] (1.4,3.1) rectangle (2.8,3.6500000000000004);
\fill[white] (2.8,3.1) rectangle (4.2,3.6500000000000004);
\fill[white] (4.2,3.1) rectangle (5.6,3.6500000000000004);
\fill[white] (5.6,3.1) rectangle (7.0,3.6500000000000004);
\draw[otNavy] (0,3.1) rectangle (7,3.6500000000000004);
\draw[otNavy] (1.4,3.1) -- (1.4,3.6500000000000004);
\draw[otNavy] (2.8,3.1) -- (2.8,3.6500000000000004);
\draw[otNavy] (4.2,3.1) -- (4.2,3.6500000000000004);
\draw[otNavy] (5.6,3.1) -- (5.6,3.6500000000000004);
\node[text=otInk] at (3.5,2.75) {Deux cinquièmes};
\fill[otNavy!25] (0.0,1.55) rectangle (1.4,2.1);
\fill[white] (1.4,1.55) rectangle (2.8,2.1);
\fill[white] (2.8,1.55) rectangle (4.2,2.1);
\fill[white] (4.2,1.55) rectangle (5.6,2.1);
\fill[white] (5.6,1.55) rectangle (7.0,2.1);
\draw[otNavy] (0,1.55) rectangle (7,2.1);
\draw[otNavy] (1.4,1.55) -- (1.4,2.1);
\draw[otNavy] (2.8,1.55) -- (2.8,2.1);
\draw[otNavy] (4.2,1.55) -- (4.2,2.1);
\draw[otNavy] (5.6,1.55) -- (5.6,2.1);
\node[text=otInk] at (3.5,1.2000000000000002) {Un cinquième};
\fill[otNavy!25] (0.0,0.0) rectangle (1.4,0.55);
\fill[otNavy!25] (1.4,0.0) rectangle (2.8,0.55);
\fill[otNavy!25] (2.8,0.0) rectangle (4.2,0.55);
\fill[white] (4.2,0.0) rectangle (5.6,0.55);
\fill[white] (5.6,0.0) rectangle (7.0,0.55);
\draw[otNavy] (0,0.0) rectangle (7,0.55);
\draw[otNavy] (1.4,0.0) -- (1.4,0.55);
\draw[otNavy] (2.8,0.0) -- (2.8,0.55);
\draw[otNavy] (4.2,0.0) -- (4.2,0.55);
\draw[otNavy] (5.6,0.0) -- (5.6,0.55);
\node[text=otInk] at (3.5,-0.35) {Trois cinquièmes réunis};
\end{tikzpicture}
""",
    'ex1_schema': r"""
\begin{tikzpicture}[x=1cm,y=1cm,font=\large,text=otInk,line width=.8pt]
\fill[otNavy!25] (0.0,1.55) rectangle (1.1666666666666667,2.1);
\fill[white] (1.1666666666666667,1.55) rectangle (2.3333333333333335,2.1);
\fill[white] (2.3333333333333335,1.55) rectangle (3.5,2.1);
\fill[white] (3.5,1.55) rectangle (4.666666666666667,2.1);
\fill[white] (4.666666666666667,1.55) rectangle (5.833333333333333,2.1);
\fill[white] (5.833333333333333,1.55) rectangle (7.0,2.1);
\draw[otNavy] (0,1.55) rectangle (7,2.1);
\draw[otNavy] (1.1666666666666667,1.55) -- (1.1666666666666667,2.1);
\draw[otNavy] (2.3333333333333335,1.55) -- (2.3333333333333335,2.1);
\draw[otNavy] (3.5,1.55) -- (3.5,2.1);
\draw[otNavy] (4.666666666666667,1.55) -- (4.666666666666667,2.1);
\draw[otNavy] (5.833333333333333,1.55) -- (5.833333333333333,2.1);
\node[text=otInk] at (3.5,1.2000000000000002) {Une part choisie};
\fill[otNavy!25] (0.0,0.0) rectangle (1.1666666666666667,0.55);
\fill[otNavy!25] (1.1666666666666667,0.0) rectangle (2.3333333333333335,0.55);
\fill[otNavy!25] (2.3333333333333335,0.0) rectangle (3.5,0.55);
\fill[white] (3.5,0.0) rectangle (4.666666666666667,0.55);
\fill[white] (4.666666666666667,0.0) rectangle (5.833333333333333,0.55);
\fill[white] (5.833333333333333,0.0) rectangle (7.0,0.55);
\draw[otNavy] (0,0.0) rectangle (7,0.55);
\draw[otNavy] (1.1666666666666667,0.0) -- (1.1666666666666667,0.55);
\draw[otNavy] (2.3333333333333335,0.0) -- (2.3333333333333335,0.55);
\draw[otNavy] (3.5,0.0) -- (3.5,0.55);
\draw[otNavy] (4.666666666666667,0.0) -- (4.666666666666667,0.55);
\draw[otNavy] (5.833333333333333,0.0) -- (5.833333333333333,0.55);
\node[text=otInk] at (3.5,-0.35) {Trois autres parts choisies};
\end{tikzpicture}
""",
    'ex1_corrige': r"""
\begin{tikzpicture}[x=1cm,y=1cm,font=\large,text=otInk,line width=.8pt]
\fill[otGreen!35] (0.0,0.0) rectangle (1.1666666666666667,0.55);
\fill[otGreen!35] (1.1666666666666667,0.0) rectangle (2.3333333333333335,0.55);
\fill[otGreen!35] (2.3333333333333335,0.0) rectangle (3.5,0.55);
\fill[otGreen!35] (3.5,0.0) rectangle (4.666666666666667,0.55);
\fill[white] (4.666666666666667,0.0) rectangle (5.833333333333333,0.55);
\fill[white] (5.833333333333333,0.0) rectangle (7.0,0.55);
\draw[otNavy] (0,0.0) rectangle (7,0.55);
\draw[otNavy] (1.1666666666666667,0.0) -- (1.1666666666666667,0.55);
\draw[otNavy] (2.3333333333333335,0.0) -- (2.3333333333333335,0.55);
\draw[otNavy] (3.5,0.0) -- (3.5,0.55);
\draw[otNavy] (4.666666666666667,0.0) -- (4.666666666666667,0.55);
\draw[otNavy] (5.833333333333333,0.0) -- (5.833333333333333,0.55);
\node[text=otGreenDark] at (3.5,-0.35) {Quatre sixièmes};
\end{tikzpicture}
""",
    'ex6_schema': r"""
\begin{tikzpicture}[x=1cm,y=1cm,font=\large,text=otInk,line width=.8pt]
\fill[white] (0.0,0.0) rectangle (0.7,0.55);
\fill[white] (0.7,0.0) rectangle (1.4,0.55);
\fill[white] (1.4,0.0) rectangle (2.1,0.55);
\fill[white] (2.1,0.0) rectangle (2.8,0.55);
\fill[white] (2.8,0.0) rectangle (3.5,0.55);
\fill[white] (3.5,0.0) rectangle (4.2,0.55);
\fill[white] (4.2,0.0) rectangle (4.9,0.55);
\fill[white] (4.9,0.0) rectangle (5.6,0.55);
\fill[white] (5.6,0.0) rectangle (6.3,0.55);
\fill[white] (6.3,0.0) rectangle (7.0,0.55);
\draw[otNavy] (0,0.0) rectangle (7,0.55);
\draw[otNavy] (0.7,0.0) -- (0.7,0.55);
\draw[otNavy] (1.4,0.0) -- (1.4,0.55);
\draw[otNavy] (2.1,0.0) -- (2.1,0.55);
\draw[otNavy] (2.8,0.0) -- (2.8,0.55);
\draw[otNavy] (3.5,0.0) -- (3.5,0.55);
\draw[otNavy] (4.2,0.0) -- (4.2,0.55);
\draw[otNavy] (4.9,0.0) -- (4.9,0.55);
\draw[otNavy] (5.6,0.0) -- (5.6,0.55);
\draw[otNavy] (6.3,0.0) -- (6.3,0.55);
\node[text=otInk] at (3.5,-0.35) {Dix parts égales à colorier};
\end{tikzpicture}
""",
    'ex6_corrige': r"""
\begin{tikzpicture}[x=1cm,y=1cm,font=\large,text=otInk,line width=.8pt]
\fill[otGreen!35] (0.0,0.0) rectangle (0.7,0.55);
\fill[otGreen!35] (0.7,0.0) rectangle (1.4,0.55);
\fill[otGreen!35] (1.4,0.0) rectangle (2.1,0.55);
\fill[otGreen!35] (2.1,0.0) rectangle (2.8,0.55);
\fill[otGreen!35] (2.8,0.0) rectangle (3.5,0.55);
\fill[otGreen!35] (3.5,0.0) rectangle (4.2,0.55);
\fill[otGreen!35] (4.2,0.0) rectangle (4.9,0.55);
\fill[white] (4.9,0.0) rectangle (5.6,0.55);
\fill[white] (5.6,0.0) rectangle (6.3,0.55);
\fill[white] (6.3,0.0) rectangle (7.0,0.55);
\draw[otNavy] (0,0.0) rectangle (7,0.55);
\draw[otNavy] (0.7,0.0) -- (0.7,0.55);
\draw[otNavy] (1.4,0.0) -- (1.4,0.55);
\draw[otNavy] (2.1,0.0) -- (2.1,0.55);
\draw[otNavy] (2.8,0.0) -- (2.8,0.55);
\draw[otNavy] (3.5,0.0) -- (3.5,0.55);
\draw[otNavy] (4.2,0.0) -- (4.2,0.55);
\draw[otNavy] (4.9,0.0) -- (4.9,0.55);
\draw[otNavy] (5.6,0.0) -- (5.6,0.55);
\draw[otNavy] (6.3,0.0) -- (6.3,0.55);
\node[text=otGreenDark] at (3.5,-0.35) {Sept dixièmes coloriés};
\end{tikzpicture}
""",
}
