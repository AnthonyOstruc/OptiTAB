# -*- coding: utf-8 -*-
"""Figures TikZ ; préambule officiel fourni par figures_livre.py."""
FIGURES = {
    'cours_schema': r"""
\begin{tikzpicture}[x=1cm,y=1cm,font=\large,text=otInk,line width=.8pt]
\draw[otNavy,fill=otSky] (0,1.4) rectangle (7,1.95);
\node[text=otInk] at (3.5,2.35) {Tout : 245};
\draw[otNavy,fill=otSky] (0,0) rectangle (3.657142857142857,.55);
\draw[otNavy,fill=white] (3.657142857142857,0) rectangle (7,.55);
\node[text=otInk] at (1.8285714285714285,-0.4) {128};
\node[text=otInk] at (5.328571428571428,-0.4) {?};
\end{tikzpicture}
""",
    'ex1_schema': r"""
\begin{tikzpicture}[x=1cm,y=1cm,font=\large,text=otInk,line width=.8pt]
\draw[otNavy,fill=otSky] (0,1.4) rectangle (7,1.95);
\node[text=otInk] at (3.5,2.35) {Tout : 360};
\draw[otNavy,fill=otSky] (0,0) rectangle (2.8194444444444446,.55);
\draw[otNavy,fill=white] (2.8194444444444446,0) rectangle (7,.55);
\node[text=otInk] at (1.4097222222222223,-0.4) {145};
\node[text=otInk] at (4.909722222222222,-0.4) {?};
\end{tikzpicture}
""",
    'ex1_corrige': r"""
\begin{tikzpicture}[x=1cm,y=1cm,font=\large,text=otInk,line width=.8pt]
\draw[otNavy,fill=otSky] (0,1.4) rectangle (7,1.95);
\node[text=otInk] at (3.5,2.35) {Tout : 360};
\draw[otNavy,fill=otSky] (0,0) rectangle (2.8194444444444446,.55);
\draw[otNavy,fill=otGreen!25] (2.8194444444444446,0) rectangle (7,.55);
\node[text=otInk] at (1.4097222222222223,-0.4) {145};
\node[text=otGreenDark] at (4.909722222222222,-0.4) {215};
\end{tikzpicture}
""",
}
