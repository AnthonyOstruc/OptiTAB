# -*- coding: utf-8 -*-
"""Figures TikZ ; pr?ambule officiel fourni par outils/figures_livre.py."""
FIGURES = {
    'cours_schema': r"""
\begin{tikzpicture}[x=1cm,y=1cm,font=\large,text=otInk,line width=0.8pt]
\draw[otNavy,fill=otSky] (0,1.3) rectangle (2.5,1.85);
\node[] at (1.25,1.575) {24 €};
\draw[otNavy,fill=otGreen!20] (0.0,0) rectangle (2.5,.55);
\node[] at (1.25,0.275) {24 €};
\draw[otNavy,fill=otGreen!20] (2.5,0) rectangle (5.0,.55);
\node[] at (3.75,0.275) {24 €};
\draw[otNavy,fill=otGreen!20] (5.0,0) rectangle (7.5,.55);
\node[] at (6.25,0.275) {24 €};
\node[font=\normalsize,text=otGreenDark] at (3.75,-0.6) {3 fois la même quantité};
\end{tikzpicture}
""",
    'ex1_schema': r"""
\begin{tikzpicture}[x=1cm,y=1cm,font=\large,text=otInk,line width=0.8pt]
\draw[otNavy,fill=otSky] (0,1.3) rectangle (2.5,1.85);
\node[] at (1.25,1.575) {7 billes};
\draw[otNavy,fill=otGreen!20] (0.0,0) rectangle (2.5,.55);
\node[] at (1.25,0.275) {7 billes};
\draw[otNavy,fill=otGreen!20] (2.5,0) rectangle (5.0,.55);
\node[] at (3.75,0.275) {7 billes};
\draw[otNavy,fill=otGreen!20] (5.0,0) rectangle (7.5,.55);
\node[] at (6.25,0.275) {7 billes};
\node[font=\normalsize,text=otGreenDark] at (3.75,-0.6) {3 fois la même quantité};
\end{tikzpicture}
""",
    'ex5_schema': r"""
\begin{tikzpicture}[x=1cm,y=1cm,font=\large,text=otInk,line width=0.8pt]
\draw[otNavy,fill=otSky] (0,1.3) rectangle (2.5,1.85);
\node[] at (1.25,1.575) {12 images};
\draw[otNavy,fill=otGreen!20] (0.0,0) rectangle (2.5,.55);
\node[] at (1.25,0.275) {12 images};
\draw[otNavy,fill=otGreen!20] (2.5,0) rectangle (5.0,.55);
\node[] at (3.75,0.275) {12 images};
\draw[otNavy,fill=otGreen!20] (5.0,0) rectangle (7.5,.55);
\node[] at (6.25,0.275) {12 images};
\node[font=\normalsize,text=otGreenDark] at (3.75,-0.6) {3 fois la même quantité};
\end{tikzpicture}
""",
    'ex9_schema': r"""
\begin{tikzpicture}[x=1cm,y=1cm,font=\large,text=otInk,line width=0.8pt]
\draw[otNavy,fill=otSky] (0,1.3) rectangle (1.875,1.85);
\node[] at (0.9375,1.575) {8 billes};
\draw[otNavy,fill=otGreen!20] (0.0,0) rectangle (1.875,.55);
\node[] at (0.9375,0.275) {8 billes};
\draw[otNavy,fill=otGreen!20] (1.875,0) rectangle (3.75,.55);
\node[] at (2.8125,0.275) {8 billes};
\draw[otNavy,fill=otGreen!20] (3.75,0) rectangle (5.625,.55);
\node[] at (4.6875,0.275) {8 billes};
\draw[otNavy,fill=otGreen!20] (5.625,0) rectangle (7.5,.55);
\node[] at (6.5625,0.275) {8 billes};
\node[font=\normalsize,text=otGreenDark] at (3.75,-0.6) {4 fois la même quantité};
\end{tikzpicture}
""",
}
