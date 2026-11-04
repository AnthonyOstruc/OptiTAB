# -*- coding: utf-8 -*-
"""Figures TikZ ; préambule officiel fourni par figures_livre.py."""
FIGURES = {
    'cours_schema': r"""
\begin{tikzpicture}[x=1cm,y=1cm,font=\large,text=otInk,line width=.8pt]
\fill[otNavy!25] (0.0,0.0) rectangle (1.75,0.55);
\fill[white] (1.75,0.0) rectangle (3.5,0.55);
\fill[white] (3.5,0.0) rectangle (5.25,0.55);
\fill[white] (5.25,0.0) rectangle (7.0,0.55);
\draw[otNavy] (0,0.0) rectangle (7,0.55);
\draw[otNavy] (1.75,0.0) -- (1.75,0.55);
\draw[otNavy] (3.5,0.0) -- (3.5,0.55);
\draw[otNavy] (5.25,0.0) -- (5.25,0.55);
\node[text=otInk] at (3.5,-0.35) {Une part sur quatre parts égales};
\end{tikzpicture}
""",
    'ex1_schema': r"""
\begin{tikzpicture}[x=1cm,y=1cm,font=\large,text=otInk,line width=.8pt]
\fill[otNavy!25] (0.0,0.0) rectangle (1.4,0.55);
\fill[white] (1.4,0.0) rectangle (2.8,0.55);
\fill[white] (2.8,0.0) rectangle (4.2,0.55);
\fill[white] (4.2,0.0) rectangle (5.6,0.55);
\fill[white] (5.6,0.0) rectangle (7.0,0.55);
\draw[otNavy] (0,0.0) rectangle (7,0.55);
\draw[otNavy] (1.4,0.0) -- (1.4,0.55);
\draw[otNavy] (2.8,0.0) -- (2.8,0.55);
\draw[otNavy] (4.2,0.0) -- (4.2,0.55);
\draw[otNavy] (5.6,0.0) -- (5.6,0.55);
\node[text=otInk] at (3.5,-0.35) {Bande entière partagée en parts égales};
\end{tikzpicture}
""",
    'ex1_corrige': r"""
\begin{tikzpicture}[x=1cm,y=1cm,font=\large,text=otInk,line width=.8pt]
\fill[otGreen!35] (0.0,0.0) rectangle (1.4,0.55);
\fill[white] (1.4,0.0) rectangle (2.8,0.55);
\fill[white] (2.8,0.0) rectangle (4.2,0.55);
\fill[white] (4.2,0.0) rectangle (5.6,0.55);
\fill[white] (5.6,0.0) rectangle (7.0,0.55);
\draw[otNavy] (0,0.0) rectangle (7,0.55);
\draw[otNavy] (1.4,0.0) -- (1.4,0.55);
\draw[otNavy] (2.8,0.0) -- (2.8,0.55);
\draw[otNavy] (4.2,0.0) -- (4.2,0.55);
\draw[otNavy] (5.6,0.0) -- (5.6,0.55);
\node[text=otGreenDark] at (3.5,-0.35) {Un cinquième};
\end{tikzpicture}
""",
    'ex2_schema': r"""
\begin{tikzpicture}[x=1cm,y=1cm,font=\large,text=otInk,line width=.8pt]
\fill[white] (0.0,0.0) rectangle (7.0,0.55);
\draw[otNavy] (0,0.0) rectangle (7,0.55);
\node[text=otInk] at (3.5,-0.35) {Bande entière à partager};
\end{tikzpicture}
""",
    'ex2_corrige': r"""
\begin{tikzpicture}[x=1cm,y=1cm,font=\large,text=otInk,line width=.8pt]
\fill[otGreen!35] (0.0,0.0) rectangle (3.5,0.55);
\fill[white] (3.5,0.0) rectangle (7.0,0.55);
\draw[otNavy] (0,0.0) rectangle (7,0.55);
\draw[otNavy] (3.5,0.0) -- (3.5,0.55);
\node[text=otGreenDark] at (3.5,-0.35) {Un demi};
\end{tikzpicture}
""",
    'ex3_schema': r"""
\begin{tikzpicture}[x=1cm,y=1cm,font=\large,text=otInk,line width=.8pt]
\fill[white] (0.0,0.0) rectangle (2.3333333333333335,0.55);
\fill[white] (2.3333333333333335,0.0) rectangle (4.666666666666667,0.55);
\fill[white] (4.666666666666667,0.0) rectangle (7.0,0.55);
\draw[otNavy] (0,0.0) rectangle (7,0.55);
\draw[otNavy] (2.3333333333333335,0.0) -- (2.3333333333333335,0.55);
\draw[otNavy] (4.666666666666667,0.0) -- (4.666666666666667,0.55);
\node[text=otInk] at (3.5,-0.35) {Bande entière partagée en parts égales};
\end{tikzpicture}
""",
    'ex3_corrige': r"""
\begin{tikzpicture}[x=1cm,y=1cm,font=\large,text=otInk,line width=.8pt]
\fill[otGreen!35] (0.0,0.0) rectangle (2.3333333333333335,0.55);
\fill[white] (2.3333333333333335,0.0) rectangle (4.666666666666667,0.55);
\fill[white] (4.666666666666667,0.0) rectangle (7.0,0.55);
\draw[otNavy] (0,0.0) rectangle (7,0.55);
\draw[otNavy] (2.3333333333333335,0.0) -- (2.3333333333333335,0.55);
\draw[otNavy] (4.666666666666667,0.0) -- (4.666666666666667,0.55);
\node[text=otGreenDark] at (3.5,-0.35) {Un tiers};
\end{tikzpicture}
""",
    'ex6_schema': r"""
\begin{tikzpicture}[x=1cm,y=1cm,font=\large,text=otInk,line width=.8pt]
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
\node[text=otInk] at (3.5,-0.35) {Bande entière partagée en parts égales};
\end{tikzpicture}
""",
    'ex6_corrige': r"""
\begin{tikzpicture}[x=1cm,y=1cm,font=\large,text=otInk,line width=.8pt]
\fill[otGreen!35] (0.0,0.0) rectangle (1.1666666666666667,0.55);
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
\node[text=otGreenDark] at (3.5,-0.35) {Un sixième};
\end{tikzpicture}
""",
    'ex9_schema': r"""
\begin{tikzpicture}[x=1cm,y=1cm,font=\large,text=otInk,line width=.8pt]
\fill[white] (0.0,0.0) rectangle (0.875,0.55);
\fill[white] (0.875,0.0) rectangle (1.75,0.55);
\fill[white] (1.75,0.0) rectangle (2.625,0.55);
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
\node[text=otInk] at (3.5,-0.35) {Bande entière partagée en parts égales};
\end{tikzpicture}
""",
    'ex9_corrige': r"""
\begin{tikzpicture}[x=1cm,y=1cm,font=\large,text=otInk,line width=.8pt]
\fill[otGreen!35] (0.0,0.0) rectangle (0.875,0.55);
\fill[white] (0.875,0.0) rectangle (1.75,0.55);
\fill[white] (1.75,0.0) rectangle (2.625,0.55);
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
\node[text=otGreenDark] at (3.5,-0.35) {Un huitième};
\end{tikzpicture}
""",
    'ex7_schema': r"""
\begin{tikzpicture}[x=1cm,y=1cm,font=\large,text=otInk,line width=.8pt]
\fill[white] (0,0.0) rectangle (1,0.55);
\fill[white] (1,0.0) rectangle (2.5,0.55);
\fill[white] (2.5,0.0) rectangle (5,0.55);
\fill[white] (5,0.0) rectangle (7,0.55);
\draw[otNavy] (0,0.0) rectangle (7,0.55);
\draw[otNavy] (1,0.0) -- (1,0.55);
\draw[otNavy] (2.5,0.0) -- (2.5,0.55);
\draw[otNavy] (5,0.0) -- (5,0.55);
\node[text=otInk] at (3.5,-0.35) {Quatre morceaux inégaux};
\end{tikzpicture}
""",
    'ex7_corrige': r"""
\begin{tikzpicture}[x=1cm,y=1cm,font=\large,text=otInk,line width=.8pt]
\fill[otGreen!35] (0.0,0.0) rectangle (1.75,0.55);
\fill[white] (1.75,0.0) rectangle (3.5,0.55);
\fill[white] (3.5,0.0) rectangle (5.25,0.55);
\fill[white] (5.25,0.0) rectangle (7.0,0.55);
\draw[otNavy] (0,0.0) rectangle (7,0.55);
\draw[otNavy] (1.75,0.0) -- (1.75,0.55);
\draw[otNavy] (3.5,0.0) -- (3.5,0.55);
\draw[otNavy] (5.25,0.0) -- (5.25,0.55);
\node[text=otGreenDark] at (3.5,-0.35) {Un quart : une part sur quatre parts égales};
\end{tikzpicture}
""",
}
