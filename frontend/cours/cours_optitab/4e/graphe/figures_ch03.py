# -*- coding: utf-8 -*-
"""Figures du chapitre 3 (puissances et notation scientifique) — 4ème OptiTAB."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fig4e import (new_fig, _save, tableau, BLUE, ORANGE, GREEN, DARK, NEUTRAL,
                   DIR_COURS, DIR_EXOS)
import numpy as np
from matplotlib.patches import Rectangle, Circle, FancyArrowPatch

C = lambda f: os.path.join(DIR_COURS, f)  # noqa: E731
X = lambda f: os.path.join(DIR_EXOS, f)   # noqa: E731
LBLUE, LORANGE, LGREEN = "#d6eafc", "#fdebd0", "#e8f5e9"


# ------------------------------------------------------------------ déplacement de la virgule
def virgule(path):
    fig, ax = new_fig(10.0, 3.6)
    def ligne(y, avant, apres, n, txt, col):
        ax.text(0.2, y, avant, fontsize=19, color=DARK, va="center", family="DejaVu Sans Mono")
        ax.text(5.3, y, apres, fontsize=19, color=col, va="center", family="DejaVu Sans Mono",
                fontweight="bold")
        ax.add_patch(FancyArrowPatch((3.4, y), (5.0, y), arrowstyle="-|>", mutation_scale=18,
                                     lw=2, color=col))
        ax.text(4.2, y + 0.38, txt, fontsize=12, color=col, ha="center", fontweight="bold")
    ligne(2.2, "3,45 × 10²", "345", 2, "virgule : 2 rangs à droite", BLUE)
    ligne(0.8, "3,45 × 10⁻²", "0,0345", -2, "virgule : 2 rangs à gauche", ORANGE)
    ax.set_xlim(0, 8.6)
    ax.set_ylim(0.2, 2.9)
    ax.axis("off")
    _save(fig, path)


virgule(C("puissances_4e_virgule.png"))

PREF = [["Préfixe", "Symbole", "Puissance de 10", "Exemple"],
        ["giga", "G", "$10^{9}$", "1 Go = $10^{9}$ octets"],
        ["méga", "M", "$10^{6}$", "1 MW = $10^{6}$ W"],
        ["kilo", "k", "$10^{3}$", "1 km = $10^{3}$ m"],
        ["(unité)", "", "$10^{0} = 1$", "1 m"],
        ["milli", "m", "$10^{-3}$", "1 mm = $10^{-3}$ m"],
        ["micro", "µ", "$10^{-6}$", "1 µm = $10^{-6}$ m"],
        ["nano", "n", "$10^{-9}$", "1 nm = $10^{-9}$ m"]]
tableau(C("puissances_4e_prefixes.png"), PREF, larg_col=[2.0, 1.7, 2.6, 3.6], entete_lig=False)
PREF_EX = [r[:3] for r in PREF]
PREF_EX_TROU = [PREF_EX[0]] + [[r[0], r[1], "?" if i in (1, 3, 5, 6) else r[2]]
                                for i, r in enumerate(PREF_EX[1:], 1)]
tableau(X("puissances_4e_prefixes_trous.png"), PREF_EX_TROU, larg_col=[2.0, 1.7, 2.6],
        entete_lig=False, surligne=[(i, 2) for i in (1, 3, 5, 6)])
tableau(X("puissances_4e_prefixes_solution.png"), PREF_EX, larg_col=[2.0, 1.7, 2.6],
        entete_lig=False, vert=[(i, 2) for i in (1, 3, 5, 6)])


# ------------------------------------------------------------------ échelle des tailles
def echelle(path, objets, lo=-11, hi=12, titre=None, place=True, h=3.4):
    fig, ax = new_fig(11.0, h)
    ax.annotate("", xy=(hi + 0.6, 0), xytext=(lo - 0.4, 0),
                arrowprops=dict(arrowstyle="->", lw=1.6, color=NEUTRAL))
    for k in range(lo, hi + 1):
        ax.plot([k, k], [-0.12, 0.12], lw=1.2, color=NEUTRAL)
        if k % 2 == 0 or (hi - lo) < 14:
            ax.text(k, -0.3, f"$10^{{{k}}}$", ha="center", va="top", fontsize=11.5, color=DARK)
    ax.text(hi + 0.7, -0.3, "m", fontsize=12, color=DARK, va="top")
    for i, (nom, e, col) in enumerate(objets):
        up = i % 2 == 0
        y = 0.75 if up else 1.55
        if place:
            ax.scatter([e], [0], s=60, color=col, zorder=5)
            ax.plot([e, e], [0.1, y - 0.15], lw=1, color=col)
        ax.text(e, y, nom, ha="center", va="bottom", fontsize=11.5, color=col, fontweight="bold")
    if titre:
        ax.text((lo + hi) / 2, 2.55, titre, ha="center", fontsize=13, color=DARK, fontweight="bold")
    ax.set_xlim(lo - 0.8, hi + 1.2)
    ax.set_ylim(-1.0, 2.9 if titre else 2.3)
    ax.axis("off")
    _save(fig, path)


echelle(C("puissances_4e_echelle.png"),
        [("atome", -10, ORANGE), ("virus", -7, ORANGE), ("cellule", -5, ORANGE),
         ("fourmi", -3, BLUE), ("humain", 0, BLUE), ("tour Eiffel", 2, BLUE),
         ("Terre", 7, GREEN), ("Terre–Soleil", 11, GREEN)],
        titre="Ordres de grandeur des longueurs (échelle des puissances de 10)")
echelle(X("puissances_4e_micro_solution.png"),
        [("atome d'hydrogène\n$1 \\times 10^{-10}$ m", -10, ORANGE),
         ("virus de la grippe\n$1{,}2 \\times 10^{-7}$ m", -6.92, BLUE),
         ("globule rouge\n$7 \\times 10^{-6}$ m", -5.15, GREEN),
         ("cheveu (épaisseur)\n$8 \\times 10^{-5}$ m", -4.1, DARK)],
        lo=-11, hi=-2, h=3.6)


# ------------------------------------------------------------------ pliage
def pliage(path):
    fig, ax = new_fig(10.0, 3.6)
    for k in range(4):
        x0 = k * 2.6
        n = 2 ** k
        for j in range(n):
            ax.add_patch(Rectangle((x0, j * 0.16), 1.8, 0.13,
                                   facecolor=LBLUE if j % 2 else "white", edgecolor=BLUE,
                                   lw=1))
        ax.text(x0 + 0.9, -0.45, f"{k} pli" + ("s" if k > 1 else ""), ha="center", fontsize=12,
                color=DARK)
        ax.text(x0 + 0.9, n * 0.16 + 0.25, f"{n} couche" + ("s" if n > 1 else ""),
                ha="center", fontsize=12, color=ORANGE, fontweight="bold")
    ax.set_xlim(-0.3, 10.0)
    ax.set_ylim(-0.8, 2.0)
    ax.set_aspect("equal")
    ax.axis("off")
    _save(fig, path)


pliage(X("puissances_4e_pliage.png"))


# ------------------------------------------------------------------ échiquier
def echiquier(path):
    fig, ax = new_fig(6.4, 6.4)
    for i in range(8):
        for j in range(8):
            ax.add_patch(Rectangle((j, 7 - i), 1, 1, facecolor="#f0d9b5" if (i + j) % 2 == 0
                                   else "#b58863", edgecolor="none"))
    vals = ["1", "2", "4", "8", "16", "32", "64", "128", "256", "512", "1024"]
    for k, v in enumerate(vals):
        i, j = k // 8, k % 8
        ax.text(j + 0.5, 7 - i + 0.5, v, ha="center", va="center", fontsize=12 if len(v) < 4 else 10,
                color=DARK, fontweight="bold")
    ax.text(3 + 0.5, 6 + 0.5, "…", ha="center", va="center", fontsize=16, color=DARK)
    ax.text(7.5, 0.5, "?", ha="center", va="center", fontsize=18, color=ORANGE, fontweight="bold")
    ax.add_patch(Rectangle((0, 0), 8, 8, facecolor="none", edgecolor=DARK, lw=2))
    ax.set_xlim(-0.1, 8.1)
    ax.set_ylim(-0.1, 8.1)
    ax.set_aspect("equal")
    ax.axis("off")
    _save(fig, path)


echiquier(X("puissances_4e_echiquier.png"))

tableau(X("puissances_4e_systeme_solaire.png"),
        [["Donnée", "Valeur"],
         ["Vitesse de la lumière", "$3 \\times 10^{5}$ km/s"],
         ["Distance Terre – Lune", "$3{,}84 \\times 10^{5}$ km"],
         ["Distance Terre – Soleil", "$1{,}5 \\times 10^{8}$ km"],
         ["Distance Soleil – Neptune", "$4{,}5 \\times 10^{9}$ km"],
         ["Durée d'une année", "$3{,}15 \\times 10^{7}$ s"]],
        larg_col=[4.4, 3.6], entete_lig=False)


# ------------------------------------------------------------------ satellite
def satellite(path):
    fig, ax = new_fig(7.0, 7.0)
    R, h = 1.0, 5.6
    ax.add_patch(Circle((0, 0), R, facecolor=LBLUE, edgecolor=BLUE, lw=2))
    ax.add_patch(Circle((0, 0), R + h, facecolor="none", edgecolor=ORANGE, lw=1.6, ls="--"))
    ax.plot([0, 0], [0, R], lw=1.6, color=BLUE)
    ax.text(0.12, R / 2, "$R$", fontsize=13, color=BLUE)
    sx, sy = (R + h) * np.cos(np.radians(60)), (R + h) * np.sin(np.radians(60))
    ex, ey = R * np.cos(np.radians(60)), R * np.sin(np.radians(60))
    ax.plot([ex, sx], [ey, sy], lw=1.6, color=ORANGE)
    ax.add_patch(Rectangle((sx - 0.25, sy - 0.15), 0.5, 0.3, facecolor=DARK))
    ax.plot([sx - 0.6, sx + 0.6], [sy, sy], lw=3, color=BLUE)
    ax.text(-3.4, 3.4, "altitude\n$3{,}6 \\times 10^{4}$ km",
            fontsize=11.5, color=ORANGE, fontweight="bold")
    ax.text(0, -0.35, "Terre", ha="center", fontsize=12, color=BLUE, fontweight="bold")
    ax.text(-1.6, -1.9, "$R = 6{,}4 \\times 10^{3}$ km", fontsize=12, color=BLUE)
    ax.set_xlim(-7, 7)
    ax.set_ylim(-7, 7)
    ax.set_aspect("equal")
    ax.axis("off")
    _save(fig, path)


satellite(X("puissances_4e_satellite.png"))

virgule(X("puissances_4e_virgule_solution.png"))
