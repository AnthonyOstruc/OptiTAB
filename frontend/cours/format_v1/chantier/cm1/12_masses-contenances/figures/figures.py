from pathlib import Path
FIGURES = {'balance': '\\begin{tikzpicture}[]\n\\draw[otNavy,line width=1pt] (-2.5,1.6)--(2.5,1.6);\n\\draw[otNavy,line width=1pt] (0,1.6)--(-.65,0)--(.65,0)--cycle;\n\\draw[otMuted] (-2.1,1.6)--(-2.7,.25)--(-1.5,.25)--cycle;\n\\draw[otMuted] (2.1,1.6)--(1.5,.25)--(2.7,.25)--cycle;\n\\node[anchor=south] at (-2.1,1.95) {Sac};\n\\node[anchor=south] at (2.1,1.95) {500 g + 200 g + 50 g};\n\\node[anchor=north,text=otGreenDark] at (0,-.4) {Équilibre : masses égales.};\n\\end{tikzpicture}'}
TOLERE = {}
