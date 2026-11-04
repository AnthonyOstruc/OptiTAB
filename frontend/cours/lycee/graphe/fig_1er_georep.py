# -*- coding: utf-8 -*-
"""Figures : Première — Géométrie repérée."""
import numpy as np
from matplotlib.patches import Circle

from figlycee import new_fig, _save, setup_repere, txt, I, right_angle, BLUE, ORANGE, GREEN, DARK, NEUTRAL, RED

P = lambda x, y: np.array([x, y], float)  # noqa: E731
BOITE = dict(fc="white", ec="none", pad=1.5)


def fleche(ax, A, B, col=BLUE, lw=2.6, ms=18):
    ax.annotate("", xy=B, xytext=A, arrowprops=dict(arrowstyle="-|>", color=col, lw=lw, mutation_scale=ms,
                                                    shrinkA=0, shrinkB=0))


def point(ax, Q, nom, d=(0, 1), col=DARK, fs=13):
    ax.scatter([Q[0]], [Q[1]], s=28, color=col, zorder=6)
    ax.annotate(f"${nom}$", Q, textcoords="offset points", xytext=(16 * d[0], 14 * d[1]), ha="center",
                va="center", fontsize=fs, color=col, fontweight="bold", bbox=BOITE)


def fin(ax):
    ax.set_aspect("equal")
    ax.axis("off")


def normal():
    fig, ax = new_fig(6.8, 6.0)
    setup_repere(ax, (-1.4, 5.4), (-1.6, 5.4))
    x = np.linspace(-0.6, 2.7, 10)
    ax.plot(x, 4 - 2 * x, color=BLUE, lw=2.6)
    A = P(1, 2)
    fleche(ax, A, A + P(2, 1), GREEN, lw=2.8)
    M = P(0.2, 3.6)
    ax.plot([A[0], M[0]], [A[1], M[1]], color=ORANGE, lw=2)
    right_angle(ax, A, (2 / np.sqrt(5), 1 / np.sqrt(5)), (-1 / np.sqrt(5), 2 / np.sqrt(5)), size=0.3)
    point(ax, A, "A(1\\,;2)", (1.9, -0.5))
    point(ax, M, "M(x\\,;y)", (1.9, 0.5))
    txt(ax, 3.1, 3.25, "$\\vec{n}\\,(2\\,;1)$", GREEN, 14, fontweight="bold")
    txt(ax, 2.7, -1.0, "$d : 2x + y - 4 = 0$", BLUE, 13.5, ha="left", va="center", fontweight="bold")
    txt(ax, 2.0, -2.2, "$M \\in d \\Leftrightarrow \\overrightarrow{AM} \\cdot \\vec{n} = 0$", DARK, 13.5, ha="center",
        va="top")
    fin(ax)
    _save(fig, I("1er_georep_normal.png"))


def projete():
    fig, ax = new_fig(6.8, 6.0)
    setup_repere(ax, (-1.4, 5.4), (-1.6, 5.4))
    x = np.linspace(-0.6, 2.7, 10)
    ax.plot(x, 4 - 2 * x, color=BLUE, lw=2.6)
    M, H = P(4, 3), P(6 / 5, 8 / 5)
    ax.plot([M[0], H[0]], [M[1], H[1]], color=GREEN, lw=2.4)
    right_angle(ax, H, (-1 / np.sqrt(5), 2 / np.sqrt(5)), (2 / np.sqrt(5), 1 / np.sqrt(5)), size=0.3)
    point(ax, M, "M(4\\,;3)", (0.3, 1.1))
    point(ax, H, "H\\left(\\frac{6}{5}\\,;\\frac{8}{5}\\right)", (3.5, -1.4), col=RED)
    txt(ax, 2.75, 2.05, "$MH = \\frac{7\\sqrt{5}}{5}$", GREEN, 13.5, ha="left", va="top", fontweight="bold")
    txt(ax, 2.7, -1.0, "$d : 2x + y - 4 = 0$", BLUE, 13.5, ha="left", va="center", fontweight="bold")
    fin(ax)
    _save(fig, I("1er_georep_projete.png"))


def cercle():
    fig, ax = new_fig(6.6, 6.2)
    setup_repere(ax, (-1.6, 5.8), (-2.6, 4.8))
    O = P(2, 1)
    ax.add_patch(Circle(O, 3, fill=False, ec=BLUE, lw=2.6))
    t = np.radians(50)
    M = O + 3 * P(np.cos(t), np.sin(t))
    ax.plot([O[0], M[0]], [O[1], M[1]], color=ORANGE, lw=2)
    txt(ax, 2.55, 2.45, "$r = 3$", ORANGE, 13.5, ha="right", fontweight="bold", bbox=BOITE)
    point(ax, O, "\\Omega(2\\,;1)", (0.3, -1.1))
    point(ax, M, "M(x\\,;y)", (1.3, 0.6))
    txt(ax, 2.0, -2.9, "$(x - 2)^2 + (y - 1)^2 = 9$", BLUE, 14, ha="center", va="top", fontweight="bold")
    fin(ax)
    _save(fig, I("1er_georep_cercle.png"))


def parabole():
    fig, ax = new_fig(6.4, 5.6)
    setup_repere(ax, (-0.8, 4.8), (-1.6, 4.4))
    x = np.linspace(-0.2, 4.2, 200)
    ax.plot(x, x ** 2 - 4 * x + 3, color=BLUE, lw=2.6)
    ax.axvline(2, color=ORANGE, lw=1.6, ls="--", ymin=0.02, ymax=0.97)
    for a in (1, 3):
        ax.scatter([a], [0], s=30, color=GREEN, zorder=6)
    ax.plot([0.5, 3.5], [1.25, 1.25], color=NEUTRAL, lw=1.1, ls=":")
    ax.scatter([0.5, 3.5], [1.25, 1.25], s=22, color=NEUTRAL, zorder=6)
    point(ax, P(2, -1), "S(2\\,;-1)", (2.1, -0.3), col=RED)
    txt(ax, 2.1, 3.9, "axe $x = 2$", ORANGE, 13, fontweight="bold", bbox=BOITE)
    txt(ax, 2.0, -1.75, "$y = x^2 - 4x + 3 = (x - 2)^2 - 1$", BLUE, 13.5, ha="center", va="top")
    fin(ax)
    _save(fig, I("1er_georep_parabole.png"))


normal()
projete()
cercle()
parabole()
