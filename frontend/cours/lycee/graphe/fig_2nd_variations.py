# -*- coding: utf-8 -*-
"""Figures : Seconde — Variations et extremums."""
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import PchipInterpolator

from figlycee import (new_fig, _save, setup_repere, txt, I, tableau_variations, BLUE, ORANGE, GREEN, DARK, NEUTRAL,
                      RED)

BOITE = dict(fc="white", ec="none", pad=1.5)
XS, YS = [-3, -1, 2, 5], [2, -2, 3, 0]
F = PchipInterpolator(XS, YS)


def sens():
    fig, axs = plt.subplots(1, 2, figsize=(10.2, 4.4))
    fig.patch.set_facecolor("white")
    for ax, croit in zip(axs, (True, False)):
        ax.set_facecolor("white")
        ax.annotate("", xy=(5.4, 0), xytext=(-0.4, 0), arrowprops=dict(arrowstyle="->", lw=1.3, color=NEUTRAL))
        ax.annotate("", xy=(0, 4.6), xytext=(0, -0.4), arrowprops=dict(arrowstyle="->", lw=1.3, color=NEUTRAL))
        x = np.linspace(0.6, 4.8, 200)
        y = 0.6 + 3.4 * ((x - 0.6) / 4.2) ** 1.4 if croit else 4.0 - 3.4 * ((x - 0.6) / 4.2) ** 0.7
        col = BLUE if croit else ORANGE
        ax.plot(x, y, color=col, lw=2.8)
        u, v = 1.6, 3.9
        fu = np.interp(u, x, y)
        fv = np.interp(v, x, y)
        for a, fa, nu, nf in ((u, fu, "u", "f(u)"), (v, fv, "v", "f(v)")):
            ax.plot([a, a], [0, fa], color=NEUTRAL, lw=1.1, ls=":")
            ax.plot([0, a], [fa, fa], color=NEUTRAL, lw=1.1, ls=":")
            ax.scatter([a], [fa], s=30, color=DARK, zorder=6)
            txt(ax, a, -0.15, f"${nu}$", DARK, 14, ha="center", va="top")
            txt(ax, -0.12, fa, f"${nf}$", DARK, 13, ha="right", va="center")
        titre = "$f$ croissante : l’ordre est conservé" if croit else "$f$ décroissante : l’ordre est inversé"
        regle = "$u < v \\Rightarrow f(u) \\leq f(v)$" if croit else "$u < v \\Rightarrow f(u) \\geq f(v)$"
        txt(ax, 2.5, 5.0, titre, col, 13.5, ha="center", fontweight="bold")
        txt(ax, 2.5, -0.9, regle, DARK, 13.5, ha="center", va="top")
        ax.set_xlim(-1.4, 5.6)
        ax.set_ylim(-1.6, 5.5)
        ax.set_aspect("equal")
        ax.axis("off")
    _save(fig, I("2nd_variations_sens.png"))


def courbe():
    fig, ax = new_fig(7.4, 5.4)
    setup_repere(ax, (-3.8, 6.0), (-3.0, 4.2))
    for a, b, col in ((-3, -1, ORANGE), (-1, 2, BLUE), (2, 5, ORANGE)):
        x = np.linspace(a, b, 120)
        ax.plot(x, F(x), color=col, lw=2.8)
    ax.scatter([-3, 5], [2, 0], s=30, color=DARK, zorder=6)
    ax.scatter([2], [3], s=46, color=GREEN, zorder=7)
    ax.scatter([-1], [-2], s=46, color=RED, zorder=7)
    ax.plot([2, 2], [0, 3], color=GREEN, lw=1.1, ls=":")
    ax.plot([-1, -1], [0, -2], color=RED, lw=1.1, ls=":")
    txt(ax, 3.5, 3.3, "maximum $3$\natteint en $2$", GREEN, 12.5, ha="center", va="bottom", fontweight="bold",
        bbox=BOITE)
    txt(ax, -1.9, -2.3, "minimum $-2$\natteint en $-1$", RED, 12.5, ha="center", va="top", fontweight="bold",
        bbox=BOITE)
    txt(ax, 1.1, -3.3, "en bleu : $f$ croissante  ;  en orange : $f$ décroissante", DARK, 12.5, ha="center",
        va="top")
    ax.set_aspect("equal")
    ax.axis("off")
    _save(fig, I("2nd_variations_courbe.png"))


def tableau():
    tableau_variations(I("2nd_variations_tableau.png"), ["$-3$", "$-1$", "$2$", "$5$"],
                       [("$2$", "h"), ("$-2$", "b"), ("$3$", "h"), ("$0$", "b")], col_w=1.6)


sens()
courbe()
tableau()
