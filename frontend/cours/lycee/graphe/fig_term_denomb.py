# -*- coding: utf-8 -*-
"""Figures : Terminale — Combinatoire et dénombrement."""
from math import comb

from matplotlib.patches import FancyBboxPatch, Polygon

from figlycee import new_fig, _save, txt, I, BLUE, ORANGE, GREEN, DARK, NEUTRAL, RED, LBLUE, LGREEN, LORANGE


def arbre():
    fig, ax = new_fig(8.0, 4.8)
    lettres = "ABC"
    ax.scatter([0], [0], s=30, color=DARK)
    y1s = {"A": 2.0, "B": 0.0, "C": -2.0}
    for l1 in lettres:
        y1 = y1s[l1]
        ax.plot([0.12, 2.0], [0, y1], color=BLUE, lw=1.8)
        txt(ax, 2.25, y1, f"${l1}$", BLUE, 16, ha="center", va="center", fontweight="bold")
        autres = [l for l in lettres if l != l1]
        for k, l2 in enumerate(autres):
            y2 = y1 + (0.5 if k == 0 else -0.5)
            ax.plot([2.5, 4.3], [y1, y2], color=ORANGE, lw=1.6)
            txt(ax, 4.55, y2, f"${l2}$", ORANGE, 15, ha="center", va="center", fontweight="bold")
            txt(ax, 5.2, y2, f"$({l1}\\,;{l2})$", DARK, 13, va="center")
    txt(ax, 2.25, 3.0, "1er choix : 3", BLUE, 12, ha="center")
    txt(ax, 4.55, 3.0, "2e choix : 2", ORANGE, 12, ha="center")
    txt(ax, 3.4, -3.15, "$3 \\times 2 = 6$ couples d’éléments distincts (arrangements)", GREEN, 13, ha="center",
        fontweight="bold")
    ax.set_xlim(-0.3, 7.2)
    ax.set_ylim(-3.6, 3.4)
    ax.set_aspect("equal")
    ax.axis("off")
    _save(fig, I("term_denomb_arbre.png"))


def pascal():
    fig, ax = new_fig(8.2, 4.8)
    N = 6
    for n in range(N + 1):
        for k in range(n + 1):
            x, y = k - n / 2, -n * 0.85
            hl = (n, k) in ((4, 1), (4, 2))
            res = (n, k) == (5, 2)
            fc = LORANGE if hl else (LGREEN if res else "white")
            ec = ORANGE if hl else (GREEN if res else "#c5ced6")
            ax.add_patch(FancyBboxPatch((x - 0.38, y - 0.3), 0.76, 0.6, boxstyle="round,pad=0.04", fc=fc, ec=ec,
                                        lw=1.6 if (hl or res) else 1))
            txt(ax, x, y, f"${comb(n, k)}$", DARK, 13, ha="center", va="center",
                fontweight="bold" if (hl or res) else "normal")
        txt(ax, -N / 2 - 1.3, -n * 0.85, f"$n = {n}$", NEUTRAL, 11.5, ha="center", va="center")
    ax.annotate("", xy=(-0.5 + 0.05, -5 * 0.85 + 0.32), xytext=(-1.0, -4 * 0.85 - 0.3),
                arrowprops=dict(arrowstyle="-|>", color=ORANGE, lw=1.4))
    ax.annotate("", xy=(-0.5 - 0.05, -5 * 0.85 + 0.32), xytext=(0.0, -4 * 0.85 - 0.3),
                arrowprops=dict(arrowstyle="-|>", color=ORANGE, lw=1.4))
    txt(ax, 4.6, -2.0, "relation de Pascal :\n$\\binom{4}{1} + \\binom{4}{2} = \\binom{5}{2}$\n$4 + 6 = 10$", DARK, 13,
        ha="center", va="center")
    ax.set_xlim(-5.0, 6.4)
    ax.set_ylim(-5.8, 0.6)
    ax.set_aspect("equal")
    ax.axis("off")
    _save(fig, I("term_denomb_pascal.png"))


def choix():
    fig, ax = new_fig(9.6, 4.6)

    def boite(x, y, s, fc, ec, w=3.2, h=0.9, fs=12.5):
        ax.add_patch(FancyBboxPatch((x - w / 2, y - h / 2), w, h, boxstyle="round,pad=0.08", fc=fc, ec=ec, lw=1.8))
        txt(ax, x, y, s, DARK, fs, ha="center", va="center")

    def losange(x, y, s):
        ax.add_patch(Polygon([(x, y + 0.6), (x + 1.9, y), (x, y - 0.6), (x - 1.9, y)], closed=True, fc=LORANGE,
                             ec=ORANGE, lw=1.8))
        txt(ax, x, y, s, DARK, 12, ha="center", va="center")

    losange(0, 3.0, "l’ordre compte ?")
    losange(-3.0, 1.0, "répétitions ?")
    boite(3.0, 1.0, "combinaisons\n$n!\\,/\\,(k!\\,(n - k)!)$", LGREEN, GREEN, w=3.4, h=1.0)
    boite(-5.0, -1.0, "$k$-uplets\n$n^k$", LBLUE, BLUE, w=2.6, h=1.0)
    boite(-1.0, -1.0, "arrangements\n$n!\\,/\\,(n - k)!$", LBLUE, BLUE, w=2.8, h=1.0)
    for (x0, y0, x1, y1, lab, col) in ((-1.9, 3.0, -3.0, 1.6, "oui", GREEN), (1.9, 3.0, 3.0, 1.45, "non", RED),
                                       (-4.9, 1.0, -5.0, -0.45, "oui", GREEN), (-1.1, 1.0, -1.0, -0.45, "non", RED)):
        ax.plot([x0, x1], [y0, y0], color=NEUTRAL, lw=1.4)
        ax.annotate("", xy=(x1, y1), xytext=(x1, y0), arrowprops=dict(arrowstyle="-|>", color=NEUTRAL, lw=1.4))
        txt(ax, (x0 + x1) / 2, y0 + 0.1, lab, col, 12, ha="center", va="bottom", fontweight="bold")
    txt(ax, 3.0, -0.3, "(tirage simultané,\nsous-ensemble)", NEUTRAL, 11, ha="center", va="top")
    txt(ax, -1.0, -1.85, "permutations si $k = n$ : $n!$", NEUTRAL, 11, ha="center", va="top")
    ax.set_xlim(-6.6, 5.0)
    ax.set_ylim(-2.4, 3.9)
    ax.set_aspect("equal")
    ax.axis("off")
    _save(fig, I("term_denomb_choix.png"))


arbre()
pascal()
choix()
