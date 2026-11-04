# -*- coding: utf-8 -*-
"""Figures : Seconde — Résoudre des problèmes de géométrie."""
from math import tan, radians

import numpy as np
from matplotlib.patches import Polygon, Arc, Ellipse

from figlycee import new_fig, _save, right_angle, txt, cadre, I, BLUE, ORANGE, GREEN, DARK, NEUTRAL, RED

P = lambda x, y: np.array([x, y], float)  # noqa: E731


def point(ax, Q, nom, d=(0, 1), col=DARK, fs=14):
    ax.scatter([Q[0]], [Q[1]], s=26, color=col, zorder=6)
    ax.annotate(f"${nom}$", Q, textcoords="offset points", xytext=(14 * d[0], 14 * d[1]), ha="center",
                va="center", fontsize=fs, color=col, fontweight="bold")


def projete():
    fig, ax = new_fig(7.4, 4.2)
    ax.plot([-0.5, 8.5], [0, 0], color=DARK, lw=2)
    M, H, N = P(3, 3), P(3, 0), P(6.2, 0)
    ax.plot([M[0], H[0]], [M[1], H[1]], color=GREEN, lw=2.6)
    ax.plot([M[0], N[0]], [M[1], N[1]], color=ORANGE, lw=2, ls="--")
    right_angle(ax, H, (1, 0), (0, 1), size=0.3)
    point(ax, M, "M", (0, 1))
    point(ax, H, "H", (0, -1.2))
    point(ax, N, "N", (0, -1.2))
    txt(ax, 8.3, 0.2, "$d$", DARK, 15)
    txt(ax, 2.85, 1.5, "$MH$", GREEN, 13, ha="right", fontweight="bold")
    txt(ax, 4.85, 1.75, "$MN$", ORANGE, 13, fontweight="bold")
    txt(ax, 4.0, -1.2, "$MN^2 = MH^2 + HN^2 > MH^2$ : $H$ est le point de $d$ le plus proche de $M$", DARK, 11.5,
        ha="center")
    cadre(ax, (-0.7, 8.7), (-1.6, 3.8))
    _save(fig, I("2nd_geometrie_projete.png"))


def trigo():
    fig, ax = new_fig(7.6, 4.6)
    A, B, C = P(0, 0), P(6, 0), P(6, 3.5)
    ax.add_patch(Polygon([A, B, C], closed=True, facecolor="#eaf2f8", edgecolor="none"))
    ax.plot([A[0], B[0]], [A[1], B[1]], color=ORANGE, lw=3.5)
    ax.plot([B[0], C[0]], [B[1], C[1]], color=GREEN, lw=3.5)
    ax.plot([A[0], C[0]], [A[1], C[1]], color=BLUE, lw=3.5)
    right_angle(ax, B, (-1, 0), (0, 1), size=0.35)
    ax.add_patch(Arc(A, 1.8, 1.8, theta1=0, theta2=30.3, color=RED, lw=2))
    txt(ax, 1.15, 0.3, "$\\alpha$", RED, 16)
    txt(ax, 3, -0.35, "côté adjacent à $\\alpha$", ORANGE, 12.5, ha="center", va="top", fontweight="bold")
    txt(ax, 6.2, 1.75, "côté\nopposé à $\\alpha$", GREEN, 12.5, va="center", fontweight="bold")
    txt(ax, 2.5, 2.1, "hypoténuse", BLUE, 12.5, ha="center", rotation=30.3, fontweight="bold")
    for Q, n, d in [(A, "A", (-1, -0.6)), (B, "B", (1, -0.6)), (C, "C", (0.3, 1))]:
        point(ax, Q, n, d)
    txt(ax, 9.6, 2.8, "$\\cos\\alpha = \\frac{\\mathrm{adjacent}}{\\mathrm{hypoténuse}}$", DARK, 14)
    txt(ax, 9.6, 1.7, "$\\sin\\alpha = \\frac{\\mathrm{opposé}}{\\mathrm{hypoténuse}}$", DARK, 14)
    txt(ax, 9.6, 0.6, "$\\tan\\alpha = \\frac{\\mathrm{opposé}}{\\mathrm{adjacent}}$", DARK, 14)
    cadre(ax, (-0.8, 14.2), (-1.2, 4.2))
    _save(fig, I("2nd_geometrie_trigo.png"))


def arbre():
    fig, ax = new_fig(7.6, 4.6)
    ax.plot([-1, 9], [0, 0], color=NEUTRAL, lw=2)
    O, H = P(0, 0), P(8, 0)
    T = P(8, 8 * tan(radians(35)))
    ax.plot([8, 8], [0, T[1]], color="#8d6e63", lw=6)
    for dx, dy, r in [(0, 0.4, 1.2), (-0.7, -0.1, 0.8), (0.7, -0.1, 0.8)]:
        ax.add_patch(Ellipse((8 + dx, T[1] + dy), 2 * r, 1.6 * r, color="#7cb342", alpha=0.45))
    ax.plot([O[0], T[0]], [O[1], T[1]], color=ORANGE, lw=1.8, ls="--")
    ax.add_patch(Arc(O, 2.4, 2.4, theta1=0, theta2=35, color=RED, lw=2))
    txt(ax, 1.4, 0.3, "$35°$", RED, 14)
    right_angle(ax, H, (-1, 0), (0, 1), size=0.3)
    ax.annotate("", xy=(8, -0.6), xytext=(0, -0.6), arrowprops=dict(arrowstyle="<->", color=DARK))
    txt(ax, 4, -0.8, "$20$ m", DARK, 13, ha="center", va="top")
    txt(ax, 8.3, T[1] / 2, "$h = 20\\tan 35° \\approx 14$ m", GREEN, 13, fontweight="bold", va="center")
    point(ax, O, "O", (-1, -0.4))
    point(ax, H, "H", (1, -0.6))
    point(ax, T, "S", (-1, 0.6))
    cadre(ax, (-1.2, 13.4), (-1.6, T[1] + 1.6))
    _save(fig, I("2nd_geometrie_arbre.png"))


def volumes():
    fig, ax = new_fig(10.4, 3.8)
    t = np.linspace(0, 2 * np.pi, 120)
    # pyramide
    base = [P(0, 0), P(2.2, 0), P(2.9, 0.7), P(0.7, 0.7)]
    S = P(1.45, 2.6)
    ax.add_patch(Polygon(base, closed=True, facecolor="#eaf2f8", edgecolor=BLUE, lw=1.6))
    for Q in base:
        ax.plot([Q[0], S[0]], [Q[1], S[1]], color=BLUE, lw=1.6)
    txt(ax, 1.45, -0.55, "pyramide\n$V = \\frac{1}{3}\\mathcal{B}h$", DARK, 12, ha="center", va="top")
    # cône
    cx = 4.6
    ax.plot(cx + 1.0 * np.cos(t), 0.3 * np.sin(t), color=ORANGE, lw=1.6)
    ax.plot([cx - 1, cx], [0, 2.6], color=ORANGE, lw=1.6)
    ax.plot([cx + 1, cx], [0, 2.6], color=ORANGE, lw=1.6)
    txt(ax, cx, -0.55, "cône\n$V = \\frac{1}{3}\\pi r^2 h$", DARK, 12, ha="center", va="top")
    # cylindre
    cx = 7.4
    ax.plot(cx + 1.0 * np.cos(t), 0.3 * np.sin(t), color=GREEN, lw=1.6)
    ax.plot(cx + 1.0 * np.cos(t), 2.3 + 0.3 * np.sin(t), color=GREEN, lw=1.6)
    ax.plot([cx - 1, cx - 1], [0, 2.3], color=GREEN, lw=1.6)
    ax.plot([cx + 1, cx + 1], [0, 2.3], color=GREEN, lw=1.6)
    txt(ax, cx, -0.55, "cylindre\n$V = \\pi r^2 h$", DARK, 12, ha="center", va="top")
    # boule
    cx = 10.4
    ax.plot(cx + 1.2 * np.cos(t), 1.2 + 1.2 * np.sin(t), color=RED, lw=1.6)
    ax.plot(cx + 1.2 * np.cos(t), 1.2 + 0.35 * np.sin(t), color=RED, lw=1, ls="--")
    txt(ax, cx, -0.55, "boule\n$V = \\frac{4}{3}\\pi r^3$", DARK, 12, ha="center", va="top")
    cadre(ax, (-0.4, 11.9), (-2.0, 2.9))
    _save(fig, I("2nd_geometrie_volumes.png"))


projete()
trigo()
arbre()
volumes()
