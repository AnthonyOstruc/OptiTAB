# -*- coding: utf-8 -*-
"""Figures : Première — Fonction exponentielle."""
import numpy as np

from figlycee import new_fig, _save, setup_repere, txt, I, BLUE, ORANGE, GREEN, DARK, NEUTRAL, RED, PURPLE

BOITE = dict(fc="white", ec="none", pad=1.5)


def fin(ax):
    ax.set_aspect("equal")
    ax.axis("off")


def courbe():
    fig, ax = new_fig(6.8, 6.2)
    setup_repere(ax, (-4.4, 2.6), (-1.2, 6.4))
    x = np.linspace(-4.2, 1.82, 300)
    ax.plot(x, np.exp(x), color=BLUE, lw=2.8)
    xs = np.array([-2.2, 2.2])
    ax.plot(xs, xs + 1, color=GREEN, lw=1.8)
    ax.scatter([0, 1], [1, np.e], s=36, color=DARK, zorder=6)
    ax.plot([1, 1], [0, np.e], color=NEUTRAL, lw=1.1, ls=":")
    ax.plot([0, 1], [np.e, np.e], color=NEUTRAL, lw=1.1, ls=":")
    txt(ax, -0.15, np.e, "$e \\approx 2{,}718$", ORANGE, 12.5, ha="right", va="center", bbox=BOITE)
    txt(ax, -0.2, 1.45, "$(0\\,;1)$", DARK, 12, ha="right", va="bottom", bbox=BOITE)
    txt(ax, 1.9, 5.6, "$y = e^x$", BLUE, 14, fontweight="bold", bbox=BOITE)
    txt(ax, 2.3, 3.2, "tangente en $0$\n$y = x + 1$", GREEN, 12, ha="left", va="center")
    txt(ax, -4.2, 0.55, "$e^x$ se rapproche de $0$", BLUE, 11.5, va="center", bbox=BOITE)
    fin(ax)
    _save(fig, I("1er_exp_courbe.png"))


def ekx():
    fig, ax = new_fig(7.4, 5.4)
    setup_repere(ax, (-3.4, 3.4), (-0.6, 5.0))
    x = np.linspace(-3.2, 3.2, 300)
    for k, col, xl, yl, ha in ((1, BLUE, 1.25, 4.6, "left"), (0.5, GREEN, 2.45, 3.0, "left"),
                               (-0.5, ORANGE, -3.2, 3.0, "left"), (-1, RED, -1.25, 4.6, "right")):
        y = np.exp(k * x)
        ok = y <= 4.8
        ax.plot(x[ok], y[ok], color=col, lw=2.4)
        lab = {1: "$e^{x}$", 0.5: "$e^{0{,}5x}$", -0.5: "$e^{-0{,}5x}$", -1: "$e^{-x}$"}[k]
        txt(ax, xl, yl, lab, col, 14, ha=ha, va="center", fontweight="bold", bbox=BOITE)
    txt(ax, 0, -1.0, "$k > 0$ : croissante  ;  $k < 0$ : décroissante  ;  toutes passent par $(0\\,;1)$", DARK, 12.5,
        ha="center", va="top")
    fin(ax)
    _save(fig, I("1er_exp_ekx.png"))


def euler():
    fig, ax = new_fig(7.2, 5.4)
    setup_repere(ax, (-0.3, 2.3), (-0.3, 7.8), 0.5, 1)
    x = np.linspace(0, 2.05, 200)
    ax.plot(x, np.exp(x), color=BLUE, lw=2.8)
    for h, col in ((0.5, ORANGE), (0.25, GREEN)):
        xs = np.arange(0, 2 + 1e-9, h)
        ys = (1 + h) ** np.arange(len(xs))
        ax.plot(xs, ys, color=col, lw=1.8, marker="o", ms=5)
    txt(ax, 2.05, np.exp(2), "$e^x$", BLUE, 14, va="center", fontweight="bold")
    txt(ax, 2.05, 1.5 ** 4, "pas $h = 0{,}5$", ORANGE, 12.5, va="center")
    txt(ax, 2.05, 1.25 ** 8 - 0.2, "pas $h = 0{,}25$", GREEN, 12.5, va="center")
    txt(ax, 1.0, -0.9, "Euler : $f(x + h) \\approx f(x) + h f'(x) = (1 + h) f(x)$", DARK, 12.5, ha="center", va="top")
    ax.set_aspect(0.3)
    ax.axis("off")
    _save(fig, I("1er_exp_euler.png"))


courbe()
ekx()
euler()
