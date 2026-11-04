# -*- coding: utf-8 -*-
"""Figures : Terminale — Représentations paramétriques et équations cartésiennes."""
import numpy as np
from matplotlib.patches import Polygon

from figlycee import new_fig, _save, txt, I, BLUE, ORANGE, GREEN, DARK, NEUTRAL, RED, PURPLE

K, ANG = 0.5, np.radians(30)


def pr(p):
    x, y, z = p
    return np.array([x + K * y * np.cos(ANG), z + K * y * np.sin(ANG)])


def droite():
    fig, ax = new_fig(8.0, 4.4)
    A = np.array([1.0, 0.5, 0.6])
    u = np.array([1.6, 0.8, 0.7])
    pts = [pr(A + t * u) for t in (-1.3, 3.0)]
    ax.plot([pts[0][0], pts[1][0]], [pts[0][1], pts[1][1]], color=BLUE, lw=2.4)
    a, b = pr(A), pr(A + u)
    ax.annotate("", xy=b, xytext=a, arrowprops=dict(arrowstyle="-|>", color=ORANGE, lw=2.8, mutation_scale=18,
                                                    shrinkA=0, shrinkB=0))
    for t in (-1, 0, 1, 2):
        p = pr(A + t * u)
        ax.scatter([p[0]], [p[1]], s=34, color=DARK if t else RED, zorder=6)
        txt(ax, p[0] + 0.05, p[1] - 0.35, f"$t = {t}$", DARK if t else RED, 12, ha="center", va="top")
    txt(ax, a[0] - 0.15, a[1] + 0.25, "$A$", RED, 15, ha="right", fontweight="bold")
    txt(ax, (a[0] + b[0]) / 2 - 0.1, (a[1] + b[1]) / 2 + 0.25, "$\\vec{u}$", ORANGE, 15, ha="right",
        fontweight="bold")
    txt(ax, 3.8, -1.9, "$M(t)$ : $\\overrightarrow{AM} = t\\,\\vec{u}$, soit $x = x_A + ta$, $y = y_A + tb$, $z = z_A + tc$",
        DARK, 12.5, ha="center", va="top")
    ax.set_xlim(-1.6, 8.6)
    ax.set_ylim(-2.5, 3.8)
    ax.set_aspect("equal")
    ax.axis("off")
    _save(fig, I("term_param_droite.png"))


def intersection():
    fig, ax = new_fig(7.4, 5.4)
    P = [(0, 0, 0), (6, 0, 0), (6, 5, 0), (0, 5, 0)]
    ax.add_patch(Polygon([pr(p) for p in P], closed=True, fc="#e8f4fd", ec=BLUE, lw=1.5))
    I0 = np.array([3.0, 2.5, 0.0])
    u = np.array([0.6, 0.3, 1.0])
    haut, bas = pr(I0 + 2.6 * u), pr(I0)
    sous = pr(I0 - 1.3 * u)
    ax.plot([bas[0], haut[0]], [bas[1], haut[1]], color=ORANGE, lw=2.4)
    ax.plot([sous[0], bas[0]], [sous[1], bas[1]], color=ORANGE, lw=2.0, ls="--")
    ax.scatter([bas[0]], [bas[1]], s=44, color=RED, zorder=6)
    txt(ax, bas[0] + 0.25, bas[1] - 0.05, "$I$", RED, 15, va="top", fontweight="bold")
    txt(ax, haut[0] + 0.1, haut[1], "$d$", ORANGE, 15, va="center", fontweight="bold")
    txt(ax, 7.6, 0.6, "plan $\\mathcal{P}$", BLUE, 13)
    txt(ax, 3.8, -1.5, "on remplace $x$, $y$, $z$ de $d$ dans l’équation de $\\mathcal{P}$ : on trouve $t$, puis $I$",
        DARK, 12.5, ha="center", va="top")
    ax.set_xlim(-0.5, 8.8)
    ax.set_ylim(-2.0, 4.6)
    ax.set_aspect("equal")
    ax.axis("off")
    _save(fig, I("term_param_intersection.png"))


def plans():
    fig, ax = new_fig(7.4, 5.4)
    P1 = [(0, 0, 0), (6, 0, 0), (6, 5, 0), (0, 5, 0)]
    ax.add_patch(Polygon([pr(p) for p in P1], closed=True, fc="#e8f4fd", ec=BLUE, lw=1.5, alpha=0.95))
    P2 = [(3, -0.6, -1.6), (3, 5.6, -1.6), (3, 5.6, 2.6), (3, -0.6, 2.6)]
    poly = [pr(p) for p in P2]
    ax.add_patch(Polygon(poly, closed=True, fc="#fdebd0", ec=ORANGE, lw=1.5, alpha=0.75))
    a, b = pr((3, 0, 0)), pr((3, 5, 0))
    ax.plot([a[0], b[0]], [a[1], b[1]], color=RED, lw=3)
    txt(ax, b[0] + 0.2, b[1] + 0.1, "$\\Delta = \\mathcal{P}_1 \\cap \\mathcal{P}_2$", RED, 13, fontweight="bold")
    txt(ax, 0.2, 0.25, "$\\mathcal{P}_1$", BLUE, 14, fontweight="bold")
    txt(ax, poly[2][0] + 0.1, poly[2][1] - 0.2, "$\\mathcal{P}_2$", ORANGE, 14, va="top", fontweight="bold")
    txt(ax, 3.8, -2.0, "deux plans sécants se coupent selon une droite :\non résout le système de leurs deux équations",
        DARK, 12.5, ha="center", va="top")
    ax.set_xlim(-0.5, 8.6)
    ax.set_ylim(-3.0, 4.6)
    ax.set_aspect("equal")
    ax.axis("off")
    _save(fig, I("term_param_plans.png"))


droite()
intersection()
plans()
