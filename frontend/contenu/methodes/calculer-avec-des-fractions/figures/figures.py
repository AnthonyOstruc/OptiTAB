# -*- coding: utf-8 -*-
"""Figures de « Calculer avec les fractions » : barres partagées."""
import sys
from fractions import Fraction as Fr
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from fig_commun import PREAMBULE_EXTRA, f, tikz, carte  # noqa: E402,F401

FIGURES = {}


def barre(num, den, y=0.0, l=6.0, h=.6, coul="otGreen!65", libelle=True):
    """Barre unité partagée en den parts, num parts colorées."""
    L = []
    w = l / den
    for i in range(den):
        c = coul if i < num else "white"
        L.append(r"\fill[%s] (%s,%s) rectangle (%s,%s);" % (c, f(i * w), f(y), f((i + 1) * w), f(y + h)))
    for i in range(1, den):
        L.append(r"\draw[otNavy!70,line width=.5pt] (%s,%s) -- (%s,%s);" % (f(i * w), f(y), f(i * w), f(y + h)))
    L.append(r"\draw[otNavy,line width=.9pt] (0,%s) rectangle (%s,%s);" % (f(y), f(l), f(y + h)))
    if libelle:
        L.append(r"\node[etiq,anchor=west] at (%s,%s) {$\dfrac{%d}{%d}$};" % (f(l + .25), f(y + h / 2), num, den))
    return L


# 3/4 = 9/12 et 5/6 = 10/12 : la même barre découpée en 12.
assert Fr(3, 4) == Fr(9, 12) and Fr(5, 6) == Fr(10, 12)
L = barre(3, 4, y=1.0) + barre(9, 12, y=0.0)
L.append(r"\node[note,anchor=east] at (-.2,1.3) {en 4 parts};")
L.append(r"\node[note,anchor=east] at (-.2,.3) {en 12 parts};")
FIGURES["fraction_egales"] = tikz(L)

# Aperçu de la carte : 3/4.
FIGURES["carte_fraction"] = carte(barre(3, 4, l=4.2, h=.7))
