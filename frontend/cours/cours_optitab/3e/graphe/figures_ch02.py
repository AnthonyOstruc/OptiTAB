# -*- coding: utf-8 -*-
"""Figures du chapitre 2 (Puissances, racines, écriture scientifique) — 3ème OptiTAB."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fig3e import new_fig, finish, BLUE, ORANGE, DARK, DIR_COURS
import matplotlib.patches as mp


def carre_racine():
    """Carré d'aire 45 cm² et côté √45."""
    fig, ax = new_fig(5.6, 5.2)
    c = 4.0
    ax.add_patch(mp.Rectangle((0, 0), c, c, facecolor="#e8f4fd",
                              edgecolor=BLUE, lw=2.4, zorder=2))
    ax.text(c / 2, c / 2, "aire\n$45$ cm$^2$", fontsize=15, ha="center",
            va="center", color=DARK, fontweight="bold")
    ax.annotate("", xy=(c, -0.45), xytext=(0, -0.45),
                arrowprops=dict(arrowstyle="<->", lw=1.6, color=ORANGE))
    ax.text(c / 2, -0.85, r"côté $= \sqrt{45} \approx 6{,}71$ cm", fontsize=13.5,
            ha="center", color=ORANGE, fontweight="bold")
    finish(fig, ax, os.path.join(DIR_COURS, "puissances_3e_carre.png"),
           [(-0.4, -1.3), (c + 0.4, c + 0.4)], margin=0.15)


carre_racine()
print("Figures chapitre 2 : OK")
