# -*- coding: utf-8 -*-
"""Figures : Seconde — Fonctions de référence."""
import matplotlib.pyplot as plt
import numpy as np

from figlycee import new_fig, _save, setup_repere, txt, I, BLUE, ORANGE, GREEN, DARK, NEUTRAL, RED, PURPLE

BOITE = dict(fc="white", ec="none", pad=1.5)


def points(ax, pts, col=DARK, fs=11, dx=0.15, dy=0.0, ha="left"):
    for x, y, lab in pts:
        ax.scatter([x], [y], s=26, color=col, zorder=6)
        if lab:
            txt(ax, x + dx, y + dy, lab, col, fs, ha=ha, va="center", bbox=BOITE)


def fin(ax, equal=True):
    if equal:
        ax.set_aspect("equal")
    ax.axis("off")


def carre():
    fig, ax = new_fig(6.4, 5.6)
    setup_repere(ax, (-3.2, 3.2), (-0.9, 5.4))
    x = np.linspace(-2.25, 2.25, 200)
    ax.plot(x, x ** 2, color=BLUE, lw=2.6)
    for a in (1, 2):
        ax.plot([-a, a], [a * a, a * a], color=ORANGE, lw=1.2, ls="--")
    points(ax, [(-2, 4, "$(-2\\,;4)$"), (-1, 1, "$(-1\\,;1)$")], dx=-0.15, ha="right")
    points(ax, [(2, 4, "$(2\\,;4)$"), (1, 1, "$(1\\,;1)$")])
    points(ax, [(0, 0, None)], col=RED)
    txt(ax, 0.35, 2.8, "$y = x^2$", BLUE, 14, fontweight="bold", bbox=BOITE)
    txt(ax, 0, -0.75, "fonction paire : courbe symétrique par rapport à l’axe des ordonnées", GREEN, 11.5,
        ha="center", va="top")
    fin(ax)
    _save(fig, I("2nd_fonref_carre.png"))


def inverse():
    fig, ax = new_fig(6.4, 6.0)
    setup_repere(ax, (-4.4, 4.4), (-4.4, 4.4))
    for s in (1, -1):
        x = np.linspace(0.26, 4.2, 200) * s
        ax.plot(x, 1 / x, color=BLUE, lw=2.6)
    points(ax, [(1, 1, "$(1\\,;1)$"), (2, 0.5, "$(2\\,;0{,}5)$"), (0.5, 2, "$(0{,}5\\,;2)$")], dx=0.2, dy=0.25)
    points(ax, [(-1, -1, "$(-1\\,;-1)$"), (-2, -0.5, "$(-2\\,;-0{,}5)$")], dx=-0.2, dy=-0.3, ha="right")
    ax.plot([-1, 1], [-1, 1], color=ORANGE, lw=1.2, ls="--")
    txt(ax, 1.6, 3.6, "$y = \\frac{1}{x}$", BLUE, 15, fontweight="bold", bbox=BOITE)
    txt(ax, 0, -4.7, "fonction impaire : courbe symétrique par rapport à l’origine $O$", GREEN, 11.5,
        ha="center", va="top")
    fin(ax)
    _save(fig, I("2nd_fonref_inverse.png"))


def racine_cube():
    fig, axs = plt.subplots(1, 2, figsize=(11.0, 5.0), gridspec_kw=dict(width_ratios=[1.35, 1], wspace=0.12))
    fig.patch.set_facecolor("white")
    ax = axs[0]
    setup_repere(ax, (-0.8, 9.8), (-0.9, 4.0))
    x = np.linspace(0, 9.4, 300)
    ax.plot(x, np.sqrt(x), color=GREEN, lw=2.6)
    points(ax, [(1, 1, "$(1\\,;1)$"), (4, 2, "$(4\\,;2)$")], dx=0.25, dy=-0.35)
    points(ax, [(9, 3, "$(9\\,;3)$")], dx=-0.25, dy=-0.35, ha="right")
    points(ax, [(0, 0, None)], col=RED)
    txt(ax, 4.6, 3.55, "$y = \\sqrt{x}$ sur $[0\\,;+\\infty[$", GREEN, 13.5, ha="center", fontweight="bold",
        bbox=BOITE)
    txt(ax, 4.6, -1.2, "croissante sur $[0\\,;+\\infty[$", GREEN, 12, ha="center", va="top")
    fin(ax, equal=False)
    ax = axs[1]
    setup_repere(ax, (-2.4, 2.4), (-4.6, 4.6))
    x = np.linspace(-1.62, 1.62, 200)
    ax.plot(x, x ** 3, color=PURPLE, lw=2.6)
    points(ax, [(1, 1, "$(1\\,;1)$")], dx=0.2)
    points(ax, [(-1, -1, "$(-1\\,;-1)$")], dx=-0.2, ha="right")
    txt(ax, 0.5, 4.0, "$y = x^3$", PURPLE, 14, fontweight="bold", bbox=BOITE)
    txt(ax, 0, -5.0, "impaire, croissante sur $\\mathbb{R}$", PURPLE, 12, ha="center", va="top")
    fin(ax, equal=False)
    _save(fig, I("2nd_fonref_racine_cube.png"))


def positions():
    fig, ax = new_fig(6.6, 6.0)
    setup_repere(ax, (-0.3, 2.0), (-0.3, 2.6), xt=0.5, yt=0.5)
    x = np.linspace(0, 1.75, 200)
    ax.plot(x, x, color=BLUE, lw=2.4)
    x2 = np.linspace(0, 1.6, 200)
    ax.plot(x2, x2 ** 2, color=ORANGE, lw=2.4)
    x3 = np.linspace(0, 1.37, 200)
    ax.plot(x3, x3 ** 3, color=PURPLE, lw=2.4)
    ax.axvline(1, color=NEUTRAL, lw=1, ls=":")
    points(ax, [(1, 1, None)], col=RED)
    txt(ax, 1.78, 1.72, "$y = x$", BLUE, 13, va="center", bbox=BOITE)
    txt(ax, 1.62, 2.45, "$y = x^2$", ORANGE, 13, va="center", bbox=BOITE)
    txt(ax, 1.05, 2.45, "$y = x^3$", PURPLE, 13, ha="right", va="center", bbox=BOITE)
    txt(ax, 0.5, -0.42, "sur $[0\\,;1]$ :\n$x^3 \\leq x^2 \\leq x$", DARK, 12.5, ha="center", va="top")
    txt(ax, 1.5, -0.42, "sur $[1\\,;+\\infty[$ :\n$x \\leq x^2 \\leq x^3$", DARK, 12.5, ha="center", va="top")
    fin(ax)
    _save(fig, I("2nd_fonref_positions.png"))


def equation():
    fig, ax = new_fig(6.6, 5.4)
    setup_repere(ax, (-3.4, 3.4), (-1.0, 6.0))
    x = np.linspace(-2.45, 2.45, 200)
    ax.plot(x, x ** 2, color=BLUE, lw=2.6)
    ax.plot([-3.2, 3.2], [4, 4], color=ORANGE, lw=2)
    ax.plot([-2, -2], [0, 4], color=NEUTRAL, lw=1.2, ls=":")
    ax.plot([2, 2], [0, 4], color=NEUTRAL, lw=1.2, ls=":")
    ax.plot([-2, 2], [0, 0], color=GREEN, lw=6, solid_capstyle="butt", alpha=0.8)
    points(ax, [(-2, 4, None), (2, 4, None)], col=RED)
    txt(ax, 3.2, 4.3, "$y = 4$", ORANGE, 13, ha="right", bbox=BOITE)
    txt(ax, -0.3, 5.5, "$y = x^2$", BLUE, 13, ha="right", bbox=BOITE)
    txt(ax, 0, -1.3, "$x^2 = 4 \\Leftrightarrow x = -2$ ou $x = 2$  ;  $x^2 \\leq 4 \\Leftrightarrow x \\in [-2\\,;2]$",
        DARK, 12.5, ha="center", va="top")
    fin(ax)
    _save(fig, I("2nd_fonref_equation.png"))


def quatre():
    fig, axs = plt.subplots(1, 4, figsize=(12.4, 3.9))
    fig.patch.set_facecolor("white")
    cas = [
        ("$x \\mapsto x^2$", BLUE, "$\\mathbb{R}$, paire", [(np.linspace(-1.75, 1.75, 100), lambda x: x ** 2)]),
        ("$x \\mapsto \\frac{1}{x}$", ORANGE, "$\\mathbb{R}^{*}$, impaire",
         [(np.linspace(0.33, 2.3, 100), lambda x: 1 / x), (np.linspace(-2.3, -0.33, 100), lambda x: 1 / x)]),
        ("$x \\mapsto \\sqrt{x}$", GREEN, "$[0\\,;+\\infty[$", [(np.linspace(0, 2.3, 100), np.sqrt)]),
        ("$x \\mapsto x^3$", PURPLE, "$\\mathbb{R}$, impaire", [(np.linspace(-1.45, 1.45, 100), lambda x: x ** 3)]),
    ]
    for ax, (nom, col, dom, morceaux) in zip(axs, cas):
        ax.set_facecolor("white")
        ax.annotate("", xy=(2.5, 0), xytext=(-2.5, 0), arrowprops=dict(arrowstyle="->", lw=1.2, color=NEUTRAL))
        ax.annotate("", xy=(0, 3.2), xytext=(0, -3.2), arrowprops=dict(arrowstyle="->", lw=1.2, color=NEUTRAL))
        for x, f in morceaux:
            ax.plot(x, f(x), color=col, lw=2.6)
        ax.scatter([1], [1], s=22, color=DARK, zorder=6)
        ax.text(0, 3.6, nom, ha="center", fontsize=15, color=col, fontweight="bold")
        ax.text(0, -3.7, dom, ha="center", va="top", fontsize=12.5, color=DARK)
        ax.set_xlim(-2.6, 2.6)
        ax.set_ylim(-4.6, 4.3)
        ax.set_aspect("equal")
        ax.axis("off")
    _save(fig, I("2nd_fonref_quatre.png"))


carre()
inverse()
racine_cube()
positions()
equation()
quatre()
