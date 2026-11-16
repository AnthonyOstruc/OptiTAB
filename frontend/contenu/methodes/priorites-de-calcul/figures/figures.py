# -*- coding: utf-8 -*-
"""Figures de « Priorités de calcul » : un calcul effectué étape par étape."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from fig_commun import PREAMBULE_EXTRA, f, tikz, carte  # noqa: E402,F401

FIGURES = {}

# 7 + 3 × (8 − 2)² = 7 + 3 × 6² = 7 + 3 × 36 = 7 + 108 = 115
ETAPES = [
    (r"7 + 3 \times (\underline{8 - 2})^2", "parenthèses"),
    (r"7 + 3 \times \underline{6^2}", "puissance"),
    (r"7 + \underline{3 \times 36}", "multiplication"),
    (r"\underline{7 + 108}", "addition"),
    (r"115", ""),
]
assert 7 + 3 * (8 - 2) ** 2 == 115


def etapes(lignes, dy=.78, note=True):
    L = []
    for i, (expr, nom) in enumerate(lignes):
        y = -i * dy
        signe = "" if i == 0 else "= "
        coul = "otGreenDark" if i == len(lignes) - 1 else "otInk"
        L.append(r"\node[etiq,anchor=base east,font=\fontsize{12.5}{15}\selectfont] at (0,%s) {$%s$};" % (f(y), signe))
        L.append(r"\node[etiq,anchor=base west,text=%s,font=\fontsize{12.5}{15}\selectfont] at (0,%s) {$%s$};" % (coul, f(y), expr))
        if note and nom:
            L.append(r"\node[note,anchor=base west,text=otNavy] at (3.9,%s) {%d. %s};" % (f(y), i + 1, nom))
    return L


FIGURES["priorites_etapes"] = tikz(etapes(ETAPES))
FIGURES["carte_priorites"] = carte(etapes(ETAPES, dy=.62, note=False))
