# -*- coding: utf-8 -*-
"""Figures du chapitre 2 (fractions et nombres premiers) — 4ème OptiTAB."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fig4e import (new_fig, _save, tableau, droite_graduee, BLUE, ORANGE, GREEN, DARK,
                   NEUTRAL, DIR_COURS, DIR_EXOS)
import numpy as np
from matplotlib.patches import Polygon, Wedge, Rectangle, FancyBboxPatch

C = lambda f: os.path.join(DIR_COURS, f)  # noqa: E731
X = lambda f: os.path.join(DIR_EXOS, f)   # noqa: E731
LBLUE, LORANGE, LGREEN = "#d6eafc", "#fdebd0", "#e8f5e9"
PREMIERS = {2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59}


# ------------------------------------------------------------------ crible
def crible(path, n=50, cols=10, solution=True, titre=None):
    rows = (n + cols - 1) // cols
    fig, ax = new_fig(cols * 0.78, rows * 0.78 + (0.6 if titre else 0.1))
    for k in range(1, n + 1):
        i, j = (k - 1) // cols, (k - 1) % cols
        prem = k in PREMIERS
        fc = LGREEN if (solution and prem) else ("#f2f2f2" if (solution and k == 1) else "white")
        ax.add_patch(Rectangle((j, -i), 1, -1, facecolor=fc, edgecolor=BLUE, lw=1.1))
        ax.text(j + 0.5, -i - 0.5, str(k), ha="center", va="center", fontsize=13,
                color=GREEN if (solution and prem) else (NEUTRAL if solution else DARK),
                fontweight="bold" if (solution and prem) else "normal")
        if solution and not prem and k > 1:
            ax.plot([j + 0.2, j + 0.8], [-i - 0.8, -i - 0.2], lw=1.2, color="#b0b7bd")
    if titre:
        ax.text(cols / 2, 0.35, titre, ha="center", fontsize=13, color=DARK, fontweight="bold")
    ax.set_xlim(-0.05, cols + 0.05)
    ax.set_ylim(-rows - 0.05, 0.9 if titre else 0.05)
    ax.set_aspect("equal")
    ax.axis("off")
    _save(fig, path)


crible(C("fractions_4e_crible.png"), 50, titre="Les nombres premiers inférieurs à 50 (en vert)")
crible(X("fractions_4e_crible60.png"), 60, solution=False)
crible(X("fractions_4e_crible60_solution.png"), 60, titre="Les 17 nombres premiers inférieurs à 60")


# ------------------------------------------------------------------ arbres
def arbre(path, n, etapes, vide=False, titre=None):
    """etapes : liste de (nombre composé, facteur premier, quotient) en cascade."""
    fig, ax = new_fig(6.4, 1.15 * len(etapes) + 1.4)
    x, y = 0.0, 0.0
    def boite(x, y, txt, col, fc="white"):
        ax.add_patch(FancyBboxPatch((x - 0.45, y - 0.28), 0.9, 0.56,
                                    boxstyle="round,pad=0.05", facecolor=fc,
                                    edgecolor=col, lw=1.8))
        ax.text(x, y, txt, ha="center", va="center", fontsize=14, color=col,
                fontweight="bold")
    boite(x, y, str(n), BLUE)
    premiers = []
    for k, (comp, p, q) in enumerate(etapes):
        yl = y - 1.15
        ax.plot([x, x - 0.9], [y - 0.32, yl + 0.3], lw=1.6, color=NEUTRAL)
        ax.plot([x, x + 0.9], [y - 0.32, yl + 0.3], lw=1.6, color=NEUTRAL)
        cache = vide and k >= 1
        boite(x - 0.9, yl, "?" if cache else str(p), ORANGE if cache else GREEN,
              LORANGE if cache else LGREEN)
        last = k == len(etapes) - 1
        txtq = "?" if (vide and k >= 1) else str(q)
        if last:
            boite(x + 0.9, yl, txtq, ORANGE if cache else GREEN, LORANGE if cache else LGREEN)
        else:
            boite(x + 0.9, yl, txtq, ORANGE if cache else BLUE, LORANGE if cache else "white")
        premiers.append(p)
        x, y = x + 0.9, yl
    if titre:
        ax.text(x + 1.6, y, titre, ha="left", va="center", fontsize=13.5, color=GREEN,
                fontweight="bold")
    ax.set_xlim(-1.6, x + (6.5 if titre else 1.6))
    ax.set_ylim(y - 0.6, 0.6)
    ax.set_aspect("equal")
    ax.axis("off")
    _save(fig, path)


arbre(C("fractions_4e_arbre84.png"), 84, [(84, 2, 42), (42, 2, 21), (21, 3, 7)],
      titre="$84 = 2 \\times 2 \\times 3 \\times 7$")
arbre(X("fractions_4e_arbre360.png"), 360,
      [(360, 2, 180), (180, 2, 90), (90, 2, 45), (45, 3, 15), (15, 3, 5)], vide=True)
arbre(X("fractions_4e_arbre360_solution.png"), 360,
      [(360, 2, 180), (180, 2, 90), (90, 2, 45), (45, 3, 15), (15, 3, 5)],
      titre="$360 = 2^3 \\times 3^2 \\times 5$")


# ------------------------------------------------------------------ modèles en barres
def barres(path, lignes, w=9.0, titre=None):
    """lignes = [(etiquette, nb_parts, parts_colorees, couleur, sous_div)]"""
    fig, ax = new_fig(w, 0.9 * len(lignes) + (0.5 if titre else 0.2))
    L = 6.0
    for i, (lab, n, k, col, sd) in enumerate(lignes):
        y = -i * 0.9
        ax.text(-0.15, y + 0.3, lab, ha="right", va="center", fontsize=18, color=DARK,
                fontweight="bold")
        for j in range(n):
            fc = {BLUE: LBLUE, ORANGE: LORANGE, GREEN: LGREEN}[col] if j < k else "white"
            ax.add_patch(Rectangle((j * L / n, y), L / n, 0.6, facecolor=fc,
                                   edgecolor=col if j < k else NEUTRAL, lw=1.5))
        if sd:
            for j in range(1, sd):
                ax.plot([j * L / sd] * 2, [y, y + 0.6], lw=0.8, color=NEUTRAL, ls=":")
    if titre:
        ax.text(L / 2, 0.85, titre, ha="center", fontsize=13, color=DARK, fontweight="bold")
    ax.set_xlim(-3.4, L + 0.2)
    ax.set_ylim(-0.9 * (len(lignes) - 1) - 0.2, 1.2 if titre else 0.8)
    ax.set_aspect("equal")
    ax.axis("off")
    _save(fig, path)


barres(C("fractions_4e_somme.png"),
       [("$\\dfrac{1}{2}$", 2, 1, BLUE, 6), ("$\\dfrac{1}{3}$", 3, 1, ORANGE, 6),
        ("$\\dfrac{1}{2}+\\dfrac{1}{3}=\\dfrac{5}{6}$", 6, 5, GREEN, 0)],
       titre="On découpe l'unité en sixièmes : $\\dfrac{3}{6} + \\dfrac{2}{6} = \\dfrac{5}{6}$")
barres(X("fractions_4e_barres.png"),
       [("$\\dfrac{1}{2}$", 2, 1, BLUE, 0), ("$\\dfrac{1}{3}$", 3, 1, ORANGE, 0)])
barres(X("fractions_4e_barres_solution.png"),
       [("$\\dfrac{1}{2} = \\dfrac{3}{6}$", 6, 3, BLUE, 0),
        ("$\\dfrac{1}{3} = \\dfrac{2}{6}$", 6, 2, ORANGE, 0),
        ("total $\\dfrac{5}{6}$", 6, 5, GREEN, 0)])


# ------------------------------------------------------------------ produit par les aires
def aire_produit(path, solution=False, titre=None):
    fig, ax = new_fig(6.6, 5.4)
    W, H = 4.0, 3.0  # colonnes : quarts ; lignes : tiers
    ax.add_patch(Rectangle((0, 0), W, H, facecolor="white", edgecolor=DARK, lw=2))
    ax.add_patch(Rectangle((0, 0), 3, H, facecolor=LBLUE, edgecolor="none"))
    ax.add_patch(Rectangle((0, 0), 3, 2, facecolor="#9fcbef" if solution else "none",
                           edgecolor=ORANGE, lw=2.6, hatch=None if solution else "//"))
    for j in range(1, 4):
        ax.plot([j, j], [0, H], lw=1, color=NEUTRAL, ls="-" if solution else "--")
    for i in range(1, 3):
        ax.plot([0, W], [i, i], lw=1, color=NEUTRAL, ls="-" if solution else "--")
    ax.annotate("", xy=(3, -0.35), xytext=(0, -0.35),
                arrowprops=dict(arrowstyle="<->", lw=1.6, color=BLUE))
    ax.text(1.5, -0.7, "$\\dfrac{3}{4}$ du rectangle", ha="center", fontsize=17, color=BLUE,
            fontweight="bold")
    ax.annotate("", xy=(-0.35, 2), xytext=(-0.35, 0),
                arrowprops=dict(arrowstyle="<->", lw=1.6, color=ORANGE))
    ax.text(-0.5, 1, "$\\dfrac{2}{3}$", ha="right", va="center", fontsize=20, color=ORANGE,
            fontweight="bold")
    if solution:
        ax.text(1.5, 1, "6 cases\nsur 12", ha="center", va="center", fontsize=13, color=GREEN,
                fontweight="bold")
        ax.text(W / 2, H + 0.35, "$\\dfrac{2}{3} \\times \\dfrac{3}{4} = \\dfrac{6}{12} = \\dfrac{1}{2}$",
                ha="center", fontsize=15, color=GREEN, fontweight="bold")
    ax.set_xlim(-1.3, W + 0.3)
    ax.set_ylim(-1.1, H + 0.9)
    ax.set_aspect("equal")
    ax.axis("off")
    _save(fig, path)


aire_produit(C("fractions_4e_produit.png"), solution=True)
aire_produit(X("fractions_4e_aire.png"))
aire_produit(X("fractions_4e_aire_solution.png"), solution=True)


# ------------------------------------------------------------------ gâteau
def gateau(path):
    fig, ax = new_fig(5.6, 5.6)
    parts = [("Léa", 3, BLUE, LBLUE), ("Tom", 4, ORANGE, LORANGE), ("Inès", 2, GREEN, LGREEN),
             ("reste", 3, NEUTRAL, "white")]
    a = 90
    for nom, k, col, fc in parts:
        for j in range(k):
            ax.add_patch(Wedge((0, 0), 2, a - 30, a, facecolor=fc, edgecolor=DARK, lw=1.2))
            a -= 30
        am = np.radians(a + 15 * k)
        ax.text(2.45 * np.cos(am), 2.45 * np.sin(am), f"{nom}\n{k}/12", ha="center",
                va="center", fontsize=12, color=col if col != NEUTRAL else DARK,
                fontweight="bold")
    ax.set_xlim(-3.1, 3.1)
    ax.set_ylim(-3.1, 3.1)
    ax.set_aspect("equal")
    ax.axis("off")
    _save(fig, path)


gateau(X("fractions_4e_gateau_solution.png"))


# ------------------------------------------------------------------ réservoir
def reservoir(path):
    fig, ax = new_fig(4.6, 5.6)
    ax.add_patch(Rectangle((0, 0), 2.4, 5, facecolor="white", edgecolor=DARK, lw=2))
    ax.add_patch(Rectangle((0, 0), 2.4, 3, facecolor=LBLUE, edgecolor="none"))
    for k in range(1, 5):
        ax.plot([2.4, 2.75], [k, k], lw=1.4, color=NEUTRAL)
    ax.text(3.0, 3, "$\\dfrac{3}{5}$", fontsize=15, color=BLUE, va="center", fontweight="bold")
    ax.text(3.0, 5, "plein", fontsize=12, color=DARK, va="center")
    ax.text(1.2, 1.5, "36 L", fontsize=16, color=BLUE, ha="center", fontweight="bold")
    ax.set_xlim(-0.3, 4.2)
    ax.set_ylim(-0.3, 5.4)
    ax.set_aspect("equal")
    ax.axis("off")
    _save(fig, path)


reservoir(X("fractions_4e_reservoir.png"))

# ------------------------------------------------------------------ droite des fractions
def droite_fractions(path):
    fig, ax = new_fig(10.5, 2.6)
    lo, hi = 12, 24  # en 24es
    ax.annotate("", xy=(hi + 0.7, 0), xytext=(lo - 0.5, 0),
                arrowprops=dict(arrowstyle="->", lw=1.6, color=NEUTRAL))
    for k in range(lo, hi + 1):
        big = k in (12, 24)
        ax.plot([k, k], [-0.18 if big else -0.1, 0.18 if big else 0.1], lw=1.6 if big else 1.0,
                color=NEUTRAL)
    ax.text(12, -0.35, "$\\dfrac{1}{2}$", ha="center", va="top", fontsize=20, color=DARK)
    ax.text(24, -0.35, "$1$", ha="center", va="top", fontsize=20, color=DARK)
    pts = [(14, "$\\dfrac{7}{12}$", ORANGE, 1), (15, "$\\dfrac{5}{8}$", BLUE, -1),
           (16, "$\\dfrac{2}{3}$", GREEN, 1), (18, "$\\dfrac{3}{4}$", DARK, -1)]
    for x, lab, col, sgn in pts:
        ax.scatter([x], [0], s=70, color=col, zorder=5)
        ax.text(x, 0.3 if sgn > 0 else -0.35, lab, ha="center", va="bottom" if sgn > 0 else "top",
                fontsize=22, color=col, fontweight="bold")
    ax.text(21.5, 1.0, "une graduation = $\\dfrac{1}{24}$", ha="center", fontsize=15, color=DARK)
    ax.set_xlim(11, 25.2)
    ax.set_ylim(-1.7, 2.1)
    ax.axis("off")
    _save(fig, path)


droite_fractions(X("fractions_4e_droite_solution.png"))


# ------------------------------------------------------------------ budget
def budget(path):
    fig, ax = new_fig(10.0, 3.4)
    parts = [("Logement", "960 €", 16, BLUE, LBLUE), ("Alimentation", "600 €", 10, ORANGE, LORANGE),
             ("Transport", "300 €", 5, DARK, "#e5e8eb"), ("Épargne", "360 €", 6, GREEN, LGREEN),
             ("Loisirs", "180 €", 3, "#8e44ad", "#efe3f5")]
    x = 0
    for i, (nom, mt, k, col, fc) in enumerate(parts):
        ax.add_patch(Rectangle((x, 0), k, 2.2, facecolor=fc, edgecolor=col, lw=1.6))
        ax.text(x + k / 2, 1.1, f"$\\dfrac{{{k}}}{{40}}$", ha="center", va="center", fontsize=15,
                color=col)
        y = -0.6 if i % 2 == 0 else -1.75
        ax.plot([x + k / 2, x + k / 2], [0, y + 0.25], lw=1, color=col)
        ax.text(x + k / 2, y, f"{nom} : {mt}", ha="center", va="top", fontsize=12, color=col,
                fontweight="bold")
        x += k
    ax.set_xlim(-2.5, 42.5)
    ax.set_ylim(-2.6, 2.4)
    ax.axis("off")
    _save(fig, path)


budget(X("fractions_4e_budget_solution.png"))


# ------------------------------------------------------------------ jardin
def jardin(path, solution=False):
    fig, ax = new_fig(7.6, 5.4)
    W, H = 18, 12
    ax.add_patch(Rectangle((0, 0), W, H, facecolor="white", edgecolor=DARK, lw=2))
    if solution:
        # potager 3/8 : bande de 18 x 4,5 ; fleurs 1/4 : 18 x 3 ; pelouse 3/8 : 18 x 4,5
        ax.add_patch(Rectangle((0, 7.5), W, 4.5, facecolor=LORANGE, edgecolor=ORANGE, lw=1.6))
        ax.add_patch(Rectangle((0, 7.5), 6, 4.5, facecolor="#f5b7a1", edgecolor=ORANGE, lw=1.6))
        ax.add_patch(Rectangle((0, 4.5), W, 3, facecolor="#efe3f5", edgecolor="#8e44ad", lw=1.6))
        ax.add_patch(Rectangle((0, 0), W, 4.5, facecolor=LGREEN, edgecolor=GREEN, lw=1.6))
        ax.text(3, 9.75, "tomates\n27 m²", ha="center", va="center", fontsize=11, color="#a04000",
                fontweight="bold")
        ax.text(12, 9.75, "potager : $\\dfrac{3}{8}$ → 81 m²", ha="center", va="center",
                fontsize=12, color=ORANGE, fontweight="bold")
        ax.text(9, 6, "fleurs : $\\dfrac{1}{4}$ → 54 m²", ha="center", va="center", fontsize=12,
                color="#8e44ad", fontweight="bold")
        ax.text(9, 2.25, "pelouse : $\\dfrac{3}{8}$ → 81 m²", ha="center", va="center",
                fontsize=12, color=GREEN, fontweight="bold")
    ax.text(W / 2, -1.0, "18 m", ha="center", fontsize=13, color=DARK)
    ax.text(-0.8, H / 2, "12 m", ha="right", va="center", fontsize=13, color=DARK)
    ax.set_xlim(-3, W + 0.5)
    ax.set_ylim(-2, H + 0.5)
    ax.set_aspect("equal")
    ax.axis("off")
    _save(fig, path)


jardin(X("fractions_4e_jardin.png"))
jardin(X("fractions_4e_jardin_solution.png"), solution=True)


# ------------------------------------------------------------------ piscine
def piscine(path):
    fig, ax = new_fig(8.6, 5.0)
    ax.add_patch(Polygon([(0, 0), (7, 0), (7, 2.4), (0, 2.4)], closed=True, facecolor="white",
                         edgecolor=DARK, lw=2))
    ax.add_patch(Rectangle((0, 0), 7, 1.1, facecolor=LBLUE, edgecolor="none"))
    for x0, nom, t in [(1.2, "A", "remplit seul le\nbassin en 6 h"),
                       (4.6, "B", "remplit seul le\nbassin en 3 h")]:
        ax.add_patch(Rectangle((x0, 2.4), 0.22, 0.75, facecolor=NEUTRAL, edgecolor=DARK))
        ax.add_patch(Rectangle((x0 - 0.6, 2.95), 0.82, 0.22, facecolor=NEUTRAL, edgecolor=DARK))
        ax.text(x0, 3.45, f"robinet {nom}", fontsize=13, color=BLUE, fontweight="bold",
                ha="center")
        ax.text(x0, 4.25, t, fontsize=11, color=DARK, ha="center", va="center")
    ax.add_patch(Rectangle((7, 0.1), 0.8, 0.25, facecolor=NEUTRAL, edgecolor=DARK))
    ax.text(8.0, 0.22, "vidange V :\nvide le bassin\nen 4 h", fontsize=11, color=ORANGE,
            va="center", fontweight="bold")
    ax.set_xlim(-0.3, 10.2)
    ax.set_ylim(-0.4, 4.8)
    ax.set_aspect("equal")
    ax.axis("off")
    _save(fig, path)


piscine(X("fractions_4e_piscine.png"))


# ------------------------------------------------------------------ carrelage
def carrelage(path, solution=False):
    fig, ax = new_fig(7.6, 5.8)
    W, H = 4.2, 3.0
    ax.add_patch(Rectangle((0, 0), W, H, facecolor="white", edgecolor=DARK, lw=2.2))
    if solution:
        for i in range(7):
            for j in range(5):
                ax.add_patch(Rectangle((i * 0.6, j * 0.6), 0.6, 0.6,
                                       facecolor=LGREEN if (i + j) % 2 else "white",
                                       edgecolor=GREEN, lw=1.2))
        ax.text(0.3, 3.25, "60 cm", ha="center", fontsize=11, color=GREEN, fontweight="bold")
        ax.text(W / 2, -0.75, "7 carreaux", ha="center", fontsize=12, color=GREEN,
                fontweight="bold")
        ax.text(W + 0.15, H / 2, "5 carreaux", ha="left", va="center", fontsize=12,
                color=GREEN, fontweight="bold", rotation=90)
    ax.text(W / 2, -0.35, "4,20 m", ha="center", fontsize=13, color=DARK)
    ax.text(-0.25, H / 2, "3 m", ha="right", va="center", fontsize=13, color=DARK)
    ax.set_xlim(-1.0, W + 0.7)
    ax.set_ylim(-1.1, H + 0.5)
    ax.set_aspect("equal")
    ax.axis("off")
    _save(fig, path)


carrelage(X("fractions_4e_piece.png"))
carrelage(X("fractions_4e_piece_solution.png"), solution=True)
