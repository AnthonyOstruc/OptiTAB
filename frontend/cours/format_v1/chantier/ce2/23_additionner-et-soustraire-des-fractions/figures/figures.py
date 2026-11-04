# -*- coding: utf-8 -*-
"""Figures TikZ ; pr?ambule officiel fourni par outils/figures_livre.py."""
FIGURES = {
    'cours_schema': r"""
\begin{tikzpicture}[x=1cm,y=1cm,font=\large,text=otInk,line width=0.8pt]
\fill[otNavy!18] (0.0000,1.1) rectangle (1.6000,1.58);
\fill[otNavy!18] (1.6000,1.1) rectangle (3.2000,1.58);
\fill[white] (3.2000,1.1) rectangle (4.8000,1.58);
\fill[white] (4.8000,1.1) rectangle (6.4000,1.58);
\draw[otNavy] (0,1.1) rectangle (6.4,1.58);
\draw[otNavy] (1.6000,1.1) -- (1.6000,1.58);
\draw[otNavy] (3.2000,1.1) -- (3.2000,1.58);
\draw[otNavy] (4.8000,1.1) -- (4.8000,1.58);
\node[] at (7.05,1.34) {$\dfrac{2}{4}$};
\fill[otOrange!35] (0.0000,0) rectangle (1.6000,0.48);
\fill[white] (1.6000,0) rectangle (3.2000,0.48);
\fill[white] (3.2000,0) rectangle (4.8000,0.48);
\fill[white] (4.8000,0) rectangle (6.4000,0.48);
\draw[otNavy] (0,0) rectangle (6.4,0.48);
\draw[otNavy] (1.6000,0) -- (1.6000,0.48);
\draw[otNavy] (3.2000,0) -- (3.2000,0.48);
\draw[otNavy] (4.8000,0) -- (4.8000,0.48);
\node[] at (7.05,0.24) {$\dfrac{1}{4}$};
\node[font=\normalsize,text=otNavy] at (3.2,2.15) {Même unité, mêmes parts};
\end{tikzpicture}
""",
}
