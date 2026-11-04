# -*- coding: utf-8 -*-
"""Figures : Seconde — Multiples, diviseurs et nombres premiers."""
from matplotlib.patches import Rectangle, FancyBboxPatch

from figlycee import new_fig, _save, txt, I, BLUE, ORANGE, GREEN, DARK, NEUTRAL, LBLUE


def rectangles_36():
    fig, ax = new_fig(9.6, 5.4)
    c = 0.32
    y = 0.0
    for L, l, col in [(36, 1, "#d6eafc"), (18, 2, "#fdebd0"), (12, 3, "#e8f5e9"), (9, 4, "#f4ecf7"), (6, 6, "#fef9e7")]:
        y0 = y - l * c
        ax.add_patch(Rectangle((0, y0), L * c, l * c, facecolor=col, edgecolor=DARK, lw=1.4))
        for i in range(1, L):
            ax.plot([i * c, i * c], [y0, y], color=NEUTRAL, lw=0.35)
        for j in range(1, l):
            ax.plot([0, L * c], [y0 + j * c, y0 + j * c], color=NEUTRAL, lw=0.35)
        txt(ax, L * c + 0.25, y0 + l * c / 2, f"${L}\\times{l}$", DARK, 13, va="center")
        y = y0 - 0.45
    txt(ax, 13.6, -0.6, "36 carreaux rangés", DARK, 12.5, fontweight="bold")
    txt(ax, 13.6, -1.2, "de 5 façons différentes", DARK, 12.5, fontweight="bold")
    txt(ax, 13.6, -2.3, "diviseurs de 36 :", BLUE, 13, fontweight="bold")
    txt(ax, 13.6, -3.0, "1, 2, 3, 4, 6,", BLUE, 13)
    txt(ax, 13.6, -3.6, "9, 12, 18, 36", BLUE, 13)
    txt(ax, 13.6, -4.7, "ils vont par paires :", NEUTRAL, 11.5)
    txt(ax, 13.6, -5.2, "$1\\times 36$, $2\\times 18$, $3\\times 12$…", NEUTRAL, 11.5)
    ax.set_xlim(-0.3, 18.6)
    ax.set_ylim(y + 0.2, 0.7)
    ax.set_aspect("equal")
    ax.axis("off")
    _save(fig, I("2nd_arithmetique_rectangles.png"))


def crible():
    premiers = [n for n in range(2, 101) if all(n % d for d in range(2, int(n ** 0.5) + 1))]
    fig, ax = new_fig(7.2, 7.6)
    for n in range(1, 101):
        i, j = (n - 1) % 10, (n - 1) // 10
        if n in premiers:
            fc, col, fw = "#d6eafc", BLUE, "bold"
        elif n == 1:
            fc, col, fw = "#f2f3f4", NEUTRAL, "normal"
        else:
            fc, col, fw = "#ffffff", "#aab7b8", "normal"
        ax.add_patch(Rectangle((i, -j), 1, 1, facecolor=fc, edgecolor="#d5d8dc", lw=1))
        txt(ax, i + 0.5, -j + 0.5, str(n), col, 12.5, ha="center", va="center", fontweight=fw)
    txt(ax, 5, 1.35, "Les 25 nombres premiers inférieurs à 100", DARK, 13, ha="center", fontweight="bold")
    txt(ax, 5, -9.55, "on barre les multiples de 2, 3, 5 et 7 (car $7^2 = 49 < 100 < 11^2$)", NEUTRAL, 11,
        ha="center", va="top")
    ax.set_xlim(-0.2, 10.2)
    ax.set_ylim(-10.3, 2.0)
    ax.set_aspect("equal")
    ax.axis("off")
    _save(fig, I("2nd_arithmetique_crible.png"))


def arbre_360():
    fig, ax = new_fig(7.0, 5.0)
    noeuds = {"360": (3.0, 4.0), "2a": (1.6, 3.0), "180": (4.4, 3.0), "2b": (3.0, 2.0), "90": (5.8, 2.0),
              "2c": (4.4, 1.0), "45": (7.2, 1.0), "3a": (5.8, 0.0), "15": (8.6, 0.0), "3b": (7.2, -1.0),
              "5": (10.0, -1.0)}
    aretes = [("360", "2a"), ("360", "180"), ("180", "2b"), ("180", "90"), ("90", "2c"), ("90", "45"), ("45", "3a"),
              ("45", "15"), ("15", "3b"), ("15", "5")]
    for a, b in aretes:
        (x1, y1), (x2, y2) = noeuds[a], noeuds[b]
        ax.plot([x1, x2], [y1, y2], color=NEUTRAL, lw=1.4)
    for k, (x, y) in noeuds.items():
        val = k.rstrip("abc")
        prem = val in ("2", "3", "5")
        ax.add_patch(FancyBboxPatch((x - 0.42, y - 0.28), 0.84, 0.56, boxstyle="round,pad=0.02,rounding_size=0.18",
                                    facecolor="#fdebd0" if prem else LBLUE, edgecolor=ORANGE if prem else BLUE,
                                    lw=1.6, zorder=3))
        txt(ax, x, y, val, ORANGE if prem else DARK, 14, ha="center", va="center", fontweight="bold", zorder=4)
    txt(ax, 0.3, -1.0, "$360 = 2^3 \\times 3^2 \\times 5$", GREEN, 16, fontweight="bold")
    txt(ax, 6.2, 4.0, "en orange : les facteurs premiers", ORANGE, 11)
    ax.set_xlim(0, 10.6)
    ax.set_ylim(-1.6, 4.6)
    ax.set_aspect("equal")
    ax.axis("off")
    _save(fig, I("2nd_arithmetique_arbre.png"))


rectangles_36()
crible()
arbre_360()
