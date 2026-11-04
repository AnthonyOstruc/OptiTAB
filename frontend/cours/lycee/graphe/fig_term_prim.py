# -*- coding: utf-8 -*-
"""Figures : Terminale — Primitives."""
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import FuncFormatter

from figlycee import new_fig, _save, setup_repere, txt, I, BLUE, ORANGE, GREEN, DARK, NEUTRAL, RED, PURPLE

BOITE = dict(fc="white", ec="none", pad=1.5)


def famille():
    fig, ax = new_fig(7.0, 6.0)
    setup_repere(ax, (-2.8, 2.8), (-2.6, 6.6))
    x = np.linspace(-2.4, 2.4, 300)
    for C in (-2, -1, 0, 1, 3, 4):
        y = x ** 2 + C
        ok = y <= 6.3
        ax.plot(x[ok], y[ok], color="#aab7c4", lw=1.3)
    y = x ** 2 + 2
    ok = y <= 6.3
    ax.plot(x[ok], y[ok], color=BLUE, lw=2.8)
    ax.scatter([1], [3], s=40, color=RED, zorder=6)
    txt(ax, 1.12, 2.85, "$(1\\,;3)$", RED, 13, va="top", bbox=BOITE)
    txt(ax, 0, -3.0, "en gris : primitives $F(x) = x^2 + C$ de $f(x) = 2x$\nen bleu : la seule qui passe par $(1\\,;3)$, $F(x) = x^2 + 2$",
        DARK, 12, ha="center", va="top")
    ax.set_aspect(0.55)
    ax.axis("off")
    _save(fig, I("term_prim_famille.png"))


def lien():
    fig, axs = plt.subplots(2, 1, figsize=(7.4, 6.4), sharex=True)
    fig.patch.set_facecolor("white")
    x = np.linspace(-2.2, 2.2, 300)
    for ax, y, col, nom in ((axs[0], x ** 2 - 1, ORANGE, "$f(x) = x^2 - 1$"),
                            (axs[1], x ** 3 / 3 - x, BLUE, "$F(x) = \\frac{x^3}{3} - x$")):
        ax.axhline(0, color=NEUTRAL, lw=1)
        ax.plot(x, y, color=col, lw=2.6)
        for v in (-1, 1):
            ax.axvline(v, color=GREEN, lw=1, ls=":")
        ax.text(0.55, 0.86, nom, transform=ax.transAxes, fontsize=13, color=col, fontweight="bold")
        for s in ("top", "right"):
            ax.spines[s].set_visible(False)
        ax.tick_params(labelsize=10)
        ax.yaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{v:g}".replace(".", ",")))
    axs[0].fill_between(x, x ** 2 - 1, 0, where=(x ** 2 - 1) < 0, color="#fdebd0")
    axs[0].text(0, -0.55, "$f < 0$", ha="center", fontsize=12, color=ORANGE)
    axs[1].text(0, 0.35, "$F$ décroissante", ha="center", fontsize=12, color=BLUE)
    axs[1].text(-1.5, -1.1, "$F$ croissante", ha="center", fontsize=11, color=BLUE)
    axs[1].text(1.5, -0.95, "$F$ croissante", ha="center", fontsize=11, color=BLUE)
    axs[1].set_xlabel("$x$", fontsize=13)
    fig.suptitle("$F' = f$ : le signe de $f$ donne les variations de $F$", fontsize=13, color=DARK)
    fig.tight_layout()
    _save(fig, I("term_prim_lien.png"))


famille()
lien()
