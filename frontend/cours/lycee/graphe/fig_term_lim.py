# -*- coding: utf-8 -*-
"""Figures : Terminale — Limites de fonctions."""
import numpy as np
from matplotlib.ticker import FuncFormatter

from figlycee import new_fig, _save, setup_repere, txt, I, BLUE, ORANGE, GREEN, DARK, NEUTRAL, RED, PURPLE

BOITE = dict(fc="white", ec="none", pad=1.5)
GRID = "#d5dde3"
VIRGULE = FuncFormatter(lambda v, _: f"{v:g}".replace(".", ","))


def asymptotes():
    fig, ax = new_fig(7.2, 6.2)
    setup_repere(ax, (-4.6, 6.6), (-4.4, 8.4))
    f = lambda x: (2 * x + 1) / (x - 1)  # noqa: E731
    for a, b in ((-4.4, 0.72), (1.33, 6.4)):
        x = np.linspace(a, b, 300)
        ax.plot(x, f(x), color=BLUE, lw=2.6)
    ax.axvline(1, color=RED, lw=1.6, ls="--")
    ax.axhline(2, color=GREEN, lw=1.6, ls="--")
    txt(ax, 1.15, 7.9, "asymptote verticale $x = 1$", RED, 12, va="top", bbox=BOITE)
    txt(ax, 6.4, 1.75, "asymptote horizontale $y = 2$", GREEN, 12, ha="right", va="top", bbox=BOITE)
    txt(ax, 3.4, 5.3, "$f(x) = \\frac{2x + 1}{x - 1}$", BLUE, 14, bbox=BOITE)
    ax.set_aspect(0.8)
    ax.axis("off")
    _save(fig, I("term_lim_asymptotes.png"))


def gendarmes():
    fig, ax = new_fig(8.6, 4.4)
    x = np.linspace(0.5, 30, 800)
    ax.plot(x, 1 / x, color=ORANGE, lw=1.6)
    ax.plot(x, -1 / x, color=GREEN, lw=1.6)
    ax.plot(x, np.sin(x) / x, color=BLUE, lw=2.4)
    ax.axhline(0, color=NEUTRAL, lw=1)
    txt(ax, 24, 0.09, "$\\frac{1}{x}$", ORANGE, 18, ha="center")
    txt(ax, 24, -0.13, "$-\\frac{1}{x}$", GREEN, 18, ha="center")
    txt(ax, 9, 0.55, "$-\\frac{1}{x} \\leq \\frac{\\sin x}{x} \\leq \\frac{1}{x}$ pour $x > 0$, donc $\\frac{\\sin x}{x} \\rightarrow 0$",
        BLUE, 13, ha="left")
    ax.set_xlim(0, 31)
    ax.set_ylim(-0.8, 0.8)
    ax.yaxis.set_major_formatter(VIRGULE)
    ax.set_xlabel("$x$", fontsize=13, color=DARK)
    ax.grid(color=GRID, lw=0.6)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    _save(fig, I("term_lim_gendarmes.png"))


def croissances():
    fig, ax = new_fig(8.6, 4.6)
    x = np.linspace(0, 7, 400)
    ax.plot(x, np.exp(x), color=BLUE, lw=2.6)
    ax.plot(x, x ** 2, color=GREEN, lw=2)
    ax.plot(x, x ** 3, color=ORANGE, lw=2)
    ax.set_xlim(0, 7.6)
    ax.set_ylim(0, 420)
    txt(ax, 6.0, 405, "$e^x$", BLUE, 15, ha="right", va="top", fontweight="bold")
    txt(ax, 7.05, 343, "$x^3$", ORANGE, 15, va="center", fontweight="bold")
    txt(ax, 7.05, 49, "$x^2$", GREEN, 15, va="center", fontweight="bold")
    txt(ax, 0.3, 300, "l’exponentielle finit par dépasser\ntoute puissance de $x$ :\n$\\frac{e^x}{x^n} \\rightarrow +\\infty$ quand $x \\rightarrow +\\infty$",
        DARK, 12.5, va="center")
    ax.set_xlabel("$x$", fontsize=13, color=DARK)
    ax.grid(color=GRID, lw=0.6)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    _save(fig, I("term_lim_croissances.png"))


asymptotes()
gendarmes()
croissances()
