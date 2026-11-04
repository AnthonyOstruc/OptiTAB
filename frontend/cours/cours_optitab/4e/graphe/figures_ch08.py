# -*- coding: utf-8 -*-
"""Figures du chapitre 8 (grandeurs composées et unités) — 4ème OptiTAB."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fig4e import (new_fig, _save, tableau, graphe, pave, BLUE, ORANGE, GREEN, DARK, NEUTRAL,
                   DIR_COURS, DIR_EXOS)
import numpy as np
from matplotlib.patches import Rectangle, Polygon, FancyArrowPatch

C = lambda f: os.path.join(DIR_COURS, f)  # noqa: E731
X = lambda f: os.path.join(DIR_EXOS, f)   # noqa: E731
LBLUE, LORANGE, LGREEN = "#d6eafc", "#fdebd0", "#e8f5e9"
PURP = "#8e44ad"


def triangle_vitesse(path):
    fig, ax = new_fig(8.6, 4.2)
    T = np.array([[0, 0], [4, 0], [2, 3.2]])
    ax.add_patch(Polygon(T, closed=True, facecolor=LBLUE, edgecolor=BLUE, lw=2.4))
    ax.plot([0.75, 3.25], [1.2, 1.2], lw=2, color=BLUE)
    ax.plot([2, 2], [0, 1.2], lw=2, color=BLUE)
    ax.text(2, 1.95, "$d$", ha="center", va="center", fontsize=24, color=ORANGE)
    ax.text(1.2, 0.55, "$v$", ha="center", va="center", fontsize=22, color=GREEN)
    ax.text(2.8, 0.55, "$t$", ha="center", va="center", fontsize=22, color=PURP)
    ax.text(4.8, 2.4, "$d = v \\times t$", fontsize=16, color=ORANGE)
    ax.text(4.8, 1.5, "$v = \\dfrac{d}{t}$", fontsize=16, color=GREEN)
    ax.text(4.8, 0.45, "$t = \\dfrac{d}{v}$", fontsize=16, color=PURP)
    ax.text(2, -0.6, "on cache la grandeur cherchée", ha="center", fontsize=11, color=DARK)
    ax.set_xlim(-0.3, 8.0)
    ax.set_ylim(-1.0, 3.5)
    ax.set_aspect("equal")
    ax.axis("off")
    _save(fig, path)


triangle_vitesse(C("grandeurs_4e_triangle.png"))
triangle_vitesse(X("grandeurs_4e_triangle_solution.png"))

tableau(C("grandeurs_4e_volumes.png"),
        [["", "", "m³", "", "", "dm³", "", "", "cm³"],
         ["", "", "", "", "", "L", "dL", "cL", "mL"],
         ["", "", "2", "5", "0", "0", "", "", ""]],
        larg_col=[1.05] * 9, entete_lig=False, entete_col=True, surligne=[(0, 5), (1, 5)],
        titre="1 dm³ = 1 L ; 1 cm³ = 1 mL ; 2,5 m³ = 2 500 dm³ = 2 500 L")


def durees(path):
    fig, ax = new_fig(10.5, 2.6)
    ax.annotate("", xy=(2.15, 0), xytext=(-0.05, 0), arrowprops=dict(arrowstyle="->", lw=1.6,
                                                                     color=NEUTRAL))
    for k in range(0, 9):
        x = k * 0.25
        big = k % 4 == 0
        ax.plot([x, x], [-0.06 if not big else -0.1, 0.06 if not big else 0.1], lw=1.4 if big else 1,
                color=NEUTRAL)
    for x, t in [(0, "0 h"), (1, "1 h"), (2, "2 h")]:
        ax.text(x, -0.18, t, ha="center", va="top", fontsize=12, color=DARK)
    for x, t in [(0.25, "15 min"), (0.5, "30 min"), (0.75, "45 min")]:
        ax.text(x, 0.14, t, ha="center", va="bottom", fontsize=10, color=NEUTRAL)
    ax.scatter([1.25], [0], s=80, color=ORANGE, zorder=5)
    ax.text(1.25, 0.18, "1,25 h = 1 h 15 min", ha="center", va="bottom", fontsize=12.5,
            color=ORANGE, fontweight="bold")
    ax.scatter([1.75], [0], s=80, color=GREEN, zorder=5)
    ax.text(1.75, 0.3, "1,75 h = 1 h 45 min", ha="center", va="bottom", fontsize=12.5,
            color=GREEN, fontweight="bold")
    ax.set_xlim(-0.15, 2.25)
    ax.set_ylim(-0.42, 0.5)
    ax.axis("off")
    _save(fig, path)


durees(C("grandeurs_4e_durees.png"))


def trajet(path, solution=False):
    pts = [(0, 0), (1, 60), (1.5, 60), (3, 150)]
    def extra(ax):
        xs, ys = zip(*pts)
        ax.plot(xs, ys, lw=2.6, color=BLUE, zorder=3)
        ax.scatter(xs, ys, s=40, color=BLUE, zorder=4)
        if solution:
            ax.text(0.15, 42, "60 km/h", color=GREEN, fontsize=12.5, fontweight="bold")
            ax.text(1.02, 68, "arrêt\n30 min", color=ORANGE, fontsize=12, fontweight="bold")
            ax.text(2.35, 95, "60 km/h", color=GREEN, fontsize=12.5, fontweight="bold")
            ax.plot([0, 3], [0, 150], lw=1.6, color=PURP, ls="--")
            ax.text(0.9, 88, "vitesse moyenne\nsur 3 h : 50 km/h", color=PURP, fontsize=11.5,
                    fontweight="bold", ha="right")
    graphe(path, curves=[], xb=(-0.2, 3.4), yb=(-12, 170), xt=0.5, yt=20,
           xlabel="durée (h)", ylabel="distance (km)", extra=extra, w=8.4, h=5.4)


trajet(X("grandeurs_4e_trajet.png"))
trajet(X("grandeurs_4e_trajet_solution.png"), solution=True)


def aquarium(path):
    from fig4e import _proj, _edges, dot_label
    L, P, H, h = 8.0, 3.5, 4.5, 4.0
    fig, ax = new_fig(7.6, 5.2)
    V = {}
    pts3 = {"A": (0, 0, 0), "B": (L, 0, 0), "C": (L, 0, H), "D": (0, 0, H), "E": (0, P, 0),
            "F": (L, P, 0), "G": (L, P, H), "H": (0, P, H)}
    for k3, c in pts3.items():
        V[k3] = _proj(*c)
    W = {k3: _proj(c[0], c[1], h if c[2] else 0) for k3, c in pts3.items()}
    ax.add_patch(Polygon([W["A"], W["B"], W["C"], W["D"]], closed=True, facecolor=LBLUE,
                         edgecolor="none", alpha=0.9))
    ax.add_patch(Polygon([W["D"], W["C"], W["G"], W["H"]], closed=True, facecolor="#b9dcf7",
                         edgecolor=BLUE, lw=1))
    edges = [("A", "B"), ("B", "C"), ("C", "D"), ("D", "A"), ("E", "F"), ("F", "G"), ("G", "H"),
             ("H", "E"), ("A", "E"), ("B", "F"), ("C", "G"), ("D", "H")]
    _edges(ax, V, edges, hidden_edges=[("E", "F"), ("H", "E"), ("A", "E")], color=DARK)
    ax.text((V["A"][0] + V["B"][0]) / 2, -0.55, "80 cm", ha="center", fontsize=12.5, color=DARK)
    ax.text(V["B"][0] + 1.0, 0.45, "35 cm", fontsize=12.5, color=DARK)
    ax.text(-0.3, H / 2, "45 cm", ha="right", va="center", fontsize=12.5, color=DARK)
    ax.text(L / 2, h / 2, "eau : hauteur 40 cm", ha="center", va="center", fontsize=12,
            color=BLUE, fontweight="bold")
    ax.set_xlim(-1.8, L + 2.6)
    ax.set_ylim(-1.0, H + 1.5)
    ax.set_aspect("equal")
    ax.axis("off")
    _save(fig, path)


aquarium(X("grandeurs_4e_aquarium.png"))


def cubes(path):
    fig, ax = new_fig(10.0, 3.6)
    data = [("fer", "7,8 kg", "#9aa5ad"), ("aluminium", "2,7 kg", "#d5dbe0"), ("bois", "600 g", "#d4a373")]
    for i, (nom, m, fc) in enumerate(data):
        x0 = i * 3.6
        f = [(x0, 0), (x0 + 2, 0), (x0 + 2, 2), (x0, 2)]
        top = [(x0, 2), (x0 + 2, 2), (x0 + 2.6, 2.5), (x0 + 0.6, 2.5)]
        side = [(x0 + 2, 0), (x0 + 2.6, 0.5), (x0 + 2.6, 2.5), (x0 + 2, 2)]
        for poly, a in ((f, 1), (top, 0.75), (side, 0.6)):
            ax.add_patch(Polygon(poly, closed=True, facecolor=fc, edgecolor=DARK, lw=1.4, alpha=a))
        ax.text(x0 + 1, 1, m, ha="center", va="center", fontsize=13, color=DARK, fontweight="bold")
        ax.text(x0 + 1.3, -0.45, nom, ha="center", va="top", fontsize=12.5, color=DARK)
    ax.text(5.0, 3.0, "trois cubes de 10 cm d'arête", ha="center", fontsize=12.5, color=BLUE,
            fontweight="bold")
    ax.set_xlim(-0.3, 10.3)
    ax.set_ylim(-1.1, 3.4)
    ax.set_aspect("equal")
    ax.axis("off")
    _save(fig, path)


cubes(X("grandeurs_4e_cubes.png"))


def aller_retour(path):
    fig, ax = new_fig(9.6, 2.6)
    ax.scatter([0, 10], [0, 0], s=80, color=DARK, zorder=5)
    ax.text(0, -0.5, "A", ha="center", fontsize=13, color=DARK, fontweight="bold")
    ax.text(10, -0.5, "B", ha="center", fontsize=13, color=DARK, fontweight="bold")
    ax.add_patch(FancyArrowPatch((0.2, 0.35), (9.8, 0.35), arrowstyle="-|>", mutation_scale=16, lw=2,
                                 color=BLUE))
    ax.text(5, 0.55, "aller : 30 km à 20 km/h", ha="center", fontsize=12.5, color=BLUE,
            fontweight="bold")
    ax.add_patch(FancyArrowPatch((9.8, -0.25), (0.2, -0.25), arrowstyle="-|>", mutation_scale=16,
                                 lw=2, color=ORANGE))
    ax.text(5, -0.95, "retour : 30 km à 30 km/h", ha="center", fontsize=12.5, color=ORANGE,
            fontweight="bold")
    ax.set_xlim(-0.8, 10.8)
    ax.set_ylim(-1.4, 1.1)
    ax.axis("off")
    _save(fig, path)


aller_retour(X("grandeurs_4e_aller_retour.png"))


def orage(path):
    fig, ax = new_fig(9.0, 3.6)
    ax.plot([0, 10], [0, 0], lw=2, color=GREEN)
    ax.add_patch(Polygon([(0.3, 0), (0.9, 0), (0.6, 0.9)], closed=True, facecolor="#e8d8b8",
                         edgecolor=DARK))
    ax.text(0.6, -0.4, "observateur", ha="center", fontsize=11.5, color=DARK)
    cloud_x = 8.5
    for dx, dy, rr in [(0, 0, 0.6), (0.6, 0.15, 0.55), (-0.6, 0.1, 0.5), (0.2, 0.45, 0.5)]:
        ax.add_patch(plt_circle((cloud_x + dx, 2.4 + dy), rr))
    ax.plot([8.4, 8.1, 8.5, 8.2], [1.9, 1.2, 1.2, 0.3], lw=2.6, color="#f1c40f")
    ax.add_patch(FancyArrowPatch((7.8, 1.0), (1.2, 0.6), arrowstyle="-|>", mutation_scale=16, lw=1.8,
                                 color=ORANGE, ls="--"))
    ax.text(4.5, 1.25, "son : 340 m/s", ha="center", fontsize=12.5, color=ORANGE, fontweight="bold")
    ax.text(4.5, 2.4, "lumière : quasi instantanée", ha="center", fontsize=12.5, color="#b7950b",
            fontweight="bold")
    ax.set_xlim(-0.3, 10.2)
    ax.set_ylim(-0.8, 3.3)
    ax.set_aspect("equal")
    ax.axis("off")
    _save(fig, path)


def plt_circle(c, r):
    from matplotlib.patches import Circle
    return Circle(c, r, facecolor="#95a5a6", edgecolor="#7f8c8d")


orage(X("grandeurs_4e_orage.png"))


def piscine(path):
    pave(path, L=6.0, P=2.4, H=1.2, noms="ABCDEFGH",
         measures=[("AB", "10 m"), ("AD", "1,5 m", dict(side=1, offset=0.55)),
                   ("BF", "4 m", dict(side=-1, offset=0.45))], w=7.6, h=4.2)


piscine(X("grandeurs_4e_piscine.png"))
