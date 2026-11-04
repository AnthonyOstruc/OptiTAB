# -*- coding: utf-8 -*-
"""Figures du chapitre 18 (Raisonner et démontrer) — 3ème OptiTAB."""
import os
import sys
from math import cos, sin, radians, sqrt

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mp

from fig3e import (new_fig, seg_label, right_angle, dot_label, _proj, BLUE, ORANGE, GREEN,
                   DARK, NEUTRAL, DIR_COURS, DIR_EXOS, ROOT)
import figures_ch16 as f16

LIGHT = "#d6eafc"
LORANGE = "#fdebd0"


def save(fig, ax, path, xlim=None, ylim=None, equal=True):
    if xlim:
        ax.set_xlim(*xlim)
    if ylim:
        ax.set_ylim(*ylim)
    if equal:
        ax.set_aspect("equal")
    ax.axis("off")
    fig.savefig(path, dpi=175, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print("OK", os.path.relpath(path, ROOT))


def P(name, xy, dx, dy, ax, color=DARK):
    dot_label(ax, xy, f"${name}$", dx, dy, color=color, s=34)


def tri(ax, pts, color=BLUE, face=LIGHT):
    ax.add_patch(mp.Polygon(pts, closed=True, facecolor=face, edgecolor=color, lw=2.2,
                            zorder=2))


# ---------------------------------------------------------------- cours

def demarche():
    fig, ax = new_fig(11.5, 3.5)
    boites = [("Données\n(hypothèses)", "Dans le triangle ABC,\n$BC^2 = AB^2 + AC^2$", BLUE,
               "#e8f4fd"),
              ("Propriété\n(théorème)", "D'après la réciproque\ndu théorème de Pythagore",
               ORANGE, "#fff4e6"),
              ("Conclusion", "le triangle ABC est\nrectangle en A", GREEN, "#e8f5e9")]
    for i, (titre, ex, col, bg) in enumerate(boites):
        x = i * 4.0
        ax.add_patch(mp.FancyBboxPatch((x, 0), 3.4, 2.3, boxstyle="round,pad=0.05,rounding_size=0.18",
                                       facecolor=bg, edgecolor=col, lw=2.2))
        ax.text(x + 1.7, 1.72, titre, ha="center", va="center", fontsize=16, color=col,
                fontweight="bold", linespacing=1.2)
        ax.text(x + 1.7, 0.62, ex, ha="center", va="center", fontsize=13, color=DARK,
                linespacing=1.35)
        if i < 2:
            ax.annotate("", xy=(x + 3.95, 1.15), xytext=(x + 3.48, 1.15),
                        arrowprops=dict(arrowstyle="-|>", lw=2.2, color=DARK))
    save(fig, ax, os.path.join(DIR_COURS, "raisonner_3e_demarche.png"), (-0.2, 11.6),
         (-0.25, 2.55))


def contre_exemple():
    fig, ax = plt.subplots(figsize=(6.4, 4.6))
    fig.patch.set_facecolor("white")
    x = np.linspace(-0.4, 1.5, 300)
    ax.axvspan(0, 1, color="#fff4e6", zorder=0)
    ax.plot(x, x ** 2, color=BLUE, lw=2.6, label="$y = x^2$")
    ax.plot(x, x, color=ORANGE, lw=2.6, label="$y = x$")
    ax.plot([0.5, 0.5], [0, 0.5], color=NEUTRAL, lw=1.0, ls=":")
    ax.scatter([0.5, 0.5], [0.25, 0.5], color=[BLUE, ORANGE], s=40, zorder=5)
    ax.annotate("$0{,}5^2 = 0{,}25$", (0.5, 0.25), textcoords="offset points", xytext=(10, -16),
                fontsize=11.5, color=BLUE, fontweight="bold")
    ax.annotate("$0{,}5$", (0.5, 0.5), textcoords="offset points", xytext=(-36, 6),
                fontsize=11.5, color=ORANGE, fontweight="bold")
    ax.text(0.5, 1.75, "pour $0 < x < 1$ :  $x^2 < x$", ha="center", fontsize=12, color=DARK,
            fontweight="bold")
    ax.axhline(0, color="#9aa5b1", lw=1)
    ax.axvline(0, color="#9aa5b1", lw=1)
    ax.set_xlim(-0.4, 1.5)
    ax.set_ylim(-0.3, 2.0)
    ax.grid(True, color="#e3e8ee", lw=0.8)
    ax.legend(loc="upper left", fontsize=11, frameon=False)
    ax.tick_params(labelsize=9.5, colors="#5d6d7e")
    for s in ax.spines.values():
        s.set_visible(False)
    fig.savefig(os.path.join(DIR_COURS, "raisonner_3e_contre_exemple.png"), dpi=175,
                bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print("OK raisonner_3e_contre_exemple.png")


# ---------------------------------------------------------------- exercices

def deux_triangles():
    fig, ax = new_fig(9.4, 4.2)
    s = 0.8
    A, B, C = (0, 0), (4 * s, 0), (0, 3 * s)
    tri(ax, [A, B, C])
    right_angle(ax, A, (1, 0), (0, 1), size=0.25)
    seg_label(ax, A, B, "4 cm", side=-1, offset=0.3)
    seg_label(ax, A, C, "3 cm", side=1, offset=0.42)
    seg_label(ax, B, C, "5 cm", side=-1, offset=-0.38, color=GREEN)
    ax.text(1.6, -1.0, "angle droit : 3 ; 4 ; 5", ha="center", fontsize=12, color=DARK,
            fontweight="bold")
    # triangle 3 ; 4 ; 6 : côtés 4 (base) et 3, troisième côté 6
    ox = 6.4
    a, b, c = 4 * s, 3 * s, 6 * s
    cosA = (a * a + b * b - c * c) / (2 * a * b)
    ang = np.arccos(cosA)
    A2, B2 = (ox, 0), (ox + a, 0)
    C2 = (ox + b * cos(ang), b * sin(ang))
    tri(ax, [A2, B2, C2], face=LORANGE, color=ORANGE)
    seg_label(ax, A2, B2, "4 cm", side=-1, offset=0.3)
    seg_label(ax, A2, C2, "3 cm", side=1, offset=0.35)
    seg_label(ax, B2, C2, "6 cm", side=-1, offset=-0.36, color=ORANGE)
    ax.text(ox + 1.0, -1.0, "pas d'angle droit : 3 ; 4 ; 6", ha="center", fontsize=12,
            color=DARK, fontweight="bold")
    save(fig, ax, os.path.join(DIR_EXOS, "raisonner_3e_triangles.png"), (-1.4, 10.0),
         (-1.4, 3.2))


def triangle_pythagore():
    fig, ax = new_fig(6.4, 5.0)
    s = 0.62
    A, B, C = (0, 0), (0, 4.8 * s), (6.4 * s, 0)
    tri(ax, [A, B, C])
    P("A", A, -16, -14, ax)
    P("B", B, -16, 4, ax)
    P("C", C, 6, -14, ax)
    seg_label(ax, A, B, "4,8 cm", side=1, offset=0.55)
    seg_label(ax, A, C, "6,4 cm", side=-1, offset=0.32)
    seg_label(ax, B, C, "8 cm", side=-1, offset=-0.4)
    save(fig, ax, os.path.join(DIR_EXOS, "raisonner_3e_pythagore.png"), (-1.3, 4.8),
         (-0.9, 3.6))


def thales():
    fig, ax = new_fig(6.2, 5.0)
    A = np.array([0.0, 0.0])
    B = A + 4.5 * np.array([cos(radians(-112)), sin(radians(-112))])
    C = A + 6.0 * np.array([cos(radians(-52)), sin(radians(-52))])
    M, N = A + 0.4 * (B - A), A + 0.4 * (C - A)
    for Q1, Q2 in [(A, B), (A, C), (B, C)]:
        ax.plot([Q1[0], Q2[0]], [Q1[1], Q2[1]], lw=2.2, color=BLUE)
    ax.plot([M[0], N[0]], [M[1], N[1]], lw=2.2, color=ORANGE)
    P("A", A, -4, 8, ax)
    P("B", B, -16, -12, ax)
    P("C", C, 6, -12, ax)
    P("M", M, -18, 0, ax, ORANGE)
    P("N", N, 8, 0, ax, ORANGE)
    save(fig, ax, os.path.join(DIR_EXOS, "raisonner_3e_thales.png"), (-2.6, 4.4), (-5.4, 0.8))


def bassin():
    fig, ax = new_fig(6.8, 4.4)
    s = 1.0
    L, Pp, H, eau = 4 * s, 2.5 * s, 0.8 * s * 1.6, 0.6 * s * 1.6
    W = [_proj(x, y, z) for x, y, z in [(0, 0, 0), (L, 0, 0), (L, 0, eau), (0, 0, eau)]]
    ax.add_patch(mp.Polygon(W, closed=True, facecolor="#cfe8fb", edgecolor="none", zorder=1))
    T = [_proj(x, y, eau) for x, y in [(0, 0), (L, 0), (L, Pp), (0, Pp)]]
    ax.add_patch(mp.Polygon(T, closed=True, facecolor="#9fd0f5", edgecolor=BLUE, lw=1.0,
                            alpha=0.8, zorder=1))
    R = [_proj(L, y, z) for y, z in [(0, 0), (Pp, 0), (Pp, eau), (0, eau)]]
    ax.add_patch(mp.Polygon(R, closed=True, facecolor="#b8dcf8", edgecolor="none", zorder=1))
    V = f16.box(ax, L, Pp, H)
    seg_label(ax, V["A"], V["B"], "4 m", side=-1, offset=0.3)
    seg_label(ax, V["B"], V["F"], "2,5 m", side=-1, offset=0.42)
    seg_label(ax, V["F"], V["G"], "0,8 m", side=-1, offset=0.5)
    save(fig, ax, os.path.join(DIR_EXOS, "raisonner_3e_bassin.png"), (-0.6, 6.0), (-0.6, 2.6))


def rectangle_aire():
    fig, axes = plt.subplots(1, 2, figsize=(9.6, 4.0), gridspec_kw=dict(width_ratios=[1, 1.45]))
    fig.patch.set_facecolor("white")
    ax = axes[0]
    ax.add_patch(mp.Rectangle((0, 0), 4.2, 2.6, facecolor=LIGHT, edgecolor=BLUE, lw=2.2))
    ax.text(2.1, -0.4, "$x$", ha="center", va="center", fontsize=17, color=ORANGE,
            fontweight="bold")
    ax.text(4.4, 1.3, "$20 - x$", ha="left", va="center", fontsize=17, color=ORANGE,
            fontweight="bold")
    ax.text(2.1, 1.3, "périmètre\n40 cm", ha="center", va="center", fontsize=15, color=DARK)
    ax.set_xlim(-0.2, 6.3)
    ax.set_ylim(-0.8, 2.9)
    ax.set_aspect("equal")
    ax.axis("off")
    ax = axes[1]
    x = np.linspace(0, 20, 300)
    ax.plot(x, x * (20 - x), color=BLUE, lw=2.6)
    ax.plot([10, 10], [0, 100], color=GREEN, ls=":", lw=1.4)
    ax.plot([0, 10], [100, 100], color=GREEN, ls=":", lw=1.4)
    ax.scatter([10], [100], color=GREEN, s=45, zorder=5)
    ax.annotate("maximum (10 ; 100)", (10, 100), textcoords="offset points", xytext=(8, 8),
                fontsize=13, color=GREEN, fontweight="bold")
    ax.set_xlim(0, 21)
    ax.set_ylim(0, 120)
    ax.set_xticks(range(0, 21, 4))
    ax.set_yticks(range(0, 111, 20))
    ax.set_xlabel("$x$ (cm)", fontsize=13, color=DARK)
    ax.set_ylabel("aire (cm²)", fontsize=13, color=DARK)
    ax.grid(True, color="#e3e8ee", lw=0.8)
    ax.tick_params(labelsize=12, colors="#5d6d7e")
    for sp in ["top", "right"]:
        ax.spines[sp].set_visible(False)
    fig.tight_layout()
    fig.savefig(os.path.join(DIR_EXOS, "raisonner_3e_aire_max.png"), dpi=175,
                bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print("OK raisonner_3e_aire_max.png")


def angle_mark(ax, Ppt, Q1, Q2, r, color, n=1, label=None, lr=None, fs=11.5):
    a1 = np.degrees(np.arctan2(Q1[1] - Ppt[1], Q1[0] - Ppt[0]))
    a2 = np.degrees(np.arctan2(Q2[1] - Ppt[1], Q2[0] - Ppt[0]))
    lo, hi = sorted([a1, a2])
    if hi - lo > 180:
        lo, hi = hi, lo + 360
    for k in range(n):
        ax.add_patch(mp.Arc(Ppt, 2 * (r + 0.09 * k), 2 * (r + 0.09 * k), theta1=lo, theta2=hi,
                            color=color, lw=1.8, zorder=4))
    if label:
        m = radians((lo + hi) / 2)
        rr = lr or r + 0.3
        ax.text(Ppt[0] + rr * cos(m), Ppt[1] + rr * sin(m), label, ha="center", va="center",
                fontsize=fs, color=color, fontweight="bold")


def triangle_or():
    fig, ax = new_fig(5.4, 6.0)
    AB = 5.0
    B = np.array([-AB * sin(radians(18)), 0.0])
    C = np.array([AB * sin(radians(18)), 0.0])
    A = np.array([0.0, AB * cos(radians(18))])
    k = (C[0] - B[0]) / AB
    D = A + k * (C - A)
    tri(ax, [A, B, C])
    ax.plot([B[0], D[0]], [B[1], D[1]], lw=2.0, color=ORANGE, ls="--")
    angle_mark(ax, A, B, C, 0.7, ORANGE, label="36°", lr=1.05)
    for Q1, Q2 in [(A, D), (D, C)]:
        angle_mark(ax, B, Q1, Q2, 0.7, GREEN, n=2)
        a1 = np.arctan2(Q1[1] - B[1], Q1[0] - B[0])
        a2 = np.arctan2(Q2[1] - B[1], Q2[0] - B[0])
        m = (a1 + a2) / 2
        ax.plot([B[0] + 0.62 * cos(m), B[0] + 0.98 * cos(m)],
                [B[1] + 0.62 * sin(m), B[1] + 0.98 * sin(m)], color=GREEN, lw=1.8)
    P("A", A, -5, 8, ax)
    P("B", B, -16, -12, ax)
    P("C", C, 6, -12, ax)
    P("D", D, 8, 0, ax, ORANGE)
    save(fig, ax, os.path.join(DIR_EXOS, "raisonner_3e_triangle_or.png"), (-2.6, 2.6),
         (-0.6, 5.4))


def poignees():
    fig, ax = new_fig(5.0, 5.0)
    noms = "ABCDE"
    pts = [(2 * cos(radians(90 + 72 * i)), 2 * sin(radians(90 + 72 * i))) for i in range(5)]
    for i in range(5):
        for j in range(i + 1, 5):
            ax.plot([pts[i][0], pts[j][0]], [pts[i][1], pts[j][1]], lw=1.8, color=BLUE,
                    zorder=1)
    for (x, y), n in zip(pts, noms):
        ax.add_patch(mp.Circle((x, y), 0.28, facecolor=ORANGE, edgecolor="#a04000", lw=1.4,
                               zorder=3))
        ax.text(x, y, n, ha="center", va="center", fontsize=13, color="white",
                fontweight="bold", zorder=4)
    save(fig, ax, os.path.join(DIR_EXOS, "raisonner_3e_poignees.png"), (-2.6, 2.6), (-2.3, 2.6))


def preuve_pythagore():
    fig, ax = new_fig(5.6, 5.6)
    a, b = 3.0, 4.0
    n = a + b
    ax.add_patch(mp.Rectangle((0, 0), n, n, facecolor="none", edgecolor=DARK, lw=2.2))
    Q = [(a, 0), (n, a), (b, n), (0, b)]
    ax.add_patch(mp.Polygon(Q, closed=True, facecolor=LORANGE, edgecolor=ORANGE, lw=2.2))
    for T in [[(0, 0), (a, 0), (0, b)], [(a, 0), (n, 0), (n, a)], [(n, a), (n, n), (b, n)],
              [(b, n), (0, n), (0, b)]]:
        ax.add_patch(mp.Polygon(T, closed=True, facecolor=LIGHT, edgecolor=BLUE, lw=1.8))
    txt = dict(ha="center", va="center", fontsize=14, fontweight="bold")
    ax.text(a / 2, -0.35, "$a$", color=BLUE, **txt)
    ax.text(a + b / 2, -0.35, "$b$", color=BLUE, **txt)
    ax.text(n + 0.35, a / 2, "$a$", color=BLUE, **txt)
    ax.text(n + 0.35, a + b / 2, "$b$", color=BLUE, **txt)
    ax.text(n - a / 2, n + 0.35, "$a$", color=BLUE, **txt)
    ax.text(b / 2, n + 0.35, "$b$", color=BLUE, **txt)
    ax.text(-0.35, b + a / 2, "$a$", color=BLUE, **txt)
    ax.text(-0.35, b / 2, "$b$", color=BLUE, **txt)
    for (x1, y1), (x2, y2) in zip(Q, Q[1:] + Q[:1]):
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        cx, cy = n / 2, n / 2
        ax.text(mx + 0.32 * (cx - mx) / 1.7, my + 0.32 * (cy - my) / 1.7, "$c$", color=ORANGE,
                **txt)
    save(fig, ax, os.path.join(DIR_EXOS, "raisonner_3e_preuve_pythagore.png"), (-0.8, n + 0.8),
         (-0.8, n + 0.8))


if __name__ == "__main__":
    demarche()
    contre_exemple()
    deux_triangles()
    triangle_pythagore()
    thales()
    bassin()
    rectangle_aire()
    triangle_or()
    poignees()
    preuve_pythagore()
    print("Figures chapitre 18 : OK")
