# -*- coding: utf-8 -*-
"""Figure de la page « Unités du Système international et constantes physiques ».

    PYTHONUTF8=1 python cours/format_v1/outils/figures_livre.py contenu/physique-chimie/unites-si-constantes-physiques --planche --jobs 1

Les 7 unités de base du SI et la constante, de valeur fixée exactement depuis le
20 mai 2019, qui définit chacune d'elles (Brochure sur le SI, BIPM, 9e édition).
Schéma original (pas le logo du BIPM) : texte sans cadre, rayons qui s'arrêtent
avant le texte.
"""
from math import cos, radians, sin

# (nom, symbole, constante) dans l'ordre de la figure, en partant du haut
UNITES = [
    ("seconde", "s", r"\Delta\nu_{\mathrm{Cs}}"),
    ("mètre", "m", r"c"),
    ("kilogramme", "kg", r"h"),
    ("ampère", "A", r"e"),
    ("kelvin", "K", r"k_{\mathrm{B}}"),
    ("mole", "mol", r"N_{\mathrm{A}}"),
    ("candela", "cd", r"K_{\mathrm{cd}}"),
]
assert len(UNITES) == 7

NOM = r"\otMedium\fontsize{10}{12}\selectfont"
CST = r"\fontsize{10.5}{12.5}\selectfont"


def unites_de_base():
    R_TEXTE, R0, R1 = 1.88, 0.78, 1.62
    s = "\\begin{tikzpicture}\n"
    s += "\\draw[otNavy,line width=1.2pt] (0,0) circle (0.68);\n"
    s += "\\node[text=otNavy,font=\\otMedium\\fontsize{15}{17}\\selectfont] at (0,0) {SI};\n"
    for i, (nom, symb, cst) in enumerate(UNITES):
        a = radians(90 - i * 360 / 7)
        # texte placé à l'extérieur du rayon : il ne peut pas le recouvrir
        ancre = "west" if cos(a) > 0.35 else "east" if cos(a) < -0.35 else ("south" if sin(a) > 0 else "north")
        s += f"\\draw[otNavy!45,line width=0.8pt] ({R0 * cos(a):.3f},{R0 * sin(a):.3f}) -- ({R1 * cos(a):.3f},{R1 * sin(a):.3f});\n"
        s += (f"\\node[align=center,inner sep=1pt,anchor={ancre}] at ({R_TEXTE * cos(a):.3f},{R_TEXTE * sin(a):.3f}) "
              f"{{{{\\color{{otInk}}{NOM} {nom} ({symb})}}\\\\[2pt]{{\\color{{otGreenDark}}{CST} ${cst}$}}}};\n")
    return s + "\\end{tikzpicture}"


FIGURES = {"unites_de_base": unites_de_base()}
