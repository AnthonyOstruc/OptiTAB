# -*- coding: utf-8 -*-
"""Figures TikZ au style livre ; compiler avec outils/figures_livre.py --jobs 1."""
FIGURES = {'cours_methode': '\\begin{tikzpicture}[x=1cm,y=1cm]\n\\node[text=otNavy] at (0.0,0) {$75$};\n\\node[text=otGreenDark] at (2.5,0) {$150$};\n\\draw[otMuted,-{Stealth[length=2mm]}] (0.65,0) -- (1.85,0);\n\\node[text=otNavy] at (1.25,.55) {$\\times 2$};\n\\end{tikzpicture}'}
