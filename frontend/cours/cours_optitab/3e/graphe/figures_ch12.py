# -*- coding: utf-8 -*-
"""Figures du chapitre 12 (Pythagore) — 3ème OptiTAB."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fig3e import (new_fig, finish, triangle_rect, graphe, dot_label, seg_label,
                   right_angle, tick_marks, BLUE, ORANGE, GREEN, DARK, NEUTRAL,
                   DIR_COURS, DIR_EXOS)
import numpy as np
import matplotlib.patches as mp


def carres():
    """Triangle 3-4-5 rectangle en A avec les carrés construits sur les côtés."""
    fig, ax = new_fig(7.2, 7.0)
    A, B, C = np.array([0., 0.]), np.array([4., 0.]), np.array([0., 3.])
    # carré sur AB (en dessous)
    ax.add_patch(mp.Polygon([A, B, B + [0, -4], A + [0, -4]], closed=True,
                            facecolor="#d6eafc", edgecolor=BLUE, lw=1.8))
    ax.text(2, -2, "$AB^2 = 16$", ha="center", va="center", fontsize=13, color=BLUE,
            fontweight="bold")
    # carré sur AC (à gauche)
    ax.add_patch(mp.Polygon([A, C, C + [-3, 0], A + [-3, 0]], closed=True,
                            facecolor="#d6eafc", edgecolor=BLUE, lw=1.8))
    ax.text(-1.5, 1.5, "$AC^2 = 9$", ha="center", va="center", fontsize=13, color=BLUE,
            fontweight="bold")
    # carré sur BC (extérieur)
    u = (C - B) / 5
    n = np.array([u[1], -u[0]]) * -1  # normale extérieure
    n = np.array([3, 4]) / 5
    P3, P4 = C + 5 * n, B + 5 * n
    ax.add_patch(mp.Polygon([B, C, P3, P4], closed=True, facecolor="#fdebd0",
                            edgecolor=ORANGE, lw=1.8))
    ctr = (B + C + P3 + P4) / 4
    ax.text(ctr[0], ctr[1], "$BC^2 = 25$", ha="center", va="center", fontsize=14,
            color=ORANGE, fontweight="bold")
    ax.plot([A[0], B[0], C[0], A[0]], [A[1], B[1], C[1], A[1]], lw=2.6, color=DARK)
    right_angle(ax, A, (1, 0), (0, 1), size=0.32)
    for P, nom, off in [(A, "A", (-16, -16)), (B, "B", (6, -16)), (C, "C", (-16, 6))]:
        dot_label(ax, P, f"${nom}$", *off, color=DARK, s=40)
    ax.text(1.2, -5.0, r"$9 + 16 = 25$  donc  $AB^2 + AC^2 = BC^2$", fontsize=13,
            ha="center", color=GREEN, fontweight="bold")
    finish(fig, ax, os.path.join(DIR_COURS, "pythagore_3e_carres.png"),
           [(-3.3, -5.5), (7.3, 7.2)], margin=0.2)


carres()

M = lambda P, Q, t, **kw: (P, Q, t, kw)  # noqa: E731
lab = dict(color=DARK, fs=12.5)
inc = dict(color=ORANGE, fs=13.5, weight="bold")

# Exercices : triangles rectangles en A (AB horizontal, AC vertical)
triangle_rect(os.path.join(DIR_EXOS, "pythagore_3e_6_8.png"), 4.8, 3.6,
              measures=[M("A", "B", "$AB = 6$ cm", side=-1, offset=0.38, **lab),
                        M("A", "C", "$AC = 8$ cm", side=1, offset=0.85, **lab),
                        M("B", "C", "$BC = $ ?", side=-1, offset=0.55, **inc)])
# NB : dessin non à l'échelle exacte, l'énoncé fait foi
triangle_rect(os.path.join(DIR_EXOS, "pythagore_3e_5_13.png"), 2.4, 5.76,
              measures=[M("A", "B", "$AB = 5$ cm", side=-1, offset=0.38, **lab),
                        M("A", "C", "$AC = $ ?", side=1, offset=0.85, **inc),
                        M("B", "C", "$BC = 13$ cm", side=-1, offset=0.75, **lab)])


def echelle():
    fig, ax = new_fig(6.2, 6.2)
    ax.plot([-0.3, 3.2], [0, 0], lw=2.4, color=NEUTRAL)            # sol
    ax.add_patch(mp.Rectangle((-0.5, 0), 0.5, 5.4, facecolor="#e0e0e0",
                              edgecolor=NEUTRAL, lw=1.4))            # mur
    A, B, C = np.array([0, 0]), np.array([1.4, 0]), np.array([0, 4.8])
    ax.plot([B[0], C[0]], [B[1], C[1]], lw=4, color=ORANGE, solid_capstyle="round")
    for t in np.linspace(0.12, 0.88, 7):
        P = B + t * (C - B)
        ax.plot([P[0] - 0.12, P[0] + 0.12], [P[1] - 0.05, P[1] + 0.05], lw=1.5,
                color="#a04000")
    right_angle(ax, A, (1, 0), (0, 1), size=0.25)
    for P, nom, off in [(A, "A", (-18, -16)), (B, "B", (6, -16)), (C, "C", (8, 2))]:
        dot_label(ax, P, f"${nom}$", *off, color=DARK, s=40)
    seg_label(ax, A, B, "1,4 m", side=-1, offset=0.35, color=DARK, fs=12.5)
    seg_label(ax, B, C, "échelle : 5 m", side=-1, offset=0.6, color=ORANGE, fs=12.5,
              weight="bold")
    ax.text(0.25, 2.4, "?", fontsize=16, color=ORANGE, fontweight="bold")
    finish(fig, ax, os.path.join(DIR_EXOS, "pythagore_3e_echelle.png"),
           [(-0.8, -0.6), (3.4, 5.6)], margin=0.2)


echelle()


def extra_repere(ax):
    ax.plot([1, 7], [2, 2], lw=1.8, color=ORANGE, linestyle="--")
    ax.plot([7, 7], [2, 10], lw=1.8, color=ORANGE, linestyle="--")
    ax.plot([1, 7], [2, 10], lw=2.4, color=BLUE)
    ax.text(4, 1.2, "6", fontsize=13, color=ORANGE, fontweight="bold", ha="center")
    ax.text(7.35, 6, "8", fontsize=13, color=ORANGE, fontweight="bold")
    ax.plot([6.6, 6.6, 7], [2, 2.4, 2.4], lw=1.3, color=NEUTRAL)


graphe(os.path.join(DIR_EXOS, "pythagore_3e_repere.png"),
       points=[("$A(1\\,;2)$", 1, 2, BLUE), ("$B(7\\,;10)$", 7, 10, BLUE)],
       xb=(-0.8, 9.2), yb=(-0.8, 11.6), extra=extra_repere, w=6.6, h=7.2, equal=True)


def parc():
    fig, ax = new_fig(8.0, 5.4)
    L, H = 8.0, 6.0  # 160 × 120 à l'échelle 1/20
    ax.add_patch(mp.Rectangle((0, 0), L, H, facecolor="#e8f5e9", edgecolor=GREEN, lw=2.2))
    ax.plot([0, L], [0, H], lw=2.6, color=ORANGE, linestyle="--")
    ax.plot([0, L, L], [0, 0, H], lw=3.2, color=BLUE, alpha=0.75)
    for P, nom, off in [((0, 0), "D", (-16, -16)), ((L, 0), "E", (6, -16)),
                        ((L, H), "F", (6, 4))]:
        dot_label(ax, P, f"${nom}$", *off, color=DARK, s=45)
    ax.text(L / 2, -0.55, "160 m", ha="center", fontsize=12.5, color=DARK)
    ax.text(L + 0.25, H / 2, "120 m", va="center", fontsize=12.5, color=DARK)
    ax.text(3.0, 3.1, "diagonale", fontsize=12, color=ORANGE, fontweight="bold",
            rotation=36.9)
    finish(fig, ax, os.path.join(DIR_EXOS, "pythagore_3e_parc.png"),
           [(-0.6, -1.0), (L + 1.2, H + 0.5)], margin=0.15)


parc()


def isocele():
    fig, ax = new_fig(6.4, 6.4)
    A, B, C = np.array([0., 0.]), np.array([5., 0.]), np.array([2.5, 6.0])
    Hh = np.array([2.5, 0.])
    ax.plot([A[0], B[0], C[0], A[0]], [A[1], B[1], C[1], A[1]], lw=2.4, color=BLUE)
    ax.plot([C[0], Hh[0]], [C[1], Hh[1]], lw=2.0, color=ORANGE, linestyle="--")
    right_angle(ax, Hh, (1, 0), (0, 1), size=0.28)
    tick_marks(ax, A, Hh, n=1)
    tick_marks(ax, Hh, B, n=1)
    tick_marks(ax, A, C, n=2)
    tick_marks(ax, B, C, n=2)
    for P, nom, off, col in [(A, "A", (-16, -16), BLUE), (B, "B", (6, -16), BLUE),
                             (C, "C", (-5, 8), BLUE), (Hh, "H", (-5, -20), ORANGE)]:
        dot_label(ax, P, f"${nom}$", *off, color=col, s=40)
    seg_label(ax, A, C, "13 cm", side=1, offset=0.45, color=DARK, fs=12.5)
    seg_label(ax, B, C, "13 cm", side=-1, offset=0.45, color=DARK, fs=12.5)
    ax.text(2.5, -0.85, "$AB = 10$ cm", ha="center", fontsize=12.5, color=DARK)
    ax.text(2.75, 2.8, "?", fontsize=15, color=ORANGE, fontweight="bold")
    finish(fig, ax, os.path.join(DIR_EXOS, "pythagore_3e_isocele.png"),
           [(-0.8, -1.3), (5.8, 6.8)], margin=0.15)


isocele()
print("Figures chapitre 12 : OK")
