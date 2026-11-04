# -*- coding: utf-8 -*-
"""Figures : Terminale — Fonctions sinus et cosinus."""
import numpy as np

from figlycee import new_fig, _save, txt, I, tableau_variations, BLUE, ORANGE, GREEN, DARK, NEUTRAL, RED, PURPLE

PI = np.pi


def axes_pi(ax, a, b, ymin, ymax, pas=0.5):
    ax.axhline(0, color=NEUTRAL, lw=1.2)
    ax.axvline(0, color=NEUTRAL, lw=1.2)
    k0, k1 = int(np.ceil(a / (pas * PI))), int(np.floor(b / (pas * PI)))
    labs = {-2: "-\\pi", -1: "-\\frac{\\pi}{2}", 1: "\\frac{\\pi}{2}", 2: "\\pi", 3: "\\frac{3\\pi}{2}", 4: "2\\pi",
            -4: "-2\\pi", -3: "-\\frac{3\\pi}{2}"}
    for k in range(k0, k1 + 1):
        x = k * pas * PI
        ax.axvline(x, color="#e5e8eb", lw=0.8, zorder=0)
        if k:
            txt(ax, x, -0.1, f"${labs[k]}$", DARK, 12, ha="center", va="top")
    for y in (-1, 1):
        ax.axhline(y, color="#e5e8eb", lw=0.8, zorder=0)
        txt(ax, -0.08, y, f"${y}$", DARK, 11, ha="right", va="center")
    ax.set_xlim(a - 0.2, b + 0.2)
    ax.set_ylim(ymin, ymax)
    ax.axis("off")


def derivees():
    fig, ax = new_fig(9.8, 4.0)
    x = np.linspace(-PI, 2 * PI, 600)
    ax.plot(x, np.sin(x), color=BLUE, lw=2.6)
    ax.plot(x, np.cos(x), color=ORANGE, lw=2, ls="--")
    for x0 in (0, PI / 2, PI):
        t = np.array([x0 - 0.8, x0 + 0.8])
        ax.plot(t, np.sin(x0) + np.cos(x0) * (t - x0), color=GREEN, lw=1.8)
        ax.scatter([x0], [np.sin(x0)], s=30, color=GREEN, zorder=6)
    axes_pi(ax, -PI, 2 * PI, -1.6, 1.7)
    txt(ax, -3.0, 1.35, "$y = \\sin x$", BLUE, 13.5, fontweight="bold")
    txt(ax, 4.4, 1.35, "$y = \\cos x = (\\sin x)'$", ORANGE, 13.5, fontweight="bold")
    txt(ax, PI / 2, -1.55, "pente de la tangente à $\\sin$ en $x$ = valeur de $\\cos x$ (ici $1$, $0$, $-1$)", GREEN,
        12, ha="center", va="top")
    _save(fig, I("term_trig_derivees.png"))


def tableau():
    tableau_variations(I("term_trig_tableau.png"), ["$-\\pi$", "$0$", "$\\pi$"],
                       [("$-1$", "b"), ("$1$", "h"), ("$-1$", "b")], signe=["+", "0", "-"], col_w=1.9,
                       nom="f(x)", titre="$f(x) = \\cos x$ et $f'(x) = -\\sin x$ sur $[-\\pi\\,;\\pi]$")


def etude():
    fig, ax = new_fig(9.4, 4.0)
    x = np.linspace(-PI / 2, 2 * PI, 600)
    ax.plot(x, np.sin(2 * x), color=BLUE, lw=2.6)
    ax.axvspan(0, PI, color="#e8f4fd", zorder=0)
    axes_pi(ax, -PI / 2, 2 * PI, -1.6, 1.7)
    ax.annotate("", xy=(PI, 1.3), xytext=(0, 1.3), arrowprops=dict(arrowstyle="<->", color=GREEN, lw=1.5))
    txt(ax, PI / 2, 1.38, "une période : $\\pi$", GREEN, 12.5, ha="center", va="bottom", fontweight="bold")
    txt(ax, 5.4, -1.35, "$f(x) = \\sin(2x)$", BLUE, 13.5, ha="center", fontweight="bold")
    _save(fig, I("term_trig_etude.png"))


derivees()
tableau()
etude()
