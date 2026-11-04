# -*- coding: utf-8 -*-
"""Figures : Première — Variables aléatoires réelles."""
import numpy as np

from figlycee import new_fig, _save, txt, I, BLUE, ORANGE, GREEN, DARK, NEUTRAL, RED

GRID = "#d5dde3"


def loi():
    fig, ax = new_fig(7.6, 4.4)
    xs, ps = [-2, 1, 5], [1 / 2, 1 / 3, 1 / 6]
    labs = ["$\\frac{1}{2}$", "$\\frac{1}{3}$", "$\\frac{1}{6}$"]
    ax.bar(xs, ps, width=0.35, color=BLUE, zorder=3)
    for x, p, l in zip(xs, ps, labs):
        txt(ax, x, p + 0.02, l, BLUE, 15, ha="center", va="bottom", fontweight="bold")
    e = 1 / 6
    ax.axvline(e, color=RED, lw=1.8, ls="--", zorder=4)
    txt(ax, e + 0.12, 0.56, "$E(X) = \\frac{1}{6} \\approx 0{,}17$", RED, 13, va="center")
    ax.set_xticks([-2, -1, 0, 1, 2, 3, 4, 5])
    ax.set_xlim(-3, 6)
    ax.set_ylim(0, 0.65)
    ax.set_yticks([0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6])
    ax.set_yticklabels(["0", "0,1", "0,2", "0,3", "0,4", "0,5", "0,6"])
    ax.set_xlabel("gain $x_i$ (en euros)", fontsize=12, color=DARK)
    ax.set_ylabel("$P(X = x_i)$", fontsize=12, color=DARK)
    ax.grid(axis="y", color=GRID, lw=0.7, zorder=0)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    _save(fig, I("1er_va_loi.png"))


def simulation():
    rng = np.random.default_rng(5)
    n = 3000
    d = rng.integers(1, 7, n)
    g = np.where(d == 6, 5, np.where(d % 2 == 0, 1, -2))
    moy = np.cumsum(g) / np.arange(1, n + 1)
    fig, ax = new_fig(8.4, 4.4)
    ax.plot(np.arange(1, n + 1), moy, color=BLUE, lw=1.6)
    ax.axhline(1 / 6, color=RED, lw=1.6, ls="--")
    ax.set_xlim(0, n)
    ax.set_ylim(-1.5, 1.5)
    ax.set_yticks([-1.5, -1, -0.5, 0, 0.5, 1, 1.5])
    ax.set_yticklabels(["-1,5", "-1", "-0,5", "0", "0,5", "1", "1,5"])
    ax.set_xlabel("nombre de parties simulées", fontsize=12, color=DARK)
    ax.set_ylabel("gain moyen (euros)", fontsize=12, color=DARK)
    ax.grid(color=GRID, lw=0.7)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    txt(ax, n * 0.97, 1 / 6 + 0.12, "$E(X) = \\frac{1}{6}$", RED, 13, ha="right", va="bottom", fontweight="bold")
    txt(ax, n / 2, 1.25, "le gain moyen se rapproche de l’espérance", DARK, 12.5, ha="center")
    _save(fig, I("1er_va_simulation.png"))
    return moy[-1]


loi()
print("moyenne finale :", simulation())
