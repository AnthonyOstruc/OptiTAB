# -*- coding: utf-8 -*-
"""Figure de la page « Lire l'heure » : une horloge expliquée (10 h 08).

    python frontend/cours/format_v1/outils/figures_livre.py frontend/contenu/methodes/lire-l-heure --planche --jobs 1

Le dessin de l'horloge vient de ../horloge_tikz.py (le même que les fiches PDF).
10 h 08 et non 10 h 10 : avec un nombre de minutes multiple de 5, la grande
aiguille passerait sur un chiffre (texte sur un trait). Légende sous l'horloge,
avec un échantillon de chaque aiguille, pour une figure étroite (téléphone).
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from horloge_tikz import BS, horloge  # noqa: E402

NOTE = BS + r"otMedium" + BS + r"fontsize{10.5}{12}" + BS + r"selectfont"


def ligne_legende(y, trait, texte, couleur):
    return (rf"{BS}draw[{trait},line cap=round] (-2.3,{y}) -- (-1.5,{y});" + "\n"
            + rf"{BS}node[anchor=west,inner sep=0pt,font={NOTE},text={couleur}] at (-1.3,{y}) {{{texte}}};")


HORLOGE_ANNOTEE = "\n".join([
    BS + "begin{tikzpicture}",
    horloge(0, 0, 1.9, 10, 8, minutes_autour=True),
    ligne_legende(-2.95, "otNavy,line width=3.8pt", "petite aiguille : les heures", "otNavy"),
    ligne_legende(-3.55, "otOrange!90!black,line width=2.4pt", "grande aiguille : les minutes", "otOrange!85!black"),
    rf"{BS}node[anchor=west,inner sep=0pt,font={NOTE},text=otGreenDark] at (-2.3,-4.15) {{05, 10, 15… : les minutes de 5 en 5}};",
    BS + "end{tikzpicture}",
])

FIGURES = {"horloge_annotee": HORLOGE_ANNOTEE}
