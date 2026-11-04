# -*- coding: utf-8 -*-
"""Figures du chapitre 4 (carrés et racines carrées) — 4ème OptiTAB."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fig4e import (new_fig, _save, tableau, graphe, BLUE, ORANGE, GREEN, DARK, NEUTRAL,
                   DIR_COURS, DIR_EXOS)
import numpy as np
from matplotlib.patches import Rectangle, Polygon, Circle

C = lambda f: os.path.join(DIR_COURS, f)  # noqa: E731
X = lambda f: os.path.join(DIR_EXOS, f)   # noqa: E731
LBLUE, LORANGE, LGREEN = "#d6eafc", "#fdebd0", "#e8f5e9"


def carre_aire(path):
    fig, ax = new_fig(5.6, 5.0)
    ax.add_patch(Rectangle((0, 0), 5, 5, facecolor=LBLUE, edgecolor=BLUE, lw=2))
    for k in range(1, 5):
        ax.plot([k, k], [0, 5], lw=0.7, color="#9fc5e8")
        ax.plot([0, 5], [k, k], lw=0.7, color="#9fc5e8")
    ax.text(2.5, 2.5, "aire = 25 cm²", ha="center", va="center", fontsize=15, color=BLUE,
            fontweight="bold", bbox=dict(fc="white", ec="none", alpha=0.85))
    ax.text(2.5, -0.55, "côté = $\\sqrt{25} = 5$ cm", ha="center", fontsize=14, color=ORANGE,
            fontweight="bold")
    ax.set_xlim(-0.4, 5.4)
    ax.set_ylim(-1.1, 5.3)
    ax.set_aspect("equal")
    ax.axis("off")
    _save(fig, path)


carre_aire(C("racines_4e_carre_aire.png"))

ns = list(range(1, 16))
tableau(C("racines_4e_carres_parfaits.png"),
        [["$n$"] + [str(n) for n in ns[:8]], ["$n^2$"] + [str(n * n) for n in ns[:8]],
         ["$n$"] + [str(n) for n in ns[8:]] + [""], ["$n^2$"] + [str(n * n) for n in ns[8:]] + [""]],
        larg_col=[1.1] + [1.05] * 8, entete_col=False, titre="Les carrés parfaits de 1 à 225")
trous = {3: "?", 6: "?", 9: "?", 11: "?", 13: "?", 15: "?"}
tableau(X("racines_4e_table_trous.png"),
        [["$n$"] + [str(n) for n in ns[:8]],
         ["$n^2$"] + [trous.get(n, str(n * n)) for n in ns[:8]],
         ["$n$"] + [str(n) for n in ns[8:]] + [""],
         ["$n^2$"] + [trous.get(n, str(n * n)) for n in ns[8:]] + [""]],
        larg_col=[1.1] + [1.05] * 8, entete_col=False,
        surligne=[(1, 3), (1, 6), (3, 1), (3, 3), (3, 5), (3, 7)])
tableau(X("racines_4e_table_solution.png"),
        [["$n$"] + [str(n) for n in ns[:8]], ["$n^2$"] + [str(n * n) for n in ns[:8]],
         ["$n$"] + [str(n) for n in ns[8:]] + [""], ["$n^2$"] + [str(n * n) for n in ns[8:]] + [""]],
        larg_col=[1.1] + [1.05] * 8, entete_col=False,
        vert=[(1, 3), (1, 6), (3, 1), (3, 3), (3, 5), (3, 7)])


def encadrement(path, pts, lo=0, hi=10, titre=None):
    fig, ax = new_fig(10.5, 2.4)
    ax.annotate("", xy=(hi + 0.5, 0), xytext=(lo - 0.3, 0),
                arrowprops=dict(arrowstyle="->", lw=1.6, color=NEUTRAL))
    for k in range(lo, hi + 1):
        ax.plot([k, k], [-0.12, 0.12], lw=1.3, color=NEUTRAL)
        ax.text(k, -0.3, str(k), ha="center", va="top", fontsize=12, color=DARK)
    for i, (lab, x, col) in enumerate(pts):
        ax.scatter([x], [0], s=70, color=col, zorder=5)
        ax.text(x, 0.3, lab, ha="center", va="bottom", fontsize=14, color=col, fontweight="bold")
    if titre:
        ax.text((lo + hi) / 2, 1.25, titre, ha="center", fontsize=12.5, color=DARK)
    ax.set_xlim(lo - 0.5, hi + 0.8)
    ax.set_ylim(-0.9, 1.6 if titre else 1.1)
    ax.axis("off")
    _save(fig, path)


encadrement(C("racines_4e_encadrement.png"), [("$\\sqrt{20} \\approx 4{,}47$", 20 ** 0.5, ORANGE)],
            lo=0, hi=8, titre="$4^2 = 16 < 20 < 25 = 5^2$ donc $4 < \\sqrt{20} < 5$")
encadrement(X("racines_4e_encadrement_solution.png"),
            [("$\\sqrt{20}$", 20 ** 0.5, ORANGE), ("$\\sqrt{50}$", 50 ** 0.5, BLUE),
             ("$\\sqrt{90}$", 90 ** 0.5, GREEN)], lo=0, hi=10)


def trois_carres(path):
    fig, ax = new_fig(9.5, 4.2)
    data = [("A", 8, "64 cm²"), ("B", 1.5, "2,25 cm²"), ("C", 30 ** 0.5, "30 cm²")]
    x = 0
    for nom, c, a in data:
        ax.add_patch(Rectangle((x, 0), c, c, facecolor=LBLUE, edgecolor=BLUE, lw=2))
        ax.text(x + c / 2, c + 0.35, f"carré {nom}", ha="center", fontsize=13, color=DARK,
                fontweight="bold")
        ax.text(x + c / 2, -0.55, f"aire : {a}", ha="center", fontsize=12.5, color=ORANGE,
                fontweight="bold")
        x += c + 1.6
    ax.set_xlim(-0.3, x)
    ax.set_ylim(-1.1, 9)
    ax.set_aspect("equal")
    ax.axis("off")
    _save(fig, path)


trois_carres(X("racines_4e_trois_carres.png"))


def carre_rectangle(path, solution=False):
    fig, ax = new_fig(9.5, 4.6)
    ax.add_patch(Rectangle((0, 0), 18, 8, facecolor=LBLUE, edgecolor=BLUE, lw=2))
    ax.text(9, -1.1, "18 cm", ha="center", fontsize=13, color=DARK)
    ax.text(-0.6, 4, "8 cm", ha="right", va="center", fontsize=13, color=DARK)
    ax.add_patch(Rectangle((21, 0), 12, 12, facecolor=LGREEN if solution else LORANGE,
                           edgecolor=GREEN if solution else ORANGE, lw=2))
    ax.text(27, -1.1, "12 cm" if solution else "?", ha="center", fontsize=13,
            color=GREEN if solution else ORANGE, fontweight="bold")
    ax.text(9, 4, "aire 144 cm²" if solution else "rectangle", ha="center", va="center",
            fontsize=13, color=BLUE, fontweight="bold")
    ax.text(27, 6, "aire 144 cm²" if solution else "carré de\nmême aire", ha="center",
            va="center", fontsize=13, color=GREEN if solution else ORANGE, fontweight="bold")
    ax.set_xlim(-3, 34)
    ax.set_ylim(-2.2, 13)
    ax.set_aspect("equal")
    ax.axis("off")
    _save(fig, path)


carre_rectangle(X("racines_4e_carre_rectangle.png"))
carre_rectangle(X("racines_4e_carre_rectangle_solution.png"), solution=True)


def menon(path, solution=False):
    from fig4e import dot_label
    fig, ax = new_fig(6.4, 6.6)
    A, B, Cc, D = np.array([0, 0]), np.array([4, 0]), np.array([4, 4]), np.array([0, 4])
    E, F = np.array([4, 8]), np.array([8, 4])
    if solution:
        ax.add_patch(Polygon([B, F, E, D], closed=True, facecolor=LGREEN, edgecolor=GREEN, lw=2.2))
        ax.plot([4, 4], [0, 8], lw=1.2, color=GREEN, ls="--")
        ax.plot([0, 8], [4, 4], lw=1.2, color=GREEN, ls="--")
        for (x, y) in [(2.9, 2.9), (5.1, 2.9), (5.1, 5.1), (2.9, 5.1)]:
            ax.text(x, y, "8 cm²", ha="center", va="center", fontsize=10.5, color=GREEN,
                    fontweight="bold")
        ax.text(4, -1.5, "carré $BFED$ construit sur la diagonale : 4 × 8 = 32 cm²",
                ha="center", fontsize=11.5, color=GREEN, fontweight="bold")
    ax.add_patch(Polygon([A, B, Cc, D], closed=True, facecolor="none" if solution else LBLUE,
                         edgecolor=BLUE, lw=2.2))
    ax.plot([B[0], D[0]], [B[1], D[1]], lw=2.2, color=ORANGE)
    if not solution:
        ax.text(2, -0.7, "4 cm", ha="center", fontsize=13, color=DARK)
        ax.text(1.2, 1.2, "16 cm²", ha="center", va="center", fontsize=12, color=BLUE,
                fontweight="bold")
        ax.text(2.35, 2.35, "diagonale", ha="left", va="bottom", fontsize=11, color=ORANGE,
                fontweight="bold", rotation=-45)
    pts = [(A, "A", (-16, -16)), (B, "B", (6, -16)), (Cc, "C", (8, 4) if not solution else (-20, 6)),
           (D, "D", (-18, 4))]
    if solution:
        pts += [(E, "E", (6, 4)), (F, "F", (6, -4))]
    for P, n, off in pts:
        dot_label(ax, P, f"${n}$", *off, color=DARK, s=30)
    if solution:
        ax.set_xlim(-1, 9)
        ax.set_ylim(-2.1, 8.8)
    else:
        ax.set_xlim(-1, 5.2)
        ax.set_ylim(-1.2, 5)
    ax.set_aspect("equal")
    ax.axis("off")
    _save(fig, path)


menon(X("racines_4e_menon.png"))
menon(X("racines_4e_menon_solution.png"), solution=True)


def allee(path):
    fig, ax = new_fig(6.0, 6.0)
    ax.add_patch(Rectangle((0, 0), 45, 45, facecolor="#e8d8b8", edgecolor=DARK, lw=2))
    ax.add_patch(Rectangle((1.2, 1.2), 42.6, 42.6, facecolor=LGREEN, edgecolor=GREEN, lw=1.6))
    ax.text(22.5, 22.5, "pelouse", ha="center", va="center", fontsize=14, color=GREEN,
            fontweight="bold")
    ax.text(22.5, -1.6, "allée de 1 m de large tout autour (en beige)", ha="center", va="center", fontsize=11,
            color="#7a5c2e", fontweight="bold")
    ax.text(22.5, 47.5, "aire totale : 2 025 m²", ha="center", fontsize=12.5, color=DARK,
            fontweight="bold")
    ax.set_xlim(-2, 47)
    ax.set_ylim(-3.5, 50)
    ax.set_aspect("equal")
    ax.axis("off")
    _save(fig, path)


allee(X("racines_4e_allee.png"))


def puzzle(path):
    fig, ax = new_fig(9.0, 4.6)
    ax.add_patch(Rectangle((0, 0), 3, 3, facecolor=LBLUE, edgecolor=BLUE, lw=2))
    ax.text(1.5, 1.5, "9 cm²", ha="center", va="center", fontsize=13, color=BLUE, fontweight="bold")
    ax.text(4.0, 1.5, "+", ha="center", va="center", fontsize=22, color=DARK)
    ax.add_patch(Rectangle((5, 0), 4, 4, facecolor=LORANGE, edgecolor=ORANGE, lw=2))
    ax.text(7, 2, "16 cm²", ha="center", va="center", fontsize=13, color=ORANGE, fontweight="bold")
    ax.text(10.0, 2, "=", ha="center", va="center", fontsize=22, color=DARK)
    ax.add_patch(Rectangle((11, 0), 5, 5, facecolor=LGREEN, edgecolor=GREEN, lw=2))
    ax.text(13.5, 2.5, "25 cm²", ha="center", va="center", fontsize=13, color=GREEN,
            fontweight="bold")
    ax.text(13.5, -0.7, "côté ?", ha="center", fontsize=13, color=GREEN, fontweight="bold")
    ax.set_xlim(-0.3, 16.4)
    ax.set_ylim(-1.3, 5.4)
    ax.set_aspect("equal")
    ax.axis("off")
    _save(fig, path)


puzzle(X("racines_4e_puzzle.png"))


def pizzas(path):
    fig, ax = new_fig(9.0, 4.2)
    for cx, d, txt, col, fc in [(0, 30, "Ø 30 cm", ORANGE, LORANGE), (27, 20, "Ø 20 cm", BLUE, LBLUE),
                                (50, 20, "Ø 20 cm", BLUE, LBLUE)]:
        ax.add_patch(Circle((cx, 0), d / 2, facecolor=fc, edgecolor=col, lw=2))
        ax.plot([cx - d / 2, cx + d / 2], [0, 0], lw=1.2, color=col, ls="--")
        ax.text(cx, -d / 2 - 3, txt, ha="center", fontsize=13, color=col, fontweight="bold")
    ax.text(38.5, 0, "+", ha="center", va="center", fontsize=22, color=DARK)
    ax.text(0, 18, "1 grande : 14 €", ha="center", fontsize=12.5, color=ORANGE, fontweight="bold")
    ax.text(38.5, 18, "2 moyennes : 9 € chacune", ha="center", fontsize=12.5, color=BLUE,
            fontweight="bold")
    ax.set_xlim(-17, 62)
    ax.set_ylim(-21, 22)
    ax.set_aspect("equal")
    ax.axis("off")
    _save(fig, path)


pizzas(X("racines_4e_pizzas.png"))

graphe(X("racines_4e_chute.png"),
       curves=[(lambda t: 4.9 * t * t, 0, 5.05, BLUE, ("$d = 4{,}9 \\times t^2$", 3.2))],
       points=[("", 1, 4.9), ("", 2, 19.6), ("", 3, 44.1)],
       xb=(-0.3, 5.6), yb=(-8, 135), xt=1, yt=20, w=8.2, h=5.4,
       xlabel="$t$ (s)", ylabel="$d$ (m)")
