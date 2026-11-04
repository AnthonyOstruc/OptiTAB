# -*- coding: utf-8 -*-
"""Figures : Seconde — Calcul littéral."""
import numpy as np
from matplotlib.patches import Rectangle

from figlycee import (new_fig, _save, setup_repere, droite, intervalle, tableau_signes, txt, cadre, I, BLUE,
                      ORANGE, GREEN, DARK, NEUTRAL)


def carre_somme():
    fig, ax = new_fig(6.4, 5.2)
    a, b = 3.0, 1.6
    for (x, y, w, h, fc, s) in [(0, b, a, a, "#d6eafc", "$a^2$"), (a, b, b, a, "#fdebd0", "$ab$"),
                                (0, 0, a, b, "#fdebd0", "$ab$"), (a, 0, b, b, "#e8f5e9", "$b^2$")]:
        ax.add_patch(Rectangle((x, y), w, h, facecolor=fc, edgecolor=DARK, lw=1.8))
        txt(ax, x + w / 2, y + h / 2, s, DARK, 18, ha="center", va="center")
    for (x1, x2, y, s) in [(0, a, a + b + 0.25, "$a$"), (a, a + b, a + b + 0.25, "$b$")]:
        ax.annotate("", xy=(x2, y), xytext=(x1, y), arrowprops=dict(arrowstyle="<->", color=NEUTRAL))
        txt(ax, (x1 + x2) / 2, y + 0.12, s, DARK, 15, ha="center", va="bottom")
    for (y1, y2, x, s) in [(b, a + b, -0.25, "$a$"), (0, b, -0.25, "$b$")]:
        ax.annotate("", xy=(x, y2), xytext=(x, y1), arrowprops=dict(arrowstyle="<->", color=NEUTRAL))
        txt(ax, x - 0.15, (y1 + y2) / 2, s, DARK, 15, ha="right", va="center")
    txt(ax, (a + b) / 2, -0.55, "$(a+b)^2 = a^2 + 2ab + b^2$", GREEN, 17, ha="center", va="top",
        fontweight="bold")
    cadre(ax, (-1.0, a + b + 0.4), (-1.4, a + b + 0.9))
    _save(fig, I("2nd_calcul_litteral_carre.png"))


def signes():
    tableau_signes(I("2nd_calcul_litteral_signes.png"), ["$2$", "$3$"],
                   [("$2x-4$", ["-", "0", "+", "", "+"]),
                    ("$-x+3$", ["+", "", "+", "0", "-"]),
                    ("$(2x-4)(-x+3)$", ["-", "0", "+", "0", "-"])], lab_w=3.6, col_w=1.4)


def carre_egal():
    fig, ax = new_fig(7.0, 5.0)
    setup_repere(ax, (-4.3, 4.3), (-2.2, 11), 1, 2)
    x = np.linspace(-3.6, 3.6, 200)
    ax.plot(x, x ** 2, color=BLUE, lw=2.6)
    ax.plot([-4.2, 4.2], [9, 9], color=GREEN, lw=1.8)
    ax.plot([-4.2, 4.2], [-1, -1], color=ORANGE, lw=1.8)
    for s in (-3, 3):
        ax.plot([s, s], [0, 9], color=GREEN, lw=1, ls="--")
        ax.scatter([s], [9], s=50, color=GREEN, zorder=5)
    txt(ax, 0, 6.6, "$y=9$ : deux solutions\n$-3$ et $3$", GREEN, 12, ha="center",
        bbox=dict(fc="white", ec="none", alpha=0.85))
    txt(ax, 4.1, -1.6, "$y=-1$ : aucune solution", ORANGE, 12, ha="right")
    txt(ax, -3.9, 6.0, "$y=x^2$", BLUE, 14)
    ax.axis("off")
    _save(fig, I("2nd_calcul_litteral_carre_egal.png"))


def inequation():
    fig, ax = new_fig(8.0, 1.9)
    droite(ax, 0, -1.6, 6.6, range(-1, 7))
    intervalle(ax, 0, 2, None, False, False, BLUE, hi=6.4)
    txt(ax, 2.5, 0.45, "$3x-6>0 \\Leftrightarrow x>2 \\Leftrightarrow x\\in\\,]2\\,;+\\infty[$", BLUE, 14, ha="center", va="bottom")
    cadre(ax, (-1.8, 6.9), (-0.7, 1.1))
    _save(fig, I("2nd_calcul_litteral_inequation.png"))


carre_somme()
signes()
carre_egal()
inequation()
