# -*- coding: utf-8 -*-
"""Figures : Seconde — Vecteurs du plan."""
import numpy as np
from matplotlib.patches import Polygon

from figlycee import new_fig, _save, setup_repere, txt, cadre, I, BLUE, ORANGE, GREEN, DARK, NEUTRAL, RED

P = lambda x, y: np.array([x, y], float)  # noqa: E731


def fleche(ax, A, B, col=BLUE, lw=2.4, ms=18, ls="-"):
    ax.annotate("", xy=B, xytext=A, arrowprops=dict(arrowstyle="-|>", color=col, lw=lw, mutation_scale=ms,
                                                    shrinkA=0, shrinkB=0, linestyle=ls))


def point(ax, Q, nom, d=(0, 1), col=DARK):
    ax.scatter([Q[0]], [Q[1]], s=26, color=col, zorder=6)
    ax.annotate(f"${nom}$", Q, textcoords="offset points", xytext=(14 * d[0], 14 * d[1]), ha="center",
                va="center", fontsize=14, color=col, fontweight="bold")


def parallelogramme():
    fig, ax = new_fig(7.0, 4.4)
    A, B, C = P(0, 0), P(4, 1), P(1, 2.6)
    D = C + (B - A)
    ax.add_patch(Polygon([A, B, D, C], closed=True, facecolor="#e8f5e9", edgecolor="none"))
    ax.plot([A[0], C[0]], [A[1], C[1]], color=NEUTRAL, lw=1.2, ls="--")
    ax.plot([B[0], D[0]], [B[1], D[1]], color=NEUTRAL, lw=1.2, ls="--")
    fleche(ax, A, B)
    fleche(ax, C, D)
    for Q, n, d in [(A, "A", (-1, -0.5)), (B, "B", (1, -0.5)), (C, "C", (-1, 0.5)), (D, "D", (1, 0.5))]:
        point(ax, Q, n, d)
    txt(ax, 2.0, 0.15, "$\\vec{u}$", BLUE, 16)
    txt(ax, 3.0, 3.75, "$\\vec{u}$", BLUE, 16)
    txt(ax, 2.5, -1.0, "$\\overrightarrow{AB} = \\overrightarrow{CD} \\Leftrightarrow ABDC$ parallélogramme", GREEN, 13,
        ha="center")
    cadre(ax, (-0.9, 5.9), (-1.4, 4.2))
    _save(fig, I("2nd_vecteurs_parallelogramme.png"))


def chasles():
    fig, ax = new_fig(9.6, 4.2)
    A, B, C = P(0, 0), P(3, 2.2), P(5.2, 0.4)
    fleche(ax, A, B)
    fleche(ax, B, C, ORANGE)
    fleche(ax, A, C, GREEN, lw=2.8)
    for Q, n, d in [(A, "A", (-1, -0.5)), (B, "B", (0, 1)), (C, "C", (1, -0.5))]:
        point(ax, Q, n, d)
    txt(ax, 2.6, -1.0, "$\\overrightarrow{AB} + \\overrightarrow{BC} = \\overrightarrow{AC}$", GREEN, 14,
        ha="center")
    O = P(8.0, 0)
    u, v = P(2.6, 0.6), P(0.8, 2.2)
    ax.add_patch(Polygon([O, O + u, O + u + v, O + v], closed=True, facecolor="#f4f6f7", edgecolor="none"))
    fleche(ax, O, O + u)
    fleche(ax, O, O + v, ORANGE)
    fleche(ax, O + u, O + u + v, ORANGE, lw=1.4, ls="--")
    fleche(ax, O + v, O + u + v, BLUE, lw=1.4, ls="--")
    fleche(ax, O, O + u + v, GREEN, lw=2.8)
    txt(ax, O[0] + 1.3, -0.45, "$\\vec{u}$", BLUE, 15)
    txt(ax, O[0] - 0.05, 1.1, "$\\vec{v}$", ORANGE, 15, ha="right")
    txt(ax, O[0] + 1.35, 1.75, "$\\vec{u}+\\vec{v}$", GREEN, 14, ha="center")
    txt(ax, O[0] + 1.7, -1.0, "règle du parallélogramme", GREEN, 13, ha="center")
    cadre(ax, (-0.8, 12.2), (-1.4, 3.3))
    _save(fig, I("2nd_vecteurs_chasles.png"))


def produit_reel():
    fig, ax = new_fig(8.4, 3.0)
    u = P(1.6, 0.5)
    for O, k, col, nom in [(P(0, 0), 1, BLUE, "$\\vec{u}$"), (P(2.6, 0), 2, GREEN, "$2\\vec{u}$"),
                           (P(9.6, 1.2), -1.5, ORANGE, "$-1{,}5\\,\\vec{u}$")]:
        fleche(ax, O, O + k * u, col)
        m = O + k * u / 2
        txt(ax, m[0], m[1] + 0.3, nom, col, 15, ha="center")
    txt(ax, 5.4, -0.8, "$k>0$ : même sens ; $k<0$ : sens contraire ; longueur multipliée par $|k|$", DARK, 12,
        ha="center")
    cadre(ax, (-0.4, 10.0), (-1.2, 2.2))
    _save(fig, I("2nd_vecteurs_produit.png"))


def coordonnees():
    fig, ax = new_fig(6.8, 5.6)
    setup_repere(ax, (-1.4, 7.4), (-1.2, 6.4), 1, 1)
    A, B = P(1, 1), P(5, 4)
    ax.plot([A[0], B[0]], [A[1], A[1]], color=ORANGE, lw=1.8, ls="--")
    ax.plot([B[0], B[0]], [A[1], B[1]], color=ORANGE, lw=1.8, ls="--")
    fleche(ax, A, B, BLUE, lw=2.8)
    point(ax, A, "A(1\\,;1)", (0.3, -1.4))
    point(ax, B, "B(5\\,;4)", (0.6, 1))
    txt(ax, 3.4, 0.55, "$x_B - x_A = 4$", ORANGE, 12.5, ha="center", va="center")
    txt(ax, 5.15, 2.5, "$y_B - y_A = 3$", ORANGE, 12.5, va="center")
    txt(ax, 2.0, 3.4, "$\\overrightarrow{AB}\\,(4\\,;3)$", BLUE, 15, ha="center")
    txt(ax, 3.4, 5.6, "$AB = \\sqrt{4^2+3^2} = 5$", GREEN, 14, ha="center", fontweight="bold")
    ax.axis("off")
    _save(fig, I("2nd_vecteurs_coordonnees.png"))


def colineaires():
    fig, ax = new_fig(7.6, 3.6)
    u, v = P(2, 1), P(-3, -1.5)
    fleche(ax, P(0, 0), u)
    fleche(ax, P(4.6, 1.8), P(4.6, 1.8) + v, ORANGE)
    txt(ax, 0.9, 0.8, "$\\vec{u}\\,(2\\,;1)$", BLUE, 14, ha="right")
    txt(ax, 4.0, 0.5, "$\\vec{v}\\,(-3\\,;-1{,}5)$", ORANGE, 14, ha="left")
    txt(ax, 2.4, -1.0, "$\\det(\\vec{u},\\vec{v}) = 2\\times(-1{,}5) - 1\\times(-3) = 0$ : colinéaires", GREEN, 13,
        ha="center", fontweight="bold")
    cadre(ax, (-1.2, 6.2), (-1.4, 2.4))
    _save(fig, I("2nd_vecteurs_colineaires.png"))


parallelogramme()
chasles()
produit_reel()
coordonnees()
colineaires()
