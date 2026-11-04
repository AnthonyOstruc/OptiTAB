# -*- coding: utf-8 -*-
"""Figures : Terminale — Concentration et loi des grands nombres."""
import numpy as np
from matplotlib.ticker import FuncFormatter
from scipy.stats import binom

from figlycee import new_fig, _save, txt, I, BLUE, ORANGE, GREEN, DARK, NEUTRAL, RED

GRID = "#d5dde3"
VIRGULE = FuncFormatter(lambda v, _: f"{v:g}".replace(".", ","))


def style(ax):
    ax.yaxis.set_major_formatter(VIRGULE)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)


def bienayme():
    fig, ax = new_fig(8.8, 4.4)
    k = np.arange(0, 21)
    p = binom.pmf(k, 20, 0.5)
    cols = [ORANGE if abs(v - 10) >= 4 else BLUE for v in k]
    ax.bar(k, p, width=0.6, color=cols, zorder=3)
    ax.axvspan(6.5, 13.5, color="#e8f5e9", zorder=0)
    ax.axvline(10, color=RED, lw=1.4, ls="--", zorder=4)
    txt(ax, 10.3, 0.19, "$E(X) = 10$", RED, 12.5, ha="left", va="bottom")
    txt(ax, 3.2, 0.12, "en orange :\n$|X - 10| \\geq 4$", ORANGE, 12.5, ha="center")
    txt(ax, 17.0, 0.12, "probabilité réelle $\\approx 0{,}115$\nmajorant $\\frac{V(X)}{\\delta^2} = \\frac{5}{16} \\approx 0{,}31$",
        DARK, 12, ha="center")
    ax.set_xticks(range(0, 21, 2))
    ax.set_ylim(0, 0.215)
    ax.set_xlabel("$k$", fontsize=13, color=DARK)
    ax.set_title("$X \\sim \\mathcal{B}(20\\,;0{,}5)$, $V(X) = 5$, $\\delta = 4$ : Bienaymé-Tchebychev", fontsize=12.5,
                 color=DARK)
    ax.grid(axis="y", color=GRID, lw=0.7, zorder=0)
    style(ax)
    _save(fig, I("term_lgn_bt.png"))


def convergence():
    rng = np.random.default_rng(3)
    fig, ax = new_fig(8.8, 4.6)
    N = 2000
    n = np.arange(1, N + 1)
    for _ in range(25):
        f = np.cumsum(rng.random(N) < 0.5) / n
        ax.plot(n, f, color=BLUE, lw=0.8, alpha=0.45)
    d = 0.05
    ax.axhspan(0.5 - d, 0.5 + d, color="#e8f5e9", zorder=0)
    ax.axhline(0.5, color=RED, lw=1.4, ls="--")
    ax.set_xscale("log")
    ax.set_xlim(1, N)
    ax.xaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{v:g}".replace("1000", "1 000")))
    ax.set_ylim(0, 1)
    ax.set_xlabel("nombre de lancers $n$ (échelle logarithmique)", fontsize=12, color=DARK)
    ax.set_ylabel("fréquence de « pile » $M_n$", fontsize=12, color=DARK)
    txt(ax, 1.3, 0.9, "25 simulations : peu à peu, toutes entrent dans la bande $[0{,}45\\,;0{,}55]$", DARK, 12)
    ax.grid(color=GRID, lw=0.6)
    style(ax)
    _save(fig, I("term_lgn_convergence.png"))


bienayme()
convergence()
