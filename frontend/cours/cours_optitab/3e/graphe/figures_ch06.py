# -*- coding: utf-8 -*-
"""Figures du chapitre 6 (Proportionnalité) — 3ème OptiTAB."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fig3e import graphe, BLUE, ORANGE, DIR_COURS

# Proportionnel (droite par l'origine) vs non proportionnel (forfait)
graphe(
    os.path.join(DIR_COURS, "proportionnalite_3e_graphique.png"),
    curves=[
        (lambda x: 2 * x, 0, 7.6, BLUE, ("proportionnel : $y = 2x$", 4.6)),
        (lambda x: 5 + 1.2 * x, 0, 7.6, ORANGE, ("non proportionnel : $y = 5 + 1{,}2x$", 1.1)),
    ],
    points=[("", 0, 0, BLUE)],
    xb=(-0.6, 8.2), yb=(-1.2, 16.5), xt=1, yt=2,
    xlabel="quantité", ylabel="prix",
    w=8.4, h=5.2,
)
print("Figures chapitre 6 : OK")
