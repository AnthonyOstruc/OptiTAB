# -*- coding: utf-8 -*-
"""Figures : Terminale — Logarithme népérien."""
import numpy as np
from matplotlib.ticker import FuncFormatter

from figlycee import new_fig, _save, setup_repere, txt, I, BLUE, ORANGE, GREEN, DARK, NEUTRAL, RED, PURPLE

BOITE = dict(fc="white", ec="none", pad=1.5)
GRID = "#d5dde3"
VIRGULE = FuncFormatter(lambda v, _: f"{v:g}".replace(".", ","))


def symetrie():
    fig, ax = new_fig(6.8, 6.8)
    setup_repere(ax, (-3.2, 5.2), (-3.2, 5.2))
    x = np.linspace(-3.0, 1.62, 300)
    ax.plot(x, np.exp(x), color=ORANGE, lw=2.6)
    x = np.linspace(0.045, 5.0, 300)
    ax.plot(x, np.log(x), color=BLUE, lw=2.6)
    t = np.array([-3, 5])
    ax.plot(t, t, color=NEUTRAL, lw=1.3, ls="--")
    for (a, b), (c, d) in (((0, 1), (1, 0)), ((1, np.e), (np.e, 1))):
        ax.plot([a, c], [b, d], color=GREEN, lw=1, ls=":")
        ax.scatter([a, c], [b, d], s=30, color=GREEN, zorder=6)
    txt(ax, 1.18, np.e - 0.05, "$(1\\,;e)$", GREEN, 12, va="center", bbox=BOITE)
    txt(ax, np.e + 0.1, 1.2, "$(e\\,;1)$", GREEN, 12, bbox=BOITE)
    txt(ax, 1.7, 4.8, "$y = e^x$", ORANGE, 14, fontweight="bold", bbox=BOITE)
    txt(ax, 4.9, 1.0, "$y = \\ln x$", BLUE, 14, ha="right", va="top", fontweight="bold", bbox=BOITE)
    txt(ax, 4.9, 4.4, "$y = x$", NEUTRAL, 12.5, ha="right", bbox=BOITE)
    txt(ax, 1.0, -3.6, "courbes symétriques par rapport à la droite $y = x$", DARK, 12.5, ha="center", va="top")
    ax.set_aspect("equal")
    ax.axis("off")
    _save(fig, I("term_ln_symetrie.png"))


def courbe():
    fig, ax = new_fig(7.6, 5.6)
    setup_repere(ax, (-0.8, 7.6), (-3.4, 3.2))
    x = np.linspace(0.035, 7.3, 400)
    ax.plot(x, np.log(x), color=BLUE, lw=2.8)
    t = np.array([-0.4, 4.2])
    ax.plot(t, t - 1, color=GREEN, lw=1.8)
    ax.scatter([1], [0], s=36, color=DARK, zorder=6)
    txt(ax, 4.25, 3.1, "tangente en $1$ : $y = x - 1$", GREEN, 12, va="center", bbox=BOITE)
    txt(ax, 7.3, 1.75, "$y = \\ln x$", BLUE, 14, ha="right", va="bottom", fontweight="bold", bbox=BOITE)
    txt(ax, 0.25, -2.9, "$\\ln x \\rightarrow -\\infty$ quand $x \\rightarrow 0^+$ :\nasymptote $x = 0$", RED, 12, va="center", bbox=BOITE)
    txt(ax, 3.4, -3.8, "$\\ln$ est concave : $\\ln x \\leq x - 1$ pour tout $x > 0$", DARK, 12.5, ha="center", va="top")
    ax.set_aspect("equal")
    ax.axis("off")
    _save(fig, I("term_ln_courbe.png"))


def croissances():
    fig, ax = new_fig(8.6, 4.4)
    x = np.linspace(0.01, 30, 500)
    ax.plot(x, x, color=ORANGE, lw=2)
    ax.plot(x, np.sqrt(x), color=GREEN, lw=2)
    ax.plot(x, np.log(x), color=BLUE, lw=2.6)
    ax.set_xlim(0, 33)
    ax.set_ylim(-1, 12)
    txt(ax, 12.3, 11.2, "$y = x$", ORANGE, 14, fontweight="bold")
    txt(ax, 30.3, np.sqrt(30), "$\\sqrt{x}$", GREEN, 14, va="center", fontweight="bold")
    txt(ax, 30.3, np.log(30), "$\\ln x$", BLUE, 14, va="center", fontweight="bold")
    txt(ax, 16, 8.4, "$\\ln x$ tend vers $+\\infty$, mais très lentement :\n$\\frac{\\ln x}{x} \\rightarrow 0$ quand $x \\rightarrow +\\infty$",
        DARK, 12.5, ha="left", va="center")
    ax.set_xlabel("$x$", fontsize=13, color=DARK)
    ax.grid(color=GRID, lw=0.6)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    _save(fig, I("term_ln_croissances.png"))


def demivie():
    fig, ax = new_fig(8.6, 4.4)
    T = 5730
    t = np.linspace(0, 20000, 400)
    ax.plot(t, 100 * 0.5 ** (t / T), color=BLUE, lw=2.6)
    for k, (v, lab) in enumerate(((50, "50 %"), (25, "25 %"))):
        x = (k + 1) * T
        ax.plot([0, x], [v, v], color=ORANGE, lw=1.2, ls="--")
        ax.plot([x, x], [0, v], color=ORANGE, lw=1.2, ls="--")
        ax.scatter([x], [v], s=34, color=ORANGE, zorder=6)
        txt(ax, x + 300, v + 2, f"{x:,} ans".replace(",", " "), ORANGE, 12, va="bottom")
    txt(ax, 10500, 82, "$N(t) = N_0\\,e^{-\\lambda t}$ avec $\\lambda = \\frac{\\ln 2}{5\\,730}$", BLUE, 13.5,
        fontweight="bold")
    ax.set_xlim(0, 20500)
    ax.set_ylim(0, 105)
    ax.xaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{int(v):,}".replace(",", " ")))
    ax.set_xlabel("temps (années)", fontsize=12, color=DARK)
    ax.set_ylabel("carbone 14 restant (%)", fontsize=12, color=DARK)
    ax.grid(color=GRID, lw=0.6)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    _save(fig, I("term_ln_demivie.png"))


symetrie()
courbe()
croissances()
demivie()
