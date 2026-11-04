# -*- coding: utf-8 -*-
"""Figures du chapitre 7 (proportionnalité et pourcentages) — 4ème OptiTAB."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fig4e import (new_fig, _save, tableau, graphe, BLUE, ORANGE, GREEN, DARK, NEUTRAL,
                   DIR_COURS, DIR_EXOS)
import numpy as np
from matplotlib.patches import Rectangle, Polygon, FancyArrowPatch

C = lambda f: os.path.join(DIR_COURS, f)  # noqa: E731
X = lambda f: os.path.join(DIR_EXOS, f)   # noqa: E731
LBLUE, LORANGE, LGREEN = "#d6eafc", "#fdebd0", "#e8f5e9"
PURP = "#8e44ad"


def grille(ax, x0, y0, titre, lignes, larg=1.35, haut=0.62, col_titre=DARK, vert=()):
    ax.text(x0, y0 + 0.25, titre, fontsize=12.5, color=col_titre, fontweight="bold")
    for i, r in enumerate(lignes):
        x = x0
        for j, txt in enumerate(r):
            w = 2.4 if j == 0 else larg
            fc = "#e8f4fd" if j == 0 else ("#e8f5e9" if (i, j) in vert else "white")
            ax.add_patch(Rectangle((x, y0 - (i + 1) * haut), w, haut, facecolor=fc,
                                   edgecolor=BLUE, lw=1.2))
            ax.text(x + w / 2, y0 - (i + 0.5) * haut, txt, ha="center", va="center", fontsize=12,
                    color=GREEN if (i, j) in vert else DARK)
            x += w


def quatre_tableaux(path):
    fig, ax = new_fig(10.5, 6.2)
    T = [("Tableau A : masse et prix de cerises", [["Masse (kg)", "2", "5", "8"],
                                                   ["Prix (€)", "7", "17,5", "28"]]),
         ("Tableau B : âge et taille d'un enfant", [["Âge (ans)", "2", "6", "10"],
                                                     ["Taille (cm)", "86", "116", "138"]]),
         ("Tableau C : côté et périmètre d'un carré", [["Côté (cm)", "1,5", "4", "7"],
                                                        ["Périmètre (cm)", "6", "16", "28"]]),
         ("Tableau D : côté et aire d'un carré", [["Côté (cm)", "1", "3", "5"],
                                                   ["Aire (cm²)", "1", "9", "25"]])]
    for k, (t, l) in enumerate(T):
        grille(ax, (k % 2) * 7.0, -(k // 2) * 2.4, t, l)
    ax.set_xlim(-0.2, 13.8)
    ax.set_ylim(-4.0, 0.7)
    ax.set_aspect("equal")
    ax.axis("off")
    _save(fig, path)


quatre_tableaux(X("proportionnalite_4e_tableaux.png"))


def produit_croix(path):
    fig, ax = new_fig(7.6, 3.2)
    grille(ax, 0, 0, "", [["Cahiers", "6", "9"], ["Prix (€)", "9,60", "?"]], larg=1.8)
    ax.text(0, 0.4, "Quatrième proportionnelle : ? = 9 × 9,60 : 6 = 14,40 €", fontsize=12.5,
            color=GREEN, fontweight="bold")
    ax.plot([2.4 + 0.9, 2.4 + 1.8 + 0.9], [-0.31, -0.93], lw=2, color=ORANGE)
    ax.plot([2.4 + 0.9, 2.4 + 1.8 + 0.9], [-0.93, -0.31], lw=2, color=BLUE, ls="--")
    ax.text(6.4, -0.62, "produit en croix :\n6 × ? = 9 × 9,60", fontsize=11.5, color=ORANGE,
            va="center")
    ax.set_xlim(-0.2, 9.4)
    ax.set_ylim(-1.5, 0.9)
    ax.set_aspect("equal")
    ax.axis("off")
    _save(fig, path)


produit_croix(C("proportionnalite_4e_produit_croix.png"))

graphe(C("proportionnalite_4e_graphique.png"),
       curves=[(lambda m: 3.5 * m, 0, 6, BLUE), (lambda m: 2 * m + 5, 0, 6, ORANGE)],
       points=[("", 0, 0, BLUE), ("", 0, 5, ORANGE)],
       extra=lambda ax: (ax.text(4.2, 19.5, "proportionnel : $y = 3{,}5x$\n(droite passant par l'origine)",
                                 color=BLUE, fontsize=11.5, fontweight="bold", ha="right"),
                         ax.text(5.9, 12.2, "non proportionnel :\n$y = 2x + 5$", color=ORANGE,
                                 fontsize=11.5, fontweight="bold", ha="right", va="top")),
       xb=(-0.5, 6.8), yb=(-2, 23), xt=1, yt=5, xlabel="$x$", ylabel="$y$", w=8.2, h=5.0)


def evolution(path, depart=100, taux=20, unite="%", titre=None):
    fig, ax = new_fig(9.5, 3.0)
    ax.add_patch(Rectangle((0, 1.2), 5, 0.8, facecolor=LBLUE, edgecolor=BLUE, lw=1.8))
    ax.text(2.5, 1.6, "prix initial : 100 %", ha="center", va="center", fontsize=12, color=BLUE,
            fontweight="bold")
    ax.add_patch(Rectangle((0, 0), 5, 0.8, facecolor=LBLUE, edgecolor=BLUE, lw=1.8))
    ax.add_patch(Rectangle((5, 0), 1, 0.8, facecolor=LORANGE, edgecolor=ORANGE, lw=1.8))
    ax.text(2.5, 0.4, "100 %", ha="center", va="center", fontsize=12, color=BLUE, fontweight="bold")
    ax.text(5.5, 0.4, "+20 %", ha="center", va="center", fontsize=11, color=ORANGE,
            fontweight="bold")
    ax.text(6.3, 0.4, "→ 120 % = × 1,20", ha="left", va="center", fontsize=12.5, color=GREEN,
            fontweight="bold")
    ax.text(6.3, 1.6, "baisse de 20 % → 80 % = × 0,80", ha="left", va="center", fontsize=12.5,
            color=PURP, fontweight="bold")
    ax.set_xlim(-0.2, 12.2)
    ax.set_ylim(-0.2, 2.2)
    ax.set_aspect("equal")
    ax.axis("off")
    _save(fig, path)


evolution(C("proportionnalite_4e_evolution.png"))

graphe(X("proportionnalite_4e_graphes.png"),
       curves=[(lambda m: 2.4 * m, 0, 7.5, BLUE), (lambda m: 1.5 * m + 6, 0, 7.5, ORANGE),
               (lambda m: 0.35 * m * m, 0, 7.5, GREEN)],
       extra=lambda ax: (ax.text(2.6, 4.4, "$\\mathcal{G}_1$", color=BLUE, fontsize=15),
                         ax.text(1.4, 9.4, "$\\mathcal{G}_2$", color=ORANGE, fontsize=15),
                         ax.text(4.4, 4.2, "$\\mathcal{G}_3$", color=GREEN, fontsize=15)),
       points=[("A(5 ; 12)", 5, 12, BLUE)],
       xb=(-0.5, 8.2), yb=(-1.5, 21), xt=1, yt=2, xlabel="masse (kg)", ylabel="prix (€)",
       w=8.4, h=5.6)


def plan(path):
    fig, ax = new_fig(8.6, 5.6)
    # échelle 1/100 : 1 cm sur le plan = 1 m ; dessin en « cm de plan »
    ax.add_patch(Rectangle((0, 0), 10.4, 6.2, facecolor="white", edgecolor=DARK, lw=3))
    ax.add_patch(Rectangle((0, 0), 6.2, 4.5, facecolor=LBLUE, edgecolor=DARK, lw=2))
    ax.add_patch(Rectangle((6.2, 0), 4.2, 3.5, facecolor=LORANGE, edgecolor=DARK, lw=2))
    ax.add_patch(Rectangle((6.2, 3.5), 4.2, 2.7, facecolor=LGREEN, edgecolor=DARK, lw=2))
    ax.add_patch(Rectangle((0, 4.5), 6.2, 1.7, facecolor="#f2f2f2", edgecolor=DARK, lw=2))
    ax.text(3.1, 2.25, "séjour", ha="center", va="center", fontsize=13, color=BLUE, fontweight="bold")
    ax.text(8.3, 1.75, "chambre", ha="center", va="center", fontsize=12.5, color=ORANGE,
            fontweight="bold")
    ax.text(8.3, 4.85, "cuisine", ha="center", va="center", fontsize=12.5, color=GREEN,
            fontweight="bold")
    ax.text(3.1, 5.35, "entrée", ha="center", va="center", fontsize=11.5, color=DARK)
    for (x1, x2, y, t) in [(0, 6.2, -0.45, "6,2 cm"), (6.2, 10.4, -0.45, "4,2 cm")]:
        ax.annotate("", xy=(x2, y), xytext=(x1, y), arrowprops=dict(arrowstyle="<->", lw=1.2))
        ax.text((x1 + x2) / 2, y - 0.15, t, ha="center", va="top", fontsize=11.5, color=DARK)
    for (y1, y2, x, t) in [(0, 4.5, -0.45, "4,5 cm"), (0, 3.5, 10.85, "3,5 cm")]:
        ax.annotate("", xy=(x, y2), xytext=(x, y1), arrowprops=dict(arrowstyle="<->", lw=1.2))
        ax.text(x + (-0.15 if x < 0 else 0.15), (y1 + y2) / 2, t, ha="right" if x < 0 else "left",
                va="center", fontsize=11.5, color=DARK, rotation=90)
    ax.text(5.2, 6.6, "Plan à l'échelle $\\frac{1}{100}$", ha="center", fontsize=13, color=DARK,
            fontweight="bold")
    ax.set_xlim(-1.5, 12.0)
    ax.set_ylim(-1.4, 7.1)
    ax.set_aspect("equal")
    ax.axis("off")
    _save(fig, path)


plan(X("proportionnalite_4e_plan.png"))

graphe(X("proportionnalite_4e_essence_solution.png"),
       curves=[(lambda v: 1.85 * v, 0, 58, BLUE, ("prix $= 1{,}85 \\times$ volume", 12))],
       points=[("(40 ; 74)", 40, 74, GREEN), ("(55 ; 101,75)", 55, 101.75, GREEN)],
       segments=[((40, 0), (40, 74), dict(color=GREEN)), ((0, 74), (40, 74), dict(color=GREEN))],
       xb=(-3, 62), yb=(-6, 115), xt=10, yt=20, xlabel="volume (L)", ylabel="prix (€)",
       w=8.2, h=5.4)


def carte(path):
    fig, ax = new_fig(8.0, 5.6)
    ax.add_patch(Rectangle((0, 0), 12, 8, facecolor="#f3f8ee", edgecolor=NEUTRAL, lw=1.4))
    xs = [1, 3, 4.5, 7, 9, 11]
    ys = [1, 2.6, 2.2, 4.8, 5.4, 7]
    ax.plot(xs, ys, lw=3, color=ORANGE, ls="--")
    ax.scatter([xs[0], xs[-1]], [ys[0], ys[-1]], s=80, color=DARK, zorder=5)
    ax.text(xs[0] + 0.2, ys[0] - 0.6, "parking", fontsize=12, color=DARK, fontweight="bold")
    ax.text(xs[-1] - 1.6, ys[-1] + 0.35, "refuge", fontsize=12, color=DARK, fontweight="bold")
    for cx, cy, r in [(6, 2, 1.0), (6, 2, 1.6), (9.6, 2.6, 0.8)]:
        t = np.linspace(0, 2 * np.pi, 80)
        ax.plot(cx + r * np.cos(t), cy + 0.7 * r * np.sin(t), lw=0.8, color="#a0b98a")
    ax.plot([0.6, 4.6], [-0.6, -0.6], lw=3, color=DARK)
    for xx in (0.6, 4.6):
        ax.plot([xx, xx], [-0.8, -0.4], lw=2, color=DARK)
    ax.text(2.6, -1.0, "4 cm", ha="center", va="top", fontsize=11.5, color=DARK)
    ax.text(7.5, -0.8, "Échelle 1 : 25 000", ha="center", va="center", fontsize=12.5, color=DARK,
            fontweight="bold")
    ax.set_xlim(-0.3, 12.3)
    ax.set_ylim(-1.6, 8.3)
    ax.set_aspect("equal")
    ax.axis("off")
    _save(fig, path)


carte(X("proportionnalite_4e_carte.png"))


def photos(path):
    fig, ax = new_fig(9.5, 4.8)
    for x0, w, h, t, col, fc in [(0, 1.0, 1.5, "10 × 15", BLUE, LBLUE),
                                 (2.0, 2.5, 3.75, "25 × 37,5", GREEN, LGREEN),
                                 (5.6, 1.3, 1.8, "13 × 18", ORANGE, LORANGE)]:
        ax.add_patch(Rectangle((x0, 0), w, h, facecolor=fc, edgecolor=col, lw=2))
        ax.text(x0 + w / 2, -0.25, t, ha="center", va="top", fontsize=12, color=col,
                fontweight="bold")
    ax.text(3.25, 4.1, "agrandissement", ha="center", fontsize=11.5, color=GREEN)
    ax.text(6.25, 2.1, "autre format", ha="center", fontsize=11.5, color=ORANGE)
    ax.set_xlim(-0.3, 7.6)
    ax.set_ylim(-0.9, 4.5)
    ax.set_aspect("equal")
    ax.axis("off")
    _save(fig, path)


photos(X("proportionnalite_4e_photos.png"))


def soldes(path):
    fig, ax = new_fig(10.0, 3.2)
    vals = [(100, "prix initial : 100 %", BLUE, LBLUE), (70, "après −30 % : 70 %", ORANGE, LORANGE),
            (56, "après −20 % de plus : 56 %", GREEN, LGREEN)]
    for i, (v, t, col, fc) in enumerate(vals):
        y = -i * 0.9
        ax.add_patch(Rectangle((0, y), v / 10, 0.6, facecolor=fc, edgecolor=col, lw=1.8))
        ax.text(v / 10 + 0.2, y + 0.3, t, va="center", fontsize=12, color=col, fontweight="bold")
    ax.text(0, -2.45, "Réduction totale : 100 % − 56 % = 44 % (et non 50 %)", fontsize=12.5,
            color=PURP, fontweight="bold")
    ax.set_xlim(-0.2, 16)
    ax.set_ylim(-2.8, 0.8)
    ax.axis("off")
    _save(fig, path)


soldes(X("proportionnalite_4e_soldes_solution.png"))
