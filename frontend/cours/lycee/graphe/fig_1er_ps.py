# -*- coding: utf-8 -*-
"""Figures : Première — Produit scalaire."""
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Arc, Circle, Polygon

from figlycee import new_fig, _save, txt, I, right_angle, BLUE, ORANGE, GREEN, DARK, NEUTRAL, RED

P = lambda x, y: np.array([x, y], float)  # noqa: E731


def fleche(ax, A, B, col=BLUE, lw=2.4, ms=18):
    ax.annotate("", xy=B, xytext=A, arrowprops=dict(arrowstyle="-|>", color=col, lw=lw, mutation_scale=ms,
                                                    shrinkA=0, shrinkB=0))


def point(ax, Q, nom, d=(0, 1), col=DARK, fs=14):
    ax.scatter([Q[0]], [Q[1]], s=26, color=col, zorder=6)
    ax.annotate(f"${nom}$", Q, textcoords="offset points", xytext=(14 * d[0], 14 * d[1]), ha="center",
                va="center", fontsize=fs, color=col, fontweight="bold")


def projection():
    fig, axs = plt.subplots(1, 2, figsize=(10.0, 4.4))
    fig.patch.set_facecolor("white")
    for ax, C, signe in ((axs[0], P(3.2, 2.4), "> 0"), (axs[1], P(-1.4, 2.4), "< 0")):
        ax.set_facecolor("white")
        A, B = P(0, 0), P(4.6, 0)
        H = P(C[0], 0)
        ax.plot([-2.2, 5.6], [0, 0], color=NEUTRAL, lw=1, ls=":")
        fleche(ax, A, B)
        fleche(ax, A, C, ORANGE)
        ax.plot([C[0], H[0]], [C[1], H[1]], color=NEUTRAL, lw=1.3, ls="--")
        right_angle(ax, H, (1, 0) if C[0] < 0 else (-1, 0), (0, 1), size=0.22)
        ax.plot([A[0], H[0]], [-0.18, -0.18], color=GREEN, lw=4, solid_capstyle="butt")
        dA, dH = ((-0.6, -0.9), (0.6, -1.1)) if C[0] > 0 else ((0.7, -0.9), (-0.7, -1.1))
        for Q, n, d in ((A, "A", dA), (B, "B", (0.6, -0.9)), (C, "C", (0, 1)), (H, "H", dH)):
            point(ax, Q, n, d)
        txt(ax, 1.7, -1.0, f"$\\overrightarrow{{AB}} \\cdot \\overrightarrow{{AC}} {'= AB \\times AH' if C[0] > 0 else '= -AB \\times AH'}$",
            DARK, 13.5, ha="center", va="top")
        txt(ax, 1.7, -1.75, f"angle aigu : produit scalaire {signe}" if C[0] > 0 else
            f"angle obtus : produit scalaire {signe}", GREEN if C[0] > 0 else RED, 12.5, ha="center", va="top")
        ax.set_xlim(-2.4, 5.8)
        ax.set_ylim(-2.4, 3.2)
        ax.set_aspect("equal")
        ax.axis("off")
    _save(fig, I("1er_ps_projection.png"))


def alkashi():
    fig, ax = new_fig(7.0, 4.8)
    A, B = P(0, 0), P(6, 0)
    C = P(2.5 * np.cos(np.radians(60)) * 2, 2.5 * np.sin(np.radians(60)) * 2)
    ax.add_patch(Polygon([A, B, C], closed=True, fc="#eaf2f8", ec=BLUE, lw=2.2))
    ax.add_patch(Arc(A, 1.6, 1.6, theta1=0, theta2=60, color=RED, lw=2))
    txt(ax, 0.95, 0.35, "$\\hat{A}$", RED, 15)
    for Q, n, d in ((A, "A", (-0.8, -0.6)), (B, "B", (0.8, -0.6)), (C, "C", (0, 1))):
        point(ax, Q, n, d)
    txt(ax, 3.0, -0.3, "$c = AB$", DARK, 13, ha="center", va="top")
    txt(ax, 0.95, 2.5, "$b = AC$", DARK, 13, ha="right", va="center")
    txt(ax, 4.6, 2.5, "$a = BC$", ORANGE, 13, ha="left", va="center", fontweight="bold")
    txt(ax, 3.0, -1.0, "$a^2 = b^2 + c^2 - 2bc\\cos\\hat{A}$", DARK, 15, ha="center", va="top", fontweight="bold")
    ax.set_xlim(-0.8, 7.2)
    ax.set_ylim(-1.9, 5.2)
    ax.set_aspect("equal")
    ax.axis("off")
    _save(fig, I("1er_ps_alkashi.png"))


def cercle():
    fig, ax = new_fig(6.4, 5.6)
    A, B = P(-2.5, 0), P(2.5, 0)
    ax.add_patch(Circle((0, 0), 2.5, fill=False, ec=BLUE, lw=2.2))
    ax.plot([A[0], B[0]], [0, 0], color=NEUTRAL, lw=1.4)
    t = np.radians(65)
    M = P(2.5 * np.cos(t), 2.5 * np.sin(t))
    fleche(ax, M, A, ORANGE)
    fleche(ax, M, B, ORANGE)
    u, v = (A - M) / np.linalg.norm(A - M), (B - M) / np.linalg.norm(B - M)
    right_angle(ax, M, u, v, size=0.32, color=RED)
    for Q, n, d in ((A, "A", (-1, 0)), (B, "B", (1, 0)), (M, "M", (0.4, 1)), (P(0, 0), "I", (0, -1))):
        point(ax, Q, n, d)
    txt(ax, 0, -3.0, "$\\overrightarrow{MA} \\cdot \\overrightarrow{MB} = 0 \\Leftrightarrow M$ est sur le cercle de diamètre $[AB]$",
        DARK, 12.5, ha="center", va="top")
    ax.set_xlim(-3.4, 3.4)
    ax.set_ylim(-3.7, 3.1)
    ax.set_aspect("equal")
    ax.axis("off")
    _save(fig, I("1er_ps_cercle.png"))


projection()
alkashi()
cercle()
