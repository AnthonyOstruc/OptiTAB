# -*- coding: utf-8 -*-
"""Figures : Terminale — Continuité, TVI, dichotomie."""
import matplotlib.pyplot as plt
import numpy as np

from figlycee import new_fig, _save, setup_repere, txt, I, BLUE, ORANGE, GREEN, DARK, NEUTRAL, RED, PURPLE

BOITE = dict(fc="white", ec="none", pad=1.5)
f3 = lambda x: x ** 3 + x - 1  # noqa: E731


def saut():
    fig, axs = plt.subplots(1, 2, figsize=(10.6, 4.4))
    fig.patch.set_facecolor("white")
    ax = axs[0]
    setup_repere(ax, (-0.6, 4.4), (-0.6, 3.6), unit_labels=False)
    x = np.linspace(0, 4, 200)
    ax.plot(x, 1 + 0.8 * np.sin(1.3 * x) + 0.3 * x, color=BLUE, lw=2.6)
    txt(ax, 2.0, -0.95, "continue : tracé sans lever le crayon", GREEN, 12.5, ha="center", va="top")
    ax.set_aspect("equal")
    ax.axis("off")
    ax = axs[1]
    setup_repere(ax, (-0.6, 4.4), (-0.6, 3.6))
    for k in range(4):
        ax.plot([k, k + 1], [k, k], color=ORANGE, lw=2.6)
        ax.scatter([k], [k], s=34, color=ORANGE, zorder=6)
        ax.scatter([k + 1], [k], s=34, facecolor="white", edgecolor=ORANGE, lw=1.6, zorder=6)
    txt(ax, 2.0, -0.95, "partie entière : discontinue en chaque entier", RED, 12.5, ha="center", va="top")
    ax.set_aspect("equal")
    ax.axis("off")
    _save(fig, I("term_cont_saut.png"))


def tvi():
    fig, ax = new_fig(7.4, 5.4)
    setup_repere(ax, (-0.4, 6.6), (-0.6, 5.2), unit_labels=False)
    g = lambda x: 1 + 1.6 * np.sin(1.2 * x - 0.5) + 0.45 * x  # noqa: E731
    a, b = 0.5, 6.0
    x = np.linspace(a, b, 400)
    ax.plot(x, g(x), color=BLUE, lw=2.6)
    k = 2.3
    ax.axhline(k, color=ORANGE, lw=1.6, ls="--", xmin=0.03)
    xs = x[np.where(np.diff(np.sign(g(x) - k)))[0]]
    for c in xs:
        ax.plot([c, c], [0, k], color=GREEN, lw=1.2, ls=":")
        ax.scatter([c], [k], s=36, color=GREEN, zorder=6)
    for v, lab in ((a, "$a$"), (b, "$b$")):
        ax.plot([v, v], [0, g(v)], color=NEUTRAL, lw=1, ls=":")
        txt(ax, v, -0.15, lab, DARK, 14, ha="center", va="top")
    txt(ax, -0.1, g(a), "$f(a)$", DARK, 13, ha="right", va="center")
    txt(ax, -0.1, g(b), "$f(b)$", DARK, 13, ha="right", va="center")
    ax.plot([0, a], [g(a), g(a)], color=NEUTRAL, lw=1, ls=":")
    ax.plot([0, b], [g(b), g(b)], color=NEUTRAL, lw=1, ls=":")
    txt(ax, -0.1, k, "$k$", ORANGE, 14, ha="right", va="center", fontweight="bold")
    txt(ax, 3.3, -0.8, "ici, l’équation $f(x) = k$ a trois solutions dans $[a\\,;b]$", GREEN, 12.5, ha="center",
        va="top")
    ax.set_aspect("equal")
    ax.axis("off")
    _save(fig, I("term_cont_tvi.png"))


def unique():
    fig, ax = new_fig(6.6, 5.6)
    setup_repere(ax, (-0.5, 1.5), (-1.4, 1.5), 0.5, 0.5)
    x = np.linspace(0, 1.2, 300)
    ax.plot(x, f3(x), color=BLUE, lw=2.6)
    al = 0.6823278
    ax.scatter([al], [0], s=44, color=RED, zorder=6)
    txt(ax, al - 0.03, 0.12, "$\\alpha \\approx 0{,}682$", RED, 13, ha="right", fontweight="bold")
    for v in (0, 1):
        ax.scatter([v], [f3(v)], s=30, color=DARK, zorder=6)
    txt(ax, 0.05, -1.0, "$f(0) = -1 < 0$", DARK, 12, va="center")
    txt(ax, 1.05, 1.0, "$f(1) = 1 > 0$", DARK, 12, va="center")
    txt(ax, 0.5, -1.65, "$f(x) = x^3 + x - 1$ continue et strictement croissante :\nune seule solution de $f(x) = 0$",
        DARK, 12, ha="center", va="top")
    ax.set_aspect(0.55)
    ax.axis("off")
    _save(fig, I("term_cont_unique.png"))


def dichotomie():
    fig, ax = new_fig(8.6, 4.0)
    a, b = 0.0, 1.0
    for k in range(6):
        y = -k * 0.55
        ax.plot([0, 1], [y, y], color="#d5dde3", lw=1)
        ax.plot([a, b], [y, y], color=BLUE if k < 5 else GREEN, lw=6, solid_capstyle="butt")
        txt(ax, a - 0.02, y, f"{a:g}".replace(".", ","), DARK, 10.5, ha="right", va="center")
        txt(ax, b + 0.02, y, f"{b:g}".replace(".", ","), DARK, 10.5, ha="left", va="center")
        txt(ax, -0.22, y, f"étape {k}", NEUTRAL, 11, ha="right", va="center")
        m = (a + b) / 2
        if k < 5:
            ax.plot([m, m], [y - 0.12, y + 0.12], color=RED, lw=1.6)
            if f3(a) * f3(m) <= 0:
                b = m
            else:
                a = m
    ax.axvline(0.6823278, color=RED, lw=1, ls=":")
    txt(ax, 0.6823278, 0.35, "$\\alpha$", RED, 14, ha="center")
    txt(ax, 0.5, -3.35, "à chaque étape, on garde la moitié où $f$ change de signe : la longueur est divisée par 2",
        DARK, 12, ha="center", va="top")
    ax.set_xlim(-0.55, 1.2)
    ax.set_ylim(-3.7, 0.6)
    ax.axis("off")
    _save(fig, I("term_cont_dichotomie.png"))


saut()
tvi()
unique()
dichotomie()
