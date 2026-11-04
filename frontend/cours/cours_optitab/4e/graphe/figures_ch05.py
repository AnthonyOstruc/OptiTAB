# -*- coding: utf-8 -*-
"""Figures du chapitre 5 (calcul littéral et distributivité) — 4ème OptiTAB."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fig4e import (new_fig, _save, tableau, BLUE, ORANGE, GREEN, DARK, NEUTRAL,
                   DIR_COURS, DIR_EXOS)
import numpy as np
from matplotlib.patches import Rectangle, Polygon

C = lambda f: os.path.join(DIR_COURS, f)  # noqa: E731
X = lambda f: os.path.join(DIR_EXOS, f)   # noqa: E731
LBLUE, LORANGE, LGREEN, LPURP = "#d6eafc", "#fdebd0", "#e8f5e9", "#efe3f5"
PURP = "#8e44ad"


def box(ax, x, y, w, h, fc, ec, txt=None, col=DARK, fs=14):
    ax.add_patch(Rectangle((x, y), w, h, facecolor=fc, edgecolor=ec, lw=2))
    if txt:
        ax.text(x + w / 2, y + h / 2, txt, ha="center", va="center", fontsize=fs, color=col,
                fontweight="bold")


def modele_simple(path, k="k", a="a", b="b", w=(3.0, 2.0), h=1.6, aires=True, titre=None):
    fig, ax = new_fig(7.6, 3.6)
    box(ax, 0, 0, w[0], h, LBLUE, BLUE, f"${k} \\times {a}$" if aires else None, BLUE)
    box(ax, w[0], 0, w[1], h, LORANGE, ORANGE, f"${k} \\times {b}$" if aires else None, ORANGE)
    ax.text(w[0] / 2, -0.35, f"${a}$", ha="center", va="top", fontsize=15, color=BLUE)
    ax.text(w[0] + w[1] / 2, -0.35, f"${b}$", ha="center", va="top", fontsize=15, color=ORANGE)
    ax.text(-0.2, h / 2, f"${k}$", ha="right", va="center", fontsize=15, color=DARK)
    if titre:
        ax.text((w[0] + w[1]) / 2, h + 0.35, titre, ha="center", fontsize=13.5, color=GREEN,
                fontweight="bold")
    ax.set_xlim(-0.9, w[0] + w[1] + 0.3)
    ax.set_ylim(-0.9, h + (0.9 if titre else 0.3))
    ax.set_aspect("equal")
    ax.axis("off")
    _save(fig, path)


def modele_double(path, a, b, c, d, wa, wb, hc, hd, aires=None, titre=None, cols=None):
    """Rectangle (a+b) × (c+d) : colonnes a, b ; lignes c (haut), d (bas)."""
    fig, ax = new_fig(7.4, 5.4)
    cols = cols or [(LBLUE, BLUE), (LORANGE, ORANGE), (LGREEN, GREEN), (LPURP, PURP)]
    cells = [(0, hd, wa, hc), (wa, hd, wb, hc), (0, 0, wa, hd), (wa, 0, wb, hd)]
    for i, (x, y, w, h) in enumerate(cells):
        txt = aires[i] if aires else None
        box(ax, x, y, w, h, cols[i][0], cols[i][1], txt, cols[i][1], fs=13.5)
    ax.text(wa / 2, -0.3, f"${a}$", ha="center", va="top", fontsize=15, color=DARK)
    ax.text(wa + wb / 2, -0.3, f"${b}$", ha="center", va="top", fontsize=15, color=DARK)
    ax.text(-0.2, hd + hc / 2, f"${c}$", ha="right", va="center", fontsize=15, color=DARK)
    ax.text(-0.2, hd / 2, f"${d}$", ha="right", va="center", fontsize=15, color=DARK)
    if titre:
        ax.text((wa + wb) / 2, hc + hd + 0.35, titre, ha="center", fontsize=13, color=GREEN,
                fontweight="bold")
    ax.set_xlim(-1.0, wa + wb + 0.3)
    ax.set_ylim(-0.9, hc + hd + (0.9 if titre else 0.3))
    ax.set_aspect("equal")
    ax.axis("off")
    _save(fig, path)


modele_simple(C("calcul_litteral_4e_simple.png"),
              titre="$k \\times (a + b) = k \\times a + k \\times b$")
modele_double(C("calcul_litteral_4e_double.png"), "a", "b", "c", "d", 3.2, 1.8, 2.2, 1.3,
              aires=["$ac$", "$bc$", "$ad$", "$bd$"],
              titre="$(a + b)(c + d) = ac + ad + bc + bd$")
modele_simple(X("calcul_litteral_4e_trois_x4.png"), k="3", a="x", b="4", w=(3.2, 1.8), h=1.5,
              aires=False)
modele_double(X("calcul_litteral_4e_double_ex.png"), "x", "3", "x", "2", 3.0, 1.6, 3.0, 1.1)
modele_double(X("calcul_litteral_4e_double_ex_solution.png"), "x", "3", "x", "2", 3.0, 1.6, 3.0,
              1.1, aires=["$x^2$", "$3x$", "$2x$", "$6$"],
              titre="$(x+3)(x+2) = x^2 + 5x + 6$")


# ------------------------------------------------------------------ allumettes
def allumettes(path):
    fig, ax = new_fig(10.5, 2.8)
    x0 = 0
    for n in (1, 2, 3):
        segs = []
        for k in range(n):
            segs += [((x0 + k, 0), (x0 + k + 1, 0)), ((x0 + k, 1), (x0 + k + 1, 1))]
        for k in range(n + 1):
            segs.append(((x0 + k, 0), (x0 + k, 1)))
        for (P, Q) in segs:
            ax.plot([P[0], Q[0]], [P[1], Q[1]], lw=4, color="#d4a373", solid_capstyle="round")
            ax.scatter([Q[0]], [Q[1]], s=28, color="#c0392b", zorder=5)
        ax.text(x0 + n / 2, -0.45, f"{n} carré" + ("s" if n > 1 else ""), ha="center",
                fontsize=12.5, color=DARK, fontweight="bold")
        x0 += n + 1.5
    ax.set_xlim(-0.4, x0 - 1.1)
    ax.set_ylim(-0.8, 1.3)
    ax.set_aspect("equal")
    ax.axis("off")
    _save(fig, path)


allumettes(X("calcul_litteral_4e_allumettes.png"))


def rectangle_x(path):
    fig, ax = new_fig(6.8, 3.6)
    box(ax, 0, 0, 5.2, 2.0, LBLUE, BLUE)
    ax.text(2.6, -0.3, "$2x + 3$", ha="center", va="top", fontsize=15, color=DARK)
    ax.text(-0.2, 1.0, "$x$", ha="right", va="center", fontsize=15, color=DARK)
    ax.set_xlim(-0.9, 5.5)
    ax.set_ylim(-0.9, 2.3)
    ax.set_aspect("equal")
    ax.axis("off")
    _save(fig, path)


rectangle_x(X("calcul_litteral_4e_rectangle.png"))


def tapis(path, solution=False):
    fig, ax = new_fig(5.8, 5.8)
    if solution:
        box(ax, 0, 0, 5, 1, LORANGE, ORANGE, "$(x+1) \\times 1$", ORANGE, 11)
        box(ax, 5, 0, 1, 5, LGREEN, GREEN)
        ax.text(5.5, 2.5, "$(x+1) \\times 1$", rotation=90, ha="center", va="center",
                fontsize=11, color=GREEN, fontweight="bold")
        box(ax, 1, 5, 5, 1, LPURP, PURP, "$(x+1) \\times 1$", PURP, 11)
        box(ax, 0, 1, 1, 5, LBLUE, BLUE)
        ax.text(0.5, 3.5, "$(x+1) \\times 1$", rotation=90, ha="center", va="center",
                fontsize=11, color=BLUE, fontweight="bold")
    else:
        ax.add_patch(Rectangle((0, 0), 6, 6, facecolor="#e8d8b8", edgecolor=DARK, lw=2))
    ax.add_patch(Rectangle((1, 1), 4, 4, facecolor="white", edgecolor=DARK, lw=2, hatch="..",
                           alpha=0.9))
    ax.text(3, 3, "tapis", ha="center", va="center", fontsize=14, color=DARK, fontweight="bold",
            bbox=dict(fc="white", ec="none"))
    ax.annotate("", xy=(5, 1.45), xytext=(1, 1.45),
                arrowprops=dict(arrowstyle="<->", lw=1.4, color=DARK))
    ax.text(3, 1.6, "$x$", ha="center", va="bottom", fontsize=15, color=DARK,
            bbox=dict(fc="white", ec="none", pad=1))
    if not solution:
        ax.text(3, 0.5, "bordure de 1 m", ha="center", va="center", fontsize=11, color="#7a5c2e",
                fontweight="bold")
    ax.set_xlim(-0.3, 6.3)
    ax.set_ylim(-0.3, 6.3)
    ax.set_aspect("equal")
    ax.axis("off")
    _save(fig, path)


tapis(X("calcul_litteral_4e_tapis.png"))
tapis(X("calcul_litteral_4e_tapis_solution.png"), solution=True)


def tables(path):
    fig, ax = new_fig(10.5, 2.8)
    x0 = 0
    for n in (1, 2, 3):
        for k in range(n):
            ax.add_patch(Rectangle((x0 + k, 0), 1, 1, facecolor="#e8d8b8", edgecolor="#7a5c2e",
                                   lw=2))
        chairs = [(x0 + k + 0.5, -0.3) for k in range(n)] + [(x0 + k + 0.5, 1.3) for k in range(n)]
        chairs += [(x0 - 0.3, 0.5), (x0 + n + 0.3, 0.5)]
        for (cx, cy) in chairs:
            ax.scatter([cx], [cy], s=120, color=BLUE, zorder=5)
        ax.text(x0 + n / 2, -0.85, f"{n} table" + ("s" if n > 1 else ""), ha="center",
                fontsize=12.5, color=DARK, fontweight="bold")
        x0 += n + 1.6
    ax.set_xlim(-0.8, x0 - 1.0)
    ax.set_ylim(-1.2, 1.7)
    ax.set_aspect("equal")
    ax.axis("off")
    _save(fig, path)


tables(X("calcul_litteral_4e_tables.png"))


def piscine(path):
    fig, ax = new_fig(7.6, 4.8)
    ax.add_patch(Rectangle((0, 0), 10, 6, facecolor="#e0e0e0", edgecolor=DARK, lw=2))
    ax.add_patch(Rectangle((1, 1), 8, 4, facecolor=LBLUE, edgecolor=BLUE, lw=2))
    ax.text(5, 3, "bassin", ha="center", va="center", fontsize=14, color=BLUE, fontweight="bold")
    ax.text(5, 1.25, "$2x$", ha="center", va="bottom", fontsize=14, color=DARK)
    ax.text(1.25, 3, "$x$", ha="left", va="center", fontsize=14, color=DARK)
    ax.text(5, 0.5, "margelle de 1 m", ha="center", va="center", fontsize=11, color=DARK,
            fontweight="bold")
    ax.set_xlim(-0.3, 10.3)
    ax.set_ylim(-0.3, 6.3)
    ax.set_aspect("equal")
    ax.axis("off")
    _save(fig, path)


piscine(X("calcul_litteral_4e_piscine.png"))

tableau(X("calcul_litteral_4e_carre_magique.png"),
        [["$x - 3$", "$x + 2$", "$x + 1$"], ["$x + 4$", "$x$", "$x - 4$"],
         ["$x - 1$", "$x - 2$", "$x + 3$"]],
        larg_col=[1.8] * 3, haut=1.0, entete_col=False, entete_lig=False, fs=16)


def boite(path):
    fig, ax = new_fig(7.6, 5.4)
    W, H, c = 30, 20, 4
    ax.add_patch(Rectangle((0, 0), W, H, facecolor="white", edgecolor=DARK, lw=2))
    for (x, y) in [(0, 0), (W - c, 0), (0, H - c), (W - c, H - c)]:
        ax.add_patch(Rectangle((x, y), c, c, facecolor=LORANGE, edgecolor=ORANGE, lw=1.6,
                               hatch="//"))
    ax.add_patch(Rectangle((c, c), W - 2 * c, H - 2 * c, facecolor=LBLUE, edgecolor=BLUE, lw=1.6,
                           ls="--"))
    ax.text(W / 2, H / 2, "fond de la boîte", ha="center", va="center", fontsize=12.5,
            color=BLUE, fontweight="bold")
    ax.text(c / 2, -1.2, "$x$", ha="center", fontsize=14, color=ORANGE)
    ax.text(-1.0, c / 2, "$x$", ha="center", va="center", fontsize=14, color=ORANGE)
    ax.text(W / 2, -2.6, "30 cm", ha="center", fontsize=13, color=DARK)
    ax.text(-2.6, H / 2, "20 cm", ha="center", va="center", fontsize=13, color=DARK, rotation=90)
    ax.text(W / 2, H + 1.0, "on découpe un carré de côté $x$ dans chaque coin, puis on plie",
            ha="center", fontsize=11.5, color=DARK)
    ax.set_xlim(-4, W + 1)
    ax.set_ylim(-4, H + 2.4)
    ax.set_aspect("equal")
    ax.axis("off")
    _save(fig, path)


boite(X("calcul_litteral_4e_boite.png"))


def deux_rectangles(path):
    fig, ax = new_fig(9.6, 4.4)
    box(ax, 0, 0, 6.5, 2.5, LBLUE, BLUE, "A", BLUE, 16)
    ax.text(3.25, -0.3, "$x + 5$", ha="center", va="top", fontsize=14, color=DARK)
    ax.text(-0.2, 1.25, "$x + 1$", ha="right", va="center", fontsize=14, color=DARK)
    box(ax, 9.0, 0, 4.5, 4.5, LORANGE, ORANGE, "B", ORANGE, 16)
    ax.text(11.25, -0.3, "$x + 3$", ha="center", va="top", fontsize=14, color=DARK)
    ax.text(8.8, 2.25, "$x + 3$", ha="right", va="center", fontsize=14, color=DARK)
    ax.set_xlim(-1.8, 13.8)
    ax.set_ylim(-1.0, 4.8)
    ax.set_aspect("equal")
    ax.axis("off")
    _save(fig, path)


deux_rectangles(X("calcul_litteral_4e_deux_rectangles.png"))
