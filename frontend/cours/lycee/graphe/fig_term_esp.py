# -*- coding: utf-8 -*-
"""Figures : Terminale — Géométrie dans l'espace (vecteurs, droites, plans, repères)."""
import numpy as np
from matplotlib.patches import Polygon

from figlycee import new_fig, _save, txt, I, BLUE, ORANGE, GREEN, DARK, NEUTRAL, RED, PURPLE

K, ANG = 0.5, np.radians(30)


def pr(p):
    x, y, z = p
    return np.array([x + K * y * np.cos(ANG), z + K * y * np.sin(ANG)])


def seg(ax, p, q, col=DARK, lw=1.8, ls="-"):
    a, b = pr(p), pr(q)
    ax.plot([a[0], b[0]], [a[1], b[1]], color=col, lw=lw, ls=ls)


def fleche(ax, p, q, col, lw=2.6):
    a, b = pr(p), pr(q)
    ax.annotate("", xy=b, xytext=a, arrowprops=dict(arrowstyle="-|>", color=col, lw=lw, mutation_scale=18,
                                                    shrinkA=0, shrinkB=0))


def nom(ax, p, s, d=(0, 0), col=DARK, fs=14):
    a = pr(p)
    txt(ax, a[0] + d[0], a[1] + d[1], f"${s}$", col, fs, ha="center", va="center", fontweight="bold")


CUBE = {"A": (0, 0, 0), "B": (3, 0, 0), "C": (3, 3, 0), "D": (0, 3, 0),
        "E": (0, 0, 3), "F": (3, 0, 3), "G": (3, 3, 3), "H": (0, 3, 3)}
ARETES = ["AB", "BC", "CD", "DA", "EF", "FG", "GH", "HE", "AE", "BF", "CG", "DH"]
CACHEES = {"CD", "DA", "DH"}
DEC = {"A": (-0.3, -0.3), "B": (0.3, -0.3), "C": (0.35, -0.1), "D": (-0.35, 0.05), "E": (-0.35, 0.1),
       "F": (0.3, 0.2), "G": (0.3, 0.25), "H": (-0.3, 0.25)}


def cube(ax, exclure=()):
    for a in ARETES:
        if a in exclure:
            continue
        seg(ax, CUBE[a[0]], CUBE[a[1]], NEUTRAL, 1.5, "--" if a in CACHEES else "-")
    for s, p in CUBE.items():
        nom(ax, p, s, DEC[s])


def fin(ax, xl=(-1.0, 5.4), yl=(-1.2, 4.4)):
    ax.set_xlim(*xl)
    ax.set_ylim(*yl)
    ax.set_aspect("equal")
    ax.axis("off")


def repere_cube():
    fig, ax = new_fig(7.0, 5.6)
    cube(ax)
    A = CUBE["A"]
    fleche(ax, A, CUBE["B"], BLUE)
    fleche(ax, A, CUBE["D"], GREEN)
    fleche(ax, A, CUBE["E"], ORANGE)
    fleche(ax, A, CUBE["G"], PURPLE, lw=2.2)
    txt(ax, 1.5, -0.4, "$\\vec{\\imath}$", BLUE, 16, ha="center", va="top", fontweight="bold")
    a = pr((0, 1.5, 0))
    txt(ax, a[0] + 0.45, a[1] - 0.12, "$\\vec{\\jmath}$", GREEN, 16, ha="center", va="center", fontweight="bold")
    txt(ax, -0.15, 1.5, "$\\vec{k}$", ORANGE, 16, ha="right", va="center", fontweight="bold")
    txt(ax, 3.3, 4.0, "$\\overrightarrow{AG}$", PURPLE, 14, ha="center", va="bottom", fontweight="bold")
    txt(ax, 2.0, -1.0, "$\\vec{\\imath} = \\overrightarrow{AB}$, $\\vec{\\jmath} = \\overrightarrow{AD}$, $\\vec{k} = \\overrightarrow{AE}$ et $\\overrightarrow{AG} = \\vec{\\imath} + \\vec{\\jmath} + \\vec{k}$\ndans le repère $(A\\,;\\vec{\\imath}, \\vec{\\jmath}, \\vec{k})$ : $G(1\\,;1\\,;1)$, $C(1\\,;1\\,;0)$, $H(0\\,;1\\,;1)$",
        DARK, 12, ha="center", va="top")
    fin(ax, (-2.4, 5.6), (-1.9, 4.6))
    _save(fig, I("term_esp_repere.png"))


def coplanaires():
    fig, ax = new_fig(7.6, 5.0)
    P = [(0, 0, 0), (5, 0, 0), (5, 4, 0), (0, 4, 0)]
    ax.add_patch(Polygon([pr(p) for p in P], closed=True, fc="#e8f4fd", ec=BLUE, lw=1.5))
    O = (1, 1, 0)
    u, v = (1.6, 0, 0), (0.3, 1.8, 0)
    w = tuple(1.2 * a + 1.0 * b for a, b in zip(u, v))
    add = lambda p, q: tuple(a + b for a, b in zip(p, q))  # noqa: E731
    fleche(ax, O, add(O, u), BLUE)
    fleche(ax, O, add(O, v), GREEN)
    fleche(ax, O, add(O, w), ORANGE)
    fleche(ax, O, add(O, (0.4, 0.6, 2.2)), RED)
    nom(ax, add(O, (0.9, -0.05, 0)), "\\vec{u}", (0, -0.3), BLUE)
    nom(ax, add(O, (0.15, 1.0, 0)), "\\vec{v}", (-0.35, 0), GREEN)
    nom(ax, add(O, w), "\\vec{w} = 1{,}2\\vec{u} + \\vec{v}", (0.4, 0.3), ORANGE, 13)
    nom(ax, add(O, (0.4, 0.6, 2.2)), "\\vec{t}", (0.25, 0.15), RED)
    txt(ax, 6.4, 0.7, "plan $\\mathcal{P}$", BLUE, 13)
    txt(ax, 3.3, -0.9, "$\\vec{u}, \\vec{v}, \\vec{w}$ coplanaires ; $\\vec{t}$ ne l’est pas avec $\\vec{u}$ et $\\vec{v}$", DARK, 12.5,
        ha="center", va="top")
    fin(ax, (-0.5, 7.6), (-1.5, 4.0))
    _save(fig, I("term_esp_coplanaires.png"))


def positions():
    fig, ax = new_fig(7.4, 5.8)
    face = [CUBE[s] for s in "ABCD"]
    ax.add_patch(Polygon([pr(p) for p in face], closed=True, fc="#e8f4fd", ec="none"))
    face = [CUBE[s] for s in "EFGH"]
    ax.add_patch(Polygon([pr(p) for p in face], closed=True, fc="#e8f4fd", ec="none"))
    cube(ax, exclure=("AB", "HG", "GH", "CG"))
    seg(ax, CUBE["A"], CUBE["B"], BLUE, 3)
    seg(ax, CUBE["H"], CUBE["G"], BLUE, 3)
    seg(ax, CUBE["C"], CUBE["G"], RED, 3)
    txt(ax, 2.3, -1.2, "$(AB)$ et $(HG)$ : parallèles ; $(AB)$ et $(CG)$ : non coplanaires\nfaces $ABCD$ et $EFGH$ : plans parallèles",
        DARK, 12, ha="center", va="top")
    fin(ax, (-1.0, 5.6), (-2.3, 4.6))
    _save(fig, I("term_esp_positions.png"))


repere_cube()
coplanaires()
positions()
