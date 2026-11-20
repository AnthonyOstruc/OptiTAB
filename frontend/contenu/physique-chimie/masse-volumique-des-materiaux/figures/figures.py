# -*- coding: utf-8 -*-
"""Figure de la page « Masse volumique des matériaux » : qui flotte, qui coule.

    PYTHONUTF8=1 python cours/format_v1/outils/figures_livre.py contenu/physique-chimie/masse-volumique-des-materiaux --planche --jobs 1

Barres en échelle logarithmique (une graduation par puissance de 10). Les valeurs
viennent de generer.py, qui vérifie qu'elles sont celles des tableaux de la page.
"""
from math import log10

BS = chr(92)
NB = chr(0xA0)
NOTE = BS + "otRegular" + BS + "fontsize{9.5}{11.5}" + BS + "selectfont"
NOM = BS + "otMedium" + BS + "fontsize{9.5}{11.5}" + BS + "selectfont"

# (nom, masse volumique en kg/m³) : moins dense que l'eau en haut, plus dense en bas
VALEURS = [
    ("liège", 200),
    ("bois de pin", 520),
    ("huile", 920),
    ("glace", 917),
    ("eau", 1000),
    ("béton", 2400),
    ("aluminium", 2700),
    ("acier", 7850),
    ("plomb", 11340),
    ("or", 19300),
]
VALEURS.sort(key=lambda v: v[1])


def fr(n):
    s = f"{n:,}".replace(",", BS + ",")
    return s


def flotte_coule():
    X0, ECH, H = 4.35, 1.55, 0.42          # début des barres, cm par puissance de 10 (de 10² à 10⁴·³), hauteur d'une ligne
    def x(rho):
        return X0 + (log10(rho) - 2) * ECH
    s = BS + "begin{tikzpicture}\n"
    n = len(VALEURS)
    for i, (nom, rho) in enumerate(VALEURS):
        y = -i * H
        couleur = "otGreen!70" if rho < 1000 else ("otNavy!40" if rho == 1000 else "otOrange!75")
        s += f"{BS}node[anchor=east,text=otInk,font={NOM}] at (2.35,{y:.3f}) {{{nom}}};\n"
        s += f"{BS}node[anchor=east,text=otMuted,font={NOTE}] at (4.15,{y:.3f}) {{{fr(rho)}}};\n"
        s += f"{BS}fill[{couleur}] ({X0:.3f},{y - 0.13:.3f}) rectangle ({x(rho):.3f},{y + 0.13:.3f});\n"
    y_bas = -(n - 1) * H - 0.35
    # graduations logarithmiques sous les barres
    s += f"{BS}draw[otMuted!70,line width=0.5pt] ({X0:.3f},{y_bas:.3f}) -- ({x(20000):.3f},{y_bas:.3f});\n"
    for p, lib in [(100, "100"), (1000, "1" + BS + ",000"), (10000, "10" + BS + ",000")]:
        s += f"{BS}draw[otMuted!70,line width=0.5pt] ({x(p):.3f},{y_bas:.3f}) -- ({x(p):.3f},{y_bas - 0.08:.3f});\n"
        s += f"{BS}node[anchor=north,text=otMuted,font={NOTE}] at ({x(p):.3f},{y_bas - 0.1:.3f}) {{{lib}}};\n"
    s += f"{BS}node[anchor=north,text=otMuted,font={NOTE}] at ({(X0 + x(20000)) / 2:.3f},{y_bas - 0.55:.3f}) {{kg/m³, échelle logarithmique}};\n"
    # seuil de l'eau et légende
    xe = x(1000)
    s += f"{BS}draw[otNavy,line width=0.8pt,dash pattern=on 3pt off 2pt] ({xe:.3f},0.42) -- ({xe:.3f},{y_bas:.3f});\n"
    s += f"{BS}node[anchor=south east,text=otGreenDark,font={NOM}] at ({xe - 0.1:.3f},0.3) {{flotte sur l’eau}};\n"
    s += f"{BS}node[anchor=south west,text=otOrange!80!black,font={NOM}] at ({xe + 0.1:.3f},0.3) {{coule}};\n"
    return s + BS + "end{tikzpicture}"


FIGURES = {"flotte_coule": flotte_coule()}
