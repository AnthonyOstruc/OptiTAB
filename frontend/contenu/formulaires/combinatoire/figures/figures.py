# -*- coding: utf-8 -*-
"""Figure de « Combinatoire » : triangle de Pascal (lignes 0 à 6), avec 4 + 6 = 10."""
from math import comb

PX, PY = 0.9, 0.76
N = 6
VERTS = {(4, 1), (4, 2)}
ORANGE = {(5, 2)}


def pos(n, k):
    return (k - n / 2) * PX, -n * PY


def triangle():
    l = [r"\begin{tikzpicture}"]
    for (n, k) in VERTS | ORANGE:
        x, y = pos(n, k)
        fond = "otGreen!28" if (n, k) in VERTS else "otOrange!35"
        l.append(rf"  \fill[{fond}] ({x:.3f},{y:.3f}) circle (0.27);")
    # flèches 4 → 10 et 6 → 10
    xa, ya = pos(5, 2)
    for k in (1, 2):
        x, y = pos(4, k)
        l.append(rf"  \draw[otGreenDark,line width=0.9pt,-{{Stealth[length=1.8mm]}}] "
                 rf"({x + (xa - x) * 0.36:.3f},{y + (ya - y) * 0.36:.3f}) -- ({x + (xa - x) * 0.64:.3f},{y + (ya - y) * 0.64:.3f});")
    for n in range(N + 1):
        for k in range(n + 1):
            x, y = pos(n, k)
            l.append(rf"  \node[text=otNavy] at ({x:.3f},{y:.3f}) {{${comb(n, k)}$}};")
        l.append(rf"  \node[text=otMuted,font=\small,anchor=east] at ({-(N / 2) * PX - 0.75:.3f},{-n * PY:.3f}) {{$n = {n}$}};")
    l.append(r"\end{tikzpicture}")
    return "\n".join(l)


FIGURES = {"triangle_pascal": triangle()}
