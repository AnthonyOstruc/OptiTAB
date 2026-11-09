# -*- coding: utf-8 -*-
"""Figure de « Équations et inéquations » : intervalles solutions sur deux droites graduées."""

U = 0.72  # cm par unité


def droite(y, debut, fin, crochets, titre):
    """Droite graduée de −4 à 5 ; solution [debut ; fin] en vert, crochets (x, sens)."""
    l = [rf"  \draw[otMuted,line width=0.7pt,-{{Stealth[length=2.3mm]}}] ({-4.7 * U},{y}) -- ({5.7 * U},{y});"]
    for k in range(-4, 6):
        l.append(rf"  \draw[otMuted,line width=0.5pt] ({k * U},{y - 0.07}) -- ({k * U},{y + 0.07});")
        txt = f"${k}$" if k >= 0 else f"$-{-k}$"
        l.append(rf"  \node[anchor=north,text=otMuted,font=\small] at ({k * U},{y - 0.3}) {{{txt}}};")
    l.append(rf"  \draw[otGreen,line width=3.2pt,opacity=0.9] ({debut * U},{y}) -- ({fin * U},{y});")
    for x, d in crochets:
        l.append(rf"  \draw[otGreenDark,line width=1.4pt] ({x * U + d},{y + 0.24}) -- ({x * U},{y + 0.24}) -- ({x * U},{y - 0.24}) -- ({x * U + d},{y - 0.24});")
    l.append(rf"  \node[anchor=south,text=otInk] at ({0.5 * U},{y + 0.42}) {{{titre}}};")
    return "\n".join(l)


INTERVALLES = "\n".join([
    r"\begin{tikzpicture}",
    droite(1.9, -4.7, 3, [(3, 0.13)], r"$x < 3$ \quad donc \quad $S = \left]-\infty\,;3\right[$"),
    droite(0, -2, 1, [(-2, 0.13), (1, -0.13)], r"$-2 \leqslant x \leqslant 1$ \quad donc \quad $S = [-2\,;1]$"),
    r"\end{tikzpicture}",
])

FIGURES = {"intervalles": INTERVALLES}
