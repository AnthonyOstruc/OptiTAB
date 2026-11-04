# -*- coding: utf-8 -*-
"""Figures TikZ de la notion, palette des livres OptiTAB."""
FIGURES = {'cours_addition': '\\begin{tikzpicture}[x=.75cm,y=1cm]\n\\draw[geoVecteur] (-5,0)--(5,0);\n\\foreach \\x in {-4,...,4}{\\draw[otMuted] (\\x,-.06)--(\\x,.06);\\node[below=7pt,text=otMuted] at (\\x,0) {$\\x$};}\n\\draw[geoReponse,-{Stealth}] (-2,.6)--(4,.6);\n\\draw[guide] (-2,.12)--(-2,.6);\n\\draw[guide] (4,.12)--(4,.6);\n\\node[text=otGreenDark] at (1,1) {$+6$};\n\\node[anchor=west,text=otInk] at (-4,-.8) {$(-2)+6=4$};\n\\end{tikzpicture}'}
