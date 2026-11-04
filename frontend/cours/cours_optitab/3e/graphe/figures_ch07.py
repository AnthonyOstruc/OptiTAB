# -*- coding: utf-8 -*-
"""Figures du chapitre 7 (Grandeurs) — 3ème OptiTAB."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fig3e import new_fig, finish, BLUE, ORANGE, GREEN, DARK, DIR_COURS
import matplotlib.patches as mp


def triangle_dvt():
    """Le triangle d = v × t et les trois formules."""
    fig, ax = new_fig(8.6, 4.6)
    # triangle découpé
    ax.add_patch(mp.Polygon([(-2.2, 0), (2.2, 0), (0, 3.1)], closed=True,
                            fill=False, edgecolor=DARK, lw=2.4))
    ax.plot([-1.49, 1.49], [1.0, 1.0], lw=2.0, color=DARK)
    ax.plot([0, 0], [0, 1.0], lw=2.0, color=DARK)
    ax.text(0, 1.9, "$d$", fontsize=22, ha="center", va="center", color=BLUE,
            fontweight="bold")
    ax.text(-0.75, 0.48, "$v$", fontsize=20, ha="center", va="center",
            color=ORANGE, fontweight="bold")
    ax.text(0.75, 0.48, "$t$", fontsize=20, ha="center", va="center",
            color=GREEN, fontweight="bold")
    ax.text(0, -0.55, "cacher la grandeur cherchée…", fontsize=11, ha="center",
            color="0.45", style="italic")
    # les trois formules
    for y, txt in [(2.5, r"$d = v \times t$"), (1.55, r"$v = \dfrac{d}{t}$"),
                   (0.4, r"$t = \dfrac{d}{v}$")]:
        ax.text(4.3, y, txt, fontsize=16, ha="center", va="center", color=DARK)
    ax.add_patch(mp.FancyBboxPatch((3.1, -0.15), 2.4, 3.3,
                 boxstyle="round,pad=0.12", fill=False, edgecolor=BLUE, lw=1.8))
    finish(fig, ax, os.path.join(DIR_COURS, "grandeurs_3e_vitesse.png"),
           [(-2.6, -0.9), (5.9, 3.5)], margin=0.2)


triangle_dvt()
print("Figures chapitre 7 : OK")
