# -*- coding: utf-8 -*-
"""Figures : Première — Suites numériques."""
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle

from figlycee import new_fig, _save, setup_repere, txt, I, BLUE, ORANGE, GREEN, DARK, NEUTRAL, RED, LBLUE, LORANGE

BOITE = dict(fc="white", ec="none", pad=1.5)


def nuages():
    fig, axs = plt.subplots(1, 2, figsize=(11.0, 4.6))
    fig.patch.set_facecolor("white")
    ax = axs[0]
    setup_repere(ax, (-0.8, 8.6), (-0.8, 13.5), 1, 2, xlabel="$n$", ylabel="$u_n$")
    n = np.arange(0, 8)
    ax.scatter(n, 1 + 1.5 * n, s=40, color=BLUE, zorder=5)
    ax.plot([0, 7.6], [1, 1 + 1.5 * 7.6], color=BLUE, lw=1, ls=":")
    for k in (2, 3):
        ax.plot([k, k + 1], [1 + 1.5 * k, 1 + 1.5 * k], color=ORANGE, lw=1.6)
        ax.plot([k + 1, k + 1], [1 + 1.5 * k, 1 + 1.5 * (k + 1)], color=ORANGE, lw=1.6)
    txt(ax, 4.15, 5.6, "$+r$", ORANGE, 13, va="center")
    txt(ax, 4.0, -2.0, "arithmétique $u_n = 1 + 1{,}5n$ :\npoints alignés", BLUE, 12.5, ha="center", va="top")
    ax.axis("off")
    ax = axs[1]
    setup_repere(ax, (-0.8, 8.6), (-0.8, 13.5), 1, 2, xlabel="$n$", ylabel="")
    v = 0.5 * 1.5 ** n
    w = 8 * 0.6 ** n
    ax.scatter(n, v, s=40, color=GREEN, zorder=5)
    ax.scatter(n, w, s=40, color=RED, zorder=5, marker="s")
    txt(ax, 7.2, 9.4, "$v_n = 0{,}5 \\times 1{,}5^n$\n$q > 1$ : croissante", GREEN, 12, ha="right", va="center",
        bbox=BOITE)
    txt(ax, 1.6, 6.6, "$w_n = 8 \\times 0{,}6^n$\n$0 < q < 1$ : décroissante", RED, 12, va="center", bbox=BOITE)
    txt(ax, 4.0, -2.0, "géométriques : croissance\nou décroissance « exponentielle »", DARK, 12.5, ha="center",
        va="top")
    ax.axis("off")
    _save(fig, I("1er_suites_nuages.png"))


def somme():
    fig, ax = new_fig(8.0, 4.4)
    n = 6
    for k in range(1, n + 1):
        for j in range(k):
            ax.add_patch(Rectangle((k - 1, j), 1, 1, fc=LBLUE, ec=BLUE, lw=1.2))
        for j in range(k, n + 1):
            ax.add_patch(Rectangle((k - 1, j), 1, 1, fc=LORANGE, ec=ORANGE, lw=1.2))
    for k in range(1, n + 1):
        txt(ax, k - 0.5, -0.35, f"${k}$", BLUE, 12, ha="center", va="top")
    ax.annotate("", xy=(n + 0.4, n + 1), xytext=(n + 0.4, 0), arrowprops=dict(arrowstyle="<->", color=DARK, lw=1.3))
    txt(ax, n + 0.6, (n + 1) / 2, "$n + 1$", DARK, 13, va="center")
    ax.annotate("", xy=(n, -1.0), xytext=(0, -1.0), arrowprops=dict(arrowstyle="<->", color=DARK, lw=1.3))
    txt(ax, n / 2, -1.15, "$n$", DARK, 13, ha="center", va="top")
    txt(ax, 8.0, 5.2, "bleu : $1 + 2 + \\cdots + n$", BLUE, 13, va="center")
    txt(ax, 8.0, 4.2, "orange : la même somme,\nretournée", ORANGE, 13, va="center")
    txt(ax, 8.0, 2.4, "$2S = n(n + 1)$", DARK, 14, va="center", fontweight="bold")
    txt(ax, 8.0, 1.3, "$S = \\frac{n(n + 1)}{2}$", GREEN, 16, va="center", fontweight="bold")
    ax.set_xlim(-0.4, 12.6)
    ax.set_ylim(-1.9, n + 1.4)
    ax.set_aspect("equal")
    ax.axis("off")
    _save(fig, I("1er_suites_somme.png"))


def escalier():
    fig, ax = new_fig(6.8, 6.0)
    setup_repere(ax, (-0.6, 6.4), (-0.6, 6.0), xlabel="$x$", ylabel="$y$", unit_labels=False)
    x = np.linspace(-0.3, 6.2, 10)
    ax.plot(x, 0.5 * x + 2, color=BLUE, lw=2.4)
    ax.plot(x, x, color=NEUTRAL, lw=1.4)
    u = 0.0
    pts = [u]
    for _ in range(5):
        v = 0.5 * u + 2
        ax.plot([u, u], [u if _ else 0, v], color=ORANGE, lw=1.6)
        ax.plot([u, v], [v, v], color=ORANGE, lw=1.6)
        u = v
        pts.append(u)
    for k, p in enumerate(pts[:4]):
        txt(ax, p, -0.25, f"$u_{k}$", ORANGE, 12.5, ha="center", va="top")
    ax.axvline(4, color=GREEN, lw=1, ls="--", ymax=0.7)
    txt(ax, 4.15, 0.35, "$4$", GREEN, 13, fontweight="bold")
    txt(ax, 6.0, 5.25, "$y = 0{,}5x + 2$", BLUE, 12.5, ha="right", bbox=BOITE)
    txt(ax, 6.0, 6.0, "$y = x$", NEUTRAL, 12.5, ha="right", va="center", bbox=BOITE)
    txt(ax, 3.0, -1.0, "$u_0 = 0$ et $u_{n+1} = 0{,}5u_n + 2$ : les termes se rapprochent de $4$", DARK, 12.5,
        ha="center", va="top")
    ax.set_aspect("equal")
    ax.axis("off")
    _save(fig, I("1er_suites_escalier.png"))


nuages()
somme()
escalier()
