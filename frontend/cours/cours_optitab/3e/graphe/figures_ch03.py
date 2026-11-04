# -*- coding: utf-8 -*-
"""Figures du chapitre 3 (Arithmétique) — 3ème OptiTAB."""
import os
import sys
from math import cos, sin, pi

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fig3e import new_fig, finish, BLUE, ORANGE, GREEN, DARK, DIR_COURS, DIR_EXOS
import matplotlib.patches as mp
import numpy as np


def arbre_360():
    """Arbre de décomposition de 360 = 2^3 × 3^2 × 5."""
    fig, ax = new_fig(7.6, 5.4)
    # (x, y, texte, premier?)
    noeuds = {
        "360": (3.2, 5.0, False), "2a": (1.9, 4.0, True), "180": (4.5, 4.0, False),
        "2b": (3.2, 3.0, True), "90": (5.8, 3.0, False),
        "2c": (4.5, 2.0, True), "45": (7.1, 2.0, False),
        "3a": (5.8, 1.0, True), "15": (8.4, 1.0, False),
        "3b": (7.1, 0.0, True), "5": (9.7, 0.0, True),
    }
    aretes = [("360", "2a"), ("360", "180"), ("180", "2b"), ("180", "90"),
              ("90", "2c"), ("90", "45"), ("45", "3a"), ("45", "15"),
              ("15", "3b"), ("15", "5")]
    txt = {"2a": "2", "2b": "2", "2c": "2", "3a": "3", "3b": "3"}
    for a, b in aretes:
        xa, ya, _ = noeuds[a]
        xb, yb, _ = noeuds[b]
        ax.plot([xa, xb], [ya - 0.22, yb + 0.26], lw=1.6, color="0.45", zorder=1)
    for n, (x, y, premier) in noeuds.items():
        label = txt.get(n, n)
        col = ORANGE if premier else BLUE
        ax.add_patch(mp.FancyBboxPatch((x - 0.52, y - 0.26), 1.04, 0.54,
                     boxstyle="round,pad=0.06", facecolor="white",
                     edgecolor=col, lw=2.0, zorder=2))
        ax.text(x, y, label, fontsize=14, ha="center", va="center",
                color=col, fontweight="bold", zorder=3)
    ax.text(5.6, -1.1, r"$360 = 2^3 \times 3^2 \times 5$", fontsize=16,
            ha="center", color=GREEN, fontweight="bold")
    ax.text(2.2, 0.1, "facteurs premiers", fontsize=11, color=ORANGE,
            style="italic", ha="center")
    finish(fig, ax, os.path.join(DIR_COURS, "arithmetique_3e_arbre.png"),
           [(0.6, -1.5), (10.4, 5.5)], margin=0.3, equal=False)


def dallage():
    """Rectangle 180 × 252 dallé en carrés de 36 (5 × 7)."""
    fig, ax = new_fig(8.2, 5.4)
    L, H = 7.0, 5.0  # 7 colonnes × 5 rangées
    for i in range(7):
        for j in range(5):
            ax.add_patch(mp.Rectangle((i, j), 1, 1, facecolor="#e8f4fd" if (i + j) % 2 else "#d6eafc",
                                      edgecolor=BLUE, lw=1.2, zorder=2))
    ax.add_patch(mp.Rectangle((0, 0), L, H, fill=False, edgecolor=DARK, lw=2.4, zorder=3))
    ax.annotate("", xy=(L, -0.45), xytext=(0, -0.45),
                arrowprops=dict(arrowstyle="<->", lw=1.5, color=DARK))
    ax.text(L / 2, -0.85, "252 cm", fontsize=13, ha="center", color=DARK)
    ax.annotate("", xy=(-0.45, H), xytext=(-0.45, 0),
                arrowprops=dict(arrowstyle="<->", lw=1.5, color=DARK))
    ax.text(-0.85, H / 2, "180 cm", fontsize=13, va="center", ha="center",
            color=DARK, rotation=90)
    ax.annotate("", xy=(1, 5.35), xytext=(0, 5.35),
                arrowprops=dict(arrowstyle="<->", lw=1.5, color=ORANGE))
    ax.text(0.5, 5.6, "? cm", fontsize=12.5, ha="center", color=ORANGE,
            fontweight="bold")
    finish(fig, ax, os.path.join(DIR_EXOS, "arithmetique_3e_dallage.png"),
           [(-1.3, -1.2), (L + 0.3, H + 0.9)], margin=0.2)


def engrenages():
    """Deux roues dentées de 24 et 40 dents, marques en contact."""
    fig, ax = new_fig(8.6, 4.6)

    def roue(cx, cy, r, n, color, label):
        t = np.linspace(0, 2 * pi, 200)
        ax.plot(cx + r * np.cos(t), cy + r * np.sin(t), lw=2.2, color=color)
        for k in range(n):
            a = 2 * pi * k / n
            x1, y1 = cx + r * cos(a), cy + r * sin(a)
            x2, y2 = cx + (r + 0.16) * cos(a), cy + (r + 0.16) * sin(a)
            ax.plot([x1, x2], [y1, y2], lw=2.0, color=color, solid_capstyle="round")
        ax.scatter([cx], [cy], s=30, color=color)
        ax.text(cx, cy - r - 0.62, label, fontsize=12.5, ha="center", color=color,
                fontweight="bold")

    r1, r2 = 1.45, 2.4  # proportionnel à 24 et 40
    c1x, c2x = 0.0, r1 + r2 + 0.34
    roue(c1x, 0, r1, 24, BLUE, "24 dents")
    roue(c2x, 0, r2, 40, ORANGE, "40 dents")
    # marques en contact
    ax.scatter([c1x + r1 + 0.08], [0], s=90, color=GREEN, zorder=5)
    ax.scatter([c2x - r2 - 0.08], [0], s=90, color=GREEN, zorder=5)
    ax.text((c1x + r1 + c2x - r2) / 2, 0.45, "dents\nmarquées", fontsize=10.5,
            ha="center", color=GREEN, fontweight="bold")
    finish(fig, ax, os.path.join(DIR_EXOS, "arithmetique_3e_engrenages.png"),
           [(-r1 - 0.8, -r2 - 1.2), (c2x + r2 + 0.8, r2 + 0.6)], margin=0.15)


arbre_360()
dallage()
engrenages()
print("Figures chapitre 3 : OK")
