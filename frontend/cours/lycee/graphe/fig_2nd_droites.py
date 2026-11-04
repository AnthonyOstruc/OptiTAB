# -*- coding: utf-8 -*-
"""Figures : Seconde — Droites du plan et systèmes."""
import matplotlib.pyplot as plt
import numpy as np

from figlycee import new_fig, _save, setup_repere, txt, I, BLUE, ORANGE, GREEN, DARK, NEUTRAL, RED, PURPLE

P = lambda x, y: np.array([x, y], float)  # noqa: E731
BOITE = dict(fc="white", ec="none", pad=1.5)


def fleche(ax, A, B, col=BLUE, lw=2.6, ms=18, ls="-"):
    ax.annotate("", xy=B, xytext=A, arrowprops=dict(arrowstyle="-|>", color=col, lw=lw, mutation_scale=ms,
                                                    shrinkA=0, shrinkB=0, linestyle=ls))


def point(ax, Q, nom, d=(0, 1), col=DARK, fs=13):
    ax.scatter([Q[0]], [Q[1]], s=28, color=col, zorder=6)
    ax.annotate(f"${nom}$", Q, textcoords="offset points", xytext=(16 * d[0], 14 * d[1]), ha="center",
                va="center", fontsize=fs, color=col, fontweight="bold", bbox=BOITE)


def trace(ax, f, x0, x1, col, lw=2.4, **kw):
    x = np.linspace(x0, x1, 50)
    ax.plot(x, f(x), color=col, lw=lw, **kw)


def fin(ax):
    ax.set_aspect("equal")
    ax.axis("off")


def directeur():
    fig, ax = new_fig(7.6, 5.2)
    setup_repere(ax, (-1.5, 9.5), (-2, 6.5))
    trace(ax, lambda x: (2 * x - 1) / 3, -1.2, 9.2, BLUE)
    A, M = P(2, 1), P(8, 5)
    fleche(ax, A, M, ORANGE, lw=2.2)
    fleche(ax, P(5, 0), P(8, 2), GREEN, lw=2.8)
    txt(ax, 6.9, 0.6, "$\\vec{u}\\,(3\\,;2)$", GREEN, 14, ha="left", bbox=BOITE)
    point(ax, A, "A(2\\,;1)", (0.9, -1.2))
    point(ax, M, "M(x\\,;y)", (-1.6, 0.8))
    txt(ax, 5.2, 3.65, "$\\overrightarrow{AM}$", ORANGE, 14, ha="right", bbox=BOITE)
    txt(ax, 9.0, 6.0, "$d$", BLUE, 15, ha="center", fontweight="bold")
    txt(ax, 4.0, -2.6, r"$M \in d \Leftrightarrow \det(\overrightarrow{AM}, \vec{u}) = 0 \Leftrightarrow 2x - 3y - 1 = 0$",
        DARK, 13.5, ha="center", va="top")
    fin(ax)
    _save(fig, I("2nd_droites_directeur.png"))


def pente():
    fig, ax = new_fig(6.6, 6.0)
    setup_repere(ax, (-1.5, 7.5), (-2.4, 6.6))
    trace(ax, lambda x: 4 * x / 3 - 5 / 3, -0.4, 6.2, BLUE)
    A, B = P(2, 1), P(5, 5)
    ax.plot([2, 5], [1, 1], color=ORANGE, lw=2.2, ls="--")
    ax.plot([5, 5], [1, 5], color=ORANGE, lw=2.2, ls="--")
    txt(ax, 3.5, 0.78, r"$\Delta x = 3$", ORANGE, 13, ha="center", va="top", bbox=BOITE)
    txt(ax, 5.2, 3.0, r"$\Delta y = 4$", ORANGE, 13, va="center", bbox=BOITE)
    point(ax, A, r"A(2\,;1)", (-1.7, 1.1))
    point(ax, B, r"B(5\,;5)", (-1.7, 0.6))
    txt(ax, 6.5, 4.6, r"$y = \frac{4}{3}x - \frac{5}{3}$", BLUE, 13, ha="center", bbox=BOITE)
    txt(ax, 3.0, -2.9, r"$m = \frac{\Delta y}{\Delta x} = \frac{y_B - y_A}{x_B - x_A} = \frac{4}{3}$", GREEN, 15,
        ha="center", va="top", fontweight="bold")
    fin(ax)
    _save(fig, I("2nd_droites_pente.png"))


def panorama():
    fig, ax = new_fig(7.2, 6.4)
    setup_repere(ax, (-4.5, 6.5), (-4.5, 6.5))
    trace(ax, lambda x: 2 * x + 1, -2.6, 2.6, BLUE)
    trace(ax, lambda x: 3 - x, -1.4, 6.2, ORANGE)
    trace(ax, lambda x: -2 + 0 * x, -4.3, 6.2, GREEN)
    ax.plot([-3, -3], [-4.3, 6.2], color=PURPLE, lw=2.4)
    txt(ax, 2.8, 5.8, "$y = 2x + 1$\n$m = 2 > 0$", BLUE, 12.5, ha="left", va="center", bbox=BOITE)
    txt(ax, 4.2, 0.6, "$y = -x + 3$\n$m = -1 < 0$", ORANGE, 12.5, ha="left", va="center", bbox=BOITE)
    txt(ax, 0.3, -3.55, "$y = -2$ : $m = 0$ (horizontale)", GREEN, 12.5, ha="left", va="center", bbox=BOITE)
    txt(ax, -2.75, 4.6, "$x = -3$\npas de pente\n(verticale)", PURPLE, 12, ha="left", va="center", bbox=BOITE)
    fin(ax)
    _save(fig, I("2nd_droites_panorama.png"))


def systemes():
    fig, axs = plt.subplots(1, 3, figsize=(11.4, 4.2))
    fig.patch.set_facecolor("white")
    cas = [
        ("sécantes", "une seule solution", "$ab' - a'b \\neq 0$",
         [(lambda x: 0.8 * x + 0.4, BLUE, "-"), (lambda x: -1.1 * x + 3.2, ORANGE, "-")], P(1.47, 1.58)),
        ("parallèles", "aucune solution", "$ab' - a'b = 0$",
         [(lambda x: 0.7 * x + 1.6, BLUE, "-"), (lambda x: 0.7 * x - 0.6, ORANGE, "-")], None),
        ("confondues", "une infinité de solutions", "$ab' - a'b = 0$",
         [(lambda x: 0.7 * x + 0.5, BLUE, "-"), (lambda x: 0.7 * x + 0.5, ORANGE, "--")], None),
    ]
    for ax, (nom, sol, crit, droites, inter) in zip(axs, cas):
        ax.set_facecolor("white")
        ax.annotate("", xy=(3.8, 0), xytext=(-0.6, 0), arrowprops=dict(arrowstyle="->", lw=1.3, color=NEUTRAL))
        ax.annotate("", xy=(0, 3.8), xytext=(0, -1.2), arrowprops=dict(arrowstyle="->", lw=1.3, color=NEUTRAL))
        for f, col, ls in droites:
            x = np.linspace(-0.5, 3.6, 40)
            y = f(x)
            ok = (y > -1.2) & (y < 3.7)
            ax.plot(x[ok], y[ok], color=col, lw=3.2 if ls == "-" else 2.4, ls=ls)
        if inter is not None:
            ax.scatter([inter[0]], [inter[1]], s=70, color=RED, zorder=6)
        ax.text(1.6, 4.35, f"droites {nom}", ha="center", fontsize=14, color=DARK, fontweight="bold")
        ax.text(1.6, -1.75, sol, ha="center", fontsize=13, color=GREEN, fontweight="bold")
        ax.text(1.6, -2.45, crit, ha="center", fontsize=13, color=DARK)
        ax.set_xlim(-0.8, 4.0)
        ax.set_ylim(-2.8, 4.8)
        ax.set_aspect("equal")
        ax.axis("off")
    _save(fig, I("2nd_droites_systemes.png"))


def intersection():
    fig, ax = new_fig(6.6, 6.0)
    setup_repere(ax, (-1.5, 6.5), (-2.2, 6.5))
    trace(ax, lambda x: 2 * x - 1, -0.55, 3.6, BLUE)
    trace(ax, lambda x: 5 - x, -1.2, 6.2, ORANGE)
    ax.plot([2, 2], [0, 3], color=NEUTRAL, lw=1.2, ls=":")
    ax.plot([0, 2], [3, 3], color=NEUTRAL, lw=1.2, ls=":")
    point(ax, P(2, 3), "I(2\\,;3)", (1.7, 0.4), col=RED)
    txt(ax, 3.7, 5.6, "$y = 2x - 1$", BLUE, 13, ha="center", bbox=BOITE)
    txt(ax, 5.0, 1.0, "$x + y = 5$", ORANGE, 13, ha="center", bbox=BOITE)
    fin(ax)
    _save(fig, I("2nd_droites_intersection.png"))


directeur()
pente()
panorama()
systemes()
intersection()
