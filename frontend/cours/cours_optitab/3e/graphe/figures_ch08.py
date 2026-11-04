# -*- coding: utf-8 -*-
"""Figures du chapitre 8 (Notion de fonction) — 3ème OptiTAB."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fig3e import graphe, BLUE, ORANGE, GREEN, DIR_COURS, DIR_EXOS

# Cours — lire une image et des antécédents sur la courbe de f(x) = x² − 2
def extra_lecture(ax):
    # image de 2 : f(2) = 2
    ax.plot([2, 2], [0, 2], lw=1.6, color=ORANGE, linestyle="--")
    ax.plot([0, 2], [2, 2], lw=1.6, color=ORANGE, linestyle="--")
    ax.annotate("image de 2", (0.15, 2.25), fontsize=11, color=ORANGE, fontweight="bold")
    # antécédents de -1 : x = ±1
    ax.plot([-3.4, 3.4], [-1, -1], lw=1.5, color=GREEN, linestyle="--")
    ax.plot([1, 1], [-1, 0], lw=1.2, color=GREEN, linestyle=":")
    ax.plot([-1, -1], [-1, 0], lw=1.2, color=GREEN, linestyle=":")
    ax.annotate("antécédents de $-1$", (-3.3, -1.75), fontsize=11, color=GREEN,
                fontweight="bold")

graphe(
    os.path.join(DIR_COURS, "fonctions_3e_lecture.png"),
    curves=[(lambda x: x * x - 2, -2.6, 2.6, BLUE, ("$f(x) = x^2 - 2$", 1.9))],
    points=[("", 2, 2, ORANGE), ("", 1, -1, GREEN), ("", -1, -1, GREEN)],
    xb=(-3.6, 3.9), yb=(-2.9, 5.2), extra=extra_lecture, w=8.4, h=5.6,
)

# E2 — ligne brisée : sommets (−4;0), (−1;3), (1;−1), (3;1)
pts_brisee = [(-4, 0), (-1, 3), (1, -1), (3, 1)]
graphe(
    os.path.join(DIR_EXOS, "fonctions_3e_brisee.png"),
    segments=[(pts_brisee[i], pts_brisee[i + 1], {"color": BLUE, "ls": "-", "lw": 2.4})
              for i in range(3)],
    points=[("", *p, BLUE) for p in pts_brisee],
    xb=(-4.9, 4.2), yb=(-2.2, 4.2), w=8.4, h=5.2,
)

# E4 — intersection de f(x) = x + 2 et g(x) = 2x − 1
graphe(
    os.path.join(DIR_EXOS, "fonctions_3e_intersection.png"),
    curves=[(lambda x: x + 2, -2.5, 5.2, BLUE, ("$f(x) = x + 2$", -1.4)),
            (lambda x: 2 * x - 1, -1.6, 4.1, ORANGE, ("$g(x) = 2x - 1$", 3.6))],
    points=[("", 3, 5, GREEN)],
    xb=(-3.2, 6.2), yb=(-4.2, 7.6), w=8.4, h=5.6,
)

# P4 — promenade : distance au départ en fonction du temps
pts_prom = [(0, 0), (10, 600), (15, 600), (25, 0)]
graphe(
    os.path.join(DIR_EXOS, "fonctions_3e_promenade.png"),
    segments=[(pts_prom[i], pts_prom[i + 1], {"color": BLUE, "ls": "-", "lw": 2.4})
              for i in range(3)],
    points=[("", *p, BLUE) for p in pts_prom],
    xb=(-1.5, 28), yb=(-80, 760), xt=5, yt=100,
    xlabel="temps (min)", ylabel="distance (m)", w=8.6, h=5.2,
)
print("Figures chapitre 8 : OK")
