# -*- coding: utf-8 -*-
"""Figures TikZ ; préambule officiel fourni par figures_livre.py."""
FIGURES = {
    'cours_schema': r"""
\begin{tikzpicture}[x=1cm,y=1cm,font=\large,text=otInk,line width=.8pt]
\draw[otNavy,fill=otSky] (0.0,2.5) rectangle (0.75,3.15);
\draw[otNavy,fill=otSky] (1.05,2.5) rectangle (1.8,3.15);
\node[text=otInk] at (6,2.7) {2 centaines};
\draw[otNavy,fill=otSky] (0.0,1.3) rectangle (0.3,1.8);
\draw[otNavy,fill=otSky] (0.55,1.3) rectangle (0.8500000000000001,1.8);
\draw[otNavy,fill=otSky] (1.1,1.3) rectangle (1.4000000000000001,1.8);
\node[text=otInk] at (6,1.5) {3 dizaines};
\draw[otNavy,fill=otSky] (0.0,0.3) rectangle (0.2,0.5);
\draw[otNavy,fill=otSky] (0.42,0.3) rectangle (0.62,0.5);
\draw[otNavy,fill=otSky] (0.84,0.3) rectangle (1.04,0.5);
\draw[otNavy,fill=otSky] (1.26,0.3) rectangle (1.46,0.5);
\node[text=otInk] at (6,0.5) {4 unités};
\end{tikzpicture}
""",
    'ex1_schema': r"""
\begin{tikzpicture}[x=1cm,y=1cm,font=\large,text=otInk,line width=.8pt]
\draw[otNavy,fill=otSky] (0.0,2.5) rectangle (0.75,3.15);
\draw[otNavy,fill=otSky] (1.05,2.5) rectangle (1.8,3.15);
\draw[otNavy,fill=otSky] (2.1,2.5) rectangle (2.85,3.15);
\node[text=otInk] at (6,2.7) {3 centaines};
\draw[otNavy,fill=otSky] (0.0,1.3) rectangle (0.3,1.8);
\draw[otNavy,fill=otSky] (0.55,1.3) rectangle (0.8500000000000001,1.8);
\node[text=otInk] at (6,1.5) {2 dizaines};
\draw[otNavy,fill=otSky] (0.0,0.3) rectangle (0.2,0.5);
\draw[otNavy,fill=otSky] (0.42,0.3) rectangle (0.62,0.5);
\draw[otNavy,fill=otSky] (0.84,0.3) rectangle (1.04,0.5);
\draw[otNavy,fill=otSky] (1.26,0.3) rectangle (1.46,0.5);
\draw[otNavy,fill=otSky] (1.68,0.3) rectangle (1.88,0.5);
\node[text=otInk] at (6,0.5) {5 unités};
\end{tikzpicture}
""",
}
