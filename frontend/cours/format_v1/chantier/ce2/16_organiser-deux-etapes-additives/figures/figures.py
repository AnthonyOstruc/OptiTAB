# -*- coding: utf-8 -*-
"""Figures TikZ ; pr?ambule officiel fourni par outils/figures_livre.py."""
FIGURES = {
    'cours_schema': r"""
\begin{tikzpicture}[x=1cm,y=1cm,font=\large,text=otInk,line width=0.8pt]
\draw[otNavy,fill=otSky] (0,1.3) rectangle (5,1.85);\draw[otNavy,fill=otSky] (0,0) rectangle (5,.55);\draw[otGreenDark,fill=otGreen!20] (5,0) rectangle (7.2,.55);
\node[] at (2.5,1.575) {128};
\node[] at (2.5,0.275) {128};
\node[] at (6.1,0.275) {+35};
\node[font=\normalsize] at (3.6,-0.6) {Ensemble : réunir les deux barres};
\end{tikzpicture}
""",
    'ex1_schema': r"""
\begin{tikzpicture}[x=1cm,y=1cm,font=\large,text=otInk,line width=0.8pt]
\draw[otNavy,fill=otSky] (0,1.3) rectangle (5,1.85);\draw[otNavy,fill=otSky] (0,0) rectangle (5,.55);\draw[otGreenDark,fill=otGreen!20] (5,0) rectangle (7.2,.55);
\node[] at (2.5,1.575) {146};
\node[] at (2.5,0.275) {146};
\node[] at (6.1,0.275) {+28};
\node[font=\normalsize] at (3.6,-0.6) {Ensemble : réunir les deux barres};
\end{tikzpicture}
""",
    'ex5_schema': r"""
\begin{tikzpicture}[x=1cm,y=1cm,font=\large,text=otInk,line width=0.8pt]
\draw[otNavy,fill=otSky] (0,0) rectangle (7.5,.6);\draw[otNavy] (3.7324,0)--(3.7324,.6);
\node[] at (1.8661764705882353,0.3) {423};
\node[text=otGreenDark] at (5.616176470588235,0.3) {?};
\node[text=otNavy] at (3.75,1.2) {Tout : 850 cm};
\end{tikzpicture}
""",
    'ex9_schema': r"""
\begin{tikzpicture}[x=1cm,y=1cm,font=\large,text=otInk,line width=0.8pt]
\draw[otNavy,fill=otSky] (0,1.3) rectangle (5,1.85);\draw[otNavy,fill=otSky] (0,0) rectangle (5,.55);\draw[otGreenDark,fill=otGreen!20] (5,0) rectangle (7.2,.55);
\node[] at (2.5,1.575) {128};
\node[] at (2.5,0.275) {128};
\node[] at (6.1,0.275) {+35};
\node[font=\normalsize] at (3.6,-0.6) {Ensemble : réunir les deux barres};
\end{tikzpicture}
""",
}
