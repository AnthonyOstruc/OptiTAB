# -*- coding: utf-8 -*-
"""Figures complémentaires du chapitre 13 (Thalès) — extension à 21 exercices."""
import os
import sys
from math import radians, cos, sin

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fig3e import (new_fig, finish, dot_label, seg_label, add_parallel_marks,
                   tick_marks, right_angle, BLUE, ORANGE, GREEN, DARK, NEUTRAL,
                   DIR_EXOS)
import numpy as np
import matplotlib.patches as mp


def thales_fig(path, kM=0.6, AB=6.0, AC=5.2, theta=55.0, labels=(), marks=True,
               extra=None):
    A = np.array([0.0, 0.0])
    B = np.array([AB, 0.0])
    C = A + AC * np.array([cos(radians(theta)), sin(radians(theta))])
    M = A + kM * (B - A)
    N = A + kM * (C - A)
    fig, ax = new_fig(8.2, 5.2)
    ax.plot([A[0], B[0], C[0], A[0]], [A[1], B[1], C[1], A[1]], lw=2.2, color=BLUE)
    for P, Q in [(A, M), (A, N), (M, N)]:
        ax.plot([P[0], Q[0]], [P[1], Q[1]], lw=3.0, color=ORANGE, zorder=3)
    if marks:
        add_parallel_marks(ax, B, C)
        add_parallel_marks(ax, M, N)
    dot_label(ax, A, "$A$", -20, -18, color="0.1", s=90)
    dot_label(ax, B, "$B$", 10, -18, color=BLUE)
    dot_label(ax, C, "$C$", 8, 4, color=BLUE)
    dot_label(ax, M, "$M$", 2, -20, color=ORANGE)
    dot_label(ax, N, "$N$", -20, 6, color=ORANGE)
    pts = {"A": A, "B": B, "C": C, "M": M, "N": N}
    for seg, text, kw in labels:
        seg_label(ax, pts[seg[0]], pts[seg[1]], text, **kw)
    if extra:
        extra(ax, pts)
    finish(fig, ax, path, [A, B, C, M, N])


# D5 — retrouver le grand côté : AM = 6, AN = 4, AC = 10, AB = ?
thales_fig(
    os.path.join(DIR_EXOS, "thales_3e_ex_d5.png"), kM=0.6, AB=6.4, AC=5.2,
    labels=[
        ("AM", "$AM = 6$ cm", dict(side=-1, offset=0.42, color=DARK, fs=12)),
        ("AB", "$AB = $ ?", dict(side=-1, offset=1.05, t=0.62, color=ORANGE, fs=13, weight="bold")),
        ("AN", "$AN = 4$ cm", dict(side=1, offset=0.42, color=DARK, fs=12)),
        ("AC", "$AC = 10$ cm", dict(side=1, offset=1.2, t=0.8, color=DARK, fs=12)),
    ],
)

# P4 — largeur inaccessible : M, N milieux, MN = 7,4 m, BC = ?
def extra_milieux(ax, p):
    tick_marks(ax, p["A"], p["M"], n=1, color=GREEN)
    tick_marks(ax, p["M"], p["B"], n=1, color=GREEN)
    tick_marks(ax, p["A"], p["N"], n=2, color=GREEN)
    tick_marks(ax, p["N"], p["C"], n=2, color=GREEN)
    mid = (p["B"] + p["C"]) / 2
    ax.add_patch(mp.Ellipse(mid + np.array([-1.3, -0.5]), 2.2, 1.1, angle=-38,
                            facecolor="#eef2f5", edgecolor="0.6", lw=1.2,
                            linestyle="--", zorder=1))
    ax.text(mid[0] - 1.3, mid[1] - 0.5, "zone\ninaccessible", fontsize=9.5,
            ha="center", va="center", color="0.45", style="italic")

thales_fig(
    os.path.join(DIR_EXOS, "thales_3e_milieux.png"), kM=0.5, AB=7.0, AC=5.6,
    labels=[
        ("MN", "$MN = 7{,}4$ m", dict(side=-1, offset=0.95, t=0.6, color=DARK, fs=12)),
        ("BC", "$BC = $ ?", dict(side=-1, offset=0.85, t=0.3, color=ORANGE, fs=13, weight="bold")),
    ],
    extra=extra_milieux,
)

# P5 — la hauteur du phare (œil, bâton, phare alignés)
def phare():
    fig, ax = new_fig(9.6, 5.0)
    ax.plot([-0.8, 14.6], [0, 0], lw=2.2, color=NEUTRAL)
    # œil au sol en A (origine), bâton en M (x=1.2, h=0.8), phare en B (x=13, h=?)
    A = np.array([0.0, 0.0])
    xb, hb = 1.2, 0.8          # bâton : 3 m -> 1.2 ; 2 m -> 0.8 (échelle 0,4)
    xp, hp = 13.0, 26 * 13 / 39 * 0.8 / (2 * 3 / 39 / 0.4 / 10)  # calculé ci-dessous
    hp = 13 * hb / xb  # alignement exact des sommets
    ax.plot([xb, xb], [0, hb], lw=4.5, color=ORANGE, solid_capstyle="round")
    ax.add_patch(mp.Rectangle((xp - 0.35, 0), 0.7, hp, facecolor="#d6eafc",
                              edgecolor=BLUE, lw=2.0))
    ax.add_patch(mp.Rectangle((xp - 0.5, hp), 1.0, 0.5, facecolor="#fdebd0",
                              edgecolor=ORANGE, lw=1.6))
    # ligne de visée
    ax.plot([0, xp], [0, hp], lw=1.5, color="0.4", linestyle="--")
    ax.scatter([0], [0], s=70, color=DARK, zorder=5)
    ax.annotate("œil ($A$)", (0, 0), textcoords="offset points", xytext=(-14, 10),
                fontsize=11.5, color=DARK, fontweight="bold")
    right_angle(ax, (xb, 0), (1, 0), (0, 1), size=0.22)
    right_angle(ax, (xp - 0.35, 0), (-1, 0), (0, 1), size=0.3)
    ax.annotate("", xy=(xb, -0.55), xytext=(0, -0.55),
                arrowprops=dict(arrowstyle="<->", lw=1.4, color=DARK))
    ax.text(xb / 2, -1.0, "3 m", fontsize=12, ha="center", color=DARK)
    ax.annotate("", xy=(xp, -1.35), xytext=(0, -1.35),
                arrowprops=dict(arrowstyle="<->", lw=1.4, color=DARK))
    ax.text(xp / 2, -1.8, "39 m", fontsize=12, ha="center", color=DARK)
    ax.text(xb + 0.3, hb / 2, "2 m", fontsize=12, color=ORANGE, va="center",
            fontweight="bold")
    ax.text(xp + 0.8, hp / 2, "$h = $ ?", fontsize=14, color=ORANGE, va="center",
            fontweight="bold")
    finish(fig, ax, os.path.join(DIR_EXOS, "thales_3e_phare.png"),
           [(-1.2, -2.2), (14.8, hp + 1.2)], margin=0.3)

phare()

# P7 — Thalès et réciproque ensemble : AM = 4,5, AB = 7,5, AN = 6, AC = 10, MN = 4,2
thales_fig(
    os.path.join(DIR_EXOS, "thales_3e_p7.png"), kM=0.6, AB=7.0, AC=5.6, marks=False,
    labels=[
        ("AM", "$AM = 4{,}5$", dict(side=-1, offset=0.42, color=DARK, fs=12)),
        ("AB", "$AB = 7{,}5$", dict(side=-1, offset=1.05, t=0.65, color=DARK, fs=12)),
        ("AN", "$AN = 6$", dict(side=1, offset=0.42, color=DARK, fs=12)),
        ("AC", "$AC = 10$", dict(side=1, offset=1.2, t=0.8, color=DARK, fs=12)),
        ("MN", "$MN = 4{,}2$", dict(side=-1, offset=0.9, t=0.55, color=DARK, fs=12)),
        ("BC", "$BC = $ ?", dict(side=-1, offset=0.5, color=ORANGE, fs=13, weight="bold")),
    ],
)

print("Figures ch13 complémentaires : OK")
