# -*- coding: utf-8 -*-
"""Figures : Terminale — Orthogonalité et distances dans l'espace."""
import numpy as np
from matplotlib.patches import Polygon

from figlycee import new_fig, _save, txt, I, BLUE, ORANGE, GREEN, DARK, NEUTRAL, RED, PURPLE
from fig_term_esp import pr, seg, fleche, nom, cube, CUBE

add = lambda p, q: tuple(a + b for a, b in zip(p, q))  # noqa: E731
mul = lambda k, p: tuple(k * a for a in p)  # noqa: E731


def angle_droit(ax, H, u, v, s=0.35, col=NEUTRAL):
    p1 = add(H, mul(s, u))
    p2 = add(p1, mul(s, v))
    p3 = add(H, mul(s, v))
    seg(ax, p1, p2, col, 1.2)
    seg(ax, p2, p3, col, 1.2)


def plan(ax, pts, col=BLUE):
    ax.add_patch(Polygon([pr(p) for p in pts], closed=True, fc="#e8f4fd", ec=col, lw=1.5))


def normal():
    fig, ax = new_fig(7.4, 5.4)
    plan(ax, [(0, 0, 0), (6, 0, 0), (6, 5, 0), (0, 5, 0)])
    A, M = (2, 1.5, 0), (4.6, 3.4, 0)
    fleche(ax, A, (2, 1.5, 2.8), RED)
    seg(ax, A, M, ORANGE, 2.2)
    u = np.array(M) - np.array(A)
    u = tuple(u / np.linalg.norm(u))
    angle_droit(ax, A, u, (0, 0, 1))
    nom(ax, A, "A", (-0.3, -0.25))
    nom(ax, M, "M", (0.3, -0.2))
    nom(ax, (2, 1.5, 2.8), "\\vec{n}\\,(a\\,;b\\,;c)", (0.9, 0.15), RED, 13)
    txt(ax, 7.6, 0.6, "plan $\\mathcal{P}$", BLUE, 13)
    txt(ax, 3.8, -0.75, "$M \\in \\mathcal{P} \\Leftrightarrow \\overrightarrow{AM} \\cdot \\vec{n} = 0 \\Leftrightarrow ax + by + cz + d = 0$",
        DARK, 13, ha="center", va="top")
    ax.set_xlim(-0.5, 8.8)
    ax.set_ylim(-1.5, 4.0)
    ax.set_aspect("equal")
    ax.axis("off")
    _save(fig, I("term_ps_normal.png"))


def projete():
    fig, ax = new_fig(7.4, 5.4)
    plan(ax, [(0, 0, 0), (6, 0, 0), (6, 5, 0), (0, 5, 0)])
    M, H = (3, 2.5, 2.8), (3, 2.5, 0)
    N = (5.0, 3.6, 0)
    seg(ax, M, H, GREEN, 2.6)
    seg(ax, M, N, ORANGE, 1.6, "--")
    seg(ax, H, N, NEUTRAL, 1.2, ":")
    w = np.array(N) - np.array(H)
    angle_droit(ax, H, tuple(w / np.linalg.norm(w)), (0, 0, 1))
    nom(ax, M, "M", (0, 0.3))
    nom(ax, H, "H", (-0.35, -0.2), RED)
    nom(ax, N, "N", (0.3, -0.2))
    ax.scatter(*pr(H), s=34, color=RED, zorder=6)
    ax.scatter(*pr(M), s=34, color=DARK, zorder=6)
    txt(ax, pr(M)[0] - 0.15, (pr(M)[1] + pr(H)[1]) / 2, "$MH$", GREEN, 14, ha="right", va="center", fontweight="bold")
    txt(ax, 3.8, -0.75, "$H$ projeté orthogonal de $M$ sur $\\mathcal{P}$ : $MH \\leq MN$ pour tout $N$ de $\\mathcal{P}$",
        DARK, 12.5, ha="center", va="top")
    ax.set_xlim(-0.5, 8.4)
    ax.set_ylim(-1.5, 4.2)
    ax.set_aspect("equal")
    ax.axis("off")
    _save(fig, I("term_ps_projete.png"))


def cube_bde():
    fig, ax = new_fig(7.0, 5.8)
    ax.add_patch(Polygon([pr(CUBE[s]) for s in "BDE"], closed=True, fc="#fdebd0", ec=ORANGE, lw=2, alpha=0.9))
    cube(ax)
    seg(ax, CUBE["A"], CUBE["G"], PURPLE, 2.6)
    K = (1, 1, 1)
    ax.scatter(*pr(K), s=36, color=RED, zorder=6)
    nom(ax, K, "K", (0.28, -0.2), RED, 13)
    txt(ax, 2.2, -1.0, "$(AG)$ est orthogonale au plan $(BDE)$ :\n$\\overrightarrow{AG} \\cdot \\overrightarrow{BD} = 0$ et $\\overrightarrow{AG} \\cdot \\overrightarrow{BE} = 0$",
        DARK, 12.5, ha="center", va="top")
    ax.set_xlim(-1.0, 5.6)
    ax.set_ylim(-2.3, 4.6)
    ax.set_aspect("equal")
    ax.axis("off")
    _save(fig, I("term_ps_cube.png"))


normal()
projete()
cube_bde()
