# -*- coding: utf-8 -*-
"""Figures : Seconde — Échantillonnage (simulations à graine fixe)."""
import numpy as np

from figlycee import new_fig, _save, txt, I, BLUE, ORANGE, GREEN, DARK, NEUTRAL, RED, PURPLE

GRID = "#d5dde3"


def stabilisation():
    rng = np.random.default_rng(7)
    fig, ax = new_fig(8.4, 4.6)
    n = np.arange(1, 2001)
    for col in (BLUE, ORANGE, PURPLE):
        lancers = rng.random(2000) < 0.5
        ax.plot(n, np.cumsum(lancers) / n, color=col, lw=1.6)
    ax.axhline(0.5, color=RED, lw=1.6, ls="--")
    ax.set_xlim(0, 2000)
    ax.set_ylim(0, 1)
    ax.set_xlabel("nombre de lancers $n$", fontsize=12, color=DARK)
    ax.set_ylabel("fréquence de « pile »", fontsize=12, color=DARK)
    ax.set_yticks([0, 0.25, 0.5, 0.75, 1])
    ax.set_yticklabels(["0", "0,25", "0,5", "0,75", "1"])
    ax.grid(color=GRID, lw=0.7)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    txt(ax, 1950, 0.46, "$p = 0{,}5$", RED, 13, ha="right", va="top", fontweight="bold")
    txt(ax, 1000, 0.9, "3 simulations : les fréquences se stabilisent autour de $p$", DARK, 12.5, ha="center")
    _save(fig, I("2nd_echant_stabilisation.png"))


def fluctuation():
    rng = np.random.default_rng(2024)
    N, n, p = 100, 100, 0.5
    f = rng.binomial(n, p, N) / n
    dans = np.abs(f - p) <= 1 / np.sqrt(n) + 1e-12
    fig, ax = new_fig(8.4, 4.6)
    ax.axhspan(p - 0.1, p + 0.1, color="#e8f5e9", zorder=0)
    ax.axhline(p, color=RED, lw=1.4, ls="--")
    for b in (p - 0.1, p + 0.1):
        ax.axhline(b, color=GREEN, lw=1.4)
    k = np.arange(1, N + 1)
    ax.scatter(k[dans], f[dans], s=22, color=BLUE, zorder=5)
    ax.scatter(k[~dans], f[~dans], s=40, color=ORANGE, marker="D", zorder=6)
    ax.set_xlim(0, N + 1)
    ax.set_ylim(0.25, 0.75)
    ax.set_xlabel("numéro de l’échantillon (taille $n = 100$)", fontsize=12, color=DARK)
    ax.set_ylabel("fréquence observée $f$", fontsize=12, color=DARK)
    ax.set_yticks([0.3, 0.4, 0.5, 0.6, 0.7])
    ax.set_yticklabels(["0,3", "0,4", "0,5", "0,6", "0,7"])
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    txt(ax, 99, 0.615, "$p + \\frac{1}{\\sqrt{n}} = 0{,}6$", GREEN, 12.5, ha="right", va="bottom")
    txt(ax, 99, 0.385, "$p - \\frac{1}{\\sqrt{n}} = 0{,}4$", GREEN, 12.5, ha="right", va="top")
    txt(ax, 50, 0.71, f"{int(dans.sum())} échantillons sur {N} ont une fréquence dans la bande verte", DARK, 12.5,
        ha="center")
    _save(fig, I("2nd_echant_fluctuation.png"))
    return int(dans.sum())


stabilisation()
print("dans la bande :", fluctuation())
