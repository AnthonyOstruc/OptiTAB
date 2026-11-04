# -*- coding: utf-8 -*-
"""Figures : Première — Dérivation."""
import numpy as np

from figlycee import (new_fig, _save, setup_repere, txt, I, tableau_variations, BLUE, ORANGE, GREEN, DARK, NEUTRAL,
                      RED, PURPLE)

BOITE = dict(fc="white", ec="none", pad=1.5)


def fin(ax):
    ax.set_aspect("equal")
    ax.axis("off")


def secantes():
    fig, ax = new_fig(7.0, 6.0)
    setup_repere(ax, (-0.8, 4.4), (-1.6, 5.2), unit_labels=False)
    f = lambda x: x ** 2 / 2  # noqa: E731
    x = np.linspace(-0.6, 3.1, 200)
    ax.plot(x, f(x), color=BLUE, lw=2.6)
    a = 1.0
    for h, col in ((2.0, "#f5b041"), (1.2, ORANGE), (0.5, "#d35400")):
        m = (f(a + h) - f(a)) / h
        xs = np.array([-0.5, 3.6])
        ax.plot(xs, f(a) + m * (xs - a), color=col, lw=1.4)
        ax.scatter([a + h], [f(a + h)], s=26, color=col, zorder=6)
    xs = np.array([-0.5, 3.8])
    ax.plot(xs, f(a) + 1.0 * (xs - a), color=GREEN, lw=2.6)
    ax.scatter([a], [f(a)], s=40, color=DARK, zorder=7)
    txt(ax, a - 0.1, f(a) + 0.25, "$A$", DARK, 14, ha="right", fontweight="bold")
    txt(ax, 3.0, 4.95, "$M$ se rapproche de $A$", ORANGE, 12.5, ha="center", bbox=BOITE)
    txt(ax, 3.95, 2.35, "tangente\npente $f'(a)$", GREEN, 12.5, va="center", fontweight="bold")
    txt(ax, 1.8, -2.0, "pente des sécantes $\\frac{f(a + h) - f(a)}{h} \\rightarrow f'(a)$ quand $h \\rightarrow 0$",
        DARK, 12.5, ha="center", va="top")
    fin(ax)
    _save(fig, I("1er_deriv_secantes.png"))


def tangente():
    fig, ax = new_fig(6.6, 6.0)
    setup_repere(ax, (-2.4, 3.4), (-1.6, 5.4))
    x = np.linspace(-2.2, 2.3, 200)
    ax.plot(x, x ** 2, color=BLUE, lw=2.6)
    xs = np.array([-0.3, 3.0])
    ax.plot(xs, 2 * xs - 1, color=GREEN, lw=2.4)
    ax.plot([1, 2], [1, 1], color=ORANGE, lw=1.8, ls="--")
    ax.plot([2, 2], [1, 3], color=ORANGE, lw=1.8, ls="--")
    txt(ax, 1.5, 0.75, "$1$", ORANGE, 13, ha="center", va="top")
    txt(ax, 2.1, 2.0, "$f'(1) = 2$", ORANGE, 13, va="center", bbox=BOITE)
    ax.scatter([1], [1], s=40, color=DARK, zorder=7)
    txt(ax, 0.88, 1.2, "$A$", DARK, 14, ha="right", fontweight="bold")
    txt(ax, -2.0, 4.4, "$y = x^2$", BLUE, 13.5, bbox=BOITE)
    txt(ax, 3.3, -1.0, "$T : y = 2x - 1$", GREEN, 13.5, ha="right", va="center", fontweight="bold")
    fin(ax)
    _save(fig, I("1er_deriv_tangente.png"))


def courbe():
    fig, ax = new_fig(6.6, 5.8)
    setup_repere(ax, (-2.6, 2.8), (-3.2, 3.4))
    x = np.linspace(-2.15, 2.15, 300)
    ax.plot(x, x ** 3 - 3 * x, color=BLUE, lw=2.6)
    for a, b, col in ((-1, 2, GREEN), (1, -2, RED)):
        ax.plot([a - 0.7, a + 0.7], [b, b], color=col, lw=2)
        ax.scatter([a], [b], s=40, color=col, zorder=7)
    txt(ax, -1, 2.3, "maximum local $2$", GREEN, 12, ha="center", va="bottom", bbox=BOITE)
    txt(ax, 1, -2.3, "minimum local $-2$", RED, 12, ha="center", va="top", bbox=BOITE)
    txt(ax, 2.5, 2.2, "$f(x) = x^3 - 3x$", BLUE, 13, ha="right", bbox=BOITE)
    txt(ax, 0.1, -3.7, "tangentes horizontales là où $f'(x) = 0$", DARK, 12.5, ha="center", va="top")
    fin(ax)
    _save(fig, I("1er_deriv_courbe.png"))


def tableau():
    tableau_variations(I("1er_deriv_tableau.png"), ["$-\\infty$", "$-1$", "$1$", "$+\\infty$"],
                       [("", "b"), ("$2$", "h"), ("$-2$", "b"), ("", "h")],
                       signe=["+", "0", "-", "0", "+"], col_w=1.6,
                       titre="$f'(x) = 3x^2 - 3 = 3(x - 1)(x + 1)$")


secantes()
tangente()
courbe()
tableau()
