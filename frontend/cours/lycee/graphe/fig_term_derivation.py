# -*- coding: utf-8 -*-
"""Figures : Terminale — Dérivation (composée, dérivée seconde, convexité, inflexion)."""
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyBboxPatch

from figlycee import new_fig, _save, setup_repere, txt, I, BLUE, ORANGE, GREEN, DARK, NEUTRAL, RED


def tangente():
    fig, ax = new_fig(7.2, 5.2)
    setup_repere(ax, (-1.6, 3.4), (-0.6, 5.2), 1, 1)
    f = lambda x: x ** 2 / 2 + 1  # noqa: E731
    x = np.linspace(-1.5, 3.0, 200)
    ax.plot(x, f(x), color=BLUE, lw=2.6)
    a = 1
    xt = np.linspace(-0.6, 3.3, 50)
    ax.plot(xt, a * (xt - a) + f(a), color=ORANGE, lw=2)
    ax.scatter([a], [f(a)], s=60, color=DARK, zorder=6)
    txt(ax, a - 0.15, f(a) + 0.25, "$A(a\\,;f(a))$", DARK, 12.5, ha="right")
    ax.plot([a, a + 1], [f(a), f(a)], color=GREEN, lw=1.8, ls="--")
    ax.plot([a + 1, a + 1], [f(a), f(a) + 1], color=GREEN, lw=1.8, ls="--")
    txt(ax, a + 0.5, f(a) - 0.35, "$1$", GREEN, 12, ha="center")
    txt(ax, a + 1.08, f(a) + 0.45, "$f'(a)$", GREEN, 12.5)
    txt(ax, 2.75, 3.4, "$\\mathcal{C}_f$", BLUE, 15)
    txt(ax, -1.45, 4.6, "tangente $T$ : $y=f'(a)(x-a)+f(a)$", ORANGE, 12.5)
    ax.axis("off")
    _save(fig, I("term_derivation_tangente.png"))


def composee():
    fig, ax = new_fig(9.2, 3.4)
    boites = [(0.0, "$x$", "#f8f9fa", NEUTRAL), (3.2, "$u(x)$", "#e8f4fd", BLUE), (6.6, "$v(u(x))$", "#fdebd0", ORANGE)]
    for x0, s, fc, ec in boites:
        ax.add_patch(FancyBboxPatch((x0, 0.6), 2.0, 1.0, boxstyle="round,pad=0.05,rounding_size=0.2", facecolor=fc,
                                    edgecolor=ec, lw=2))
        txt(ax, x0 + 1.0, 1.1, s, DARK, 16, ha="center", va="center")
    for x1, x2, nom, col in [(2.05, 3.15, "$u$", BLUE), (5.25, 6.55, "$v$", ORANGE)]:
        ax.annotate("", xy=(x2, 1.1), xytext=(x1, 1.1), arrowprops=dict(arrowstyle="-|>", color=col, lw=2,
                                                                         mutation_scale=18))
        txt(ax, (x1 + x2) / 2, 1.3, nom, col, 15, ha="center", va="bottom")
    txt(ax, 4.3, 2.35, "fonction intérieure $u$, puis fonction extérieure $v$", NEUTRAL, 11.5, ha="center")
    txt(ax, 4.3, 0.05, "$(v\\circ u)'(x)=v'(u(x))\\times u'(x)$", GREEN, 16, ha="center", va="top",
        fontweight="bold")
    txt(ax, 4.3, -0.75, "exemple : $x\\mapsto x^2+1\\mapsto e^{x^2+1}$ donc $f'(x)=e^{x^2+1}\\times 2x$", DARK, 12.5,
        ha="center", va="top")
    ax.set_xlim(-0.3, 8.9)
    ax.set_ylim(-1.4, 2.7)
    ax.set_aspect("equal")
    ax.axis("off")
    _save(fig, I("term_derivation_composee.png"))


def convexite():
    fig, axs = plt.subplots(1, 2, figsize=(10.4, 4.6))
    cas = [(np.exp, np.exp, np.linspace(-2.2, 1.6, 200), [-1.5, 0, 1], BLUE, "convexe : $f''\\geq 0$",
            "courbe au-dessus de ses tangentes", (-2.3, 1.8), (-1.2, 5.2), "$y=e^x$"),
           (np.log, lambda x: 1 / x, np.linspace(0.08, 5.2, 200), [0.5, 1.5, 3.5], ORANGE, "concave : $f''\\leq 0$",
            "courbe en dessous de ses tangentes", (-0.3, 5.4), (-3.2, 2.6), "$y=\\ln x$")]
    for ax, (f, df, x, pts, col, titre, sous, xl, yl, nom) in zip(axs, cas):
        ax.axhline(0, color=NEUTRAL, lw=1)
        ax.axvline(0, color=NEUTRAL, lw=1)
        ax.plot(x, f(x), color=col, lw=2.8)
        for a in pts:
            xt = np.linspace(xl[0], xl[1], 50)
            ax.plot(xt, df(a) * (xt - a) + f(a), color=GREEN, lw=1.2, ls="--")
            ax.scatter([a], [f(a)], s=30, color=GREEN, zorder=5)
        ax.set_xlim(*xl)
        ax.set_ylim(*yl)
        ax.set_title(titre, fontsize=13.5, color=col, fontweight="bold")
        ax.text(0.5, -0.08, sous, transform=ax.transAxes, ha="center", va="top", fontsize=11.5, color=DARK)
        ax.text(0.04, 0.92, nom, transform=ax.transAxes, fontsize=13, color=col)
        ax.set_xticks([])
        ax.set_yticks([])
        for s in ax.spines.values():
            s.set_color("#d5d8dc")
    _save(fig, I("term_derivation_convexite.png"))


def inflexion():
    fig, ax = new_fig(7.4, 5.4)
    setup_repere(ax, (-2.6, 2.6), (-4.2, 4.2), 1, 1)
    x = np.linspace(-2.25, 2.25, 300)
    y = x ** 3 - 3 * x
    ax.axvspan(-2.6, 0, color="#fdebd0", alpha=0.45, zorder=0)
    ax.axvspan(0, 2.6, color="#d6eafc", alpha=0.45, zorder=0)
    ax.plot(x, y, color=DARK, lw=2.6)
    xt = np.linspace(-1.35, 1.35, 20)
    ax.plot(xt, -3 * xt, color=GREEN, lw=2, ls="--")
    ax.scatter([0], [0], s=70, color=RED, zorder=6)
    txt(ax, 0.15, 0.25, "$I(0\\,;0)$", RED, 13, fontweight="bold")
    txt(ax, -2.45, 3.6, "concave\n$f''(x)<0$", ORANGE, 12.5, fontweight="bold")
    txt(ax, 1.35, 3.6, "convexe\n$f''(x)>0$", BLUE, 12.5, fontweight="bold")
    txt(ax, 1.25, -2.9, "tangente en $I$ :\n$y=-3x$", GREEN, 12)
    txt(ax, -1.0, -3.9, "$f(x)=x^3-3x$", DARK, 13, ha="center")
    ax.axis("off")
    _save(fig, I("term_derivation_inflexion.png"))


def exemple():
    fig, ax = new_fig(7.6, 5.4)
    setup_repere(ax, (-2.9, 2.9), (-6.5, 6.0), 1, 1)
    f = lambda x: x ** 4 - 6 * x ** 2 + 4  # noqa: E731
    x = np.linspace(-2.75, 2.75, 400)
    for a, b, c in [(-2.9, -1, "#d6eafc"), (-1, 1, "#fdebd0"), (1, 2.9, "#d6eafc")]:
        ax.axvspan(a, b, color=c, alpha=0.45, zorder=0)
    ax.plot(x, f(x), color=DARK, lw=2.6)
    for xi in (-1, 1):
        ax.scatter([xi], [f(xi)], s=70, color=RED, zorder=6)
    for xi, xs, nom in [(-1, -1.75, "$I_1(-1\\,;-1)$"), (1, 1.75, "$I_2(1\\,;-1)$")]:
        ax.annotate(nom, xy=(xi, -1), xytext=(xs, -5.9), fontsize=12.5, color=RED, ha="center", va="center",
                    fontweight="bold", arrowprops=dict(arrowstyle="->", color=RED, lw=1.2))
    txt(ax, -2.8, 5.5, "convexe", BLUE, 12, fontweight="bold")
    txt(ax, 0.55, 5.5, "concave", ORANGE, 12, fontweight="bold", ha="center")
    txt(ax, 2.0, 5.5, "convexe", BLUE, 12, fontweight="bold")
    txt(ax, 0, -4.6, "$f''(x)=12(x-1)(x+1)$", DARK, 12, ha="center")
    ax.axis("off")
    _save(fig, I("term_derivation_exemple.png"))


def lorenz():
    fig, ax = new_fig(5.8, 5.6)
    setup_repere(ax, (-8, 108), (-8, 108), 20, 20, xlabel="% population", ylabel="% richesses")
    x = np.linspace(0, 100, 200)
    L = x ** 2 / 100
    ax.fill_between(x, L, x, color="#fdebd0", alpha=0.8)
    ax.plot(x, x, color=GREEN, lw=2, ls="--")
    ax.plot(x, L, color=BLUE, lw=2.6)
    txt(ax, 38, 55, "égalité parfaite $y=x$", GREEN, 11.5, rotation=45, ha="center")
    txt(ax, 80, 28, "courbe de Lorenz\n(convexe)", BLUE, 11.5, ha="center")
    txt(ax, 64, 47, "inégalités", ORANGE, 11, ha="center", fontweight="bold")
    ax.axis("off")
    _save(fig, I("term_derivation_lorenz.png"))


tangente()
composee()
convexite()
inflexion()
exemple()
lorenz()
