# -*- coding: utf-8 -*-
"""Figures de « Arrondir un nombre » : droite graduée entre deux centièmes."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from fig_commun import PREAMBULE_EXTRA, f, tikz, carte  # noqa: E402,F401

FIGURES = {}


def droite(a_txt, b_txt, x_val, val_txt, l=6.0, milieu=True):
    """Segment [a ; b] gradué en 10, point placé à x_val (fraction de 0 à 1)."""
    L = [r"\draw[otMuted,line width=.8pt] (-.3,0) -- (%s,0);" % f(l + .3)]
    for i in range(11):
        x = l * i / 10
        hh = .2 if i in (0, 10) else (.14 if i == 5 else .08)
        L.append(r"\draw[otNavy,line width=%spt] (%s,%s) -- (%s,%s);" % ("1" if i in (0, 10) else ".6", f(x), f(-hh), f(x), f(hh)))
    L.append(r"\node[grad,anchor=north] at (0,-.28) {$%s$};" % a_txt)
    L.append(r"\node[grad,anchor=north] at (%s,-.28) {$%s$};" % (f(l), b_txt))
    if milieu:
        L.append(r"\node[note,anchor=north] at (%s,-.28) {milieu};" % f(l / 2))
    x = l * x_val
    L.append(r"\fill[otGreenDark] (%s,0) circle (2.6pt);" % f(x))
    L.append(r"\node[etiq,anchor=south,text=otGreenDark] at (%s,.3) {$%s$};" % (f(x), val_txt))
    # flèche sous les graduations écrites (aucun texte traversé)
    L.append(r"\draw[otGreenDark,line width=1pt,-{Stealth[length=2.2mm]}] (%s,-.85) -- (0,-.85);" % f(x + .4))
    L.append(r"\node[note,anchor=west,text=otGreenDark] at (%s,-.85) {plus proche de $%s$};" % (f(x + .5), a_txt))
    return L


# 3,14159 entre 3,14 et 3,15 : position 0,159 du segment.
FIGURES["arrondi_droite"] = tikz(droite("3{,}14", "3{,}15", .159, "3{,}14159"))
FIGURES["carte_arrondi"] = carte(droite("3{,}14", "3{,}15", .159, "3{,}14159", l=4.8, milieu=False))
