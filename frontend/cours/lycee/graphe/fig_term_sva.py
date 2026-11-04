# -*- coding: utf-8 -*-
"""Figures : Terminale — Sommes de variables aléatoires."""
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import FuncFormatter

from figlycee import _save, I, BLUE, ORANGE, GREEN, DARK, RED, PURPLE

GRID = "#d5dde3"
VIRGULE = FuncFormatter(lambda v, _: f"{v:g}".replace(".", ","))
DE = np.ones(6) / 6


def style(ax):
    ax.grid(axis="y", color=GRID, lw=0.7, zorder=0)
    ax.yaxis.set_major_formatter(VIRGULE)
    ax.xaxis.set_major_formatter(VIRGULE)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)


def somme():
    fig, axs = plt.subplots(1, 2, figsize=(11.0, 3.9))
    fig.patch.set_facecolor("white")
    ax = axs[0]
    ax.bar(range(1, 7), DE, width=0.55, color=BLUE, zorder=3)
    ax.set_title("un dé : $X$ uniforme, $E(X) = 3{,}5$", fontsize=12.5, color=BLUE)
    ax.set_xticks(range(1, 7))
    ax.set_ylim(0, 0.2)
    style(ax)
    ax = axs[1]
    loi = np.convolve(DE, DE)
    ax.bar(range(2, 13), loi, width=0.55, color=ORANGE, zorder=3)
    ax.axvline(7, color=RED, lw=1.3, ls="--", zorder=4)
    ax.set_title("deux dés : $X + Y$, $E(X + Y) = 7$", fontsize=12.5, color=ORANGE)
    ax.set_xticks(range(2, 13))
    ax.set_ylim(0, 0.2)
    style(ax)
    fig.tight_layout()
    _save(fig, I("term_sva_somme.png"))


def moyenne():
    fig, ax = plt.subplots(figsize=(8.6, 4.4))
    fig.patch.set_facecolor("white")
    for n, col in ((1, BLUE), (4, ORANGE), (16, GREEN)):
        loi = DE.copy()
        for _ in range(n - 1):
            loi = np.convolve(loi, DE)
        sommes = np.arange(n, 6 * n + 1)
        x = sommes / n
        ax.plot(x, loi * n, color=col, lw=2.2, marker="o", ms=3.5, label=f"$n = {n}$")
    ax.axvline(3.5, color=RED, lw=1.3, ls="--")
    ax.legend(fontsize=12, frameon=False)
    ax.set_xlabel("valeur de la moyenne $M_n$ de $n$ dés", fontsize=12, color=DARK)
    ax.set_ylabel("densité (probabilité × $n$)", fontsize=11, color=DARK)
    ax.set_title("plus $n$ est grand, plus $M_n$ se concentre autour de $3{,}5$ : $\\sigma(M_n) = \\frac{\\sigma(X)}{\\sqrt{n}}$",
                 fontsize=12.5, color=DARK)
    style(ax)
    _save(fig, I("term_sva_moyenne.png"))


somme()
moyenne()
