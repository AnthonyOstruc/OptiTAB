# -*- coding: utf-8 -*-
"""Figures de « Calculer une moyenne » (valeurs vérifiées)."""
import sys
from fractions import Fraction as Fr
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from fig_commun import PREAMBULE_EXTRA, f, tikz, carte  # noqa: E402,F401

FIGURES = {}


def barres(notes, moyenne, l=.9, ecart=.55, k=.17, etiquettes=True, libelle="moyenne "):
    """Diagramme en barres des notes avec la ligne de la moyenne (k cm par point)."""
    L = []
    n = len(notes)
    largeur = n * l + (n + 1) * ecart
    L.append(r"\draw[otMuted,line width=.6pt] (0,0) -- (%s,0);" % f(largeur))
    for i, (nom, v) in enumerate(notes):
        x = ecart + i * (l + ecart)
        L.append(r"\fill[otNavy!80] (%s,0) rectangle (%s,%s);" % (f(x), f(x + l), f(v * k)))
        # valeur au-dessus de la barre ; les notes sont choisies loin de la moyenne
        assert abs(v - float(moyenne)) * k > .5 or v > moyenne, "étiquette trop près de la ligne de la moyenne"
        L.append(r"\node[etiq,anchor=south] at (%s,%s) {$%s$};" % (f(x + l / 2), f(v * k + .05), f(v).replace(".", "{,}")))
        if etiquettes:
            L.append(r"\node[note,anchor=north] at (%s,-.08) {%s};" % (f(x + l / 2), nom))
    y = float(moyenne) * k
    L.append(r"\draw[otGreenDark,line width=1.1pt,dash pattern=on 5pt off 3pt] (0,%s) -- (%s,%s);" % (f(y), f(largeur), f(y)))
    L.append(r"\node[etiq,anchor=west,text=otGreenDark] at (%s,%s) {%s$%s$};" % (f(largeur + .1), f(y), libelle, f(moyenne).replace(".", "{,}")))
    return L


# Moyenne simple : 9, 16, 8, 17 → 50 ÷ 4 = 12,5.
notes = [("maths", 9), ("français", 16), ("anglais", 8), ("histoire", 17)]
m = Fr(sum(v for _, v in notes), len(notes))
assert m == Fr(25, 2)
FIGURES["moyenne_barres"] = tikz(barres(notes, m))

# Aperçu de la carte.
FIGURES["carte_moyenne"] = carte(barres([("", 9), ("", 16), ("", 8), ("", 17)], m, l=.7, ecart=.4, k=.15, etiquettes=False, libelle=""))
