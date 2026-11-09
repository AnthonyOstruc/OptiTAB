# -*- coding: utf-8 -*-
"""Figure « Carrés, cubes et racines » : carrés parfaits 1, 4, 9, 16."""

C = 0.42


def carres():
    l = [r"\begin{tikzpicture}"]
    x = 0
    for n in (1, 2, 3, 4):
        cote = n * C
        l.append(rf"  \fill[otSky] ({x},0) rectangle ++({cote},{cote});")
        # quadrillage tracé ligne par ligne depuis le coin du carré (grid s'alignerait sur l'origine)
        for k in range(1, n):
            l.append(rf"  \draw[otNavy!40,line width=0.4pt] ({x + k * C:.4f},0) -- ++(0,{cote:.4f});")
            l.append(rf"  \draw[otNavy!40,line width=0.4pt] ({x:.4f},{k * C:.4f}) -- ++({cote:.4f},0);")
        l.append(rf"  \draw[otNavy,line width=1.1pt] ({x},0) rectangle ++({cote},{cote});")
        l.append(rf"  \node[anchor=north,inner sep=2pt] at ({x + cote / 2},-0.08) {{${n}^2 = {n * n}$}};")
        l.append(rf"  \node[anchor=south,inner sep=1.5pt,text=otMuted,font=\otRegular\fontsize{{9}}{{10}}\selectfont] at ({x + cote / 2},{cote + 0.05}) {{côté {n}}};")
        x += cote + 0.9
    l.append(r"\end{tikzpicture}")
    return "\n".join(l)


FIGURES = {"carres_parfaits": carres()}
