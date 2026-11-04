# -*- coding: utf-8 -*-
"""Figures : Seconde — Probabilités."""
from matplotlib.patches import Circle, Rectangle, FancyBboxPatch

from figlycee import new_fig, _save, txt, I, BLUE, ORANGE, GREEN, DARK, NEUTRAL, RED, LBLUE, LORANGE, LGREEN


def venn():
    fig, ax = new_fig(7.6, 4.6)
    ax.add_patch(FancyBboxPatch((-4.2, -2.4), 8.4, 4.8, boxstyle="round,pad=0.1", fc="#fafafa", ec=NEUTRAL, lw=1.5))
    ax.add_patch(Circle((-1.0, 0), 1.9, fc=LBLUE, ec=BLUE, lw=2.4, alpha=0.9))
    ax.add_patch(Circle((1.0, 0), 1.9, fc=LORANGE, ec=ORANGE, lw=2.4, alpha=0.6))
    # lentille A ∩ B
    import numpy as np
    t = np.linspace(-1, 1, 200)
    yb = np.sqrt(np.maximum(1.9 ** 2 - 1.0 ** 2, 0)) * t
    xa = 1.0 - np.sqrt(1.9 ** 2 - yb ** 2)
    xb = -1.0 + np.sqrt(1.9 ** 2 - yb ** 2)
    ax.fill(np.concatenate([xa, xb[::-1]]), np.concatenate([yb, yb[::-1]]), color=GREEN, alpha=0.3)
    txt(ax, -3.9, 2.0, "$\\Omega$", DARK, 17)
    txt(ax, -2.0, 0.2, "$A$", BLUE, 20, ha="center", va="center", fontweight="bold")
    txt(ax, 2.0, 0.2, "$B$", ORANGE, 20, ha="center", va="center", fontweight="bold")
    txt(ax, 0, 0, "$A \\cap B$", DARK, 13, ha="center", va="center", fontweight="bold")
    txt(ax, 0, -2.9, "$p(A \\cup B) = p(A) + p(B) - p(A \\cap B)$", DARK, 15, ha="center", va="top")
    ax.set_xlim(-4.5, 4.5)
    ax.set_ylim(-3.6, 2.7)
    ax.set_aspect("equal")
    ax.axis("off")
    _save(fig, I("2nd_proba_venn.png"))


def arbre():
    fig, ax = new_fig(8.2, 4.8)
    racine = (0, 0)
    niv1 = [("P", 2.6, 1.6), ("F", 2.6, -1.6)]
    for n1, x1, y1 in niv1:
        ax.plot([0.15, x1 - 0.3], [0, y1], color=BLUE, lw=1.8)
        txt(ax, (0.15 + x1 - 0.3) / 2, y1 / 2 + (0.28 if y1 > 0 else -0.28), "$\\frac{1}{2}$", DARK, 13,
            ha="center", va="center")
        txt(ax, x1, y1, f"${n1}$", BLUE, 17, ha="center", va="center", fontweight="bold")
        for k, n2 in enumerate(("P", "F")):
            y2 = y1 + (0.8 if k == 0 else -0.8)
            ax.plot([x1 + 0.3, 5.2 - 0.3], [y1, y2], color=ORANGE, lw=1.8)
            txt(ax, (x1 + 5.2) / 2, (y1 + y2) / 2 + (0.25 if k == 0 else -0.25), "$\\frac{1}{2}$", DARK, 12,
                ha="center", va="center")
            txt(ax, 5.2, y2, f"${n2}$", ORANGE, 17, ha="center", va="center", fontweight="bold")
            txt(ax, 6.0, y2, f"issue $({n1}\\,;{n2})$ : $p = \\frac{{1}}{{4}}$", DARK, 13, va="center")
    ax.scatter([0], [0], s=30, color=DARK)
    txt(ax, 2.6, 3.0, "1er lancer", BLUE, 12.5, ha="center")
    txt(ax, 5.2, 3.0, "2e lancer", ORANGE, 12.5, ha="center")
    ax.set_xlim(-0.4, 10.6)
    ax.set_ylim(-3.0, 3.5)
    ax.set_aspect("equal")
    ax.axis("off")
    _save(fig, I("2nd_proba_arbre.png"))


def tableau():
    fig, ax = new_fig(6.2, 5.6)
    c = 1.0
    for i in range(7):
        for j in range(7):
            x, y = j * c, -i * c
            if i == 0 and j == 0:
                ax.add_patch(Rectangle((x, y - c), c, c, fc="#ecf0f1", ec=NEUTRAL, lw=1))
                txt(ax, x + 0.5, y - 0.5, "$+$", DARK, 15, ha="center", va="center")
            elif i == 0 or j == 0:
                ax.add_patch(Rectangle((x, y - c), c, c, fc=LBLUE, ec=NEUTRAL, lw=1))
                txt(ax, x + 0.5, y - 0.5, f"${i + j}$", BLUE, 15, ha="center", va="center", fontweight="bold")
            else:
                s = i + j
                ax.add_patch(Rectangle((x, y - c), c, c, fc=LGREEN if s == 7 else "white", ec=NEUTRAL, lw=1))
                txt(ax, x + 0.5, y - 0.5, f"${s}$", GREEN if s == 7 else DARK, 14, ha="center", va="center",
                    fontweight="bold" if s == 7 else "normal")
    txt(ax, 4.0, 0.35, "dé 2", BLUE, 12.5, ha="center", va="bottom")
    txt(ax, -0.25, -4.0, "dé 1", BLUE, 12.5, ha="right", va="center", rotation=90)
    txt(ax, 3.5, -7.3, "$p(\\text{somme} = 7) = \\frac{6}{36} = \\frac{1}{6}$", GREEN, 15, ha="center", va="top",
        fontweight="bold")
    ax.set_xlim(-0.9, 7.2)
    ax.set_ylim(-8.4, 1.0)
    ax.set_aspect("equal")
    ax.axis("off")
    _save(fig, I("2nd_proba_tableau.png"))


venn()
arbre()
tableau()
