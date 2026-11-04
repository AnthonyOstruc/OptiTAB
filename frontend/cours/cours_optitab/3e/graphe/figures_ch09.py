# -*- coding: utf-8 -*-
"""Figures du chapitre 9 (Fonctions linéaires et affines) — 3ème OptiTAB."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fig3e import graphe, BLUE, ORANGE, GREEN, DIR_COURS, DIR_EXOS

# Cours — une linéaire (origine) et une affine (ordonnée à l'origine b)
def extra_cours(ax):
    ax.annotate("$b = -3$", (0, -3), textcoords="offset points", xytext=(10, -14),
                fontsize=12, color=ORANGE, fontweight="bold")
    ax.annotate("passe par l'origine", (0, 0), textcoords="offset points",
                xytext=(-105, 8), fontsize=10.5, color=BLUE, fontweight="bold")

graphe(
    os.path.join(DIR_COURS, "affines_3e_droites.png"),
    curves=[(lambda x: 1.5 * x, -3.2, 3.6, BLUE, ("linéaire : $f(x) = 1{,}5x$", 2.2)),
            (lambda x: 2 * x - 3, -1.2, 4.2, ORANGE, ("affine : $g(x) = 2x - 3$", 3.4))],
    points=[("", 0, 0, BLUE), ("", 0, -3, ORANGE)],
    xb=(-4.2, 5.6), yb=(-5.6, 6.2), extra=extra_cours, w=8.4, h=5.6,
)

# D4 — tracer f(x) = 1,5x avec O et A(2;3)
graphe(
    os.path.join(DIR_EXOS, "affines_3e_trace_lineaire.png"),
    curves=[(lambda x: 1.5 * x, -2.8, 3.4, BLUE, ("$f(x) = 1{,}5x$", 2.6))],
    points=[("$O$", 0, 0, ORANGE), ("$A(2\\,;3)$", 2, 3, ORANGE)],
    xb=(-3.6, 4.4), yb=(-4.6, 5.6), w=7.8, h=5.2,
)

# D5 — tracer g(x) = −x + 4 avec (0;4) et (4;0)
graphe(
    os.path.join(DIR_EXOS, "affines_3e_trace_affine.png"),
    curves=[(lambda x: -x + 4, -1.6, 5.6, BLUE, ("$g(x) = -x + 4$", 4.6))],
    points=[("", 0, 4, ORANGE), ("", 4, 0, ORANGE)],
    xb=(-2.6, 6.4), yb=(-2.2, 6.4), w=7.8, h=5.2,
)

# E4 — lecture des paramètres : f(x) = −2x + 3
graphe(
    os.path.join(DIR_EXOS, "affines_3e_lecture.png"),
    curves=[(lambda x: -2 * x + 3, -1.6, 3.4, BLUE, None)],
    points=[("", 0, 3, ORANGE)],
    xb=(-2.6, 4.4), yb=(-4.2, 6.6), w=7.8, h=5.2,
)

# E5 — deux droites parallèles : 4x − 1 et 4x + 6
graphe(
    os.path.join(DIR_EXOS, "affines_3e_paralleles.png"),
    curves=[(lambda x: 4 * x - 1, -1.8, 2.2, BLUE, ("$f(x) = 4x - 1$", 1.5)),
            (lambda x: 4 * x + 6, -3.2, 0.7, ORANGE, ("$g(x) = 4x + 6$", -2.4))],
    xb=(-4.2, 3.6), yb=(-8.2, 9.6), yt=2, w=7.8, h=5.6,
)

# P1 — deux abonnements : 20 + 3n et 8 + 5n, intersection (6 ; 38)
graphe(
    os.path.join(DIR_EXOS, "affines_3e_tarifs.png"),
    curves=[(lambda x: 20 + 3 * x, 0, 12, BLUE, ("A : $20 + 3n$", 9.6)),
            (lambda x: 8 + 5 * x, 0, 12, ORANGE, ("B : $8 + 5n$", 9.0))],
    points=[("$(6\\,;38)$", 6, 38, GREEN)],
    xb=(-0.8, 13.6), yb=(-5, 75), xt=1, yt=10,
    xlabel="séances", ylabel="coût (€)", w=8.6, h=5.4,
)
print("Figures chapitre 9 : OK")
