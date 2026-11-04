# -*- coding: utf-8 -*-
"""Figures : Première — Probabilités conditionnelles et indépendance."""
import numpy as np
from matplotlib.patches import Ellipse, FancyBboxPatch

from figlycee import new_fig, _save, txt, I, BLUE, ORANGE, GREEN, DARK, NEUTRAL, RED, LBLUE, LORANGE, LGREEN

BOITE = dict(fc="white", ec="none", pad=1.2)


def arbre():
    fig, ax = new_fig(9.4, 5.2)
    n1 = [("A", 0.3, 1.7, BLUE), ("\\overline{A}", 0.7, -1.7, ORANGE)]
    feuilles = {"A": [("B", 0.8), ("\\overline{B}", 0.2)], "\\overline{A}": [("B", 0.1), ("\\overline{B}", 0.9)]}
    ax.scatter([0], [0], s=30, color=DARK)
    for nom, p, y1, col in n1:
        ax.plot([0.15, 2.3], [0.0, y1], color=col, lw=2)
        txt(ax, 1.1, y1 / 2 + (0.32 if y1 > 0 else -0.32), f"${p:g}$".replace(".", "{,}"), col, 13, ha="center",
            va="center", fontweight="bold", bbox=BOITE)
        txt(ax, 2.6, y1, f"${nom}$", col, 17, ha="center", va="center", fontweight="bold")
        for k, (f, q) in enumerate(feuilles[nom]):
            y2 = y1 + (0.85 if k == 0 else -0.85)
            ax.plot([2.9, 5.0], [y1, y2], color=NEUTRAL, lw=1.6)
            txt(ax, 3.95, (y1 + y2) / 2 + (0.25 if k == 0 else -0.25), f"${q:g}$".replace(".", "{,}"), DARK, 12.5,
                ha="center", va="center", bbox=BOITE)
            txt(ax, 5.3, y2, f"${f}$", GREEN if f == "B" else DARK, 16, ha="center", va="center",
                fontweight="bold")
            prod = p * q
            txt(ax, 6.0, y2, f"$P({nom} \\cap {f}) = {p:g} \\times {q:g} = {prod:.2f}$".replace(".", "{,}"),
                GREEN if f == "B" else DARK, 12.5, va="center")
    txt(ax, 2.6, 3.0, "1re épreuve", BLUE, 12, ha="center")
    txt(ax, 5.3, 3.0, "2e épreuve", NEUTRAL, 12, ha="center")
    txt(ax, 4.7, -3.4, "$P(B) = 0{,}24 + 0{,}07 = 0{,}31$ (somme des chemins menant à $B$)", GREEN, 13, ha="center",
        va="center", fontweight="bold")
    ax.set_xlim(-0.4, 11.4)
    ax.set_ylim(-3.9, 3.4)
    ax.set_aspect("equal")
    ax.axis("off")
    _save(fig, I("1er_pcond_arbre.png"))


def partition():
    fig, ax = new_fig(8.2, 4.4)
    ax.add_patch(FancyBboxPatch((0, 0), 9, 4, boxstyle="round,pad=0.05", fc="#fafafa", ec=NEUTRAL, lw=1.5))
    for x in (3, 6):
        ax.plot([x, x], [0, 4], color=NEUTRAL, lw=1.5)
    for k, (col, fc) in enumerate(((BLUE, LBLUE), (ORANGE, LORANGE), (RED, "#fdecea"))):
        ax.add_patch(FancyBboxPatch((3 * k + 0.08, 0.08), 2.84, 3.84, boxstyle="square,pad=0", fc=fc, ec="none",
                                    zorder=0))
        txt(ax, 3 * k + 0.35, 3.45, f"$A_{k + 1}$", col, 17, fontweight="bold")
    ax.add_patch(Ellipse((4.5, 1.7), 8.3, 1.9, fc=GREEN, ec=GREEN, lw=2.2, alpha=0.25))
    ax.add_patch(Ellipse((4.5, 1.7), 8.3, 1.9, fill=False, ec=GREEN, lw=2.2))
    txt(ax, 8.2, 2.85, "$B$", GREEN, 18, fontweight="bold")
    for k in range(3):
        txt(ax, 3 * k + 1.5, 1.7, f"$A_{k + 1} \\cap B$", DARK, 13, ha="center", va="center")
    txt(ax, 4.5, -0.5, "$P(B) = P(A_1 \\cap B) + P(A_2 \\cap B) + P(A_3 \\cap B)$", DARK, 14, ha="center", va="top")
    ax.set_xlim(-0.3, 9.3)
    ax.set_ylim(-1.3, 4.3)
    ax.set_aspect("equal")
    ax.axis("off")
    _save(fig, I("1er_pcond_partition.png"))


arbre()
partition()
