# -*- coding: utf-8 -*-
"""Figures : Seconde — Représenter algébriquement et graphiquement les fonctions."""
import matplotlib.pyplot as plt
import numpy as np

from figlycee import (new_fig, _save, setup_repere, txt, I, tableau_signes, BLUE, ORANGE, GREEN, DARK, NEUTRAL,
                      RED, PURPLE)

BOITE = dict(fc="white", ec="none", pad=1.5)
f = lambda x: x ** 2 - 2 * x - 3  # noqa: E731


def lecture():
    fig, ax = new_fig(6.6, 6.4)
    setup_repere(ax, (-2.6, 5.2), (-4.8, 6.6))
    x = np.linspace(-1.9, 4.15, 300)
    ax.plot(x, f(x), color=BLUE, lw=2.6)
    # image de 4
    ax.plot([4, 4], [0, 5], color=GREEN, lw=1.6, ls="--")
    ax.plot([0, 4], [5, 5], color=GREEN, lw=1.6, ls="--")
    ax.scatter([4], [5], s=30, color=GREEN, zorder=6)
    txt(ax, 2.0, 5.35, "$f(4) = 5$", GREEN, 13, ha="center", fontweight="bold", bbox=BOITE)
    # antécédents de -3
    ax.plot([-2.4, 4.9], [-3, -3], color=ORANGE, lw=1.6, ls="--")
    for a in (0, 2):
        ax.plot([a, a], [-3, 0], color=ORANGE, lw=1.4, ls=":")
        ax.scatter([a], [-3], s=30, color=ORANGE, zorder=6)
    txt(ax, 3.7, -3.35, "antécédents\nde $-3$ : $0$ et $2$", ORANGE, 12.5, ha="center", va="top")
    txt(ax, -2.0, 2.0, "$\\mathcal{C}_f$", BLUE, 15, ha="right", fontweight="bold")
    _fin(ax)
    _save(fig, I("2nd_repfct_lecture.png"))


def _fin(ax):
    ax.set_aspect("equal")
    ax.axis("off")


def resolution():
    fig, ax = new_fig(6.6, 6.4)
    setup_repere(ax, (-2.6, 5.4), (-4.8, 6.8))
    x = np.linspace(-1.9, 4.2, 300)
    ax.plot(x, f(x), color=BLUE, lw=2.6)
    x = np.linspace(-2.4, 5.0, 10)
    ax.plot(x, x + 1, color=ORANGE, lw=2.4)
    for a in (-1, 4):
        ax.plot([a, a], [0, a + 1], color=NEUTRAL, lw=1.2, ls=":")
        ax.scatter([a], [a + 1], s=34, color=RED, zorder=6)
    ax.plot([-1, 4], [0, 0], color=GREEN, lw=6, solid_capstyle="butt", alpha=0.8)
    txt(ax, -1.95, 2.0, "$\\mathcal{C}_f$", BLUE, 15, ha="right", fontweight="bold")
    txt(ax, 4.9, 6.4, "$\\mathcal{C}_g$", ORANGE, 15, ha="right", fontweight="bold")
    txt(ax, 1.5, -5.2, "$f(x) \\leq g(x) \\Leftrightarrow x \\in [-1\\,;4]$", GREEN, 13.5, ha="center", va="top",
        fontweight="bold")
    _fin(ax)
    _save(fig, I("2nd_repfct_resolution.png"))


def parite():
    fig, axs = plt.subplots(1, 2, figsize=(10.4, 4.6))
    fig.patch.set_facecolor("white")
    ax = axs[0]
    setup_repere(ax, (-3.2, 3.2), (-1.8, 4.6), unit_labels=False)
    g = lambda x: x ** 4 / 2 - 2 * x ** 2 + 1  # noqa: E731
    x = np.linspace(-2.32, 2.32, 300)
    ax.plot(x, g(x), color=BLUE, lw=2.6)
    a = 2.2
    ax.plot([-a, a], [g(a), g(a)], color=ORANGE, lw=1.3, ls="--")
    for s, nom in ((1, "M"), (-1, "M'")):
        ax.scatter([s * a], [g(a)], s=34, color=ORANGE, zorder=6)
        txt(ax, s * (a + 0.25), g(a), f"${nom}$", ORANGE, 14, ha="left" if s > 0 else "right", va="center")
    txt(ax, 0, -2.3, "fonction paire : $f(-x) = f(x)$\nsymétrie par rapport à l’axe des ordonnées", GREEN, 12,
        ha="center", va="top")
    _fin(ax)
    ax = axs[1]
    setup_repere(ax, (-3.2, 3.2), (-3.2, 3.2), unit_labels=False)
    h = lambda x: x ** 3 - 3 * x  # noqa: E731
    x = np.linspace(-2.18, 2.18, 300)
    ax.plot(x, h(x), color=PURPLE, lw=2.6)
    ax.plot([-2, 2], [-2, 2], color=ORANGE, lw=1.3, ls="--")
    ax.scatter([2, -2], [2, -2], s=34, color=ORANGE, zorder=6)
    txt(ax, 2.25, 2, "$N$", ORANGE, 14, va="center")
    txt(ax, -2.25, -2, "$N'$", ORANGE, 14, ha="right", va="center")
    txt(ax, 0, -3.5, "fonction impaire : $f(-x) = -f(x)$\nsymétrie par rapport à l’origine $O$", GREEN, 12,
        ha="center", va="top")
    _fin(ax)
    _save(fig, I("2nd_repfct_parite.png"))


def signes():
    tableau_signes(I("2nd_repfct_signes.png"), ["$-1$", "$3$"],
                   [("$x+1$", ["-", "0", "+", "", "+"]),
                    ("$x-3$", ["-", "", "-", "0", "+"]),
                    ("$(x+1)(x-3)$", ["+", "0", "-", "0", "+"])], lab_w=3.4, col_w=1.4)


lecture()
resolution()
parite()
signes()
