# -*- coding: utf-8 -*-
"""Figure de « Matrices et déterminants » : ligne de A × colonne de B = coefficient de AB."""

DX, DY = 0.82, 0.72


def crochets(x0, x1, y0, y1):
    """Crochets d'une matrice entre x0 et x1, de y0 (bas) à y1 (haut)."""
    t = 0.12
    return (rf"  \draw[otInk,line width=0.9pt] ({x0 + t},{y1}) -- ({x0},{y1}) -- ({x0},{y0}) -- ({x0 + t},{y0});" "\n"
            rf"  \draw[otInk,line width=0.9pt] ({x1 - t},{y1}) -- ({x1},{y1}) -- ({x1},{y0}) -- ({x1 - t},{y0});")


def matrice(nom, x, y, lignes, colonnes, lettre):
    """Coefficients lettre_{ij} centrés sur (x, y)."""
    l = []
    for i in range(lignes):
        for j in range(colonnes):
            cx = x + (j - (colonnes - 1) / 2) * DX
            cy = y + ((lignes - 1) / 2 - i) * DY
            l.append(rf"  \node[text=otInk] at ({cx:.3f},{cy:.3f}) {{${lettre}_{{{i + 1}{j + 1}}}$}};")
    demi_l, demi_h = colonnes * DX / 2 + 0.08, lignes * DY / 2 + 0.05
    l.append(crochets(x - demi_l, x + demi_l, y - demi_h, y + demi_h))
    l.append(rf"  \node[text=otMuted,anchor=north] at ({x},{y - demi_h - 0.12}) {{${nom}$}};")
    return "\n".join(l)


XA, XB, XC = 0.0, 3.55, 6.75
PRODUIT = "\n".join([
    r"\begin{tikzpicture}",
    # surlignages (sous les coefficients)
    rf"  \fill[otSky,rounded corners=3pt] ({XA - 1.5 * DX + 0.05},{DY / 2 - 0.27}) rectangle ({XA + 1.5 * DX - 0.05},{DY / 2 + 0.27});",
    rf"  \fill[otGreen!25,rounded corners=3pt] ({XB + DX / 2 - 0.34},{-DY - 0.3}) rectangle ({XB + DX / 2 + 0.34},{DY + 0.3});",
    rf"  \fill[otOrange!30,rounded corners=3pt] ({XC + DX / 2 - 0.34},{DY / 2 - 0.27}) rectangle ({XC + DX / 2 + 0.34},{DY / 2 + 0.27});",
    matrice("A", XA, 0, 2, 3, "a"),
    rf"  \node[text=otInk] at ({(XA + 1.5 * DX + XB - DX) / 2},0) {{$\times$}};",
    matrice("B", XB, 0, 3, 2, "b"),
    rf"  \node[text=otInk] at ({(XB + DX + XC - DX) / 2},0) {{$=$}};",
    matrice("AB", XC, 0, 2, 2, "c"),
    rf"  \node[text=otInk,anchor=north] at ({(XA + XC) / 2},{-1.5 * DY - 0.75}) "
    r"{$c_{12} = a_{11}\,b_{12} + a_{12}\,b_{22} + a_{13}\,b_{32}$};",
    r"\end{tikzpicture}",
])

FIGURES = {"produit_matrices": PRODUIT}
