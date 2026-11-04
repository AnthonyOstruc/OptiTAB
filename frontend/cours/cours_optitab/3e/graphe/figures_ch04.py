# -*- coding: utf-8 -*-
"""Figures du chapitre 4 (Calcul littéral) — 3ème OptiTAB."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fig3e import new_fig, finish, BLUE, ORANGE, DARK, DIR_COURS, DIR_EXOS
import matplotlib.patches as mp


def distributivite():
    """Modèle en aires : k(a+b) = ka + kb."""
    fig, ax = new_fig(8.0, 3.4)
    k, a, b = 2.0, 3.6, 2.2
    ax.add_patch(mp.Rectangle((0, 0), a, k, facecolor="#d6eafc", edgecolor=BLUE, lw=2))
    ax.add_patch(mp.Rectangle((a, 0), b, k, facecolor="#fdebd0", edgecolor=ORANGE, lw=2))
    ax.text(a / 2, k / 2, r"$k \times a$", fontsize=15, ha="center", va="center", color=BLUE, fontweight="bold")
    ax.text(a + b / 2, k / 2, r"$k \times b$", fontsize=15, ha="center", va="center", color=ORANGE, fontweight="bold")
    ax.annotate("", xy=(a, -0.35), xytext=(0, -0.35), arrowprops=dict(arrowstyle="<->", lw=1.4, color=BLUE))
    ax.text(a / 2, -0.7, "$a$", fontsize=14, ha="center", color=BLUE)
    ax.annotate("", xy=(a + b, -0.35), xytext=(a, -0.35), arrowprops=dict(arrowstyle="<->", lw=1.4, color=ORANGE))
    ax.text(a + b / 2, -0.7, "$b$", fontsize=14, ha="center", color=ORANGE)
    ax.annotate("", xy=(-0.35, k), xytext=(-0.35, 0), arrowprops=dict(arrowstyle="<->", lw=1.4, color=DARK))
    ax.text(-0.7, k / 2, "$k$", fontsize=14, va="center", ha="center", color=DARK)
    ax.text((a + b) / 2, k + 0.45, r"aire totale $= k(a+b) = ka + kb$", fontsize=14,
            ha="center", color=DARK, fontweight="bold")
    finish(fig, ax, os.path.join(DIR_COURS, "calcul_litteral_3e_distributivite.png"),
           [(-1.1, -1.1), (a + b + 0.3, k + 0.9)], margin=0.15)


def bordure():
    """Carré de côté x entouré d'une bordure de largeur 2."""
    fig, ax = new_fig(5.8, 5.4)
    x, e = 3.2, 1.0
    big = x + 2 * e
    ax.add_patch(mp.Rectangle((0, 0), big, big, facecolor="#fdebd0", edgecolor=ORANGE, lw=2.2))
    ax.add_patch(mp.Rectangle((e, e), x, x, facecolor="#d6eafc", edgecolor=BLUE, lw=2.2))
    ax.text(e + x / 2, e + x / 2, "$x$", fontsize=16, ha="center", va="center",
            color=BLUE, fontweight="bold")
    ax.annotate("", xy=(e + x, e + x / 2), xytext=(e, e + x / 2), arrowprops=dict(arrowstyle="<->", lw=1.3, color=BLUE))
    ax.text(big / 2, -0.5, "côté du grand carré : $x + 4$", fontsize=12.5,
            ha="center", color=ORANGE, fontweight="bold")
    ax.annotate("", xy=(big, big + 0.3), xytext=(big - e, big + 0.3),
                arrowprops=dict(arrowstyle="<->", lw=1.3, color=ORANGE))
    ax.text(big - e / 2, big + 0.6, "2 cm", fontsize=11.5, ha="center", color=ORANGE)
    ax.text(big / 2, e / 2, "bordure", fontsize=11.5, ha="center", va="center",
            color=ORANGE, style="italic")
    finish(fig, ax, os.path.join(DIR_EXOS, "calcul_litteral_3e_bordure.png"),
           [(-0.4, -0.9), (big + 0.4, big + 1.0)], margin=0.15)


distributivite()
bordure()
print("Figures chapitre 4 : OK")
