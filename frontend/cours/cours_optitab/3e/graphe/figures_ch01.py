# -*- coding: utf-8 -*-
"""Figures du chapitre 1 (Nombres rationnels et fractions) — 3ème OptiTAB."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fig3e import (new_fig, finish, BLUE, ORANGE, GREEN, DARK, GRID,
                   DIR_COURS, DIR_EXOS)
import numpy as np


def barre_fraction(path, n, k, total_txt, part_txt, titre, couleur=ORANGE,
                   reste_txt=None):
    """Barre découpée en n parts, k coloriées."""
    fig, ax = new_fig(8.6, 2.6)
    w, h = 10.0, 1.4
    for i in range(n):
        x = i * w / n
        face = couleur if i < k else "#eef2f5"
        ax.add_patch(__import__("matplotlib").patches.Rectangle(
            (x, 0), w / n, h, facecolor=face, edgecolor=DARK, lw=1.4, zorder=2))
    ax.annotate("", xy=(w, -0.55), xytext=(0, -0.55),
                arrowprops=dict(arrowstyle="<->", lw=1.4, color=DARK))
    ax.text(w / 2, -1.05, total_txt, fontsize=12.5, ha="center", color=DARK)
    ax.annotate("", xy=(k * w / n, h + 0.5), xytext=(0, h + 0.5),
                arrowprops=dict(arrowstyle="<->", lw=1.4, color=couleur))
    ax.text(k * w / n / 2, h + 0.85, part_txt, fontsize=12.5, ha="center",
            color=couleur, fontweight="bold")
    if reste_txt:
        ax.text((k * w / n + w) / 2, h / 2, reste_txt, fontsize=11.5, ha="center",
                va="center", color=DARK)
    ax.text(w / 2, h + 1.55, titre, fontsize=13, ha="center", color=DARK,
            fontweight="bold")
    finish(fig, ax, path, [(-0.4, -1.5), (w + 0.4, h + 2.0)], margin=0.1)


# 1. Cours : les 3/5 de 40
barre_fraction(os.path.join(DIR_COURS, "fractions_3e_quantite.png"),
               5, 3, "le tout : 40", r"$\frac{3}{5}$ de 40 = 24",
               "Prendre une fraction d'une quantité")

# 2. Cours : droite graduée avec des fractions
def droite_graduee():
    fig, ax = new_fig(8.8, 2.2)
    ax.annotate("", xy=(2.3, 0), xytext=(-0.3, 0),
                arrowprops=dict(arrowstyle="->", lw=1.6, color=DARK))
    for v in [0, 1, 2]:
        ax.plot([v, v], [-0.09, 0.09], lw=1.8, color=DARK)
        ax.text(v, -0.33, str(v), fontsize=13, ha="center", color=DARK)
    for v in np.arange(0, 2.01, 0.25):
        ax.plot([v, v], [-0.05, 0.05], lw=0.9, color=DARK)
    for frac, val, col in [(r"$\frac{1}{4}$", 0.25, BLUE),
                           (r"$\frac{2}{3}$", 2 / 3, ORANGE),
                           (r"$\frac{5}{6}$", 5 / 6, GREEN),
                           (r"$\frac{3}{2}$", 1.5, BLUE)]:
        ax.scatter([val], [0], s=55, color=col, zorder=5)
        ax.text(val, 0.22, frac, fontsize=14, ha="center", color=col,
                fontweight="bold")
    finish(fig, ax, os.path.join(DIR_COURS, "fractions_3e_droite.png"),
           [(-0.4, -0.6), (2.4, 0.6)], margin=0.1, equal=False)

droite_graduee()

# 3. Exercice P1 : le livre (2/5 lundi, 1/5 mardi, 2/5 reste)
def barre_lecture():
    fig, ax = new_fig(8.6, 2.6)
    w, h = 10.0, 1.4
    import matplotlib.patches as mp
    zones = [(0, 2, BLUE, "lundi\n2/5"), (2, 3, ORANGE, "mardi\n1/5"),
             (3, 5, "#eef2f5", "reste\n2/5")]
    for i in range(5):
        x = i * w / 5
        face = next(c for a, b, c, _ in zones if a <= i < b)
        ax.add_patch(mp.Rectangle((x, 0), w / 5, h, facecolor=face,
                                  edgecolor=DARK, lw=1.4, zorder=2))
    for a, b, c, lab in zones:
        col = "white" if c in (BLUE, ORANGE) else DARK
        ax.text((a + b) / 2 * w / 5, h / 2, lab, fontsize=11.5, ha="center",
                va="center", color=col, fontweight="bold")
    ax.annotate("", xy=(w, -0.5), xytext=(0, -0.5),
                arrowprops=dict(arrowstyle="<->", lw=1.4, color=DARK))
    ax.text(w / 2, -1.0, "le livre entier : 270 pages", fontsize=12.5,
            ha="center", color=DARK)
    finish(fig, ax, os.path.join(DIR_EXOS, "fractions_3e_lecture.png"),
           [(-0.4, -1.4), (w + 0.4, h + 0.5)], margin=0.1)

barre_lecture()
print("Figures chapitre 1 : OK")
