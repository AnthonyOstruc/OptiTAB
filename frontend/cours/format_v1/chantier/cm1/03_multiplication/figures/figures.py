# -*- coding: utf-8 -*-
FIGURES = {'groupes': '\n\\begin{tikzpicture}[x=1cm,y=1cm]\n\\node[text=otNavy] at (3.5,1.6) {Quatre groupes égaux};\n\\foreach \\x in {0,1.8,3.6,5.4}{\n\\draw[geoTrait,fill=otSky] (\\x,0) rectangle +(1.5,.9);\n\\node at (\\x+.75,.45) {45};}\n\\node[text=otGreenDark] at (3.45,-.55) {$4\\times45=180$};\n\\end{tikzpicture}'}
