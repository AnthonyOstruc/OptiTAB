# -*- coding: utf-8 -*-
"""Figures TikZ ; préambule officiel fourni par figures_livre.py."""
FIGURES = {
    'cours_schema': r"""
\begin{tikzpicture}[x=1cm,y=1cm,font=\large,text=otInk,line width=.8pt]
\fill[otNavy!25] (0.0,1.55) rectangle (1.4,2.1);
\fill[otNavy!25] (1.4,1.55) rectangle (2.8,2.1);
\fill[white] (2.8,1.55) rectangle (4.2,2.1);
\fill[white] (4.2,1.55) rectangle (5.6,2.1);
\fill[white] (5.6,1.55) rectangle (7.0,2.1);
\draw[otNavy] (0,1.55) rectangle (7,2.1);
\draw[otNavy] (1.4,1.55) -- (1.4,2.1);
\draw[otNavy] (2.8,1.55) -- (2.8,2.1);
\draw[otNavy] (4.2,1.55) -- (4.2,2.1);
\draw[otNavy] (5.6,1.55) -- (5.6,2.1);
\node[text=otInk] at (3.5,1.2000000000000002) {Deux cinquièmes};
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
\node[text=otInk] at (3.5,-0.35) {Trois cinquièmes};
\end{tikzpicture}
""",
    'ex1_schema': r"""
\begin{tikzpicture}[x=1cm,y=1cm,font=\large,text=otInk,line width=.8pt]
\fill[otNavy!25] (0.0,0.0) rectangle (0.875,0.55);
\fill[otNavy!25] (0.875,0.0) rectangle (1.75,0.55);
\fill[otNavy!25] (1.75,0.0) rectangle (2.625,0.55);
\fill[white] (2.625,0.0) rectangle (3.5,0.55);
\fill[white] (3.5,0.0) rectangle (4.375,0.55);
\fill[white] (4.375,0.0) rectangle (5.25,0.55);
\fill[white] (5.25,0.0) rectangle (6.125,0.55);
\fill[white] (6.125,0.0) rectangle (7.0,0.55);
\draw[otNavy] (0,0.0) rectangle (7,0.55);
\draw[otNavy] (0.875,0.0) -- (0.875,0.55);
\draw[otNavy] (1.75,0.0) -- (1.75,0.55);
\draw[otNavy] (2.625,0.0) -- (2.625,0.55);
\draw[otNavy] (3.5,0.0) -- (3.5,0.55);
\draw[otNavy] (4.375,0.0) -- (4.375,0.55);
\draw[otNavy] (5.25,0.0) -- (5.25,0.55);
\draw[otNavy] (6.125,0.0) -- (6.125,0.55);
\node[text=otInk] at (3.5,-0.35) {Bande entière en parts égales};
\end{tikzpicture}
""",
    'ex1_corrige': r"""
\begin{tikzpicture}[x=1cm,y=1cm,font=\large,text=otInk,line width=.8pt]
\fill[otGreen!35] (0.0,0.0) rectangle (0.875,0.55);
\fill[otGreen!35] (0.875,0.0) rectangle (1.75,0.55);
\fill[otGreen!35] (1.75,0.0) rectangle (2.625,0.55);
\fill[white] (2.625,0.0) rectangle (3.5,0.55);
\fill[white] (3.5,0.0) rectangle (4.375,0.55);
\fill[white] (4.375,0.0) rectangle (5.25,0.55);
\fill[white] (5.25,0.0) rectangle (6.125,0.55);
\fill[white] (6.125,0.0) rectangle (7.0,0.55);
\draw[otNavy] (0,0.0) rectangle (7,0.55);
\draw[otNavy] (0.875,0.0) -- (0.875,0.55);
\draw[otNavy] (1.75,0.0) -- (1.75,0.55);
\draw[otNavy] (2.625,0.0) -- (2.625,0.55);
\draw[otNavy] (3.5,0.0) -- (3.5,0.55);
\draw[otNavy] (4.375,0.0) -- (4.375,0.55);
\draw[otNavy] (5.25,0.0) -- (5.25,0.55);
\draw[otNavy] (6.125,0.0) -- (6.125,0.55);
\node[text=otGreenDark] at (3.5,-0.35) {$\frac{3}{8}$};
\end{tikzpicture}
""",
    'ex2_schema': r"""
\begin{tikzpicture}[x=1cm,y=1cm,font=\large,text=otInk,line width=.8pt]
\fill[white] (0.0,0.0) rectangle (1.75,0.55);
\fill[white] (1.75,0.0) rectangle (3.5,0.55);
\fill[white] (3.5,0.0) rectangle (5.25,0.55);
\fill[white] (5.25,0.0) rectangle (7.0,0.55);
\draw[otNavy] (0,0.0) rectangle (7,0.55);
\draw[otNavy] (1.75,0.0) -- (1.75,0.55);
\draw[otNavy] (3.5,0.0) -- (3.5,0.55);
\draw[otNavy] (5.25,0.0) -- (5.25,0.55);
\node[text=otInk] at (3.5,-0.35) {Bande entière en parts égales};
\end{tikzpicture}
""",
    'ex2_corrige': r"""
\begin{tikzpicture}[x=1cm,y=1cm,font=\large,text=otInk,line width=.8pt]
\fill[otGreen!35] (0.0,0.0) rectangle (1.75,0.55);
\fill[otGreen!35] (1.75,0.0) rectangle (3.5,0.55);
\fill[otGreen!35] (3.5,0.0) rectangle (5.25,0.55);
\fill[white] (5.25,0.0) rectangle (7.0,0.55);
\draw[otNavy] (0,0.0) rectangle (7,0.55);
\draw[otNavy] (1.75,0.0) -- (1.75,0.55);
\draw[otNavy] (3.5,0.0) -- (3.5,0.55);
\draw[otNavy] (5.25,0.0) -- (5.25,0.55);
\node[text=otGreenDark] at (3.5,-0.35) {$\frac{3}{4}$};
\end{tikzpicture}
""",
    'ex4_schema': r"""
\begin{tikzpicture}[x=1cm,y=1cm,font=\large,text=otInk,line width=.8pt]
\fill[otNavy!25] (0.0,1.55) rectangle (2.3333333333333335,2.1);
\fill[white] (2.3333333333333335,1.55) rectangle (4.666666666666667,2.1);
\fill[white] (4.666666666666667,1.55) rectangle (7.0,2.1);
\draw[otNavy] (0,1.55) rectangle (7,2.1);
\draw[otNavy] (2.3333333333333335,1.55) -- (2.3333333333333335,2.1);
\draw[otNavy] (4.666666666666667,1.55) -- (4.666666666666667,2.1);
\node[text=otInk] at (3.5,1.2000000000000002) {Un tiers};
\fill[otNavy!25] (0.0,0.0) rectangle (1.1666666666666667,0.55);
\fill[white] (1.1666666666666667,0.0) rectangle (2.3333333333333335,0.55);
\fill[white] (2.3333333333333335,0.0) rectangle (3.5,0.55);
\fill[white] (3.5,0.0) rectangle (4.666666666666667,0.55);
\fill[white] (4.666666666666667,0.0) rectangle (5.833333333333333,0.55);
\fill[white] (5.833333333333333,0.0) rectangle (7.0,0.55);
\draw[otNavy] (0,0.0) rectangle (7,0.55);
\draw[otNavy] (1.1666666666666667,0.0) -- (1.1666666666666667,0.55);
\draw[otNavy] (2.3333333333333335,0.0) -- (2.3333333333333335,0.55);
\draw[otNavy] (3.5,0.0) -- (3.5,0.55);
\draw[otNavy] (4.666666666666667,0.0) -- (4.666666666666667,0.55);
\draw[otNavy] (5.833333333333333,0.0) -- (5.833333333333333,0.55);
\node[text=otInk] at (3.5,-0.35) {Un sixième};
\end{tikzpicture}
""",
    'ex8_schema': r"""
\begin{tikzpicture}[x=1cm,y=1cm,font=\large,text=otInk,line width=.8pt]
\fill[otNavy!25] (0.0,1.55) rectangle (2.0,2.1);
\fill[white] (2.0,1.55) rectangle (4.0,2.1);
\draw[otNavy] (0,1.55) rectangle (4,2.1);
\draw[otNavy] (2.0,1.55) -- (2.0,2.1);
\node[text=otInk] at (2.0,1.2000000000000002) {Moitié de la petite bande};
\fill[otNavy!25] (0.0,0.0) rectangle (3.5,0.55);
\fill[white] (3.5,0.0) rectangle (7.0,0.55);
\draw[otNavy] (0,0.0) rectangle (7,0.55);
\draw[otNavy] (3.5,0.0) -- (3.5,0.55);
\node[text=otInk] at (3.5,-0.35) {Moitié de la grande bande};
\end{tikzpicture}
""",
    'ex9_schema': r"""
\begin{tikzpicture}[x=1cm,y=1cm,font=\large,text=otInk,line width=.8pt]
\fill[otNavy!25] (0.0,1.55) rectangle (1.75,2.1);
\fill[otNavy!25] (1.75,1.55) rectangle (3.5,2.1);
\fill[white] (3.5,1.55) rectangle (5.25,2.1);
\fill[white] (5.25,1.55) rectangle (7.0,2.1);
\draw[otNavy] (0,1.55) rectangle (7,2.1);
\draw[otNavy] (1.75,1.55) -- (1.75,2.1);
\draw[otNavy] (3.5,1.55) -- (3.5,2.1);
\draw[otNavy] (5.25,1.55) -- (5.25,2.1);
\node[text=otInk] at (3.5,1.2000000000000002) {Deux quarts};
\fill[otNavy!25] (0.0,0.0) rectangle (3.5,0.55);
\fill[white] (3.5,0.0) rectangle (7.0,0.55);
\draw[otNavy] (0,0.0) rectangle (7,0.55);
\draw[otNavy] (3.5,0.0) -- (3.5,0.55);
\node[text=otInk] at (3.5,-0.35) {Une moitié};
\end{tikzpicture}
""",
}
