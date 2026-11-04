# -*- coding: utf-8 -*-
"""Figures TikZ ; pr?ambule officiel fourni par outils/figures_livre.py."""
FIGURES = {
    'cours_schema': r"""
\begin{tikzpicture}[x=1cm,y=1cm,font=\large,text=otInk,line width=0.8pt]
\fill[otGreen!30] (0.0000,1.1) rectangle (1.6000,1.58);
\fill[otGreen!30] (1.6000,1.1) rectangle (3.2000,1.58);
\fill[otGreen!30] (3.2000,1.1) rectangle (4.8000,1.58);
\fill[white] (4.8000,1.1) rectangle (6.4000,1.58);
\draw[otNavy] (0,1.1) rectangle (6.4,1.58);
\draw[otNavy] (1.6000,1.1) -- (1.6000,1.58);
\draw[otNavy] (3.2000,1.1) -- (3.2000,1.58);
\draw[otNavy] (4.8000,1.1) -- (4.8000,1.58);
\node[] at (7.05,1.34) {$\dfrac{3}{4}$};
\fill[otGreen!30] (0.0000,0.0) rectangle (0.8000,0.48);
\fill[otGreen!30] (0.8000,0.0) rectangle (1.6000,0.48);
\fill[otGreen!30] (1.6000,0.0) rectangle (2.4000,0.48);
\fill[otGreen!30] (2.4000,0.0) rectangle (3.2000,0.48);
\fill[otGreen!30] (3.2000,0.0) rectangle (4.0000,0.48);
\fill[otGreen!30] (4.0000,0.0) rectangle (4.8000,0.48);
\fill[white] (4.8000,0.0) rectangle (5.6000,0.48);
\fill[white] (5.6000,0.0) rectangle (6.4000,0.48);
\draw[otNavy] (0,0.0) rectangle (6.4,0.48);
\draw[otNavy] (0.8000,0.0) -- (0.8000,0.48);
\draw[otNavy] (1.6000,0.0) -- (1.6000,0.48);
\draw[otNavy] (2.4000,0.0) -- (2.4000,0.48);
\draw[otNavy] (3.2000,0.0) -- (3.2000,0.48);
\draw[otNavy] (4.0000,0.0) -- (4.0000,0.48);
\draw[otNavy] (4.8000,0.0) -- (4.8000,0.48);
\draw[otNavy] (5.6000,0.0) -- (5.6000,0.48);
\node[] at (7.05,0.24) {$\dfrac{6}{8}$};
\end{tikzpicture}
""",
    'ex1_enonce': r"""
\begin{tikzpicture}[x=1cm,y=1cm,font=\large,text=otInk,line width=0.8pt]
\fill[otGreen!30] (0.0000,1.1) rectangle (3.2000,1.58);
\fill[white] (3.2000,1.1) rectangle (6.4000,1.58);
\draw[otNavy] (0,1.1) rectangle (6.4,1.58);
\draw[otNavy] (3.2000,1.1) -- (3.2000,1.58);
\node[] at (7.05,1.34) {$\dfrac{1}{2}$};
\fill[otGreen!30] (0.0000,0.0) rectangle (0.6400,0.48);
\fill[otGreen!30] (0.6400,0.0) rectangle (1.2800,0.48);
\fill[otGreen!30] (1.2800,0.0) rectangle (1.9200,0.48);
\fill[otGreen!30] (1.9200,0.0) rectangle (2.5600,0.48);
\fill[otGreen!30] (2.5600,0.0) rectangle (3.2000,0.48);
\fill[white] (3.2000,0.0) rectangle (3.8400,0.48);
\fill[white] (3.8400,0.0) rectangle (4.4800,0.48);
\fill[white] (4.4800,0.0) rectangle (5.1200,0.48);
\fill[white] (5.1200,0.0) rectangle (5.7600,0.48);
\fill[white] (5.7600,0.0) rectangle (6.4000,0.48);
\draw[otNavy] (0,0.0) rectangle (6.4,0.48);
\draw[otNavy] (0.6400,0.0) -- (0.6400,0.48);
\draw[otNavy] (1.2800,0.0) -- (1.2800,0.48);
\draw[otNavy] (1.9200,0.0) -- (1.9200,0.48);
\draw[otNavy] (2.5600,0.0) -- (2.5600,0.48);
\draw[otNavy] (3.2000,0.0) -- (3.2000,0.48);
\draw[otNavy] (3.8400,0.0) -- (3.8400,0.48);
\draw[otNavy] (4.4800,0.0) -- (4.4800,0.48);
\draw[otNavy] (5.1200,0.0) -- (5.1200,0.48);
\draw[otNavy] (5.7600,0.0) -- (5.7600,0.48);
\node[] at (7.05,0.24) {$\dfrac{5}{10}$};
\end{tikzpicture}
""",
    'ex2_enonce': r"""
\begin{tikzpicture}[x=1cm,y=1cm,font=\large,text=otInk,line width=0.8pt]
\fill[white] (0.0000,0) rectangle (0.8000,0.48);
\fill[white] (0.8000,0) rectangle (1.6000,0.48);
\fill[white] (1.6000,0) rectangle (2.4000,0.48);
\fill[white] (2.4000,0) rectangle (3.2000,0.48);
\fill[white] (3.2000,0) rectangle (4.0000,0.48);
\fill[white] (4.0000,0) rectangle (4.8000,0.48);
\fill[white] (4.8000,0) rectangle (5.6000,0.48);
\fill[white] (5.6000,0) rectangle (6.4000,0.48);
\draw[otNavy] (0,0) rectangle (6.4,0.48);
\draw[otNavy] (0.8000,0) -- (0.8000,0.48);
\draw[otNavy] (1.6000,0) -- (1.6000,0.48);
\draw[otNavy] (2.4000,0) -- (2.4000,0.48);
\draw[otNavy] (3.2000,0) -- (3.2000,0.48);
\draw[otNavy] (4.0000,0) -- (4.0000,0.48);
\draw[otNavy] (4.8000,0) -- (4.8000,0.48);
\draw[otNavy] (5.6000,0) -- (5.6000,0.48);
\end{tikzpicture}
""",
    'ex2_correction': r"""
\begin{tikzpicture}[x=1cm,y=1cm,font=\large,text=otInk,line width=0.8pt]
\fill[otGreen!30] (0.0000,0) rectangle (0.8000,0.48);
\fill[otGreen!30] (0.8000,0) rectangle (1.6000,0.48);
\fill[otGreen!30] (1.6000,0) rectangle (2.4000,0.48);
\fill[otGreen!30] (2.4000,0) rectangle (3.2000,0.48);
\fill[white] (3.2000,0) rectangle (4.0000,0.48);
\fill[white] (4.0000,0) rectangle (4.8000,0.48);
\fill[white] (4.8000,0) rectangle (5.6000,0.48);
\fill[white] (5.6000,0) rectangle (6.4000,0.48);
\draw[otNavy] (0,0) rectangle (6.4,0.48);
\draw[otNavy] (0.8000,0) -- (0.8000,0.48);
\draw[otNavy] (1.6000,0) -- (1.6000,0.48);
\draw[otNavy] (2.4000,0) -- (2.4000,0.48);
\draw[otNavy] (3.2000,0) -- (3.2000,0.48);
\draw[otNavy] (4.0000,0) -- (4.0000,0.48);
\draw[otNavy] (4.8000,0) -- (4.8000,0.48);
\draw[otNavy] (5.6000,0) -- (5.6000,0.48);
\end{tikzpicture}
""",
    'ex6_correction': r"""
\begin{tikzpicture}[x=1cm,y=1cm,font=\large,text=otInk,line width=0.8pt]
\fill[otGreen!30] (0.0000,1.1) rectangle (2.1333,1.58);
\fill[otGreen!30] (2.1333,1.1) rectangle (4.2667,1.58);
\fill[white] (4.2667,1.1) rectangle (6.4000,1.58);
\draw[otNavy] (0,1.1) rectangle (6.4,1.58);
\draw[otNavy] (2.1333,1.1) -- (2.1333,1.58);
\draw[otNavy] (4.2667,1.1) -- (4.2667,1.58);
\node[] at (7.05,1.34) {$\dfrac{2}{3}$};
\fill[otGreen!30] (0.0000,0.0) rectangle (1.0667,0.48);
\fill[otGreen!30] (1.0667,0.0) rectangle (2.1333,0.48);
\fill[otGreen!30] (2.1333,0.0) rectangle (3.2000,0.48);
\fill[otGreen!30] (3.2000,0.0) rectangle (4.2667,0.48);
\fill[white] (4.2667,0.0) rectangle (5.3333,0.48);
\fill[white] (5.3333,0.0) rectangle (6.4000,0.48);
\draw[otNavy] (0,0.0) rectangle (6.4,0.48);
\draw[otNavy] (1.0667,0.0) -- (1.0667,0.48);
\draw[otNavy] (2.1333,0.0) -- (2.1333,0.48);
\draw[otNavy] (3.2000,0.0) -- (3.2000,0.48);
\draw[otNavy] (4.2667,0.0) -- (4.2667,0.48);
\draw[otNavy] (5.3333,0.0) -- (5.3333,0.48);
\node[] at (7.05,0.24) {$\dfrac{4}{6}$};
\end{tikzpicture}
""",
    'ex9_correction': r"""
\begin{tikzpicture}[x=1cm,y=1cm,font=\large,text=otInk,line width=0.8pt]
\fill[otGreen!30] (0.0000,1.1) rectangle (1.6000,1.58);
\fill[otGreen!30] (1.6000,1.1) rectangle (3.2000,1.58);
\fill[white] (3.2000,1.1) rectangle (4.8000,1.58);
\fill[white] (4.8000,1.1) rectangle (6.4000,1.58);
\draw[otNavy] (0,1.1) rectangle (6.4,1.58);
\draw[otNavy] (1.6000,1.1) -- (1.6000,1.58);
\draw[otNavy] (3.2000,1.1) -- (3.2000,1.58);
\draw[otNavy] (4.8000,1.1) -- (4.8000,1.58);
\node[] at (7.05,1.34) {$\dfrac{2}{4}$};
\fill[otGreen!30] (0.0000,0.0) rectangle (3.2000,0.48);
\fill[white] (3.2000,0.0) rectangle (6.4000,0.48);
\draw[otNavy] (0,0.0) rectangle (6.4,0.48);
\draw[otNavy] (3.2000,0.0) -- (3.2000,0.48);
\node[] at (7.05,0.24) {$\dfrac{1}{2}$};
\end{tikzpicture}
""",
}
