# -*- coding: utf-8 -*-
"""Figures : Seconde — Manipuler les nombres réels."""
from math import sqrt, pi

from figlycee import (new_fig, _save, cadre, droite, intervalle, txt, I, BLUE, ORANGE, GREEN, DARK, NEUTRAL, LBLUE,
                      RED, PURPLE, FancyBboxPatch)


def ensembles():
    fig, ax = new_fig(8.6, 5.6)
    couches = [("$\\mathbb{R}$", 0.0, "#eaf2f8", BLUE, ["$\\sqrt{2}$", "$\\pi$", "$-\\sqrt{5}$"]),
               ("$\\mathbb{Q}$", 0.9, "#f4ecf7", PURPLE, ["$\\frac{1}{3}$", "$-\\frac{5}{7}$"]),
               ("$\\mathbb{D}$", 1.8, "#e8f8f5", GREEN, ["$0{,}25$", "$-3{,}4$"]),
               ("$\\mathbb{Z}$", 2.7, "#fef5e7", ORANGE, ["$-5$", "$-1$"]),
               ("$\\mathbb{N}$", 3.6, "#fdedec", RED, ["$0$", "$3$", "$17$"])]
    W, gx, gy, hin = 16.0, 1.0, 1.25, 1.6
    H = 2 * 4 * gy + hin
    for k, (nom, _, fc, ec, ex) in enumerate(couches):
        dx, dy = k * gx, k * gy
        ax.add_patch(FancyBboxPatch((dx, dy), W - 2 * dx, H - 2 * dy,
                                    boxstyle="round,pad=0,rounding_size=0.5", facecolor=fc, edgecolor=ec, lw=2.2))
        yb = H - dy - gy / 2
        txt(ax, dx + 0.3, yb, nom, ec, 18, va="center", fontweight="bold")
        for j, e in enumerate(ex):
            txt(ax, dx + 2.1 + 2.0 * j, yb, e, ec, 15, ha="center", va="center")
    txt(ax, W / 2, -0.4, "$\\mathbb{N}\\subset\\mathbb{Z}\\subset\\mathbb{D}\\subset\\mathbb{Q}\\subset\\mathbb{R}$",
        DARK, 17, ha="center", va="top")
    cadre(ax, (-0.3, W + 0.3), (-1.4, H + 0.3))
    _save(fig, I("2nd_reels_ensembles.png"))


def droite_reels():
    fig, ax = new_fig(9.0, 2.6)
    droite(ax, 0, -3.4, 4.4, range(-3, 5))
    pts = [(-2, "$-2$", ORANGE), (1 / 3, "$\\frac{1}{3}$", PURPLE), (sqrt(2), "$\\sqrt{2}$", BLUE),
           (pi, "$\\pi$", BLUE), (-0.75, "$-0{,}75$", GREEN)]
    for x, s, c in pts:
        ax.scatter([x], [0], s=55, color=c, zorder=5)
        ax.annotate(s, (x, 0), textcoords="offset points", xytext=(0, 16), ha="center", fontsize=14, color=c)
    txt(ax, 0.5, -0.95, "à chaque point de la droite correspond un unique réel, et réciproquement", NEUTRAL, 11,
        ha="center")
    txt(ax, 0.5, -1.35, "(mêmes couleurs que les ensembles : $\\mathbb{Z}$ orange, $\\mathbb{D}$ vert, "
        "$\\mathbb{Q}$ violet, $\\mathbb{R}$ bleu)", NEUTRAL, 9.5, ha="center")
    cadre(ax, (-3.6, 4.6), (-1.6, 1.0))
    _save(fig, I("2nd_reels_droite.png"))


def intervalles():
    fig, ax = new_fig(8.6, 5.4)
    lignes = [("$[2\\,;5]$", "$2\\leq x\\leq 5$", 2, 5, True, True),
              ("$]2\\,;5[$", "$2< x< 5$", 2, 5, False, False),
              ("$[2\\,;+\\infty[$", "$x\\geq 2$", 2, None, True, False),
              ("$]-\\infty\\,;1]$", "$x\\leq 1$", None, 1, False, True)]
    for k, (nom, ineg, a, b, fa, fb) in enumerate(lignes):
        y = -1.25 * k
        droite(ax, y, -1.5, 7.2, range(-1, 8), fs=9.5)
        intervalle(ax, y, a, b, fa, fb, BLUE if k % 2 == 0 else ORANGE, lo=-1.5, hi=7.0)
        txt(ax, -2.0, y, nom, DARK, 14, ha="right", va="center")
        txt(ax, 7.6, y, ineg, NEUTRAL, 13, ha="left", va="center")
    txt(ax, 2.8, 0.75, "crochet tourné vers l'intérieur : borne incluse ; vers l'extérieur : borne exclue", NEUTRAL,
        10.5, ha="center")
    cadre(ax, (-4.4, 9.6), (-4.4, 1.1))
    _save(fig, I("2nd_reels_intervalles.png"))


def distance():
    fig, ax = new_fig(8.6, 2.9)
    droite(ax, 0, -4.5, 6.6, range(-4, 7))
    for x, c in [(-3, ORANGE), (0, DARK), (5, BLUE)]:
        ax.scatter([x], [0], s=55, color=c, zorder=5)
    ax.annotate("", xy=(0, 0.55), xytext=(-3, 0.55), arrowprops=dict(arrowstyle="<->", color=ORANGE, lw=1.8))
    txt(ax, -1.5, 0.7, "$|-3| = 3$", ORANGE, 13, ha="center", va="bottom")
    ax.annotate("", xy=(5, 1.45), xytext=(-3, 1.45), arrowprops=dict(arrowstyle="<->", color=GREEN, lw=1.8))
    txt(ax, 1, 1.6, "$d(-3\\,;5) = |5-(-3)| = 8$", GREEN, 13, ha="center", va="bottom", fontweight="bold")
    for x in (-3, 5):
        ax.plot([x, x], [0, 1.45], color=GREEN, lw=0.9, ls=":")
    cadre(ax, (-4.8, 6.9), (-0.7, 2.2))
    _save(fig, I("2nd_reels_distance.png"))


def centre():
    fig, ax = new_fig(8.0, 2.9)
    droite(ax, 0, -0.6, 6.8, range(0, 7))
    intervalle(ax, 0, 1, 5, True, True, BLUE)
    ax.scatter([3], [0], s=70, color=ORANGE, zorder=6)
    txt(ax, 3, 0.35, "centre $a=3$", ORANGE, 12, ha="center", va="bottom", fontweight="bold")
    for x1, x2 in [(1, 3), (3, 5)]:
        ax.annotate("", xy=(x2, -0.75), xytext=(x1, -0.75), arrowprops=dict(arrowstyle="<->", color=GREEN, lw=1.6))
        txt(ax, (x1 + x2) / 2, -0.9, "$r=2$", GREEN, 12, ha="center", va="top")
    txt(ax, 3, 1.05, "$x\\in[1\\,;5] \\Leftrightarrow |x-3|\\leq 2$", DARK, 14, ha="center", va="bottom")
    cadre(ax, (-0.8, 7.0), (-1.5, 1.7))
    _save(fig, I("2nd_reels_centre.png"))


def encadrement():
    fig, ax = new_fig(8.6, 4.4)
    niveaux = [(1, 2, 0.1, 1, "amplitude $1$"), (1.4, 1.5, 0.01, 2, "amplitude $10^{-1}$"),
               (1.41, 1.42, 0.001, 3, "amplitude $10^{-2}$")]
    r2 = sqrt(2)
    X0, X1 = 0.0, 10.0
    for k, (a, b, pas, dec, nom) in enumerate(niveaux):
        y = -1.55 * k
        ax.plot([X0, X1], [y, y], color=NEUTRAL, lw=1.6)
        n = round((b - a) / pas)
        for j in range(n + 1):
            x = X0 + (X1 - X0) * j / n
            hgt = 0.14 if j in (0, n) else 0.07
            ax.plot([x, x], [y - hgt, y + hgt], color=NEUTRAL, lw=1.2)
        for v, x in [(a, X0), (b, X1)]:
            txt(ax, x, y - 0.22, f"{v:.{dec - 1 if dec > 1 else 0}f}".replace(".", ","), DARK, 11.5, ha="center",
                va="top")
        xr = X0 + (X1 - X0) * (r2 - a) / (b - a)
        ax.scatter([xr], [y], s=55, color=BLUE, zorder=5)
        txt(ax, xr, y + 0.18, "$\\sqrt{2}$", BLUE, 13, ha="center", va="bottom")
        txt(ax, X1 + 0.4, y, nom, NEUTRAL, 11, va="center")
        if k < 2:
            na, nb, *_ = niveaux[k + 1]
            xa = X0 + (X1 - X0) * (na - a) / (b - a)
            xb = X0 + (X1 - X0) * (nb - a) / (b - a)
            ax.plot([xa, X0], [y - 0.05, y - 1.55 + 0.25], color=ORANGE, lw=0.9, ls="--")
            ax.plot([xb, X1], [y - 0.05, y - 1.55 + 0.25], color=ORANGE, lw=0.9, ls="--")
            ax.plot([xa, xb], [y, y], color=ORANGE, lw=4, alpha=0.6)
    txt(ax, 5, -4.25, "$1{,}41 \\leq \\sqrt{2} \\leq 1{,}42$ : encadrement à $10^{-2}$ près", GREEN, 13, ha="center",
        fontweight="bold")
    cadre(ax, (-0.5, 12.8), (-4.6, 0.7))
    _save(fig, I("2nd_reels_encadrement.png"))


ensembles()
droite_reels()
intervalles()
distance()
centre()
encadrement()
