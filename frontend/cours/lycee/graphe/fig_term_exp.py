# -*- coding: utf-8 -*-
"""Figures : Terminale — Fonction exponentielle (limites, étude, modèle)."""
import numpy as np
from matplotlib.ticker import FuncFormatter

from figlycee import (new_fig, _save, setup_repere, txt, I, tableau_variations, BLUE, ORANGE, GREEN, DARK, NEUTRAL,
                      RED, PURPLE)

BOITE = dict(fc="white", ec="none", pad=1.5)
GRID = "#d5dde3"
VIRGULE = FuncFormatter(lambda v, _: f"{v:g}".replace(".", ","))


def etude():
    fig, ax = new_fig(8.4, 5.2)
    setup_repere(ax, (-0.9, 8.4), (-0.85, 0.65), 1, 0.25)
    x = np.linspace(-0.4, 8.2, 400)
    ax.plot(x, x * np.exp(-x), color=BLUE, lw=2.6, zorder=5)
    ax.scatter([1], [np.exp(-1)], s=40, color=GREEN, zorder=6)
    ax.plot([1, 1], [0, np.exp(-1)], color=GREEN, lw=1.1, ls=":")
    txt(ax, 1.0, np.exp(-1) + 0.04, "$M$", GREEN, 15, ha="center", va="bottom", fontweight="bold")
    ax.scatter([2], [2 * np.exp(-2)], s=34, color=PURPLE, zorder=6)
    txt(ax, 2.1, 2 * np.exp(-2) + 0.03, "$I$", PURPLE, 15, va="bottom", fontweight="bold")
    txt(ax, 8.2, -0.45, "$f(x) = xe^{-x}$", BLUE, 15, ha="right", va="center", fontweight="bold")
    txt(ax, 3.7, -0.95, r"$M\left(1\,;\frac{1}{e}\right)$ maximum ; $I$ point d'inflexion d'abscisse $2$ ; asymptote $y = 0$ en $+\infty$",
        DARK, 12, ha="center", va="top")
    ax.set_aspect(3.2)
    ax.axis("off")
    _save(fig, I("term_exp_etude.png"))


def tableau():
    tableau_variations(I("term_exp_tableau.png"), ["$-\\infty$", "$1$", "$+\\infty$"],
                       [("$-\\infty$", "b"), ("$\\frac{1}{e}$", "h"), ("$0$", "b")], signe=["+", "0", "-"],
                       col_w=1.9, titre="$f'(x) = (1 - x)e^{-x}$, du signe de $1 - x$")


def modele():
    fig, ax = new_fig(8.2, 4.4)
    t = np.linspace(0, 12, 300)
    ax.plot(t, 5 * (1 - np.exp(-0.5 * t)), color=BLUE, lw=2.6)
    ax.axhline(5, color=RED, lw=1.5, ls="--")
    txt(ax, 11.8, 5.1, "$5$ V : valeur limite", RED, 12.5, ha="right", va="bottom")
    txt(ax, 4.2, 2.2, "$u(t) = 5\\left(1 - e^{-0{,}5t}\\right)$", BLUE, 14, fontweight="bold")
    ax.set_xlim(0, 12.4)
    ax.set_ylim(0, 6)
    ax.set_xlabel("temps $t$ (s)", fontsize=12, color=DARK)
    ax.set_ylabel("tension $u(t)$ (V)", fontsize=12, color=DARK)
    ax.grid(color=GRID, lw=0.6)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    _save(fig, I("term_exp_modele.png"))


etude()
tableau()
modele()
