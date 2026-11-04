# -*- coding: utf-8 -*-
"""Figures du chapitre 6 (équations) — 4ème OptiTAB."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fig4e import (new_fig, _save, draw_schema, dot_label, seg_label, angle_arc, BLUE, ORANGE,
                   GREEN, DARK, NEUTRAL, DIR_COURS, DIR_EXOS)
import numpy as np
from matplotlib.patches import Rectangle, Circle, Polygon, FancyBboxPatch, FancyArrowPatch

C = lambda f: os.path.join(DIR_COURS, f)  # noqa: E731
X = lambda f: os.path.join(DIR_EXOS, f)   # noqa: E731
LBLUE, LORANGE, LGREEN, LPURP = "#d6eafc", "#fdebd0", "#e8f5e9", "#efe3f5"


def plateau(ax, cx, boites, billes, y=1.25):
    """Plateau centré en cx : boîtes « x » puis billes, rangées par lignes de 5."""
    ax.plot([cx - 1.75, cx + 1.75], [y, y], lw=3.2, color=DARK, solid_capstyle="round")
    items = ["b"] * boites + ["o"] * billes
    per_row = 5
    for i, kind in enumerate(items):
        r, c = divmod(i, per_row)
        n_row = min(per_row, len(items) - r * per_row)
        x = cx - (n_row - 1) * 0.33 + c * 0.66
        yy = y + 0.06 + r * 0.62
        if kind == "b":
            ax.add_patch(Rectangle((x - 0.28, yy), 0.56, 0.56, facecolor=LORANGE, edgecolor=ORANGE,
                                   lw=1.6))
            ax.text(x, yy + 0.28, "$x$", ha="center", va="center", fontsize=12, color=ORANGE)
        else:
            ax.add_patch(Circle((x, yy + 0.27), 0.26, facecolor=LBLUE, edgecolor=BLUE, lw=1.3))


def balance(ax, x0, gauche, droite, titre=None):
    ax.add_patch(Polygon([(x0 + 4.1, 0), (x0 + 4.9, 0), (x0 + 4.5, 1.0)], closed=True,
                         facecolor="#cfd8dc", edgecolor=DARK, lw=1.4))
    ax.plot([x0 + 0.3, x0 + 8.7], [1.0, 1.0], lw=3.2, color=DARK, solid_capstyle="round")
    for cx in (x0 + 2.0, x0 + 7.0):
        ax.plot([cx, cx], [1.0, 1.25], lw=2.4, color=DARK)
    plateau(ax, x0 + 2.0, *gauche)
    plateau(ax, x0 + 7.0, *droite)
    if titre:
        ax.text(x0 + 4.5, -0.45, titre, ha="center", va="top", fontsize=13, color=DARK,
                fontweight="bold")


def balances(path, cas, w=11.0, h=3.8):
    fig, ax = new_fig(w, h)
    for i, (g, d, t) in enumerate(cas):
        balance(ax, i * 10.0, g, d, t)
    ax.set_xlim(-0.3, 10.0 * len(cas) - 0.9)
    ax.set_ylim(-1.3, 4.0)
    ax.set_aspect("equal")
    ax.axis("off")
    _save(fig, path)


balances(C("equations_4e_balance.png"),
         [((3, 4), (0, 19), "$3x + 4 = 19$"), ((3, 0), (0, 15), "on enlève 4 de chaque côté : $3x = 15$")],
         w=11.5, h=3.9)
balances(X("equations_4e_balances.png"),
         [((3, 4), (0, 19), "balance 1"), ((2, 7), (5, 1), "balance 2")], w=11.5, h=3.9)
balances(X("equations_4e_balances_solution.png"),
         [((1, 0), (0, 5), "balance 1 : $x = 5$"), ((0, 6), (3, 0), "balance 2 : $6 = 3x$, donc $x = 2$")],
         w=11.5, h=3.9)


def methode(path):
    fig, ax = new_fig(11.0, 2.6)
    etapes = [("1. Choisir\nl'inconnue", BLUE), ("2. Écrire\nl'équation", ORANGE),
              ("3. Résoudre", GREEN), ("4. Vérifier et\nrépondre par\nune phrase", "#8e44ad")]
    for i, (t, col) in enumerate(etapes):
        x = i * 2.8
        ax.add_patch(FancyBboxPatch((x, 0), 2.2, 1.5, boxstyle="round,pad=0.08", facecolor="white",
                                    edgecolor=col, lw=2.2))
        ax.text(x + 1.1, 0.75, t, ha="center", va="center", fontsize=12, color=col,
                fontweight="bold")
        if i < 3:
            ax.add_patch(FancyArrowPatch((x + 2.32, 0.75), (x + 2.68, 0.75), arrowstyle="-|>",
                                         mutation_scale=16, lw=2, color=NEUTRAL))
    ax.set_xlim(-0.2, 11.2)
    ax.set_ylim(-0.2, 1.75)
    ax.axis("off")
    _save(fig, path)


methode(C("equations_4e_methode.png"))


def iso_rect(path):
    fig, ax = new_fig(10.0, 4.2)
    A, B, Cc = np.array([0, 0]), np.array([4, 0]), np.array([2, 4.2])
    ax.add_patch(Polygon([A, B, Cc], closed=True, facecolor=LBLUE, edgecolor=BLUE, lw=2))
    seg_label(ax, A, Cc, "$x + 3$", side=1, offset=0.45, fs=14)
    seg_label(ax, B, Cc, "$x$", side=-1, offset=0.4, fs=14)
    seg_label(ax, A, B, "$x$", side=-1, offset=0.4, fs=14)
    ax.text(2, -1.2, "triangle : périmètre 36 cm", ha="center", fontsize=12, color=BLUE,
            fontweight="bold")
    ax.add_patch(Rectangle((6.5, 0.5), 6, 2, facecolor=LORANGE, edgecolor=ORANGE, lw=2))
    ax.text(9.5, 0.1, "longueur = 3 × largeur", ha="center", va="top", fontsize=12, color=DARK)
    ax.text(6.3, 1.5, "$\\ell$", ha="right", va="center", fontsize=14, color=DARK)
    ax.text(9.5, -1.2, "rectangle : périmètre 56 cm", ha="center", fontsize=12, color=ORANGE,
            fontweight="bold")
    ax.set_xlim(-1.2, 13)
    ax.set_ylim(-1.7, 4.6)
    ax.set_aspect("equal")
    ax.axis("off")
    _save(fig, path)


iso_rect(X("equations_4e_perimetres.png"))


def angles(path):
    fig, ax = new_fig(7.0, 4.2)
    A, B, Cc = np.array([0, 0]), np.array([6, 0]), np.array([1.95, 3.35])
    ax.add_patch(Polygon([A, B, Cc], closed=True, facecolor=LBLUE, edgecolor=BLUE, lw=2))
    angle_arc(ax, A, B - A, Cc - A, r=0.7, color=ORANGE, label="$2x$", label_r=1.15, fs=14)
    angle_arc(ax, B, A - B, Cc - B, r=0.9, color=GREEN, label="$x$", label_r=1.35, fs=14)
    angle_arc(ax, Cc, A - Cc, B - Cc, r=0.55, color="#8e44ad", label="$x + 20$", label_r=1.05,
              fs=13)
    for P, n, off in [(A, "A", (-16, -14)), (B, "B", (6, -14)), (Cc, "C", (-4, 8))]:
        dot_label(ax, P, f"${n}$", *off, color=DARK, s=30)
    ax.set_xlim(-0.8, 6.6)
    ax.set_ylim(-0.7, 4.1)
    ax.set_aspect("equal")
    ax.axis("off")
    _save(fig, path)


angles(X("equations_4e_angles.png"))


def carre_rect(path):
    fig, ax = new_fig(9.0, 4.0)
    ax.add_patch(Rectangle((0, 0), 3.2, 3.2, facecolor=LBLUE, edgecolor=BLUE, lw=2))
    ax.text(1.6, -0.3, "$x$", ha="center", va="top", fontsize=14)
    ax.text(-0.2, 1.6, "$x$", ha="right", va="center", fontsize=14)
    ax.add_patch(Rectangle((5, 0.6), 5.0, 1.8, facecolor=LORANGE, edgecolor=ORANGE, lw=2))
    ax.text(7.5, 0.3, "$x + 4$", ha="center", va="top", fontsize=14)
    ax.text(4.8, 1.5, "$x - 2$", ha="right", va="center", fontsize=14)
    ax.set_xlim(-0.8, 10.4)
    ax.set_ylim(-0.9, 3.5)
    ax.set_aspect("equal")
    ax.axis("off")
    _save(fig, path)


carre_rect(X("equations_4e_carre_rectangle.png"))


def poursuite(path, solution=False):
    fig, ax = new_fig(10.5, 3.0)
    ax.annotate("", xy=(25, 0), xytext=(-0.5, 0), arrowprops=dict(arrowstyle="->", lw=1.6,
                                                                    color=NEUTRAL))
    for k in range(0, 25, 5):
        ax.plot([k, k], [-0.25, 0.25], lw=1.2, color=NEUTRAL)
        ax.text(k, -0.55, f"{k} km", ha="center", va="top", fontsize=10.5, color=DARK)
    ax.scatter([0], [0], s=70, color=DARK, zorder=5)
    ax.text(0, 0.5, "départ", ha="center", fontsize=11, color=DARK)
    if not solution:
        ax.text(7.5, 1.3, "Léo : part à 14 h, 15 km/h", color=BLUE, fontsize=12, fontweight="bold")
        ax.text(7.5, 2.1, "Mia : part à 14 h 30, 25 km/h", color=ORANGE, fontsize=12,
                fontweight="bold")
        ax.scatter([7.5], [0], s=70, color=BLUE, zorder=5)
        ax.text(7.5, -1.25, "Léo à 14 h 30", ha="center", fontsize=10.5, color=BLUE)
    else:
        ax.scatter([18.75], [0], s=90, color=GREEN, zorder=5)
        ax.annotate("rattrapage à 15 h 15\nà 18,75 km du départ", (18.75, 0), xytext=(13, 1.2),
                    fontsize=12, color=GREEN, fontweight="bold",
                    arrowprops=dict(arrowstyle="->", color=GREEN))
    ax.set_xlim(-1.2, 26)
    ax.set_ylim(-1.7, 2.8)
    ax.axis("off")
    _save(fig, path)


poursuite(X("equations_4e_poursuite.png"))
poursuite(X("equations_4e_poursuite_solution.png"), solution=True)


def terrain(path, solution=False):
    fig, ax = new_fig(8.0, 4.8)
    L, H, x = 12.0, 8.0, 8.0
    ax.add_patch(Rectangle((0, 0), x, H, facecolor=LGREEN, edgecolor=GREEN, lw=2))
    ax.add_patch(Rectangle((x, 0), L - x, H, facecolor=LORANGE, edgecolor=ORANGE, lw=2))
    ax.text(x / 2, H / 2, "parcelle 1", ha="center", va="center", fontsize=13, color=GREEN,
            fontweight="bold")
    ax.text(x + (L - x) / 2, H / 2, "parcelle 2", ha="center", va="center", fontsize=12,
            color=ORANGE, fontweight="bold")
    ax.annotate("", xy=(x, -0.6), xytext=(0, -0.6), arrowprops=dict(arrowstyle="<->", lw=1.4))
    ax.text(x / 2, -0.8, "80 m" if solution else "$x$", ha="center", va="top", fontsize=14,
            color=GREEN if solution else DARK, fontweight="bold" if solution else "normal")
    ax.text(L / 2, H + 0.3, "120 m", ha="center", fontsize=13, color=DARK)
    ax.text(-0.3, H / 2, "80 m", ha="right", va="center", fontsize=13, color=DARK)
    ax.set_xlim(-2, L + 0.4)
    ax.set_ylim(-2.0, H + 1.1)
    ax.set_aspect("equal")
    ax.axis("off")
    _save(fig, path)


terrain(X("equations_4e_terrain.png"))
terrain(X("equations_4e_terrain_solution.png"), solution=True)


def tri_carre(path):
    fig, ax = new_fig(9.0, 4.2)
    A, B, Cc = np.array([0, 0]), np.array([4.4, 0]), np.array([2.2, 3.81])
    ax.add_patch(Polygon([A, B, Cc], closed=True, facecolor=LBLUE, edgecolor=BLUE, lw=2))
    seg_label(ax, A, B, "$x + 4$", side=-1, offset=0.45, fs=14)
    ax.text(2.2, 1.2, "équilatéral", ha="center", fontsize=11.5, color=BLUE)
    ax.add_patch(Rectangle((6.5, 0), 3.4, 3.4, facecolor=LORANGE, edgecolor=ORANGE, lw=2))
    ax.text(8.2, -0.3, "$x + 1$", ha="center", va="top", fontsize=14)
    ax.text(8.2, 1.7, "carré", ha="center", va="center", fontsize=12, color=ORANGE)
    ax.set_xlim(-0.6, 10.4)
    ax.set_ylim(-1.0, 4.2)
    ax.set_aspect("equal")
    ax.axis("off")
    _save(fig, path)


tri_carre(X("equations_4e_triangle_carre.png"))


def diophante(path):
    fig, ax = new_fig(11.0, 2.6)
    parts = [("enfance\n14 ans", 14, BLUE, LBLUE), ("jeunesse\n7 ans", 7, ORANGE, LORANGE),
             ("célibat\n12 ans", 12, GREEN, LGREEN), ("5", 5, DARK, "#e5e8eb"),
             ("vie du fils : 42 ans", 42, "#8e44ad", LPURP), ("4", 4, DARK, "#e5e8eb")]
    x = 0
    for t, k, col, fc in parts:
        ax.add_patch(Rectangle((x, 0), k, 2, facecolor=fc, edgecolor=col, lw=1.6))
        ax.text(x + k / 2, 1, t, ha="center", va="center", fontsize=10.5 if k > 6 else 10,
                color=col, fontweight="bold")
        x += k
    for a in (0, 14, 21, 33, 38, 80, 84):
        ax.text(a, -0.35, str(a), ha="center", va="top", fontsize=10.5, color=DARK)
    ax.text(42, 2.5, "Diophante a vécu 84 ans", ha="center", fontsize=12.5, color=GREEN,
            fontweight="bold")
    ax.set_xlim(-1, 85)
    ax.set_ylim(-1.1, 3.0)
    ax.axis("off")
    _save(fig, path)


diophante(X("equations_4e_diophante_solution.png"))
