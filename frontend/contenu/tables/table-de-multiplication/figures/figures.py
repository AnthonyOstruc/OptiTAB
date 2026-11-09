# -*- coding: utf-8 -*-
"""Figures de la « Table de multiplication ».

    python frontend/cours/format_v1/outils/figures_livre.py frontend/contenu/tables/table-de-multiplication --planche --jobs 1
"""

C = 0.74  # côté d'une case (cm)


def grille():
    """Table de Pythagore 1 à 10 : en-têtes bleus, carrés (diagonale) en vert."""
    l = [r"\begin{tikzpicture}"]
    for i in range(11):
        for j in range(11):
            x, y = j * C, -i * C
            if i == 0 and j == 0:
                l.append(rf"  \fill[otNavy] ({x},{y}) rectangle ++({C},{-C});")
                l.append(rf"  \node[text=white,font=\Large] at ({x + C / 2},{y - C / 2}) {{$\times$}};")
                continue
            if i == 0 or j == 0:
                l.append(rf"  \fill[otNavy] ({x},{y}) rectangle ++({C},{-C});")
                n = j if i == 0 else i
                l.append(rf"  \node[text=white,font=\otMedium\bfseries\fontsize{{10}}{{12}}\selectfont] at ({x + C / 2},{y - C / 2}) {{{n}}};")
                continue
            if i == j:
                l.append(rf"  \fill[otGreen!28] ({x},{y}) rectangle ++({C},{-C});")
            elif (i + j) % 2 == 0:
                l.append(rf"  \fill[otSky!55] ({x},{y}) rectangle ++({C},{-C});")
            couleur = "otGreenDark" if i == j else "otInk"
            gras = r"\bfseries" if i == j else ""
            l.append(rf"  \node[text={couleur},font=\otRegular{gras}\fontsize{{10}}{{12}}\selectfont] at ({x + C / 2},{y - C / 2}) {{{i * j}}};")
    l.append(rf"  \draw[otRule,line width=0.4pt] (0,0) grid[step={C}] ({11 * C},{-11 * C});")
    l.append(rf"  \draw[otNavy,line width=0.9pt] (0,0) rectangle ({11 * C},{-11 * C});")
    l.append(r"\end{tikzpicture}")
    return "\n".join(l)


# 7 × 8 = 56 : 7 rangées de 8 points.
def points():
    l = [r"\begin{tikzpicture}[x=0.5cm,y=0.5cm]"]
    for r in range(7):
        for c in range(8):
            l.append(rf"  \fill[otNavy] ({c},{-r}) circle (0.17);")
    l.append(r"  \draw[otGreenDark,line width=0.8pt,decorate,decoration={brace,amplitude=4pt}] (-0.3,0.45) -- (7.3,0.45);")
    l.append(r"  \node[anchor=south,text=otGreenDark,yshift=5pt] at (3.5,0.45) {$8$ points par rangée};")
    l.append(r"  \draw[otOrange!85!black,line width=0.8pt,decorate,decoration={brace,amplitude=4pt,mirror}] (-0.5,0.3) -- (-0.5,-6.3);")
    l.append(r"  \node[anchor=east,text=otOrange!75!black,xshift=-6pt,align=right] at (-0.5,-3) {$7$\\rangées};")
    l.append(r"  \node[anchor=west,xshift=10pt,font=\large] at (7.3,-3) {$7 \times 8 = 56$};")
    l.append(r"\end{tikzpicture}")
    return "\n".join(l)


FIGURES = {"table_pythagore": grille(), "rangees_7x8": points()}

TOLERE = {"table_pythagore": "chiffres blancs sur les cases d’en-tête bleues pleines : le fond plein est pris pour un trait (vérifié à l’œil)"}
