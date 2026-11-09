# -*- coding: utf-8 -*-
"""Figures de « PGCD et PPCM » : partage en carrés, algorithme d'Euclide en image."""

# Rectangle 36 × 24 pavé par des carrés de côté 12 = PGCD(36 ; 24).
U = 0.14  # cm par unité


def partage():
    l = [r"\begin{tikzpicture}"]
    for i in range(3):
        for j in range(2):
            fond = "otSky" if (i + j) % 2 == 0 else "otGreen!22"
            l.append(rf"  \fill[{fond}] ({12 * i * U:.3f},{12 * j * U:.3f}) rectangle ({12 * (i + 1) * U:.3f},{12 * (j + 1) * U:.3f});")
    for i in range(1, 3):
        l.append(rf"  \draw[otNavy,line width=0.7pt] ({12 * i * U:.3f},0) -- ({12 * i * U:.3f},{24 * U:.3f});")
    l.append(rf"  \draw[otNavy,line width=0.7pt] (0,{12 * U:.3f}) -- ({36 * U:.3f},{12 * U:.3f});")
    l.append(rf"  \draw[geoTrait,line width=1.2pt] (0,0) rectangle ({36 * U:.3f},{24 * U:.3f});")
    l.append(rf"  \coordinate (O) at (0,0); \coordinate (L) at ({36 * U:.3f},0); \coordinate (H) at (0,{24 * U:.3f}); \coordinate (C) at ({12 * U:.3f},{24 * U:.3f});")
    l.append(r"  \cote[0.35]{L}{O}{$36$}")
    l.append(r"  \cote[0.35]{O}{H}{$24$}")
    l.append(r"  \cote[0.35]{H}{C}{$12$}")
    l.append(r"\end{tikzpicture}")
    return "\n".join(l)


# Rectangle 21 × 15 : un carré de 15, deux carrés de 6, deux carrés de 3.
V = 0.25
CARRES = [  # (x, y, côté, couleur, taille de l'étiquette)
    (0, 0, 15, "otSky", r"\large"),
    (15, 0, 6, "otGreen!22", ""),
    (15, 6, 6, "otGreen!22", ""),
    (15, 12, 3, "otOrange!30", r"\small"),
    (18, 12, 3, "otOrange!30", r"\small"),
]


def euclide():
    l = [r"\begin{tikzpicture}"]
    for x, y, c, fond, taille in CARRES:
        l.append(rf"  \fill[{fond}] ({x * V},{y * V}) rectangle ({(x + c) * V},{(y + c) * V});")
        l.append(rf"  \draw[otNavy,line width=0.7pt] ({x * V},{y * V}) rectangle ({(x + c) * V},{(y + c) * V});")
        l.append(rf"  \node[text=otInk,font={taille or r'\normalsize'}] at ({(x + c / 2) * V},{(y + c / 2) * V}) {{${c}$}};")
    l.append(rf"  \draw[geoTrait,line width=1.2pt] (0,0) rectangle ({21 * V},{15 * V});")
    l.append(rf"  \coordinate (O) at (0,0); \coordinate (L) at ({21 * V},0); \coordinate (H) at (0,{15 * V});")
    l.append(r"  \cote[0.35]{L}{O}{$21$}")
    l.append(r"  \cote[0.35]{O}{H}{$15$}")
    l.append(rf"  \node[anchor=north,text=otInk,align=center] at ({10.5 * V},-0.95) "
             r"{$21 = 1 \times 15 + 6$\\[2pt]$15 = 2 \times 6 + 3$\\[2pt]$6 = 2 \times 3 + 0$\\[6pt]"
             r"\textcolor{otGreenDark}{PGCD $= 3$}};")
    l.append(r"\end{tikzpicture}")
    return "\n".join(l)


FIGURES = {"partage_carres": partage(), "euclide_rectangle": euclide()}
