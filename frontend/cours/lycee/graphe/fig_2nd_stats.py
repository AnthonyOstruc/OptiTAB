# -*- coding: utf-8 -*-
"""Figures : Seconde — Information chiffrée et statistique descriptive."""
import numpy as np
from matplotlib.patches import FancyBboxPatch

from figlycee import new_fig, _save, txt, I, BLUE, ORANGE, GREEN, DARK, NEUTRAL, RED, LBLUE, LGREEN, LORANGE

SERIE = [4, 7, 8, 9, 10, 11, 12, 12, 14, 15, 19]


def boite_txt(ax, x, y, s, fc, ec, w=1.6, h=0.9, fs=18):
    ax.add_patch(FancyBboxPatch((x - w / 2, y - h / 2), w, h, boxstyle="round,pad=0.08", fc=fc, ec=ec, lw=2))
    txt(ax, x, y, s, DARK, fs, ha="center", va="center", fontweight="bold")


def evolutions():
    fig, ax = new_fig(9.6, 3.6)
    xs = [0, 4.6, 9.2]
    for x, v, fc, ec in zip(xs, ["$80$", "$100$", "$80$"], [LBLUE, LGREEN, LBLUE], [BLUE, GREEN, BLUE]):
        boite_txt(ax, x, 0, v, fc, ec)
    for (a, b), (lab, sous, col) in zip(((0, 4.6), (4.6, 9.2)),
                                        (("$\\times 1{,}25$", "hausse de $25\\,\\%$", GREEN),
                                         ("$\\times 0{,}8$", "baisse de $20\\,\\%$", ORANGE))):
        ax.annotate("", xy=(b - 1.0, 0), xytext=(a + 1.0, 0),
                    arrowprops=dict(arrowstyle="-|>", color=col, lw=2.4, mutation_scale=20))
        txt(ax, (a + b) / 2, 0.35, lab, col, 16, ha="center", va="bottom", fontweight="bold")
        txt(ax, (a + b) / 2, -0.35, sous, col, 12.5, ha="center", va="top")
    txt(ax, 4.6, -1.35, "coefficient multiplicateur $CM = 1 + t$  ;  $1{,}25 \\times 0{,}8 = 1$ : évolutions réciproques",
        DARK, 12.5, ha="center", va="top")
    ax.set_xlim(-1.2, 10.4)
    ax.set_ylim(-2.1, 1.2)
    ax.set_aspect("equal")
    ax.axis("off")
    _save(fig, I("2nd_stats_evolutions.png"))


def boite():
    fig, ax = new_fig(9.6, 3.8)
    ax.plot([0, 21], [0, 0], color=NEUTRAL, lw=1.3)
    for k in range(0, 21):
        ax.plot([k, k], [-0.08, 0.08], color=NEUTRAL, lw=1)
        if k % 2 == 0:
            txt(ax, k, -0.2, f"${k}$", DARK, 11, ha="center", va="top")
    # valeurs de la série
    vus = {}
    for v in SERIE:
        n = vus.get(v, 0)
        vus[v] = n + 1
        ax.scatter([v], [2.35 + 0.32 * n], s=40, color=BLUE, zorder=5)
    mn, q1, me, q3, mx = 4, 8, 11, 14, 19
    y0, h = 1.0, 0.8
    ax.add_patch(FancyBboxPatch((q1, y0 - h / 2), q3 - q1, h, boxstyle="square,pad=0", fc=LORANGE, ec=ORANGE, lw=2))
    ax.plot([me, me], [y0 - h / 2, y0 + h / 2], color=RED, lw=3)
    ax.plot([mn, q1], [y0, y0], color=ORANGE, lw=2)
    ax.plot([q3, mx], [y0, y0], color=ORANGE, lw=2)
    for v in (mn, mx):
        ax.plot([v, v], [y0 - 0.25, y0 + 0.25], color=ORANGE, lw=2)
    for v, lab, col in ((mn, "min", DARK), (q1, "$Q_1$", ORANGE), (me, "Me", RED), (q3, "$Q_3$", ORANGE),
                        (mx, "max", DARK)):
        ax.plot([v, v], [0.08, y0 - h / 2 if v in (q1, me, q3) else y0 - 0.25], color=NEUTRAL, lw=0.8, ls=":")
        txt(ax, v, -0.75, lab, col, 13, ha="center", va="top", fontweight="bold")
    ax.annotate("", xy=(q3, 1.75), xytext=(q1, 1.75), arrowprops=dict(arrowstyle="<->", color=GREEN, lw=1.6))
    txt(ax, (q1 + q3) / 2 + 3.2, 1.75, "écart interquartile $Q_3 - Q_1 = 6$", GREEN, 12, va="center")
    ax.set_xlim(-0.6, 21.6)
    ax.set_ylim(-1.4, 3.3)
    ax.axis("off")
    _save(fig, I("2nd_stats_boite.png"))


def dispersion():
    fig, ax = new_fig(9.6, 3.8)
    A = [9, 10, 10, 11, 11, 11, 12, 12, 13]
    B = [4, 6, 8, 10, 11, 13, 14, 16, 17]
    for y, S, col, nom in ((2.2, A, BLUE, "série A"), (0, B, ORANGE, "série B")):
        ax.plot([2, 19], [y, y], color=NEUTRAL, lw=1.2)
        for k in range(2, 20):
            ax.plot([k, k], [y - 0.06, y + 0.06], color=NEUTRAL, lw=0.8)
        for k in (4, 8, 12, 16):
            txt(ax, k, y - 0.15, f"${k}$", DARK, 10, ha="center", va="top")
        vus = {}
        for v in S:
            n = vus.get(v, 0)
            vus[v] = n + 1
            ax.scatter([v], [y + 0.3 + 0.3 * n], s=40, color=col, zorder=5)
        ax.plot([11, 11], [y - 0.1, y + 1.3], color=RED, lw=1.6, ls="--")
        s = np.std(S)
        txt(ax, 1.6, y + 0.35, nom, col, 13, ha="right", va="center", fontweight="bold")
        txt(ax, 19.6, y + 0.35, f"$\\sigma \\approx {s:.1f}$".replace(".", "{,}"), col, 13, va="center",
            fontweight="bold")
    txt(ax, 11, 3.75, "même moyenne $\\bar{x} = 11$", RED, 12.5, ha="center")
    ax.set_xlim(-0.6, 22.2)
    ax.set_ylim(-0.7, 4.1)
    ax.axis("off")
    _save(fig, I("2nd_stats_dispersion.png"))


evolutions()
boite()
dispersion()
