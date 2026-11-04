# -*- coding: utf-8 -*-
"""Figures du chapitre 16 (translations, agrandissements et réductions) — 4ème OptiTAB."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fig4e import (new_fig, _save, right_angle, angle_arc, setup_repere, tick_marks,
                   BLUE, ORANGE, GREEN, DARK, NEUTRAL, DIR_COURS, DIR_EXOS)
import numpy as np
from matplotlib.patches import Polygon, Rectangle, Circle

C = lambda f: os.path.join(DIR_COURS, f)  # noqa: E731
X = lambda f: os.path.join(DIR_EXOS, f)   # noqa: E731
P = lambda x, y: np.array([x, y], float)  # noqa: E731
LBLUE, LORANGE, LGREEN, GRILLE = "#d6eafc", "#fdebd0", "#e8f5e9", "#d5d8dc"
GAMMA = [(0, 0), (1, 0), (1, 2), (2, 2), (2, 3), (0, 3)]


def unit(v):
    v = np.array(v, float)
    return v / np.linalg.norm(v)


def point(ax, Pt, nom, d, fs=14, s=26, col=DARK):
    d = unit(d)
    ax.scatter([Pt[0]], [Pt[1]], s=s, zorder=6, color=col)
    ax.annotate(f"${nom}$", (Pt[0], Pt[1]), textcoords="offset points", xytext=(15 * d[0], 15 * d[1]),
                ha="center", va="center", fontsize=fs, color=col, fontweight="bold")


def grille(ax, x0, x1, y0, y1):
    for x in np.arange(x0, x1 + 0.01, 1):
        ax.plot([x, x], [y0, y1], lw=0.7, color=GRILLE, zorder=0)
    for y in np.arange(y0, y1 + 0.01, 1):
        ax.plot([x0, x1], [y, y], lw=0.7, color=GRILLE, zorder=0)


def poly(ax, pts, fc=LBLUE, ec=BLUE, lw=2.2, dec=(0, 0), k=1.0, ls="-", z=2):
    pts = [P(x * k + dec[0], y * k + dec[1]) for x, y in pts]
    ax.add_patch(Polygon(pts, closed=True, facecolor=fc, edgecolor=ec, lw=lw, ls=ls, zorder=z))
    return pts


def fleche(ax, A, B, col=GREEN, lw=2.2, ms=16):
    ax.annotate("", xy=B, xytext=A, arrowprops=dict(arrowstyle="-|>", color=col, lw=lw, mutation_scale=ms,
                                                    shrinkA=0, shrinkB=0), annotation_clip=False)


def cadre(ax, xl, yl):
    ax.set_xlim(*xl)
    ax.set_ylim(*yl)
    ax.set_aspect("equal")
    ax.axis("off")


def txt(ax, x, y, s, col=DARK, fs=12, **kw):
    ax.text(x, y, s, color=col, fontsize=fs, **kw)


# ======================================================================= COURS
def glissement(path):
    fig, ax = new_fig(8.6, 4.6)
    grille(ax, 0, 14, 0, 7)
    A, B, Cc = P(1, 1), P(5, 1), P(2, 4)
    v = P(7, 2)
    poly(ax, [A, B, Cc])
    poly(ax, [A + v, B + v, Cc + v], fc=LORANGE, ec=ORANGE)
    for Q in (A, B, Cc):
        fleche(ax, Q, Q + v)
    for Q, n, d in [(A, "A", (-1, -1)), (B, "B", (1, -1)), (Cc, "C", (-1, 1))]:
        point(ax, Q, n, d)
        point(ax, Q + v, n + "'", d, col="#a04000")
    txt(ax, 7.0, -0.45, "même direction, même sens, même longueur", GREEN, 12, ha="center", va="top",
        fontweight="bold")
    cadre(ax, (-0.3, 14.3), (-1.3, 7.3))
    _save(fig, path)


glissement(C("translations_4e_glissement.png"))


def parallelogramme(path, solution=False, cours=True):
    A, A2, M = P(0, 0), P(5.5, 1.5), P(1.3, 3.2)
    M2 = M + (A2 - A)
    fig, ax = new_fig(6.8, 4.4)
    if cours or solution:
        ax.add_patch(Polygon([A, A2, M2, M], closed=True, facecolor=LGREEN, edgecolor="none", zorder=0))
        ax.plot([A[0], M[0]], [A[1], M[1]], lw=1.6, color=NEUTRAL, ls="--")
        ax.plot([A2[0], M2[0]], [A2[1], M2[1]], lw=1.6, color=NEUTRAL, ls="--")
        fleche(ax, M, M2)
        tick_marks(ax, A, A2, n=2, color=GREEN)
        tick_marks(ax, M, M2, n=2, color=GREEN)
    fleche(ax, A, A2)
    if solution:
        txt(ax, 2.6, 0.25, "5 cm", DARK, 12)
        txt(ax, 3.9, 2.85, "5 cm", GREEN, 12, fontweight="bold")
        txt(ax, 0.05, 1.9, "3 cm", DARK, 12, ha="right")
        txt(ax, 6.35, 3.25, "3 cm", GREEN, 12, fontweight="bold")
    names = ("A", "B", "M", "M'") if not cours else ("A", "A'", "M", "M'")
    for Q, n, d in [(A, names[0], (-1, -0.6)), (A2, names[1], (1, -0.6)), (M, names[2], (-1, 0.6))]:
        point(ax, Q, n, d)
    if cours or solution:
        point(ax, M2, names[3], (1, 0.6), col="#a04000")
    if cours:
        txt(ax, 3.4, -0.9, "$AA'M'M$ est un parallélogramme", GREEN, 13, ha="center", fontweight="bold")
    cadre(ax, (-1.2, 8.0), (-1.3, 5.4))
    _save(fig, path)


parallelogramme(C("translations_4e_parallelogramme.png"))


def agrandissement_cours(path):
    fig, ax = new_fig(8.6, 4.6)
    grille(ax, 0, 15, 0, 8)
    poly(ax, [(1, 1), (5, 1), (1, 4)])
    poly(ax, [(7, 0), (15, 0), (7, 6)], fc=LORANGE, ec=ORANGE)
    for (x, y, s, c) in [(3, 0.45, "4", BLUE), (0.55, 2.5, "3", BLUE), (3.3, 2.75, "5", BLUE),
                         (11, -0.55, "8", ORANGE), (6.5, 3, "6", ORANGE), (11.4, 3.4, "10", ORANGE)]:
        txt(ax, x, y, s, c, 13, ha="center", va="center", fontweight="bold")
    right_angle(ax, P(1, 1), (1, 0), (0, 1), size=0.35)
    right_angle(ax, P(7, 0), (1, 0), (0, 1), size=0.35)
    fleche(ax, P(4.0, 5.0), P(6.2, 5.0), GREEN)
    txt(ax, 5.1, 5.35, "× 2", GREEN, 15, ha="center", fontweight="bold")
    txt(ax, 7.5, 7.2, "longueurs × 2 ; angles conservés", GREEN, 12, ha="center", fontweight="bold")
    cadre(ax, (-0.3, 15.3), (-1.0, 8.0))
    _save(fig, path)


agrandissement_cours(C("translations_4e_agrandissement.png"))


def frise(path, n=6, numeros=False, regle=False, solution=False):
    fig, ax = new_fig(10.0, 2.8)
    for i in range(n):
        dx = 3 * i
        poly(ax, [(0.6, 0.3), (2.4, 0.3), (2.4, 0.9), (1.5, 1.7), (2.4, 2.5), (0.6, 2.5), (1.4, 1.4)],
             fc=LORANGE if i else LBLUE, ec=ORANGE if i else BLUE, dec=(dx, 0))
        ax.add_patch(Circle((dx + 1.0, 1.9), 0.18, color=GREEN, zorder=3))
        if numeros:
            txt(ax, dx + 1.5, -0.35, str(i + 1), DARK, 13, ha="center", va="top", fontweight="bold")
    if regle:
        for x in range(0, 3 * n + 1, 3):
            ax.plot([x, x], [2.85, 3.05], lw=1.2, color=DARK)
            txt(ax, x, 3.15, f"{x}", DARK, 10, ha="center", va="bottom")
        ax.plot([0, 3 * n], [2.95, 2.95], lw=1.2, color=DARK)
        txt(ax, 3 * n + 0.3, 2.95, "cm", DARK, 10, va="center")
    if solution:
        fleche(ax, P(1.5, 2.75), P(4.5, 2.75) + P(0, 0))
        fleche(ax, P(1.5, -0.95), P(10.5, -0.95), ORANGE)
        txt(ax, 6.0, -1.55, "motif 1 → motif 4 : 9 cm vers la droite", ORANGE, 11.5, ha="center", fontweight="bold")
    cadre(ax, (-0.3, 3 * n + 1.2), (-1.9 if solution else -1.0, 3.7))
    _save(fig, path)


frise(C("translations_4e_frise.png"))


# ================================================================== DÉCOUVERTE
def reconnaitre(path):
    fig, ax = new_fig(11.0, 6.0)
    titres = ["figure a", "figure b", "figure c", "figure d"]
    for k in range(4):
        x0, y0 = (k % 2) * 11, (1 - k // 2) * 8.5
        grille(ax, x0, x0 + 10, y0, y0 + 7)
        poly(ax, GAMMA, dec=(x0 + 1, y0 + 2))
        if k == 0:
            poly(ax, GAMMA, fc=LORANGE, ec=ORANGE, dec=(x0 + 6, y0 + 3))
        elif k == 1:
            poly(ax, [(-x, y) for x, y in GAMMA], fc=LORANGE, ec=ORANGE, dec=(x0 + 8, y0 + 2))
            ax.plot([x0 + 5, x0 + 5], [y0, y0 + 7], lw=1.6, color=NEUTRAL, ls="--")
        elif k == 2:
            poly(ax, [(-x, -y) for x, y in GAMMA], fc=LORANGE, ec=ORANGE, dec=(x0 + 8, y0 + 6))
        else:
            poly(ax, GAMMA, fc=LORANGE, ec=ORANGE, dec=(x0 + 4.5, y0 + 0.5), k=2)
        txt(ax, x0 + 5, y0 - 0.35, titres[k], DARK, 13, ha="center", va="top", fontweight="bold")
    txt(ax, 10.5, 16.6, "En bleu : la figure de départ ; en orange : son image", NEUTRAL, 12, ha="center")
    cadre(ax, (-0.3, 21.3), (-1.4, 17.2))
    _save(fig, path)


reconnaitre(X("translations_4e_reconnaitre.png"))


def repere(path, pts, sol_pts=(), fleches=(), xb=(-4, 8), yb=(-4, 8), w=6.4, h=6.4):
    fig, ax = new_fig(w, h)
    setup_repere(ax, xb, yb)
    for (x, y), n, d, col in pts:
        point(ax, P(x, y), n, d, col=col)
    for (x, y), n, d in sol_pts:
        point(ax, P(x, y), n, d, col=GREEN)
    for A, B, col in fleches:
        fleche(ax, P(*A), P(*B), col, lw=1.8, ms=13)
    ax.set_aspect("equal")
    ax.axis("off")
    _save(fig, path)


D2 = [((1, 1), "A", (-1, -0.5), DARK), ((4, 3), "A'", (1, -0.4), "#a04000"), ((2, 4), "B", (-1, 0.4), DARK),
      ((-2, 3), "C", (-1, 0.4), DARK), ((-1, -2), "D", (-1, -0.4), DARK)]
repere(X("translations_4e_repere.png"), D2, fleches=[((1, 1), (4, 3), GREEN)])
repere(X("translations_4e_repere_solution.png"), D2,
       sol_pts=[((5, 6), "B'", (1, 0.4)), ((1, 5), "C'", (1, 0.4)), ((2, 0), "D'", (1, -0.6)),
                ((-2, -1), "E", (-1, -0.4))],
       fleches=[((1, 1), (4, 3), GREEN), ((2, 4), (5, 6), GREEN), ((-2, 3), (1, 5), GREEN),
                ((-1, -2), (2, 0), GREEN), ((-2, -1), (1, 1), GREEN)])


def triangle_grille(path, solution=False):
    fig, ax = new_fig(7.6, 4.6)
    grille(ax, 0, 11, 0, 7)
    A, B, Cc = P(1, 1), P(5, 1), P(2, 4)
    v = P(5, 2)
    poly(ax, [A, B, Cc])
    fleche(ax, A, A + v)
    for Q, n, d in [(A, "A", (-1, -1)), (B, "B", (1, -1)), (Cc, "C", (-1, 1))]:
        point(ax, Q, n, d)
    point(ax, A + v, "A'", (-1, -0.6), col="#a04000")
    if solution:
        poly(ax, [A + v, B + v, Cc + v], fc=LORANGE, ec=ORANGE)
        for Q in (B, Cc):
            fleche(ax, Q, Q + v, lw=1.6, ms=12)
        point(ax, B + v, "B'", (1, -1), col="#a04000")
        point(ax, Cc + v, "C'", (-1, 1), col="#a04000")
    cadre(ax, (-0.3, 11.3), (-0.3, 7.3))
    _save(fig, path)


triangle_grille(X("translations_4e_triangle_grille.png"))
triangle_grille(X("translations_4e_triangle_grille_solution.png"), solution=True)
parallelogramme(X("translations_4e_parallelogramme_d4.png"), cours=False)
parallelogramme(X("translations_4e_parallelogramme_d4_solution.png"), solution=True, cours=False)


def rectangle(path, solution=False):
    fig, ax = new_fig(7.6, 4.2)
    grille(ax, 0, 13, 0, 6)
    poly(ax, [(1, 1), (4, 1), (4, 3), (1, 3)])
    txt(ax, 2.5, 0.45, "3 cm", BLUE, 12, ha="center", va="center", fontweight="bold")
    txt(ax, 0.45, 2, "2 cm", BLUE, 12, ha="center", va="center", rotation=90, fontweight="bold")
    fleche(ax, P(4.5, 2), P(6.0, 2), GREEN)
    txt(ax, 5.25, 2.3, "× 2", GREEN, 14, ha="center", fontweight="bold")
    if solution:
        poly(ax, [(6.5, 1), (12.5, 1), (12.5, 5), (6.5, 5)], fc=LORANGE, ec=ORANGE)
        txt(ax, 9.5, 0.45, "6 cm", ORANGE, 12, ha="center", va="center", fontweight="bold")
        txt(ax, 13.0, 3, "4 cm", ORANGE, 12, ha="center", va="center", rotation=90, fontweight="bold")
        txt(ax, 9.5, 3, "24 carreaux", ORANGE, 12, ha="center", va="center")
        txt(ax, 2.5, 2, "6", BLUE, 12, ha="center", va="center")
    cadre(ax, (-0.3, 13.6), (-0.3, 6.3))
    _save(fig, path)


rectangle(X("translations_4e_rectangle.png"))
rectangle(X("translations_4e_rectangle_solution.png"), solution=True)


def reduction(path, solution=False):
    fig, ax = new_fig(8.0, 3.8)
    s = 0.6
    for dx, k, fc, ec, L in [(0, 1, LBLUE, BLUE, ("8 cm", "6 cm", "10 cm")),
                             (7.5, 0.5, LORANGE, ORANGE, ("4 cm", "3 cm", "5 cm") if solution else ("?", "?", "?"))]:
        T, S, R = P(dx, 0), P(dx + 8 * k * s, 0), P(dx, 6 * k * s)
        ax.add_patch(Polygon([T, S, R], closed=True, facecolor=fc, edgecolor=ec, lw=2.2))
        right_angle(ax, T, (1, 0), (0, 1), size=0.25)
        col = GREEN if (solution and k < 1) else (ORANGE if k < 1 else DARK)
        txt(ax, dx + 4 * k * s, -0.35, L[0], col, 12, ha="center", va="top", fontweight="bold" if k < 1 else "normal")
        txt(ax, dx - 0.2, 3 * k * s, L[1], col, 12, ha="right", va="center", fontweight="bold" if k < 1 else "normal")
        txt(ax, dx + 4 * k * s + 0.25, 3 * k * s + 0.25, L[2], col, 12, ha="left", va="bottom",
            fontweight="bold" if k < 1 else "normal")
        for Q, n, d in [(T, "T", (-1, -1)), (S, "S", (1, -1)), (R, "R", (-1, 1))]:
            point(ax, Q, n + ("'" if k < 1 else ""), d, fs=13)
    fleche(ax, P(5.6, 2.0), P(7.0, 2.0), GREEN)
    txt(ax, 6.3, 2.3, "× 0,5", GREEN, 13, ha="center", fontweight="bold")
    cadre(ax, (-1.3, 11.3), (-1.0, 4.3))
    _save(fig, path)


reduction(X("translations_4e_reduction.png"))
reduction(X("translations_4e_reduction_solution.png"), solution=True)


def vf(path):
    fig, ax = new_fig(9.0, 4.0)
    grille(ax, 0, 17, 0, 7)
    poly(ax, GAMMA, dec=(1, 1))
    poly(ax, GAMMA, fc=LORANGE, ec=ORANGE, dec=(5, 2))
    poly(ax, GAMMA, fc=LGREEN, ec=GREEN, dec=(10, 0.5), k=2)
    fleche(ax, P(1, 1), P(5, 2), ORANGE, lw=1.6, ms=12)
    txt(ax, 2.5, 6.0, "figure ①", BLUE, 12, ha="center", fontweight="bold")
    txt(ax, 6.3, 6.0, "image par\nune translation", ORANGE, 11, ha="center", fontweight="bold")
    txt(ax, 14.5, 6.7, "agrandissement × 2", GREEN, 11, ha="center", fontweight="bold")
    cadre(ax, (-0.3, 17.3), (-0.3, 7.6))
    _save(fig, path)


vf(X("translations_4e_vf.png"))

# ================================================================ ENTRAÎNEMENT
frise(X("translations_4e_frise_e1.png"), n=8, numeros=True, regle=True)
frise(X("translations_4e_frise_e1_solution.png"), n=8, numeros=True, regle=True, solution=True)

E2 = [((-2, 1), "A", (-1, 0.4), DARK), ((3, -1), "B", (1, -0.5), "#a04000"), ((1, 3), "C", (-1, 0.4), DARK)]
repere(X("translations_4e_repere_e2.png"), E2, fleches=[((-2, 1), (3, -1), GREEN)], xb=(-5, 8), yb=(-4, 5),
       w=6.6, h=5.2)
repere(X("translations_4e_repere_e2_solution.png"), E2,
       sol_pts=[((6, 1), "C'", (1, 0.4)), ((5, -2), "O'", (1, -0.5)), ((-4, 3), "D", (-1, 0.4)),
                ((1, 1), "D'", (0.4, 1))],
       fleches=[((-2, 1), (3, -1), GREEN), ((1, 3), (6, 1), GREEN), ((0, 0), (5, -2), GREEN),
                ((-4, 3), (1, 1), GREEN)], xb=(-5, 8), yb=(-4, 5), w=6.6, h=5.2)


def construction(path, solution=False):
    s = 1.0
    E, F, G = P(0, 0), P(4 * s, 0), P(0, 3 * s)
    v = P(5.0, 1.8)
    fig, ax = new_fig(7.4, 4.6)
    ax.add_patch(Polygon([E, F, G], closed=True, facecolor=LBLUE, edgecolor=BLUE, lw=2.2))
    right_angle(ax, E, (1, 0), (0, 1), size=0.3)
    fleche(ax, E, E + v)
    txt(ax, 2, -0.45, "4 cm", DARK, 12, ha="center", va="center")
    txt(ax, -0.45, 1.5, "3 cm", DARK, 12, ha="center", va="center", rotation=90)
    txt(ax, 2.3, 1.75, "5 cm", DARK, 12, ha="center", va="center")
    for Q, n, d in [(E, "E", (-1, -1)), (F, "F", (1, -1)), (G, "G", (-1, 1))]:
        point(ax, Q, n, d)
    point(ax, E + v, "E'", (0.2, -1), col="#a04000")
    if solution:
        ax.add_patch(Polygon([E + v, F + v, G + v], closed=True, facecolor=LORANGE, edgecolor=ORANGE, lw=2.2))
        right_angle(ax, E + v, (1, 0), (0, 1), size=0.3, color=ORANGE)
        for Q in (F, G):
            ax.plot([Q[0], Q[0] + v[0]], [Q[1], Q[1] + v[1]], lw=1.4, color=GREEN, ls="--")
        ax.add_patch(Polygon([F, F + v, G + v, G], closed=True, facecolor=LGREEN, edgecolor="none", zorder=0,
                             alpha=0.7))
        point(ax, F + v, "F'", (1, -1), col="#a04000")
        point(ax, G + v, "G'", (-0.4, 1), col="#a04000")
    cadre(ax, (-1.2, 10.4), (-1.0, 5.4))
    _save(fig, path)


construction(X("translations_4e_construction.png"))
construction(X("translations_4e_construction_solution.png"), solution=True)


def plan_piece(path):
    fig, ax = new_fig(6.6, 5.0)
    ax.add_patch(Rectangle((0, 0), 9, 7, facecolor="#fbfcfc", edgecolor=DARK, lw=4))
    ax.plot([2.0, 3.8], [0, 0], lw=6, color="white")
    ax.add_patch(Polygon([(2.0, 0), (2.0, 1.8), (2.12, 1.8), (2.12, 0)], closed=True, color=NEUTRAL))
    ax.add_patch(matplotlib_arc((2.0, 0), 3.6))
    txt(ax, 2.9, -0.45, "porte : 1,8 cm", DARK, 11, ha="center", va="top")
    txt(ax, 4.5, 7.35, "9 cm", DARK, 13, ha="center", fontweight="bold")
    txt(ax, 9.35, 3.5, "7 cm", DARK, 13, va="center", fontweight="bold")
    txt(ax, 4.5, 3.6, "chambre", NEUTRAL, 14, ha="center", va="center")
    txt(ax, 4.5, 2.8, "plan à l'échelle 1/50", ORANGE, 12, ha="center", va="center", fontweight="bold")
    ax.plot([0, 2], [-1.6, -1.6], lw=3, color=DARK)
    txt(ax, 2.3, -1.6, "1 cm sur le plan = 50 cm en réalité", DARK, 10.5, va="center")
    cadre(ax, (-0.6, 10.6), (-2.1, 8.0))
    _save(fig, path)


def matplotlib_arc(c, d):
    from matplotlib.patches import Arc
    return Arc(c, d, d, theta1=0, theta2=90, lw=1.2, color=NEUTRAL, ls="--")


plan_piece(X("translations_4e_plan_piece.png"))


def photos(path, solution=False):
    fig, ax = new_fig(6.4, 6.4)
    s = 0.3
    for (w_, h_), col, nom in [((20, 30), GREEN, "20 × 30"), ((13, 18), ORANGE, "13 × 18"), ((10, 15), BLUE, "10 × 15")]:
        ax.add_patch(Rectangle((0, 0), w_ * s, h_ * s, facecolor="none", edgecolor=col, lw=2.4))
        txt(ax, 0.12, h_ * s - 0.15, nom, col, 11.5, ha="left", va="top", fontweight="bold")
    if solution:
        ax.plot([0, 20 * s], [0, 30 * s], lw=1.6, color=GREEN, ls="--")
        ax.plot([0, 13 * s], [0, 18 * s], lw=1.4, color=ORANGE, ls=":")
        txt(ax, 3.0, -0.95, "- - - même diagonale : 20 × 30 agrandit 10 × 15", GREEN, 10.5, ha="center", va="top",
            fontweight="bold")
    txt(ax, 3.0, -0.4, "dimensions en cm", NEUTRAL, 10.5, ha="center", va="top")
    cadre(ax, (-0.4, 6.6), (-1.6, 9.4))
    _save(fig, path)


photos(X("translations_4e_photos.png"))
photos(X("translations_4e_photos_solution.png"), solution=True)


def voiture(ax, x0, y0, L, col, fc):
    k = L / 10
    corps = [(0, 0.5), (10, 0.5), (10, 1.9), (8.6, 2.2), (7, 3.4), (3.2, 3.4), (2, 2.3), (0, 2.0)]
    ax.add_patch(Polygon([(x0 + x * k, y0 + y * k) for x, y in corps], closed=True, facecolor=fc, edgecolor=col,
                         lw=2))
    for xr in (2.3, 7.7):
        ax.add_patch(Circle((x0 + xr * k, y0 + 0.6 * k), 0.75 * k, facecolor="#566573", edgecolor=DARK))


def maquette(path):
    fig, ax = new_fig(9.0, 3.4)
    voiture(ax, 0, 0, 10, BLUE, LBLUE)
    voiture(ax, 12.5, 0, 3.2, ORANGE, LORANGE)
    ax.annotate("", xy=(10, -0.6), xytext=(0, -0.6), arrowprops=dict(arrowstyle="<->", color=DARK))
    txt(ax, 5, -0.8, "voiture réelle : 4,30 m", DARK, 12, ha="center", va="top")
    ax.annotate("", xy=(15.7, -0.6), xytext=(12.5, -0.6), arrowprops=dict(arrowstyle="<->", color=DARK))
    txt(ax, 14.1, -0.8, "maquette 1/43", ORANGE, 12, ha="center", va="top", fontweight="bold")
    cadre(ax, (-0.4, 16.5), (-1.8, 3.8))
    _save(fig, path)


maquette(X("translations_4e_maquette.png"))


def triangle_angles(path, solution=False):
    from math import acos, degrees, sqrt
    fig, ax = new_fig(8.6, 4.4)
    s = 0.55
    xa = (16 - 25 + 36) / 12
    ya = sqrt(16 - xa * xa)
    for dx, k, fc, ec, labs in [(0, 1, LBLUE, BLUE, ("4 cm", "6 cm", "5 cm")),
                                (5.0, 1.5, LORANGE, ORANGE, ("6 cm", "9 cm", "7,5 cm") if solution else ("?", "?", "?"))]:
        B = P(dx, 0)
        Cc = P(dx + 6 * k * s, 0)
        A = P(dx + xa * k * s, ya * k * s)
        ax.add_patch(Polygon([A, B, Cc], closed=True, facecolor=fc, edgecolor=ec, lw=2.2))
        lab = "≈ 56°" if (k == 1 or solution) else "?"
        angle_arc(ax, B, Cc - B, A - B, r=0.55, color=GREEN if (k > 1 and solution) else ORANGE, lw=2,
                  label=lab, label_r=1.15, fs=11.5)
        col = GREEN if (k > 1 and solution) else (ORANGE if k > 1 else DARK)
        mid = lambda U, V: (U + V) / 2  # noqa: E731
        for (U, V), L, off in [((A, B), labs[0], P(-0.55, 0.1)), ((B, Cc), labs[1], P(0, -0.4)),
                               ((A, Cc), labs[2], P(0.6, 0.2))]:
            m = mid(U, V) + off
            txt(ax, m[0], m[1], L, col, 12, ha="center", va="center")
        prime = "'" if k > 1 else ""
        for Q, n, d in [(A, "A", (0, 1)), (B, "B", (-1, -0.6)), (Cc, "C", (1, -0.6))]:
            point(ax, Q, n + prime, d, fs=13)
    txt(ax, 4.3, 3.6, "× 1,5", GREEN, 14, ha="center", fontweight="bold")
    fleche(ax, P(3.6, 3.3), P(5.0, 3.3), GREEN)
    cadre(ax, (-1.0, 13.8), (-1.0, 5.0))
    _save(fig, path)


triangle_angles(X("translations_4e_triangle_angles.png"))
triangle_angles(X("translations_4e_triangle_angles_solution.png"), solution=True)


# =================================================================== PROBLÈMES
def pavage(path, solution=False):
    fig, ax = new_fig(8.0, 5.2)
    grille(ax, 0, 17, 0, 9)
    tuile = [(0, 0), (3, 0), (4, 2), (1, 2)]
    numero = {(0, 0): "1", (1, 0): "2", (0, 1): "3", (1, 1): "4"}
    for j in range(4):
        for i in range(4):
            dec = (3 * i + j, 2 * j + 0.5)
            first = (i, j) == (0, 0)
            poly(ax, tuile, fc=LBLUE if first else LORANGE, ec=BLUE if first else ORANGE, dec=dec, lw=1.8)
            if (i, j) in numero:
                txt(ax, dec[0] + 2.6, dec[1] + 1.35, numero[(i, j)], DARK, 14, ha="center", va="center", fontweight="bold")
    if solution:
        c1 = P(2.0, 1.1)
        fleche(ax, c1, c1 + P(3, 0))
        fleche(ax, c1, c1 + P(1, 2), "#8e44ad")
        fleche(ax, c1, c1 + P(4, 2), ORANGE)
    cadre(ax, (-0.3, 17.3), (-0.3, 9.3))
    _save(fig, path)


pavage(X("translations_4e_pavage.png"))
pavage(X("translations_4e_pavage_solution.png"), solution=True)

R2 = [((1, 1), "R", (-1, -0.5), DARK)]
repere(X("translations_4e_robot.png"), R2, fleches=[], xb=(-2, 9), yb=(-3, 6), w=6.6, h=5.4)
repere(X("translations_4e_robot_solution.png"), R2,
       sol_pts=[((4, 3), "R_1", (-0.6, 1)), ((6, -1), "R_2", (1, -0.4))],
       fleches=[((1, 1), (4, 3), BLUE), ((4, 3), (6, -1), ORANGE), ((1, 1), (6, -1), GREEN)],
       xb=(-2, 9), yb=(-3, 6), w=6.6, h=5.4)

LOGO = [(0, 0), (4, 0), (4, 2), (2, 2), (2, 4), (0, 4)]


def logo(path, solution=False):
    fig, ax = new_fig(8.0, 4.6)
    grille(ax, 0, 15, 0, 8)
    poly(ax, LOGO, dec=(1, 1))
    for (x, y, s) in [(3, 0.55, "4"), (5.45, 2, "2"), (4, 3.45, "2"), (2.55, 4, "2"), (2, 5.45, "2"), (0.55, 3, "4")]:
        txt(ax, x, y, s, BLUE, 12, ha="center", va="center", fontweight="bold")
    fleche(ax, P(5.6, 6.3), P(7.6, 6.3), GREEN)
    txt(ax, 6.6, 6.65, "× 1,5", GREEN, 13, ha="center", fontweight="bold")
    if solution:
        poly(ax, LOGO, fc=LORANGE, ec=ORANGE, dec=(8, 1), k=1.5)
        for (x, y, s) in [(11, 0.55, "6"), (14.45, 2.5, "3"), (12.5, 4.45, "3"), (11.45, 5.5, "3"),
                          (9.5, 7.45, "3"), (7.55, 4, "6")]:
            txt(ax, x, y, s, ORANGE, 12, ha="center", va="center", fontweight="bold")
        txt(ax, 3, 2, "12", BLUE, 13, ha="center", va="center")
        txt(ax, 10.5, 3, "27", ORANGE, 14, ha="center", va="center", fontweight="bold")
    cadre(ax, (-0.3, 15.3), (-0.3, 8.3))
    _save(fig, path)


logo(X("translations_4e_logo.png"))
logo(X("translations_4e_logo_solution.png"), solution=True)


def jardin(path):
    fig, ax = new_fig(7.6, 4.8)
    ax.add_patch(Rectangle((0, 0), 15, 8, facecolor="#d5f5e3", edgecolor="#1e8449", lw=2.5))
    ax.add_patch(Circle((11, 5), 1, facecolor="#aed6f1", edgecolor="#2874a6", lw=1.8))
    txt(ax, 11, 5, "bassin", "#21618c", 10, ha="center", va="center")
    ax.annotate("", xy=(12, 3.6), xytext=(10, 3.6), arrowprops=dict(arrowstyle="<->", color=DARK))
    txt(ax, 11, 3.35, "2 cm", DARK, 11, ha="center", va="top")
    txt(ax, 7.5, -0.4, "15 cm", DARK, 13, ha="center", va="top", fontweight="bold")
    txt(ax, -0.35, 4, "8 cm", DARK, 13, ha="right", va="center", fontweight="bold")
    txt(ax, 5, 4, "pelouse", "#1e8449", 14, ha="center", va="center")
    txt(ax, 7.5, 8.35, "plan du jardin — échelle 1/200", ORANGE, 12.5, ha="center", fontweight="bold")
    cadre(ax, (-2.0, 15.5), (-1.3, 9.2))
    _save(fig, path)


jardin(X("translations_4e_jardin.png"))


def tour(ax, x0, h, col, fc):
    b = h * 0.38
    pts = [(x0 - b / 2, 0), (x0 - b * 0.12, h * 0.32), (x0 - b * 0.05, h * 0.9), (x0, h), (x0 + b * 0.05, h * 0.9),
           (x0 + b * 0.12, h * 0.32), (x0 + b / 2, 0), (x0 + b * 0.22, 0), (x0, h * 0.2), (x0 - b * 0.22, 0)]
    ax.add_patch(Polygon(pts, closed=True, facecolor=fc, edgecolor=col, lw=2))
    for t in (0.18, 0.36, 0.62):
        w_ = b / 2 * (1 - t) * (0.95 if t > 0.3 else 1)
        ax.plot([x0 - w_ * (0.5 if t > 0.3 else 1), x0 + w_ * (0.5 if t > 0.3 else 1)], [h * t, h * t], lw=1.6,
                color=col)


def tours(path):
    fig, ax = new_fig(7.0, 4.6)
    tour(ax, 2.5, 6.6, "#784212", "#f0b27a")
    tour(ax, 7.5, 0.66 * 3, ORANGE, LORANGE)
    ax.annotate("", xy=(5.0, 6.6), xytext=(5.0, 0), arrowprops=dict(arrowstyle="<->", color=DARK))
    txt(ax, 5.15, 3.3, "330 m", DARK, 12, va="center", fontweight="bold")
    ax.plot([-0.3, 9.6], [0, 0], lw=2, color=NEUTRAL)
    txt(ax, 2.5, -0.35, "la tour réelle", "#784212", 11.5, ha="center", va="top", fontweight="bold")
    txt(ax, 7.5, -0.35, "maquette", ORANGE, 11.5, ha="center", va="top", fontweight="bold")
    cadre(ax, (-0.4, 9.8), (-1.0, 7.2))
    _save(fig, path)


tours(X("translations_4e_tour.png"))


def formats(path, solution=False):
    s = 0.17
    fig, ax = new_fig(5.4, 7.2)
    for (w_, h_), col, nom in [((29.7, 42), GREEN, "A3"), ((21, 29.7), BLUE, "A4"), ((14.85, 21), ORANGE, "A5")]:
        ax.add_patch(Rectangle((0, 0), w_ * s, h_ * s, facecolor="none", edgecolor=col, lw=2.4))
        txt(ax, 0.12, h_ * s - 0.12, nom, col, 13, ha="left", va="top", fontweight="bold")
    if solution:
        ax.plot([0, 29.7 * s], [0, 42 * s], lw=1.6, color=DARK, ls="--")
        txt(ax, 29.7 * s / 2, -0.3, "- - - les trois diagonales sont alignées", DARK, 10.5, ha="center", va="top")
    cadre(ax, (-0.4, 29.7 * s + 0.4), (-1.0, 42 * s + 0.4))
    _save(fig, path)


formats(X("translations_4e_formats.png"))
formats(X("translations_4e_formats_solution.png"), solution=True)


def ombre_chinoise(path, solution=False):
    s = 0.035
    L = P(0, 0)
    A, B = P(50 * s, 0), P(50 * s, 10 * s * 1.0)
    A2, B2 = P(200 * s, 0), P(200 * s, 40 * s)
    fig, ax = new_fig(8.4, 3.6)
    ax.plot([-0.4, A2[0] + 0.6], [0, 0], lw=1.5, color=NEUTRAL)
    ax.add_patch(Rectangle((A2[0], -0.2), 0.15, 1.9, facecolor="#f2f3f4", edgecolor=NEUTRAL))
    txt(ax, A2[0] + 0.3, 1.6, "écran", NEUTRAL, 10.5)
    ax.add_patch(Circle(L, 0.14, facecolor="#f4d03f", edgecolor="#b7950b", zorder=5))
    txt(ax, -0.15, 0.25, "lampe", "#b7950b", 10.5, ha="right")
    ax.plot([L[0], B2[0]], [L[1], B2[1]], lw=1.3, color="#f39c12", ls="--")
    ax.plot([A[0], B[0]], [A[1], B[1]], lw=4, color=BLUE, solid_capstyle="round")
    ax.plot([A2[0], B2[0]], [A2[1], B2[1]], lw=5, color="#2c3e50", solid_capstyle="round")
    for x1, x2, y, t in [(0, A[0], -0.35, "50 cm"), (0, A2[0], -0.75, "200 cm")]:
        ax.annotate("", xy=(x2, y), xytext=(x1, y), arrowprops=dict(arrowstyle="<->", color=DARK))
        txt(ax, (x1 + x2) / 2, y - 0.08, t, DARK, 11, ha="center", va="top")
    txt(ax, A[0] + 0.12, B[1] / 2, "10 cm", BLUE, 11, va="center", fontweight="bold")
    txt(ax, A2[0] - 0.12, B2[1] / 2, "40 cm" if solution else "?", GREEN if solution else ORANGE, 12,
        ha="right", va="center", fontweight="bold")
    for Q, n, d in [(L, "L", (-0.3, -1)), (A, "A", (0.6, -1)), (B, "B", (-0.6, 1)), (A2, "A'", (-0.8, -1)),
                    (B2, "B'", (-0.8, 1))]:
        point(ax, Q, n, d, fs=12.5, s=18)
    cadre(ax, (-1.4, A2[0] + 1.2), (-1.4, B2[1] + 0.5))
    _save(fig, path)


ombre_chinoise(X("translations_4e_ombre_chinoise.png"))
ombre_chinoise(X("translations_4e_ombre_chinoise_solution.png"), solution=True)
