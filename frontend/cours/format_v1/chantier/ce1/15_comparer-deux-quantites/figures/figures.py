# -*- coding: utf-8 -*-
"""Figures TikZ ; préambule officiel fourni par figures_livre.py."""
FIGURES = {
    'cours_schema': r"""
\begin{tikzpicture}[x=1cm,y=1cm,font=\large,text=otInk,line width=.8pt]
\draw[otNavy,fill=otSky] (0,1.4) rectangle (5.66120218579235,1.95);
\node[text=otInk] at (2.830601092896175,2.35) {148};
\draw[otNavy,fill=otSky] (0,0) rectangle (5.66120218579235,.55);
\draw[otNavy,fill=white] (5.66120218579235,0) rectangle (7,.55);
\node[text=otInk] at (6.330601092896175,-0.4) {Écart : 35};
\node[text=otInk] at (2.830601092896175,-0.4) {148};
\node[text=otInk] at (3.5,-1) {Grande quantité : ?};
\end{tikzpicture}
""",
    'ex1_schema': r"""
\begin{tikzpicture}[x=1cm,y=1cm,font=\large,text=otInk,line width=.8pt]
\draw[otNavy,fill=otSky] (0,1.4) rectangle (5.718954248366013,1.95);
\node[text=otInk] at (2.8594771241830066,2.35) {125};
\draw[otNavy,fill=otSky] (0,0) rectangle (5.718954248366013,.55);
\draw[otNavy,fill=white] (5.718954248366013,0) rectangle (7,.55);
\node[text=otInk] at (6.359477124183007,-0.4) {Écart : 28};
\node[text=otInk] at (2.8594771241830066,-0.4) {125};
\node[text=otInk] at (3.5,-1) {Grande quantité : ?};
\end{tikzpicture}
""",
    'ex1_corrige': r"""
\begin{tikzpicture}[x=1cm,y=1cm,font=\large,text=otInk,line width=.8pt]
\draw[otNavy,fill=otSky] (0,1.4) rectangle (5.718954248366013,1.95);
\node[text=otInk] at (2.8594771241830066,2.35) {125};
\draw[otNavy,fill=otSky] (0,0) rectangle (5.718954248366013,.55);
\draw[otNavy,fill=otGreen!25] (5.718954248366013,0) rectangle (7,.55);
\node[text=otInk] at (6.359477124183007,-0.4) {Écart : 28};
\node[text=otInk] at (2.8594771241830066,-0.4) {125};
\node[text=otGreenDark] at (3.5,-1) {Grande quantité : 153};
\end{tikzpicture}
""",
}
